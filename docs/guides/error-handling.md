# Error Handling Guide

Build robust applications with comprehensive error handling strategies for the WFRMLS Python client.

---

## 🎯 Overview

Proper error handling is crucial for building reliable real estate applications. This guide covers all aspects of handling errors with the WFRMLS Python client, from basic exception handling to advanced retry strategies.

### What You'll Learn

- **Exception types** - Understanding different error categories
- **Basic error handling** - Simple try/catch patterns
- **Advanced strategies** - Retry logic, circuit breakers, and fallbacks
- **Logging and monitoring** - Tracking errors for debugging
- **Production patterns** - Real-world error handling scenarios

---

## 🚨 Exception Types

### WFRMLS Exception Hierarchy

```python
from wfrmls.exceptions import (
    WFRMLSError,           # Base exception
    AuthenticationError,    # Invalid credentials
    NotFoundError,         # Resource not found
    ValidationError,       # Invalid parameters
    RateLimitError,        # Rate limit exceeded
    ServerError,           # Server-side issues
    NetworkError,          # Connection problems
    TimeoutError          # Request timeout
)
```

### Exception Details

| Exception | HTTP Code | Description | Common Causes |
|-----------|-----------|-------------|---------------|
| **`AuthenticationError`** | 401, 403 | Invalid or expired credentials | Wrong token, expired access |
| **`NotFoundError`** | 404 | Resource doesn't exist | Invalid listing ID, deleted record |
| **`ValidationError`** | 400 | Invalid request parameters | Bad filter syntax, invalid field names |
| **`RateLimitError`** | 429 | API rate limit exceeded | Too many requests per minute/hour |
| **`ServerError`** | 500, 502, 503 | Server-side problems | API maintenance, server overload |
| **`NetworkError`** | - | Connection issues | Internet problems, DNS issues |
| **`TimeoutError`** | - | Request took too long | Slow queries, network latency |

---

## 🔧 Basic Error Handling

### Simple Try/Catch Pattern

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError, AuthenticationError

def get_properties_safely():
    """Get properties with basic error handling."""
    
    try:
        client = WFRMLSClient()
        properties = client.property.get_properties(top=10)
        return properties
        
    except AuthenticationError:
        print("Authentication failed - check your API token")
        return None
        
    except WFRMLSError as e:
        print(f"API error occurred: {e}")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

### Specific Exception Handling

```python
from wfrmls.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

def robust_property_search(listing_id):
    """Search for property with comprehensive error handling."""
    
    try:
        client = WFRMLSClient()
        property_data = client.property.get_property(listing_id)
        return property_data
        
    except AuthenticationError:
        # Handle authentication issues
        print("❌ Authentication failed")
        print("Check your WFRMLS_BEARER_TOKEN environment variable")
        return None
        
    except NotFoundError:
        # Handle missing resources
        print(f"❌ Property {listing_id} not found")
        print("The property may have been deleted or the ID is incorrect")
        return None
        
    except ValidationError as e:
        # Handle invalid parameters
        print(f"❌ Invalid request: {e}")
        print("Check your listing ID format")
        return None
        
    except RateLimitError:
        # Handle rate limiting
        print("❌ Rate limit exceeded")
        print("Wait before making more requests")
        return None
        
    except ServerError as e:
        # Handle server issues
        print(f"❌ Server error: {e}")
        print("The API may be experiencing issues")
        return None
        
    except Exception as e:
        # Handle unexpected errors
        print(f"❌ Unexpected error: {e}")
        return None
```

---

## 🔄 Advanced Error Handling

### Retry with Exponential Backoff

```python
import time
import random
from functools import wraps
from wfrmls.exceptions import RateLimitError, ServerError, NetworkError

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for retrying functions with exponential backoff."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except (RateLimitError, ServerError, NetworkError) as e:
                    if attempt == max_retries - 1:
                        # Last attempt, re-raise the exception
                        raise
                    
                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, 0.1) * delay
                    total_delay = delay + jitter
                    
                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {total_delay:.2f} seconds...")
                    time.sleep(total_delay)
                    
                except Exception:
                    # Don't retry on other exceptions
                    raise
                    
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3)
def get_properties_with_retry():
    """Get properties with automatic retry on transient errors."""
    client = WFRMLSClient()
    return client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        top=50
    )

# Call the function
try:
    properties = get_properties_with_retry()
    print(f"Successfully retrieved {len(properties)} properties")
except Exception as e:
    print(f"Failed after all retries: {e}")
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker for WFRMLS API calls."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: tuple = (ServerError, NetworkError, TimeoutError)
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )
    
    def _on_success(self):
        """Handle successful request."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker()

def safe_api_call():
    """Make API call with circuit breaker protection."""
    
    def api_operation():
        client = WFRMLSClient()
        return client.property.get_properties(top=10)
    
    try:
        return circuit_breaker.call(api_operation)
    except Exception as e:
        print(f"Circuit breaker prevented call or call failed: {e}")
        return None
```

### Graceful Degradation

```python
from typing import Optional, List, Dict, Any

class PropertyService:
    """Property service with graceful degradation."""
    
    def __init__(self):
        self.client = WFRMLSClient()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_properties(
        self,
        use_cache: bool = True,
        fallback_to_cached: bool = True
    ) -> Optional[List[Dict[str, Any]]]:
        """Get properties with graceful degradation."""
        
        # Try cache first if enabled
        if use_cache:
            cached_data = self._get_from_cache('properties')
            if cached_data:
                print("✅ Returning cached data")
                return cached_data
        
        # Try live API
        try:
            properties = self.client.property.get_properties(
                filter_query="StandardStatus eq 'Active'",
                top=50
            )
            
            # Cache successful result
            self._cache_data('properties', properties)
            print("✅ Retrieved fresh data from API")
            return properties
            
        except (RateLimitError, ServerError, NetworkError) as e:
            print(f"⚠️ API call failed: {e}")
            
            # Fallback to cached data if available
            if fallback_to_cached:
                cached_data = self._get_from_cache('properties', ignore_ttl=True)
                if cached_data:
                    print("⚠️ Using stale cached data as fallback")
                    return cached_data
            
            # Fallback to minimal static data
            print("⚠️ Using minimal fallback data")
            return self._get_fallback_data()
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def _get_from_cache(self, key: str, ignore_ttl: bool = False) -> Optional[Any]:
        """Get data from cache if valid."""
        if key not in self.cache:
            return None
        
        data, timestamp = self.cache[key]
        
        if not ignore_ttl:
            if time.time() - timestamp > self.cache_ttl:
                return None
        
        return data
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp."""
        self.cache[key] = (data, time.time())
    
    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        """Return minimal fallback data."""
        return [
            {
                "ListingId": "UNAVAILABLE",
                "ListPrice": 0,
                "City": "Service Temporarily Unavailable",
                "StandardStatus": "Unknown"
            }
        ]

# Usage
service = PropertyService()

properties = service.get_properties()
if properties:
    for prop in properties:
        print(f"{prop['ListingId']}: ${prop.get('ListPrice', 0):,}")
```

---

## 📊 Logging and Monitoring

### Structured Logging

```python
import logging
import json
from datetime import datetime
from wfrmls.exceptions import WFRMLSError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class WFRMLSLogger:
    """Structured logger for WFRMLS operations."""
    
    def __init__(self):
        self.logger = logging.getLogger('wfrmls_client')
    
    def log_api_call(self, method: str, endpoint: str, params: dict = None):
        """Log API call details."""
        log_data = {
            'event': 'api_call_start',
            'method': method,
            'endpoint': endpoint,
            'params': params or {},
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data))
    
    def log_api_success(self, method: str, endpoint: str, result_count: int, duration: float):
        """Log successful API call."""
        log_data = {
            'event': 'api_call_success',
            'method': method,
            'endpoint': endpoint,
            'result_count': result_count,
            'duration_ms': duration * 1000,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data))
    
    def log_api_error(self, method: str, endpoint: str, error: Exception, duration: float):
        """Log API error."""
        log_data = {
            'event': 'api_call_error',
            'method': method,
            'endpoint': endpoint,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'duration_ms': duration * 1000,
            'timestamp': datetime.now().isoformat()
        }
        
        if isinstance(error, WFRMLSError):
            log_data['wfrmls_error'] = True
            if hasattr(error, 'status_code'):
                log_data['http_status'] = error.status_code
        
        self.logger.error(json.dumps(log_data))

# Usage with timing
import time

def logged_property_search(listing_id: str):
    """Property search with comprehensive logging."""
    
    wfrmls_logger = WFRMLSLogger()
    start_time = time.time()
    
    wfrmls_logger.log_api_call(
        method='GET',
        endpoint='/Property',
        params={'listing_id': listing_id}
    )
    
    try:
        client = WFRMLSClient()
        result = client.property.get_property(listing_id)
        
        duration = time.time() - start_time
        wfrmls_logger.log_api_success(
            method='GET',
            endpoint='/Property',
            result_count=1 if result else 0,
            duration=duration
        )
        
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        wfrmls_logger.log_api_error(
            method='GET',
            endpoint='/Property',
            error=e,
            duration=duration
        )
        raise
```

### Error Metrics and Alerting

```python
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading

class ErrorMetrics:
    """Track error metrics for monitoring and alerting."""
    
    def __init__(self, window_minutes: int = 60):
        self.window_minutes = window_minutes
        self.error_counts = defaultdict(int)
        self.error_history = deque()
        self.lock = threading.Lock()
    
    def record_error(self, error_type: str, details: dict = None):
        """Record an error occurrence."""
        with self.lock:
            now = datetime.now()
            
            # Add to history
            self.error_history.append({
                'timestamp': now,
                'error_type': error_type,
                'details': details or {}
            })
            
            # Increment counter
            self.error_counts[error_type] += 1
            
            # Clean old entries
            self._cleanup_old_entries()
    
    def get_error_rate(self, error_type: str = None) -> float:
        """Get error rate per minute."""
        with self.lock:
            self._cleanup_old_entries()
            
            if error_type:
                count = sum(1 for entry in self.error_history 
                           if entry['error_type'] == error_type)
            else:
                count = len(self.error_history)
            
            return count / self.window_minutes
    
    def should_alert(self, error_type: str, threshold_per_minute: float) -> bool:
        """Check if error rate exceeds threshold."""
        return self.get_error_rate(error_type) > threshold_per_minute
    
    def get_error_summary(self) -> dict:
        """Get summary of recent errors."""
        with self.lock:
            self._cleanup_old_entries()
            
            summary = defaultdict(int)
            for entry in self.error_history:
                summary[entry['error_type']] += 1
            
            return dict(summary)
    
    def _cleanup_old_entries(self):
        """Remove entries older than the window."""
        cutoff = datetime.now() - timedelta(minutes=self.window_minutes)
        
        while self.error_history and self.error_history[0]['timestamp'] < cutoff:
            self.error_history.popleft()

# Usage
metrics = ErrorMetrics()

def monitored_api_call():
    """API call with error monitoring."""
    
    try:
        client = WFRMLSClient()
        return client.property.get_properties(top=10)
        
    except RateLimitError as e:
        metrics.record_error('rate_limit', {'message': str(e)})
        
        # Check if we should alert
        if metrics.should_alert('rate_limit', threshold_per_minute=5):
            print("🚨 ALERT: High rate limit error rate!")
            send_alert("Rate limit errors exceeding threshold")
        
        raise
        
    except AuthenticationError as e:
        metrics.record_error('authentication', {'message': str(e)})
        
        # Authentication errors are always critical
        print("🚨 CRITICAL: Authentication failure!")
        send_alert("Authentication error - check API credentials")
        
        raise
        
    except Exception as e:
        metrics.record_error('general', {'type': type(e).__name__, 'message': str(e)})
        raise

def send_alert(message: str):
    """Send alert (implement your alerting mechanism)."""
    print(f"ALERT: {message}")
    # Implement: email, Slack, PagerDuty, etc.
    pass

# Monitor error rates
def print_error_summary():
    """Print current error summary."""
    summary = metrics.get_error_summary()
    print("\n📊 Error Summary (last hour):")
    for error_type, count in summary.items():
        rate = metrics.get_error_rate(error_type)
        print(f"  {error_type}: {count} total ({rate:.2f}/min)")
```

---

## 🎯 Production Patterns

### Centralized Error Handler

```python
import traceback
from functools import wraps
from typing import Callable, Any, Optional

class WFRMLSErrorHandler:
    """Centralized error handling for WFRMLS operations."""
    
    def __init__(self, logger=None, metrics=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metrics = metrics
        self.error_callbacks = {}
    
    def register_callback(self, error_type: type, callback: Callable):
        """Register callback for specific error type."""
        self.error_callbacks[error_type] = callback
    
    def handle_error(
        self,
        error: Exception,
        context: dict = None,
        reraise: bool = True
    ) -> Optional[Any]:
        """Handle error with logging, metrics, and callbacks."""
        
        error_context = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
            'traceback': traceback.format_exc()
        }
        
        # Log error
        if self.logger:
            self.logger.error(f"Error in WFRMLS operation: {error_context}")
        
        # Record metrics
        if self.metrics:
            self.metrics.record_error(type(error).__name__, error_context)
        
        # Execute callback if registered
        callback = self.error_callbacks.get(type(error))
        if callback:
            try:
                return callback(error, error_context)
            except Exception as callback_error:
                self.logger.error(f"Error in callback: {callback_error}")
        
        # Re-raise or return None
        if reraise:
            raise
        return None

# Global error handler instance
error_handler = WFRMLSErrorHandler()

# Register callbacks
def handle_rate_limit(error: RateLimitError, context: dict):
    """Handle rate limit errors."""
    print("⏱️ Rate limit hit - implementing backoff")
    time.sleep(60)  # Wait 1 minute
    return "rate_limited"

def handle_auth_error(error: AuthenticationError, context: dict):
    """Handle authentication errors."""
    print("🔐 Authentication failed - check credentials")
    # Could trigger credential refresh here
    return None

error_handler.register_callback(RateLimitError, handle_rate_limit)
error_handler.register_callback(AuthenticationError, handle_auth_error)

# Decorator for automatic error handling
def with_error_handling(reraise: bool = True):
    """Decorator for automatic error handling."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                return error_handler.handle_error(e, context, reraise)
        return wrapper
    return decorator

# Usage
@with_error_handling()
def get_properties():
    """Get properties with automatic error handling."""
    client = WFRMLSClient()
    return client.property.get_properties(top=10)
```

### Health Check System

```python
from enum import Enum
from datetime import datetime, timedelta

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class WFRMLSHealthChecker:
    """Health checker for WFRMLS API connectivity."""
    
    def __init__(self):
        self.last_check = None
        self.consecutive_failures = 0
        self.status = HealthStatus.HEALTHY
        self.check_interval = timedelta(minutes=5)
    
    def check_health(self, force: bool = False) -> dict:
        """Check WFRMLS API health."""
        
        now = datetime.now()
        
        # Skip if recent check unless forced
        if not force and self.last_check:
            if now - self.last_check < self.check_interval:
                return self._get_status()
        
        self.last_check = now
        
        try:
            # Minimal API call to test connectivity
            client = WFRMLSClient()
            start_time = time.time()
            
            # Test with minimal request
            client.property.get_properties(top=1)
            
            response_time = time.time() - start_time
            
            # Reset failure count on success
            self.consecutive_failures = 0
            
            # Determine status based on response time
            if response_time < 2.0:
                self.status = HealthStatus.HEALTHY
            elif response_time < 5.0:
                self.status = HealthStatus.DEGRADED
            else:
                self.status = HealthStatus.UNHEALTHY
            
            return {
                'status': self.status.value,
                'response_time_seconds': response_time,
                'consecutive_failures': self.consecutive_failures,
                'last_check': now.isoformat(),
                'healthy': self.status == HealthStatus.HEALTHY
            }
            
        except Exception as e:
            self.consecutive_failures += 1
            
            # Set status based on failure count
            if self.consecutive_failures >= 3:
                self.status = HealthStatus.UNHEALTHY
            else:
                self.status = HealthStatus.DEGRADED
            
            return {
                'status': self.status.value,
                'error': str(e),
                'error_type': type(e).__name__,
                'consecutive_failures': self.consecutive_failures,
                'last_check': now.isoformat(),
                'healthy': False
            }
    
    def _get_status(self) -> dict:
        """Get current status without new check."""
        return {
            'status': self.status.value,
            'consecutive_failures': self.consecutive_failures,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'healthy': self.status == HealthStatus.HEALTHY
        }
    
    def is_healthy(self) -> bool:
        """Check if service is healthy."""
        health = self.check_health()
        return health.get('healthy', False)

# Usage
health_checker = WFRMLSHealthChecker()

def safe_operation_with_health_check():
    """Perform operation with health check."""
    
    if not health_checker.is_healthy():
        health_status = health_checker.check_health(force=True)
        print(f"⚠️ Service unhealthy: {health_status}")
        return None
    
    try:
        client = WFRMLSClient()
        return client.property.get_properties(top=10)
        
    except Exception as e:
        # Update health status after error
        health_checker.check_health(force=True)
        raise
```

---

## 📚 Next Steps

### **Related Guides**
- **[Rate Limits Guide](rate-limits.md)** - Managing API quotas and implementing proper throttling
- **[Property Search Guide](property-search.md)** - Error handling in search operations
- **[Data Synchronization Guide](data-sync.md)** - Error recovery in data pipelines

### **Development Resources**
- **[Testing Guide](../development/testing.md)** - Testing error handling scenarios
- **[Contributing Guide](../development/contributing.md)** - Error handling standards for contributors

### **API Reference**
- **[Exceptions API](../api/exceptions.md)** - Complete exception class documentation
- **[Client API](../api/client.md)** - Client configuration options

---

*Ready to implement robust error handling? Start with our [Rate Limits Guide](rate-limits.md) to learn about managing API quotas.* 