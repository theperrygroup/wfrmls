# API Reference

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **Core Client**

    ---

    The main entry point for accessing all WFRMLS API functionality

    [:octicons-arrow-right-24: WFRMLSClient](api/client.md)

-   :material-home-city:{ .lg .middle } **Properties**

    ---

    Search, retrieve, and analyze property listings with comprehensive filtering

    [:octicons-arrow-right-24: Property API](api/properties.md)

-   :material-account-group:{ .lg .middle } **Members & Offices**

    ---

    Access agent, broker, and office information for the MLS network

    [:octicons-arrow-right-24: Members](api/members.md) · [:octicons-arrow-right-24: Offices](api/offices.md)

-   :material-calendar:{ .lg .middle } **Open Houses**

    ---

    Manage and query open house schedules and showing information

    [:octicons-arrow-right-24: Open Houses](api/openhouse.md)

-   :material-database:{ .lg .middle } **Data & Lookups**

    ---

    Access reference data, lookups, and system metadata

    [:octicons-arrow-right-24: Data System](api/data-system.md) · [:octicons-arrow-right-24: Lookups](api/lookup.md)

-   :material-tools:{ .lg .middle } **Specialized**

    ---

    ADU data, deleted records, analytics, and property unit types

    [:octicons-arrow-right-24: Specialized APIs](api/specialized.md)

</div>

## Quick Start Reference

=== "Basic Usage"

    ```python
    from wfrmls import WFRMLSClient
    
    # Initialize client
    client = WFRMLSClient(bearer_token="your_token")
    
    # Get active properties (first 10)
    properties = client.property.get_active_properties(top=10)
    
    # Get property details
    property_detail = client.property.get_property("12345678")
    ```

=== "Search Properties"

    ```python
    # Search by location
    properties = client.property.search_properties_by_radius(
        latitude=40.7608, 
        longitude=-111.8910, 
        radius_miles=10,
        top=50
    )
    
    # Search with filters
    properties = client.property.get_properties(
        filter_query="ListPrice gt 500000 and City eq 'Salt Lake City'",
        orderby="ListPrice desc",
        top=25
    )
    ```

=== "Members & Offices"

    ```python
    # Get active agents
    members = client.member.get_active_members(top=50)
    
    # Get member with office info
    member_detail = client.member.get_member_with_office("12345")
    
    # Get active offices
    offices = client.office.get_active_offices(top=50)
    ```

=== "Open Houses"

    ```python
    # Get upcoming open houses
    open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=7)
    
    # Get open houses for specific property
    property_opens = client.openhouse.get_open_houses_for_property("1611952")
    
    # Get open houses by agent
    agent_opens = client.openhouse.get_open_houses_by_agent("96422")
    ```

## Service Status

!!! success "Available Endpoints"
    The following endpoints are fully operational and ready for production use:
    
    ✅ **Properties** - Complete property data and search capabilities  
    ✅ **Members** - Agent and broker information  
    ✅ **Offices** - Brokerage and office data  
    ✅ **Open Houses** - Showing schedules and events  
    ✅ **Data System** - System metadata and information  
    ✅ **Resource** - API resource definitions  
    ✅ **Lookup** - Reference data and enumerations  
    ✅ **ADU** - Accessory Dwelling Unit data  
    ✅ **Property Unit Types** - Unit classification data  
    ✅ **Deleted** - Deleted record tracking  

!!! warning "Temporarily Unavailable"
    The following endpoints are experiencing server-side issues and have been temporarily disabled:
    
    ⚠️ **Media** - Property photos and documents (504 Gateway Timeouts)  
    ⚠️ **History** - Property and listing history (Missing entity type)  
    ⚠️ **Green Verification** - Green building certifications (Missing entity type)  
    ⚠️ **Analytics** - Market analytics and reporting (Limited availability)

## Authentication

All API calls require a bearer token for authentication:

```python
# Method 1: Pass token directly
client = WFRMLSClient(bearer_token="9d0243d7632d115b002acf3547d2d7ee")

# Method 2: Use environment variable
import os
os.environ['WFRMLS_BEARER_TOKEN'] = "9d0243d7632d115b002acf3547d2d7ee"
client = WFRMLSClient()  # Will auto-load from environment
```

!!! tip "Environment Variables"
    It's recommended to store your bearer token in the `WFRMLS_BEARER_TOKEN` environment variable for security.

## Error Handling

The WFRMLS client uses a comprehensive exception hierarchy for error handling:

```python
from wfrmls.exceptions import (
    WFRMLSError,           # Base exception
    AuthenticationError,   # Invalid credentials
    NotFoundError,        # Resource not found  
    RateLimitError,       # Rate limit exceeded
    ValidationError       # Invalid parameters
)

try:
    properties = client.property.get_properties()
except AuthenticationError:
    print("❌ Invalid API credentials")
except RateLimitError:
    print("⏱️ Rate limit exceeded - please wait")
except NotFoundError:
    print("🔍 Resource not found")
except ValidationError as e:
    print(f"📝 Invalid parameters: {e}")
except WFRMLSError as e:
    print(f"🚨 API error: {e}")
```

## Response Format

All API responses follow the OData v4 standard format:

```json
{
    "@odata.context": "https://api.wfrmls.com/RETS/api/$metadata#Property",
    "@odata.count": 1250,
    "value": [
        {
            "ListingId": "12345678",
            "ListPrice": 750000,
            "Address": "123 Main St",
            "City": "Salt Lake City",
            "StateOrProvince": "Utah",
            "@odata.etag": "W/\"datetime'2024-01-15T10%3A30%3A00.000Z'\""
        }
    ]
}
```

## Pagination

Use `$top`, `$skip`, and `$count` parameters for pagination:

```python
# Get first 50 properties
page1 = client.property.get_properties(top=50)

# Get next 50 properties  
page2 = client.property.get_properties(top=50, skip=50)

# Include total count
with_count = client.property.get_properties(top=10, count=True)
print(f"Total properties: {with_count.get('@odata.count', 'Unknown')}")
```

## Filtering and Ordering

The API supports OData v4 query syntax for filtering and ordering:

```python
# Filter by price range and city
properties = client.property.get_properties(
    filter_query="ListPrice ge 400000 and ListPrice le 800000 and City eq 'Park City'",
    orderby="ListPrice desc",
    top=25
)

# Filter by date range
from datetime import datetime, timedelta
recent_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
recent_properties = client.property.get_properties(
    filter_query=f"ModificationTimestamp ge {recent_date}",
    orderby="ModificationTimestamp desc"
)
```

!!! info "OData Query Reference"
    For complete OData v4 query syntax, refer to the [OData documentation](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html).

## Rate Limits

The WFRMLS API implements rate limiting to ensure fair usage:

- **Standard Rate**: 1000 requests per hour per token
- **Burst Rate**: 100 requests per minute  
- **Concurrent**: Maximum 10 simultaneous connections

!!! tip "Rate Limit Best Practices"
    - Implement exponential backoff for rate limit errors
    - Use appropriate `$top` values to minimize requests
    - Cache frequently accessed data when possible
    - Monitor rate limit headers in responses

---

*For detailed method documentation, parameter specifications, and return types, explore the individual API sections using the navigation above.* 