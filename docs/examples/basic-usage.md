# Basic Usage Examples

This page provides simple, practical examples to get you started with the WFRMLS Python client.

## Getting Started

### Installation and Setup

```python
# Install the package
# pip install wfrmls

from wfrmls import WFRMLSClient

# Initialize the client
client = WFRMLSClient(bearer_token="your_bearer_token_here")

# Or use environment variable
import os
os.environ['WFRMLS_BEARER_TOKEN'] = "your_bearer_token_here"
client = WFRMLSClient()  # Will use environment variable
```

### Your First API Call

```python
# Get the first 5 properties
properties = client.property.get_properties(top=5)

print(f"Retrieved {len(properties)} properties:")
for prop in properties:
    print(f"- {prop['ListingId']}: ${prop.get('ListPrice', 'N/A'):,}")
```

## Property Examples

### Basic Property Search

```python
# Get active residential properties under $500,000
affordable_homes = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and PropertyType eq 'RES' and ListPrice le 500000",
    select=["ListingId", "ListPrice", "UnparsedAddress", "City", "StandardStatus"],
    top=20,
    orderby="ListPrice asc"
)

print("Affordable homes:")
for home in affordable_homes:
    print(f"${home['ListPrice']:,} - {home['UnparsedAddress']}, {home['City']}")
```

### Get Property Details

```python
# Get detailed information for a specific property
property_id = "1611952"  # Example listing ID

try:
    property_details = client.property.get_property(property_id)
    
    print(f"Property Details for {property_id}:")
    print(f"Address: {property_details.get('UnparsedAddress', 'N/A')}")
    print(f"Price: ${property_details.get('ListPrice', 0):,}")
    print(f"Bedrooms: {property_details.get('BedroomsTotal', 'N/A')}")
    print(f"Bathrooms: {property_details.get('BathroomsTotalInteger', 'N/A')}")
    print(f"Square Feet: {property_details.get('LivingArea', 'N/A'):,}")
    print(f"Status: {property_details.get('StandardStatus', 'N/A')}")
    
except Exception as e:
    print(f"Error retrieving property {property_id}: {e}")
```

### Search by Location

```python
# Find properties in specific cities
cities = ["Salt Lake City", "Park City", "Provo"]
city_filter = " or ".join([f"City eq '{city}'" for city in cities])

city_properties = client.property.get_properties(
    filter_query=f"({city_filter}) and StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "City", "PropertyType"],
    top=50,
    orderby="City asc, ListPrice asc"
)

# Group by city
by_city = {}
for prop in city_properties:
    city = prop['City']
    if city not in by_city:
        by_city[city] = []
    by_city[city].append(prop)

for city, properties in by_city.items():
    print(f"\n{city} ({len(properties)} properties):")
    for prop in properties[:3]:  # Show first 3
        print(f"  ${prop['ListPrice']:,} - {prop['ListingId']}")
```

## Member Examples

### Find Real Estate Agents

```python
# Get active real estate agents
agents = client.member.get_members(
    filter_query="MemberStatus eq 'Active' and MemberType eq 'Agent'",
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail", "MemberMobilePhone"],
    top=10,
    orderby="MemberLastName asc"
)

print("Active Real Estate Agents:")
for agent in agents:
    name = f"{agent['MemberFirstName']} {agent['MemberLastName']}"
    email = agent.get('MemberEmail', 'N/A')
    phone = agent.get('MemberMobilePhone', 'N/A')
    print(f"- {name} | {email} | {phone}")
```

### Get Agent Details

```python
# Get detailed information for a specific agent
agent_key = "12345"  # Example member key

try:
    agent = client.member.get_member(agent_key)
    
    print(f"Agent Profile:")
    print(f"Name: {agent['MemberFirstName']} {agent['MemberLastName']}")
    print(f"Email: {agent.get('MemberEmail', 'N/A')}")
    print(f"Phone: {agent.get('MemberMobilePhone', 'N/A')}")
    print(f"Status: {agent.get('MemberStatus', 'N/A')}")
    print(f"License: {agent.get('MemberStateLicense', 'N/A')}")
    
except Exception as e:
    print(f"Error retrieving agent {agent_key}: {e}")
```

## Office Examples

### Find Real Estate Offices

```python
# Get active real estate offices
offices = client.office.get_offices(
    filter_query="OfficeStatus eq 'Active'",
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeCity"],
    top=15,
    orderby="OfficeName asc"
)

print("Real Estate Offices:")
for office in offices:
    print(f"- {office['OfficeName']} | {office['OfficeCity']} | {office.get('OfficePhone', 'N/A')}")
```

### Get Office Team

```python
# Get all agents working at a specific office
office_key = "67890"  # Example office key

try:
    # Get office details
    office = client.office.get_office(office_key)
    print(f"Office: {office['OfficeName']}")
    
    # Get office team members
    team_members = client.member.get_members(
        filter_query=f"OfficeKey eq '{office_key}' and MemberStatus eq 'Active'",
        select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberType"],
        orderby="MemberLastName asc"
    )
    
    print(f"Team Members ({len(team_members)}):")
    for member in team_members:
        name = f"{member['MemberFirstName']} {member['MemberLastName']}"
        role = member.get('MemberType', 'N/A')
        print(f"  - {name} ({role})")
        
except Exception as e:
    print(f"Error retrieving office team: {e}")
```

## Open House Examples

### Find Upcoming Open Houses

```python
from datetime import datetime, timedelta

# Get open houses for the next 7 days
next_week = datetime.now() + timedelta(days=7)

upcoming_open_houses = client.openhouse.get_open_houses(
    filter_query=f"OpenHouseDate ge datetime'{datetime.now().isoformat()}Z' and OpenHouseDate le datetime'{next_week.isoformat()}Z'",
    select=["OpenHouseKey", "ListingId", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime"],
    top=20,
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)

print("Upcoming Open Houses:")
for oh in upcoming_open_houses:
    date = oh['OpenHouseDate'][:10]  # Extract date part
    start_time = oh['OpenHouseStartTime']
    end_time = oh['OpenHouseEndTime']
    print(f"- {date} {start_time}-{end_time}: Property {oh['ListingId']}")
```

### Open Houses by Property

```python
# Get all open houses for a specific property
property_id = "1611952"

property_open_houses = client.openhouse.get_open_houses(
    filter_query=f"ListingId eq '{property_id}'",
    select=["OpenHouseKey", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseStatus"],
    orderby="OpenHouseDate desc"
)

print(f"Open Houses for Property {property_id}:")
for oh in property_open_houses:
    date = oh['OpenHouseDate'][:10]
    time_range = f"{oh['OpenHouseStartTime']}-{oh['OpenHouseEndTime']}"
    status = oh.get('OpenHouseStatus', 'N/A')
    print(f"- {date} {time_range} ({status})")
```

## Lookup Examples

### Get Reference Data

```python
# Get property types
property_types = client.lookup.get_property_types()
print("Property Types:")
for pt in property_types:
    print(f"- {pt['LookupKey']}: {pt['LookupValue']}")

print("\n" + "="*50 + "\n")

# Get property statuses
statuses = client.lookup.get_property_statuses()
print("Property Statuses:")
for status in statuses:
    print(f"- {status['LookupKey']}: {status['LookupValue']}")

print("\n" + "="*50 + "\n")

# Get cities
cities = client.lookup.get_cities()
print(f"Available Cities ({len(cities)}):")
for city in cities[:10]:  # Show first 10
    print(f"- {city['LookupValue']}")
if len(cities) > 10:
    print(f"... and {len(cities) - 10} more")
```

## Error Handling Examples

### Basic Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError, RateLimitError

def safe_property_lookup(listing_id):
    """Safely look up a property with error handling."""
    try:
        property_data = client.property.get_property(listing_id)
        return property_data
    
    except NotFoundError:
        print(f"Property {listing_id} not found")
        return None
    
    except ValidationError as e:
        print(f"Invalid request for property {listing_id}: {e}")
        return None
    
    except RateLimitError as e:
        print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
property_data = safe_property_lookup("1611952")
if property_data:
    print(f"Found property: {property_data['UnparsedAddress']}")
```

### Batch Operations with Error Handling

```python
def get_multiple_properties(listing_ids):
    """Get multiple properties with individual error handling."""
    results = {}
    
    for listing_id in listing_ids:
        try:
            property_data = client.property.get_property(listing_id)
            results[listing_id] = {
                "success": True,
                "data": property_data
            }
        except Exception as e:
            results[listing_id] = {
                "success": False,
                "error": str(e)
            }
    
    return results

# Usage
listing_ids = ["1611952", "1234567", "invalid_id"]
results = get_multiple_properties(listing_ids)

for listing_id, result in results.items():
    if result["success"]:
        prop = result["data"]
        print(f"✓ {listing_id}: {prop['UnparsedAddress']}")
    else:
        print(f"✗ {listing_id}: {result['error']}")
```

## Pagination Examples

### Handling Large Result Sets

```python
def get_all_active_properties():
    """Get all active properties using pagination."""
    all_properties = []
    batch_size = 100
    skip = 0
    
    while True:
        batch = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            select=["ListingId", "ListPrice", "City"],
            top=batch_size,
            skip=skip,
            orderby="ListingId asc"
        )
        
        if not batch:
            break
        
        all_properties.extend(batch)
        skip += batch_size
        
        print(f"Retrieved {len(all_properties)} properties so far...")
        
        # Break if we got less than batch size (last batch)
        if len(batch) < batch_size:
            break
    
    return all_properties

# Usage (be careful with large datasets!)
# all_properties = get_all_active_properties()
# print(f"Total active properties: {len(all_properties)}")
```

## Filtering Examples

### Price Range Searches

```python
# Different price ranges
price_ranges = [
    {"name": "Under $300K", "max": 300000},
    {"name": "$300K - $500K", "min": 300000, "max": 500000},
    {"name": "$500K - $1M", "min": 500000, "max": 1000000},
    {"name": "Over $1M", "min": 1000000}
]

for price_range in price_ranges:
    # Build filter
    filters = ["StandardStatus eq 'Active'", "PropertyType eq 'RES'"]
    
    if "min" in price_range:
        filters.append(f"ListPrice ge {price_range['min']}")
    if "max" in price_range:
        filters.append(f"ListPrice le {price_range['max']}")
    
    filter_query = " and ".join(filters)
    
    # Get count
    properties = client.property.get_properties(
        filter_query=filter_query,
        select=["ListingId"],
        top=1,
        count=True
    )
    
    # Note: count functionality depends on API implementation
    print(f"{price_range['name']}: {len(properties)} properties")
```

### Date-Based Searches

```python
from datetime import datetime, timedelta

# Properties listed in the last 30 days
thirty_days_ago = datetime.now() - timedelta(days=30)

recent_listings = client.property.get_properties(
    filter_query=f"OriginalEntryTimestamp ge datetime'{thirty_days_ago.isoformat()}Z' and StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "OriginalEntryTimestamp", "UnparsedAddress"],
    top=20,
    orderby="OriginalEntryTimestamp desc"
)

print("Recent Listings (Last 30 Days):")
for prop in recent_listings:
    entry_date = prop['OriginalEntryTimestamp'][:10]  # Extract date part
    print(f"- {entry_date}: ${prop['ListPrice']:,} - {prop['UnparsedAddress']}")
```

## Utility Functions

### Helper Functions for Common Tasks

```python
def format_price(price):
    """Format price for display."""
    if price is None:
        return "N/A"
    return f"${price:,}"

def format_address(property_data):
    """Format property address for display."""
    address = property_data.get('UnparsedAddress', '')
    city = property_data.get('City', '')
    state = property_data.get('StateOrProvince', '')
    zip_code = property_data.get('PostalCode', '')
    
    parts = [address, city, state, zip_code]
    return ", ".join([part for part in parts if part])

def get_property_summary(listing_id):
    """Get a formatted summary of a property."""
    try:
        prop = client.property.get_property(listing_id)
        
        summary = {
            "listing_id": listing_id,
            "address": format_address(prop),
            "price": format_price(prop.get('ListPrice')),
            "bedrooms": prop.get('BedroomsTotal', 'N/A'),
            "bathrooms": prop.get('BathroomsTotalInteger', 'N/A'),
            "sqft": prop.get('LivingArea', 'N/A'),
            "status": prop.get('StandardStatus', 'N/A'),
            "property_type": prop.get('PropertyType', 'N/A')
        }
        
        return summary
        
    except Exception as e:
        return {"error": str(e)}

# Usage
summary = get_property_summary("1611952")
if "error" not in summary:
    print(f"Property Summary:")
    print(f"  Address: {summary['address']}")
    print(f"  Price: {summary['price']}")
    print(f"  Beds/Baths: {summary['bedrooms']}/{summary['bathrooms']}")
    print(f"  Sq Ft: {summary['sqft']}")
    print(f"  Status: {summary['status']}")
else:
    print(f"Error: {summary['error']}")
```

## Next Steps

Once you're comfortable with these basic examples, explore:

- [Advanced Queries](advanced-queries.md) - Complex filtering and searching
- [Real Estate Apps](real-estate-apps.md) - Building complete applications
- [Data Integration](data-integration.md) - Integrating with other systems
- [Property Search Guide](../guides/property-search.md) - Detailed search strategies
- [Error Handling Guide](../guides/error-handling.md) - Robust error handling patterns