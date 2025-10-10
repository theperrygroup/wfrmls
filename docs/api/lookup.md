# Lookup API

Complete reference for the Lookup endpoint of the WFRMLS Python client.

---

## 📚 Overview

The Lookup API provides access to enumeration values and reference data used throughout the MLS system. This includes standardized values for property types, statuses, architectural styles, appliances, and dozens of other fields.

### Key Features

- **Enumeration values** - Get valid values for dropdown fields
- **Standardized codes** - Access RESO standard values
- **Legacy mappings** - See OData legacy values for compatibility
- **Category browsing** - Explore all available lookup categories
- **Value descriptions** - Get human-readable labels for codes

---

## 📚 Methods

### `get_lookups()`

Retrieve lookup values with optional filtering.

```python
def get_lookups(
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
- `Dict[str, Any]` - Response dictionary containing lookup values

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get all standard status values
status_lookups = client.lookup.get_lookups(
    filter_query="LookupName eq 'StandardStatus'"
)

# Get property types
property_types = client.lookup.get_lookups(
    filter_query="LookupName eq 'PropertyType'"
)

# Get lookups with full details
detailed_lookups = client.lookup.get_lookups(
    filter_query="LookupName eq 'PropertySubType'",
    top=20
)
```

### `get_lookup_names()`

Get all available lookup categories/names.

```python
def get_lookup_names() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - Response with unique lookup names

**Examples:**

```python
# Get all lookup categories
names_response = client.lookup.get_lookup_names()

# Extract unique categories
lookup_names = set()
for item in names_response["value"]:
    lookup_names.add(item.get("LookupName"))

print("Available lookup categories:")
for name in sorted(lookup_names):
    print(f"  - {name}")
```

### `get_property_type_lookups()`

Helper method to get property type enumeration values.

```python
def get_property_type_lookups() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - Property type lookup values

---

## 🏷️ Field Reference

Each lookup record contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **LookupKey** | `string` | Unique identifier | `"42471"` |
| **LookupName** | `string` | Category/field name | `"StandardStatus"` |
| **LookupValue** | `string` | Display value | `"Active"` |
| **StandardLookupValue** | `string` | RESO standard value | `null` |
| **LegacyODataValue** | `string` | Legacy API value | `"Active"` |
| **ModificationTimestamp** | `datetime` | Last modified | `"2024-01-25T11:35:01Z"` |

---

## 📋 Available Lookup Categories

Based on the API, the following lookup categories are available:

### Property Related
- `PropertyType` - Main property types (Residential, Commercial, Land, etc.)
- `PropertySubType` - Detailed property subtypes  
- `PropertyCondition` - Property condition values
- `CurrentUse` - Current property use
- `PossibleUse` - Possible use options

### Status & Listing
- `StandardStatus` - RESO standard status values
- `MlsStatus` - MLS-specific status
- `ShowingContactType` - Showing contact types
- `SpecialListingConditions` - Special conditions

### Architecture & Features
- `ArchitecturalStyle` - Architectural styles
- `ConstructionMaterials` - Construction materials
- `Roof` - Roof types
- `Flooring` - Flooring materials
- `Basement` - Basement types
- `Levels` - Level descriptions

### Amenities & Equipment
- `Appliances` - Included appliances
- `Cooling` - Cooling systems
- `Heating` - Heating systems
- `FireplaceFeatures` - Fireplace types
- `InteriorFeatures` - Interior features
- `ExteriorFeatures` - Exterior features

### Lot & Location
- `LotFeatures` - Lot characteristics
- `View` - View types
- `WaterSource` - Water sources
- `Sewer` - Sewer types
- `Utilities` - Utility options

### Association & Community
- `AssociationAmenities` - HOA amenities
- `AssociationFeeIncludes` - What HOA fees cover
- `CommunityFeatures` - Community amenities

### Access & Parking
- `AccessibilityFeatures` - Accessibility options
- `ParkingFeatures` - Parking features
- `RoadFrontageType` - Road frontage
- `RoadSurfaceType` - Road surfaces

### Business (Commercial)
- `BusinessType` - Business categories
- `BuildingFeatures` - Building features
- `CurrentUse` - Current use

### Other Categories
- `AOR` - Association of Realtors
- `AreaSource` - Area measurement source
- `AreaUnits` - Area units (sqft, acres)
- `Attended` - Attendance types
- `BodyType` - Structure body types

---

## 🔍 Common Usage Patterns

### Building Dynamic Forms

```python
def get_form_options(field_name: str):
    """Get valid options for a form field."""
    
    response = client.lookup.get_lookups(
        filter_query=f"LookupName eq '{field_name}'",
        orderby="LookupValue asc"
    )
    
    options = []
    for lookup in response["value"]:
        options.append({
            "value": lookup["LegacyODataValue"],
            "label": lookup["LookupValue"],
            "key": lookup["LookupKey"]
        })
    
    return options

# Get options for property type dropdown
property_type_options = get_form_options("PropertyType")
```

### Status Value Mapping

```python
def get_status_mappings():
    """Create mapping between display and API values."""
    
    response = client.lookup.get_lookups(
        filter_query="LookupName eq 'StandardStatus'"
    )
    
    # Create bidirectional mappings
    display_to_api = {}
    api_to_display = {}
    
    for lookup in response["value"]:
        display_value = lookup["LookupValue"]
        api_value = lookup["LegacyODataValue"]
        
        display_to_api[display_value] = api_value
        api_to_display[api_value] = display_value
    
    return display_to_api, api_to_display

# Usage
display_to_api, api_to_display = get_status_mappings()

# Convert user selection to API value
user_selected = "Active Under Contract"
api_filter_value = display_to_api[user_selected]  # "ActiveUnderContract"
```

### Lookup Caching

```python
class LookupCache:
    """Cache lookup values to reduce API calls."""
    
    def __init__(self, client):
        self.client = client
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = 3600  # 1 hour
    
    def get_lookups(self, lookup_name: str):
        """Get lookups with caching."""
        
        # Check cache
        if lookup_name in self.cache:
            if time.time() - self.cache_time[lookup_name] < self.cache_duration:
                return self.cache[lookup_name]
        
        # Fetch from API
        response = self.client.lookup.get_lookups(
            filter_query=f"LookupName eq '{lookup_name}'"
        )
        
        # Cache results
        self.cache[lookup_name] = response["value"]
        self.cache_time[lookup_name] = time.time()
        
        return response["value"]

# Initialize cache
lookup_cache = LookupCache(client)

# Use cached lookups
property_types = lookup_cache.get_lookups("PropertyType")
```

### Validation Helper

```python
def validate_field_value(field_name: str, value: str) -> bool:
    """Validate if a value is valid for a field."""
    
    response = client.lookup.get_lookups(
        filter_query=f"LookupName eq '{field_name}'"
    )
    
    valid_values = set()
    for lookup in response["value"]:
        valid_values.add(lookup["LegacyODataValue"])
        valid_values.add(lookup["LookupValue"])
    
    return value in valid_values

# Validate user input
is_valid = validate_field_value("StandardStatus", "Active")  # True
is_valid = validate_field_value("StandardStatus", "Invalid")  # False
```

---

## 📊 Standard Status Values

The most commonly used lookup values:

| Display Value | API Value | Description |
|---------------|-----------|-------------|
| Active | Active | Property is actively listed |
| Active Under Contract | ActiveUnderContract | Accepted offer, still showing |
| Pending | Pending | Under contract |
| Withdrawn | Withdrawn | Temporarily off market |
| Expired | Expired | Listing period ended |
| Closed | Closed | Sale completed |
| Canceled | Canceled | Listing canceled |
| Hold | Hold | On hold status |

---

## ⚡ Performance Tips

### Batch Loading

```python
def load_all_lookups_for_form(lookup_names: List[str]):
    """Load multiple lookup categories efficiently."""
    
    # Build filter for multiple categories
    filters = [f"LookupName eq '{name}'" for name in lookup_names]
    filter_query = " or ".join(filters)
    
    response = client.lookup.get_lookups(
        filter_query=f"({filter_query})",
        top=1000  # Get many at once
    )
    
    # Group by LookupName
    grouped = {}
    for lookup in response["value"]:
        name = lookup["LookupName"]
        if name not in grouped:
            grouped[name] = []
        grouped[name].append(lookup)
    
    return grouped

# Load all form lookups at once
form_lookups = load_all_lookups_for_form([
    "PropertyType", "StandardStatus", "PropertySubType"
])