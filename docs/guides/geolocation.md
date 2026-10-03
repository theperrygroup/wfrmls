---
title: "Geographic-query limitations"
description: "Understand why WFRMLS radius and polygon helpers raise ValidationError, use supported city filters, and verify geographic data separately."
---

# Geographic-query limitations

The current library does not perform radius or polygon searches. Both
`search_properties_by_radius()` and `search_properties_by_polygon()` raise
`ValidationError` before sending a request. There is no built-in bounding-box
search, geocoder, coordinate cache, or map integration.

## Check the implemented behavior

This example runs without provider access because the radius helper rejects
the call locally. The token is an intentionally invalid test value:

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import ValidationError

client = WFRMLSClient(bearer_token="documentation-test-token")
try:
    client.property.search_properties_by_radius(
        latitude=40.7608,
        longitude=-111.8910,
        radius_miles=5,
    )
except ValidationError:
    print("Radius search is not implemented by this library.")
```

Do not interpret this library limitation as proof that the provider never has
coordinate fields or spatial endpoints. The copied provider guide and the
implemented helpers differ; check current metadata and vendor documentation
before designing a spatial integration.

## Search by an available location field

A city filter is a supported client query, although the provider still decides
which fields and records are available to your account:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    filter_query="City eq 'Salt Lake City'",
    select=["ListingId", "City", "ListPrice"],
    top=20,
)
for record in response["value"]:
    print(record.get("ListingId"), record.get("City"))
```

A city boundary is different from a radius or polygon. Do not describe these
results as being within a requested distance.

## Understand the address helper's city fallback

`search_properties_near_address()` behaves differently from the radius and
polygon methods. With at least one comma, it takes the second-to-last address
component and builds a `City eq '...'` query. It never geocodes the address or
uses `radius_miles` to restrict the results. Its city interpolation also does
not escape apostrophes; prefer an explicitly escaped filter for user input.

Without a comma, it returns an empty `value` list and an `error` field without
sending a request. This offline example shows that result:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="documentation-test-token")
response = client.property.search_properties_near_address(
    address="Synthetic unstructured address",
)
assert response["value"] == []
print(response["error"])
```

Do not treat this fallback as a successful nearby-property search. In either
branch, the helper provides no distance coverage guarantee.

## Design a separate spatial workflow

If your application needs maps or distance filtering, first confirm that its
licensed feed supplies usable coordinates or that another licensed source can
provide them. Check coordinate order, units, missing values, accuracy, and the
rights to transmit addresses to a geocoding service.

Distance calculations and polygon membership would be application code, with
their own validation and tests. Filtering a single page locally can miss
matches on later pages. Exhaust the permitted candidate set using
[paging](odata-queries.md#follow-collection-next-links) before claiming full
search coverage, or use a provider-supported spatial query once independently
verified. The current client offers no guarantee for either approach.

## Related guides

Use [property search](property-search.md) for available filters and
[data licensing](../legal/index.md) for display, data-sharing, and media terms.
