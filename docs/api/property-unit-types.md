# Property Unit Types API

Complete reference for property unit types endpoints in the WFRMLS Python client.

---

## Overview

The **Property Unit Types** module provides access to property unit type information, including condos, townhomes, apartments, and other unit classifications. This is essential for understanding property categorization and unit-specific details.

### Key Features

- **Unit Type Classification** - Access to different property unit types
- **Property Relationships** - Link unit types to specific properties  
- **Residential Filtering** - Convenience methods for residential unit types
- **Modification Tracking** - Incremental sync capabilities

---

## Class Reference

### PropertyUnitTypesClient

```python
from wfrmls.property_unit_types import PropertyUnitTypesClient

client = PropertyUnitTypesClient(bearer_token="your_token")
```

---

## Core Methods

### get_property_unit_types()

Get property unit types with optional OData filtering.

```python
get_property_unit_types(
    top: Optional[int] = None,
    skip: Optional[int] = None,
    filter_query: Optional[str] = None,
    select: Optional[Union[List[str], str]] = None,
    orderby: Optional[str] = None,
    expand: Optional[Union[List[str], str]] = None,
    count: Optional[bool] = None,
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| **top** | int | No | Number of results to return (max 200) | None |
| **skip** | int | No | Number of results to skip | None |
| **filter_query** | str | No | OData filter expression | None |
| **select** | List[str] \| str | No | Fields to include in response | None |
| **orderby** | str | No | Field(s) to sort by | None |
| **expand** | List[str] \| str | No | Related resources to include | None |
| **count** | bool | No | Include total count in response | None |

#### Examples

=== "Basic Usage"

    ```python
    # Get all unit types
    unit_types = client.property_unit_types.get_property_unit_types()
    
    for unit in unit_types.get('value', []):
        print(f"Unit Type: {unit['UnitType']}")
    ```

=== "Filtered Results"

    ```python
    # Get specific unit types
    condos = client.property_unit_types.get_property_unit_types(
        filter_query="UnitType eq 'Condo'",
        select=["UnitTypeKey", "UnitType", "Description"]
    )
    ```

=== "With Relationships"

    ```python
    # Get unit types with property relationships
    unit_types = client.property_unit_types.get_property_unit_types(
        expand="Properties",
        top=10
    )
    ```

---

### get_property_unit_type()

Get a specific property unit type by its unique key.

```python
get_property_unit_type(unit_type_key: str) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **unit_type_key** | str | Yes | Unique unit type identifier |

#### Example

```python
# Get specific unit type
unit_type = client.property_unit_types.get_property_unit_type("CONDO")

print(f"Unit Type: {unit_type['UnitType']}")
print(f"Description: {unit_type.get('Description', 'No description')}")
```

---

## Convenience Methods

### get_unit_types_for_property()

Get unit types for a specific property.

```python
get_unit_types_for_property(
    listing_key: str, 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **listing_key** | str | Yes | Property listing key to filter by |
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get unit types for a property
property_units = client.property_unit_types.get_unit_types_for_property(
    listing_key="1611952"
)
```

---

### get_unit_types_by_type()

Get properties by unit type classification.

```python
get_unit_types_by_type(
    unit_type: str, 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **unit_type** | str | Yes | Unit type to filter by (e.g., "Condo", "Townhome") |
| **kwargs** | Any | No | Additional OData parameters |

#### Examples

```python
# Get all condo unit types
condos = client.property_unit_types.get_unit_types_by_type(
    unit_type="Condo",
    expand="Properties"
)

# Get all townhome unit types
townhomes = client.property_unit_types.get_unit_types_by_type("Townhome")
```

---

### get_residential_unit_types()

Get residential unit types with common residential classifications.

```python
get_residential_unit_types(**kwargs: Any) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **kwargs** | Any | No | Additional OData parameters |

#### Included Unit Types

- Condo
- Townhome  
- Apartment
- Single Family
- Duplex
- Triplex
- Fourplex

#### Example

```python
# Get all residential unit types
residential_units = client.property_unit_types.get_residential_unit_types()

for unit in residential_units.get('value', []):
    print(f"Residential Unit: {unit['UnitType']}")
```

---

### get_unit_types_with_properties()

Get unit types with property information expanded.

```python
get_unit_types_with_properties(**kwargs: Any) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get unit types with property information
units_with_props = client.property_unit_types.get_unit_types_with_properties(
    top=10
)

# Access property info for first unit type
first_unit = units_with_props['value'][0]
if 'Properties' in first_unit:
    properties = first_unit['Properties']
    print(f"Unit type {first_unit['UnitType']} has {len(properties)} properties")
```

---

## Data Synchronization

### get_modified_unit_types()

Get unit types modified since a specific date/time for incremental synchronization.

```python
get_modified_unit_types(
    since: Union[str, date, datetime], 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **since** | str \| date \| datetime | Yes | Cutoff time for modifications |
| **kwargs** | Any | No | Additional OData parameters |

#### Examples

=== "Recent Updates"

    ```python
    from datetime import datetime, timedelta, timezone

    # Get unit types modified in last week
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=7)
    updates = client.property_unit_types.get_modified_unit_types(
        since=cutoff_time
    )
    ```

=== "Specific Date"

    ```python
    # Get unit types modified since a specific date
    updates = client.property_unit_types.get_modified_unit_types(
        since="2023-01-01T00:00:00Z",
        orderby="ModificationTimestamp desc"
    )
    ```

---

## Response Format

### Standard Response Structure

```python
{
    "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#PropertyUnitTypes",
    "value": [
        {
            "PropertyUnitTypeKey": "PUT123",
            "PropertyKey": "1611952",
            "UnitType": "Condo",
            "UnitNumber": "2A",
            "UnitFloor": 2,
            "UnitSquareFeet": 1200,
            "UnitBedrooms": 2,
            "UnitBathrooms": 2.0,
            "UnitRent": 2500.00,
            "ModificationTimestamp": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| **PropertyUnitTypeKey** | string | Unique unit type identifier |
| **PropertyKey** | string | Associated property key |
| **UnitType** | string | Type classification (Condo, Townhome, etc.) |
| **UnitNumber** | string | Unit number/identifier |
| **UnitFloor** | integer | Floor number |
| **UnitSquareFeet** | integer | Unit square footage |
| **UnitBedrooms** | integer | Number of bedrooms |
| **UnitBathrooms** | decimal | Number of bathrooms |
| **UnitRent** | decimal | Monthly rent amount |
| **ModificationTimestamp** | datetime | Last modification time |

---

## Common Usage Patterns

### Multi-Unit Property Analysis

```python
# Get all unit types for a multi-unit property
property_units = client.property_unit_types.get_unit_types_for_property(
    listing_key="1611952",
    orderby="UnitNumber"
)

total_units = len(property_units.get('value', []))
total_sqft = sum(unit.get('UnitSquareFeet', 0) for unit in property_units['value'])

print(f"Property has {total_units} units totaling {total_sqft:,} sq ft")
```

### Unit Type Market Analysis

```python
# Analyze condo market
condos = client.property_unit_types.get_unit_types_by_type(
    unit_type="Condo",
    select=["UnitSquareFeet", "UnitRent", "PropertyKey"]
)

condo_data = condos.get('value', [])
avg_rent = sum(unit.get('UnitRent', 0) for unit in condo_data) / len(condo_data)
avg_sqft = sum(unit.get('UnitSquareFeet', 0) for unit in condo_data) / len(condo_data)

print(f"Average condo rent: ${avg_rent:,.2f}")
print(f"Average condo size: {avg_sqft:,.0f} sq ft")
```

### Residential Portfolio Overview

```python
# Get comprehensive residential unit overview
residential = client.property_unit_types.get_residential_unit_types(
    select=["UnitType", "UnitSquareFeet", "UnitRent"],
    orderby="UnitType"
)

# Group by unit type
from collections import defaultdict
by_type = defaultdict(list)

for unit in residential.get('value', []):
    unit_type = unit.get('UnitType', 'Unknown')
    by_type[unit_type].append(unit)

# Print summary
for unit_type, units in by_type.items():
    count = len(units)
    avg_rent = sum(u.get('UnitRent', 0) for u in units) / count
    print(f"{unit_type}: {count} units, avg rent ${avg_rent:,.2f}")
```

---

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    unit_type = client.property_unit_types.get_property_unit_type("INVALID")
except NotFoundError:
    print("Unit type not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

---

## Related Documentation

- **[Properties API](properties.md)** - Main property listings
- **[Client Setup](client.md)** - Authentication and initialization
- **[OData Queries](../guides/odata-queries.md)** - Advanced filtering
- **[Error Handling](../guides/error-handling.md)** - Exception management 