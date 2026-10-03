---
title: WFRMLS Python client for UtahRealEstate.com
description: Query Utah MLS listings, agents, offices, and open houses with the WFRMLS Python client. Learn authentication, OData filters, pagination, and synchronization.
---

# WFRMLS Python client

Use `wfrmls` to query UtahRealEstate.com's Wasatch Front Regional MLS
RESO Web API from Python. The library provides resource clients for listings,
agents, offices, open houses, and supporting metadata.

## Start with a working request

You need Python 3.8 or later and a provider-issued bearer token. Install the
package with `python -m pip install wfrmls`, then configure
`WFRMLS_BEARER_TOKEN` in your application's environment.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    top=10,
    filter_query="StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "City"],
)

listings = response.get("value", [])
print(f"Retrieved {len(listings)} listings")
for listing in listings:
    print(listing.get("ListingId"), listing.get("ListPrice"))
```

Collections return an OData dictionary whose `value` field contains the
records. `get_property(listing_id)` returns one property dictionary.
The [quick start](getting-started/quickstart.md) explains both response shapes
and how to handle errors.

## Find the documentation you need

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting started**

    ---

    Install the client, configure authentication, and query your first listings.

    [:octicons-arrow-right-24: Follow the quick start](getting-started/quickstart.md)

-   :material-filter-variant:{ .lg .middle } **Search and synchronization**

    ---

    Compose OData filters and plan pagination, updates, and deletion processing.

    [:octicons-arrow-right-24: Read the guides](guides/index.md)

-   :material-api:{ .lg .middle } **API reference**

    ---

    Check real method signatures, return values, and resource-specific behavior.

    [:octicons-arrow-right-24: Browse resource clients](api/index.md)

-   :material-code-braces:{ .lg .middle } **Examples**

    ---

    Adapt complete examples for listing queries and integration workflows.

    [:octicons-arrow-right-24: Explore the examples](examples/index.md)

</div>

## Supported resource access

| Task | Client or guide |
| --- | --- |
| Search listings by status, price, city, or address | [`client.property`](api/properties.md) |
| Query real estate agents and brokerages | [`client.member`](api/members.md), [`client.office`](api/offices.md) |
| Retrieve open house events | [`client.openhouse`](api/openhouse.md) |
| Discover lookup values | [`client.lookup`](api/lookup.md) |
| Query ADUs and unit types | [`client.adu`](api/adu.md), [`client.property_unit_types`](api/property-unit-types.md) |
| Track deleted records | [`client.deleted`](api/deleted.md) |
| Inspect resource and system information | [`client.resource`](api/resource.md), [`client.data_system`](api/data-system.md) |
| Summarize retrieved samples | [`WFRMLSAnalytics(client)`](api/analytics.md) |

Use the [service document and XML metadata](api/client.md) to discover the
resources and fields exposed to your token. The provider determines data access
and query support.

## Understand the library's limits

!!! warning "Location searches"
    Radius and polygon helpers raise `ValidationError`. The near-address helper
    only falls back to a city query or returns an empty error payload; it does
    not geocode or apply a radius. Use the supported
    [city and address search patterns](guides/geolocation.md).

!!! info "Media, history, and green verification"
    Standalone client classes are exported, but `WFRMLSClient` has no media,
    history, or green verification attributes. Read the
    [API reference](api/index.md) and verify provider access before using them.

Ordinary requests do not retry automatically or set a timeout. HTTP 429 raises
`RateLimitError`; your application supplies any waiting or retry policy.
The property pagination helper uses `$skip` and `$top`, rather than following
`@odata.nextLink`, and can silently return partial results after an error.
See [rate limits](guides/rate-limits.md),
[error handling](guides/error-handling.md), and
[data synchronization](guides/data-sync.md) before building an importer.

## Documentation scope and support

This site documents the repository's `master` branch. Check the
[PyPI package](https://pypi.org/project/wfrmls/) and
[release history](https://github.com/theperrygroup/wfrmls/releases) when matching
examples to an installed release.

The Python client is distributed under the [MIT License](legal/license.md).
That license covers the software, not permission to access or redistribute MLS
data. Obtain API access through the
[UtahRealEstate.com vendor dashboard](https://vendor.utahrealestate.com/).

For library bugs or documentation corrections, use
[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues). For contributions,
read the [development guide](development/index.md).
