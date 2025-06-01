# Properties API

Complete reference for the Properties endpoint of the WFRMLS Python client.

---

## 🏠 Overview

The Properties API provides access to property listings, including residential, commercial, and land listings. This is the most commonly used endpoint for retrieving property data from the WFRMLS.

### Key Features

- **Property listings** - Search and retrieve property data
- **Individual properties** - Get detailed information for specific listings
- **Advanced filtering** - Use OData queries for complex searches
- **Field selection** - Request only the data you need
- **Pagination** - Handle large result sets efficiently

---

## 📚 Methods

### `get_properties()`

Retrieve multiple property listings with optional filtering and pagination.

```python
def get_properties(
    top: Optional[int] = None,
    skip: Optional[int] = None,
    filter_query: Optional[str] = None,
    select: Optional[List[str]] = None,
    orderby: Optional[str] = None,
    count: bool = False
) -> List[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top` | `Optional[int]` | `None` | Maximum number of results to return |
| `skip` | `Optional[int]` | `None` | Number of results to skip (for pagination) |
| `filter_query` | `Optional[str]` | `None` | OData filter expression |
| `select` | `Optional[List[str]]` | `None` | List of fields to include in response |
| `orderby` | `Optional[str]` | `None` | Field(s) to sort by with optional direction |
| `count` | `bool` | `False` | Include total count in response metadata |

**Returns:**
- `List[Dict[str, Any]]` - List of property dictionaries

**Raises:**
- `ValidationError` - Invalid query parameters
- `AuthenticationError` - Invalid API credentials
- `RateLimitError` - API rate limit exceeded
- `WFRMLSError` - Other API errors

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Basic usage - get first 10 active properties
properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    top=10
)

# Advanced filtering with field selection
luxury_homes = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "ListPrice ge 750000 and "
        "BedroomsTotal ge 4"
    ),
    select=["ListingId", "ListPrice", "Address", "City", "BedroomsTotal"],
    orderby="ListPrice desc",
    top=25
)

# Pagination example
page_1 = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="ListingId asc",
    top=50,
    skip=0
)

page_2 = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="ListingId asc",
    top=50,
    skip=50
)

# Count total results
result_with_count = client.property.get_properties(
    filter_query="City eq 'Salt Lake City'",
    count=True,
    top=10
)
```

### `get_property()`

Retrieve detailed information for a specific property by listing ID.

```python
def get_property(listing_id: str) -> Optional[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `listing_id` | `str` | Unique property listing identifier |

**Returns:**
- `Optional[Dict[str, Any]]` - Property dictionary or `None` if not found

**Raises:**
- `NotFoundError` - Property not found
- `ValidationError` - Invalid listing ID format
- `AuthenticationError` - Invalid API credentials
- `WFRMLSError` - Other API errors

**Examples:**

```python
# Get specific property
property_detail = client.property.get_property("12345678")

if property_detail:
    print(f"Property: {property_detail['Address']}")
    print(f"Price: ${property_detail['ListPrice']:,}")
    print(f"Bedrooms: {property_detail.get('BedroomsTotal', 'N/A')}")
else:
    print("Property not found")

# Error handling
try:
    property_data = client.property.get_property("invalid_id")
except NotFoundError:
    print("Property does not exist")
except ValidationError:
    print("Invalid listing ID format")
```

---

## 🏷️ Field Reference

### Core Fields

These fields are commonly available across all property types:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListingId** | `string` | Unique property identifier | `"12345678"` |
| **StandardStatus** | `string` | Current listing status | `"Active"`, `"Pending"`, `"Sold"` |
| **ListPrice** | `integer` | Current asking price | `450000` |
| **OriginalListPrice** | `integer` | Initial listing price | `475000` |
| **Address** | `string` | Full property address | `"123 Main Street"` |
| **City** | `string` | Property city | `"Salt Lake City"` |
| **StateOrProvince** | `string` | State abbreviation | `"UT"` |
| **PostalCode** | `string` | ZIP code | `"84101"` |
| **County** | `string` | County name | `"Salt Lake"` |

### Property Details

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **PropertyType** | `string` | Type of property | `"Residential"`, `"Condominium"`, `"Land"` |
| **BedroomsTotal** | `integer` | Total number of bedrooms | `3` |
| **BathroomsTotal** | `decimal` | Total bathrooms (with decimals) | `2.5` |
| **BathroomsTotalInteger** | `integer` | Total bathrooms (integer only) | `2` |
| **SquareFeet** | `integer` | Living area square footage | `2150` |
| **LotSizeSquareFeet** | `integer` | Lot size in square feet | `8712` |
| **YearBuilt** | `integer` | Year property was built | `1998` |
| **Stories** | `decimal` | Number of stories | `2.0` |

### Financial Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListPrice** | `integer` | Current asking price | `450000` |
| **OriginalListPrice** | `integer` | Initial asking price | `475000` |
| **PreviousListPrice** | `integer` | Previous listing price | `460000` |
| **ClosePrice** | `integer` | Final sale price | `440000` |
| **PricePerSquareFoot** | `decimal` | Price per square foot | `209.30` |
| **TaxAnnualAmount** | `decimal` | Annual property taxes | `3250.00` |
| **HOAFee** | `decimal` | Monthly HOA fee | `125.00` |

### Location and Geography

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **Latitude** | `decimal` | GPS latitude coordinate | `40.7589` |
| **Longitude** | `decimal` | GPS longitude coordinate | `-111.8883` |
| **MapCoordinateSource** | `string` | Source of coordinates | `"Geocoder"` |
| **StreetName** | `string` | Street name only | `"Main Street"` |
| **StreetNumber** | `string` | House number | `"123"` |
| **UnitNumber** | `string` | Unit or apartment number | `"A"` |
| **Directions** | `string` | Driving directions | `"Take I-15 to Exit 300"` |

### Listing Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OnMarketDate** | `datetime` | Date listed on market | `"2024-01-15T00:00:00Z"` |
| **OffMarketDate** | `datetime` | Date removed from market | `"2024-02-15T00:00:00Z"` |
| **DaysOnMarket** | `integer` | Days currently on market | `45` |
| **CumulativeDaysOnMarket** | `integer` | Total days on market | `60` |
| **ModificationTimestamp** | `datetime` | Last modified date/time | `"2024-01-20T14:30:00Z"` |
| **PriceChangeTimestamp** | `datetime` | Last price change date | `"2024-01-18T09:00:00Z"` |

### Agent and Office Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListAgentKey** | `string` | Listing agent identifier | `"AGT123456"` |
| **ListAgentFullName** | `string` | Listing agent name | `"John Smith"` |
| **ListAgentEmail** | `string` | Listing agent email | `"john@example.com"` |
| **ListAgentPhone** | `string` | Listing agent phone | `"801-555-0123"` |
| **ListOfficeKey** | `string` | Listing office identifier | `"OFF789"` |
| **ListOfficeName** | `string` | Listing office name | `"ABC Realty"` |
| **CoListAgentKey** | `string` | Co-listing agent identifier | `"AGT654321"` |

### Property Features

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **Garage** | `string` | Garage description | `"2 Car Attached"` |
| **GarageSpaces** | `integer` | Number of garage spaces | `2` |
| **ParkingTotal** | `integer` | Total parking spaces | `3` |
| **Appliances** | `string` | Included appliances | `"Dishwasher, Microwave"` |
| **Flooring** | `string` | Flooring types | `"Hardwood, Carpet"` |
| **Heating** | `string` | Heating system | `"Forced Air, Gas"` |
| **Cooling** | `string` | Cooling system | `"Central Air"` |
| **Pool** | `string` | Pool information | `"In Ground, Heated"` |

### Descriptive Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **PublicRemarks** | `string` | Public description | `"Beautiful home with..."` |
| **PrivateRemarks** | `string` | Agent-only remarks | `"Seller motivated"` |
| **ShowingInstructions** | `string` | Showing instructions | `"Call listing agent"` |
| **InternetEntireListingDisplay** | `boolean` | Display on internet | `true` |
| **InternetAddressDisplay** | `boolean` | Display address online | `true` |

---

## 🔍 Common Query Patterns

### Basic Searches

```python
# Active properties
active_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'"
)

# Properties in specific city
salt_lake_properties = client.property.get_properties(
    filter_query="City eq 'Salt Lake City' and StandardStatus eq 'Active'"
)

# Price range search
mid_range_homes = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "ListPrice ge 300000 and "
        "ListPrice le 600000"
    )
)
```

### Advanced Filters

```python
# Family homes with specific criteria
family_homes = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "PropertyType eq 'Residential' and "
        "BedroomsTotal ge 3 and "
        "BathroomsTotalInteger ge 2 and "
        "SquareFeet ge 2000"
    ),
    select=[
        "ListingId", "Address", "ListPrice", "BedroomsTotal",
        "BathroomsTotalInteger", "SquareFeet"
    ],
    orderby="ListPrice asc"
)

# Recently updated properties
from datetime import datetime, timedelta

week_ago = (datetime.now() - timedelta(days=7)).isoformat()
recent_updates = client.property.get_properties(
    filter_query=f"ModificationTimestamp ge {week_ago}",
    orderby="ModificationTimestamp desc"
)

# Properties with price reductions
price_drops = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "ListPrice lt OriginalListPrice"
    ),
    select=[
        "ListingId", "Address", "ListPrice", "OriginalListPrice",
        "PriceChangeTimestamp"
    ],
    orderby="PriceChangeTimestamp desc"
)
```

### Geographic Searches

```python
# Properties with coordinates
properties_with_coords = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "Latitude ne null and "
        "Longitude ne null"
    ),
    select=["ListingId", "Address", "ListPrice", "Latitude", "Longitude"]
)

# Properties in specific ZIP codes
target_zips = ['84101', '84102', '84103']
zip_filter = " or ".join([f"PostalCode eq '{zip}'" for zip in target_zips])

zip_properties = client.property.get_properties(
    filter_query=f"StandardStatus eq 'Active' and ({zip_filter})"
)

# Approximate proximity search (simplified)
downtown_lat, downtown_lon = 40.7589, -111.8883
tolerance = 0.01  # Roughly 0.7 miles

near_downtown = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        f"abs(Latitude sub {downtown_lat}) le {tolerance} and "
        f"abs(Longitude sub {downtown_lon}) le {tolerance}"
    )
)
```

### Agent and Office Queries

```python
# Properties by specific agent
agent_listings = client.property.get_properties(
    filter_query="ListAgentKey eq 'AGT123456' and StandardStatus eq 'Active'",
    select=[
        "ListingId", "Address", "ListPrice", "DaysOnMarket",
        "ListAgentFullName"
    ]
)

# Properties by office
office_listings = client.property.get_properties(
    filter_query="ListOfficeKey eq 'OFF789' and StandardStatus eq 'Active'",
    select=[
        "ListingId", "Address", "ListPrice", "ListAgentFullName",
        "ListOfficeName"
    ]
)
```

---

## 📊 Pagination Examples

### Manual Pagination

```python
def paginate_properties(page_size=100):
    """Manually paginate through all active properties."""
    
    all_properties = []
    skip = 0
    
    while True:
        batch = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            top=page_size,
            skip=skip,
            orderby="ListingId asc"  # Consistent ordering
        )
        
        if not batch:
            break
            
        all_properties.extend(batch)
        skip += page_size
        
        print(f"Retrieved {len(all_properties)} properties so far...")
    
    return all_properties

# Usage
all_active_properties = paginate_properties()
print(f"Total: {len(all_active_properties)} active properties")
```

### Page-Based Navigation

```python
class PropertyPaginator:
    """Helper class for page-based property navigation."""
    
    def __init__(self, filter_query="StandardStatus eq 'Active'", page_size=50):
        self.filter_query = filter_query
        self.page_size = page_size
        self.client = WFRMLSClient()
    
    def get_page(self, page_number: int) -> dict:
        """Get specific page of results (1-indexed)."""
        
        skip = (page_number - 1) * self.page_size
        
        properties = self.client.property.get_properties(
            filter_query=self.filter_query,
            top=self.page_size,
            skip=skip,
            orderby="ListingId asc",
            count=True
        )
        
        # Calculate pagination info
        total_count = len(properties)  # This would need to be extracted from metadata
        total_pages = (total_count + self.page_size - 1) // self.page_size
        
        return {
            'properties': properties,
            'page_number': page_number,
            'page_size': self.page_size,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_next': page_number < total_pages,
            'has_previous': page_number > 1
        }

# Usage
paginator = PropertyPaginator()

# Get first page
page_1 = paginator.get_page(1)
print(f"Page 1: {len(page_1['properties'])} properties")

# Get next page
if page_1['has_next']:
    page_2 = paginator.get_page(2)
    print(f"Page 2: {len(page_2['properties'])} properties")
```

---

## ⚡ Performance Tips

### Field Selection Optimization

```python
# ❌ Inefficient - retrieves all fields
all_fields = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    top=100
)

# ✅ Efficient - only needed fields
minimal_fields = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "Address", "City"],
    top=100
)

# Field sets for different use cases
FIELD_SETS = {
    'list_view': [
        'ListingId', 'ListPrice', 'Address', 'City', 'BedroomsTotal',
        'BathroomsTotalInteger', 'SquareFeet'
    ],
    'map_view': [
        'ListingId', 'ListPrice', 'Address', 'Latitude', 'Longitude'
    ],
    'detail_view': [
        'ListingId', 'ListPrice', 'Address', 'City', 'PostalCode',
        'BedroomsTotal', 'BathroomsTotalInteger', 'SquareFeet',
        'YearBuilt', 'PropertyType', 'PublicRemarks'
    ]
}

# Use appropriate field set
list_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    select=FIELD_SETS['list_view'],
    top=50
)
```

### Query Optimization

```python
# ❌ Slow - expensive string operations
slow_query = client.property.get_properties(
    filter_query="contains(tolower(PublicRemarks), 'pool') and StandardStatus eq 'Active'"
)

# ✅ Fast - indexed fields first
fast_query = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and contains(PublicRemarks, 'pool')"
)

# ❌ Slow - complex calculations in filter
slow_calc = client.property.get_properties(
    filter_query="(ListPrice div SquareFeet) le 200"
)

# ✅ Fast - use client-side filtering for complex calculations
properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and SquareFeet gt 0",
    select=["ListingId", "ListPrice", "SquareFeet"]
)

# Filter client-side
affordable_per_sqft = [
    prop for prop in properties 
    if (prop['ListPrice'] / prop['SquareFeet']) <= 200
]
```

---

## 🚨 Error Handling

### Common Error Scenarios

```python
from wfrmls.exceptions import (
    ValidationError, NotFoundError, AuthenticationError, 
    RateLimitError, WFRMLSError
)

def robust_property_search(filter_query, **kwargs):
    """Property search with comprehensive error handling."""
    
    try:
        return client.property.get_properties(
            filter_query=filter_query,
            **kwargs
        )
        
    except ValidationError as e:
        print(f"❌ Invalid query parameters: {e}")
        # Log the problematic filter query
        print(f"Filter: {filter_query}")
        return []
        
    except AuthenticationError:
        print("❌ Authentication failed - check API credentials")
        return []
        
    except RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        # Could implement retry logic here
        return []
        
    except WFRMLSError as e:
        print(f"❌ API error: {e}")
        return []

# Usage with validation
def safe_property_lookup(listing_id):
    """Safe property lookup with validation."""
    
    # Validate listing ID format
    if not isinstance(listing_id, str) or len(listing_id) != 8:
        print("❌ Invalid listing ID format (should be 8-character string)")
        return None
    
    try:
        return client.property.get_property(listing_id)
        
    except NotFoundError:
        print(f"❌ Property {listing_id} not found")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Examples
properties = robust_property_search("StandardStatus eq 'Active'", top=10)
property_detail = safe_property_lookup("12345678")
```

---

## 📚 Related Documentation

### **Guides**
- **[Property Search Guide](../guides/property-search.md)** - Advanced search patterns and techniques
- **[OData Queries Guide](../guides/odata-queries.md)** - Complete OData syntax reference
- **[Error Handling Guide](../guides/error-handling.md)** - Robust error handling patterns

### **Reference**
- **[Field Reference](../reference/fields.md)** - Complete field documentation
- **[Status Codes](../reference/status-codes.md)** - API response codes
- **[Data Types](../reference/data-types.md)** - Field types and formats

### **Examples**
- **[Basic Usage](../examples/basic-usage.md)** - Simple property query examples
- **[Advanced Queries](../examples/advanced-queries.md)** - Complex search patterns
- **[Real Estate Apps](../examples/real-estate-apps.md)** - Complete application examples

---

*Need help with property searches? Check out our [Property Search Guide](../guides/property-search.md) for advanced techniques.* 