# First Steps

Now that you have the WFRMLS package installed and authentication configured, let's explore the core concepts and take your first steps with the API.

## 🎯 Core Concepts

### Understanding the WFRMLS API

The WFRMLS (Wasatch Front Regional Multiple Listing Service) API provides access to real estate data following the RESO (Real Estate Standards Organization) standards. Key concepts include:

- **Resources**: Different data types (Properties, Members, Offices, etc.)
- **OData v4**: Query standard for filtering, sorting, and pagination
- **Bearer Token**: Authentication method for API access
- **Rate Limits**: Usage constraints to ensure fair access

### Key Data Types

<div class="grid cards" markdown>

-   :material-home:{ .lg .middle } **Properties**

    ---

    Real estate listings with detailed information about homes, condos, land, and commercial properties

-   :material-account-group:{ .lg .middle } **Members**

    ---

    Real estate agents and brokers registered with the MLS

-   :material-office-building:{ .lg .middle } **Offices**

    ---

    Real estate offices and brokerages where agents work

-   :material-calendar:{ .lg .middle } **Open Houses**

    ---

    Scheduled property showings and events

</div>

## 🚀 Your First API Calls

Let's start with some basic examples to get you familiar with the API:

### 1. Initialize the Client

```python
from wfrmls import WFRMLSClient

# Initialize client (loads token from environment)
client = WFRMLSClient()
print("✅ Client initialized successfully!")
```

### 2. Explore Available Resources

```python
# Get service document to see what's available
service_doc = client.get_service_document()

print("📋 Available Resources:")
for resource in service_doc.get('value', []):
    name = resource.get('name', 'Unknown')
    title = resource.get('title', 'No description')
    print(f"   • {name}: {title}")
```

### 3. Get Some Properties

```python
# Get your first 10 properties
properties = client.property.get_active_properties(top=10)

print(f"\n🏠 Found {len(properties.get('value', []))} properties:")
for prop in properties.get('value', [])[:3]:  # Show first 3
    listing_id = prop.get('ListingId', 'Unknown')
    price = prop.get('ListPrice', 0)
    city = prop.get('City', 'Unknown')
    address = prop.get('UnparsedAddress', 'Unknown Address')
    
    print(f"   📍 {listing_id}: {address}, {city} - ${price:,}")
```

### 4. Search for Agents

```python
# Get some active real estate agents
agents = client.member.get_active_members(top=5)

print(f"\n👥 Found {len(agents.get('value', []))} agents:")
for agent in agents.get('value', []):
    first_name = agent.get('MemberFirstName', '')
    last_name = agent.get('MemberLastName', '')
    email = agent.get('MemberEmail', 'No email')
    
    print(f"   🤝 {first_name} {last_name} - {email}")
```

## 📖 Understanding Responses

WFRMLS API responses follow the OData v4 format:

```json
{
    "@odata.context": "https://api.wfrmls.com/RETS/api/$metadata#Property",
    "@odata.count": 1250,
    "value": [
        {
            "ListingId": "12345678",
            "ListPrice": 750000,
            "City": "Salt Lake City",
            "@odata.etag": "W/\"datetime'2024-01-15T10%3A30%3A00.000Z'\""
        }
    ]
}
```

Key components:

- **`@odata.context`**: Metadata about the response type
- **`@odata.count`**: Total number of records (if requested)
- **`value`**: Array containing the actual data
- **`@odata.etag`**: Version information for change tracking

## 🔍 Basic Filtering and Searching

### Simple Filters

```python
# Properties in a specific city
slc_properties = client.property.get_properties(
    filter_query="City eq 'Salt Lake City'",
    top=20
)

# Properties above a certain price
expensive_properties = client.property.get_properties(
    filter_query="ListPrice gt 500000",
    orderby="ListPrice desc",
    top=10
)

# Active agents in a specific office
office_agents = client.member.get_members(
    filter_query="MemberOfficeKey eq '12345' and MemberStatus eq 'Active'",
    top=50
)
```

### Common Filter Operations

| Operation | Symbol | Example |
|-----------|--------|---------|
| Equals | `eq` | `City eq 'Provo'` |
| Not equals | `ne` | `ListPrice ne null` |
| Greater than | `gt` | `ListPrice gt 300000` |
| Greater or equal | `ge` | `BedroomsTotal ge 3` |
| Less than | `lt` | `LivingArea lt 3000` |
| Less or equal | `le` | `ListPrice le 1000000` |
| Contains | `contains` | `contains(City, 'Salt')` |

### Combining Filters

```python
# Multiple conditions with AND
family_homes = client.property.get_properties(
    filter_query="BedroomsTotal ge 3 and BathroomsTotalInteger ge 2 and ListPrice le 800000",
    orderby="ListPrice asc"
)

# Multiple conditions with OR
utah_county_cities = client.property.get_properties(
    filter_query="City eq 'Provo' or City eq 'Orem' or City eq 'American Fork'",
    top=50
)
```

## 📄 Pagination and Data Management

### Working with Large Result Sets

```python
# Get first page
page1 = client.property.get_properties(top=50)

# Get second page
page2 = client.property.get_properties(top=50, skip=50)

# Include total count
with_count = client.property.get_properties(top=10, count=True)
total_properties = with_count.get('@odata.count', 'Unknown')
print(f"Total properties available: {total_properties}")
```

### Pagination Helper Function

```python
def get_all_pages(client, resource_method, page_size=100, max_pages=None):
    """Get all pages of data from a resource method."""
    all_data = []
    skip = 0
    pages_fetched = 0
    
    while True:
        # Get next page
        page = resource_method(top=page_size, skip=skip)
        page_data = page.get('value', [])
        
        if not page_data:
            break
        
        all_data.extend(page_data)
        skip += page_size
        pages_fetched += 1
        
        print(f"📄 Fetched page {pages_fetched}: {len(page_data)} records")
        
        # Stop if max pages reached
        if max_pages and pages_fetched >= max_pages:
            break
    
    return all_data

# Usage
all_active_properties = get_all_pages(
    client, 
    client.property.get_active_properties,
    page_size=100,
    max_pages=5  # Limit to first 5 pages for testing
)
```

## 🛠️ Error Handling Basics

Always handle potential errors in your API calls:

```python
from wfrmls.exceptions import (
    WFRMLSError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError
)

def safe_api_call():
    """Example of proper error handling."""
    try:
        # Make API call
        properties = client.property.get_properties(top=10)
        
        print("✅ Success!")
        return properties
        
    except AuthenticationError:
        print("❌ Authentication failed - check your token")
        
    except NotFoundError:
        print("🔍 Resource not found")
        
    except RateLimitError:
        print("⏱️ Rate limit exceeded - please wait")
        
    except ValidationError as e:
        print(f"📝 Invalid parameters: {e}")
        
    except WFRMLSError as e:
        print(f"🚨 API error: {e}")
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
    
    return None

# Usage
result = safe_api_call()
```

## 🎯 Common Use Cases

### 1. Property Search by Location

```python
def search_properties_by_city(city_name, max_price=None):
    """Search for properties in a specific city."""
    
    # Build filter query
    filter_parts = [f"City eq '{city_name}'"]
    if max_price:
        filter_parts.append(f"ListPrice le {max_price}")
    
    filter_query = " and ".join(filter_parts)
    
    # Search properties
    properties = client.property.get_properties(
        filter_query=filter_query,
        orderby="ListPrice asc",
        top=50
    )
    
    return properties.get('value', [])

# Usage
park_city_homes = search_properties_by_city("Park City", max_price=1000000)
print(f"Found {len(park_city_homes)} properties in Park City under $1M")
```

### 2. Agent Directory

```python
def create_agent_directory(office_name=None):
    """Create a directory of active agents."""
    
    # Build filter for active agents
    filter_query = "MemberStatus eq 'Active' and MemberType eq 'Agent'"
    
    # Get agents
    agents = client.member.get_members(
        filter_query=filter_query,
        select="MemberFirstName,MemberLastName,MemberEmail,MemberDirectPhone",
        orderby="MemberLastName asc",
        top=100
    )
    
    # Format for display
    directory = []
    for agent in agents.get('value', []):
        directory.append({
            'name': f"{agent.get('MemberFirstName', '')} {agent.get('MemberLastName', '')}".strip(),
            'email': agent.get('MemberEmail', ''),
            'phone': agent.get('MemberDirectPhone', '')
        })
    
    return directory

# Usage
agent_list = create_agent_directory()
for agent in agent_list[:5]:  # Show first 5
    print(f"👤 {agent['name']} - {agent['email']}")
```

### 3. Market Summary

```python
def get_market_summary(city="Salt Lake City"):
    """Get basic market statistics for a city."""
    
    # Get active properties in the city
    properties = client.property.get_properties(
        filter_query=f"City eq '{city}' and StandardStatus eq 'Active'",
        select="ListPrice,BedroomsTotal,LivingArea",
        top=500
    )
    
    props = properties.get('value', [])
    if not props:
        return {"error": f"No properties found in {city}"}
    
    # Calculate statistics
    prices = [p.get('ListPrice', 0) for p in props if p.get('ListPrice')]
    
    summary = {
        'city': city,
        'total_active': len(props),
        'avg_price': sum(prices) / len(prices) if prices else 0,
        'min_price': min(prices) if prices else 0,
        'max_price': max(prices) if prices else 0,
        'median_price': sorted(prices)[len(prices)//2] if prices else 0
    }
    
    return summary

# Usage
market_data = get_market_summary("Provo")
print(f"📊 Market Summary for {market_data['city']}:")
print(f"   Active Listings: {market_data['total_active']}")
print(f"   Average Price: ${market_data['avg_price']:,.0f}")
print(f"   Price Range: ${market_data['min_price']:,.0f} - ${market_data['max_price']:,.0f}")
```

## 📚 What's Next?

Now that you understand the basics, explore these areas:

### 🎯 Deepen Your Knowledge
- **[API Reference](../api/)** - Complete method documentation
- **[Guides](../guides/)** - Detailed how-to guides for specific tasks
- **[Examples](../examples/)** - Real-world code examples

### 🚀 Build Something
- Property search application
- Agent contact management
- Market analysis dashboard
- Open house scheduling system

### 🛠️ Advanced Topics
- [Performance Optimization](../guides/performance-optimization.md)
- [Data Synchronization](../guides/data-synchronization.md)
- [Error Handling](../guides/error-handling.md)

---

*Ready for more? Check out our [Property Search Guide](../guides/property-search.md) to learn advanced search techniques, or browse [Examples](../examples/) for complete applications.* 