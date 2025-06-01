# Core Client

The `WFRMLSClient` is the main entry point for accessing the WFRMLS API. It provides access to all available resources through service-specific client properties using lazy initialization.

!!! example "Quick Start"
    ```python
    from wfrmls import WFRMLSClient
    
    # Initialize with bearer token
    client = WFRMLSClient(bearer_token="your_token_here")
    
    # Or use environment variable (recommended)
    import os
    os.environ['WFRMLS_BEARER_TOKEN'] = "your_token_here"
    client = WFRMLSClient()
    
    # Discover available resources
    service_doc = client.get_service_document()
    metadata = client.get_metadata()
    ```

## Main Client Class

::: wfrmls.client.WFRMLSClient
    options:
      members:
        - __init__
        - get_service_document  
        - get_metadata
        - property
        - member
        - office
        - openhouse
        - data_system
        - resource
        - property_unit_types
        - lookup
        - adu
        - deleted
      show_root_heading: true
      show_source: false
      heading_level: 3

## Service Discovery

The client provides two methods for discovering available API resources and understanding the data schema:

### Service Document

The service document lists all available entity sets (resources) that can be accessed:

```python
service_doc = client.get_service_document()

# Explore available resources
for resource in service_doc.get('value', []):
    print(f"📋 {resource['name']} - {resource['url']}")
    if 'title' in resource:
        print(f"   {resource['title']}")
```

??? example "Example Service Document Response"
    ```json
    {
        "@odata.context": "https://api.wfrmls.com/RETS/api/$metadata",
        "value": [
            {
                "name": "Property",
                "kind": "EntitySet",
                "url": "Property",
                "title": "Property listings and details"
            },
            {
                "name": "Member", 
                "kind": "EntitySet",
                "url": "Member",
                "title": "Real estate agents and brokers"
            },
            {
                "name": "Office",
                "kind": "EntitySet", 
                "url": "Office",
                "title": "Real estate offices and brokerages"
            }
        ]
    }
    ```

### Metadata Document

The metadata document provides the complete schema definition with entity types, properties, and relationships:

```python
metadata_xml = client.get_metadata()

# Save for inspection (useful for development)
with open('wfrmls_schema.xml', 'w') as f:
    f.write(metadata_xml)
```

!!! tip "Schema Exploration"
    The metadata document is essential for understanding:
    
    - Available entity properties and their data types
    - Required vs. optional fields  
    - Relationships between entities
    - Enumeration values and constraints

## Service Clients

Each service client provides specialized access to different parts of the WFRMLS API:

<div class="grid cards" markdown>

-   :material-home-city:{ .lg .middle } **property**
    
    ---
    
    Property listings, search, and analysis
    
    ```python
    properties = client.property.get_active_properties()
    ```

-   :material-account:{ .lg .middle } **member**
    
    ---
    
    Real estate agents and brokers
    
    ```python
    agents = client.member.get_active_members()
    ```

-   :material-office-building:{ .lg .middle } **office**
    
    ---
    
    Real estate offices and brokerages
    
    ```python
    offices = client.office.get_active_offices()
    ```

-   :material-calendar:{ .lg .middle } **openhouse**
    
    ---
    
    Open house schedules and events
    
    ```python
    opens = client.openhouse.get_upcoming_open_houses()
    ```

-   :material-database:{ .lg .middle } **data_system**
    
    ---
    
    System metadata and information
    
    ```python
    system_info = client.data_system.get_system_info()
    ```

-   :material-api:{ .lg .middle } **resource**
    
    ---
    
    API resource definitions and metadata
    
    ```python
    resources = client.resource.get_resources()
    ```

-   :material-magnify:{ .lg .middle } **lookup**
    
    ---
    
    Reference data and lookup tables
    
    ```python
    lookups = client.lookup.get_lookup_names()
    ```

-   :material-home-plus:{ .lg .middle } **adu**
    
    ---
    
    Accessory Dwelling Unit data
    
    ```python
    adus = client.adu.get_existing_adus()
    ```

-   :material-format-list-bulleted-type:{ .lg .middle } **property_unit_types**
    
    ---
    
    Property unit classifications
    
    ```python
    unit_types = client.property_unit_types.get_residential_unit_types()
    ```

-   :material-delete:{ .lg .middle } **deleted**
    
    ---
    
    Deleted record tracking
    
    ```python
    deleted = client.deleted.get_recent_deletions()
    ```

</div>

## Best Practices

### Initialization

=== "Environment Variable (Recommended)"
    ```python
    import os
    
    # Set token in environment
    os.environ['WFRMLS_BEARER_TOKEN'] = "your_token_here"
    
    # Initialize client
    client = WFRMLSClient()
    ```

=== "Direct Token"
    ```python
    # For testing or scripts
    client = WFRMLSClient(bearer_token="your_token_here")
    ```

=== "Custom Base URL"
    ```python
    # For testing against different environments
    client = WFRMLSClient(
        bearer_token="your_token",
        base_url="https://test-api.wfrmls.com/RETS/api"
    )
    ```

### Resource Discovery

```python
# Check what's available before building queries
service_doc = client.get_service_document()
available_resources = [r['name'] for r in service_doc.get('value', [])]

if 'Property' in available_resources:
    properties = client.property.get_active_properties(top=10)
    
if 'OpenHouse' in available_resources:
    open_houses = client.openhouse.get_upcoming_open_houses()
```

### Error Handling

```python
from wfrmls.exceptions import AuthenticationError, WFRMLSError

try:
    # Initialize client
    client = WFRMLSClient()
    
    # Test connection
    service_doc = client.get_service_document()
    print(f"✅ Connected! Found {len(service_doc.get('value', []))} resources")
    
except AuthenticationError:
    print("❌ Authentication failed - check your bearer token")
except WFRMLSError as e:
    print(f"🚨 API error: {e}")
```

## Client Lifecycle

The `WFRMLSClient` uses lazy initialization for optimal performance:

1. **Initialization**: Only stores configuration, no API calls made
2. **First Access**: Service clients are created when first accessed
3. **Reuse**: Service clients are cached for subsequent calls
4. **Thread Safety**: Each thread should use its own client instance

```python
# Client creation is lightweight
client = WFRMLSClient()  # No API calls yet

# First access creates the service client  
properties = client.property.get_properties()  # PropertyClient created

# Subsequent calls reuse the same client instance
more_properties = client.property.get_active_properties()  # Reuses PropertyClient
``` 