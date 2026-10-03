---
title: "Synchronize WFRMLS data safely"
description: "Plan WFRMLS baseline and incremental replication, stage timestamp-window updates, commit checkpoints safely, and verify deletion-feed contracts."
---

# Synchronize WFRMLS data safely

The library exposes queries, not a replication engine. Your application owns
storage, paging, checkpoints, scheduling, deletion reconciliation, and recovery.
Configure [authentication](../getting-started/authentication.md), confirm your
licensed feed scope, and review the [paging helper](odata-queries.md#follow-collection-next-links)
before persisting records.

## Establish a baseline and a definition of success

For an initial load, exhaust the permitted source collection, validate its keys
and required fields, and stage the results before replacing or publishing a
dataset. Record the feed's resource, filters, selected fields, account scope,
and a UTC checkpoint. A count from one page is not a baseline audit.

A successful run means every required page was fetched, every required write
committed, and the checkpoint was persisted with those writes. If a request,
validation, or storage operation fails, leave the checkpoint unchanged and
report the failure. Do not replace failures with empty lists.

`get_all_properties_paginated()` suppresses page exceptions and returns partial
records. `get_all_deleted_for_sync()` fetches one page per resource and substitutes
an empty list after an exception. Neither helper proves a complete sync.

## Query an overlapping UTC window

For incremental property updates, choose an upper boundary before fetching
pages. Query from a little before the previous checkpoint through that boundary,
using an inclusive lower bound and an exclusive upper bound. Upsert by a stable
key so repeated records are harmless. A strict `gt` cursor can miss records
that share a boundary timestamp if the preceding run was incomplete.

An overlap is an application recovery choice, not a guarantee against all late
or backdated changes. Size it using observed/provider-supported behavior and
retain a periodic audit. RESO recommends `ModificationTimestamp` for replication
and explains why deleted or disappearing records need additional reconciliation.
[RESO data FAQ](https://www.reso.org/knowledge-base/data-topics-faq/)

## Commit property updates and the checkpoint together

This example updates a local SQLite cache after a **previously completed and
audited baseline**. It handles property updates only; it does not delete rows
or establish display eligibility. Save the paging helper from the
[OData guide](odata-queries.md#follow-collection-next-links) as `wfrmls_paging.py`,
then save this block as `property_sync.py` in the same directory.

The baseline process must populate the cache and its `Property` checkpoint in
the schema below. `sync_property_window()` refuses to invent a missing baseline.
Use a dedicated SQLite connection, with no pending transaction.

```python
import json
from datetime import datetime, timedelta, timezone

from wfrmls_paging import iter_collection


def utc_time(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("A checkpoint must include a timezone.")
    return parsed.astimezone(timezone.utc)


def utc_literal(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Use an aware datetime.")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def initialize_schema(connection):
    with connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS property_cache "
            "(listing_key INTEGER PRIMARY KEY, payload TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS sync_state "
            "(stream TEXT PRIMARY KEY, watermark TEXT NOT NULL)"
        )


def sync_property_window(client, connection, upper, overlap=timedelta(minutes=5)):
    if connection.in_transaction:
        raise ValueError("Use a connection without a pending transaction.")
    row = connection.execute(
        "SELECT watermark FROM sync_state WHERE stream = ?", ("Property",)
    ).fetchone()
    if row is None:
        raise RuntimeError("Complete and audit the baseline before this step.")
    previous = row[0]
    checkpoint = utc_time(previous)
    upper_literal = utc_literal(upper)
    upper = utc_time(upper_literal)
    if upper <= checkpoint or overlap < timedelta(0):
        raise ValueError("Advance the checkpoint and use a nonnegative overlap.")
    lower = checkpoint - overlap
    service = client.property
    staged = {}
    for records in iter_collection(
        service.session,
        service.base_url,
        "Property",
        params={
            "$filter": (
                "ModificationTimestamp ge "
                + utc_literal(lower)
                + " and ModificationTimestamp lt "
                + upper_literal
            ),
            "$orderby": "ModificationTimestamp asc,ListingKeyNumeric asc",
        },
    ):
        for record in records:
            key = record["ListingKeyNumeric"]
            modified = utc_time(record["ModificationTimestamp"])
            if isinstance(key, bool) or not isinstance(key, int):
                raise ValueError("Expected a numeric property key.")
            if not lower <= modified < upper:
                raise ValueError("Record lies outside the requested window.")
            staged[key] = json.dumps(record)

    with connection:
        connection.execute("BEGIN IMMEDIATE")
        current = connection.execute(
            "SELECT watermark FROM sync_state WHERE stream = ?", ("Property",)
        ).fetchone()
        if current != (previous,):
            raise RuntimeError(
                "Another run advanced this stream; retry from its state."
            )
        for key, payload in staged.items():
            connection.execute(
                "INSERT INTO property_cache(listing_key, payload) VALUES (?, ?) "
                "ON CONFLICT(listing_key) DO UPDATE SET payload = excluded.payload",
                (key, payload),
            )
        connection.execute(
            "UPDATE sync_state SET watermark = ? WHERE stream = ?",
            (upper_literal, "Property"),
        )
    return len(staged)
```

Call `initialize_schema(connection)` when creating your dedicated database.
After the baseline, call `sync_property_window(client, connection, upper)` with
an aware datetime captured at run start, such as `datetime.now(timezone.utc)`.
The sample retains the fetched window in memory; use durable staging for large
windows. SQLite must support `ON CONFLICT ... DO UPDATE` (SQLite 3.24 or later).

No write occurs until paging and validation finish. Writes and checkpoint
changes share one transaction; failures roll it back. A competing checkpoint
change is detected before applying the staged data. This still does not create
a provider snapshot or prevent every visibility race. Audit the full permitted
key set periodically and repeat windows idempotently.

## Verify deletion schemas before applying tombstones

The repository contains conflicting deletion field conventions:

| Source | Resource field | Record key | Deletion timestamp |
| --- | --- | --- | --- |
| Implemented `DeletedClient` helpers/tests | `ResourceName` | `ResourceRecordKey` in fixtures | `DeletedDateTime` |
| Copied provider replication examples | `resource` | `primary_key` | `ts` |

These are repository observations, not a verified current provider contract.
The copied examples are visible in the
[repository replication document](https://github.com/theperrygroup/wfrmls/blob/master/api_docs/replication.md).
Confirm resource availability, actual field names/types, key mapping, retention,
and licensed scope with current metadata and provider instructions before
filtering or deleting local records. The library's convenience methods do not
translate between the two schemas.

Once the contract is verified, page the entire deletion window, stage its
tombstones, and atomically commit removals with that stream's checkpoint.
Keep property and deletion checkpoints separate unless both streams are
successfully committed as a single unit. A deletion-feed failure must not be
reported as a completed full replication.

## Reconcile records that disappear from your view

A record can leave a filtered or licensed feed without appearing as a physical
deletion. A missing result might reflect status, seller restrictions, account
access, or changed filters. Compare against a completed source-key audit under
the same scope and investigate access changes before pruning local records.
Follow the provider agreement when withdrawing records from display.

Track run boundaries, page/write counts, and sanitized failures. Choose the
schedule from your agreement and workload; this package implements no scheduler
or universal polling interval. See [rate limits](rate-limits.md) and
[data licensing](../legal/index.md).
