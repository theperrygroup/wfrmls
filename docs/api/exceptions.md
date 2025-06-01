# Exceptions API

The Exceptions module provides a comprehensive set of exception classes for handling errors in the WFRMLS Python client. These exceptions help you identify and handle different types of errors that may occur during API interactions.

## Overview

All WFRMLS exceptions inherit from the base `WFRMLSError` class, providing a consistent error handling interface across the entire library.

```python
from wfrmls.exceptions import WFRMLSError, NotFoundError, RateLimitError

try:
    properties = client.property.get_properties()
except NotFoundError:
    print("Resource not found")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after}")
except WFRMLSError as e:
    print(f"API error: {e}")
```

## Exception Hierarchy

```
WFRMLSError (Base Exception)
├── AuthenticationError
├── ValidationError
├── NotFoundError
├── RateLimitError
├── ServerError
└── NetworkError
```

## Exception Classes

### WFRMLSError

Base exception class for all WFRMLS-related errors.

```python
class WFRMLSError(Exception):
    """Base exception for WFRMLS API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Error message |
| `status_code` | `int` | HTTP status code (if applicable) |
| `response` | `dict` | Full API response (if available) |

#### Example

```python
try:
    data = client.property.get_property("invalid_id")
except WFRMLSError as e:
    print(f"Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    if e.response:
        print(f"Response: {e.response}")
```

### AuthenticationError

Raised when authentication fails or credentials are invalid.

```python
class AuthenticationError(WFRMLSError):
    """Raised when authentication fails."""
    pass
```

#### Common Causes

- Invalid bearer token
- Expired credentials
- Insufficient permissions
- Missing authentication headers

#### Example

```python
try:
    client = WFRMLSClient(bearer_token="invalid_token")
    properties = client.property.get_properties()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Handle re-authentication or credential refresh
```

### ValidationError

Raised when request parameters are invalid or malformed.

```python
class ValidationError(WFRMLSError):
    """Raised when request validation fails."""
    
    def __init__(
        self,
        message: str,
        field_errors: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ):
        self.field_errors = field_errors or {}
        super().__init__(message, **kwargs)
```

#### Additional Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `field_errors` | `dict` | Field-specific validation errors |

#### Example

```python
try:
    properties = client.property.get_properties(
        filter_query="InvalidField eq 'value'"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
    if e.field_errors:
        for field, errors in e.field_errors.items():
            print(f"  {field}: {', '.join(errors)}")
```

### NotFoundError

Raised when a requested resource is not found.

```python
class NotFoundError(WFRMLSError):
    """Raised when a resource is not found."""
    pass
```

#### Common Causes

- Invalid resource ID
- Resource has been deleted
- Insufficient permissions to view resource
- Resource not in current user's scope

#### Example

```python
try:
    property_data = client.property.get_property("nonexistent_id")
except NotFoundError:
    print("Property not found")
    # Handle missing resource gracefully
```

### RateLimitError

Raised when API rate limits are exceeded.

```python
class RateLimitError(WFRMLSError):
    """Raised when rate limits are exceeded."""
    
    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        **kwargs
    ):
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        super().__init__(message, **kwargs)
```

#### Additional Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `retry_after` | `int` | Seconds to wait before retrying |
| `limit` | `int` | Rate limit threshold |
| `remaining` | `int` | Remaining requests in current window |

#### Example

```python
import time

try:
    properties = client.property.get_properties()
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    if e.retry_after:
        print(f"Retrying after {e.retry_after} seconds")
        time.sleep(e.retry_after)
        # Retry the request
```

### ServerError

Raised when the server encounters an internal error.

```python
class ServerError(WFRMLSError):
    """Raised when the server encounters an error."""
    pass
```

#### Common Causes

- Internal server error (500)
- Service temporarily unavailable (503)
- Database connection issues
- Maintenance mode

#### Example

```python
try:
    properties = client.property.get_properties()
except ServerError as e:
    print(f"Server error: {e}")
    # Implement retry logic or fallback behavior
```

### NetworkError

Raised when network-related issues occur.

```python
class NetworkError(WFRMLSError):
    """Raised when network errors occur."""
    pass
```

#### Common Causes

- Connection timeout
- DNS resolution failure
- Network connectivity issues
- SSL/TLS errors

#### Example

```python
try:
    properties = client.property.get_properties()
except NetworkError as e:
    print(f"Network error: {e}")
    # Check network connectivity or retry with backoff
```

## Error Handling Patterns

### Basic Error Handling

```python
from wfrmls.exceptions import WFRMLSError

def safe_api_call():
    try:
        return client.property.get_properties(top=10)
    except WFRMLSError as e:
        print(f"API error occurred: {e}")
        return []
```

### Specific Exception Handling

```python
from wfrmls.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError
)

def robust_api_call():
    try:
        return client.property.get_property("12345")
    
    except AuthenticationError:
        # Handle authentication issues
        print("Authentication failed - check credentials")
        refresh_credentials()
        return None
    
    except ValidationError as e:
        # Handle validation errors
        print(f"Invalid request: {e}")
        if e.field_errors:
            for field, errors in e.field_errors.items():
                print(f"  {field}: {', '.join(errors)}")
        return None
    
    except NotFoundError:
        # Handle missing resources
        print("Property not found")
        return None
    
    except RateLimitError as e:
        # Handle rate limiting
        print(f"Rate limited - retry after {e.retry_after} seconds")
        if e.retry_after:
            time.sleep(e.retry_after)
            return robust_api_call()  # Retry
        return None
    
    except ServerError:
        # Handle server errors
        print("Server error - try again later")
        return None
    
    except NetworkError:
        # Handle network issues
        print("Network error - check connectivity")
        return None
```

### Retry Logic with Exponential Backoff

```python
import time
import random
from typing import Optional, Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0
) -> Optional[Any]:
    """Retry function with exponential backoff."""
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        
        except RateLimitError as e:
            if e.retry_after:
                time.sleep(e.retry_after)
            else:
                delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                jitter = random.uniform(0, 0.1) * delay
                time.sleep(delay + jitter)
        
        except (ServerError, NetworkError) as e:
            if attempt == max_retries:
                raise e
            
            delay = min(base_delay * (backoff_factor ** attempt), max_delay)
            jitter = random.uniform(0, 0.1) * delay
            time.sleep(delay + jitter)
        
        except (AuthenticationError, ValidationError, NotFoundError):
            # Don't retry for these errors
            raise
    
    raise Exception(f"Max retries ({max_retries}) exceeded")

# Usage
def get_property_with_retry(property_id: str):
    return retry_with_backoff(
        lambda: client.property.get_property(property_id),
        max_retries=3
    )
```

### Logging and Monitoring

```python
import logging
from wfrmls.exceptions import WFRMLSError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitored_api_call():
    try:
        result = client.property.get_properties()
        logger.info(f"Successfully retrieved {len(result)} properties")
        return result
    
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        # Send alert to monitoring system
        send_alert("authentication_failure", str(e))
        raise
    
    except RateLimitError as e:
        logger.warning(f"Rate limit exceeded: {e}")
        # Track rate limit metrics
        track_metric("rate_limit_hit", {
            "retry_after": e.retry_after,
            "remaining": e.remaining
        })
        raise
    
    except ServerError as e:
        logger.error(f"Server error: {e}")
        # Send alert for server issues
        send_alert("server_error", str(e))
        raise
    
    except WFRMLSError as e:
        logger.error(f"Unexpected API error: {e}")
        # Track unexpected errors
        track_metric("unexpected_error", {
            "error_type": type(e).__name__,
            "status_code": e.status_code
        })
        raise

def send_alert(alert_type: str, message: str):
    """Send alert to monitoring system."""
    # Implement your alerting logic
    pass

def track_metric(metric_name: str, data: dict):
    """Track metrics for monitoring."""
    # Implement your metrics tracking
    pass
```

### Context Manager for Error Handling

```python
from contextlib import contextmanager
from wfrmls.exceptions import WFRMLSError

@contextmanager
def handle_api_errors(operation_name: str):
    """Context manager for consistent error handling."""
    try:
        yield
    except AuthenticationError as e:
        logger.error(f"Authentication failed during {operation_name}: {e}")
        raise
    except ValidationError as e:
        logger.error(f"Validation error during {operation_name}: {e}")
        raise
    except NotFoundError as e:
        logger.warning(f"Resource not found during {operation_name}: {e}")
        raise
    except RateLimitError as e:
        logger.warning(f"Rate limited during {operation_name}: {e}")
        raise
    except ServerError as e:
        logger.error(f"Server error during {operation_name}: {e}")
        raise
    except NetworkError as e:
        logger.error(f"Network error during {operation_name}: {e}")
        raise
    except WFRMLSError as e:
        logger.error(f"Unexpected error during {operation_name}: {e}")
        raise

# Usage
with handle_api_errors("property_search"):
    properties = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'"
    )
```

## Best Practices

### Error Handling Strategy

1. **Catch specific exceptions** rather than generic ones
2. **Log errors appropriately** for debugging and monitoring
3. **Implement retry logic** for transient errors
4. **Provide meaningful error messages** to users
5. **Monitor error rates** and patterns

### Retry Guidelines

1. **Retry rate limit errors** after the specified delay
2. **Retry server/network errors** with exponential backoff
3. **Don't retry authentication/validation errors**
4. **Limit maximum retry attempts** to prevent infinite loops
5. **Add jitter** to prevent thundering herd problems

### Monitoring and Alerting

1. **Track error rates** by exception type
2. **Alert on authentication failures** (potential security issue)
3. **Monitor rate limit usage** to optimize request patterns
4. **Set up dashboards** for error trends
5. **Implement circuit breakers** for cascading failures

## Testing Exception Handling

```python
import pytest
from unittest.mock import Mock, patch
from wfrmls.exceptions import NotFoundError, RateLimitError

def test_not_found_handling():
    """Test handling of NotFoundError."""
    with patch.object(client.property, 'get_property') as mock_get:
        mock_get.side_effect = NotFoundError("Property not found")
        
        result = safe_get_property("invalid_id")
        assert result is None

def test_rate_limit_handling():
    """Test handling of RateLimitError."""
    with patch.object(client.property, 'get_properties') as mock_get:
        mock_get.side_effect = RateLimitError(
            "Rate limit exceeded",
            retry_after=60
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            client.property.get_properties()
        
        assert exc_info.value.retry_after == 60

def safe_get_property(property_id: str):
    """Safe property getter for testing."""
    try:
        return client.property.get_property(property_id)
    except NotFoundError:
        return None
```

## Related Resources

- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling strategies
- [Rate Limits Guide](../guides/rate-limits.md) - Understanding and handling rate limits
- [Client API](client.md) - Main client configuration and usage