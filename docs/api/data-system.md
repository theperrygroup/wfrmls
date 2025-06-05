# Data System API

Complete reference for the Data System endpoint of the WFRMLS Python client.

---

## 🖥️ Overview

The Data System API provides metadata about the WFRMLS API service itself, including version information, service URIs, and data dictionary details. This endpoint is useful for understanding the API's capabilities and configuration.

### Key Features

- **Service information** - Get API service details
- **Version tracking** - Access API and data dictionary versions
- **Configuration data** - Retrieve service URIs and settings
- **System metadata** - Understand the API implementation
- **Compatibility checking** - Verify API version support

---

## 📚 Methods

### `get_data_systems()`

Retrieve information about all data systems.

```python
def get_data_systems() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - Data system information

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get data system information
systems = client.data_system.get_data_systems()

# Display system info
for system in systems["value"]:
    print(f"System: {system['DSName']}")
    print(f"Service URI: {system['ServiceUri']}")
    print(f"Data Dictionary Version: {system['DataDictionaryVersion']}")
```

### `get_system_info()`

Get information about the current data system.

```python
def get_system_info() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - Current system information

**Examples:**

```python
# Get current system info
info = client.data_system.get_system_info()

# Access version information
transport_version = info["value"][0]["TransportVersion"]
dd_version = info["value"][0]["DataDictionaryVersion"]

print(f"Transport Version: {transport_version}")
print(f"Data Dictionary Version: {dd_version}")
```

### `get_service_info()`

Get detailed service information.

```python
def get_service_info() -> Dict[str, Any]
```

**Returns:**
- `Dict[str, Any]` - Service configuration details

---

## 🏷️ Field Reference

Each data system record contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **DSName** | `string` | Data system name | `"WEB_API"` |
| **ServiceUri** | `string` | Base service URI | `"https://resoapi.utahrealestate.com/reso/odata"` |
| **TransportVersion** | `string` | API transport version | `"1.02"` |
| **DataDictionaryVersion** | `string` | RESO data dictionary version | `"1.7"` |
| **TimestampModified** | `datetime` | Last modification date | `"2021-11-16T00:00:13Z"` |

---

## 🔍 Common Usage Patterns

### Version Compatibility Check

```python
def check_api_compatibility(required_version: str = "1.7"):
    """Check if API data dictionary version meets requirements."""
    
    system_info = client.data_system.get_system_info()
    
    if system_info["value"]:
        current_version = system_info["value"][0]["DataDictionaryVersion"]
        
        # Simple version comparison (in practice, use proper version parsing)
        is_compatible = current_version >= required_version
        
        return {
            "compatible": is_compatible,
            "current_version": current_version,
            "required_version": required_version,
            "message": "Compatible" if is_compatible else "Update required"
        }
    
    return {
        "compatible": False,
        "message": "Unable to retrieve version information"
    }

# Check compatibility
compatibility = check_api_compatibility()
print(f"API Compatible: {compatibility['compatible']}")
```

### Service Health Check

```python
from datetime import datetime, timedelta

def check_service_health():
    """Perform a health check on the API service."""
    
    health_status = {
        "status": "unknown",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    try:
        # Check data system endpoint
        system_info = client.data_system.get_data_systems()
        
        if system_info.get("value"):
            health_status["checks"]["data_system"] = "ok"
            
            # Check modification date
            modified = system_info["value"][0].get("TimestampModified")
            if modified:
                mod_date = datetime.fromisoformat(modified.replace("Z", "+00:00"))
                age_days = (datetime.now(mod_date.tzinfo) - mod_date).days
                
                health_status["checks"]["last_update"] = f"{age_days} days ago"
            
            # Check service URI accessibility
            service_uri = system_info["value"][0].get("ServiceUri")
            if service_uri:
                health_status["checks"]["service_uri"] = service_uri
                health_status["status"] = "healthy"
            else:
                health_status["status"] = "degraded"
        else:
            health_status["status"] = "unhealthy"
            health_status["checks"]["data_system"] = "no data"
            
    except Exception as e:
        health_status["status"] = "error"
        health_status["error"] = str(e)
    
    return health_status

# Perform health check
health = check_service_health()
print(f"Service Status: {health['status']}")
```

### API Configuration Manager

```python
class APIConfigManager:
    """Manage API configuration based on data system info."""
    
    def __init__(self, client):
        self.client = client
        self._config = None
        self._loaded_at = None
        self.cache_duration = 3600  # 1 hour
    
    def get_config(self, force_refresh=False):
        """Get API configuration with caching."""
        
        # Check cache
        if not force_refresh and self._config:
            if time.time() - self._loaded_at < self.cache_duration:
                return self._config
        
        # Load fresh configuration
        system_info = self.client.data_system.get_system_info()
        
        if system_info.get("value"):
            data = system_info["value"][0]
            
            self._config = {
                "service_uri": data.get("ServiceUri"),
                "base_url": data.get("ServiceUri", "").replace("/odata", ""),
                "transport_version": data.get("TransportVersion"),
                "data_dictionary_version": data.get("DataDictionaryVersion"),
                "system_name": data.get("DSName"),
                "last_modified": data.get("TimestampModified"),
                "loaded_at": datetime.now().isoformat()
            }
            
            self._loaded_at = time.time()
        
        return self._config
    
    def get_version_info(self):
        """Get version information only."""
        
        config = self.get_config()
        
        return {
            "transport": config.get("transport_version"),
            "data_dictionary": config.get("data_dictionary_version")
        }

# Use configuration manager
config_manager = APIConfigManager(client)
config = config_manager.get_config()
versions = config_manager.get_version_info()
```

### Service Documentation Generator

```python
def generate_service_documentation():
    """Generate documentation about the API service."""
    
    system_info = client.data_system.get_system_info()
    
    if not system_info.get("value"):
        return "Unable to retrieve system information"
    
    data = system_info["value"][0]
    
    docs = []
    docs.append("# WFRMLS API Service Information\n")
    docs.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    docs.append("## Service Details\n")
    docs.append(f"- **System Name**: {data.get('DSName')}")
    docs.append(f"- **Service URI**: `{data.get('ServiceUri')}`")
    docs.append(f"- **Last Modified**: {data.get('TimestampModified')}\n")
    
    docs.append("## Version Information\n")
    docs.append(f"- **Transport Version**: {data.get('TransportVersion')}")
    docs.append(f"- **Data Dictionary Version**: {data.get('DataDictionaryVersion')}")
    docs.append(f"  - RESO Standard Version: {data.get('DataDictionaryVersion')}\n")
    
    docs.append("## API Endpoints\n")
    docs.append(f"Base URL: `{data.get('ServiceUri')}`\n")
    
    docs.append("### Available Resources")
    docs.append("- Property")
    docs.append("- Member")
    docs.append("- Office")
    docs.append("- OpenHouse")
    docs.append("- Media\n")
    
    docs.append("## OData Support\n")
    docs.append("This API supports OData v4 query syntax including:")
    docs.append("- `$filter` - Filter results")
    docs.append("- `$select` - Choose fields")
    docs.append("- `$orderby` - Sort results")
    docs.append("- `$top` / `$skip` - Pagination")
    docs.append("- `$count` - Get total count")
    
    return "\n".join(docs)

# Generate documentation
service_docs = generate_service_documentation()
print(service_docs)
```

### Multi-Environment Support

```python
class EnvironmentManager:
    """Manage multiple API environments."""
    
    def __init__(self):
        self.environments = {}
        self.current_env = None
    
    def add_environment(self, name: str, client: WFRMLSClient):
        """Add an environment configuration."""
        
        system_info = client.data_system.get_system_info()
        
        if system_info.get("value"):
            data = system_info["value"][0]
            
            self.environments[name] = {
                "client": client,
                "service_uri": data.get("ServiceUri"),
                "version": data.get("DataDictionaryVersion"),
                "transport": data.get("TransportVersion"),
                "system": data.get("DSName")
            }
            
            if not self.current_env:
                self.current_env = name
    
    def switch_environment(self, name: str):
        """Switch to a different environment."""
        
        if name in self.environments:
            self.current_env = name
            return self.environments[name]["client"]
        
        raise ValueError(f"Unknown environment: {name}")
    
    def get_environment_info(self, name: str = None):
        """Get information about an environment."""
        
        env_name = name or self.current_env
        
        if env_name in self.environments:
            return self.environments[env_name]
        
        return None
    
    def compare_environments(self):
        """Compare all environments."""
        
        comparison = {}
        
        for name, env in self.environments.items():
            comparison[name] = {
                "service_uri": env["service_uri"],
                "version": env["version"],
                "transport": env["transport"]
            }
        
        return comparison

# Example usage
env_manager = EnvironmentManager()
env_manager.add_environment("production", client)
# env_manager.add_environment("staging", staging_client)

# Compare environments
comparison = env_manager.compare_environments()
```

---

## ⚡ Performance Tips

1. **Cache system info** - Data system info rarely changes
2. **Version check once** - Check compatibility at startup
3. **Monitor changes** - Periodically check for updates
4. **Store configuration** - Save service URIs for reuse
5. **Handle timeouts** - System endpoint may be slow

---

## 🚨 Important Notes

- Data system information is primarily for API metadata
- Version numbers follow RESO standards
- Service URI should match the configured base URL
- Transport version indicates OData protocol version
- System information is read-only