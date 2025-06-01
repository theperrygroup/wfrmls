# Client API

Complete reference for the WFRMLSClient class and client initialization options.

---

## 🔧 Overview

The `WFRMLSClient` is the main entry point for interacting with the WFRMLS API. It provides access to all endpoints and handles authentication, request formatting, and response processing.

### Key Features

- **Automatic authentication** - Handles bearer token authentication
- **Endpoint access** - Provides access to all WFRMLS API endpoints
- **Error handling** - Converts API errors to appropriate Python exceptions
- **Request optimization** - Efficient HTTP connection management
- **Response parsing** - Automatic JSON parsing and data extraction

---

## 🏗️ Client Initialization

### `WFRMLSClient`

Main client class for accessing the WFRMLS API.

```python
class WFRMLSClient:
    def __init__(
        self,
        bearer_token: Optional[str] = None,
        base_url: str = "https://api.wfrmls.com/reso/odata",
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        user_agent: Optional[str] = None,
        verify_ssl: bool = True
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bearer_token` | `Optional[str]` | `None` | API bearer token. If None, reads from `WFRMLS_BEARER_TOKEN` environment variable |
| `base_url` | `str` | `"https://api.wfrmls.com/reso/odata"` | Base URL for the WFRMLS API |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum number of retry attempts for failed requests |
| `retry_delay` | `float` | `1.0` | Delay between retry attempts in seconds |
| `user_agent` | `Optional[str]` | `None` | Custom User-Agent header. Defaults to library version |
| `verify_ssl` | `bool` | `True` | Whether to verify SSL certificates |

**Raises:**
- `ValueError` - If bearer token is not provided and not found in environment
- `AuthenticationError` - If bearer token is invalid or expired

**Examples:**

```python
from wfrmls import WFRMLSClient
import os

# Basic initialization (uses environment variable)
client = WFRMLSClient()

# Explicit token initialization
client = WFRMLSClient(bearer_token="your_bearer_token_here")

# Custom configuration
client = WFRMLSClient(
    bearer_token=os.getenv('WFRMLS_BEARER_TOKEN'),
    timeout=60.0,
    max_retries=5,
    retry_delay=2.0
)

# Development/testing configuration
client = WFRMLSClient(
    bearer_token="test_token",
    base_url="https://api-staging.wfrmls.com/reso/odata",
    verify_ssl=False  # Only for development
)
```

---

## 🌐 Endpoint Access

The client provides access to all WFRMLS API endpoints through dedicated attributes:

### Available Endpoints

| Endpoint | Attribute | Description |
|----------|-----------|-------------|
| **Properties** | `client.property` | Property listings and details |
| **Members** | `client.member` | Real estate agent information |
| **Offices** | `client.office` | Brokerage and office data |
| **Open Houses** | `client.openhouse` | Open house schedules |
| **Lookup** | `client.lookup` | Reference data and lookup tables |
| **ADU** | `client.adu` | Accessory dwelling unit information |
| **Analytics** | `client.analytics` | Market insights and analytics |
| **Deleted** | `client.deleted` | Deleted record tracking |
| **Data System** | `client.data_system` | System metadata |

### Basic Usage

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Access different endpoints
properties = client.property.get_properties(top=10)
agents = client.member.get_members(top=5)
offices = client.office.get_offices()
open_houses = client.openhouse.get_open_houses()

# All endpoints follow similar patterns
for prop in properties:
    print(f"Property: {prop['ListingId']} - ${prop['ListPrice']:,}")

for agent in agents:
    print(f"Agent: {agent['MemberFullName']}")
```

---

## ⚙️ Configuration Options

### Authentication Configuration

```python
import os
from wfrmls import WFRMLSClient

# Method 1: Environment variable (recommended)
os.environ['WFRMLS_BEARER_TOKEN'] = 'your_token_here'
client = WFRMLSClient()

# Method 2: Direct token passing
client = WFRMLSClient(bearer_token='your_token_here')

# Method 3: Configuration from file or service
def get_token_from_config():
    # Your token retrieval logic here
    return 'your_token_here'

client = WFRMLSClient(bearer_token=get_token_from_config())
```

### Network Configuration

```python
# Custom timeout settings
client = WFRMLSClient(
    timeout=60.0,  # 60 second timeout
    max_retries=5,  # Retry up to 5 times
    retry_delay=2.0  # Wait 2 seconds between retries
)

# Custom User-Agent
client = WFRMLSClient(
    user_agent="MyApp/1.0 (contact@example.com)"
)

# SSL configuration (for development/testing)
client = WFRMLSClient(
    verify_ssl=False  # Not recommended for production
)
```

### Base URL Configuration

```python
# Production (default)
prod_client = WFRMLSClient()

# Custom/staging environment
staging_client = WFRMLSClient(
    base_url="https://api-staging.wfrmls.com/reso/odata"
)

# Local development
dev_client = WFRMLSClient(
    base_url="http://localhost:8080/reso/odata",
    verify_ssl=False
)
```

---

## 🔄 Connection Management

### HTTP Session Management

The client automatically manages HTTP connections for optimal performance:

```python
from wfrmls import WFRMLSClient

# Client maintains persistent connections
client = WFRMLSClient()

# Multiple requests reuse the same connection
properties_page1 = client.property.get_properties(top=50, skip=0)
properties_page2 = client.property.get_properties(top=50, skip=50)
properties_page3 = client.property.get_properties(top=50, skip=100)

# Connection is automatically closed when client is destroyed
# or you can explicitly close it
client.close()
```

### Connection Pooling

```python
# For high-throughput applications, configure connection pooling
import requests.adapters

class HighPerformanceClient(WFRMLSClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure adapter for connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

# Usage
high_perf_client = HighPerformanceClient()
```

---

## 🚨 Error Handling

### Exception Hierarchy

The client converts HTTP errors into specific Python exceptions:

```python
from wfrmls.exceptions import (
    WFRMLSError,           # Base exception
    AuthenticationError,    # 401, 403 errors
    NotFoundError,         # 404 errors
    ValidationError,       # 400 errors
    RateLimitError,        # 429 errors
    ServerError,           # 5xx errors
    NetworkError,          # Connection issues
    TimeoutError          # Request timeouts
)

client = WFRMLSClient()

try:
    properties = client.property.get_properties()
    
except AuthenticationError:
    print("Invalid API credentials")
    
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
    
except ValidationError as e:
    print(f"Invalid request: {e}")
    
except ServerError:
    print("Server error - try again later")
    
except NetworkError:
    print("Network connection issue")
    
except TimeoutError:
    print("Request timed out")
    
except WFRMLSError as e:
    print(f"API error: {e}")
```

### Retry Configuration

```python
# Configure automatic retries
client = WFRMLSClient(
    max_retries=3,      # Retry up to 3 times
    retry_delay=1.0     # Wait 1 second between retries
)

# Custom retry logic
import time
from wfrmls.exceptions import RateLimitError, ServerError

def robust_request(func, *args, **kwargs):
    """Make request with custom retry logic."""
    
    max_attempts = 5
    
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
            
        except RateLimitError as e:
            if attempt < max_attempts - 1:
                wait_time = getattr(e, 'retry_after', 60)
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
                
        except ServerError:
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Server error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise

# Usage
properties = robust_request(
    client.property.get_properties,
    filter_query="StandardStatus eq 'Active'",
    top=100
)
```

---

## 🔍 Request Debugging

### Logging Configuration

```python
import logging
from wfrmls import WFRMLSClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wfrmls')

client = WFRMLSClient()

# Requests will now be logged
properties = client.property.get_properties(top=5)
```

### Request Inspection

```python
# Custom client with request inspection
class DebuggingClient(WFRMLSClient):
    def _make_request(self, method, endpoint, **kwargs):
        """Override to add request inspection."""
        
        print(f"Making {method} request to: {endpoint}")
        print(f"Parameters: {kwargs}")
        
        response = super()._make_request(method, endpoint, **kwargs)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        return response

# Usage
debug_client = DebuggingClient()
properties = debug_client.property.get_properties(top=3)
```

### Response Analysis

```python
import json

def analyze_response(client, endpoint_func, *args, **kwargs):
    """Analyze API response structure."""
    
    try:
        data = endpoint_func(*args, **kwargs)
        
        print(f"Response type: {type(data)}")
        print(f"Number of records: {len(data) if isinstance(data, list) else 1}")
        
        if isinstance(data, list) and data:
            sample = data[0]
            print(f"Sample record keys: {list(sample.keys())}")
            print(f"Sample record: {json.dumps(sample, indent=2)[:500]}...")
        elif isinstance(data, dict):
            print(f"Record keys: {list(data.keys())}")
            
    except Exception as e:
        print(f"Error analyzing response: {e}")

# Usage
client = WFRMLSClient()

analyze_response(
    client, 
    client.property.get_properties,
    filter_query="StandardStatus eq 'Active'",
    top=1
)
```

---

## 🏭 Production Patterns

### Client Factory

```python
import os
from typing import Optional
from wfrmls import WFRMLSClient

class WFRMLSClientFactory:
    """Factory for creating configured WFRMLS clients."""
    
    @staticmethod
    def create_client(
        environment: str = "production",
        bearer_token: Optional[str] = None,
        **kwargs
    ) -> WFRMLSClient:
        """Create client for specific environment."""
        
        config = {
            "production": {
                "base_url": "https://api.wfrmls.com/reso/odata",
                "timeout": 30.0,
                "max_retries": 3,
                "verify_ssl": True
            },
            "staging": {
                "base_url": "https://api-staging.wfrmls.com/reso/odata",
                "timeout": 60.0,
                "max_retries": 5,
                "verify_ssl": True
            },
            "development": {
                "base_url": "http://localhost:8080/reso/odata",
                "timeout": 10.0,
                "max_retries": 1,
                "verify_ssl": False
            }
        }
        
        env_config = config.get(environment, config["production"])
        env_config.update(kwargs)
        
        # Get token from environment if not provided
        if not bearer_token:
            token_var = f"WFRMLS_BEARER_TOKEN_{environment.upper()}"
            bearer_token = os.getenv(token_var) or os.getenv("WFRMLS_BEARER_TOKEN")
        
        return WFRMLSClient(bearer_token=bearer_token, **env_config)

# Usage
prod_client = WFRMLSClientFactory.create_client("production")
staging_client = WFRMLSClientFactory.create_client("staging")
dev_client = WFRMLSClientFactory.create_client("development")
```

### Connection Pool Management

```python
from contextlib import contextmanager
from wfrmls import WFRMLSClient

@contextmanager
def wfrmls_client(**kwargs):
    """Context manager for WFRMLS client with proper cleanup."""
    
    client = WFRMLSClient(**kwargs)
    try:
        yield client
    finally:
        client.close()

# Usage
with wfrmls_client() as client:
    properties = client.property.get_properties(top=10)
    agents = client.member.get_members(top=5)
    # Client automatically closed when exiting context
```

### Singleton Pattern

```python
class WFRMLSClientSingleton:
    """Singleton WFRMLS client for application-wide use."""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_client(self, **kwargs) -> WFRMLSClient:
        """Get or create WFRMLS client instance."""
        
        if self._client is None:
            self._client = WFRMLSClient(**kwargs)
        
        return self._client
    
    def close(self):
        """Close client connection."""
        if self._client:
            self._client.close()
            self._client = None

# Usage
singleton = WFRMLSClientSingleton()
client = singleton.get_client()

# Use client throughout application
properties = client.property.get_properties()

# Clean up on application exit
singleton.close()
```

---

## 🔧 Advanced Configuration

### Custom Headers

```python
from wfrmls import WFRMLSClient

class CustomHeaderClient(WFRMLSClient):
    def __init__(self, custom_headers=None, **kwargs):
        super().__init__(**kwargs)
        
        if custom_headers:
            self.session.headers.update(custom_headers)

# Usage
client = CustomHeaderClient(
    custom_headers={
        'X-Application-Name': 'MyRealEstateApp',
        'X-Application-Version': '1.0.0',
        'X-User-ID': 'user123'
    }
)
```

### Request Middleware

```python
from wfrmls import WFRMLSClient
import time

class InstrumentedClient(WFRMLSClient):
    """Client with request instrumentation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_count = 0
        self.total_time = 0.0
    
    def _make_request(self, method, endpoint, **kwargs):
        """Override to add instrumentation."""
        
        start_time = time.time()
        self.request_count += 1
        
        try:
            response = super()._make_request(method, endpoint, **kwargs)
            
            elapsed = time.time() - start_time
            self.total_time += elapsed
            
            print(f"Request #{self.request_count}: {method} {endpoint} "
                  f"({elapsed:.2f}s)")
            
            return response
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.total_time += elapsed
            
            print(f"Request #{self.request_count}: {method} {endpoint} "
                  f"FAILED ({elapsed:.2f}s) - {e}")
            
            raise
    
    def get_stats(self):
        """Get request statistics."""
        avg_time = self.total_time / self.request_count if self.request_count > 0 else 0
        
        return {
            'total_requests': self.request_count,
            'total_time': self.total_time,
            'average_time': avg_time
        }

# Usage
client = InstrumentedClient()

properties = client.property.get_properties(top=10)
agents = client.member.get_members(top=5)

stats = client.get_stats()
print(f"Made {stats['total_requests']} requests in {stats['total_time']:.2f}s")
print(f"Average request time: {stats['average_time']:.2f}s")
```

---

## 📚 Related Documentation

### **Getting Started**
- **[Installation](../getting-started/installation.md)** - Package installation and setup
- **[Authentication](../getting-started/authentication.md)** - API credentials configuration
- **[Quick Start](../getting-started/quickstart.md)** - First steps with the client

### **Guides**
- **[Error Handling](../guides/error-handling.md)** - Comprehensive error handling strategies
- **[Rate Limits](../guides/rate-limits.md)** - Managing API quotas and limits
- **[Property Search](../guides/property-search.md)** - Using the properties endpoint

### **API Endpoints**
- **[Properties API](properties.md)** - Property listings and search
- **[Members API](members.md)** - Real estate agent information
- **[Offices API](offices.md)** - Brokerage and office data
- **[Exceptions API](exceptions.md)** - Error handling reference

### **Examples**
- **[Basic Usage](../examples/basic-usage.md)** - Simple client usage patterns
- **[Advanced Queries](../examples/advanced-queries.md)** - Complex search examples

---

*Ready to start using the client? Check out our [Quick Start Guide](../getting-started/quickstart.md) for step-by-step instructions.* 