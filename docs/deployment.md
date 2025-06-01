# Deployment Guide

This guide covers deploying and using the WFRMLS Python API wrapper in production environments.

## Table of Contents

1. [Production Environment Setup](#production-environment-setup)
2. [Configuration Management](#configuration-management)
3. [Performance Optimization](#performance-optimization)
4. [Monitoring and Logging](#monitoring-and-logging)
5. [Security Best Practices](#security-best-practices)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Production Troubleshooting](#production-troubleshooting)

## Production Environment Setup

### System Requirements

- **Python**: 3.8 or higher
- **Memory**: Minimum 512MB RAM (recommended 2GB+ for high-volume applications)
- **Network**: Stable internet connection with access to `api.wfrmls.com`
- **Storage**: Sufficient space for logs and temporary files

### Installation in Production

```bash
# Create production virtual environment
python -m venv /opt/wfrmls-env
source /opt/wfrmls-env/bin/activate

# Install from PyPI
pip install wfrmls

# Verify installation
python -c "import wfrmls; print(f'WFRMLS version: {wfrmls.__version__}')"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "your_app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  wfrmls-app:
    build: .
    environment:
      - WFRMLS_BEARER_TOKEN=${WFRMLS_BEARER_TOKEN}
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

## Configuration Management

### Environment Variables

Set these environment variables in production:

```bash
# Required
export WFRMLS_BEARER_TOKEN="your_production_api_key"

# Optional - Performance tuning
export WFRMLS_TIMEOUT=30
export WFRMLS_RETRY_ATTEMPTS=3
export WFRMLS_RATE_LIMIT_DELAY=0.1

# Optional - Logging
export LOG_LEVEL=INFO
export LOG_FILE="/var/log/wfrmls/app.log"
```

### Configuration File Pattern

```python
# config.py
import os
from typing import Optional

class WFRMLSConfig:
    """Configuration for WFRMLS client in production."""
    
    # API Configuration
    API_KEY: str = os.getenv("WFRMLS_BEARER_TOKEN", "")
    BASE_URL: str = os.getenv("WFRMLS_BASE_URL", "https://api.wfrmls.com")
    TIMEOUT: int = int(os.getenv("WFRMLS_TIMEOUT", "30"))
    
    # Rate Limiting
    RATE_LIMIT_DELAY: float = float(os.getenv("WFRMLS_RATE_LIMIT_DELAY", "0.1"))
    MAX_RETRIES: int = int(os.getenv("WFRMLS_MAX_RETRIES", "3"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    # Cache settings (if using cache)
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if not cls.API_KEY:
            raise ValueError("WFRMLS_BEARER_TOKEN is required")
        
        if cls.TIMEOUT <= 0:
            raise ValueError("WFRMLS_TIMEOUT must be positive")

# Usage
config = WFRMLSConfig()
config.validate()
```

### Production Client Setup

```python
# production_client.py
import logging
import time
from typing import Dict, Any, Optional
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError, AuthenticationError

class ProductionWFRMLSClient:
    """Production wrapper for WFRMLS client with error handling and monitoring."""
    
    def __init__(self, config: WFRMLSConfig):
        self.config = config
        self.client = WFRMLSClient(api_key=config.API_KEY)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up production logging."""
        logger = logging.getLogger("wfrmls_production")
        logger.setLevel(getattr(logging, self.config.LOG_LEVEL))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler if configured
        if self.config.LOG_FILE:
            file_handler = logging.FileHandler(self.config.LOG_FILE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def safe_api_call(self, operation_name: str, func, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """Execute API call with production error handling."""
        start_time = time.time()
        
        for attempt in range(self.config.MAX_RETRIES):
            try:
                self.logger.info(f"Executing {operation_name} (attempt {attempt + 1})")
                result = func(*args, **kwargs)
                
                duration = time.time() - start_time
                self.logger.info(
                    f"{operation_name} completed successfully in {duration:.2f}s"
                )
                return result
                
            except AuthenticationError as e:
                self.logger.error(f"{operation_name} authentication failed: {e}")
                raise  # Don't retry auth errors
                
            except WFRMLSError as e:
                self.logger.warning(
                    f"{operation_name} failed (attempt {attempt + 1}): {e}"
                )
                
                if attempt < self.config.MAX_RETRIES - 1:
                    delay = self.config.RATE_LIMIT_DELAY * (2 ** attempt)
                    self.logger.info(f"Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"{operation_name} failed after all retries")
                    raise
                    
            except Exception as e:
                self.logger.error(f"Unexpected error in {operation_name}: {e}")
                if attempt == self.config.MAX_RETRIES - 1:
                    raise
        
        return None
```

## Performance Optimization

### Connection Pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedWFRMLSClient(WFRMLSClient):
    """WFRMLS client optimized for production use."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_session()
    
    def _setup_session(self):
        """Configure session with connection pooling and retries."""
        # Connection pooling
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            pool_block=False
        )
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter.max_retries = retry_strategy
        
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
```

### Caching Strategy

```python
import functools
import time
from typing import Dict, Any, Optional

class CachedWFRMLSClient:
    """WFRMLS client with intelligent caching."""
    
    def __init__(self, client: WFRMLSClient, cache_ttl: int = 300):
        self.client = client
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _cache_key(self, method: str, **kwargs) -> str:
        """Generate cache key from method and parameters."""
        key_parts = [method]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        return "|".join(key_parts)
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid."""
        return time.time() - cache_entry["timestamp"] < self.cache_ttl
    
    def cached_lookup_values(self, lookup_type: str) -> list:
        """Get lookup values with caching (lookup data changes rarely)."""
        cache_key = self._cache_key("lookup_values", lookup_type=lookup_type)
        
        if cache_key in self._cache and self._is_cache_valid(self._cache[cache_key]):
            return self._cache[cache_key]["data"]
        
        # Fetch from API
        data = self.client.lookup.get_lookup_values(lookup_type)
        
        # Cache result
        self._cache[cache_key] = {
            "data": data,
            "timestamp": time.time()
        }
        
        return data
```

### Batch Processing

```python
class BatchProcessor:
    """Efficiently process multiple WFRMLS requests."""
    
    def __init__(self, client: WFRMLSClient, batch_size: int = 50, delay: float = 0.1):
        self.client = client
        self.batch_size = batch_size
        self.delay = delay
        self.logger = logging.getLogger(__name__)
    
    def process_properties_batch(self, property_ids: list) -> list:
        """Process multiple property IDs efficiently."""
        results = []
        failed = []
        
        for i in range(0, len(property_ids), self.batch_size):
            batch = property_ids[i:i + self.batch_size]
            
            self.logger.info(f"Processing batch {i//self.batch_size + 1}")
            
            for property_id in batch:
                try:
                    property_data = self.client.properties.get_property(property_id)
                    results.append(property_data)
                    
                except WFRMLSError as e:
                    self.logger.warning(f"Failed to get property {property_id}: {e}")
                    failed.append(property_id)
                
                # Rate limiting
                time.sleep(self.delay)
        
        self.logger.info(f"Processed {len(results)} properties, {len(failed)} failed")
        return results
```

## Monitoring and Logging

### Application Metrics

```python
import time
from typing import Dict
from dataclasses import dataclass, field

@dataclass
class APIMetrics:
    """Track API usage metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    error_counts: Dict[str, int] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def average_response_time(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_response_time / self.successful_requests

class MonitoredWFRMLSClient:
    """WFRMLS client with monitoring capabilities."""
    
    def __init__(self, client: WFRMLSClient):
        self.client = client
        self.metrics = APIMetrics()
        self.logger = logging.getLogger(__name__)
    
    def monitored_request(self, method_name: str, func, *args, **kwargs):
        """Execute request with monitoring."""
        start_time = time.time()
        self.metrics.total_requests += 1
        
        try:
            result = func(*args, **kwargs)
            
            # Record success
            response_time = time.time() - start_time
            self.metrics.successful_requests += 1
            self.metrics.total_response_time += response_time
            
            self.logger.info(
                f"{method_name} completed in {response_time:.2f}s "
                f"(success rate: {self.metrics.success_rate:.2%})"
            )
            
            return result
            
        except Exception as e:
            # Record failure
            self.metrics.failed_requests += 1
            error_type = type(e).__name__
            self.metrics.error_counts[error_type] = self.metrics.error_counts.get(error_type, 0) + 1
            
            self.logger.error(f"{method_name} failed: {e}")
            raise
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current metrics summary."""
        return {
            "total_requests": self.metrics.total_requests,
            "success_rate": f"{self.metrics.success_rate:.2%}",
            "average_response_time": f"{self.metrics.average_response_time:.2f}s",
            "error_counts": self.metrics.error_counts
        }
```

### Health Check Endpoint

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring systems."""
    try:
        # Test WFRMLS API connectivity
        client = WFRMLSClient()
        resources = client.resource.get_resources()
        
        return jsonify({
            "status": "healthy",
            "wfrmls_api": "connected",
            "version": os.getenv("APP_VERSION", "unknown"),
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route('/metrics')
def metrics():
    """Expose metrics for monitoring."""
    # Return your application metrics
    return jsonify(monitored_client.get_metrics_summary())
```

## Security Best Practices

### API Key Management

```python
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration management."""
    
    @staticmethod
    def get_api_key() -> str:
        """Get API key from secure source."""
        
        # Option 1: Environment variable (recommended for containers)
        api_key = os.getenv("WFRMLS_BEARER_TOKEN")
        if api_key:
            return api_key
        
        # Option 2: Encrypted file
        encrypted_file = os.getenv("WFRMLS_KEY_FILE")
        if encrypted_file and os.path.exists(encrypted_file):
            return SecureConfig._decrypt_key_file(encrypted_file)
        
        # Option 3: Key management service (AWS KMS, HashiCorp Vault, etc.)
        # Implementation depends on your infrastructure
        
        raise ValueError("No API key found in secure sources")
    
    @staticmethod
    def _decrypt_key_file(file_path: str) -> str:
        """Decrypt API key from file."""
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("Encryption key not found")
        
        cipher = Fernet(encryption_key.encode())
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        return cipher.decrypt(encrypted_data).decode()
```

### Network Security

```python
import ssl
import certifi

# Configure SSL context for secure connections
def create_secure_session():
    """Create session with strict SSL verification."""
    session = requests.Session()
    
    # Use system certificates
    session.verify = certifi.where()
    
    # Configure SSL context
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    
    return session
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          pytest --cov=wfrmls --cov-report=xml
        env:
          WFRMLS_BEARER_TOKEN: ${{ secrets.WFRMLS_TEST_TOKEN }}
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Your deployment commands here
          echo "Deploying to production..."
        env:
          WFRMLS_BEARER_TOKEN: ${{ secrets.WFRMLS_PROD_TOKEN }}
```

### Deployment Checklist

Before each production deployment:

- [ ] All tests pass
- [ ] Code coverage remains at target level
- [ ] Documentation is updated
- [ ] API keys are properly configured
- [ ] Monitoring is in place
- [ ] Rollback plan is ready
- [ ] Performance benchmarks are acceptable

## Production Troubleshooting

### Common Production Issues

**1. Rate Limiting**
```python
# Monitor rate limit headers
def check_rate_limits(response):
    if 'X-RateLimit-Remaining' in response.headers:
        remaining = int(response.headers['X-RateLimit-Remaining'])
        if remaining < 10:
            logger.warning(f"Rate limit warning: {remaining} requests remaining")
```

**2. Memory Management**
```python
# Monitor memory usage
import psutil

def check_memory_usage():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        logger.warning(f"High memory usage: {memory.percent}%")
```

**3. Error Recovery**
```python
def graceful_degradation(func):
    """Decorator for graceful degradation of functionality."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WFRMLSError as e:
            logger.error(f"API error, falling back to cached data: {e}")
            return get_cached_fallback()
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    return wrapper
```

### Performance Monitoring

```bash
# Production monitoring commands
# CPU and memory usage
top -p $(pgrep -f "python.*wfrmls")

# Network connections
netstat -an | grep :443

# Log monitoring
tail -f /var/log/wfrmls/app.log | grep ERROR

# Disk usage
df -h
```

### Emergency Procedures

**API Service Down:**
1. Check WFRMLS status page
2. Enable fallback/cached responses
3. Notify stakeholders
4. Monitor for service restoration

**High Error Rate:**
1. Check API key validity
2. Verify network connectivity
3. Review recent code changes
4. Scale back request rate

**Memory Issues:**
1. Restart application gracefully
2. Clear caches
3. Check for memory leaks
4. Scale up resources if needed

Remember to always test deployment procedures in a staging environment that mirrors production as closely as possible. 