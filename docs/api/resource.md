---
description: Query resource metadata by key or ResourceName, request Fields expansion, and distinguish service discovery from implemented client accessors.
---

# Resource metadata API reference

`ResourceClient` requests records from the `Resource` metadata collection. It
supports key and name queries, standard-name filtering, field expansion, and
modification queries. Service metadata and the package's client accessors are
separate sources of information.

## Configure access

Use `WFRMLSClient().resource` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`resource`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.

## Query resource records

```text
get_resources(top=None, skip=None, filter_query=None, select=None,
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

The method requests `Resource` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve resource metadata

| Method | Actual request and return value |
| --- | --- |
| `get_resource(resource_key: str) -> Dict[str, Any]` | Requests `Resource('<key>')`; returns one record; HTTP 404 raises `NotFoundError` |
| `get_resource_by_name(resource_name: str, **kwargs)` | Filters `ResourceName eq '<name>'`; returns a collection response |
| `get_standard_resources(**kwargs)` | Filters `StandardName ne null`; returns a collection |
| `get_resources_with_fields(**kwargs)` | Sets `expand="Fields"`; returns a collection |
| `get_modified_resources(since: Union[str, date, datetime], **kwargs)` | Filters `ModificationTimestamp`; timestamp handling is described below |

Collection helpers return `Dict[str, Any]` and forward their `**kwargs` to
`get_resources()`. Name and standard helpers append an extra `filter_query` with
`and`. Parenthesize additional filters containing `or`. Resource names are
interpolated directly; escape apostrophes as doubled quotes in OData string literals.

Do not pass `expand` to `get_resources_with_fields()` because the helper already
sets it; duplicate arguments raise `TypeError`. To request other relationships,
use `get_resources(expand=...)` directly.

## Inspect metadata for a named resource

Set `WFRMLS_BEARER_TOKEN` before running this example. A name query returns a
collection, including an empty collection when there are no matches. It does not
select a single record or raise `NotFoundError` for an empty result.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.resource.get_resource_by_name(
    "Property",
    expand="Fields",
    top=10,
)
for resource in response.get("value", []):
    print(resource.get("ResourceKey"), resource.get("ResourceName"))
    print("Fields:", resource.get("Fields"))
```

## Retrieve standard-named resources

This example retrieves one page with a non-null `StandardName`. That filter does
not prove standards compliance or guarantee that the resource is accessible.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.resource.get_standard_resources(
    select=["ResourceKey", "ResourceName", "StandardName"],
    orderby="ResourceName asc,ResourceKey asc",
    top=200,
)
for resource in response.get("value", []):
    print(resource.get("ResourceName"), resource.get("StandardName"))
```

## Query modified records

`get_modified_resources(since, **kwargs)` builds `ModificationTimestamp gt '<timestamp>'`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDT00:00:00Z`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


## Distinguish metadata from client support

Client queries and tests use `ResourceKey`, `ResourceName`, `StandardName`,
`ModificationTimestamp`, and the `Fields` relationship. The client does not rename
these fields to historical aliases such as `RName`. If your service returns another
schema, inspect its metadata and build an explicit query for that schema.

A `Resource` record is not a complete guarantee of request permissions, service
health, or package support. Do not invent Python method names from resource names.
For example, this release has no `client.media`, `client.history`, or
`client.green_verification` accessor. Their presence in provider metadata would not
create those accessors.

Use [main-client discovery](client.md) for `get_service_document()` and
`get_metadata()`. The service document lists advertised entity sets; XML metadata
describes fields and relationships. `ResourceClient` neither parses that XML nor
creates dynamic client methods.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Main client](client.md) for implemented accessors and metadata discovery.
- [Lookup values](lookup.md) for field categories and enumerations.
- [Data systems](data-system.md) for data-system records.
