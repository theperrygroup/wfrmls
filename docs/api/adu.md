# ADU API

The ADU (Accessory Dwelling Unit) API provides access to accessory dwelling unit information within the WFRMLS system. This includes details about secondary housing units on properties, such as mother-in-law apartments, basement units, and detached ADUs.

## Overview

The `AduClient` class handles all ADU-related operations, providing methods to search, retrieve, and filter accessory dwelling unit data.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
adus = client.adu.get_adus(top=10)
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_adus()` | Retrieve multiple ADUs with filtering | `List[Dict[str, Any]]` |
| `get_adu()` | Get a specific ADU by ID | `Dict[str, Any]` |
| `search_adus()` | Search ADUs by criteria | `List[Dict[str, Any]]` |
| `get_property_adus()` | Get ADUs for a specific property | `List[Dict[str, Any]]` |

## Methods

### get_adus()

Retrieve multiple ADUs with optional filtering, sorting, and pagination.

```python
def get_adus(
    self,
    select: Optional[List[str]] = None,
    filter_query: Optional[str] = None,
    orderby: Optional[str] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    count: bool = False,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `select` | `List[str]` | No | Specific fields to return |
| `filter_query` | `str` | No | OData filter expression |
| `orderby` | `str` | No | Field(s) to sort by |
| `top` | `int` | No | Maximum number of records to return |
| `skip` | `int` | No | Number of records to skip |
| `count` | `bool` | No | Include total count in response |

#### Examples

=== "Basic Usage"

    ```python
    # Get first 10 ADUs
    adus = client.adu.get_adus(
        top=10,
        filter_query="AduStatus eq 'Active'"
    )
    
    for adu in adus:
        print(f"ADU {adu['AduKey']}: {adu['AduType']}")
    ```

=== "Specific Fields"

    ```python
    # Get only specific fields
    adus = client.adu.get_adus(
        select=["AduKey", "ListingId", "AduType", "AduBedrooms", "AduBathrooms"],
        filter_query="AduStatus eq 'Active'",
        orderby="AduType"
    )
    ```

=== "Type Filtering"

    ```python
    # Find specific ADU types
    basement_adus = client.adu.get_adus(
        filter_query="AduType eq 'Basement' and AduStatus eq 'Active'",
        orderby="ListingId asc"
    )
    ```

### get_adu()

Retrieve a specific ADU by its unique identifier.

```python
def get_adu(
    self,
    adu_key: str,
    select: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adu_key` | `str` | Yes | Unique ADU identifier |
| `select` | `List[str]` | No | Specific fields to return |

#### Example

```python
# Get specific ADU details
adu = client.adu.get_adu(
    adu_key="12345",
    select=["AduKey", "ListingId", "AduType", "AduBedrooms", "AduBathrooms", "AduSquareFeet"]
)

print(f"ADU: {adu['AduType']}")
print(f"Bedrooms: {adu['AduBedrooms']}")
print(f"Bathrooms: {adu['AduBathrooms']}")
print(f"Square Feet: {adu['AduSquareFeet']}")
```

### search_adus()

Search for ADUs using various criteria.

```python
def search_adus(
    self,
    listing_id: Optional[str] = None,
    adu_type: Optional[AduType] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[float] = None,
    status: Optional[AduStatus] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `listing_id` | `str` | No | Associated property listing ID |
| `adu_type` | `AduType` | No | Type of ADU |
| `bedrooms` | `int` | No | Number of bedrooms |
| `bathrooms` | `float` | No | Number of bathrooms |
| `status` | `AduStatus` | No | ADU status |

#### Example

```python
from wfrmls import AduType, AduStatus

# Search by type
detached_adus = client.adu.search_adus(
    adu_type=AduType.DETACHED,
    status=AduStatus.ACTIVE
)

# Search by size
large_adus = client.adu.search_adus(
    bedrooms=2,
    bathrooms=1.0,
    status=AduStatus.ACTIVE
)
```

### get_property_adus()

Retrieve all ADUs associated with a specific property.

```python
def get_property_adus(
    self,
    listing_id: str,
    select: Optional[List[str]] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `listing_id` | `str` | Yes | Property listing identifier |
| `select` | `List[str]` | No | Specific fields to return |

#### Example

```python
# Get all ADUs for a property
property_adus = client.adu.get_property_adus(
    listing_id="1611952",
    select=["AduKey", "AduType", "AduBedrooms", "AduBathrooms", "AduSquareFeet"]
)

print(f"Property has {len(property_adus)} ADUs:")
for adu in property_adus:
    print(f"  {adu['AduType']}: {adu['AduBedrooms']}BR/{adu['AduBathrooms']}BA")
```

## Enums and Constants

### AduStatus

Enumeration of possible ADU statuses:

```python
from wfrmls import AduStatus

class AduStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"
    COMPLETED = "Completed"
```

### AduType

Enumeration of ADU types:

```python
from wfrmls import AduType

class AduType(str, Enum):
    BASEMENT = "Basement"
    DETACHED = "Detached"
    ATTACHED = "Attached"
    GARAGE_CONVERSION = "Garage Conversion"
    MOTHER_IN_LAW = "Mother-in-Law"
    STUDIO = "Studio"
```

## Common Use Cases

### Property ADU Analysis

```python
# Analyze ADU distribution across properties
def analyze_adu_distribution():
    adus = client.adu.get_adus(
        filter_query="AduStatus eq 'Active'",
        select=["AduKey", "ListingId", "AduType", "AduBedrooms", "AduBathrooms"]
    )
    
    # Group by type
    type_distribution = {}
    for adu in adus:
        adu_type = adu['AduType']
        if adu_type not in type_distribution:
            type_distribution[adu_type] = 0
        type_distribution[adu_type] += 1
    
    # Display results
    print("ADU Distribution by Type:")
    for adu_type, count in sorted(type_distribution.items()):
        print(f"  {adu_type}: {count} units")
    
    return type_distribution

distribution = analyze_adu_distribution()
```

### Investment Property Search

```python
# Find properties with income-generating ADUs
def find_investment_properties():
    # Get properties with ADUs
    adus = client.adu.get_adus(
        filter_query="AduStatus eq 'Active' and AduBedrooms ge 1",
        select=["AduKey", "ListingId", "AduType", "AduBedrooms", "AduBathrooms", "AduSquareFeet"]
    )
    
    # Group by property
    properties_with_adus = {}
    for adu in adus:
        listing_id = adu['ListingId']
        if listing_id not in properties_with_adus:
            properties_with_adus[listing_id] = []
        properties_with_adus[listing_id].append(adu)
    
    # Find properties with multiple or large ADUs
    investment_candidates = []
    for listing_id, property_adus in properties_with_adus.items():
        total_bedrooms = sum(adu['AduBedrooms'] for adu in property_adus)
        if len(property_adus) > 1 or total_bedrooms >= 2:
            investment_candidates.append({
                'listing_id': listing_id,
                'adu_count': len(property_adus),
                'total_adu_bedrooms': total_bedrooms,
                'adus': property_adus
            })
    
    return investment_candidates

investment_properties = find_investment_properties()
```

### ADU Market Report

```python
# Generate ADU market report
def generate_adu_market_report():
    adus = client.adu.get_adus(
        filter_query="AduStatus eq 'Active'",
        select=[
            "AduKey", "ListingId", "AduType", "AduBedrooms", 
            "AduBathrooms", "AduSquareFeet", "AduRentAmount"
        ]
    )
    
    # Calculate statistics
    total_adus = len(adus)
    avg_bedrooms = sum(adu.get('AduBedrooms', 0) for adu in adus) / total_adus if total_adus > 0 else 0
    avg_bathrooms = sum(adu.get('AduBathrooms', 0) for adu in adus) / total_adus if total_adus > 0 else 0
    avg_sqft = sum(adu.get('AduSquareFeet', 0) for adu in adus if adu.get('AduSquareFeet')) / total_adus if total_adus > 0 else 0
    
    # Rent analysis
    rented_adus = [adu for adu in adus if adu.get('AduRentAmount')]
    avg_rent = sum(adu['AduRentAmount'] for adu in rented_adus) / len(rented_adus) if rented_adus else 0
    
    report = {
        'total_adus': total_adus,
        'average_bedrooms': round(avg_bedrooms, 1),
        'average_bathrooms': round(avg_bathrooms, 1),
        'average_square_feet': round(avg_sqft, 0),
        'average_rent': round(avg_rent, 2),
        'rental_units': len(rented_adus)
    }
    
    print("ADU Market Report:")
    print(f"  Total ADUs: {report['total_adus']}")
    print(f"  Average Bedrooms: {report['average_bedrooms']}")
    print(f"  Average Bathrooms: {report['average_bathrooms']}")
    print(f"  Average Square Feet: {report['average_square_feet']}")
    print(f"  Rental Units: {report['rental_units']}")
    print(f"  Average Rent: ${report['average_rent']}")
    
    return report

market_report = generate_adu_market_report()
```

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `AduKey` | `str` | Unique ADU identifier |
| `ListingId` | `str` | Associated property listing ID |
| `AduType` | `str` | Type of ADU (Basement, Detached, etc.) |
| `AduStatus` | `str` | Current status |
| `AduDescription` | `str` | Detailed description |

### Size and Layout

| Field | Type | Description |
|-------|------|-------------|
| `AduBedrooms` | `int` | Number of bedrooms |
| `AduBathrooms` | `float` | Number of bathrooms |
| `AduSquareFeet` | `int` | Total square footage |
| `AduLivingArea` | `int` | Living area square footage |

### Features and Amenities

| Field | Type | Description |
|-------|------|-------------|
| `AduKitchen` | `bool` | Has kitchen |
| `AduLaundry` | `bool` | Has laundry facilities |
| `AduParking` | `bool` | Has dedicated parking |
| `AduSeparateEntrance` | `bool` | Has separate entrance |
| `AduUtilities` | `str` | Utility arrangement |

### Financial Information

| Field | Type | Description |
|-------|------|-------------|
| `AduRentAmount` | `float` | Monthly rent amount |
| `AduRentIncludes` | `str` | What rent includes |
| `AduDeposit` | `float` | Security deposit amount |
| `AduLeaseTerms` | `str` | Lease term options |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `OriginalEntryTimestamp` | `datetime` | When record was created |
| `ModificationTimestamp` | `datetime` | Last modification time |

## Advanced Filtering

### Size-based Queries

```python
# Find large ADUs suitable for families
large_family_adus = client.adu.get_adus(
    filter_query="""
        AduBedrooms ge 2 and 
        AduBathrooms ge 1.5 and 
        AduSquareFeet ge 800 and
        AduStatus eq 'Active'
    """,
    orderby="AduSquareFeet desc"
)
```

### Feature-based Search

```python
# Find self-contained ADUs
self_contained_adus = client.adu.get_adus(
    filter_query="""
        AduKitchen eq true and 
        AduSeparateEntrance eq true and 
        AduParking eq true and
        AduStatus eq 'Active'
    """,
    orderby="AduRentAmount desc"
)
```

### Investment Analysis

```python
# Find high-yield rental ADUs
high_yield_adus = client.adu.get_adus(
    filter_query="""
        AduRentAmount ge 1000 and 
        AduBedrooms ge 1 and
        AduStatus eq 'Active'
    """,
    select=[
        "AduKey", "ListingId", "AduType", "AduBedrooms", 
        "AduBathrooms", "AduRentAmount", "AduSquareFeet"
    ],
    orderby="AduRentAmount desc"
)

# Calculate rent per square foot
for adu in high_yield_adus:
    if adu.get('AduSquareFeet') and adu.get('AduRentAmount'):
        rent_per_sqft = adu['AduRentAmount'] / adu['AduSquareFeet']
        print(f"ADU {adu['AduKey']}: ${rent_per_sqft:.2f}/sqft")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    adu = client.adu.get_adu("invalid_key")
except NotFoundError:
    print("ADU not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Use specific filters** to limit result sets
2. **Select only needed fields** to reduce data transfer
3. **Cache ADU data** for properties when appropriate
4. **Use pagination** for large queries

### Data Analysis

1. **Validate ADU data** before calculations
2. **Handle missing values** appropriately
3. **Consider market context** in analysis
4. **Track changes over time** for trends

### Investment Analysis

1. **Calculate rent-to-size ratios** for comparison
2. **Consider location factors** in valuation
3. **Analyze utility arrangements** for costs
4. **Evaluate parking availability** for desirability

## Integration Examples

### Property Listing Enhancement

```python
# Enhance property listings with ADU information
def enhance_property_with_adu_info(property_data):
    listing_id = property_data.get('ListingId')
    if not listing_id:
        return property_data
    
    # Get ADUs for this property
    adus = client.adu.get_property_adus(
        listing_id,
        select=["AduKey", "AduType", "AduBedrooms", "AduBathrooms", "AduRentAmount"]
    )
    
    # Enhance property data
    enhanced = property_data.copy()
    enhanced['AdusCount'] = len(adus)
    enhanced['AdusDetails'] = adus
    
    # Calculate potential rental income
    total_rent = sum(adu.get('AduRentAmount', 0) for adu in adus)
    enhanced['AduRentalIncome'] = total_rent
    
    return enhanced

# Usage
properties = client.property.get_properties(top=10)
enhanced_properties = [enhance_property_with_adu_info(prop) for prop in properties]
```

### Investment Calculator

```python
# Calculate ADU investment potential
def calculate_adu_investment_potential(listing_id: str):
    # Get property ADUs
    adus = client.adu.get_property_adus(
        listing_id,
        select=[
            "AduKey", "AduType", "AduBedrooms", "AduBathrooms",
            "AduSquareFeet", "AduRentAmount", "AduUtilities"
        ]
    )
    
    if not adus:
        return {"has_adus": False}
    
    # Calculate metrics
    total_rent = sum(adu.get('AduRentAmount', 0) for adu in adus)
    total_sqft = sum(adu.get('AduSquareFeet', 0) for adu in adus)
    avg_rent_per_sqft = total_rent / total_sqft if total_sqft > 0 else 0
    
    analysis = {
        "has_adus": True,
        "adu_count": len(adus),
        "total_monthly_rent": total_rent,
        "annual_rental_income": total_rent * 12,
        "total_adu_sqft": total_sqft,
        "avg_rent_per_sqft": round(avg_rent_per_sqft, 2),
        "adu_details": adus
    }
    
    return analysis

# Usage
investment_analysis = calculate_adu_investment_potential("1611952")
if investment_analysis["has_adus"]:
    print(f"Annual rental income potential: ${investment_analysis['annual_rental_income']:,}")
```

## Related Resources

- [Properties API](properties.md) - For main property information
- [Lookup API](lookup.md) - For ADU type and status codes
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management