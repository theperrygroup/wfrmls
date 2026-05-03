# Reference

Shared reference material for response structure, common fields, and practical WFRMLS data conventions documented in this repository.

---

## Quick Navigation

<div class="grid cards" markdown>

-   :material-code-json:{ .lg .middle } **Response Structure**

    ---

    Review the OData response format returned by client methods.

    [:octicons-arrow-right-24: Response Structure](#odata-response-structure)

-   :material-table:{ .lg .middle } **Common Fields**

    ---

    Look up frequently used property and member fields.

    [:octicons-arrow-right-24: Common Fields](#common-fields)

-   :material-domain:{ .lg .middle } **Resource Highlights**

    ---

    Compare the main resources exposed by the client.

    [:octicons-arrow-right-24: Resource Highlights](#resource-highlights)

-   :material-timer-cog:{ .lg .middle } **Technical Notes**

    ---

    Review date formats, coordinates, and practical limits.

    [:octicons-arrow-right-24: Technical Notes](#technical-notes)

</div>

---

## OData Response Structure

Most collection endpoints expose an OData-style payload. The client may wrap or return the payload depending on the helper method, so inspect the endpoint documentation when you need exact behavior.

```json
{
  "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#Property",
  "@odata.count": 1234,
  "value": [
    {
      "ListingId": "12345678",
      "ListPrice": 450000,
      "StandardStatus": "Active"
    }
  ]
}
```

---

## Common Fields

### Property fields

| Field | Type | Description |
|-------|------|-------------|
| `ListingId` | `string` | Human-readable listing identifier. |
| `ListingKey` | `string` | Stable resource key for joins and direct lookups. |
| `ListPrice` | `number` | Current asking price. |
| `StandardStatus` | `string` | Listing lifecycle status such as `Active` or `Pending`. |
| `ModificationTimestamp` | `datetime` | Last update timestamp for incremental sync workflows. |
| `City` | `string` | Listing city name. |
| `BedroomsTotal` | `integer` | Total bedrooms. |
| `BathroomsTotalInteger` | `integer` | Whole-bath equivalent count used in many examples. |

### Member and office fields

| Field | Type | Description |
|-------|------|-------------|
| `MemberKey` | `string` | Member resource key. |
| `MemberFullName` | `string` | Agent or member display name. |
| `MemberStatus` | `string` | Member lifecycle state. |
| `OfficeKey` | `string` | Office resource key. |
| `OfficeName` | `string` | Brokerage or office name. |
| `OfficeCity` | `string` | Office city. |

### Open house fields

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseKey` | `string` | Unique open house event key. |
| `ListingKey` | `string` | Listing associated with the event. |
| `OpenHouseDate` | `date` | Event date. |
| `OpenHouseStartTime` | `time` | Event start time. |
| `OpenHouseEndTime` | `time` | Event end time. |
| `OpenHouseStatus` | `string` | Event status, often `Active`, `Ended`, or `Cancelled`. |

---

## Resource Highlights

| Resource | Typical Use |
|----------|-------------|
| `Property` | Search listings, sync updates, and inspect listing details. |
| `Member` | Retrieve agent and member information. |
| `Office` | Retrieve brokerage and office information. |
| `OpenHouse` | Work with scheduled showing data. |
| `Lookup` | Inspect enumerations and supporting reference values. |
| `Deleted` | Track deletions for sync workflows. |

---

## Technical Notes

### Dates and timestamps

- Prefer ISO 8601 strings when passing timestamps in filters.
- Many sync workflows filter on `ModificationTimestamp`.
- Open house date filters often use date-only values such as `2026-04-12`.

### Coordinates

The repository's guides assume latitude and longitude are provided in decimal degrees. Use the geolocation guide for practical query patterns instead of relying on a separate local coordinate-system reference page.

### Practical limits

- The client docs commonly demonstrate `top` values up to `200` for collection endpoints.
- Use field selection and server-side filters to reduce payload size.
- Batch or paginate long-running sync jobs.

---

## Related Documentation

- **[API Reference](../api/index.md)** - Endpoint-specific pages and generated API docs.
- **[Property Search Guide](../guides/property-search.md)** - Search patterns and filtering examples.
- **[OData Queries Guide](../guides/odata-queries.md)** - Query syntax and composition examples.
- **[Geolocation Guide](../guides/geolocation.md)** - Location-based query workflows.
