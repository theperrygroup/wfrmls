---
title: "Build OData queries and read every page"
description: "Build WFRMLS OData filters with correct literals, map client parameters to query options, and follow collection next links safely."
---

# Build OData queries and read every page

The service helpers translate Python arguments into OData query options.
They forward query expressions to the provider; they do not validate every
field, expression, or feed entitlement. Configure
[authentication](../getting-started/authentication.md) first and inspect your
service's current metadata when choosing fields and types.

## Map Python arguments to query options

For `client.property.get_properties()`, the supported arguments are:

| Python argument | OData option | Accepted form | Default | Behavior |
| --- | --- | --- | --- | --- |
| `filter_query` | `$filter` | String | Omitted | Forwarded without field/type validation. |
| `select` | `$select` | String or list of strings | Omitted | Lists are joined with commas. |
| `orderby` | `$orderby` | String | Omitted | Supply direction and tie-breaking fields explicitly. |
| `expand` | `$expand` | String or list of strings | Omitted | Support and nested paging depend on the service. |
| `top` | `$top` | Integer | Omitted | Clamped to 200; positive-value validation is application code. |
| `skip` | `$skip` | Integer | Omitted | Forwarded as an offset. |
| `count` | `$count` | Boolean | Omitted | Sent as `true` or `false`; count availability depends on the service. |

OData defines these options in its
[protocol specification](https://docs.oasis-open.org/odata/odata/v4.0/errata03/os/complete/part1-protocol/odata-v4.0-errata03-os-part1-protocol-complete.html).
A provider can restrict supported expressions and resources. `$top` limits
the requested result count; it is not a universal server page-size setting.
Do not set a total-result cap when you intend to replicate every matching row.

## Build filter literals

OData string literals use single quotes. Escape an embedded apostrophe by
doubling it before Requests URL-encodes the query. URL encoding alone does
not make a user-supplied value a valid OData literal. Numeric and Boolean
literals are unquoted; an `Edm.DateTimeOffset` literal is also unquoted.
Enums require the type-qualified form declared by the metadata. See the
[OData URL conventions](https://docs.oasis-open.org/odata/odata/v4.0/errata03/os/complete/part2-url-conventions/odata-v4.0-errata03-os-part2-url-conventions-complete.html).

```python
from wfrmls import WFRMLSClient


def odata_string(value):
    return "'" + value.replace("'", "''") + "'"


client = WFRMLSClient()
response = client.property.get_properties(
    filter_query="City eq " + odata_string("O'Fallon") + " and ListPrice le 500000",
    select=["ListingId", "City", "ListPrice"],
    orderby="ListPrice asc,ListingKeyNumeric asc",
    top=10,
    count=True,
)
print("Records on this page:", len(response["value"]))
print("Provider count, if supplied:", response.get("@odata.count"))
```

Validate field names against an application allowlist rather than interpolating
arbitrary field names or complete expressions from user input. A string-escaping
helper handles values only.

## Express a UTC timestamp window

Use explicit UTC strings when filtering `ModificationTimestamp`. This
example assumes the field is `Edm.DateTimeOffset` in the current schema:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    filter_query=(
        "ModificationTimestamp ge 2026-01-01T00:00:00Z and "
        "ModificationTimestamp lt 2026-01-02T00:00:00Z"
    ),
    orderby="ModificationTimestamp asc,ListingKeyNumeric asc",
    select=["ListingKeyNumeric", "ModificationTimestamp"],
    top=10,
)
print("Records on this page:", len(response["value"]))
```

This is a page of a bounded query, not a complete synchronization. The
`get_modified_properties()` helper uses a strict `gt` lower bound and normalizes
a string by appending `Z`. Pass an already normalized UTC string to that helper;
do not rely on it to convert arbitrary offsets or datetime objects correctly.

## Follow collection next links

OData collections use a `value` array and may include `@odata.nextLink`.
Follow the server's continuation URL without appending new system query
options; it is an opaque continuation token under the
[OData paging rules](https://docs.oasis-open.org/odata/odata/v4.0/errata03/os/complete/part1-protocol/odata-v4.0-errata03-os-part1-protocol-complete.html).
The library does not follow these links automatically.

Save this application helper as `wfrmls_paging.py`. It uses an existing service
session so the token stays in its header, checks each URL before sending it,
rejects redirects, sets connect/read timeouts, validates collection shape,
and propagates every failure. It handles the outer collection only.

```python
from urllib.parse import unquote, urljoin, urlsplit


def iter_collection(session, base_url, resource, params=None, max_pages=10000):
    if max_pages < 1:
        raise ValueError("max_pages must be positive.")
    if not resource.isidentifier():
        raise ValueError("Use a collection resource name, not a URL.")
    base_url = base_url.rstrip("/")
    base = urlsplit(base_url)
    if (
        base.scheme != "https"
        or not base.hostname
        or base.username is not None
        or base.password is not None
        or base.query
        or base.fragment
    ):
        raise ValueError("Use an approved HTTPS service base URL.")
    origin = (base.scheme, base.hostname, base.port or 443)
    prefix = base.path.rstrip("/") + "/"
    url = base_url + "/" + resource
    seen = set()
    pages = 0

    while True:
        target = urlsplit(url)
        path_parts = unquote(target.path).split("/")
        if (
            (target.scheme, target.hostname, target.port or 443) != origin
            or target.username is not None
            or target.password is not None
            or target.fragment
            or not target.path.startswith(prefix)
            or any(part in (".", "..") for part in path_parts)
        ):
            raise ValueError("Continuation URL is outside the approved service.")
        if url in seen or pages >= max_pages:
            raise RuntimeError("Repeated continuation URL or page limit exceeded.")
        seen.add(url)
        response = session.get(
            url, params=params, timeout=(5, 30), allow_redirects=False
        )
        if 300 <= response.status_code < 400:
            raise ValueError("Unexpected redirect; confirm the service URL.")
        response.raise_for_status()
        payload = response.json()
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("value"), list)
            or not all(isinstance(row, dict) for row in payload["value"])
        ):
            raise ValueError("Expected an OData collection with object records.")
        pages += 1
        yield payload["value"]
        link = payload.get("@odata.nextLink")
        if link is None:
            return
        if not isinstance(link, str) or not link:
            raise ValueError("Invalid continuation link.")
        url = urljoin(response.url, link)
        params = None
```

Use it from a script in the same directory:

```python
from wfrmls import WFRMLSClient
from wfrmls_paging import iter_collection

client = WFRMLSClient()
service = client.property
records_read = 0
for records in iter_collection(
    service.session,
    service.base_url,
    "Property",
    params={
        "$select": "ListingKeyNumeric,ListingId",
        "$orderby": "ListingKeyNumeric asc",
    },
):
    records_read += len(records)
print("Records read:", records_read)
```

Because this helper uses Requests directly, transport errors, timeouts, and
bad statuses raise Requests exceptions rather than the library's mapped error
classes. It does not retry. A page limit raises an error rather than reporting
a truncated result as complete. Do not advance a checkpoint if iteration fails.

## Know the completeness limits

The absence of a next link is the protocol's end-of-collection signal; verify
that your provider follows that contract. A changing feed is not necessarily
a stable snapshot, even with deterministic ordering. Use overlap and periodic
reconciliation when replicating data.

`get_all_properties_paginated()` instead increments `$skip` and stops after
any exception, returning accumulated records. It ignores next links and
stores the combined result in memory. Use it only when partial results are
acceptable; its return value cannot prove a complete replication.

See [data synchronization](data-sync.md) for transaction and checkpoint
boundaries, and [property search](property-search.md) for media expansion.
