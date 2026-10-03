---
title: "WFRMLS task guides"
description: "Task guides for WFRMLS property filters, OData paging, synchronization checkpoints, error handling, rate limits, and geographic-search limits."
---

# WFRMLS task guides

These guides explain how to use the implemented client methods and where your
application must supply its own logic. Start with the
[quick start](../getting-started/quickstart.md) if you have not made a request yet.

<div class="grid cards" markdown>

-   :material-home-search: **Search properties**

    ---

    Combine filters, select fields, fetch a listing, and expand media.

    [Property search](property-search.md)

-   :material-filter: **Build OData queries**

    ---

    Escape literals and follow validated collection next links.

    [OData queries and paging](odata-queries.md)

-   :material-sync: **Synchronize records**

    ---

    Define complete runs, durable checkpoints, and deletion reconciliation.

    [Data synchronization](data-sync.md)

-   :material-alert-circle: **Handle failures**

    ---

    Match actual exception types and use bounded application retries.

    [Error handling](error-handling.md)

-   :material-speedometer: **Manage request traffic**

    ---

    Recognize 429 responses and configure pacing for your provider agreement.

    [Rate limits](rate-limits.md)

-   :material-map-marker: **Understand geographic limits**

    ---

    Check the radius and polygon helper limitations before building map searches.

    [Geographic queries](geolocation.md)

</div>

Examples are application patterns rather than guarantees about current provider
permissions, quotas, or snapshots. Check your service metadata and licensed
scope before adopting them. Runnable mocked examples are in the
[examples section](../examples/index.md).
