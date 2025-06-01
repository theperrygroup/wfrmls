# Quick Start

Get started with the WFRMLS Python client in under 5 minutes. This guide walks you through making your first API call and exploring basic functionality.

---

## 🚀 Your First API Call

### Step 1: Install and Import

```python
from wfrmls import WFRMLSClient

# Initialize the client (uses WFRMLS_BEARER_TOKEN environment variable)
client = WFRMLSClient()

# Or initialize with explicit token
# client = WFRMLSClient(bearer_token="your_bearer_token_here")
```

### Step 2: Fetch Properties

```python
# Get the first 5 active properties
properties = client.property.get_properties(
    top=5,
    filter_query="StandardStatus eq 'Active'"
)

print(f"Found {len(properties)} properties")
for prop in properties:
    print(f"- {prop['ListingId']}: ${prop['ListPrice']:,} in {prop.get('City', 'Unknown')}")
```

### Step 3: Explore Property Details

```python
# Get a specific property by listing ID
if properties:
    listing_id = properties[0]['ListingId']
    property_detail = client.property.get_property(listing_id)
    
    print(f"\nProperty Details for {listing_id}:")
    print(f"Address: {property_detail.get('StreetName', 'N/A')}")
    print(f"Price: ${property_detail.get('ListPrice', 0):,}")
    print(f"Bedrooms: {property_detail.get('BedroomsTotal', 'N/A')}")
    print(f"Bathrooms: {property_detail.get('BathroomsTotalInteger', 'N/A')}")
```

---

## 🎯 Testing Your Installation

Run this complete test script to verify everything is working:

```python
"""
WFRMLS Client Test Script
Run this to verify your installation and API access.
"""

import os
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError, AuthenticationError

def test_client():
    """Test basic client functionality."""
    
    # Check environment variable
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    if not token:
        print("❌ WFRMLS_BEARER_TOKEN environment variable not set")
        print("Set it with: export WFRMLS_BEARER_TOKEN='your_token_here'")
        return False
    
    try:
        # Initialize client
        client = WFRMLSClient()
        print("✅ Client initialized successfully")
        
        # Test API call
        properties = client.property.get_properties(top=1)
        print(f"✅ API call successful - retrieved {len(properties)} property")
        
        # Test different endpoints
        members = client.member.get_members(top=1)
        print(f"✅ Members endpoint - retrieved {len(members)} member")
        
        offices = client.office.get_offices(top=1)
        print(f"✅ Offices endpoint - retrieved {len(offices)} office")
        
        print("\n🎉 All tests passed! Your setup is working correctly.")
        return True
        
    except AuthenticationError:
        print("❌ Authentication failed - check your bearer token")
        return False
    except WFRMLSError as e:
        print(f"❌ API error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_client()
```

---

## 🔍 Understanding Responses

### Response Structure

All WFRMLS API responses follow the OData standard:

```python
{
    "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#Property",
    "@odata.count": 1234,  # Total count (if $count=true)
    "value": [             # Array of results
        {
            "ListingId": "12345678",
            "ListPrice": 450000,
            "StandardStatus": "Active",
            # ... more fields
        }
    ]
}
```

### Working with Data

```python
# The client returns the 'value' array directly
properties = client.property.get_properties(top=10)

# Each item is a dictionary
for prop in properties:
    listing_id = prop['ListingId']
    price = prop.get('ListPrice', 0)  # Use .get() for optional fields
    status = prop['StandardStatus']
    
    print(f"{listing_id}: ${price:,} - {status}")
```

---

## 🚀 Exploring Other Endpoints

### Real Estate Agents (Members)

```python
# Get active agents
agents = client.member.get_members(
    filter_query="MemberStatus eq 'Active'",
    top=10
)

for agent in agents:
    print(f"{agent['MemberFullName']} - {agent.get('MemberEmail', 'No email')}")
```

### Offices and Brokerages

```python
# Get office information
offices = client.office.get_offices(top=5)

for office in offices:
    print(f"{office['OfficeName']} in {office.get('OfficeCity', 'Unknown')}")
```

### Open Houses

```python
# Get upcoming open houses
from datetime import datetime

open_houses = client.openhouse.get_open_houses(
    filter_query=f"OpenHouseDate ge {datetime.now().isoformat()}",
    top=10
)

for oh in open_houses:
    print(f"Open House: {oh['OpenHouseDate']} - {oh.get('ListingId', 'N/A')}")
```

---

## 🎯 Common Use Cases

### Property Search with Filters

```python
# Search for properties in a price range
expensive_homes = client.property.get_properties(
    filter_query="ListPrice ge 500000 and ListPrice le 1000000 and StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "City", "BedroomsTotal", "BathroomsTotalInteger"],
    orderby="ListPrice desc",
    top=20
)

print(f"Found {len(expensive_homes)} homes between $500K-$1M")
```

### Recently Updated Properties

```python
from datetime import datetime, timedelta

# Properties modified in the last 7 days
week_ago = (datetime.now() - timedelta(days=7)).isoformat()

recent_updates = client.property.get_properties(
    filter_query=f"ModificationTimestamp ge {week_ago}",
    orderby="ModificationTimestamp desc",
    top=50
)

print(f"Found {len(recent_updates)} recently updated properties")
```

### Agent Contact Information

```python
# Find agents by name or email
agent_search = client.member.get_members(
    filter_query="contains(MemberFullName, 'Smith')",
    select=["MemberKey", "MemberFullName", "MemberEmail", "MemberMobilePhone"]
)

for agent in agent_search:
    print(f"{agent['MemberFullName']}: {agent.get('MemberEmail', 'No email')}")
```

---

## ⚠️ Error Handling

### Basic Error Handling

```python
from wfrmls.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    WFRMLSError
)

try:
    properties = client.property.get_properties()
    
except AuthenticationError:
    print("Invalid API token - check your credentials")
    
except RateLimitError:
    print("Rate limit exceeded - wait before making more requests")
    
except ValidationError as e:
    print(f"Invalid request parameters: {e}")
    
except NotFoundError:
    print("Requested resource not found")
    
except WFRMLSError as e:
    print(f"API error: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Robust Error Handling with Retries

```python
import time
from wfrmls.exceptions import RateLimitError

def fetch_with_retry(func, max_retries=3, **kwargs):
    """Fetch data with automatic retry on rate limits."""
    
    for attempt in range(max_retries):
        try:
            return func(**kwargs)
            
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
                
        except Exception:
            raise

# Usage
properties = fetch_with_retry(
    client.property.get_properties,
    top=100,
    filter_query="StandardStatus eq 'Active'"
)
```

---

## 📚 Next Steps

!!! success "You're Ready!"
    Congratulations! You've successfully made your first WFRMLS API calls. Here's where to go next:

### **Learn More**
- **[Property Search Guide](../guides/property-search.md)** - Advanced property filtering
- **[Error Handling Guide](../guides/error-handling.md)** - Robust error management
- **[API Reference](../api/index.md)** - Complete method documentation

### **Build Something**
- **[Real Estate Apps](../examples/real-estate-apps.md)** - Complete application examples
- **[Data Integration](../examples/data-integration.md)** - Sync with your systems
- **[Advanced Queries](../examples/advanced-queries.md)** - Complex search examples

### **Get Help**
- **[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)** - Report bugs
- **[Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Ask questions
- **[WFRMLS Support](https://vendor.utahrealestate.com)** - API access issues

---

*Ready for more advanced features? Check out our [Guides](../guides/index.md) section for in-depth tutorials.* 