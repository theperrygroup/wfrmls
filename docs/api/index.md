# API Reference

Complete documentation for all WFRMLS Python client methods, classes, and modules.

---

## 📚 Core Components

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **Client**

    ---

    Main client class and initialization options

    [:octicons-arrow-right-24: View Client API](client.md)

-   :material-home:{ .lg .middle } **Properties**

    ---

    Property listings, details, and search functionality

    [:octicons-arrow-right-24: Properties API](properties.md)

-   :material-account:{ .lg .middle } **Members**

    ---

    Real estate agent information and contact details

    [:octicons-arrow-right-24: Members API](members.md)

-   :material-office-building:{ .lg .middle } **Offices**

    ---

    Brokerage and office information

    [:octicons-arrow-right-24: Offices API](offices.md)

-   :material-door-open:{ .lg .middle } **Open Houses**

    ---

    Open house schedules and event details

    [:octicons-arrow-right-24: Open Houses API](openhouses.md)

-   :material-chart-line:{ .lg .middle } **Analytics**

    ---

    Market insights and data analytics

    [:octicons-arrow-right-24: Analytics API](analytics.md)

</div>

---

## 🔧 Specialized Modules

<div class="grid cards" markdown>

-   :material-database-search:{ .lg .middle } **Lookup**

    ---

    Reference data and lookup tables

    [:octicons-arrow-right-24: Lookup API](lookup.md)

-   :material-home-city:{ .lg .middle } **Property Unit Types**

    ---

    Property unit type classifications and multi-unit information

    [:octicons-arrow-right-24: Property Unit Types API](property-unit-types.md)

-   :material-home-plus:{ .lg .middle } **ADU (Accessory Dwelling Units)**

    ---

    Additional dwelling unit information and regulations

    [:octicons-arrow-right-24: ADU API](adu.md)

-   :material-delete:{ .lg .middle } **Deleted Records**

    ---

    Tracking deleted and archived listings

    [:octicons-arrow-right-24: Deleted API](deleted.md)

-   :material-database-cog:{ .lg .middle } **Data System**

    ---

    System metadata and configuration

    [:octicons-arrow-right-24: Data System API](data-system.md)

-   :material-history:{ .lg .middle } **History**

    ---

    Property and listing history tracking

    [:octicons-arrow-right-24: History API](history.md)

-   :material-image:{ .lg .middle } **Media**

    ---

    Property photos and media files

    [:octicons-arrow-right-24: Media API](media.md)

-   :material-alert-circle:{ .lg .middle } **Exceptions**

    ---

    Error handling and exception classes

    [:octicons-arrow-right-24: Exceptions API](exceptions.md)

</div>

---

## 🚀 Quick Start

### Initialize the Client

```python
from wfrmls import WFRMLSClient

# Initialize with environment variable
client = WFRMLSClient()

# Or initialize with explicit token
client = WFRMLSClient(bearer_token="your_bearer_token")
```

### Basic Usage Examples

=== "Properties"

    ```python
    # Get active properties
    properties = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        top=10
    )
    
    # Get specific property
    property_detail = client.property.get_property("12345678")
    
    # Search with complex filters
    luxury_homes = client.property.get_properties(
        filter_query="ListPrice ge 1000000 and BedroomsTotal ge 4",
        select=["ListingId", "ListPrice", "Address"],
        orderby="ListPrice desc"
    )
    ```

=== "Members"

    ```python
    # Get active agents
    agents = client.member.get_members(
        filter_query="MemberStatus eq 'Active'",
        top=20
    )
    
    # Get specific agent
    agent = client.member.get_member("AGENT123")
    
    # Search agents by name
    smiths = client.member.get_members(
        filter_query="contains(MemberFullName, 'Smith')"
    )
    ```

=== "Offices"

    ```python
    # Get all offices
    offices = client.office.get_offices()
    
    # Get specific office
    office = client.office.get_office("OFF123")
    
    # Get offices in specific city
    local_offices = client.office.get_offices(
        filter_query="OfficeCity eq 'Salt Lake City'"
    )
    ```

---

## 📊 Method Reference

### Common Parameters

All endpoint methods support these standard OData parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **`top`** | `int` | Limit number of results | `top=50` |
| **`skip`** | `int` | Skip first N results | `skip=100` |
| **`filter_query`** | `str` | OData filter expression | `"ListPrice gt 300000"` |
| **`select`** | `List[str]` | Fields to include | `["ListingId", "Price"]` |
| **`orderby`** | `str` | Sorting specification | `"ListPrice desc"` |
| **`count`** | `bool` | Include total count | `count=True` |

### Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| **`eq`** | Equal to | `"StandardStatus eq 'Active'"` |
| **`ne`** | Not equal to | `"ListPrice ne 0"` |
| **`gt`** | Greater than | `"ListPrice gt 500000"` |
| **`ge`** | Greater than or equal | `"BedroomsTotal ge 3"` |
| **`lt`** | Less than | `"DaysOnMarket lt 30"` |
| **`le`** | Less than or equal | `"ListPrice le 1000000"` |
| **`and`** | Logical AND | `"Active and Price gt 300000"` |
| **`or`** | Logical OR | `"City eq 'Provo' or City eq 'Orem'"` |
| **`contains`** | String contains | `"contains(City, 'Lake')"` |

---

## 🔍 Response Format

### Standard Response Structure

All API responses follow the OData standard format:

```python
{
    "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#Property",
    "@odata.count": 1234,  # Total count (if count=True)
    "value": [             # Array of results
        {
            # Resource data
            "ListingId": "12345678",
            "ListPrice": 450000,
            # ... more fields
        }
    ]
}
```

### Client Response Processing

The client automatically extracts the `value` array:

```python
# Raw API response includes @odata.* metadata
# Client returns just the data array
properties = client.property.get_properties(top=5)

# properties is a list of dictionaries
for prop in properties:
    print(f"{prop['ListingId']}: ${prop['ListPrice']:,}")
```

### Error Responses

API errors are automatically converted to appropriate exceptions:

```python
from wfrmls.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)

try:
    property_data = client.property.get_property("invalid_id")
except NotFoundError:
    print("Property not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

---

## 📖 Detailed Documentation

### Core Resources

| Module | Description | Key Methods |
|--------|-------------|-------------|
| **[Client](client.md)** | Main client initialization | `WFRMLSClient()` |
| **[Properties](properties.md)** | Property listings and details | `get_properties()`, `get_property()` |
| **[Members](members.md)** | Real estate agent information | `get_members()`, `get_member()` |
| **[Offices](offices.md)** | Brokerage and office data | `get_offices()`, `get_office()` |
| **[Open Houses](openhouses.md)** | Open house schedules | `get_openhouses()`, `get_openhouse()` |
| **[Analytics](analytics.md)** | Market analytics and insights | `get_analytics()`, `get_analytic()` |

### Extended Resources

| Module | Description | Key Methods |
|--------|-------------|-------------|
| **[Lookup](lookup.md)** | Reference data and codes | `get_lookup_values()` |
| **[ADU](adu.md)** | Accessory dwelling units | `get_adu_data()` |
| **[Deleted](deleted.md)** | Deleted record tracking | `get_deleted_listings()` |
| **[Data System](data-system.md)** | System metadata | `get_system_info()` |
| **[History](history.md)** | Property and listing history | `get_history()` |
| **[Media](media.md)** | Property photos and media | `get_media()` |

### Error Handling

| Exception | Description | When Raised |
|-----------|-------------|-------------|
| **[WFRMLSError](exceptions.md#wfrmlserror)** | Base exception class | All API errors |
| **[AuthenticationError](exceptions.md#authenticationerror)** | Invalid credentials | 401, 403 responses |
| **[NotFoundError](exceptions.md#notfounderror)** | Resource not found | 404 responses |
| **[ValidationError](exceptions.md#validationerror)** | Invalid parameters | 400 responses |
| **[RateLimitError](exceptions.md#ratelimiterror)** | Rate limit exceeded | 429 responses |

---

## 🎯 Common Patterns

### Pagination

```python
# Manual pagination
page_size = 100
skip = 0

while True:
    properties = client.property.get_properties(
        top=page_size,
        skip=skip,
        filter_query="StandardStatus eq 'Active'"
    )
    
    if not properties:
        break
        
    # Process this page
    for prop in properties:
        print(f"Processing {prop['ListingId']}")
    
    skip += page_size
```

### Field Selection

```python
# Request only needed fields for better performance
properties = client.property.get_properties(
    select=[
        "ListingId",
        "ListPrice", 
        "StandardStatus",
        "City",
        "BedroomsTotal"
    ],
    top=100
)
```

### Complex Filtering

```python
# Combine multiple conditions
recent_expensive = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "ListPrice ge 750000 and "
        "ModificationTimestamp ge 2024-01-01T00:00:00Z and "
        "contains(City, 'Salt Lake')"
    ),
    orderby="ModificationTimestamp desc"
)
```

---

## 📚 Related Documentation

### **Getting Started**
- **[Installation](../getting-started/installation.md)** - Package installation
- **[Authentication](../getting-started/authentication.md)** - API credentials
- **[Quick Start](../getting-started/quickstart.md)** - First API calls

### **Guides**
- **[Property Search](../guides/property-search.md)** - Advanced property queries
- **[Error Handling](../guides/error-handling.md)** - Robust error management
- **[OData Queries](../guides/odata-queries.md)** - Complex filtering syntax

### **Examples**
- **[Basic Usage](../examples/basic-usage.md)** - Common patterns
- **[Advanced Queries](../examples/advanced-queries.md)** - Complex examples
- **[Real Estate Apps](../examples/real-estate-apps.md)** - Complete applications

---

## 🆘 Support

### **API Issues**
- **[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)** - Report bugs
- **[GitHub Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Ask questions

### **Account & Access**
- **[WFRMLS Support](https://vendor.utahrealestate.com)** - API access issues
- **[Vendor Dashboard](https://vendor.utahrealestate.com)** - Manage credentials

---

*Looking for something specific? Use the search function or browse the detailed module documentation above.* 