---
description: Query Deleted records with exact resource and timestamp filters, legacy method aliases, and limits of aggregation, summaries, and monitoring helpers.
---

# Deleted records API

`DeletedClient` reads deletion records from the `Deleted` resource.
It can help identify removed records, but it does not delete local data, restore records, or implement a complete synchronization workflow.

## Configure the client

```text
DeletedClient(bearer_token=None, base_url=None)
```

The service constructor accepts a bearer token or reads `WFRMLS_BEARER_TOKEN`.
The default base URL is `https://resoapi.utahrealestate.com/reso/odata`.
Direct construction requires credentials immediately. `WFRMLSClient` initializes it lazily and checks credentials when `.deleted` is first accessed.

Examples require a configured `WFRMLS_BEARER_TOKEN`.
Check [service discovery](client.md) for the schema available to your account.
The helpers and mocked tests use `ResourceName`, `ResourceRecordKey`, and `DeletedDateTime`.
The library does not rename server fields such as `resource`, `primary_key`, or `ts`; those names cannot be substituted in helper results automatically.

## Query one page of deletion records

```text
get_deleted(top=None, skip=None, filter_query=None, select=None,
            orderby=None, expand=None, count=None) -> Dict[str, Any]
```

| Parameter | Accepted type | Request behavior |
| --- | --- | --- |
| `top` | `int` or `None` | Sends `$top=min(top, 200)` when provided. |
| `skip` | `int` or `None` | Sends `$skip` unchanged. |
| `filter_query` | `str` or `None` | Sends the expression as `$filter`. |
| `select` | `list[str]`, `str`, or `None` | Joins lists with commas for `$select`. |
| `orderby` | `str` or `None` | Sends `$orderby` unchanged. |
| `expand` | `list[str]`, `str`, or `None` | Joins lists with commas for `$expand`. |
| `count` | `bool` or `None` | Sends `$count=true` or `$count=false`; `None` omits it. |

Query expressions are not validated locally. The server determines supported fields, relationships, and operators.
The method returns the server's JSON dictionary unchanged, usually with a `value` list.
OData metadata such as `@odata.count` or `@odata.nextLink` is present only when the server supplies it.
No method on this page follows pagination links automatically.

## Filter by timestamp and resource

```text
get_deleted_by_resource(resource_name: Union[ResourceName, str], **kwargs) -> Dict[str, Any]
get_deleted_since(since: Union[str, date], resource_name=None, **kwargs) -> Dict[str, Any]
```

`get_deleted_by_resource()` adds `ResourceName eq '<resource_name>'`.
It accepts a `ResourceName` enum member or a string and unwraps enum values.

`get_deleted_since()` adds `DeletedDateTime gt <since>` without quotes around the timestamp.
An optional `resource_name` adds the same resource filter.
Both helpers append a supplied `filter_query` with `and` and forward the remaining query keywords to `get_deleted()`.
Parenthesize a custom expression containing `or` if it should apply as a group.
Resource strings are interpolated without escaping; use trusted values.

```python
from datetime import datetime, timedelta, timezone

from wfrmls import ResourceName, WFRMLSClient

client = WFRMLSClient()
cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
cutoff_utc = cutoff.isoformat().replace("+00:00", "Z")
response = client.deleted.get_deleted_since(
    since=cutoff_utc,
    resource_name=ResourceName.PROPERTY,
    top=200,
    select=["ResourceName", "ResourceRecordKey", "DeletedDateTime"],
    orderby="DeletedDateTime asc",
)

for record in response.get("value", []):
    print(record.get("ResourceName"), record.get("ResourceRecordKey"))
if response.get("@odata.nextLink"):
    print("Additional pages remain; this response is not a complete sync.")
```

A string timestamp is used unchanged. A `date` becomes `YYYY-MM-DDZ`, without a midnight time component.
Although `datetime` is a subclass of `date`, it is not a declared input type for these deletion helpers.
It would become `isoformat() + "Z"`, without time-zone conversion.
Use a full normalized UTC timestamp string, as above, to avoid ambiguous dates or offset-plus-`Z` combinations.

### Resource constants and aliases

`ResourceName` provides these filter constants:

| Member | Value |
| --- | --- |
| `PROPERTY` | `Property` |
| `MEMBER` | `Member` |
| `OFFICE` | `Office` |
| `OPENHOUSE` | `OpenHouse` |
| `MEDIA` | `Media` |
| `HISTORY_TRANSACTIONAL` | `HistoryTransactional` |
| `PROPERTY_GREEN_VERIFICATION` | `PropertyGreenVerification` |
| `PROPERTY_UNIT_TYPES` | `PropertyUnitTypes` |
| `ADU` | `Adu` |

Constants describe filter strings, not proof that a corresponding resource is available.
The main client has no media, history, or green verification accessors. Standalone classes exist, but their presence does not verify provider availability.
Filtering deletion records does not establish access to those resources.

Each convenience method below accepts `**kwargs` for `get_deleted()` and returns one deletion page:

| Method | Resource filter | Legacy alias |
| --- | --- | --- |
| `get_deleted_property_records(**kwargs)` | `Property` | `get_deleted_properties(**kwargs)` |
| `get_deleted_member_records(**kwargs)` | `Member` | `get_deleted_members(**kwargs)` |
| `get_deleted_office_records(**kwargs)` | `Office` | `get_deleted_offices(**kwargs)` |
| `get_deleted_media_records(**kwargs)` | `Media` | None |
| `get_deleted_open_houses(**kwargs)` | `OpenHouse` | This is the implemented method name. |

There are no `get_recent_deletions()` or `get_deletions_by_resource()` methods.
Use `get_deleted_since()` and `get_deleted_by_resource()` respectively.

## Aggregate pages across resource types

```text
get_all_deleted_for_sync(since: Union[str, date], resource_types=None,
                         **kwargs) -> Dict[str, Any]
```

`resource_types` accepts a list of enum members or strings.
When omitted, the helper queries `Property`, `Member`, `Office`, `Media`, and `OpenHouse` in that order.
It calls `get_deleted_since()` once per resource and concatenates only those returned pages.
An empty list makes no requests. Pass query options such as `top` or `select`; do not pass `resource_name`, which the helper supplies itself.

| Return key | Contents |
| --- | --- |
| `@odata.context` | Literal string `Comprehensive deletion sync`. |
| `value` | Concatenated records from successful pages. |
| `by_resource` | Resource name mapped to records from its page. |
| `sync_info.total_deleted_records` | Number of concatenated records, not a provider total. |
| `sync_info.resource_types_checked` | Length of the requested resource list. |
| `sync_info.since_timestamp` | Supplied or converted timestamp string. |
| `sync_info.resources_with_deletions` | Number of nonempty entries in `by_resource`. |

!!! warning "Aggregation does not establish sync completion"
    This helper catches every per-resource exception and records an empty list without an error indicator.
    It discards pagination and count metadata. An empty result may mean a request failed, and successful results may have more pages.
    For a sync that must detect failures, call `get_deleted_since()` for each resource, handle exceptions, and account for all pages before advancing your checkpoint.

## Summarize one deletion page

```text
get_deletion_summary(since: Union[str, date], **kwargs) -> Dict[str, Any]
```

This calls `get_deleted_since()` once and builds a dictionary with `@odata.context="Deletion summary"`, the page's `value`, and a `summary` dictionary:

- `total_deletions`: Number of records in that page.
- `resource_types_affected`: Number of resource names represented.
- `by_resource_count`: Counts grouped by `ResourceName`, defaulting to `Unknown` when missing.
- `by_resource_latest`: Greatest `DeletedDateTime` string per resource; timestamps are compared as strings without parsing.
- `analysis_period`: The cutoff and `analysis_timestamp`, generated as the local calendar date followed by `Z`.

The summary does not include pagination metadata or a full timestamp for `analysis_timestamp`.
It is not a total across the provider's result set.

```python
from wfrmls import ResourceName, WFRMLSClient

client = WFRMLSClient()
result = client.deleted.get_deletion_summary(
    since="2024-01-01T00:00:00Z",
    resource_name=ResourceName.PROPERTY,
    top=200,
    select=["ResourceName", "ResourceRecordKey", "DeletedDateTime"],
)

print("Records in this page:", result["summary"]["total_deletions"])
for resource, count in result["summary"]["by_resource_count"].items():
    print(resource, count)
```

## Understand the monitoring helper

```text
monitor_deletion_activity(hours_back: int = 24, alert_threshold: int = 100,
                          **kwargs) -> Dict[str, Any]
```

This synchronous method computes a cutoff and summarizes one page. It does not schedule monitoring or send notifications.
The return keys are `@odata.context`, `monitoring_period`, `summary`, `alerts`, `recommendations`, `status`, and `monitoring_timestamp`.
`status` is `ALERT` when any alert string exists, otherwise `NORMAL`.

A total greater than `alert_threshold` generates an alert.
Each resource count is also compared with `alert_threshold // number_of_resource_types`; equality alone does not trigger that comparison.
Recommendations are strings for the caller to interpret and do not execute cleanup.

The current implementation appends `Z` to timezone-aware ISO timestamps, producing an offset-plus-`Z` cutoff and `monitoring_timestamp`.
The provider may reject the generated cutoff. For an explicit valid cutoff, use `get_deletion_summary()` with a normalized UTC string instead.

## Handle request failures

Except for the aggregation helper's suppressed exceptions, failures propagate through the shared HTTP client.
HTTP 400, 401, 404, 429, and 5xx responses raise `ValidationError`, `AuthenticationError`, `NotFoundError`, `RateLimitError`, and `ServerError` respectively.
Request exceptions raise `NetworkError`; other unsuccessful statuses raise `WFRMLSError`.
The client provides no automatic retries, deletion-retention guarantee, or record-recovery method.

See [error handling](../guides/error-handling.md) and the [main client reference](client.md).
