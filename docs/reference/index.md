# Reference

Quick reference materials and technical documentation for the WFRMLS API. Use this section to quickly look up information while developing.

## 📚 Reference Materials

<div class="grid cards" markdown>

-   :material-alert-circle:{ .lg .middle } **Error Codes**

    ---

    Complete list of error codes, meanings, and solutions

    [:octicons-arrow-right-24: Error Codes](error-codes.md)

-   :material-speedometer:{ .lg .middle } **Rate Limits**

    ---

    API rate limiting details and best practices

    [:octicons-arrow-right-24: Rate Limits](rate-limits.md)

-   :material-database:{ .lg .middle } **Field Reference**

    ---

    Complete field definitions and data types

    [:octicons-arrow-right-24: Field Reference](field-reference.md)

-   :material-code-braces:{ .lg .middle } **OData Queries**

    ---

    OData v4 query syntax and examples

    [:octicons-arrow-right-24: OData Queries](odata-queries.md)

-   :material-history:{ .lg .middle } **Changelog**

    ---

    Version history and release notes

    [:octicons-arrow-right-24: Changelog](changelog.md)

</div>

## Quick Reference Tables

### Authentication
```python
# Environment variable (recommended)
os.environ['WFRMLS_BEARER_TOKEN'] = "your_token"
client = WFRMLSClient()

# Direct token
client = WFRMLSClient(bearer_token="your_token")
```

### Common Status Codes
| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid credentials |
| 404 | Not Found | Resource not found |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Internal server error |

### Rate Limits
| Limit Type | Value | Description |
|------------|-------|-------------|
| Hourly | 1000 requests | Standard rate limit |
| Burst | 100 requests/minute | Short-term burst |
| Concurrent | 10 connections | Max simultaneous |

### Common OData Operators
| Operator | Usage | Example |
|----------|-------|---------|
| `eq` | Equals | `City eq 'Salt Lake City'` |
| `ne` | Not equals | `ListPrice ne null` |
| `gt` | Greater than | `ListPrice gt 500000` |
| `ge` | Greater or equal | `BedroomsTotal ge 3` |
| `lt` | Less than | `LivingArea lt 3000` |
| `le` | Less or equal | `ListPrice le 1000000` |
| `and` | Logical AND | `City eq 'Provo' and ListPrice gt 300000` |
| `or` | Logical OR | `City eq 'Provo' or City eq 'Orem'` |
| `contains` | Contains text | `contains(tolower(City), 'salt')` |

### Standard Query Parameters
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `$top` | int | Limit results | `$top=50` |
| `$skip` | int | Skip results | `$skip=100` |
| `$filter` | string | Filter criteria | `$filter=City eq 'Provo'` |
| `$orderby` | string | Sort order | `$orderby=ListPrice desc` |
| `$select` | string | Choose fields | `$select=ListingId,ListPrice` |
| `$count` | bool | Include count | `$count=true` |

## Property Field Quick Reference

### Core Property Fields
| Field | Type | Description |
|-------|------|-------------|
| `ListingId` | string | Unique listing identifier |
| `ListPrice` | decimal | Current listing price |
| `StandardStatus` | string | Active, Pending, Sold, etc. |
| `City` | string | Property city |
| `BedroomsTotal` | int | Number of bedrooms |
| `BathroomsTotalInteger` | int | Number of bathrooms |
| `LivingArea` | decimal | Square footage |
| `PropertyType` | string | Residential, Commercial, etc. |
| `PropertySubType` | string | Single Family, Condo, etc. |

### Location Fields
| Field | Type | Description |
|-------|------|-------------|
| `UnparsedAddress` | string | Full address |
| `Latitude` | decimal | Geographic latitude |
| `Longitude` | decimal | Geographic longitude |
| `PostalCode` | string | ZIP/postal code |
| `CountyOrParish` | string | County name |

### Date Fields
| Field | Type | Description |
|-------|------|-------------|
| `ListingContractDate` | datetime | Date listed |
| `ModificationTimestamp` | datetime | Last modified |
| `CloseDate` | datetime | Closing date |
| `OriginalEntryTimestamp` | datetime | First entry |

## Member Field Quick Reference

### Core Member Fields
| Field | Type | Description |
|-------|------|-------------|
| `MemberKey` | string | Unique member identifier |
| `MemberFirstName` | string | Agent first name |
| `MemberLastName` | string | Agent last name |
| `MemberEmail` | string | Contact email |
| `MemberDirectPhone` | string | Direct phone |
| `MemberType` | string | Agent, Broker, etc. |
| `MemberStatus` | string | Active, Inactive, etc. |
| `MemberOfficeKey` | string | Associated office |

## Office Field Quick Reference

### Core Office Fields
| Field | Type | Description |
|-------|------|-------------|
| `OfficeKey` | string | Unique office identifier |
| `OfficeName` | string | Office/brokerage name |
| `OfficePhone` | string | Main phone number |
| `OfficeEmail` | string | Contact email |
| `OfficeCity` | string | Office city |
| `OfficeStatus` | string | Active, Inactive, etc. |

## Need More Detail?

- 📖 **Complete Documentation**: See the [API Reference](../api/) for detailed method documentation
- 🎯 **How-To Guides**: Check [Guides](../guides/) for step-by-step instructions
- 💡 **Examples**: Browse [Examples](../examples/) for practical code samples
- 🛠️ **Issues**: Report problems on [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)

---

*This reference is generated from the latest API version. For historical information, see the [Changelog](changelog.md).* 