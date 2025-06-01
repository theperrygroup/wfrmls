# Troubleshooting Guide

This guide covers common issues and their solutions when using the WFRMLS Python API wrapper.

## Table of Contents

1. [Authentication Issues](#authentication-issues)
2. [API Request Problems](#api-request-problems)
3. [Installation Issues](#installation-issues)
4. [Data and Response Issues](#data-and-response-issues)
5. [Performance Issues](#performance-issues)
6. [Development Issues](#development-issues)
7. [Network and Connectivity](#network-and-connectivity)
8. [Getting Additional Help](#getting-additional-help)

## Authentication Issues

### Issue: "Authentication failed - invalid API key"

**Symptoms:**
```python
AuthenticationError: Authentication failed - invalid API key
```

**Solutions:**
1. **Verify your API key:**
   ```python
   import os
   print(f"API Key: {os.getenv('WFRMLS_BEARER_TOKEN')}")
   ```

2. **Check environment variable name:**
   ```bash
   # Must be exactly this name
   export WFRMLS_BEARER_TOKEN="your_key_here"
   ```

3. **Test with direct parameter:**
   ```python
   client = WFRMLSClient(api_key="your_key_here")
   ```

4. **Verify .env file format:**
   ```bash
   # .env file - no quotes, no spaces around =
   WFRMLS_BEARER_TOKEN=your_actual_key_here
   ```

### Issue: "API key is required" Error

**Symptoms:**
```python
AuthenticationError: API key is required. Set WFRMLS_BEARER_TOKEN environment variable or pass api_key parameter.
```

**Solutions:**
1. **Set environment variable properly:**
   ```bash
   # Linux/macOS
   export WFRMLS_BEARER_TOKEN="your_key_here"
   
   # Windows
   set WFRMLS_BEARER_TOKEN=your_key_here
   ```

2. **Use .env file in project root:**
   ```bash
   WFRMLS_BEARER_TOKEN=your_key_here
   ```

3. **Pass API key directly:**
   ```python
   from wfrmls import WFRMLSClient
   client = WFRMLSClient(api_key="your_key_here")
   ```

## API Request Problems

### Issue: "404 Not Found" Errors

**Symptoms:**
```python
WFRMLSError: 404 Client Error: Not Found
```

**Solutions:**
1. **Verify endpoint exists:**
   ```python
   # Check available resources
   resources = client.resource.get_resources()
   print([r['resourceName'] for r in resources])
   ```

2. **Check record ID format:**
   ```python
   # Property IDs should be strings
   property_details = client.properties.get_property("123456")  # Not integer
   ```

3. **Verify resource permissions:**
   - Contact WFRMLS support to verify your API access level
   - Some endpoints may require specific permissions

### Issue: "400 Bad Request" Errors

**Symptoms:**
```python
WFRMLSError: 400 Client Error: Bad Request
```

**Solutions:**
1. **Check parameter format:**
   ```python
   from datetime import date
   
   # Correct date format
   properties = client.properties.search_properties(
       modification_timestamp_from=date(2024, 1, 1)  # Use date object
   )
   ```

2. **Validate required parameters:**
   ```python
   # Some endpoints require specific parameters
   media = client.media.search_media(
       resource_name="Property",  # Required
       resource_record_key="123456"  # Required
   )
   ```

3. **Check parameter values:**
   ```python
   # Use valid enum values or strings
   properties = client.properties.search_properties(
       listing_status="Active"  # Must be valid status
   )
   ```

### Issue: "429 Too Many Requests" Errors

**Symptoms:**
```python
WFRMLSError: 429 Client Error: Too Many Requests
```

**Solutions:**
1. **Implement rate limiting:**
   ```python
   import time
   
   def rate_limited_requests(requests_list):
       results = []
       for request in requests_list:
           try:
               result = request()
               results.append(result)
               time.sleep(0.1)  # 100ms delay
           except Exception as e:
               print(f"Error: {e}")
               time.sleep(1)  # Longer delay on error
       return results
   ```

2. **Use batch operations when available:**
   ```python
   # Instead of multiple individual requests
   property_ids = ["123", "456", "789"]
   
   # Use pagination to get multiple results
   properties = client.properties.search_properties(
       page_size=100  # Get more results per request
   )
   ```

## Installation Issues

### Issue: Package Not Found

**Symptoms:**
```bash
ERROR: Could not find a version that satisfies the requirement wfrmls
```

**Solutions:**
1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

2. **Check Python version:**
   ```bash
   python --version  # Must be 3.8+
   ```

3. **Use specific index if needed:**
   ```bash
   pip install --index-url https://pypi.org/simple/ wfrmls
   ```

### Issue: Permission Denied During Installation

**Symptoms:**
```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
1. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   pip install wfrmls
   ```

2. **Install for user only:**
   ```bash
   pip install --user wfrmls
   ```

### Issue: Import Errors

**Symptoms:**
```python
ModuleNotFoundError: No module named 'wfrmls'
```

**Solutions:**
1. **Verify installation:**
   ```bash
   pip list | grep wfrmls
   ```

2. **Check Python environment:**
   ```python
   import sys
   print(sys.path)
   ```

3. **Reinstall package:**
   ```bash
   pip uninstall wfrmls
   pip install wfrmls
   ```

## Data and Response Issues

### Issue: Empty Results

**Symptoms:**
```python
properties = client.properties.search_properties(city="Salt Lake City")
print(len(properties))  # Returns 0
```

**Solutions:**
1. **Check filter parameters:**
   ```python
   # Remove filters to see if data exists
   all_properties = client.properties.search_properties()
   print(f"Total properties: {len(all_properties)}")
   ```

2. **Verify search criteria:**
   ```python
   # Use broader search criteria
   properties = client.properties.search_properties(
       city="Salt Lake City",
       listing_status="Active"  # Try different statuses
   )
   ```

3. **Check pagination:**
   ```python
   # Increase page size
   properties = client.properties.search_properties(
       city="Salt Lake City",
       page_size=100  # Default might be too small
   )
   ```

### Issue: Unexpected Data Structure

**Symptoms:**
```python
property_data = client.properties.get_property("123456")
print(property_data['Address'])  # KeyError: 'Address'
```

**Solutions:**
1. **Inspect response structure:**
   ```python
   import json
   property_data = client.properties.get_property("123456")
   print(json.dumps(property_data, indent=2)[:500])  # First 500 chars
   ```

2. **Use safe dictionary access:**
   ```python
   address = property_data.get('UnparsedAddress', 'Address not available')
   ```

3. **Check API documentation:**
   - Review field names in `api_docs/` directory
   - Field names may differ from expectations

## Performance Issues

### Issue: Slow API Responses

**Solutions:**
1. **Use pagination effectively:**
   ```python
   # Request smaller pages
   properties = client.properties.search_properties(
       page_size=25,  # Smaller page size
       page_number=0
   )
   ```

2. **Filter requests:**
   ```python
   # Be specific with filters to reduce response size
   properties = client.properties.search_properties(
       city="Salt Lake City",
       property_type="Residential",
       listing_status="Active"
   )
   ```

3. **Cache results when appropriate:**
   ```python
   import time
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_lookup_values(lookup_type):
       return client.lookup.get_lookup_values(lookup_type)
   ```

### Issue: Memory Usage

**Solutions:**
1. **Process data in chunks:**
   ```python
   def process_properties_in_chunks(search_params, chunk_size=50):
       page_number = 0
       while True:
           properties = client.properties.search_properties(
               **search_params,
               page_number=page_number,
               page_size=chunk_size
           )
           
           if not properties:
               break
               
           # Process chunk
           yield properties
           page_number += 1
   ```

2. **Clear large variables:**
   ```python
   large_dataset = client.properties.search_properties(page_size=1000)
   # Process data
   del large_dataset  # Free memory
   ```

## Development Issues

### Issue: Type Checking Errors

**Symptoms:**
```bash
mypy error: Argument has incompatible type
```

**Solutions:**
1. **Import type hints:**
   ```python
   from typing import Optional, Dict, Any, List
   from datetime import date
   
   def search_properties(
       client,
       city: Optional[str] = None,
       min_price: Optional[int] = None
   ) -> List[Dict[str, Any]]:
       return client.properties.search_properties(
           city=city,
           min_list_price=min_price
       )
   ```

2. **Handle union types:**
   ```python
   from wfrmls.lookup import PropertyType  # If enum exists
   
   # Use enum or string
   property_type: Union[PropertyType, str] = "Residential"
   ```

### Issue: Test Failures

**Solutions:**
1. **Mock API responses:**
   ```python
   import responses
   import json
   
   @responses.activate
   def test_property_search():
       responses.add(
           responses.GET,
           "https://api.wfrmls.com/properties",
           json=[{"ListingKey": "123", "City": "Salt Lake City"}],
           status=200
       )
       
       client = WFRMLSClient(api_key="test_key")
       properties = client.properties.search_properties(city="Salt Lake City")
       assert len(properties) == 1
   ```

2. **Use environment variables for tests:**
   ```python
   import os
   import pytest
   
   @pytest.fixture
   def test_client():
       return WFRMLSClient(api_key=os.getenv("TEST_API_KEY", "test_key"))
   ```

## Network and Connectivity

### Issue: SSL Certificate Errors

**Symptoms:**
```python
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solutions:**
1. **Update certificates:**
   ```bash
   pip install --upgrade certifi
   ```

2. **Check system time:**
   - Ensure system clock is accurate
   - SSL certificates are time-sensitive

### Issue: Timeout Errors

**Symptoms:**
```python
requests.exceptions.ReadTimeout: HTTPSConnectionPool
```

**Solutions:**
1. **Increase timeout (for development only):**
   ```python
   # Note: This requires custom timeout handling in client
   # Contact support if timeouts are frequent
   ```

2. **Check network connectivity:**
   ```bash
   ping api.wfrmls.com
   ```

3. **Retry logic:**
   ```python
   import time
   
   def retry_request(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return func()
           except requests.exceptions.Timeout:
               if attempt == max_retries - 1:
                   raise
               time.sleep(2 ** attempt)  # Exponential backoff
   ```

## Getting Additional Help

### Before Seeking Help

1. **Check this troubleshooting guide**
2. **Review the [API Reference](api-reference.md)**
3. **Search [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)**
4. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### Creating a Bug Report

Include the following information:

1. **Environment details:**
   ```python
   import sys
   import wfrmls
   print(f"Python: {sys.version}")
   print(f"WFRMLS: {wfrmls.__version__}")
   print(f"Platform: {sys.platform}")
   ```

2. **Minimal reproduction case:**
   ```python
   from wfrmls import WFRMLSClient
   
   client = WFRMLSClient(api_key="test_key")
   # Minimal code that reproduces the issue
   ```

3. **Complete error message:**
   - Include full traceback
   - Remove sensitive information (API keys, etc.)

4. **Expected vs actual behavior**

### Contact Options

- **GitHub Issues**: For bugs and feature requests
- **Documentation**: Check all documentation files first
- **WFRMLS Support**: For API access and permission issues
- **Community**: Stack Overflow with `wfrmls` tag

### Emergency Workarounds

If you need immediate functionality while waiting for a fix:

1. **Use direct requests:**
   ```python
   import requests
   
   headers = {"Authorization": "Bearer your_token"}
   response = requests.get("https://api.wfrmls.com/endpoint", headers=headers)
   ```

2. **Downgrade to previous version:**
   ```bash
   pip install wfrmls==1.0.0  # Use last working version
   ```

3. **Use alternative endpoints:**
   - Check if similar data is available from other endpoints
   - Some endpoints may have different parameter requirements 