# Lookup API

The Lookup API provides access to enumeration values and reference data used throughout the MLS system, including property types, statuses, and other lookup values. This API is essential for understanding valid values for filtering and data validation.

!!! example "Quick Start"
    ```python
    # Get all lookup names
    lookup_names = client.lookup.get_lookup_names()
    
    # Get property type lookups
    property_types = client.lookup.get_property_type_lookups()
    
    # Get specific lookup values
    lookup_values = client.lookup.get_lookup("PropertyType")
    ```

## Lookup Client

::: wfrmls.lookup.LookupClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### Basic Lookup Retrieval

=== "Available Lookups"
    ```python
    # Get all available lookup names
    lookup_names = client.lookup.get_lookup_names()
    
    # Get lookups with specific ordering
    ordered_lookups = client.lookup.get_lookups(
        orderby="LookupName asc",
        top=50
    )
    
    # Get lookup metadata
    lookup_info = client.lookup.get_lookups(
        select="LookupName,LookupValue,StandardLookupValue,LookupDisplayOrder"
    )
    ```

=== "Property-Related Lookups"
    ```python
    # Get property type values
    property_types = client.lookup.get_property_type_lookups()
    
    # Get property subtypes
    property_subtypes = client.lookup.get_lookup("PropertySubType")
    
    # Get status values
    status_values = client.lookup.get_lookup("StandardStatus")
    
    # Get property features
    architectural_styles = client.lookup.get_lookup("ArchitecturalStyle")
    ```

=== "Specific Lookup Categories"
    ```python
    # Get all lookups for a specific category
    status_lookups = client.lookup.get_lookups(
        filter_query="LookupName eq 'StandardStatus'",
        orderby="LookupDisplayOrder asc"
    )
    
    # Get lookup values with descriptions
    city_lookups = client.lookup.get_lookups(
        filter_query="LookupName eq 'City'",
        select="LookupValue,StandardLookupValue,LookupDisplayOrder",
        orderby="LookupValue asc"
    )
    ```

### Advanced Filtering and Search

=== "Search Lookup Values"
    ```python
    # Search for specific lookup values
    salt_lake_lookups = client.lookup.get_lookups(
        filter_query="contains(tolower(LookupValue), 'salt lake')",
        orderby="LookupName asc, LookupValue asc"
    )
    
    # Find lookups with standard values
    standard_lookups = client.lookup.get_lookups(
        filter_query="StandardLookupValue ne null",
        select="LookupName,LookupValue,StandardLookupValue"
    )
    ```

=== "Lookup Validation"
    ```python
    # Get valid values for validation
    def get_valid_values(client, lookup_name):
        lookups = client.lookup.get_lookups(
            filter_query=f"LookupName eq '{lookup_name}'",
            select="LookupValue,StandardLookupValue",
            orderby="LookupDisplayOrder asc"
        )
        
        values = []
        for lookup in lookups.get('value', []):
            values.append(lookup.get('LookupValue'))
            if lookup.get('StandardLookupValue'):
                values.append(lookup.get('StandardLookupValue'))
        
        return sorted(list(set(values)))  # Remove duplicates and sort
    
    # Usage
    valid_property_types = get_valid_values(client, "PropertyType")
    valid_cities = get_valid_values(client, "City")
    ```

=== "Lookup Hierarchy"
    ```python
    # Get hierarchical lookup data
    def get_lookup_hierarchy(client):
        all_lookups = client.lookup.get_lookups(
            select="LookupName,LookupValue,StandardLookupValue,LookupDisplayOrder",
            orderby="LookupName asc, LookupDisplayOrder asc",
            top=2000
        )
        
        hierarchy = {}
        for lookup in all_lookups.get('value', []):
            lookup_name = lookup.get('LookupName', 'Unknown')
            if lookup_name not in hierarchy:
                hierarchy[lookup_name] = []
            
            hierarchy[lookup_name].append({
                'value': lookup.get('LookupValue'),
                'standard_value': lookup.get('StandardLookupValue'),
                'display_order': lookup.get('LookupDisplayOrder', 999)
            })
        
        return hierarchy
    
    # Usage
    lookup_hierarchy = get_lookup_hierarchy(client)
    ```

## Lookup Data Structure

Lookups in WFRMLS follow the RESO standard with comprehensive reference data:

??? info "Key Lookup Fields"
    **Lookup Identification**
    
    - `LookupKey` - Unique lookup identifier
    - `LookupName` - Category/field name this lookup applies to
    - `LookupValue` - The actual lookup value
    - `StandardLookupValue` - RESO standard equivalent value
    - `LegacyODataValue` - Legacy value for compatibility

    **Display and Ordering**
    
    - `LookupDisplayOrder` - Sort order for display
    - `LookupDisplayName` - Human-friendly display name
    - `LookupShortValue` - Abbreviated value
    - `LookupLongValue` - Extended description

    **Metadata**
    
    - `LookupActive` - Whether the lookup is active
    - `LookupDefault` - Whether this is a default value
    - `LookupDescription` - Detailed description of the lookup
    - `LookupGroup` - Grouping category

    **System Information**
    
    - `ModificationTimestamp` - Last update time
    - `OriginalEntryTimestamp` - Initial creation time

## Integration Examples

### Dynamic Form Generation

```python
def generate_property_search_form(client):
    """Generate dynamic search form options from lookup data."""
    
    form_fields = {}
    
    # Define the lookups we need for the form
    form_lookups = [
        'PropertyType',
        'PropertySubType', 
        'StandardStatus',
        'City',
        'StateOrProvince',
        'ArchitecturalStyle',
        'Heating',
        'Cooling'
    ]
    
    for lookup_name in form_lookups:
        try:
            lookups = client.lookup.get_lookups(
                filter_query=f"LookupName eq '{lookup_name}' and LookupActive eq true",
                select="LookupValue,StandardLookupValue,LookupDisplayOrder,LookupDisplayName",
                orderby="LookupDisplayOrder asc, LookupValue asc"
            )
            
            options = []
            for lookup in lookups.get('value', []):
                display_name = lookup.get('LookupDisplayName') or lookup.get('LookupValue', '')
                value = lookup.get('StandardLookupValue') or lookup.get('LookupValue', '')
                
                options.append({
                    'label': display_name,
                    'value': value,
                    'display_order': lookup.get('LookupDisplayOrder', 999)
                })
            
            form_fields[lookup_name] = sorted(options, key=lambda x: x['display_order'])
            
        except Exception as e:
            print(f"Warning: Could not load lookups for {lookup_name}: {e}")
            form_fields[lookup_name] = []
    
    return form_fields

# Usage
search_form = generate_property_search_form(client)

print("🔍 Property Search Form Options:")
for field_name, options in search_form.items():
    print(f"\n📋 {field_name} ({len(options)} options):")
    for option in options[:10]:  # Show first 10 options
        print(f"   • {option['label']} ({option['value']})")
    if len(options) > 10:
        print(f"   ... and {len(options) - 10} more options")
```

### Data Validation System

```python
def create_lookup_validator(client):
    """Create a data validation system using lookup values."""
    
    # Cache all lookup values for validation
    validation_cache = {}
    
    # Get all lookups
    all_lookups = client.lookup.get_lookups(
        select="LookupName,LookupValue,StandardLookupValue,LookupActive",
        top=5000
    )
    
    for lookup in all_lookups.get('value', []):
        lookup_name = lookup.get('LookupName')
        if not lookup_name:
            continue
            
        if lookup_name not in validation_cache:
            validation_cache[lookup_name] = set()
        
        # Add both regular and standard values
        if lookup.get('LookupValue'):
            validation_cache[lookup_name].add(lookup.get('LookupValue'))
        if lookup.get('StandardLookupValue'):
            validation_cache[lookup_name].add(lookup.get('StandardLookupValue'))
    
    def validate_value(field_name, value):
        """Validate a value against lookup data."""
        if field_name not in validation_cache:
            return {'valid': None, 'message': f'No validation data for field: {field_name}'}
        
        valid_values = validation_cache[field_name]
        is_valid = value in valid_values
        
        if is_valid:
            return {'valid': True, 'message': 'Valid value'}
        else:
            # Find close matches
            close_matches = [v for v in valid_values if value.lower() in v.lower() or v.lower() in value.lower()]
            
            return {
                'valid': False,
                'message': f'Invalid value: {value}',
                'suggestions': close_matches[:5]  # Top 5 suggestions
            }
    
    def get_valid_values(field_name):
        """Get all valid values for a field."""
        return sorted(list(validation_cache.get(field_name, [])))
    
    return {
        'validate': validate_value,
        'get_valid_values': get_valid_values,
        'cache': validation_cache
    }

# Usage
validator = create_lookup_validator(client)

# Test validation
test_values = [
    ('PropertyType', 'Residential'),
    ('PropertyType', 'Invalid Type'),
    ('City', 'Salt Lake City'),
    ('City', 'Fake City'),
    ('StandardStatus', 'Active')
]

print("🔍 Data Validation Results:")
for field, value in test_values:
    result = validator['validate'](field, value)
    status = "✅" if result['valid'] else "❌" if result['valid'] is False else "❓"
    print(f"{status} {field}: '{value}' - {result['message']}")
    
    if result.get('suggestions'):
        print(f"   💡 Suggestions: {', '.join(result['suggestions'])}")
```

### Lookup Change Tracking

```python
def track_lookup_changes(client, days_back=30):
    """Track changes to lookup values over time."""
    
    from datetime import datetime, timedelta
    
    cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + "Z"
    
    # Get recently modified lookups
    recent_lookups = client.lookup.get_lookups(
        filter_query=f"ModificationTimestamp ge {cutoff_date}",
        select="LookupName,LookupValue,StandardLookupValue,ModificationTimestamp,LookupActive",
        orderby="ModificationTimestamp desc",
        top=500
    )
    
    changes = {
        'total_changes': 0,
        'by_lookup_name': {},
        'recent_additions': [],
        'recent_modifications': [],
        'deactivations': []
    }
    
    for lookup in recent_lookups.get('value', []):
        changes['total_changes'] += 1
        
        lookup_name = lookup.get('LookupName', 'Unknown')
        if lookup_name not in changes['by_lookup_name']:
            changes['by_lookup_name'][lookup_name] = 0
        changes['by_lookup_name'][lookup_name] += 1
        
        lookup_entry = {
            'name': lookup_name,
            'value': lookup.get('LookupValue', ''),
            'standard_value': lookup.get('StandardLookupValue', ''),
            'timestamp': lookup.get('ModificationTimestamp', ''),
            'active': lookup.get('LookupActive', True)
        }
        
        # Categorize the change (this is simplified - would need original entry timestamp comparison)
        mod_time = lookup.get('ModificationTimestamp', '')
        orig_time = lookup.get('OriginalEntryTimestamp', '')
        
        if not lookup.get('LookupActive', True):
            changes['deactivations'].append(lookup_entry)
        elif mod_time == orig_time:  # Likely a new addition
            changes['recent_additions'].append(lookup_entry)
        else:
            changes['recent_modifications'].append(lookup_entry)
    
    # Sort by lookup name for better organization
    changes['by_lookup_name'] = dict(sorted(changes['by_lookup_name'].items(), key=lambda x: x[1], reverse=True))
    
    return changes

# Usage
lookup_changes = track_lookup_changes(client, days_back=30)
print(f"📊 Lookup Changes (Last 30 Days) - {lookup_changes['total_changes']} total changes")

print(f"\n📋 Changes by Lookup Type:")
for lookup_name, count in lookup_changes['by_lookup_name'].items():
    print(f"   {lookup_name}: {count} changes")

if lookup_changes['recent_additions']:
    print(f"\n➕ Recent Additions ({len(lookup_changes['recent_additions'])}):")
    for addition in lookup_changes['recent_additions'][:10]:
        print(f"   • {addition['name']}: {addition['value']}")

if lookup_changes['deactivations']:
    print(f"\n🚫 Recent Deactivations ({len(lookup_changes['deactivations'])}):")
    for deactivation in lookup_changes['deactivations'][:10]:
        print(f"   • {deactivation['name']}: {deactivation['value']}")
```

### Lookup Data Export

```python
def export_lookup_data(client, format='json'):
    """Export all lookup data for external use."""
    
    # Get all active lookups
    all_lookups = client.lookup.get_lookups(
        filter_query="LookupActive eq true",
        select="LookupName,LookupValue,StandardLookupValue,LookupDisplayOrder,LookupDisplayName",
        orderby="LookupName asc, LookupDisplayOrder asc",
        top=5000
    )
    
    if format == 'json':
        # Organize as nested JSON
        export_data = {}
        for lookup in all_lookups.get('value', []):
            lookup_name = lookup.get('LookupName', 'Unknown')
            if lookup_name not in export_data:
                export_data[lookup_name] = []
            
            export_data[lookup_name].append({
                'value': lookup.get('LookupValue'),
                'standard_value': lookup.get('StandardLookupValue'),
                'display_name': lookup.get('LookupDisplayName'),
                'display_order': lookup.get('LookupDisplayOrder')
            })
        
        return export_data
    
    elif format == 'csv':
        # Flat CSV format
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['LookupName', 'LookupValue', 'StandardLookupValue', 'DisplayName', 'DisplayOrder'])
        
        # Write data
        for lookup in all_lookups.get('value', []):
            writer.writerow([
                lookup.get('LookupName', ''),
                lookup.get('LookupValue', ''),
                lookup.get('StandardLookupValue', ''),
                lookup.get('LookupDisplayName', ''),
                lookup.get('LookupDisplayOrder', '')
            ])
        
        return output.getvalue()
    
    elif format == 'summary':
        # Summary statistics
        summary = {'total_lookups': 0, 'by_category': {}}
        
        for lookup in all_lookups.get('value', []):
            summary['total_lookups'] += 1
            
            lookup_name = lookup.get('LookupName', 'Unknown')
            if lookup_name not in summary['by_category']:
                summary['by_category'][lookup_name] = 0
            summary['by_category'][lookup_name] += 1
        
        summary['by_category'] = dict(sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True))
        return summary

# Usage examples
print("📤 Exporting Lookup Data...")

# Get summary
summary = export_lookup_data(client, format='summary')
print(f"📊 Lookup Summary: {summary['total_lookups']} total lookup values")
print(f"🏷️ Top Categories:")
for category, count in list(summary['by_category'].items())[:10]:
    print(f"   {category}: {count} values")

# Export as JSON (example of first few categories)
json_data = export_lookup_data(client, format='json')
print(f"\n💾 JSON Export Sample:")
for category in list(json_data.keys())[:3]:
    print(f"   {category}: {len(json_data[category])} values")
    for value in json_data[category][:3]:
        print(f"     • {value['display_name'] or value['value']}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    # Try to get lookup values
    property_types = client.lookup.get_property_type_lookups()
    
except NotFoundError:
    print("❌ Lookup data not found")
    
except ValidationError as e:
    print(f"📝 Invalid lookup request: {e}")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Performance Tips

!!! tip "Optimization Strategies"
    **Efficient Queries**
    
    - Lookup data changes infrequently - cache results for extended periods
    - Use `filter_query` to get only active lookups: `LookupActive eq true`
    - Use `select` to limit fields when you only need values for validation
    
    **Common Patterns**
    
    ```python
    # Get lookup values for dropdown lists
    dropdown_values = client.lookup.get_lookups(
        filter_query="LookupName eq 'PropertyType' and LookupActive eq true",
        select="LookupValue,LookupDisplayName,LookupDisplayOrder",
        orderby="LookupDisplayOrder asc"
    )
    
    # Validate field values efficiently
    valid_statuses = client.lookup.get_lookups(
        filter_query="LookupName eq 'StandardStatus'",
        select="LookupValue,StandardLookupValue"
    )
    ```
    
    **Caching Considerations**
    
    - Lookup values rarely change - safe to cache for hours or days
    - Build validation caches on application startup
    - Monitor `ModificationTimestamp` to detect lookup changes
    - Cache by lookup category for faster access 