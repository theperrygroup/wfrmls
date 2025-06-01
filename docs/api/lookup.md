# Lookup API

The Lookup API provides access to reference data and code tables within the WFRMLS system. This includes standardized values for property types, statuses, and other enumerated fields used throughout the MLS.

## Overview

The `LookupClient` class handles all lookup-related operations, providing methods to retrieve reference data, code tables, and standardized values.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
property_types = client.lookup.get_property_types()
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_property_types()` | Get all property type codes | `List[Dict[str, Any]]` |
| `get_property_statuses()` | Get all property status codes | `List[Dict[str, Any]]` |
| `get_cities()` | Get all city names | `List[Dict[str, Any]]` |
| `get_counties()` | Get all county names | `List[Dict[str, Any]]` |
| `get_subdivisions()` | Get all subdivision names | `List[Dict[str, Any]]` |
| `get_schools()` | Get all school information | `List[Dict[str, Any]]` |
| `get_lookup_values()` | Get values for any lookup field | `List[Dict[str, Any]]` |

## Methods

### get_property_types()

Retrieve all available property type codes and descriptions.

```python
def get_property_types(
    self,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Example

```python
# Get all property types
property_types = client.lookup.get_property_types()

for prop_type in property_types:
    print(f"{prop_type['LookupKey']}: {prop_type['LookupValue']}")

# Example output:
# RES: Residential
# COM: Commercial
# LND: Land
# RNT: Rental
```

### get_property_statuses()

Retrieve all available property status codes and descriptions.

```python
def get_property_statuses(
    self,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Example

```python
# Get all property statuses
statuses = client.lookup.get_property_statuses()

for status in statuses:
    print(f"{status['LookupKey']}: {status['LookupValue']}")

# Example output:
# Active: Active
# Pending: Pending
# Sold: Sold
# Expired: Expired
```

### get_cities()

Retrieve all city names available in the MLS system.

```python
def get_cities(
    self,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Example

```python
# Get all cities
cities = client.lookup.get_cities()

for city in cities:
    print(f"{city['LookupValue']}")

# Example output:
# Salt Lake City
# Provo
# Ogden
# Park City
```

### get_counties()

Retrieve all county names available in the MLS system.

```python
def get_counties(
    self,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Example

```python
# Get all counties
counties = client.lookup.get_counties()

for county in counties:
    print(f"{county['LookupValue']}")

# Example output:
# Salt Lake County
# Utah County
# Davis County
# Weber County
```

### get_subdivisions()

Retrieve all subdivision names available in the MLS system.

```python
def get_subdivisions(
    self,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Example

```python
# Get all subdivisions
subdivisions = client.lookup.get_subdivisions()

for subdivision in subdivisions:
    print(f"{subdivision['LookupValue']}")

# Example output:
# The Avenues
# Sugar House
# Cottonwood Heights
# Park Meadows
```

### get_schools()

Retrieve all school information including districts and individual schools.

```python
def get_schools(
    self,
    school_type: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `school_type` | `str` | No | Filter by school type (Elementary, Middle, High) |

#### Example

```python
# Get all schools
schools = client.lookup.get_schools()

for school in schools:
    print(f"{school['LookupValue']} ({school.get('SchoolType', 'Unknown')})")

# Get only high schools
high_schools = client.lookup.get_schools(school_type="High")
```

### get_lookup_values()

Retrieve values for any lookup field in the system.

```python
def get_lookup_values(
    self,
    lookup_name: str,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lookup_name` | `str` | Yes | Name of the lookup field |

#### Example

```python
# Get values for a specific lookup field
heating_types = client.lookup.get_lookup_values("HeatingYN")
cooling_types = client.lookup.get_lookup_values("CoolingYN")
architectural_styles = client.lookup.get_lookup_values("ArchitecturalStyle")

for style in architectural_styles:
    print(f"{style['LookupKey']}: {style['LookupValue']}")
```

## Common Use Cases

### Building Form Dropdowns

```python
# Create dropdown options for property search forms
def build_search_form_options():
    options = {
        'property_types': client.lookup.get_property_types(),
        'cities': client.lookup.get_cities(),
        'counties': client.lookup.get_counties(),
        'subdivisions': client.lookup.get_subdivisions()
    }
    
    # Format for web forms
    formatted_options = {}
    for category, values in options.items():
        formatted_options[category] = [
            {'value': item['LookupKey'], 'label': item['LookupValue']}
            for item in values
        ]
    
    return formatted_options

form_options = build_search_form_options()
```

### Data Validation

```python
# Validate property data against lookup values
def validate_property_data(property_data):
    # Get valid values
    valid_types = {pt['LookupKey'] for pt in client.lookup.get_property_types()}
    valid_statuses = {ps['LookupKey'] for ps in client.lookup.get_property_statuses()}
    valid_cities = {c['LookupValue'] for c in client.lookup.get_cities()}
    
    errors = []
    
    # Validate property type
    if property_data.get('PropertyType') not in valid_types:
        errors.append(f"Invalid property type: {property_data.get('PropertyType')}")
    
    # Validate status
    if property_data.get('StandardStatus') not in valid_statuses:
        errors.append(f"Invalid status: {property_data.get('StandardStatus')}")
    
    # Validate city
    if property_data.get('City') not in valid_cities:
        errors.append(f"Invalid city: {property_data.get('City')}")
    
    return errors

# Example usage
property_data = {
    'PropertyType': 'RES',
    'StandardStatus': 'Active',
    'City': 'Salt Lake City'
}

validation_errors = validate_property_data(property_data)
if validation_errors:
    print("Validation errors:", validation_errors)
```

### Reference Data Caching

```python
# Cache lookup data for performance
import time
from typing import Dict, Any

class LookupCache:
    def __init__(self, client, cache_duration=3600):  # 1 hour cache
        self.client = client
        self.cache_duration = cache_duration
        self._cache = {}
        self._cache_timestamps = {}
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[key] < self.cache_duration
    
    def get_property_types(self) -> List[Dict[str, Any]]:
        key = 'property_types'
        if not self._is_cache_valid(key):
            self._cache[key] = self.client.lookup.get_property_types()
            self._cache_timestamps[key] = time.time()
        return self._cache[key]
    
    def get_cities(self) -> List[Dict[str, Any]]:
        key = 'cities'
        if not self._is_cache_valid(key):
            self._cache[key] = self.client.lookup.get_cities()
            self._cache_timestamps[key] = time.time()
        return self._cache[key]
    
    def clear_cache(self):
        self._cache.clear()
        self._cache_timestamps.clear()

# Usage
lookup_cache = LookupCache(client)
property_types = lookup_cache.get_property_types()  # Fetches from API
property_types = lookup_cache.get_property_types()  # Returns from cache
```

## Field Reference

### Standard Lookup Fields

| Field | Type | Description |
|-------|------|-------------|
| `LookupKey` | `str` | Unique identifier/code |
| `LookupValue` | `str` | Human-readable description |
| `LookupName` | `str` | Field name this lookup applies to |
| `StandardLookupValue` | `str` | RESO standard value |

### Extended Fields

| Field | Type | Description |
|-------|------|-------------|
| `LookupDisplayOrder` | `int` | Display order for UI |
| `LookupIsActive` | `bool` | Whether value is currently active |
| `LookupDescription` | `str` | Extended description |

## Common Lookup Fields

### Property Related

- **PropertyType**: Residential, Commercial, Land, Rental
- **PropertySubType**: Single Family, Condo, Townhouse, etc.
- **StandardStatus**: Active, Pending, Sold, Expired, etc.
- **ArchitecturalStyle**: Colonial, Contemporary, Ranch, etc.

### Location Related

- **City**: All cities in the MLS coverage area
- **County**: All counties in the coverage area
- **Subdivision**: All subdivision names
- **PostalCode**: All ZIP codes

### Property Features

- **HeatingYN**: Heating system types
- **CoolingYN**: Cooling system types
- **FireplaceYN**: Fireplace types
- **GarageYN**: Garage types
- **PoolYN**: Pool types

### Schools

- **ElementarySchool**: Elementary school names
- **MiddleSchool**: Middle school names
- **HighSchool**: High school names
- **SchoolDistrict**: School district names

## Advanced Usage

### Dynamic Lookup Retrieval

```python
# Get all available lookup fields
def get_all_lookup_fields():
    # This would require introspection of the API metadata
    # Common lookup fields in RESO systems
    lookup_fields = [
        'PropertyType', 'PropertySubType', 'StandardStatus',
        'ArchitecturalStyle', 'HeatingYN', 'CoolingYN',
        'FireplaceYN', 'GarageYN', 'PoolYN'
    ]
    
    all_lookups = {}
    for field in lookup_fields:
        try:
            all_lookups[field] = client.lookup.get_lookup_values(field)
        except Exception as e:
            print(f"Could not retrieve lookup for {field}: {e}")
    
    return all_lookups

all_lookup_data = get_all_lookup_fields()
```

### Lookup Value Mapping

```python
# Create mapping dictionaries for easy lookups
def create_lookup_mappings():
    mappings = {}
    
    # Property types
    property_types = client.lookup.get_property_types()
    mappings['property_type_to_name'] = {
        pt['LookupKey']: pt['LookupValue'] for pt in property_types
    }
    mappings['property_name_to_type'] = {
        pt['LookupValue']: pt['LookupKey'] for pt in property_types
    }
    
    # Cities
    cities = client.lookup.get_cities()
    mappings['cities'] = {city['LookupValue'] for city in cities}
    
    return mappings

lookup_mappings = create_lookup_mappings()

# Usage
property_type_code = "RES"
property_type_name = lookup_mappings['property_type_to_name'].get(property_type_code)
print(f"Property type {property_type_code} is: {property_type_name}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    lookup_values = client.lookup.get_lookup_values("InvalidField")
except NotFoundError:
    print("Lookup field not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Cache lookup data** as it changes infrequently
2. **Batch lookup requests** when possible
3. **Use specific methods** instead of generic get_lookup_values when available
4. **Implement cache invalidation** for data freshness

### Data Management

1. **Validate against current values** before using cached data
2. **Handle inactive lookup values** appropriately
3. **Use standard RESO values** when available
4. **Document custom lookup fields** for maintenance

### User Experience

1. **Sort lookup values** alphabetically for dropdowns
2. **Provide search/filter** for long lists
3. **Use descriptive labels** instead of codes
4. **Handle missing/unknown values** gracefully

## Integration Examples

### Web Form Generation

```python
# Generate HTML select options
def generate_select_options(lookup_data, selected_value=None):
    options = ['<option value="">Select...</option>']
    
    for item in sorted(lookup_data, key=lambda x: x['LookupValue']):
        selected = 'selected' if item['LookupKey'] == selected_value else ''
        options.append(
            f'<option value="{item["LookupKey"]}" {selected}>'
            f'{item["LookupValue"]}</option>'
        )
    
    return '\n'.join(options)

# Usage
property_types = client.lookup.get_property_types()
select_html = generate_select_options(property_types, selected_value="RES")
```

### API Response Enhancement

```python
# Enhance property data with lookup descriptions
def enhance_property_with_lookups(property_data):
    # Get lookup mappings
    property_types = {pt['LookupKey']: pt['LookupValue'] 
                     for pt in client.lookup.get_property_types()}
    
    # Enhance property data
    enhanced = property_data.copy()
    
    if 'PropertyType' in enhanced:
        enhanced['PropertyTypeName'] = property_types.get(
            enhanced['PropertyType'], 
            enhanced['PropertyType']
        )
    
    return enhanced

# Usage
properties = client.property.get_properties(top=10)
enhanced_properties = [enhance_property_with_lookups(prop) for prop in properties]
```

## Related Resources

- [Properties API](properties.md) - For property data validation
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management
- [RESO Standards](../reference/reso-standards.md) - Industry standards