---
description: Query PropertyUnitTypes records by key, listing, or unit type with exact parameter behavior, residential filters, and incremental-update limitations.
---

# Property unit types API

`PropertyUnitTypesClient` queries the `PropertyUnitTypes` resource and returns the server's JSON response.
Access it through `WFRMLSClient.property_unit_types` or construct the service client directly.

## Configure the client

```text
PropertyUnitTypesClient(bearer_token=None, base_url=None)
```

The constructor accepts a bearer token or reads `WFRMLS_BEARER_TOKEN`.
The default base URL is `https://resoapi.utahrealestate.com/reso/odata`.
Direct construction requires credentials immediately; `WFRMLSClient` checks them when `.property_unit_types` is first accessed.

The examples require a configured `WFRMLS_BEARER_TOKEN` and use illustrative keys.
Check [service discovery](client.md) for the schema available to your account before selecting fields or expanding relationships.

## Query one page of unit types

```text
get_property_unit_types(top=None, skip=None, filter_query=None,
                        select=None, orderby=None, expand=None,
                        count=None) -> Dict[str, Any]
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

The library does not validate field names, filter syntax, or negative pagination values.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property_unit_types.get_unit_types_for_property(
    listing_key="1611952",
    top=25,
    select=["UnitTypeKey", "ListingKey", "UnitType"],
    orderby="UnitTypeKey asc",
    count=True,
)

for unit in response.get("value", []):
    print(unit.get("UnitTypeKey"), unit.get("ListingKey"), unit.get("UnitType"))
print("Count supplied by the server:", response.get("@odata.count"))
print("Next page supplied by the server:", response.get("@odata.nextLink"))
```

The method returns one response page, usually containing a `value` list.
`@odata.context`, `@odata.count`, and `@odata.nextLink` are retained when supplied by the server.
Records are not normalized, and pagination links are not followed automatically.

`UnitTypeKey`, `ListingKey`, and `UnitType` are used by the library's helpers and mocked tests.
The library does not define an exhaustive schema or guarantee rent, bedroom, bathroom, or unit-count fields.
Use the provider's metadata before building reports from those fields.

## Retrieve a unit type by key

```text
get_property_unit_type(unit_type_key: str) -> Dict[str, Any]
```

This method requests `PropertyUnitTypes('<unit_type_key>')` and returns the single-record JSON dictionary directly.
It does not add a `value` wrapper. A 404 response raises `NotFoundError`.
The key is interpolated without escaping, so use a trusted key.

## Filter by listing or unit type

The following helpers accept query keywords from `get_property_unit_types()` through `**kwargs` and return the same page shape.

| Method signature | Generated query |
| --- | --- |
| `get_unit_types_for_property(listing_key: str, **kwargs)` | `ListingKey eq '<listing_key>'` |
| `get_unit_types_by_type(unit_type: str, **kwargs)` | `UnitType eq '<unit_type>'` |
| `get_residential_unit_types(**kwargs)` | Parenthesized `or` filter for seven unit-type names. |
| `get_unit_types_with_properties(**kwargs)` | Sets `expand="Properties"`. |

Use `get_unit_types_for_property()` for a listing. There is no `get_unit_types_by_listing()` method.
The residential helper uses these exact strings: `Condo`, `Townhome`, `Apartment`, `Single Family`, `Duplex`, `Triplex`, and `Fourplex`.
It is a fixed list of filters, not a provider-validated classification of every residential record.

The filter helpers append a supplied `filter_query` with `and` without grouping that expression.
Parenthesize expressions containing `or` when they should apply together.
Listing keys and unit-type names are interpolated without escaping; use trusted values or construct an escaped expression for the base query method.

`get_unit_types_with_properties()` fixes `expand`, so passing `expand` also raises `TypeError`.
Use `get_property_unit_types()` to choose your own expansions. The server determines whether the `Properties` relationship is available.

## Query modified unit types

```text
get_modified_unit_types(since: Union[str, date, datetime], **kwargs) -> Dict[str, Any]
```

The helper sets `filter_query="ModificationTimestamp gt '<timestamp>'"`.
It forwards other query keywords to `get_property_unit_types()`.
Passing another `filter_query` raises `TypeError`; combine filters in the base query method instead.

| `since` input | Conversion performed by the helper |
| --- | --- |
| `str` | Used unchanged inside the quoted filter literal. |
| `date` | Converted to `YYYY-MM-DDT00:00:00Z`. |
| `datetime` | Converted with `isoformat()`, then appended with `Z`. |

The helper does not normalize time zones.
An aware datetime generates an offset followed by `Z`, such as `+00:00Z`; pass a normalized UTC string instead.

```python
from datetime import datetime, timedelta, timezone

from wfrmls import WFRMLSClient

client = WFRMLSClient()
condos = client.property_unit_types.get_unit_types_by_type("Condo", top=25)
residential = client.property_unit_types.get_residential_unit_types(
    filter_query="ListingKey eq '1611952'",
    top=25,
)
cutoff = datetime.now(timezone.utc) - timedelta(days=1)
cutoff_utc = cutoff.isoformat().replace("+00:00", "Z")
updates = client.property_unit_types.get_modified_unit_types(
    since=cutoff_utc,
    top=200,
    orderby="ModificationTimestamp asc",
)

print("Condo page:", len(condos.get("value", [])))
print("Residential page:", len(residential.get("value", [])))
print("Modified page:", len(updates.get("value", [])))
```

## Handle request failures

The shared client maps HTTP 400, 401, 404, 429, and 5xx responses to `ValidationError`, `AuthenticationError`, `NotFoundError`, `RateLimitError`, and `ServerError`.
Request exceptions raise `NetworkError`; other unsuccessful statuses raise `WFRMLSError`.
These methods do not retry requests or retrieve additional pages automatically.

See [error handling](../guides/error-handling.md), the [property API](properties.md), and the [main client reference](client.md).
