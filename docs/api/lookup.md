---
description: Retrieve MLS lookup categories and values, distinguish standard and active filters, and understand LookupClient paging and name results.
---

# Lookup API reference

`LookupClient` requests the `Lookup` resource for service-defined categories and
values. Use returned records and metadata to build field options; the package does
not ship a verified, exhaustive catalog of current provider categories.

## Configure access

Use `WFRMLSClient().lookup` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`lookup`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.

## Query lookup records

```text
get_lookups(top=None, skip=None, filter_query=None, select=None,
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

The method requests `Lookup` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve lookup records

| Method | Actual request and result |
| --- | --- |
| `get_lookup(lookup_key: str) -> Dict[str, Any]` | Requests `Lookup('<key>')`; returns one record; HTTP 404 raises `NotFoundError` |
| `get_lookups_by_name(lookup_name: str, **kwargs)` | Filters `LookupName eq '<name>'`; returns a collection |
| `get_property_type_lookups(**kwargs)` | Calls the name helper with `PropertyType` |
| `get_property_status_lookups(**kwargs)` | Calls the name helper with `PropertyStatus` |
| `get_standard_lookups(**kwargs)` | Filters `StandardLookupValue ne null` |
| `get_active_lookups(**kwargs)` | Filters `IsActive eq true` |
| `get_lookup_names() -> Dict[str, Any]` | Requests `select=["LookupName"]` and `orderby="LookupName asc"`; returns a collection page |
| `get_modified_lookups(since: Union[str, date, datetime], **kwargs)` | Filters `ModificationTimestamp`; timestamp handling is described below |

All collection helpers return `Dict[str, Any]`. Helpers accepting `**kwargs`
forward the collection options from `get_lookups()`. The name, standard, and active
helpers combine an extra `filter_query` with `and`; parenthesize expressions that
contain `or`. Lookup names are interpolated directly, so escape apostrophes as
doubled quotes in OData string literals.

The status helper uses the literal category **`PropertyStatus`**. It does not query
`StandardStatus` or `MlsStatus`. Use `get_lookups_by_name()` with a category returned
by your service when you need those categories.

## Retrieve values for a category

Set `WFRMLS_BEARER_TOKEN` before running this example. `PropertyType` is the
category used by the built-in helper; confirm its fields and values in metadata.
The example retrieves one page, not every category value automatically.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.lookup.get_property_type_lookups(
    select=["LookupKey", "LookupName", "LookupValue", "StandardLookupValue"],
    orderby="LookupKey asc",
    top=200,
)
for record in response.get("value", []):
    print(record.get("LookupValue"), record.get("StandardLookupValue"))
```

## Discover unique category names

`get_lookup_names()` neither deduplicates names nor fetches all pages. This
example collects categories from explicit pages and deduplicates them locally.
If the dataset changes during offset pagination, restart discovery or use the
service's continuation mechanism in your application.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
names = set()
skip = 0
while True:
    response = client.lookup.get_lookups(
        select=["LookupName", "LookupKey"],
        orderby="LookupName asc,LookupKey asc",
        top=200,
        skip=skip,
    )
    records = response.get("value", [])
    if not records:
        break
    names.update(record["LookupName"] for record in records if record.get("LookupName"))
    skip += len(records)
print(sorted(names))
```

An empty page ends this example; a short page alone does not prove discovery is
complete. Keep the stable key in `orderby` to reduce inconsistent ordering.

## Query modified records

`get_modified_lookups(since, **kwargs)` builds `ModificationTimestamp gt '<timestamp>'`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDT00:00:00Z`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


## Interpret returned values

Client filters and tests use `LookupKey`, `LookupName`, `LookupValue`,
`StandardLookupValue`, `IsActive`, and `ModificationTimestamp`. Other fields may be
available in service metadata. A standard value can be null; the standard helper
filters out null values but does not validate that the remainder is a complete
RESO catalog. The active helper relies on the service's `IsActive` field.

The library leaves JSON values and types unchanged. Do not assume display labels,
local lookup values, standard values, and property filter values are interchangeable.
Derive any mapping from the actual records and the target property's metadata.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Resource metadata](resource.md) for field discovery.
- [Property records](properties.md) for property filters.
- [OData queries](../guides/odata-queries.md) for paging and string literals.
