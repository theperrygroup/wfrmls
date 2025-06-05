# ADU (Accessory Dwelling Units) API

Complete reference for the ADU endpoint of the WFRMLS Python client.

---

## 🏘️ Overview

The ADU API provides access to Accessory Dwelling Unit information associated with properties. ADUs include secondary housing units like basement apartments, mother-in-law suites, garage apartments, and other additional dwelling spaces.

### Key Features

- **ADU details** - Access information about additional dwelling units
- **Unit specifications** - Get bedroom/bathroom counts and square footage
- **Rental information** - View rental status and rates
- **Property associations** - Link ADUs to primary properties
- **Utility separation** - Check for separate meters

---

## 📚 Methods

### `get_adus()`

Retrieve multiple ADU records with optional filtering and pagination.

```python
def get_adus(
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
  - `value`: List of ADU dictionaries
  - `@odata.count`: Total count (if requested)
  - `@odata.nextLink`: URL for next page of results

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get first 10 ADUs
response = client.adu.get_adus(top=10)
adus = response["value"]

# Get ADUs with specific features
attached_adus = client.adu.get_adus(
    filter_query="AttachedYN eq true and KitchenYN eq true",
    select=["AduKeyNumeric", "BedroomsTotal", "SquareFeet", "Rent"]
)

# Get currently rented ADUs
rented_adus = client.adu.get_adus(
    filter_query="CurrentlyRentedYN eq true",
    select=["AduKeyNumeric", "Rent", "BedroomsTotal", "BathroomsTotal"]
)
```

### `get_existing_adus()`

Retrieve ADUs that are marked as existing (helper method).

```python
def get_existing_adus(
    top: Optional[int] = None,
    select: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Examples:**

```python
# Get existing ADUs
existing = client.adu.get_existing_adus(top=20)

# Get existing ADUs with selected fields
existing_minimal = client.adu.get_existing_adus(
    select=["AduKeyNumeric", "BedroomsTotal", "AttachedYN"]
)
```

### `get_adus_for_property()`

Retrieve ADUs associated with a specific property.

```python
def get_adus_for_property(listing_id: str) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `listing_id` | `str` | Property listing ID |

**Returns:**
- `Dict[str, Any]` - Response with ADUs for the property

**Examples:**

```python
# Get ADUs for a specific property
property_adus = client.adu.get_adus_for_property("1611952")

if property_adus["value"]:
    for adu in property_adus["value"]:
        print(f"ADU: {adu['BedroomsTotal']} bed, {adu['BathroomsTotal']} bath")
        print(f"Size: {adu['SquareFeet']} sq ft")
```

---

## 🏷️ Field Reference

### Core Identification

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **AduKeyNumeric** | `integer` | Unique ADU identifier | `1777403` |
| **OriginatingSystemName** | `string` | Source system | `"UtahRealEstate.com"` |

### Unit Details

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **BedroomsTotal** | `integer` | Number of bedrooms | `3` |
| **BathroomsTotal** | `integer` | Number of bathrooms | `2` |
| **SquareFeet** | `decimal` | Unit square footage | `1491.0` |

### Rental Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **Rent** | `decimal` | Monthly rent amount | `null` |
| **CurrentlyRentedYN** | `boolean` | Is currently rented | `false` |
| **Remarks** | `string` | Additional notes | `"This attached casita has..."` |

### Physical Characteristics

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **AttachedYN** | `boolean` | Is attached to main house | `true` |
| **SeparateEntranceYN** | `boolean` | Has separate entrance | `true` |
| **KitchenYN** | `boolean` | Has kitchen | `true` |

### Utilities

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **SeparateGasMeterYN** | `boolean` | Has separate gas meter | `false` |
| **SeparateElectricMeterYN** | `boolean` | Has separate electric meter | `false` |
| **WaterYN** | `boolean` | Has water access | `false` |

### System Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ModificationTimestamp** | `datetime` | Last modified | `"2023-04-20T17:19:45Z"` |

---

## 🔍 Common Query Patterns

### ADU Types

```python
# Attached ADUs only
attached = client.adu.get_adus(
    filter_query="AttachedYN eq true"
)

# Detached ADUs with separate entrance
detached_separate = client.adu.get_adus(
    filter_query="AttachedYN eq false and SeparateEntranceYN eq true"
)
```

### Size and Features

```python
# ADUs by size
large_adus = client.adu.get_adus(
    filter_query="SquareFeet ge 800",
    orderby="SquareFeet desc"
)

# ADUs with specific bedroom count
two_bedroom_adus = client.adu.get_adus(
    filter_query="BedroomsTotal eq 2"
)

# Full apartments (kitchen + separate entrance)
full_apartments = client.adu.get_adus(
    filter_query="KitchenYN eq true and SeparateEntranceYN eq true"
)
```

### Rental Searches

```python
# Currently rented ADUs
rented = client.adu.get_adus(
    filter_query="CurrentlyRentedYN eq true",
    select=["AduKeyNumeric", "Rent", "BedroomsTotal", "SquareFeet"]
)

# ADUs with rent information
with_rent = client.adu.get_adus(
    filter_query="Rent ne null",
    orderby="Rent asc"
)
```

### Utility Independence

```python
# ADUs with separate utilities
independent_adus = client.adu.get_adus(
    filter_query=(
        "SeparateElectricMeterYN eq true or "
        "SeparateGasMeterYN eq true"
    )
)

# Fully independent units
fully_independent = client.adu.get_adus(
    filter_query=(
        "SeparateEntranceYN eq true and "
        "KitchenYN eq true and "
        "(SeparateElectricMeterYN eq true or SeparateGasMeterYN eq true)"
    )
)
```

---

## 📊 Analysis Examples

### ADU Inventory Summary

```python
def analyze_adu_inventory():
    """Analyze ADU inventory by type and features."""
    
    # Get all ADUs with key fields
    response = client.adu.get_adus(
        select=[
            "AduKeyNumeric", "AttachedYN", "BedroomsTotal", 
            "SquareFeet", "KitchenYN", "CurrentlyRentedYN"
        ]
    )
    
    adus = response["value"]
    
    # Calculate statistics
    total_adus = len(adus)
    attached = sum(1 for a in adus if a.get("AttachedYN"))
    with_kitchen = sum(1 for a in adus if a.get("KitchenYN"))
    rented = sum(1 for a in adus if a.get("CurrentlyRentedYN"))
    
    avg_size = sum(a.get("SquareFeet", 0) for a in adus) / total_adus if total_adus > 0 else 0
    
    return {
        "total_adus": total_adus,
        "attached_percentage": (attached / total_adus * 100) if total_adus > 0 else 0,
        "with_kitchen_percentage": (with_kitchen / total_adus * 100) if total_adus > 0 else 0,
        "rented_percentage": (rented / total_adus * 100) if total_adus > 0 else 0,
        "average_size": avg_size
    }
```

### Rental Market Analysis

```python
def analyze_adu_rentals():
    """Analyze ADU rental market."""
    
    # Get rented ADUs with rent amounts
    rented = client.adu.get_adus(
        filter_query="CurrentlyRentedYN eq true and Rent ne null",
        select=["Rent", "BedroomsTotal", "BathroomsTotal", "SquareFeet"]
    )
    
    rentals = rented["value"]
    
    if rentals:
        # Group by bedroom count
        by_bedrooms = {}
        for rental in rentals:
            beds = rental.get("BedroomsTotal", 0)
            if beds not in by_bedrooms:
                by_bedrooms[beds] = []
            by_bedrooms[beds].append(rental.get("Rent", 0))
        
        # Calculate average rent by bedroom count
        avg_rents = {}
        for beds, rents in by_bedrooms.items():
            avg_rents[f"{beds}_bedroom"] = sum(rents) / len(rents)
        
        return avg_rents
    
    return {}
```

---

## ⚡ Performance Tips

### Efficient ADU Queries

```python
# ❌ Inefficient - gets all fields for counting
count_query = client.adu.get_adus()
total = len(count_query["value"])

# ✅ Efficient - use count parameter
count_response = client.adu.get_adus(top=0, count=True)
total = count_response["@odata.count"]
```

### Selective Field Loading

```python
# For listing displays
list_fields = client.adu.get_adus(
    select=["AduKeyNumeric", "BedroomsTotal", "BathroomsTotal", "Rent"],
    top=50
)

# For detailed views
detail_fields = client.adu.get_adus(
    filter_query=f"AduKeyNumeric eq {adu_id}",
    select=["AduKeyNumeric", "BedroomsTotal", "BathroomsTotal", 
            "SquareFeet", "Rent", "Remarks", "AttachedYN", 
            "SeparateEntranceYN", "KitchenYN"]
)