# API Reference

Comprehensive API documentation for the WFRMLS Python client.

---

## 📚 Available Endpoints

### Core Resources

- **[Properties](properties.md)** - Search and retrieve property listings
- **[Members](members.md)** - Access real estate agent and broker information
- **[Offices](offices.md)** - Get brokerage and office details
- **[OpenHouse](openhouse.md)** - Find scheduled open house events

### Specialized Endpoints

- **[ADU](adu.md)** - Accessory Dwelling Unit information
- **[Property Unit Types](property-unit-types.md)** - Multi-unit property details
- **[Lookup](lookup.md)** - Enumeration values and reference data
- **[Deleted](deleted.md)** - Track deleted records for synchronization

### System Endpoints

- **[Resource](resource.md)** - Discover available API endpoints
- **[Data System](data-system.md)** - API version and configuration information

---

## � Quick Start

```python
from wfrmls import WFRMLSClient

# Initialize client
client = WFRMLSClient(bearer_token="your_token_here")

# Search properties
properties = client.property.get_properties(
    filter_query="ListPrice ge 500000 and ListPrice le 750000",
    select=["ListingKey", "UnparsedAddress", "ListPrice"],
    top=10
)

# Get agent information
member = client.member.get_member_by_mls_id("123456")

# Find open houses
open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=7)
```

---

## 📊 Common Patterns

### Pagination

All endpoints support pagination using `top` and `skip` parameters:

```python
# Get results in pages of 50
page_size = 50
page = 0

while True:
    results = client.property.get_properties(
        top=page_size,
        skip=page * page_size
    )
    
    if not results["value"]:
        break
        
    # Process results
    for property in results["value"]:
        process_property(property)
    
    page += 1
```

### Field Selection

Use the `select` parameter to request only needed fields:

```python
# Get only specific fields
results = client.property.get_properties(
    select=["ListingKey", "UnparsedAddress", "ListPrice", "BedroomsTotal"]
)
```

### Filtering

Use OData filter syntax for complex queries:

```python
# Complex filter example
filter_query = (
    "StandardStatus eq 'Active' and "
    "BedroomsTotal ge 3 and "
    "ListPrice ge 400000 and ListPrice le 600000"
)

results = client.property.get_properties(filter_query=filter_query)
```

### Sorting

Control result order with the `orderby` parameter:

```python
# Sort by price descending
results = client.property.get_properties(
    orderby="ListPrice desc"
)

# Multiple sort fields
results = client.property.get_properties(
    orderby="City asc, ListPrice desc"
)
```

---

## �️ Response Structure

All endpoints return a consistent OData response format:

```json
{
    "@odata.context": "$metadata#EntityType",
    "value": [
        // Array of results
    ],
    "@odata.count": 12345,  // When count=true
    "@odata.nextLink": "https://..."  // When more pages available
}
```

The actual data is always in the `value` array.

---

## ⚡ Best Practices

1. **Use field selection** - Only request fields you need to reduce payload size
2. **Implement pagination** - Always paginate large result sets
3. **Cache lookup values** - Store enumeration values locally
4. **Handle rate limits** - Implement retry logic with exponential backoff
5. **Monitor deletions** - Regularly sync deleted records
6. **Validate data** - Always validate critical fields exist before use

---

## � Related Documentation

- [Authentication Guide](../guides/authentication.md)
- [OData Query Syntax](../reference/odata-syntax.md)
- [Error Handling](../guides/error-handling.md)
- [Examples](../examples/index.md) 