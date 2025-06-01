# Data System API

The Data System API provides access to system-level information and metadata about the WFRMLS system. This includes system status, configuration details, and operational metrics.

## Overview

The `DataSystemClient` class handles all data system operations, providing methods to retrieve system information, check status, and access metadata.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
system_info = client.data_system.get_system_info()
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_system_info()` | Get system information and metadata | `Dict[str, Any]` |
| `get_system_status()` | Get current system status | `Dict[str, Any]` |
| `get_metadata()` | Get API metadata and schema information | `Dict[str, Any]` |
| `get_resource_metadata()` | Get metadata for specific resource | `Dict[str, Any]` |
| `get_lookup_metadata()` | Get lookup field metadata | `Dict[str, Any]` |

## Methods

### get_system_info()

Retrieve general system information and configuration.

```python
def get_system_info(
    self,
    **kwargs
) -> Dict[str, Any]
```

#### Example

```python
# Get system information
system_info = client.data_system.get_system_info()

print(f"System Name: {system_info['system_name']}")
print(f"Version: {system_info['version']}")
print(f"Last Updated: {system_info['last_updated']}")
print(f"Timezone: {system_info['timezone']}")
print(f"Data Coverage: {system_info['coverage_area']}")
```

### get_system_status()

Retrieve current system operational status.

```python
def get_system_status(
    self,
    **kwargs
) -> Dict[str, Any]
```

#### Example

```python
# Check system status
status = client.data_system.get_system_status()

print(f"System Status: {status['status']}")
print(f"Uptime: {status['uptime']}")
print(f"Last Maintenance: {status['last_maintenance']}")

# Check individual service status
for service, service_status in status['services'].items():
    print(f"  {service}: {service_status['status']}")
```

### get_metadata()

Retrieve comprehensive API metadata including available resources and fields.

```python
def get_metadata(
    self,
    **kwargs
) -> Dict[str, Any]
```

#### Example

```python
# Get API metadata
metadata = client.data_system.get_metadata()

print("Available Resources:")
for resource in metadata['resources']:
    print(f"  - {resource['name']}: {resource['description']}")

print(f"\nAPI Version: {metadata['api_version']}")
print(f"RESO Version: {metadata['reso_version']}")
```

### get_resource_metadata()

Retrieve metadata for a specific resource type.

```python
def get_resource_metadata(
    self,
    resource_name: str,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resource_name` | `str` | Yes | Name of the resource (Property, Member, etc.) |

#### Example

```python
# Get property resource metadata
property_metadata = client.data_system.get_resource_metadata("Property")

print(f"Resource: {property_metadata['resource_name']}")
print(f"Description: {property_metadata['description']}")
print(f"Total Fields: {len(property_metadata['fields'])}")

# List available fields
print("\nAvailable Fields:")
for field in property_metadata['fields'][:10]:  # Show first 10
    print(f"  {field['name']}: {field['type']} - {field['description']}")
```

### get_lookup_metadata()

Retrieve metadata about lookup fields and their possible values.

```python
def get_lookup_metadata(
    self,
    lookup_name: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lookup_name` | `str` | No | Specific lookup field name |

#### Example

```python
# Get all lookup metadata
lookup_metadata = client.data_system.get_lookup_metadata()

print("Available Lookup Fields:")
for lookup in lookup_metadata['lookups']:
    print(f"  {lookup['name']}: {len(lookup['values'])} values")

# Get specific lookup metadata
property_type_metadata = client.data_system.get_lookup_metadata("PropertyType")
print(f"\nProperty Type Values:")
for value in property_type_metadata['values']:
    print(f"  {value['key']}: {value['value']}")
```

## Common Use Cases

### System Health Monitoring

```python
# Monitor system health and status
def monitor_system_health():
    """Monitor system health and generate alerts if needed."""
    
    try:
        status = client.data_system.get_system_status()
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": status['status'],
            "uptime": status['uptime'],
            "services": {},
            "alerts": []
        }
        
        # Check individual services
        for service_name, service_info in status['services'].items():
            service_status = service_info['status']
            health_report['services'][service_name] = service_status
            
            # Generate alerts for down services
            if service_status.lower() != 'operational':
                health_report['alerts'].append(
                    f"Service {service_name} is {service_status}"
                )
        
        # Check for maintenance windows
        if 'maintenance_window' in status:
            maintenance = status['maintenance_window']
            if maintenance['active']:
                health_report['alerts'].append(
                    f"Maintenance window active: {maintenance['description']}"
                )
        
        return health_report
        
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "error",
            "error": str(e),
            "alerts": ["Failed to retrieve system status"]
        }

# Run health check
health = monitor_system_health()
if health['alerts']:
    print("⚠️  System Alerts:")
    for alert in health['alerts']:
        print(f"  - {alert}")
else:
    print("✅ All systems operational")
```

### API Documentation Generation

```python
# Generate API documentation from metadata
def generate_api_documentation():
    """Generate comprehensive API documentation from system metadata."""
    
    # Get overall metadata
    metadata = client.data_system.get_metadata()
    
    documentation = {
        "api_info": {
            "version": metadata['api_version'],
            "reso_version": metadata['reso_version'],
            "generated_at": datetime.now().isoformat()
        },
        "resources": {}
    }
    
    # Get detailed metadata for each resource
    for resource in metadata['resources']:
        resource_name = resource['name']
        
        try:
            resource_metadata = client.data_system.get_resource_metadata(resource_name)
            
            documentation['resources'][resource_name] = {
                "description": resource_metadata['description'],
                "endpoint": resource_metadata.get('endpoint', f"/{resource_name}"),
                "fields": {},
                "lookup_fields": []
            }
            
            # Process fields
            for field in resource_metadata['fields']:
                field_info = {
                    "type": field['type'],
                    "description": field['description'],
                    "required": field.get('required', False),
                    "max_length": field.get('max_length'),
                    "is_lookup": field.get('is_lookup', False)
                }
                
                documentation['resources'][resource_name]['fields'][field['name']] = field_info
                
                # Track lookup fields
                if field.get('is_lookup'):
                    documentation['resources'][resource_name]['lookup_fields'].append(field['name'])
        
        except Exception as e:
            print(f"Could not get metadata for {resource_name}: {e}")
    
    return documentation

# Generate documentation
api_docs = generate_api_documentation()

# Save to file
import json
with open("api_documentation.json", "w") as f:
    json.dump(api_docs, f, indent=2)

print(f"Generated documentation for {len(api_docs['resources'])} resources")
```

### Field Validation Setup

```python
# Set up field validation based on metadata
def setup_field_validation():
    """Create validation rules based on system metadata."""
    
    validation_rules = {}
    
    # Get metadata for key resources
    resources = ["Property", "Member", "Office"]
    
    for resource_name in resources:
        try:
            metadata = client.data_system.get_resource_metadata(resource_name)
            
            validation_rules[resource_name] = {
                "required_fields": [],
                "field_types": {},
                "max_lengths": {},
                "lookup_fields": {}
            }
            
            for field in metadata['fields']:
                field_name = field['name']
                
                # Required fields
                if field.get('required'):
                    validation_rules[resource_name]['required_fields'].append(field_name)
                
                # Field types
                validation_rules[resource_name]['field_types'][field_name] = field['type']
                
                # Max lengths
                if field.get('max_length'):
                    validation_rules[resource_name]['max_lengths'][field_name] = field['max_length']
                
                # Lookup fields
                if field.get('is_lookup'):
                    lookup_name = field.get('lookup_name', field_name)
                    try:
                        lookup_metadata = client.data_system.get_lookup_metadata(lookup_name)
                        valid_values = [v['key'] for v in lookup_metadata['values']]
                        validation_rules[resource_name]['lookup_fields'][field_name] = valid_values
                    except Exception as e:
                        print(f"Could not get lookup values for {lookup_name}: {e}")
        
        except Exception as e:
            print(f"Could not get metadata for {resource_name}: {e}")
    
    return validation_rules

def validate_record(resource_name: str, record_data: dict, validation_rules: dict):
    """Validate a record against the validation rules."""
    
    if resource_name not in validation_rules:
        return {"valid": False, "errors": [f"No validation rules for {resource_name}"]}
    
    rules = validation_rules[resource_name]
    errors = []
    
    # Check required fields
    for required_field in rules['required_fields']:
        if required_field not in record_data or not record_data[required_field]:
            errors.append(f"Required field missing: {required_field}")
    
    # Check field types and constraints
    for field_name, field_value in record_data.items():
        if field_value is None:
            continue
        
        # Check max length
        if field_name in rules['max_lengths']:
            max_length = rules['max_lengths'][field_name]
            if isinstance(field_value, str) and len(field_value) > max_length:
                errors.append(f"Field {field_name} exceeds max length {max_length}")
        
        # Check lookup values
        if field_name in rules['lookup_fields']:
            valid_values = rules['lookup_fields'][field_name]
            if field_value not in valid_values:
                errors.append(f"Invalid value for {field_name}: {field_value}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

# Setup validation
validation_rules = setup_field_validation()

# Example validation
property_data = {
    "ListingId": "1234567",
    "PropertyType": "RES",
    "StandardStatus": "Active",
    "ListPrice": 500000
}

validation_result = validate_record("Property", property_data, validation_rules)
if not validation_result["valid"]:
    print("Validation errors:")
    for error in validation_result["errors"]:
        print(f"  - {error}")
```

### Schema Evolution Tracking

```python
# Track schema changes over time
def track_schema_changes():
    """Track changes in API schema over time."""
    
    import json
    from pathlib import Path
    
    schema_file = Path("schema_history.json")
    
    # Load previous schema if exists
    if schema_file.exists():
        with open(schema_file, 'r') as f:
            schema_history = json.load(f)
    else:
        schema_history = {"versions": []}
    
    # Get current metadata
    current_metadata = client.data_system.get_metadata()
    current_timestamp = datetime.now().isoformat()
    
    # Create current schema snapshot
    current_schema = {
        "timestamp": current_timestamp,
        "api_version": current_metadata['api_version'],
        "reso_version": current_metadata['reso_version'],
        "resources": {}
    }
    
    # Get detailed schema for each resource
    for resource in current_metadata['resources']:
        resource_name = resource['name']
        try:
            resource_metadata = client.data_system.get_resource_metadata(resource_name)
            current_schema['resources'][resource_name] = {
                "field_count": len(resource_metadata['fields']),
                "fields": {field['name']: field['type'] for field in resource_metadata['fields']}
            }
        except Exception as e:
            print(f"Could not get metadata for {resource_name}: {e}")
    
    # Compare with previous version if exists
    changes = []
    if schema_history['versions']:
        previous_schema = schema_history['versions'][-1]
        
        # Check for version changes
        if current_schema['api_version'] != previous_schema['api_version']:
            changes.append(f"API version changed: {previous_schema['api_version']} -> {current_schema['api_version']}")
        
        # Check for resource changes
        for resource_name, resource_info in current_schema['resources'].items():
            if resource_name in previous_schema['resources']:
                prev_resource = previous_schema['resources'][resource_name]
                
                # Check field count changes
                if resource_info['field_count'] != prev_resource['field_count']:
                    changes.append(f"{resource_name}: Field count changed {prev_resource['field_count']} -> {resource_info['field_count']}")
                
                # Check for new/removed fields
                current_fields = set(resource_info['fields'].keys())
                previous_fields = set(prev_resource['fields'].keys())
                
                new_fields = current_fields - previous_fields
                removed_fields = previous_fields - current_fields
                
                if new_fields:
                    changes.append(f"{resource_name}: New fields added: {', '.join(new_fields)}")
                if removed_fields:
                    changes.append(f"{resource_name}: Fields removed: {', '.join(removed_fields)}")
            else:
                changes.append(f"New resource added: {resource_name}")
    
    # Add current schema to history
    current_schema['changes'] = changes
    schema_history['versions'].append(current_schema)
    
    # Keep only last 10 versions
    if len(schema_history['versions']) > 10:
        schema_history['versions'] = schema_history['versions'][-10:]
    
    # Save updated history
    with open(schema_file, 'w') as f:
        json.dump(schema_history, f, indent=2)
    
    return {
        "current_version": current_schema['api_version'],
        "changes_detected": len(changes),
        "changes": changes
    }

# Track schema changes
schema_changes = track_schema_changes()
if schema_changes['changes']:
    print("Schema changes detected:")
    for change in schema_changes['changes']:
        print(f"  - {change}")
```

## Field Reference

### System Information Fields

| Field | Type | Description |
|-------|------|-------------|
| `system_name` | `str` | Name of the MLS system |
| `version` | `str` | System version |
| `api_version` | `str` | API version |
| `reso_version` | `str` | RESO standard version |
| `timezone` | `str` | System timezone |
| `coverage_area` | `str` | Geographic coverage area |

### Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `str` | Overall system status |
| `uptime` | `str` | System uptime |
| `last_maintenance` | `datetime` | Last maintenance timestamp |
| `services` | `dict` | Individual service statuses |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `resources` | `list` | Available API resources |
| `field_count` | `int` | Total number of fields |
| `lookup_count` | `int` | Number of lookup fields |
| `last_updated` | `datetime` | Metadata last update time |

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    system_info = client.data_system.get_system_info()
except ValidationError as e:
    print(f"Invalid request: {e}")
except Exception as e:
    print(f"Error retrieving system info: {e}")
```

## Best Practices

### Monitoring

1. **Check system status regularly** for operational awareness
2. **Monitor for maintenance windows** to plan operations
3. **Track API version changes** for compatibility
4. **Set up alerts** for system issues

### Metadata Usage

1. **Cache metadata** as it changes infrequently
2. **Use metadata for validation** before API calls
3. **Generate documentation** from metadata
4. **Track schema evolution** over time

### Integration

1. **Validate system compatibility** before deployment
2. **Handle version differences** gracefully
3. **Use lookup metadata** for data validation
4. **Monitor field availability** for new features

## Related Resources

- [Error Handling Guide](../guides/error-handling.md) - Exception management
- [API Reference](index.md) - Complete API documentation
- [RESO Standards](../reference/reso-standards.md) - Industry standards