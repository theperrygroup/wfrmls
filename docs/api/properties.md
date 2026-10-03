---
description: Query WFRMLS Property records with exact OData parameters, numeric key lookups, supported search helpers, and documented pagination limitations.
---

# Property queries and listing lookups

`client.property` provides `PropertyClient`. Collection methods return the server's JSON dictionary; `get_property()` returns a single listing dictionary.

## Query a collection

`get_properties(top=None, skip=None, filter_query=None, select=None, orderby=None, expand=None, count=None)` sends a GET to `Property`. `search_properties()` has the same parameters and delegates to it.

| Parameter | Type | Required | Description | Default |
| --- | --- | --- | --- | --- |
| `top` | `int \| None` | No | `$top`; values above 200 are clamped to 200 | `None` |
| `skip` | `int \| None` | No | `$skip` offset | `None` |
| `filter_query` | `str \| None` | No | `$filter` expression passed to the server | `None` |
| `select` | `list[str] \| str \| None` | No | `$select`; lists become comma-separated strings | `None` |
| `orderby` | `str \| None` | No | `$orderby` expression | `None` |
| `expand` | `list[str] \| str \| None` | No | `$expand`; lists become comma-separated strings | `None` |
| `count` | `bool \| None` | No | `$count` becomes `true` or `false` | `None` |

Omitted parameters are not sent. The wrapper does not validate field names, enum values, filter syntax, or positive pagination values. Check your metadata for supported fields and relationships.

With `WFRMLS_BEARER_TOKEN` configured:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    top=25,
    filter_query="StandardStatus eq 'Active' and City eq 'Salt Lake City'",
    select=["ListingId", "ListPrice", "City"],
    orderby="ListPrice desc",
    count=True,
)
print("Returned records:", len(response.get("value", [])))
print("Server count:", response.get("@odata.count"))
```

`@odata.count`, when supplied by the server, is separate from the number of returned records. Collection methods make one request and do not follow `@odata.nextLink` automatically.

## Retrieve one property by numeric key

`get_property(listing_id)` converts the supplied string to an integer and requests `Property(<number>)`. It cannot look up arbitrary alphanumeric `ListingKey` values.

| Parameter | Type | Required | Description | Default |
| --- | --- | --- | --- | --- |
| **`listing_id`** | `str` | Yes | Numeric key accepted by `int()` | — |

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
listing = client.property.get_property("12345")
print(listing.get("ListingId"), listing.get("ListPrice"))
```

A direct object response is returned unchanged. If the response contains a `value` array, the first object is returned. An empty array raises `NotFoundError`; a non-list `value` or non-object first item raises `WFRMLSError`. A nonnumeric string raises `ValidationError` before a request.

## Use the supported search helpers

All collection helpers below return a JSON dictionary. Their `**kwargs` must be accepted by `get_properties()`; arbitrary OData keywords are not forwarded.

| Helper | Filter or behavior | Default |
| --- | --- | --- |
| `get_active_properties(**kwargs)` | `StandardStatus eq 'Active'` | No pagination default |
| `get_properties_by_price_range(min_price=None, max_price=None, **kwargs)` | Inclusive `ListPrice ge/le` comparisons | No price restriction |
| `get_properties_by_city(city, **kwargs)` | `City eq '<city>'`; combines `filter_query` with `and` | City required |
| `get_properties_with_media(**kwargs)` | Sets `$expand=Media` | No extra filter |
| `get_modified_properties(since, **kwargs)` | `ModificationTimestamp gt <cutoff>` | Cutoff required |
| `get_luxury_properties(min_price=1000000, **kwargs)` | Minimum price and Active status; combines filters | 1,000,000 |
| `get_new_listings(days_back=7, **kwargs)` | `OnMarketDate gt <UTC date>`; combines filters | 7 days |

The active, price-range, and modified-property helpers supply their own `filter_query`. Do not pass another `filter_query` to those helpers when they build a filter: Python raises a duplicate-keyword `TypeError`. Use `get_properties()` for combined filters instead. Likewise, do not pass `expand` to `get_properties_with_media()`.

Use `PropertyStatus.ACTIVE.value` or a string when building filters. The enums contain constants; collection methods do not convert enum objects.

```python
from datetime import datetime, timedelta, timezone
from wfrmls import WFRMLSClient

client = WFRMLSClient()
city_page = client.property.get_properties_by_city(
    "Salt Lake City", filter_query="ListPrice le 600000", top=25
)
cutoff = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
updates = client.property.get_modified_properties(since=cutoff, top=100)
print(len(city_page.get("value", [])), len(updates.get("value", [])))
```

Prefer an explicit UTC datetime string for modification cutoffs. The helper removes `+00:00` and trailing `Z`, then appends `Z`; other offsets are not converted to UTC. `date` objects are accepted but become date-only text with `Z`. Numeric zero values are not validated or normalized elsewhere.

### Combine criteria in a dictionary

`search_properties_by_multiple_criteria(criteria, **kwargs)` builds filters for these exact keys:

| Criteria keys | Property fields |
| --- | --- |
| `status`, `property_type` | `StandardStatus`, `PropertyType` |
| `min_price`, `max_price` | `ListPrice` |
| `city`, `zip_code`, `school_district` | `City`, `PostalCode`, `SchoolDistrict` |
| `min_bedrooms`, `max_bedrooms` | `BedroomsTotal` |
| `min_bathrooms`, `max_bathrooms` | `BathroomsTotalInteger` |
| `min_sqft`, `max_sqft` | `LivingArea` |

Unknown keys and falsey values, including numeric zero, are ignored. Existing `filter_query` is joined with `and` without added parentheses. Text values are inserted into expressions without escaping; build properly escaped OData literals yourself for text containing apostrophes.

## Pagination and partial results

`get_all_properties_paginated(page_size=200, max_pages=None, **kwargs)` sends repeated `$top`/`$skip` queries. It replaces any supplied `top` and `skip`, clamps `page_size` above 200, and accumulates records in memory.

The return dictionary contains `value`, `@odata.context`, and `pagination_info` with `pages_fetched`, `total_records`, `page_size`, and `last_skip`. `@odata.count` is copied only if it appears in the last response.

**This helper catches request exceptions and returns accumulated results without an error marker.** An empty result can therefore mean an empty dataset or failure on the first request. A successful-looking dictionary does not prove a complete sync. Use explicit page requests with your own error handling when completeness matters.

Use a positive `page_size` and a positive `max_pages` when limiting work. `max_pages=None` or `0` adds no page limit. The helper stops after an empty/short page or the requested page limit; it does not follow next links.

## Location helper limitations

- `search_properties_by_radius(...)` and `search_properties_by_polygon(...)` always raise `ValidationError` before an HTTP request.
- `search_properties_near_address(address, radius_miles=5.0, **kwargs)` only splits a comma-delimited address and filters on its second-to-last component as a city. It does not geocode, calculate distance, or use `radius_miles`.
- An address without a comma returns `{"value": [], "@odata.context": "", "error": "..."}` locally.

Use a city or other verified field filter for server-side location queries. The compatibility [notes](live-api-updates.md) explain the boundary between implemented request behavior and current provider availability.

## Generated method and enum reference

::: wfrmls.properties
    options:
      show_root_heading: false
      show_source: false
