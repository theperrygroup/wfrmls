---
description: Retrieve DataSystem collection and key records, understand get_system_info's ten-record limit, and query modification timestamps.
---

# Data system API reference

`DataSystemClient` requests the `DataSystem` resource. It returns service data-system
records without interpreting version fields, configuring endpoints, or performing
health or compatibility checks.

## Configure access

Use `WFRMLSClient().data_system` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`data_system`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.

## Query data system records

```text
get_data_systems(top=None, skip=None, filter_query=None, select=None,
             orderby=None, expand=None, count=None) -> Dict[str, Any]
```

| Parameter | Accepted value | Default | Request behavior |
| --- | --- | --- | --- |
| `top` | `int` | `None` | Sends `$top`, capped at 200 |
| `skip` | `int` | `None` | Sends `$skip` |
| `filter_query` | `str` | `None` | Sends the OData expression as `$filter` |
| `select` | `list[str]` or `str` | `None` | Sends `$select`; lists become comma-separated strings |
| `orderby` | `str` | `None` | Sends `$orderby` |
| `expand` | `list[str]` or `str` | `None` | Sends `$expand`; lists become comma-separated strings |
| `count` | `bool` | `None` | Sends `$count=true` or `$count=false` when provided |

`None` omits a parameter. The client forwards filters and field names without
checking them against the service schema. Check your service metadata for supported
fields, relationships, and value types. The 200-record cap is applied locally;
negative pagination values are not validated locally.

The method requests `DataSystem` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve a data system by key

`get_data_system(data_system_key: str) -> Dict[str, Any]` requests
`DataSystem('<key>')` and returns one record dictionary. HTTP 404 raises
`NotFoundError`. Use a key returned by the service; a data-system name is not
automatically converted to its key.

## Understand the system-info helper

`get_system_info() -> Dict[str, Any]` is exactly a call to
`get_data_systems(top=10)`. It returns a collection page, including a `value` list
when supplied by the service. It does not identify a preferred or current system,
return the first record directly, or fetch every system.

The method accepts no query arguments. Use `get_data_systems()` to select fields,
filter, order, count, expand, or request another page. `get_service_info()` does not
exist on `DataSystemClient`. For the service document and XML schema, use the
[main client's discovery methods](client.md).

## Read the system-info collection

Set `WFRMLS_BEARER_TOKEN` before running this example. Field names below are used
in repository test fixtures; confirm the schema in your service metadata.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.data_system.get_system_info()
for system in response.get("value", []):
    print(system.get("DataSystemKey"), system.get("DataSystemName"))
```

## Filter and select data-system records

The client forwards field names and filters to the service. This example uses
fields found in the repository's mocked tests; metadata determines whether your
service exposes the same schema.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.data_system.get_data_systems(
    filter_query="DataSystemStatus eq 'Active'",
    select=["DataSystemKey", "DataSystemName", "DataSystemStatus"],
    orderby="DataSystemName asc,DataSystemKey asc",
    top=50,
    count=True,
)
for system in response.get("value", []):
    print(system.get("DataSystemName"), system.get("DataSystemStatus"))
print("Matching systems:", response.get("@odata.count"))
```

## Query modified records

`get_modified_data_systems(since: Union[str, date, datetime], **kwargs)` builds `ModificationTimestamp gt '<timestamp>'`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDT00:00:00Z`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


The modification helper returns a collection response and forwards other
collection options to `get_data_systems()`. It does not maintain a synchronization
cursor or cache the response.

## Interpret data-system metadata

The implementation and tests reference `DataSystemKey`, `DataSystemName`,
`DataSystemStatus`, and `ModificationTimestamp`; tests also exercise expansion
with `Resources`. These are request-building examples, not a guarantee of current
provider fields. Historical documentation used fields such as `DSName`,
`ServiceUri`, and `TransportVersion`; the client does not require, translate, or
derive those fields.

Read the fields your service actually returns. A reported version or modification
timestamp does not establish endpoint health, current resource access, or
compatibility with your application's expected schema. The client provides no
version-comparison logic, endpoint reconfiguration, caching, or health monitor.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Main-client metadata methods](client.md) for service discovery and XML schema.
- [Resource records](resource.md) for resource-level metadata.
- [OData queries](../guides/odata-queries.md) for collection filtering and paging.
