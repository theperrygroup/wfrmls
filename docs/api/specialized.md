# Specialized APIs

This section covers the specialized WFRMLS APIs that provide access to specific data types and system functionality: ADU (Accessory Dwelling Units), Deleted Records, Property Unit Types, and Resource metadata.

<div class="grid cards" markdown>

-   :material-home-plus:{ .lg .middle } **ADU API**

    ---

    Accessory Dwelling Unit data and classifications

    [:octicons-arrow-right-24: ADU Documentation](#adu-api)

-   :material-delete:{ .lg .middle } **Deleted Records**

    ---

    Deleted record tracking for data synchronization

    [:octicons-arrow-right-24: Deleted Records](#deleted-records-api)

-   :material-format-list-bulleted-type:{ .lg .middle } **Property Unit Types**

    ---

    Property unit classifications and types

    [:octicons-arrow-right-24: Unit Types](#property-unit-types-api)

-   :material-api:{ .lg .middle } **Resource Metadata**

    ---

    API resource definitions and metadata

    [:octicons-arrow-right-24: Resource API](#resource-api)

</div>

---

## ADU API

The ADU (Accessory Dwelling Unit) API provides access to information about secondary housing units on properties, including types, statuses, and property relationships.

!!! example "Quick Start"
    ```python
    # Get all ADUs
    adus = client.adu.get_adus()
    
    # Get existing ADUs
    existing_adus = client.adu.get_existing_adus()
    
    # Get ADUs for a specific property
    property_adus = client.adu.get_adus_for_property("1611952")
    ```

### ADU Client

::: wfrmls.adu.AduClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Common ADU Usage Patterns

=== "Basic ADU Retrieval"
    ```python
    # Get all ADUs
    all_adus = client.adu.get_adus(top=100)
    
    # Get existing/completed ADUs
    existing_adus = client.adu.get_existing_adus(top=50)
    
    # Get ADUs with specific status
    permitted_adus = client.adu.get_adus(
        filter_query="AduStatus eq 'Permitted'",
        orderby="ModificationTimestamp desc"
    )
    ```

=== "Property-Specific ADUs"
    ```python
    # Get ADUs for a specific property
    property_adus = client.adu.get_adus_for_property("1611952")
    
    # Get ADUs with property information
    adus_with_property = client.adu.get_adus_with_property(
        filter_query="AduType eq 'Detached'",
        top=25
    )
    ```

=== "ADU Analytics"
    ```python
    # Get ADU distribution by type
    def get_adu_analytics(client):
        adus = client.adu.get_adus(
            select="AduType,AduStatus,AduSquareFootage,PropertyKey",
            top=1000
        )
        
        analytics = {
            'total_adus': 0,
            'by_type': {},
            'by_status': {},
            'avg_sq_ft': 0
        }
        
        sq_ft_values = []
        for adu in adus.get('value', []):
            analytics['total_adus'] += 1
            
            adu_type = adu.get('AduType', 'Unknown')
            analytics['by_type'][adu_type] = analytics['by_type'].get(adu_type, 0) + 1
            
            status = adu.get('AduStatus', 'Unknown')
            analytics['by_status'][status] = analytics['by_status'].get(status, 0) + 1
            
            sq_ft = adu.get('AduSquareFootage')
            if sq_ft:
                sq_ft_values.append(sq_ft)
        
        if sq_ft_values:
            analytics['avg_sq_ft'] = sum(sq_ft_values) / len(sq_ft_values)
        
        return analytics
    ```

---

## Deleted Records API

The Deleted Records API provides access to deleted record tracking, essential for maintaining data integrity when replicating MLS data.

!!! example "Quick Start"
    ```python
    # Get recent deletions
    deleted = client.deleted.get_deleted(top=50)
    
    # Get deleted properties since yesterday
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    deleted_properties = client.deleted.get_deleted_since(
        since=yesterday.isoformat() + "Z",
        resource_name="Property"
    )
    
    # Get deleted property records
    deleted_props = client.deleted.get_deleted_property_records()
    ```

### Deleted Records Client

::: wfrmls.deleted.DeletedClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Common Deleted Records Patterns

=== "Basic Deletion Tracking"
    ```python
    # Get all recent deletions
    recent_deletions = client.deleted.get_deleted(
        orderby="DeletedDateTime desc",
        top=100
    )
    
    # Get deletions for specific resource
    deleted_properties = client.deleted.get_deleted_property_records(
        orderby="DeletedDateTime desc",
        top=50
    )
    
    # Get deletions within date range
    from datetime import datetime, timedelta
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    
    weekly_deletions = client.deleted.get_deleted(
        filter_query=f"DeletedDateTime ge {week_ago}",
        orderby="DeletedDateTime desc"
    )
    ```

=== "Synchronization Support"
    ```python
    # Sync deleted records since last update
    def sync_deletions(client, last_sync_time):
        """Sync deletions since last synchronization."""
        
        deleted_records = client.deleted.get_deleted_since(
            since=last_sync_time,
            orderby="DeletedDateTime asc"
        )
        
        sync_report = {
            'total_deletions': 0,
            'by_resource': {},
            'sync_timestamp': datetime.utcnow().isoformat() + "Z"
        }
        
        for record in deleted_records.get('value', []):
            sync_report['total_deletions'] += 1
            
            resource_name = record.get('ResourceName', 'Unknown')
            if resource_name not in sync_report['by_resource']:
                sync_report['by_resource'][resource_name] = []
            
            sync_report['by_resource'][resource_name].append({
                'key': record.get('ResourceRecordKey'),
                'deleted_at': record.get('DeletedDateTime')
            })
        
        return sync_report
    
    # Usage
    last_sync = "2024-01-01T00:00:00Z"
    sync_results = sync_deletions(client, last_sync)
    ```

=== "Deletion Analytics"
    ```python
    # Analyze deletion patterns
    def analyze_deletion_patterns(client, days_back=30):
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + "Z"
        
        deletions = client.deleted.get_deleted(
            filter_query=f"DeletedDateTime ge {cutoff_date}",
            select="ResourceName,ResourceRecordKey,DeletedDateTime",
            top=1000
        )
        
        analysis = {
            'total_deletions': 0,
            'by_resource': defaultdict(int),
            'by_day': defaultdict(int),
            'deletion_rate': {}
        }
        
        for deletion in deletions.get('value', []):
            analysis['total_deletions'] += 1
            
            resource = deletion.get('ResourceName', 'Unknown')
            analysis['by_resource'][resource] += 1
            
            # Parse date for daily analysis
            deleted_at = deletion.get('DeletedDateTime', '')
            if deleted_at:
                try:
                    date = datetime.fromisoformat(deleted_at.replace('Z', '+00:00')).date()
                    analysis['by_day'][str(date)] += 1
                except:
                    pass
        
        # Calculate daily averages
        for resource, count in analysis['by_resource'].items():
            analysis['deletion_rate'][resource] = count / days_back
        
        return analysis
    ```

---

## Property Unit Types API

The Property Unit Types API provides access to property unit classifications and type information.

!!! example "Quick Start"
    ```python
    # Get all unit types
    unit_types = client.property_unit_types.get_property_unit_types()
    
    # Get residential unit types
    residential = client.property_unit_types.get_residential_unit_types()
    
    # Get commercial unit types
    commercial = client.property_unit_types.get_commercial_unit_types()
    ```

### Property Unit Types Client

::: wfrmls.property_unit_types.PropertyUnitTypesClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Common Unit Types Patterns

=== "Basic Unit Type Retrieval"
    ```python
    # Get all property unit types
    all_types = client.property_unit_types.get_property_unit_types(top=100)
    
    # Get residential unit types
    residential_types = client.property_unit_types.get_residential_unit_types()
    
    # Get commercial unit types  
    commercial_types = client.property_unit_types.get_commercial_unit_types()
    
    # Get unit types with specific classification
    condo_types = client.property_unit_types.get_property_unit_types(
        filter_query="contains(tolower(PropertyUnitTypeName), 'condo')"
    )
    ```

=== "Unit Type Analysis"
    ```python
    # Analyze unit type distribution
    def analyze_unit_types(client):
        unit_types = client.property_unit_types.get_property_unit_types(
            select="PropertyUnitTypeKey,PropertyUnitTypeName,PropertyUnitTypeCategory",
            top=200
        )
        
        analysis = {
            'total_types': 0,
            'by_category': {},
            'categories': []
        }
        
        for unit_type in unit_types.get('value', []):
            analysis['total_types'] += 1
            
            category = unit_type.get('PropertyUnitTypeCategory', 'Unknown')
            if category not in analysis['by_category']:
                analysis['by_category'][category] = []
            
            analysis['by_category'][category].append({
                'key': unit_type.get('PropertyUnitTypeKey'),
                'name': unit_type.get('PropertyUnitTypeName', 'Unknown')
            })
        
        analysis['categories'] = list(analysis['by_category'].keys())
        return analysis
    ```

---

## Resource API

The Resource API provides access to API resource metadata, including field definitions, data types, and resource relationships.

!!! example "Quick Start"
    ```python
    # Get all resources
    resources = client.resource.get_resources()
    
    # Get Property resource metadata
    property_resource = client.resource.get_resource_by_name("Property")
    
    # Get specific resource by key
    resource_detail = client.resource.get_resource("PropertyResourceKey")
    ```

### Resource Client

::: wfrmls.resource.ResourceClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Common Resource Patterns

=== "Resource Discovery"
    ```python
    # Get all available resources
    all_resources = client.resource.get_resources(top=50)
    
    # Get resources with field information
    resources_with_fields = client.resource.get_resources_with_fields()
    
    # Get specific resource metadata
    property_resource = client.resource.get_resource_by_name("Property")
    
    # Discover resource capabilities
    def discover_resources(client):
        resources = client.resource.get_resources(
            select="ResourceName,ResourceDescription,ResourcePath"
        )
        
        discovery = {
            'available_resources': [],
            'total_count': 0
        }
        
        for resource in resources.get('value', []):
            discovery['total_count'] += 1
            discovery['available_resources'].append({
                'name': resource.get('ResourceName', 'Unknown'),
                'description': resource.get('ResourceDescription', ''),
                'path': resource.get('ResourcePath', '')
            })
        
        return discovery
    ```

=== "Field Analysis"
    ```python
    # Analyze resource fields
    def analyze_resource_fields(client, resource_name="Property"):
        try:
            resource = client.resource.get_resource_by_name(resource_name)
            fields_info = client.resource.get_resource_fields(resource_name)
            
            analysis = {
                'resource_name': resource_name,
                'total_fields': 0,
                'field_types': {},
                'required_fields': [],
                'optional_fields': []
            }
            
            for field in fields_info.get('value', []):
                analysis['total_fields'] += 1
                
                field_type = field.get('FieldType', 'Unknown')
                analysis['field_types'][field_type] = analysis['field_types'].get(field_type, 0) + 1
                
                field_name = field.get('FieldName', '')
                is_required = field.get('IsRequired', False)
                
                if is_required:
                    analysis['required_fields'].append(field_name)
                else:
                    analysis['optional_fields'].append(field_name)
            
            return analysis
            
        except Exception as e:
            return {'error': f'Could not analyze fields for {resource_name}: {e}'}
    ```

## Integration Examples

### Data Synchronization System

```python
def create_sync_system(client):
    """Create a comprehensive data synchronization system."""
    
    sync_manager = {
        'last_sync_times': {},
        'deletion_log': [],
        'resource_metadata': {}
    }
    
    def initialize_sync():
        # Get available resources
        resources = client.resource.get_resources()
        for resource in resources.get('value', []):
            resource_name = resource.get('ResourceName', '')
            if resource_name:
                sync_manager['last_sync_times'][resource_name] = datetime.utcnow().isoformat() + "Z"
                sync_manager['resource_metadata'][resource_name] = resource
        
        return f"Initialized sync for {len(sync_manager['last_sync_times'])} resources"
    
    def sync_deletions(resource_name=None):
        if resource_name and resource_name in sync_manager['last_sync_times']:
            last_sync = sync_manager['last_sync_times'][resource_name]
            
            deletions = client.deleted.get_deleted_since(
                since=last_sync,
                resource_name=resource_name
            )
            
            for deletion in deletions.get('value', []):
                sync_manager['deletion_log'].append({
                    'resource': resource_name,
                    'record_key': deletion.get('ResourceRecordKey'),
                    'deleted_at': deletion.get('DeletedDateTime'),
                    'synced_at': datetime.utcnow().isoformat() + "Z"
                })
            
            # Update last sync time
            sync_manager['last_sync_times'][resource_name] = datetime.utcnow().isoformat() + "Z"
            
            return f"Synced {len(deletions.get('value', []))} deletions for {resource_name}"
        else:
            return "Resource not found or not initialized"
    
    def get_sync_status():
        return {
            'resources_tracked': len(sync_manager['last_sync_times']),
            'total_deletions_synced': len(sync_manager['deletion_log']),
            'last_sync_times': sync_manager['last_sync_times']
        }
    
    return {
        'initialize': initialize_sync,
        'sync_deletions': sync_deletions,
        'get_status': get_sync_status,
        'manager': sync_manager
    }

# Usage
sync_system = create_sync_system(client)
print(sync_system['initialize']())
print(sync_system['sync_deletions']('Property'))
print(sync_system['get_status']())
```

### Comprehensive System Health Check

```python
def perform_comprehensive_health_check(client):
    """Perform health check across all specialized APIs."""
    
    health_report = {
        'timestamp': datetime.utcnow().isoformat() + "Z",
        'overall_status': 'HEALTHY',
        'api_status': {},
        'issues': []
    }
    
    # Test ADU API
    try:
        adus = client.adu.get_adus(top=5)
        health_report['api_status']['ADU'] = {
            'status': 'OK',
            'record_count': len(adus.get('value', [])),
            'response_time': 'N/A'  # Would need timing logic
        }
    except Exception as e:
        health_report['api_status']['ADU'] = {'status': 'ERROR', 'error': str(e)}
        health_report['issues'].append(f'ADU API: {str(e)}')
    
    # Test Deleted Records API
    try:
        deleted = client.deleted.get_deleted(top=5)
        health_report['api_status']['Deleted'] = {
            'status': 'OK',
            'record_count': len(deleted.get('value', [])),
            'response_time': 'N/A'
        }
    except Exception as e:
        health_report['api_status']['Deleted'] = {'status': 'ERROR', 'error': str(e)}
        health_report['issues'].append(f'Deleted Records API: {str(e)}')
    
    # Test Property Unit Types API
    try:
        unit_types = client.property_unit_types.get_property_unit_types(top=5)
        health_report['api_status']['PropertyUnitTypes'] = {
            'status': 'OK',
            'record_count': len(unit_types.get('value', [])),
            'response_time': 'N/A'
        }
    except Exception as e:
        health_report['api_status']['PropertyUnitTypes'] = {'status': 'ERROR', 'error': str(e)}
        health_report['issues'].append(f'Property Unit Types API: {str(e)}')
    
    # Test Resource API
    try:
        resources = client.resource.get_resources(top=5)
        health_report['api_status']['Resource'] = {
            'status': 'OK',
            'record_count': len(resources.get('value', [])),
            'response_time': 'N/A'
        }
    except Exception as e:
        health_report['api_status']['Resource'] = {'status': 'ERROR', 'error': str(e)}
        health_report['issues'].append(f'Resource API: {str(e)}')
    
    # Determine overall status
    error_count = sum(1 for api in health_report['api_status'].values() if api['status'] == 'ERROR')
    if error_count > 0:
        health_report['overall_status'] = 'ERROR' if error_count >= 2 else 'WARNING'
    
    return health_report

# Usage
health_check = perform_comprehensive_health_check(client)
status_icon = {'HEALTHY': '✅', 'WARNING': '⚠️', 'ERROR': '❌'}.get(health_check['overall_status'], '❓')

print(f"🏥 Specialized APIs Health Check: {status_icon} {health_check['overall_status']}")
for api_name, status in health_check['api_status'].items():
    api_icon = "✅" if status['status'] == 'OK' else "❌"
    print(f"   {api_icon} {api_name}: {status['status']}")
    if status['status'] == 'OK':
        print(f"      Records: {status['record_count']}")

if health_check['issues']:
    print(f"\n⚠️ Issues Detected:")
    for issue in health_check['issues']:
        print(f"   - {issue}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

# ADU API error handling
try:
    adus = client.adu.get_adus_for_property("invalid_property_id")
except NotFoundError:
    print("❌ Property not found or has no ADUs")
except Exception as e:
    print(f"🚨 ADU API error: {e}")

# Deleted Records API error handling
try:
    deleted = client.deleted.get_deleted_since("invalid_date")
except ValidationError as e:
    print(f"📝 Invalid date format: {e}")
except Exception as e:
    print(f"🚨 Deleted Records API error: {e}")
```

## Performance Tips

!!! tip "Specialized APIs Optimization"
    **Caching Strategies**
    
    - ADU data changes infrequently - cache for hours
    - Property Unit Types rarely change - cache for days
    - Resource metadata is static - cache for extended periods
    - Deleted records need frequent updates for sync accuracy
    
    **Efficient Queries**
    
    ```python
    # Efficient ADU queries
    recent_adus = client.adu.get_adus(
        filter_query="ModificationTimestamp ge '2024-01-01T00:00:00Z'",
        select="AduKey,AduType,AduStatus,PropertyKey",
        top=100
    )
    
    # Efficient deletion tracking
    recent_deletions = client.deleted.get_deleted(
        filter_query="DeletedDateTime ge '2024-01-15T00:00:00Z'",
        select="ResourceName,ResourceRecordKey,DeletedDateTime",
        orderby="DeletedDateTime desc"
    )
    