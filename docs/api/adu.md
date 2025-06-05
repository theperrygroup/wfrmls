# ADU (Accessory Dwelling Units) API

Complete reference for Accessory Dwelling Unit endpoints in the WFRMLS Python client.

---

## Overview

The **ADU (Accessory Dwelling Units)** module provides access to accessory dwelling unit information, including types, statuses, and property relationships for secondary housing units. ADUs are increasingly important in real estate markets as they provide additional housing options and rental income opportunities.

### Key Features

- **ADU Classification** - Different types of accessory dwelling units
- **Property Relationships** - Link ADUs to primary properties
- **Status Tracking** - Current status and availability of ADUs
- **Modification Tracking** - Incremental sync capabilities

---

## Class Reference

### AduClient

```python
from wfrmls.adu import AduClient

client = AduClient(bearer_token="your_token")
```

---

## Core Methods

### get_adus()

Get ADU records with optional OData filtering.

```python
get_adus(
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
    # Get all ADUs
    adus = client.adu.get_adus()
    
    for adu in adus.get('value', []):
        print(f"ADU: {adu['AduType']} - Status: {adu['AduStatus']}")
    ```

=== "Filtered Results"

    ```python
    # Get existing/active ADUs
    existing_adus = client.adu.get_adus(
        filter_query="AduStatus eq 'Existing'",
        select=["AduKey", "AduType", "AduStatus", "PropertyKey"]
    )
    ```

=== "With Relationships"

    ```python
    # Get ADUs with property information
    adus_with_props = client.adu.get_adus(
        expand="Property",
        top=20
    )
    ```

---

### get_adu()

Get a specific ADU by its unique key.

```python
get_adu(adu_key: str) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **adu_key** | str | Yes | Unique ADU identifier |

#### Example

```python
# Get specific ADU
adu = client.adu.get_adu("ADU123")

print(f"ADU Type: {adu['AduType']}")
print(f"Status: {adu['AduStatus']}")
print(f"Square Feet: {adu.get('AduSquareFeet', 'Not specified')}")
```

---

## Convenience Methods

### get_adus_for_property()

Get ADUs associated with a specific property.

```python
get_adus_for_property(
    property_key: str, 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **property_key** | str | Yes | Property key to filter by |
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get ADUs for a property
property_adus = client.adu.get_adus_for_property(
    property_key="1611952"
)

adu_count = len(property_adus.get('value', []))
print(f"Property has {adu_count} ADUs")
```

---

### get_existing_adus()

Get ADUs with "Existing" status.

```python
get_existing_adus(**kwargs: Any) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get all existing ADUs
existing_adus = client.adu.get_existing_adus(
    orderby="ModificationTimestamp desc"
)

for adu in existing_adus.get('value', []):
    print(f"Existing ADU: {adu['AduType']} - {adu.get('AduSquareFeet', 'N/A')} sq ft")
```

---

### get_adus_by_type()

Get ADUs filtered by type.

```python
get_adus_by_type(
    adu_type: str, 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **adu_type** | str | Yes | ADU type to filter by |
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get all detached ADUs
detached_adus = client.adu.get_adus_by_type(
    adu_type="Detached",
    select=["AduKey", "AduSquareFeet", "PropertyKey"]
)
```

---

### get_adus_with_properties()

Get ADUs with property information expanded.

```python
get_adus_with_properties(**kwargs: Any) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **kwargs** | Any | No | Additional OData parameters |

#### Example

```python
# Get ADUs with property details
adus_with_props = client.adu.get_adus_with_properties(top=25)

for adu in adus_with_props.get('value', []):
    property_info = adu.get('Property', {})
    property_city = property_info.get('City', 'Unknown')
    print(f"ADU in {property_city}: {adu['AduType']}")
```

---

## Data Synchronization

### get_modified_adus()

Get ADUs modified since a specific date/time for incremental synchronization.

```python
get_modified_adus(
    since: Union[str, date], 
    **kwargs: Any
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **since** | str \| date | Yes | Cutoff time for modifications |
| **kwargs** | Any | No | Additional OData parameters |

#### Examples

=== "Recent Updates"

    ```python
    from datetime import datetime, timedelta, timezone

    # Get ADUs modified in last week
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=7)
    updates = client.adu.get_modified_adus(
        since=cutoff_time.isoformat() + "Z"
    )
    ```

=== "Specific Date"

    ```python
    from datetime import date

    # Get ADUs modified since specific date
    since_date = date(2024, 1, 1)
    updates = client.adu.get_modified_adus(
        since=since_date,
        orderby="ModificationTimestamp desc"
    )
    ```

---

## Response Format

### Standard Response Structure

```python
{
    "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#Adu",
    "value": [
        {
            "AduKey": "ADU123",
            "PropertyKey": "1611952",
            "AduType": "Detached",
            "AduStatus": "Existing",
            "AduSquareFeet": 800,
            "AduBedrooms": 1,
            "AduBathrooms": 1.0,
            "AduKitchen": "Full",
            "AduRent": 1800.00,
            "AduDescription": "Modern detached ADU with full kitchen",
            "ModificationTimestamp": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| **AduKey** | string | Unique ADU identifier |
| **PropertyKey** | string | Associated property key |
| **AduType** | string | Type of ADU (Detached, Attached, Internal, etc.) |
| **AduStatus** | string | Current status (Existing, Planned, Under Construction) |
| **AduSquareFeet** | integer | ADU square footage |
| **AduBedrooms** | integer | Number of bedrooms |
| **AduBathrooms** | decimal | Number of bathrooms |
| **AduKitchen** | string | Kitchen type (Full, Kitchenette, None) |
| **AduRent** | decimal | Monthly rent amount |
| **AduDescription** | string | Detailed description |
| **ModificationTimestamp** | datetime | Last modification time |

---

## Common Usage Patterns

### ADU Market Analysis

```python
# Analyze ADU market by type
adu_types = ["Detached", "Attached", "Internal", "Garage Conversion"]
analysis = {}

for adu_type in adu_types:
    adus = client.adu.get_adus_by_type(
        adu_type=adu_type,
        filter_query="AduStatus eq 'Existing'",
        select=["AduSquareFeet", "AduRent", "AduBedrooms"]
    )
    
    adu_data = adus.get('value', [])
    if adu_data:
        avg_size = sum(a.get('AduSquareFeet', 0) for a in adu_data) / len(adu_data)
        avg_rent = sum(a.get('AduRent', 0) for a in adu_data) / len(adu_data)
        
        analysis[adu_type] = {
            'count': len(adu_data),
            'avg_size': avg_size,
            'avg_rent': avg_rent,
            'rent_per_sqft': avg_rent / avg_size if avg_size > 0 else 0
        }

# Print analysis
for adu_type, stats in analysis.items():
    print(f"{adu_type} ADUs:")
    print(f"  Count: {stats['count']}")
    print(f"  Avg Size: {stats['avg_size']:.0f} sq ft")
    print(f"  Avg Rent: ${stats['avg_rent']:.2f}")
    print(f"  Rent/sq ft: ${stats['rent_per_sqft']:.2f}")
```

### Property ADU Portfolio

```python
# Get properties with multiple ADUs
properties_with_adus = {}

# Get all existing ADUs
all_adus = client.adu.get_existing_adus()

# Group by property
for adu in all_adus.get('value', []):
    prop_key = adu.get('PropertyKey')
    if prop_key:
        if prop_key not in properties_with_adus:
            properties_with_adus[prop_key] = []
        properties_with_adus[prop_key].append(adu)

# Find properties with multiple ADUs
multi_adu_properties = {
    k: v for k, v in properties_with_adus.items() 
    if len(v) > 1
}

print(f"Found {len(multi_adu_properties)} properties with multiple ADUs")
for prop_key, adus in multi_adu_properties.items():
    total_adu_sqft = sum(adu.get('AduSquareFeet', 0) for adu in adus)
    total_rent = sum(adu.get('AduRent', 0) for adu in adus)
    print(f"Property {prop_key}: {len(adus)} ADUs, {total_adu_sqft} sq ft, ${total_rent:.2f}/month")
```

### ADU Development Tracking

```python
# Track ADU development pipeline
pipeline_adus = client.adu.get_adus(
    filter_query="AduStatus ne 'Existing'",
    orderby="ModificationTimestamp desc"
)

status_counts = {}
for adu in pipeline_adus.get('value', []):
    status = adu.get('AduStatus', 'Unknown')
    status_counts[status] = status_counts.get(status, 0) + 1

print("ADU Development Pipeline:")
for status, count in status_counts.items():
    print(f"  {status}: {count} units")
```

---

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    adu = client.adu.get_adu("INVALID_ADU")
except NotFoundError:
    print("ADU not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

---

## Related Documentation

- **[Properties API](properties.md)** - Main property listings
- **[Property Unit Types API](property-unit-types.md)** - Unit classifications
- **[Client Setup](client.md)** - Authentication and initialization
- **[OData Queries](../guides/odata-queries.md)** - Advanced filtering
- **[Error Handling](../guides/error-handling.md)** - Exception management 