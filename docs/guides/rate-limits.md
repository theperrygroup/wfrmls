# Rate Limits Guide

Manage API quotas and implement efficient request patterns with the WFRMLS Python client.

---

## 🎯 Overview

Understanding and properly managing rate limits is essential for building reliable real estate applications. This guide covers WFRMLS API rate limits, detection strategies, and best practices for staying within quotas.

### What You'll Learn

- **Rate limit structure** - Understanding WFRMLS API quotas and limits
- **Detection and monitoring** - Identifying when you're approaching limits
- **Throttling strategies** - Implementing proper request pacing
- **Optimization techniques** - Reducing API usage while maintaining functionality
- **Production patterns** - Real-world rate limiting implementations

---

## 📊 WFRMLS Rate Limits

### Current Limits

| Limit Type | Value | Scope | Reset Period |
|------------|-------|-------|--------------|
| **Requests per minute** | 100 | Per IP address | 1 minute |
| **Requests per hour** | 6,000 | Per bearer token | 1 hour |
| **Requests per day** | 50,000 | Per bearer token | 24 hours |
| **Concurrent requests** | 10 | Per bearer token | N/A |

### Response Headers

The API includes rate limit information in response headers:

```http
X-RateLimit-Limit: 6000
X-RateLimit-Remaining: 5847
X-RateLimit-Reset: 1640995200
X-RateLimit-RetryAfter: 60
```

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Total requests allowed in current window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when window resets |
| `X-RateLimit-RetryAfter` | Seconds to wait before retry (if rate limited) |

---

## 🚨 Rate Limit Detection

### Basic Rate Limit Handling

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import RateLimitError
import time

def handle_rate_limit_basic():
    """Basic rate limit handling with simple retry."""
    
    try:
        client = WFRMLSClient()
        properties = client.property.get_properties(top=100)
        return properties
        
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        
        # Extract retry delay from exception or use default
        retry_after = getattr(e, 'retry_after', 60)
        print(f"Waiting {retry_after} seconds before retry...")
        
        time.sleep(retry_after)
        
        # Retry once
        try:
            properties = client.property.get_properties(top=100)
            return properties
        except RateLimitError:
            print("Still rate limited after retry")
            return None
```

### Response Header Monitoring

```python
import requests
from typing import Optional, Dict, Any

class RateLimitMonitor:
    """Monitor rate limit status from API responses."""
    
    def __init__(self):
        self.last_headers = {}
        self.requests_made = 0
    
    def update_from_response(self, response: requests.Response):
        """Update rate limit info from response headers."""
        
        headers = response.headers
        self.last_headers = {
            'limit': int(headers.get('X-RateLimit-Limit', 0)),
            'remaining': int(headers.get('X-RateLimit-Remaining', 0)),
            'reset': int(headers.get('X-RateLimit-Reset', 0)),
            'retry_after': int(headers.get('X-RateLimit-RetryAfter', 60))
        }
        self.requests_made += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current rate limit status."""
        if not self.last_headers:
            return {'status': 'unknown'}
        
        remaining = self.last_headers['remaining']
        limit = self.last_headers['limit']
        
        usage_percent = ((limit - remaining) / limit) * 100 if limit > 0 else 0
        
        return {
            'limit': limit,
            'remaining': remaining,
            'usage_percent': usage_percent,
            'reset_timestamp': self.last_headers['reset'],
            'requests_made': self.requests_made,
            'status': self._get_status_level(usage_percent)
        }
    
    def _get_status_level(self, usage_percent: float) -> str:
        """Determine status level based on usage."""
        if usage_percent < 70:
            return 'ok'
        elif usage_percent < 90:
            return 'warning'
        else:
            return 'critical'
    
    def should_throttle(self) -> bool:
        """Check if requests should be throttled."""
        status = self.get_status()
        return status.get('usage_percent', 0) > 80
    
    def get_recommended_delay(self) -> float:
        """Get recommended delay between requests."""
        status = self.get_status()
        usage_percent = status.get('usage_percent', 0)
        
        if usage_percent < 50:
            return 0.1  # 100ms
        elif usage_percent < 80:
            return 0.5  # 500ms
        else:
            return 2.0  # 2 seconds

# Usage with custom client wrapper
class ThrottledClient:
    """WFRMLS client with automatic throttling."""
    
    def __init__(self):
        self.client = WFRMLSClient()
        self.monitor = RateLimitMonitor()
    
    def get_properties(self, **kwargs):
        """Get properties with automatic throttling."""
        
        # Check if we should delay
        if self.monitor.should_throttle():
            delay = self.monitor.get_recommended_delay()
            print(f"Throttling: waiting {delay}s due to rate limit usage")
            time.sleep(delay)
        
        try:
            # Make the request (assuming we can access response headers)
            properties = self.client.property.get_properties(**kwargs)
            
            # In a real implementation, you'd need to access the response
            # headers. This would require modifying the client or using
            # a requests session with hooks.
            
            return properties
            
        except RateLimitError as e:
            print("Rate limited despite throttling")
            retry_after = getattr(e, 'retry_after', 60)
            time.sleep(retry_after)
            raise
```

---

## ⏱️ Throttling Strategies

### Fixed Delay Throttling

```python
import time
from functools import wraps

def throttle(delay: float):
    """Decorator to add fixed delay between calls."""
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < delay:
                time.sleep(delay - elapsed)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
            
        return wrapper
    return decorator

# Usage
@throttle(delay=0.5)  # 500ms delay between calls
def get_properties_throttled(**kwargs):
    """Get properties with fixed throttling."""
    client = WFRMLSClient()
    return client.property.get_properties(**kwargs)

# This will automatically wait 500ms between calls
properties1 = get_properties_throttled(top=50)
properties2 = get_properties_throttled(top=50, skip=50)  # Waits 500ms
```

### Adaptive Throttling

```python
import time
from threading import Lock

class AdaptiveThrottler:
    """Adaptive throttling based on success/failure rates."""
    
    def __init__(self, initial_delay: float = 0.1, max_delay: float = 5.0):
        self.delay = initial_delay
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.consecutive_successes = 0
        self.consecutive_failures = 0
        self.lock = Lock()
    
    def wait(self):
        """Wait for the current delay period."""
        time.sleep(self.delay)
    
    def record_success(self):
        """Record successful request and adjust delay."""
        with self.lock:
            self.consecutive_successes += 1
            self.consecutive_failures = 0
            
            # Decrease delay on consecutive successes
            if self.consecutive_successes >= 5:
                self.delay = max(self.initial_delay, self.delay * 0.8)
                self.consecutive_successes = 0
    
    def record_failure(self, is_rate_limit: bool = False):
        """Record failed request and adjust delay."""
        with self.lock:
            self.consecutive_failures += 1
            self.consecutive_successes = 0
            
            # Increase delay on failures, especially rate limits
            if is_rate_limit:
                self.delay = min(self.max_delay, self.delay * 3.0)
            else:
                self.delay = min(self.max_delay, self.delay * 1.5)
    
    def get_current_delay(self) -> float:
        """Get current delay value."""
        return self.delay

# Usage
throttler = AdaptiveThrottler()

def adaptive_api_call(func, *args, **kwargs):
    """Make API call with adaptive throttling."""
    
    throttler.wait()
    
    try:
        result = func(*args, **kwargs)
        throttler.record_success()
        return result
        
    except RateLimitError:
        throttler.record_failure(is_rate_limit=True)
        raise
        
    except Exception:
        throttler.record_failure(is_rate_limit=False)
        raise

# Example usage
for i in range(10):
    try:
        client = WFRMLSClient()
        properties = adaptive_api_call(
            client.property.get_properties,
            top=50,
            skip=i*50
        )
        print(f"Retrieved page {i+1}, delay: {throttler.get_current_delay():.2f}s")
        
    except RateLimitError:
        print(f"Rate limited on page {i+1}")
        break
```

### Token Bucket Algorithm

```python
import time
import threading

class TokenBucket:
    """Token bucket rate limiter."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum number of tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, tokens: int = 1) -> bool:
        """Try to acquire tokens from bucket."""
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_for_tokens(self, tokens: int = 1, timeout: float = None):
        """Wait until tokens are available."""
        start_time = time.time()
        
        while not self.acquire(tokens):
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError("Timeout waiting for tokens")
            
            # Calculate how long to wait for next token
            with self.lock:
                wait_time = min(1.0, tokens / self.refill_rate)
            
            time.sleep(wait_time)
    
    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def get_status(self) -> dict:
        """Get current bucket status."""
        with self.lock:
            self._refill()
            return {
                'tokens': int(self.tokens),
                'capacity': self.capacity,
                'fill_percentage': (self.tokens / self.capacity) * 100
            }

# Usage for WFRMLS API (100 requests per minute)
bucket = TokenBucket(capacity=100, refill_rate=100/60)  # 100 tokens, 1.67/sec refill

def rate_limited_request(func, *args, **kwargs):
    """Make request with token bucket rate limiting."""
    
    # Wait for token availability
    bucket.wait_for_tokens(tokens=1, timeout=30)
    
    try:
        return func(*args, **kwargs)
    except RateLimitError:
        # If we hit rate limit despite token bucket, something's wrong
        print("Rate limited despite token bucket - adjusting...")
        time.sleep(60)
        raise

# Example usage
client = WFRMLSClient()

for i in range(10):
    try:
        properties = rate_limited_request(
            client.property.get_properties,
            top=50,
            skip=i*50
        )
        
        status = bucket.get_status()
        print(f"Page {i+1}: {len(properties)} properties, "
              f"tokens: {status['tokens']}/{status['capacity']}")
        
    except Exception as e:
        print(f"Error on page {i+1}: {e}")
        break
```

---

## 🎯 Optimization Techniques

### Request Batching

```python
from typing import List, Dict, Any
import asyncio

class BatchProcessor:
    """Batch multiple requests to optimize API usage."""
    
    def __init__(self, batch_size: int = 10, delay_between_batches: float = 1.0):
        self.batch_size = batch_size
        self.delay_between_batches = delay_between_batches
        self.client = WFRMLSClient()
    
    def process_listing_ids(self, listing_ids: List[str]) -> List[Dict[str, Any]]:
        """Process multiple listing IDs in batches."""
        
        results = []
        
        for i in range(0, len(listing_ids), self.batch_size):
            batch = listing_ids[i:i + self.batch_size]
            
            print(f"Processing batch {i//self.batch_size + 1}: "
                  f"{len(batch)} listings")
            
            batch_results = self._process_batch(batch)
            results.extend(batch_results)
            
            # Delay between batches
            if i + self.batch_size < len(listing_ids):
                time.sleep(self.delay_between_batches)
        
        return results
    
    def _process_batch(self, listing_ids: List[str]) -> List[Dict[str, Any]]:
        """Process a single batch of listing IDs."""
        
        results = []
        
        for listing_id in listing_ids:
            try:
                property_data = self.client.property.get_property(listing_id)
                if property_data:
                    results.append(property_data)
                    
            except Exception as e:
                print(f"Error processing {listing_id}: {e}")
                continue
            
            # Small delay between individual requests in batch
            time.sleep(0.1)
        
        return results

# Usage
batch_processor = BatchProcessor(batch_size=5, delay_between_batches=2.0)

listing_ids = ["12345678", "23456789", "34567890", "45678901", "56789012"]
properties = batch_processor.process_listing_ids(listing_ids)

print(f"Retrieved {len(properties)} properties")
```

### Intelligent Caching

```python
import time
import json
import hashlib
from typing import Optional, Any, Dict

class RateLimitAwareCache:
    """Cache with rate limit optimization."""
    
    def __init__(self, default_ttl: int = 300, rate_limit_ttl: int = 3600):
        """
        Args:
            default_ttl: Normal cache TTL in seconds
            rate_limit_ttl: Extended TTL when rate limited
        """
        self.cache = {}
        self.default_ttl = default_ttl
        self.rate_limit_ttl = rate_limit_ttl
        self.rate_limited = False
    
    def _make_key(self, method: str, **kwargs) -> str:
        """Create cache key from method and parameters."""
        key_data = f"{method}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, method: str, **kwargs) -> Optional[Any]:
        """Get cached result if available and valid."""
        key = self._make_key(method, **kwargs)
        
        if key not in self.cache:
            return None
        
        data, timestamp, ttl = self.cache[key]
        
        if time.time() - timestamp > ttl:
            del self.cache[key]
            return None
        
        return data
    
    def set(self, method: str, data: Any, **kwargs):
        """Cache result with appropriate TTL."""
        key = self._make_key(method, **kwargs)
        
        # Use extended TTL if we've been rate limited
        ttl = self.rate_limit_ttl if self.rate_limited else self.default_ttl
        
        self.cache[key] = (data, time.time(), ttl)
    
    def set_rate_limited(self, is_rate_limited: bool):
        """Update rate limit status."""
        self.rate_limited = is_rate_limited
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        current_time = time.time()
        valid_entries = 0
        expired_entries = 0
        
        for data, timestamp, ttl in self.cache.values():
            if current_time - timestamp > ttl:
                expired_entries += 1
            else:
                valid_entries += 1
        
        return {
            'total_entries': len(self.cache),
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'rate_limited': self.rate_limited
        }

# Usage
cache = RateLimitAwareCache()

def cached_get_properties(**kwargs):
    """Get properties with intelligent caching."""
    
    # Try cache first
    cached_result = cache.get('get_properties', **kwargs)
    if cached_result:
        print("✅ Cache hit")
        return cached_result
    
    try:
        client = WFRMLSClient()
        properties = client.property.get_properties(**kwargs)
        
        # Cache successful result
        cache.set('get_properties', properties, **kwargs)
        cache.set_rate_limited(False)
        
        print("✅ Fresh data retrieved and cached")
        return properties
        
    except RateLimitError:
        cache.set_rate_limited(True)
        print("⚠️ Rate limited - future requests will use extended cache TTL")
        raise

# Example usage
for i in range(5):
    try:
        properties = cached_get_properties(
            filter_query="StandardStatus eq 'Active'",
            top=50,
            skip=i*50
        )
        
        stats = cache.get_stats()
        print(f"Page {i+1}: {len(properties)} properties, "
              f"cache: {stats['valid_entries']} entries")
        
    except RateLimitError:
        print("Rate limited - using cached data for subsequent requests")
        break
```

### Field Selection Optimization

```python
from typing import List, Dict, Any, Optional

class OptimizedPropertyClient:
    """Property client optimized for minimal API usage."""
    
    # Minimal fields for different use cases
    FIELD_SETS = {
        'listing': ['ListingId', 'ListPrice', 'StandardStatus', 'City'],
        'search': ['ListingId', 'ListPrice', 'City', 'BedroomsTotal', 'BathroomsTotalInteger'],
        'map': ['ListingId', 'ListPrice', 'Latitude', 'Longitude', 'Address'],
        'detail': [
            'ListingId', 'ListPrice', 'Address', 'City', 'PostalCode',
            'BedroomsTotal', 'BathroomsTotalInteger', 'SquareFeet',
            'YearBuilt', 'PropertyType', 'StandardStatus'
        ]
    }
    
    def __init__(self):
        self.client = WFRMLSClient()
        self.request_count = 0
    
    def get_properties(
        self,
        use_case: str = 'listing',
        custom_fields: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Get properties with optimized field selection."""
        
        # Use predefined field set or custom fields
        if custom_fields:
            select_fields = custom_fields
        else:
            select_fields = self.FIELD_SETS.get(use_case, self.FIELD_SETS['listing'])
        
        self.request_count += 1
        
        print(f"Request #{self.request_count}: "
              f"Using {len(select_fields)} fields for '{use_case}' use case")
        
        return self.client.property.get_properties(
            select=select_fields,
            **kwargs
        )
    
    def get_detailed_property(self, listing_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed property info (only when needed)."""
        
        self.request_count += 1
        
        print(f"Request #{self.request_count}: "
              f"Getting detailed info for {listing_id}")
        
        return self.client.property.get_property(listing_id)
    
    def search_and_detail_workflow(
        self,
        search_criteria: Dict[str, Any],
        detail_limit: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Optimized workflow: search with minimal fields, then get details."""
        
        # Step 1: Search with minimal fields
        search_results = self.get_properties(
            use_case='search',
            **search_criteria
        )
        
        print(f"Found {len(search_results)} properties in search")
        
        # Step 2: Get detailed info for subset
        detailed_properties = []
        for prop in search_results[:detail_limit]:
            try:
                detailed = self.get_detailed_property(prop['ListingId'])
                if detailed:
                    detailed_properties.append(detailed)
            except Exception as e:
                print(f"Error getting details for {prop['ListingId']}: {e}")
        
        return {
            'search_results': search_results,
            'detailed_properties': detailed_properties,
            'total_requests': self.request_count
        }

# Usage
optimized_client = OptimizedPropertyClient()

# Different use cases with appropriate field sets
listings = optimized_client.get_properties(
    use_case='listing',
    filter_query="StandardStatus eq 'Active'",
    top=50
)

map_data = optimized_client.get_properties(
    use_case='map',
    filter_query="StandardStatus eq 'Active' and Latitude ne null",
    top=100
)

# Workflow optimization
workflow_results = optimized_client.search_and_detail_workflow(
    search_criteria={
        'filter_query': "ListPrice ge 500000 and StandardStatus eq 'Active'",
        'top': 20
    },
    detail_limit=5
)

print(f"\nWorkflow completed with {workflow_results['total_requests']} total API requests")
print(f"Found {len(workflow_results['search_results'])} search results")
print(f"Retrieved details for {len(workflow_results['detailed_properties'])} properties")
```

---

## 📊 Production Monitoring

### Rate Limit Dashboard

```python
import time
from datetime import datetime, timedelta
from collections import deque, defaultdict

class RateLimitDashboard:
    """Monitor and display rate limit usage patterns."""
    
    def __init__(self, window_minutes: int = 60):
        self.window_minutes = window_minutes
        self.request_history = deque()
        self.error_history = deque()
        self.rate_limit_events = deque()
        
    def record_request(self, endpoint: str, success: bool = True):
        """Record API request."""
        now = datetime.now()
        
        self.request_history.append({
            'timestamp': now,
            'endpoint': endpoint,
            'success': success
        })
        
        self._cleanup_old_records()
    
    def record_rate_limit(self, endpoint: str, retry_after: int):
        """Record rate limit event."""
        now = datetime.now()
        
        self.rate_limit_events.append({
            'timestamp': now,
            'endpoint': endpoint,
            'retry_after': retry_after
        })
        
        self._cleanup_old_records()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current rate limit metrics."""
        self._cleanup_old_records()
        
        now = datetime.now()
        
        # Request rate (per minute)
        total_requests = len(self.request_history)
        request_rate = total_requests / self.window_minutes
        
        # Success rate
        successful_requests = sum(1 for req in self.request_history if req['success'])
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Rate limit events
        rate_limit_count = len(self.rate_limit_events)
        
        # Endpoint breakdown
        endpoint_stats = defaultdict(int)
        for req in self.request_history:
            endpoint_stats[req['endpoint']] += 1
        
        return {
            'window_minutes': self.window_minutes,
            'total_requests': total_requests,
            'request_rate_per_minute': request_rate,
            'success_rate_percent': success_rate,
            'rate_limit_events': rate_limit_count,
            'endpoint_breakdown': dict(endpoint_stats),
            'last_updated': now.isoformat()
        }
    
    def print_dashboard(self):
        """Print rate limit dashboard."""
        metrics = self.get_metrics()
        
        print("\n" + "="*60)
        print("🚦 RATE LIMIT DASHBOARD")
        print("="*60)
        print(f"📊 Window: {metrics['window_minutes']} minutes")
        print(f"📈 Total Requests: {metrics['total_requests']}")
        print(f"⚡ Rate: {metrics['request_rate_per_minute']:.1f} req/min")
        print(f"✅ Success Rate: {metrics['success_rate_percent']:.1f}%")
        print(f"🚨 Rate Limit Events: {metrics['rate_limit_events']}")
        
        print("\n📍 Endpoint Breakdown:")
        for endpoint, count in metrics['endpoint_breakdown'].items():
            print(f"  {endpoint}: {count} requests")
        
        print(f"\n🕒 Last Updated: {metrics['last_updated']}")
        print("="*60)
    
    def _cleanup_old_records(self):
        """Remove records older than window."""
        cutoff = datetime.now() - timedelta(minutes=self.window_minutes)
        
        while self.request_history and self.request_history[0]['timestamp'] < cutoff:
            self.request_history.popleft()
            
        while self.rate_limit_events and self.rate_limit_events[0]['timestamp'] < cutoff:
            self.rate_limit_events.popleft()

# Usage
dashboard = RateLimitDashboard(window_minutes=60)

def monitored_api_call(func, endpoint_name: str, *args, **kwargs):
    """Make API call with monitoring."""
    
    try:
        result = func(*args, **kwargs)
        dashboard.record_request(endpoint_name, success=True)
        return result
        
    except RateLimitError as e:
        retry_after = getattr(e, 'retry_after', 60)
        dashboard.record_rate_limit(endpoint_name, retry_after)
        dashboard.record_request(endpoint_name, success=False)
        raise
        
    except Exception:
        dashboard.record_request(endpoint_name, success=False)
        raise

# Example usage
client = WFRMLSClient()

for i in range(10):
    try:
        properties = monitored_api_call(
            client.property.get_properties,
            'get_properties',
            top=50,
            skip=i*50
        )
        
        if i % 3 == 0:  # Print dashboard every 3 requests
            dashboard.print_dashboard()
        
    except RateLimitError:
        print("Rate limited!")
        dashboard.print_dashboard()
        break
    except Exception as e:
        print(f"Error: {e}")
```

### Alert System

```python
import smtplib
from email.mime.text import MIMEText
from typing import Callable, List

class RateLimitAlertSystem:
    """Alert system for rate limit events."""
    
    def __init__(self):
        self.alert_handlers: List[Callable] = []
        self.alert_thresholds = {
            'requests_per_minute': 80,  # Alert at 80 req/min
            'success_rate_threshold': 95,  # Alert if success rate < 95%
            'consecutive_rate_limits': 3  # Alert after 3 consecutive rate limits
        }
        self.consecutive_rate_limits = 0
    
    def add_alert_handler(self, handler: Callable):
        """Add alert handler function."""
        self.alert_handlers.append(handler)
    
    def check_and_alert(self, metrics: Dict[str, Any]):
        """Check metrics and trigger alerts if needed."""
        
        alerts = []
        
        # High request rate
        if metrics['request_rate_per_minute'] > self.alert_thresholds['requests_per_minute']:
            alerts.append(
                f"🚨 HIGH REQUEST RATE: {metrics['request_rate_per_minute']:.1f} req/min "
                f"(threshold: {self.alert_thresholds['requests_per_minute']})"
            )
        
        # Low success rate
        if metrics['success_rate_percent'] < self.alert_thresholds['success_rate_threshold']:
            alerts.append(
                f"🚨 LOW SUCCESS RATE: {metrics['success_rate_percent']:.1f}% "
                f"(threshold: {self.alert_thresholds['success_rate_threshold']}%)"
            )
        
        # Rate limit events
        if metrics['rate_limit_events'] > 0:
            self.consecutive_rate_limits += metrics['rate_limit_events']
            
            if self.consecutive_rate_limits >= self.alert_thresholds['consecutive_rate_limits']:
                alerts.append(
                    f"🚨 MULTIPLE RATE LIMITS: {self.consecutive_rate_limits} consecutive events"
                )
        else:
            self.consecutive_rate_limits = 0
        
        # Send alerts
        for alert_message in alerts:
            self._send_alert(alert_message, metrics)
    
    def _send_alert(self, message: str, metrics: Dict[str, Any]):
        """Send alert through all configured handlers."""
        for handler in self.alert_handlers:
            try:
                handler(message, metrics)
            except Exception as e:
                print(f"Error sending alert: {e}")

# Alert handler functions
def console_alert_handler(message: str, metrics: Dict[str, Any]):
    """Print alert to console."""
    print(f"\n{message}")
    print(f"Current metrics: {metrics}")

def email_alert_handler(message: str, metrics: Dict[str, Any]):
    """Send alert via email (example implementation)."""
    # This is a simplified example - implement with your email settings
    print(f"📧 EMAIL ALERT: {message}")
    # Actual email implementation would go here

def slack_alert_handler(message: str, metrics: Dict[str, Any]):
    """Send alert to Slack (example implementation)."""
    # This is a simplified example - implement with your Slack webhook
    print(f"💬 SLACK ALERT: {message}")
    # Actual Slack implementation would go here

# Setup alert system
alert_system = RateLimitAlertSystem()
alert_system.add_alert_handler(console_alert_handler)
alert_system.add_alert_handler(email_alert_handler)

# Integrate with dashboard
dashboard_with_alerts = RateLimitDashboard()

def check_for_alerts():
    """Check current metrics and send alerts if needed."""
    metrics = dashboard_with_alerts.get_metrics()
    alert_system.check_and_alert(metrics)

# Usage in monitoring loop
def monitoring_loop():
    """Continuous monitoring with alerts."""
    
    while True:
        try:
            # Your API operations here
            client = WFRMLSClient()
            properties = monitored_api_call(
                client.property.get_properties,
                'get_properties',
                top=50
            )
            
            # Check for alerts every few requests
            check_for_alerts()
            
            time.sleep(1)  # Adjust based on your needs
            
        except KeyboardInterrupt:
            print("Monitoring stopped")
            break
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(5)
```

---

## 📚 Next Steps

### **Related Guides**
- **[Error Handling Guide](error-handling.md)** - Comprehensive error handling including rate limit errors
- **[Property Search Guide](property-search.md)** - Optimizing search queries to reduce API usage
- **[Data Synchronization Guide](data-sync.md)** - Efficient data sync patterns

### **API Reference**
- **[Client API](../api/client.md)** - Client configuration options for rate limiting
- **[Exceptions API](../api/exceptions.md)** - RateLimitError details

### **Examples**
- **[Advanced Queries](../examples/advanced-queries.md)** - Efficient query patterns
- **[Monitoring Examples](../examples/monitoring.md)** - Production monitoring setups

---

*Ready to implement efficient rate limiting? Check out our [Data Synchronization Guide](data-sync.md) for advanced patterns.* 