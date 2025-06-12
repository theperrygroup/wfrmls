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
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top` | `Optional[int]` | `None` | Maximum number of results to return (max 200) |
| `skip` | `Optional[int]` | `None` | Number of results to skip (for pagination) |
| `filter_query` | `Optional[str]` | `None` | OData filter expression |
| `select` | `Optional[List[str]]` | `None` | List of fields to include in response |
| `orderby` | `Optional[str]` | `None` | Field(s) to sort by with optional direction |
| `count` | `bool` | `False` | Include total count in response metadata |

**Returns:**
- `Dict[str, Any]` - Response dictionary containing:
  - `@odata.context`: OData context URL
  - `value`: List of property dictionaries
  - `@odata.count`: Total count (if requested)
  - `@odata.nextLink`: URL for next page of results

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
response = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    top=10
)
properties = response["value"]

# Advanced filtering with field selection
luxury_response = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "ListPrice ge 750000 and "
        "BedroomsTotal ge 4"
    ),
    select=["ListingId", "ListPrice", "City", "BedroomsTotal"],
    orderby="ListPrice desc",
    top=25
)

# Pagination using @odata.nextLink
first_page = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    top=50
)

# If there's a next page
if "@odata.nextLink" in first_page:
    # Extract skip value from nextLink for next page
    # The nextLink contains the full URL with skip parameter
    pass

# Count total results
result_with_count = client.property.get_properties(
    filter_query="City eq 'Salt Lake City'",
    count=True,
    top=10
)
total_properties = result_with_count.get("@odata.count", 0)
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
- `ValidationError` - Invalid listing ID format
- `AuthenticationError` - Invalid API credentials
- `WFRMLSError` - Other API errors

**Examples:**

```python
# Get specific property
property_detail = client.property.get_property("1611952")

if property_detail:
    print(f"Address: {property_detail['UnparsedAddress']}")
    print(f"Price: ${property_detail['ListPrice']:,}")
    print(f"Bedrooms: {property_detail.get('BedroomsTotal', 'N/A')}")
```

---

## 🏷️ Field Reference

### Core Identification Fields

These fields uniquely identify and track properties:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListingKeyNumeric** | `integer` | Numeric listing key | `1611952` |
| **ListingId** | `string` | String listing identifier | `"1611952"` |
| **ListingKey** | `string` | Primary listing key | `"1611952"` |
| **OriginatingSystemID** | `string` | Source system ID | `"M00000628"` |
| **OriginatingSystemKey** | `string` | Source system key | `"2cb5b35c..."` |
| **OriginatingSystemName** | `string` | Source system name | `"UtahRealEstate.com"` |
| **SourceSystemID** | `string` | Source system identifier | `"M00000628"` |
| **SourceSystemKey** | `string` | Source system key | `"M00000628"` |
| **SourceSystemName** | `string` | Source system name | `"UtahRealEstate.com"` |

### Property Status & Type

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **StandardStatus** | `string` | RESO standard status | `"Active"`, `"Pending"`, `"Sold"`, `"Expired"` |
| **MlsStatus** | `string` | MLS-specific status | `"Active"`, `"Expired"` |
| **PropertyType** | `string` | Property category | `"Residential"`, `"Commercial Lease"`, `"Land"` |
| **PropertySubType** | `string` | Property subcategory | `"Single Family Residence"`, `"Condominium"`, `"Retail"` |
| **CurrentUse** | `string` | Current property use | `"Single Family"`, `"Retail"` |

### Address & Location

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **UnparsedAddress** | `string` | Full address string | `"1611 S MAIN ST 200"` |
| **StreetNumber** | `string` | Street number | `"1611"` |
| **StreetNumberNumeric** | `integer` | Numeric street number | `1611` |
| **StreetName** | `string` | Street name | `"MAIN"` |
| **StreetDirPrefix** | `string` | Street direction prefix | `"S"` |
| **StreetDirSuffix** | `string` | Street direction suffix | `""` |
| **StreetSuffix** | `string` | Street type suffix | `"ST"` |
| **UnitNumber** | `string` | Unit/apartment number | `"200"` |
| **City** | `string` | City name | `"Salt Lake City"` |
| **PostalCity** | `string` | Postal city name | `"Salt Lake City"` |
| **StateOrProvince** | `string` | State abbreviation | `"UT"` |
| **PostalCode** | `string` | ZIP code | `"84115"` |
| **PostalCodePlus4** | `string` | ZIP+4 extension | `null` |
| **CountyOrParish** | `string` | County name | `"Salt Lake"` |
| **Country** | `string` | Country code | `"US"` |

### Financial Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListPrice** | `decimal` | Current asking price | `1600.0` |
| **OriginalListPrice** | `decimal` | Initial listing price | `1750.0` |
| **ClosePrice** | `decimal` | Final sale price | `null` |
| **LeaseAmount** | `decimal` | Lease amount (for rentals) | `1600.0` |
| **ConcessionsAmount** | `decimal` | Seller concessions | `null` |
| **TaxAnnualAmount** | `decimal` | Annual property taxes | `6924.0` |
| **AssociationFee** | `decimal` | HOA/Association fee | `null` |
| **AssociationFeeFrequency** | `string` | Fee payment frequency | `""` |

### Property Details

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **BedroomsTotal** | `integer` | Total bedrooms | `2` |
| **BathroomsFull** | `integer` | Full bathrooms | `1` |
| **BathroomsHalf** | `integer` | Half bathrooms | `null` |
| **BathroomsThreeQuarter** | `integer` | Three-quarter bathrooms | `null` |
| **BathroomsTotalInteger** | `integer` | Total bathrooms (integer) | `1` |
| **LivingArea** | `decimal` | Living area square feet | `868.0` |
| **BuildingAreaTotal** | `decimal` | Total building area | `868.0` |
| **AboveGradeFinishedArea** | `decimal` | Above grade finished sqft | `868.0` |
| **YearBuilt** | `integer` | Year constructed | `1993` |
| **YearBuiltEffective** | `integer` | Effective year built | `null` |
| **Stories** | `integer` | Number of stories | `1` |
| **RoomsTotal** | `integer` | Total room count | `5` |

### Lot Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **LotSizeAcres** | `decimal` | Lot size in acres | `0.27` |
| **LotSizeSquareFeet** | `decimal` | Lot size in square feet | `11761.2` |
| **LotSizeArea** | `decimal` | General lot size | `10000.0` |
| **LotSizeDimensions** | `string` | Lot dimensions | `"0.0x0.0x0.0"` |
| **FrontageLength** | `string` | Street frontage | `"0.0"` |

### Parking & Garage

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **GarageSpaces** | `decimal` | Garage parking spaces | `2.0` |
| **CarportSpaces** | `decimal` | Carport spaces | `null` |
| **CoveredSpaces** | `decimal` | Covered parking spaces | `1.0` |
| **OpenParkingSpaces** | `decimal` | Open parking spaces | `null` |
| **ParkingTotal** | `decimal` | Total parking spaces | `2.0` |
| **AttachedGarageYN** | `boolean` | Has attached garage | `false` |
| **CarportYN** | `boolean` | Has carport | `false` |
| **GarageYN** | `boolean` | Has garage | `true` |

### Features & Amenities

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **FireplacesTotal** | `integer` | Number of fireplaces | `null` |
| **FireplaceYN** | `boolean` | Has fireplace | `false` |
| **HeatingYN** | `boolean` | Has heating | `true` |
| **CoolingYN** | `boolean` | Has cooling | `true` |
| **PoolPrivateYN** | `boolean` | Has private pool | `false` |
| **SpaYN** | `boolean` | Has spa/hot tub | `false` |
| **WaterfrontYN** | `boolean` | Is waterfront property | `false` |
| **ViewYN** | `boolean` | Has view | `false` |
| **NewConstructionYN** | `boolean` | Is new construction | `false` |

### Listing Dates & Times

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OnMarketDate** | `datetime` | Date listed | `"2024-12-27"` |
| **OffMarketDate** | `datetime` | Date delisted | `null` |
| **ContractStatusChangeDate** | `datetime` | Contract status change | `"2025-01-29"` |
| **ListingContractDate** | `datetime` | Listing agreement date | `"2024-12-27"` |
| **CloseDate** | `datetime` | Closing date | `null` |
| **ModificationTimestamp** | `datetime` | Last modification | `"2025-01-31T18:48:38Z"` |
| **OriginalEntryTimestamp** | `datetime` | Original entry date | `"2024-12-27T21:56:13Z"` |
| **PhotosChangeTimestamp** | `datetime` | Photos last updated | `"2025-01-24T20:18:07Z"` |
| **PriceChangeTimestamp** | `datetime` | Price last changed | `"2025-01-22T23:11:33Z"` |
| **StatusChangeTimestamp** | `datetime` | Status last changed | `"2025-01-29T17:48:45Z"` |

### Days on Market

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **DaysOnMarket** | `integer` | Current days on market | `35` |
| **CumulativeDaysOnMarket** | `integer` | Total cumulative DOM | `null` |

### Agent & Office Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListAgentKeyNumeric** | `integer` | Listing agent numeric key | `69404` |
| **ListAgentKey** | `string` | Listing agent key | `"69404"` |
| **ListAgentMlsId** | `string` | Agent MLS ID | `"69404"` |
| **ListAgentFirstName** | `string` | Agent first name | `"Andrea"` |
| **ListAgentLastName** | `string` | Agent last name | `"Miller"` |
| **ListAgentFullName** | `string` | Agent full name | `"Andrea Lynn Miller"` |
| **ListAgentPreferredPhone** | `string` | Agent phone | `"801-450-2200"` |
| **ListAgentOfficePhone** | `string` | Office phone | `"801-676-0400"` |
| **ListAgentStateLicense** | `string` | Agent license | `"13757889-SA00"` |
| **ListOfficeKeyNumeric** | `integer` | Office numeric key | `51607` |
| **ListOfficeKey** | `string` | Office key | `"51607"` |
| **ListOfficeMlsId** | `string` | Office MLS ID | `"51607"` |
| **ListOfficeName** | `string` | Office name | `"Equity Real Estate (Solid)"` |

### Additional Details

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **PublicRemarks** | `string` | Public description | `"Beautiful home..."` |
| **ShowingContactName** | `string` | Showing contact | `"Andrea Miller"` |
| **ShowingContactPhone** | `string` | Showing phone | `"801-450-2200"` |
| **Directions** | `string` | Property directions | `""` |
| **VirtualTourURLBranded** | `string` | Branded virtual tour | `null` |
| **VirtualTourURLUnbranded** | `string` | Unbranded virtual tour | `null` |

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