# Resource API

Complete reference for the Resource endpoint of the WFRMLS Python client.

---

## 🗂️ Overview

The Resource API provides metadata about available resources (endpoints) in the WFRMLS system. This endpoint helps developers discover what data is available and understand the structure of the API.

### Key Features

- **Resource discovery** - List all available API endpoints
- **Metadata access** - Get information about each resource
- **API structure** - Understand the organization of data
- **Version information** - Access timestamp and path details
- **Service exploration** - Discover available data types

---

## 📚 Methods

### `get_resources()`

Retrieve all available resources in the WFRMLS system.

```python
def get_resources() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - List of all available resources

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get all available resources
resources = client.resource.get_resources()

# List resource names
for resource in resources["value"]:
    name = resource.get("RName")
    path = resource.get("ResourcePath")
    print(f"{name}: {path}")
```

### `get_resource_by_name()`

Get detailed information about a specific resource.

```python
def get_resource_by_name(
    resource_name: str
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|----------|------|-------------|
| `resource_name` | `str` | Name of the resource (e.g., "Property") |

**Returns:**
- `Dict[str, Any]` - Resource details

**Examples:**

```python
# Get details about the Property resource
property_resource = client.resource.get_resource_by_name("Property")

# Get details about the Member resource
member_resource = client.resource.get_resource_by_name("Member")
```

---

## 🏷️ Field Reference

Each resource record contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **RName** | `string` | Resource name | `"Property"` |
| **ResourcePath** | `string` | API endpoint path | `"/Property"` |
| **Description** | `string` | Resource description | `"Property"` |
| **DSName** | `string` | Data system name | `"WEB_API"` |
| **TimeZoneOffset** | `integer` | Timezone offset hours | `-7` |
| **TimestampModified** | `datetime` | Last modified date | `"2021-11-16T00:00:13Z"` |

---

## 📋 Available Resources

Based on the API, the following resources are available:

| Resource | Path | Description |
|----------|------|-------------|
| **Media** | `/Media` | Property photos and media files |
| **Member** | `/Member` | Real estate agents and brokers |
| **Office** | `/Office` | Real estate offices and brokerages |
| **OpenHouse** | `/OpenHouse` | Open house events |
| **Property** | `/Property` | Property listings |

---

## 🔍 Common Usage Patterns

### Dynamic API Exploration

```python
def explore_api_structure():
    """Dynamically explore available API endpoints."""
    
    # Get all resources
    resources = client.resource.get_resources()
    
    api_structure = {
        "base_url": client.base_url,
        "resources": {},
        "total_resources": len(resources["value"])
    }
    
    # Build resource map
    for resource in resources["value"]:
        name = resource.get("RName")
        api_structure["resources"][name] = {
            "path": resource.get("ResourcePath"),
            "description": resource.get("Description"),
            "last_modified": resource.get("TimestampModified")
        }
    
    return api_structure

# Explore API
api_map = explore_api_structure()
print(f"Found {api_map['total_resources']} resources")
```

### Endpoint Validation

```python
def validate_endpoint_exists(endpoint_name: str) -> bool:
    """Check if an endpoint exists in the API."""
    
    resources = client.resource.get_resources()
    
    valid_endpoints = set()
    for resource in resources["value"]:
        name = resource.get("RName", "").lower()
        valid_endpoints.add(name)
    
    return endpoint_name.lower() in valid_endpoints

# Validate endpoints
print(validate_endpoint_exists("Property"))  # True
print(validate_endpoint_exists("InvalidEndpoint"))  # False
```

### API Documentation Generator

```python
def generate_api_docs():
    """Generate documentation for available endpoints."""
    
    resources = client.resource.get_resources()
    
    docs = []
    docs.append("# WFRMLS API Endpoints\n")
    docs.append("## Available Resources\n")
    
    for resource in sorted(resources["value"], key=lambda x: x.get("RName", "")):
        name = resource.get("RName")
        path = resource.get("ResourcePath")
        desc = resource.get("Description")
        modified = resource.get("TimestampModified")
        
        docs.append(f"\n### {name}")
        docs.append(f"- **Endpoint**: `{path}`")
        docs.append(f"- **Description**: {desc}")
        docs.append(f"- **Last Modified**: {modified}")
        docs.append("")
    
    return "\n".join(docs)

# Generate documentation
api_docs = generate_api_docs()
```

### Resource Availability Monitor

```python
from datetime import datetime

def check_resource_updates():
    """Check for updates to API resources."""
    
    current_resources = client.resource.get_resources()
    
    # In a real application, you'd compare with stored data
    updates = {
        "check_time": datetime.now().isoformat(),
        "resources": {}
    }
    
    for resource in current_resources["value"]:
        name = resource.get("RName")
        modified = resource.get("TimestampModified")
        
        updates["resources"][name] = {
            "available": True,
            "last_modified": modified,
            "path": resource.get("ResourcePath")
        }
    
    return updates

# Check for updates
resource_status = check_resource_updates()
```

### API Client Configuration

```python
def configure_client_from_resources():
    """Configure API client based on available resources."""
    
    resources = client.resource.get_resources()
    
    config = {
        "endpoints": {},
        "timezone_offset": None
    }
    
    for resource in resources["value"]:
        name = resource.get("RName")
        path = resource.get("ResourcePath")
        
        # Store endpoint configuration
        config["endpoints"][name.lower()] = {
            "path": path,
            "full_url": f"{client.base_url}{path}"
        }
        
        # Get timezone (should be consistent)
        if config["timezone_offset"] is None:
            config["timezone_offset"] = resource.get("TimeZoneOffset")
    
    return config

# Get client configuration
client_config = configure_client_from_resources()
```

---

## 🔄 Integration with Other Endpoints

### Dynamic Method Builder

```python
def build_dynamic_client():
    """Build client methods based on available resources."""
    
    resources = client.resource.get_resources()
    
    class DynamicClient:
        def __init__(self, base_client):
            self.client = base_client
            self._endpoints = {}
            
            # Build endpoint map
            for resource in resources["value"]:
                name = resource.get("RName", "").lower()
                self._endpoints[name] = resource.get("ResourcePath")
        
        def get_endpoint_data(self, endpoint_name: str, **kwargs):
            """Generic method to get data from any endpoint."""
            
            if endpoint_name.lower() not in self._endpoints:
                raise ValueError(f"Unknown endpoint: {endpoint_name}")
            
            # Use the appropriate client method
            if hasattr(self.client, endpoint_name.lower()):
                endpoint_client = getattr(self.client, endpoint_name.lower())
                if hasattr(endpoint_client, f"get_{endpoint_name.lower()}s"):
                    method = getattr(endpoint_client, f"get_{endpoint_name.lower()}s")
                    return method(**kwargs)
            
            return None
    
    return DynamicClient(client)

# Create dynamic client
dynamic = build_dynamic_client()
```

---

## ⚡ Performance Tips

1. **Cache resource list** - Resources rarely change, cache for session
2. **Validate once** - Check available endpoints at startup
3. **Build endpoint maps** - Create lookup dictionaries for fast access
4. **Monitor changes** - Periodically check for API updates
5. **Handle missing resources** - Gracefully handle unavailable endpoints

---

## 🚨 Important Notes

- Resources represent available API endpoints
- Not all resources may be accessible based on permissions
- Resource availability may vary by MLS
- The Resource endpoint itself is not typically listed
- Always handle cases where resources may be unavailable