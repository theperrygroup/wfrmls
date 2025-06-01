# Property API

The Property API provides comprehensive access to property listings, search functionality, and property details. This is the primary resource for real estate data in the WFRMLS system.

!!! example "Quick Start"
    ```python
    # Get active properties
    properties = client.property.get_active_properties(top=50)
    
    # Search by location
    nearby = client.property.search_properties_by_radius(
        latitude=40.7608, longitude=-111.8910, radius_miles=10
    )
    
    # Get property details
    property_detail = client.property.get_property("12345678")
    ```

## Property Client

::: wfrmls.properties.PropertyClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### Basic Property Retrieval

=== "Active Properties"
    ```python
    # Get the first 50 active properties
    properties = client.property.get_active_properties(top=50)
    
    # Get active properties ordered by list price
    expensive_properties = client.property.get_active_properties(
        orderby="ListPrice desc",
        top=25
    )
    ```

=== "Property Details"
    ```python
    # Get a specific property by ID
    property_detail = client.property.get_property("12345678")
    
    # Get property with expanded related data
    property_expanded = client.property.get_property_with_expansion(
        listing_id="12345678",
        expand="Media,OpenHouse"
    )
    ```

=== "Property History"
    ```python
    # Get properties modified in the last 24 hours
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    recent_changes = client.property.get_properties(
        filter_query=f"ModificationTimestamp ge {yesterday.isoformat()}Z",
        orderby="ModificationTimestamp desc"
    )
    ```

### Advanced Search and Filtering

=== "Geographic Search"
    ```python
    # Search within radius (Salt Lake City downtown)
    downtown_properties = client.property.search_properties_by_radius(
        latitude=40.7608,
        longitude=-111.8910, 
        radius_miles=5,
        top=100
    )
    
    # Search by city
    park_city_properties = client.property.get_properties(
        filter_query="City eq 'Park City'",
        orderby="ListPrice desc"
    )
    ```

=== "Price and Size Filters"
    ```python
    # Luxury properties ($1M+, 3000+ sqft)
    luxury_properties = client.property.get_properties(
        filter_query="ListPrice ge 1000000 and LivingArea ge 3000",
        orderby="ListPrice desc",
        top=50
    )
    
    # Properties with specific bedroom/bathroom count
    family_homes = client.property.get_properties(
        filter_query="BedroomsTotal ge 4 and BathroomsTotalInteger ge 3",
        orderby="ListPrice asc"
    )
    ```

=== "Status and Date Filters"
    ```python
    # Recently listed properties (last 7 days)
    from datetime import datetime, timedelta
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_listings = client.property.get_properties(
        filter_query=f"ListingContractDate ge {week_ago}",
        orderby="ListingContractDate desc"
    )
    
    # Properties with specific status
    active_properties = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        top=100
    )
    ```

### Specialized Searches

=== "Property Type Filtering"
    ```python
    # Single family homes only
    single_family = client.property.get_properties(
        filter_query="PropertyType eq 'Residential' and PropertySubType eq 'Single Family Residence'",
        top=50
    )
    
    # Condos and townhomes
    condos_townhomes = client.property.get_properties(
        filter_query="PropertySubType in ('Condominium', 'Townhouse')",
        top=50
    )
    ```

=== "Amenities and Features"
    ```python
    # Properties with pools
    pool_properties = client.property.get_properties(
        filter_query="PoolPrivateYN eq true",
        top=25
    )
    
    # Properties with garages
    garage_properties = client.property.get_properties(
        filter_query="GarageSpaces ge 2",
        orderby="GarageSpaces desc"
    )
    ```

=== "Agent and Office Filters"
    ```python
    # Properties by specific agent
    agent_listings = client.property.get_properties(
        filter_query="ListAgentKey eq '12345'",
        orderby="ListingContractDate desc"
    )
    
    # Properties by office
    office_listings = client.property.get_properties(
        filter_query="ListOfficeKey eq '67890'",
        top=100
    )
    ```

## Property Data Structure

Properties in WFRMLS follow the RESO standard with extensive field coverage:

??? info "Key Property Fields"
    **Identification & Status**
    
    - `ListingId` - Unique listing identifier
    - `StandardStatus` - Current listing status (Active, Pending, Sold, etc.)
    - `MlsStatus` - MLS-specific status information
    - `ListingContractDate` - Date property was listed
    - `ModificationTimestamp` - Last modification date

    **Location & Address**
    
    - `UnparsedAddress` - Full property address
    - `StreetNumber`, `StreetName`, `StreetSuffix` - Address components
    - `City`, `StateOrProvince`, `PostalCode` - Geographic location
    - `Latitude`, `Longitude` - Geographic coordinates
    - `CountyOrParish` - County information

    **Property Details**
    
    - `PropertyType` - Residential, Commercial, Land, etc.
    - `PropertySubType` - Single Family, Condo, Townhouse, etc.
    - `BedroomsTotal` - Number of bedrooms
    - `BathroomsTotalInteger` - Number of bathrooms
    - `LivingArea` - Square footage of living space
    - `LotSizeAcres` - Lot size in acres

    **Financial Information**
    
    - `ListPrice` - Current listing price
    - `OriginalListPrice` - Initial listing price
    - `SoldPrice` - Sale price (if sold)
    - `ClosePrice` - Final closing price
    - `TaxAssessedValue` - Assessed value for taxes

## Pagination and Performance

### Efficient Data Retrieval

```python
# Use top parameter to limit results
properties = client.property.get_properties(top=50)

# Implement pagination for large datasets
def get_all_properties_paginated(client, page_size=100):
    skip = 0
    all_properties = []
    
    while True:
        page = client.property.get_properties(
            top=page_size,
            skip=skip,
            count=True
        )
        
        properties = page.get('value', [])
        if not properties:
            break
            
        all_properties.extend(properties)
        skip += page_size
        
        # Check if we've got all records
        total_count = page.get('@odata.count')
        if total_count and len(all_properties) >= total_count:
            break
    
    return all_properties
```

### Performance Best Practices

!!! tip "Optimization Tips"
    **Efficient Queries**
    
    - Use specific filters to reduce result set size
    - Order by indexed fields when possible (ListPrice, ModificationTimestamp)
    - Limit results with `top` parameter
    
    **Field Selection**
    
    ```python
    # Select only needed fields
    properties = client.property.get_properties(
        select="ListingId,ListPrice,Address,City,BedroomsTotal,BathroomsTotalInteger",
        top=100
    )
    ```
    
    **Caching Considerations**
    
    - Cache property details for frequently accessed listings
    - Use modification timestamps to detect changes
    - Implement local storage for large datasets

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError, RateLimitError

try:
    # Try to get a property
    property_detail = client.property.get_property("12345678")
    
except NotFoundError:
    print("❌ Property not found - it may have been deleted or the ID is incorrect")
    
except ValidationError as e:
    print(f"📝 Invalid search parameters: {e}")
    
except RateLimitError:
    print("⏱️ Rate limit exceeded - please wait before making more requests")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Integration Examples

### Real Estate Dashboard

```python
def create_market_summary(client, city="Salt Lake City"):
    """Create a market summary for a specific city."""
    
    # Get active properties
    active_properties = client.property.get_properties(
        filter_query=f"City eq '{city}' and StandardStatus eq 'Active'",
        select="ListingId,ListPrice,BedroomsTotal,LivingArea,PropertySubType",
        top=1000
    )
    
    properties = active_properties.get('value', [])
    
    if not properties:
        return {"error": f"No active properties found in {city}"}
    
    # Calculate statistics
    prices = [p.get('ListPrice', 0) for p in properties if p.get('ListPrice')]
    
    summary = {
        "city": city,
        "total_active": len(properties),
        "avg_price": sum(prices) / len(prices) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "property_types": {}
    }
    
    # Count by property type
    for prop in properties:
        prop_type = prop.get('PropertySubType', 'Unknown')
        summary["property_types"][prop_type] = summary["property_types"].get(prop_type, 0) + 1
    
    return summary

# Usage
market_data = create_market_summary(client, "Park City")
print(f"📊 Market Summary for {market_data['city']}:")
print(f"   Active Listings: {market_data['total_active']}")
print(f"   Average Price: ${market_data['avg_price']:,.0f}")
```

### Property Matching System

```python
def find_matching_properties(client, criteria):
    """Find properties matching specific buyer criteria."""
    
    filters = []
    
    # Price range
    if criteria.get('min_price'):
        filters.append(f"ListPrice ge {criteria['min_price']}")
    if criteria.get('max_price'):
        filters.append(f"ListPrice le {criteria['max_price']}")
    
    # Bedrooms/bathrooms
    if criteria.get('min_bedrooms'):
        filters.append(f"BedroomsTotal ge {criteria['min_bedrooms']}")
    if criteria.get('min_bathrooms'):
        filters.append(f"BathroomsTotalInteger ge {criteria['min_bathrooms']}")
    
    # Location
    if criteria.get('cities'):
        city_filter = " or ".join([f"City eq '{city}'" for city in criteria['cities']])
        filters.append(f"({city_filter})")
    
    # Property type
    if criteria.get('property_types'):
        type_filter = " or ".join([f"PropertySubType eq '{ptype}'" for ptype in criteria['property_types']])
        filters.append(f"({type_filter})")
    
    # Combine filters
    filter_query = " and ".join(filters) if filters else None
    
    # Search
    results = client.property.get_properties(
        filter_query=filter_query,
        orderby="ListPrice asc",
        top=50
    )
    
    return results.get('value', [])

# Usage
buyer_criteria = {
    'min_price': 400000,
    'max_price': 800000, 
    'min_bedrooms': 3,
    'min_bathrooms': 2,
    'cities': ['Salt Lake City', 'West Valley City'],
    'property_types': ['Single Family Residence', 'Townhouse']
}

matches = find_matching_properties(client, buyer_criteria)
print(f"🎯 Found {len(matches)} matching properties")
``` 