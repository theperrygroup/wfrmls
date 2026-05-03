# Examples

Practical examples for common WFRMLS client workflows. This section stays intentionally compact and points to the guides that already exist in the repository.

---

## Quick Navigation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Make your first request and inspect a simple response.

    [:octicons-arrow-right-24: Quick Start](../getting-started/quickstart.md)

-   :material-home-search:{ .lg .middle } **Property Search**

    ---

    Work with filtering, sorting, and field selection.

    [:octicons-arrow-right-24: Property Search Guide](../guides/property-search.md)

-   :material-filter-cog:{ .lg .middle } **OData Queries**

    ---

    Build more precise query expressions for real workloads.

    [:octicons-arrow-right-24: OData Queries Guide](../guides/odata-queries.md)

-   :material-database-sync:{ .lg .middle } **Data Sync**

    ---

    Use incremental update patterns for local stores.

    [:octicons-arrow-right-24: Data Sync Guide](../guides/data-sync.md)

-   :material-shield-alert:{ .lg .middle } **Error Handling**

    ---

    Add retries, logging, and defensive response handling.

    [:octicons-arrow-right-24: Error Handling Guide](../guides/error-handling.md)

</div>

---

## Short Examples

### Property search

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and ListPrice le 500000",
    select=["ListingId", "ListPrice", "City", "BedroomsTotal"],
    orderby="ListPrice asc",
    top=10,
)

for property_record in properties:
    print(
        property_record["ListingId"],
        property_record.get("City"),
        property_record.get("ListPrice"),
    )
```

### Open house lookup

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=7, top=10)

for open_house in open_houses.get("value", []):
    print(open_house.get("OpenHouseDate"), open_house.get("ListingKey"))
```

### Incremental sync pattern

```python
from datetime import datetime, timedelta, timezone
from wfrmls import WFRMLSClient

client = WFRMLSClient()
cutoff = datetime.now(timezone.utc) - timedelta(minutes=15)

recent_updates = client.property.get_properties(
    filter_query=f"ModificationTimestamp gt '{cutoff.isoformat()}'",
    orderby="ModificationTimestamp desc",
    top=200,
)
```

---

## When To Use Guides Instead

Use the dedicated guides when you need more than a quick pattern:

- **[Property Search Guide](../guides/property-search.md)** for search-oriented applications.
- **[OData Queries Guide](../guides/odata-queries.md)** for complex filters and sorting.
- **[Data Sync Guide](../guides/data-sync.md)** for synchronization workflows.
- **[Rate Limits Guide](../guides/rate-limits.md)** for pacing and retry strategies.

---

## Next Steps

- **[API Reference](../api/index.md)** - Review the full client surface.
- **[Reference Guide](../reference/index.md)** - Check shared field and response conventions.
- **[Getting Started](../getting-started/index.md)** - Revisit installation and authentication setup.
