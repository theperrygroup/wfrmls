# Quick Start Guide

Get up and running with the WFRMLS Python API wrapper in 5 minutes.

## 1. Installation

```bash
pip install wfrmls
```

## 2. Set Up Authentication

Set your API key as an environment variable:

```bash
export WFRMLS_BEARER_TOKEN="your_api_key_here"
```

## 3. Basic Usage

### Initialize the Client

```python
from wfrmls import WFRMLSClient

# Initialize client (uses WFRMLS_BEARER_TOKEN environment variable)
client = WFRMLSClient()

# Or provide API key directly
client = WFRMLSClient(api_key="your_api_key_here")
```

### Your First API Call

```python
# Get available resources to verify connection
resources = client.resource.get_resources()
print("Available resources:", [r['resourceName'] for r in resources])
```

## 4. Common Use Cases

### Property Search

```python
# Search for properties in Salt Lake City under $500k
properties = client.properties.search_properties(
    city="Salt Lake City",
    max_list_price=500000,
    property_type="Residential"
)

print(f"Found {len(properties)} properties")

# Get details for the first property
if properties:
    property_id = properties[0]['ListingKey']
    details = client.properties.get_property(property_id)
    print(f"Property address: {details.get('UnparsedAddress')}")
```

### Agent Search

```python
# Search for agents by name
agents = client.member.search_members(
    first_name="John",
    last_name="Smith"
)

print(f"Found {len(agents)} agents named John Smith")

# Get agent details
if agents:
    agent_id = agents[0]['MemberKey']
    agent_details = client.member.get_member(agent_id)
    print(f"Agent: {agent_details.get('MemberFullName')}")
```

### Office Search

```python
# Search for offices in a specific city
offices = client.office.search_offices(
    office_city="Salt Lake City"
)

print(f"Found {len(offices)} offices in Salt Lake City")
```

### Media and Photos

```python
# Get media for a property
property_id = "123456"
media = client.media.search_media(
    resource_name="Property",
    resource_record_key=property_id
)

print(f"Found {len(media)} media items for property {property_id}")

# Download first image
if media:
    media_url = media[0]['MediaURL']
    photo_data = client.media.get_media_object(media_url)
    with open(f"property_{property_id}_photo.jpg", "wb") as f:
        f.write(photo_data)
```

## 5. Error Handling

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError, AuthenticationError

client = WFRMLSClient()

try:
    # Attempt to get property with invalid ID
    property_details = client.properties.get_property("invalid_id")
except AuthenticationError:
    print("Authentication failed - check your API key")
except WFRMLSError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 6. Advanced Features

### Pagination

```python
# Get paginated results
page_1 = client.properties.search_properties(
    city="Salt Lake City",
    page_number=0,
    page_size=25
)

page_2 = client.properties.search_properties(
    city="Salt Lake City", 
    page_number=1,
    page_size=25
)
```

### Filtering and Sorting

```python
from datetime import date

# Advanced property search with filters
properties = client.properties.search_properties(
    city="Salt Lake City",
    min_list_price=200000,
    max_list_price=800000,
    bedrooms_total=3,
    bathrooms_total_integer=2,
    listing_status="Active",
    modification_timestamp_from=date(2024, 1, 1)
)
```

### Analytics and Market Data

```python
# Get market analytics
analytics = client.analytics.get_market_statistics(
    area="Salt Lake County",
    property_type="Residential",
    date_range="last_30_days"
)

print(f"Average price: ${analytics.get('average_price')}")
print(f"Days on market: {analytics.get('average_dom')}")
```

## 7. Working with Different Data Types

### Open Houses

```python
from datetime import date

# Find upcoming open houses
open_houses = client.openhouse.search_open_houses(
    open_house_date_from=date.today(),
    city="Salt Lake City"
)

print(f"Found {len(open_houses)} upcoming open houses")
```

### Lookup Data

```python
# Get reference data
property_types = client.lookup.get_lookup_values("PropertyType")
listing_statuses = client.lookup.get_lookup_values("MlsStatus")

print("Available property types:", property_types)
print("Available listing statuses:", listing_statuses)
```

### History Data

```python
# Get property history
property_id = "123456"
history = client.history.get_property_history(property_id)

print(f"Property has {len(history)} historical records")
```

## 8. Best Practices

### Environment Configuration

Create a `.env` file for local development:

```bash
# .env file
WFRMLS_BEARER_TOKEN=your_api_key_here
```

### Error Handling Pattern

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(client, operation):
    try:
        return operation()
    except WFRMLSError as e:
        logger.error(f"WFRMLS API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

# Usage
client = WFRMLSClient()
properties = safe_api_call(
    client, 
    lambda: client.properties.search_properties(city="Salt Lake City")
)
```

### Rate Limiting

```python
import time

def batch_process_properties(property_ids):
    """Process properties with rate limiting."""
    client = WFRMLSClient()
    results = []
    
    for property_id in property_ids:
        try:
            details = client.properties.get_property(property_id)
            results.append(details)
            
            # Add small delay to respect rate limits
            time.sleep(0.1)
            
        except WFRMLSError as e:
            print(f"Error processing {property_id}: {e}")
            continue
    
    return results
```

## Next Steps

Now that you've learned the basics:

1. **Explore the [Examples](examples.md)** for more detailed use cases
2. **Read the [API Reference](api-reference.md)** for complete endpoint documentation
3. **Check the [Troubleshooting Guide](troubleshooting.md)** if you encounter issues
4. **Review the [Contributing Guide](contributing.md)** if you want to contribute

## Quick Reference

### Most Common Endpoints

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `client.properties.search_properties()` | Search properties | Property listings |
| `client.properties.get_property(id)` | Get property details | Individual property |
| `client.member.search_members()` | Search agents | Agent directory |
| `client.office.search_offices()` | Search offices | Office listings |
| `client.media.search_media()` | Get property media | Photos, documents |
| `client.lookup.get_lookup_values()` | Reference data | Valid values |

### Common Parameters

- `page_number`: Page for pagination (starts at 0)
- `page_size`: Items per page (default 20, max varies by endpoint)
- `modification_timestamp_from`: Get records modified since date
- `listing_status`: Filter by listing status (Active, Sold, etc.)
- `city`: Filter by city name
- `property_type`: Filter by property type

That's it! You're now ready to start building with the WFRMLS API wrapper. 