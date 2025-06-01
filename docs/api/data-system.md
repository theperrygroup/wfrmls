# Data System API

The Data System API provides access to data system metadata, including version details, contact information, and system capabilities. This API is essential for understanding the WFRMLS system configuration and capabilities.

!!! example "Quick Start"
    ```python
    # Get system information
    system_info = client.data_system.get_system_info()
    
    # Get specific data system by key
    system = client.data_system.get_data_system("WFRMLS")
    
    # Get all data systems
    systems = client.data_system.get_data_systems()
    ```

## Data System Client

::: wfrmls.data_system.DataSystemClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### System Information Retrieval

=== "Basic System Info"
    ```python
    # Get general system information
    system_info = client.data_system.get_system_info()
    
    # Get all available data systems
    all_systems = client.data_system.get_data_systems(top=50)
    
    # Get data systems with specific ordering
    systems_by_name = client.data_system.get_data_systems(
        orderby="DataSystemName asc"
    )
    ```

=== "Specific System Details"
    ```python
    # Get WFRMLS system details
    wfrmls_system = client.data_system.get_data_system("WFRMLS")
    
    # Get system by name (if different from key)
    system = client.data_system.get_data_systems(
        filter_query="DataSystemName eq 'WFRMLS Production'",
        top=1
    )
    ```

=== "System Capabilities"
    ```python
    # Get systems with contact information
    systems_with_contact = client.data_system.get_data_systems(
        filter_query="DataSystemContactEmail ne null",
        select="DataSystemKey,DataSystemName,DataSystemContactEmail,DataSystemVersion"
    )
    
    # Get systems by status
    active_systems = client.data_system.get_data_systems(
        filter_query="DataSystemStatus eq 'Active'",
        orderby="DataSystemName asc"
    )
    ```

## Data System Data Structure

Data Systems in WFRMLS follow the RESO standard with comprehensive system metadata:

??? info "Key Data System Fields"
    **System Identification**
    
    - `DataSystemKey` - Unique system identifier
    - `DataSystemName` - Human-readable system name
    - `DataSystemDescription` - System description
    - `DataSystemAbbreviation` - System abbreviation
    - `DataSystemVersion` - Current system version

    **Contact Information**
    
    - `DataSystemContactEmail` - Contact email for support
    - `DataSystemContactPhone` - Contact phone number
    - `DataSystemContactName` - Contact person name
    - `DataSystemURL` - System website URL

    **Technical Details**
    
    - `DataSystemStatus` - System status (Active, Inactive, etc.)
    - `DataSystemTimeZone` - System timezone
    - `DataSystemLocale` - System locale/language
    - `DataSystemCurrency` - Default currency

    **Timestamps**
    
    - `ModificationTimestamp` - Last update time
    - `OriginalEntryTimestamp` - Initial creation time

## Integration Examples

### System Status Dashboard

```python
def create_system_status_dashboard(client):
    """Create a comprehensive system status dashboard."""
    
    # Get all data systems
    systems = client.data_system.get_data_systems(
        select="DataSystemKey,DataSystemName,DataSystemVersion,DataSystemStatus,DataSystemContactEmail,ModificationTimestamp",
        orderby="DataSystemName asc",
        top=50
    )
    
    dashboard = {
        'total_systems': 0,
        'active_systems': 0,
        'systems_with_contact': 0,
        'systems': [],
        'latest_update': None
    }
    
    latest_timestamp = None
    
    for system in systems.get('value', []):
        dashboard['total_systems'] += 1
        
        status = system.get('DataSystemStatus', 'Unknown')
        if status == 'Active':
            dashboard['active_systems'] += 1
        
        if system.get('DataSystemContactEmail'):
            dashboard['systems_with_contact'] += 1
        
        # Track latest modification
        mod_timestamp = system.get('ModificationTimestamp')
        if mod_timestamp:
            if not latest_timestamp or mod_timestamp > latest_timestamp:
                latest_timestamp = mod_timestamp
                dashboard['latest_update'] = mod_timestamp
        
        dashboard['systems'].append({
            'key': system.get('DataSystemKey', 'Unknown'),
            'name': system.get('DataSystemName', 'Unknown'),
            'version': system.get('DataSystemVersion', 'Unknown'),
            'status': status,
            'contact_email': system.get('DataSystemContactEmail'),
            'last_modified': mod_timestamp
        })
    
    return dashboard

# Usage
system_dashboard = create_system_status_dashboard(client)
print(f"🖥️ Data System Status Dashboard")
print(f"   Total Systems: {system_dashboard['total_systems']}")
print(f"   Active Systems: {system_dashboard['active_systems']} ({system_dashboard['active_systems']/system_dashboard['total_systems']*100:.1f}%)")
print(f"   Systems with Contact: {system_dashboard['systems_with_contact']}")
print(f"   Latest Update: {system_dashboard['latest_update']}")

print(f"\n📋 System Details:")
for system in system_dashboard['systems']:
    status_icon = "✅" if system['status'] == 'Active' else "❌"
    contact_icon = "📧" if system['contact_email'] else "❓"
    print(f"   {status_icon} {system['name']} (v{system['version']})")
    print(f"      Key: {system['key']} | Contact: {contact_icon}")
```

### System Configuration Audit

```python
def audit_system_configuration(client):
    """Audit system configuration for completeness and compliance."""
    
    # Get all systems with full details
    systems = client.data_system.get_data_systems(top=100)
    
    audit_results = {
        'total_systems': 0,
        'complete_configs': 0,
        'missing_contact': [],
        'missing_version': [],
        'inactive_systems': [],
        'outdated_systems': [],
        'configuration_issues': []
    }
    
    for system in systems.get('value', []):
        audit_results['total_systems'] += 1
        
        name = system.get('DataSystemName', 'Unknown')
        key = system.get('DataSystemKey', 'Unknown')
        system_display = f"{name} ({key})"
        
        issues = []
        
        # Check contact information
        if not system.get('DataSystemContactEmail'):
            issues.append('Missing contact email')
            audit_results['missing_contact'].append(system_display)
        
        # Check version information
        version = system.get('DataSystemVersion')
        if not version or version.lower() in ['unknown', 'n/a', '']:
            issues.append('Missing version info')
            audit_results['missing_version'].append(system_display)
        
        # Check system status
        status = system.get('DataSystemStatus', 'Unknown')
        if status != 'Active':
            issues.append(f'Inactive status: {status}')
            audit_results['inactive_systems'].append(system_display)
        
        # Check for potential outdated systems (basic heuristic)
        if version and any(old_version in version.lower() for old_version in ['1.0', '2.0', 'beta', 'test']):
            issues.append('Potentially outdated version')
            audit_results['outdated_systems'].append(system_display)
        
        if not issues:
            audit_results['complete_configs'] += 1
        else:
            audit_results['configuration_issues'].append({
                'system': system_display,
                'issues': issues
            })
    
    return audit_results

# Usage
audit_report = audit_system_configuration(client)
print(f"🔍 System Configuration Audit")
print(f"   Total Systems: {audit_report['total_systems']}")
print(f"   Complete Configurations: {audit_report['complete_configs']} ({audit_report['complete_configs']/audit_report['total_systems']*100:.1f}%)")
print(f"   Missing Contact Info: {len(audit_report['missing_contact'])} systems")
print(f"   Missing Version Info: {len(audit_report['missing_version'])} systems")
print(f"   Inactive Systems: {len(audit_report['inactive_systems'])} systems")

if audit_report['configuration_issues']:
    print(f"\n⚠️ Configuration Issues:")
    for issue in audit_report['configuration_issues'][:10]:
        print(f"   - {issue['system']}")
        for problem in issue['issues']:
            print(f"     • {problem}")
```

### Version Tracking

```python
def track_system_versions(client):
    """Track system versions and update history."""
    
    # Get systems with version information
    systems = client.data_system.get_data_systems(
        select="DataSystemKey,DataSystemName,DataSystemVersion,ModificationTimestamp,OriginalEntryTimestamp",
        orderby="ModificationTimestamp desc",
        top=100
    )
    
    version_tracking = {
        'systems_by_version': {},
        'recent_updates': [],
        'version_distribution': {},
        'update_timeline': []
    }
    
    for system in systems.get('value', []):
        name = system.get('DataSystemName', 'Unknown')
        version = system.get('DataSystemVersion', 'Unknown')
        mod_time = system.get('ModificationTimestamp')
        
        # Group by version
        if version not in version_tracking['systems_by_version']:
            version_tracking['systems_by_version'][version] = []
        version_tracking['systems_by_version'][version].append(name)
        
        # Count version distribution
        version_tracking['version_distribution'][version] = version_tracking['version_distribution'].get(version, 0) + 1
        
        # Track recent updates
        if mod_time:
            from datetime import datetime, timedelta
            try:
                mod_datetime = datetime.fromisoformat(mod_time.replace('Z', '+00:00'))
                days_ago = (datetime.now(mod_datetime.tzinfo) - mod_datetime).days
                
                if days_ago <= 30:  # Recent updates (last 30 days)
                    version_tracking['recent_updates'].append({
                        'system': name,
                        'version': version,
                        'days_ago': days_ago,
                        'timestamp': mod_time
                    })
                
                version_tracking['update_timeline'].append({
                    'system': name,
                    'version': version,
                    'date': mod_datetime.strftime('%Y-%m-%d'),
                    'days_ago': days_ago
                })
            except:
                pass
    
    # Sort recent updates by recency
    version_tracking['recent_updates'].sort(key=lambda x: x['days_ago'])
    
    return version_tracking

# Usage
version_report = track_system_versions(client)
print(f"📊 System Version Tracking")

print(f"\n🏷️ Version Distribution:")
for version, count in sorted(version_report['version_distribution'].items(), key=lambda x: x[1], reverse=True):
    print(f"   {version}: {count} systems")

if version_report['recent_updates']:
    print(f"\n🔄 Recent Updates (Last 30 days):")
    for update in version_report['recent_updates'][:10]:
        print(f"   📅 {update['days_ago']} days ago: {update['system']} → v{update['version']}")

print(f"\n📈 Systems by Version:")
for version, systems in version_report['systems_by_version'].items():
    print(f"   {version}:")
    for system in systems[:5]:  # Show first 5 systems per version
        print(f"     - {system}")
    if len(systems) > 5:
        print(f"     ... and {len(systems) - 5} more")
```

### System Health Check

```python
def perform_system_health_check(client):
    """Perform a comprehensive system health check."""
    
    try:
        # Test basic connectivity
        systems = client.data_system.get_data_systems(top=5)
        
        health_status = {
            'connectivity': 'OK',
            'response_time': None,
            'data_availability': 'OK',
            'system_count': len(systems.get('value', [])),
            'issues': []
        }
        
        # Check if we got any data
        if not systems.get('value'):
            health_status['data_availability'] = 'WARNING'
            health_status['issues'].append('No data systems returned')
        
        # Basic validation of returned data
        for system in systems.get('value', []):
            if not system.get('DataSystemKey'):
                health_status['issues'].append('System missing DataSystemKey')
            if not system.get('DataSystemName'):
                health_status['issues'].append('System missing DataSystemName')
        
        # Check for required WFRMLS system
        wfrmls_found = False
        for system in systems.get('value', []):
            if 'WFRMLS' in system.get('DataSystemName', '').upper():
                wfrmls_found = True
                break
        
        if not wfrmls_found:
            health_status['issues'].append('WFRMLS system not found in first 5 results')
        
        # Determine overall health
        if health_status['issues']:
            health_status['overall'] = 'WARNING' if len(health_status['issues']) < 3 else 'ERROR'
        else:
            health_status['overall'] = 'HEALTHY'
        
        return health_status
        
    except Exception as e:
        return {
            'connectivity': 'ERROR',
            'overall': 'ERROR',
            'error': str(e),
            'issues': [f'Connection failed: {str(e)}']
        }

# Usage
health_check = perform_system_health_check(client)
status_icon = {
    'HEALTHY': '✅',
    'WARNING': '⚠️',
    'ERROR': '❌'
}.get(health_check['overall'], '❓')

print(f"🏥 System Health Check: {status_icon} {health_check['overall']}")
print(f"   Connectivity: {health_check['connectivity']}")
print(f"   Data Availability: {health_check.get('data_availability', 'Unknown')}")
print(f"   Systems Found: {health_check.get('system_count', 0)}")

if health_check.get('issues'):
    print(f"\n⚠️ Issues Detected:")
    for issue in health_check['issues']:
        print(f"   - {issue}")

if health_check.get('error'):
    print(f"\n❌ Error: {health_check['error']}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    # Try to get system information
    system_info = client.data_system.get_system_info()
    
except NotFoundError:
    print("❌ Data system information not found")
    
except ValidationError as e:
    print(f"📝 Invalid request parameters: {e}")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Performance Tips

!!! tip "Optimization Strategies"
    **Efficient Queries**
    
    - Data system information changes infrequently - cache results for extended periods
    - Use `select` to limit fields when you only need basic system info
    - Filter by status to get only active systems if needed
    
    **Common Patterns**
    
    ```python
    # Get essential system info only
    basic_systems = client.data_system.get_data_systems(
        select="DataSystemKey,DataSystemName,DataSystemVersion,DataSystemStatus",
        orderby="DataSystemName asc"
    )
    
    # Check for specific system efficiently
    wfrmls_system = client.data_system.get_data_systems(
        filter_query="contains(tolower(DataSystemName), 'wfrmls')",
        top=1
    )
    ```
    
    **Caching Considerations**
    
    - System metadata rarely changes - safe to cache for hours or days
    - Monitor `ModificationTimestamp` to detect configuration changes
    - Use system health checks periodically to ensure connectivity 