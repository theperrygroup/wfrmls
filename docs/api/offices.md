---
description: Retrieve MLS office records and filter brokerages by city, postal code, name, status, or modification time with OfficeClient.
---

# Office API reference

`OfficeClient` requests brokerage records from the `Office` resource. Its helpers
build name, city, postal-code, status, and modification filters and can request
expanded member relationships.

## Configure access

Use `WFRMLSClient().office` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`office`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.

## Query office records

```text
get_offices(top=None, skip=None, filter_query=None, select=None,
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

The method requests `Office` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve one office

`get_office(office_key: str) -> Dict[str, Any]` requests `Office('<key>')` and
returns the record dictionary. A missing office reported with HTTP 404 raises
`NotFoundError`; it does not return `None`.

## Use office helpers

Each helper returns a collection response dictionary and forwards its `**kwargs`
to `get_offices()`.

| Method | Filter or expansion |
| --- | --- |
| `get_active_offices(**kwargs)` | Sets `OfficeStatus eq 'Active'` |
| `get_offices_by_city(city: str, **kwargs)` | Sets `OfficeCity eq '<city>'` |
| `search_offices_by_name(name: str, **kwargs)` | Sets `contains(OfficeName, '<name>')` |
| `get_offices_by_zipcode(zipcode: str, **kwargs)` | Sets `OfficePostalCode eq '<zipcode>'` |
| `get_offices_with_members(**kwargs)` | Sets `expand="Members"` |
| `get_modified_offices(since: Union[str, date], **kwargs)` | Filters `ModificationTimestamp`; timestamp handling is described below |

City, name, and postal-code helpers append a supplied `filter_query` with `and`.
Parenthesize any additional expression containing `or`. These helpers interpolate
strings directly; escape apostrophes as doubled quotes in an OData string literal.
Postal codes are strings so leading zeros are retained.

Do not supply `filter_query` to the active helper or `expand` to the member
expansion helper: those arguments are already set and duplicates raise `TypeError`.
The expansion name is `Members`, not `Member`. Relationship availability is
determined by the service metadata and your credentials.

## Find active offices in a city

Set `WFRMLS_BEARER_TOKEN` before running this example. Change the city to match
your query. The result is one page of office records.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.office.get_offices_by_city(
    "Salt Lake City",
    filter_query="OfficeStatus eq 'Active'",
    select=["OfficeKey", "OfficeName", "OfficeCity", "OfficePostalCode"],
    orderby="OfficeName asc,OfficeKey asc",
    top=50,
)
for office in response.get("value", []):
    print(office.get("OfficeKey"), office.get("OfficeName"))
```

## Retrieve an office with its members

Replace `office-key` with a key returned by your service. A collection filter can
request related members, while `get_office()` accepts only the key.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.office.get_offices_with_members(
    filter_query="OfficeKey eq 'office-key'",
    top=1,
)
for office in response.get("value", []):
    print(office.get("OfficeName"))
    for member in office.get("Members") or []:
        print(member.get("MemberKey"), member.get("MemberLastName"))
```

## Query modified records

`get_modified_offices(since, **kwargs)` builds `ModificationTimestamp gt <timestamp>`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDZ`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


## Interpret fields and enums

Fields referenced by client queries and tests include `OfficeKey`, `OfficeName`,
`OfficeStatus`, `OfficeCity`, `OfficePostalCode`, `OfficePhone`, and
`ModificationTimestamp`. `Members` is the relationship requested by the expansion
helper. The client does not guarantee a field catalog or convert JSON values.
Consult metadata for contact fields, broker fields, branch relationships, types,
and nullability before selecting them.

`wfrmls.office.OfficeStatus` defines `ACTIVE="Active"`, `INACTIVE="Inactive"`,
and `SUSPENDED="Suspended"`. `OfficeType` defines `MAIN="Main"`,
`BRANCH="Branch"`, and `FRANCHISE="Franchise"`. These are library constants;
they do not validate provider data or confirm current service lookup values.
Use the enum's `.value` in a filter expression.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Member records](members.md) for queries using `OfficeKey`.
- [OData queries](../guides/odata-queries.md) for compound filters and paging.
- [Resource metadata](resource.md) for resource and field discovery.
