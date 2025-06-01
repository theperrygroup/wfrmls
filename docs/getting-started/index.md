# Getting Started

Get up and running with the WFRMLS Python client in minutes. This guide will walk you through installation, authentication, and making your first API calls.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install the Python client and set up your development environment

    [:octicons-arrow-right-24: Install Now](installation.md)

-   :material-key:{ .lg .middle } **Authentication**

    ---

    Configure your API credentials and authentication settings

    [:octicons-arrow-right-24: Set Up Auth](authentication.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Make your first API call and explore basic functionality

    [:octicons-arrow-right-24: Start Tutorial](quickstart.md)

</div>

---

## 📋 Prerequisites

Before you begin, ensure you have:

!!! note "Requirements"
    - **Python 3.8+** - The client requires Python 3.8 or higher
    - **WFRMLS API Access** - Valid bearer token from the vendor dashboard
    - **Internet Connection** - For API requests and package installation

### Getting API Access

To use the WFRMLS API, you need:

1. **Account Setup**: Register at the [Vendor Dashboard](https://vendor.utahrealestate.com)
2. **API Token**: Generate your bearer token from the Service Details section
3. **Rate Limits**: Understand your account's rate limits and usage quotas

---

## ⚡ Quick Setup (2 Minutes)

=== ":material-auto-fix: Automatic Setup"

    ```bash
    # Install the client
    pip install wfrmls
    
    # Set environment variable (recommended)
    export WFRMLS_BEARER_TOKEN="your_bearer_token_here"
    
    # Test the installation
    python -c "from wfrmls import WFRMLSClient; print('✅ Installation successful!')"
    ```

=== ":material-cog: Manual Configuration"

    ```python
    from wfrmls import WFRMLSClient
    
    # Initialize with explicit token
    client = WFRMLSClient(bearer_token="your_bearer_token_here")
    
    # Test the connection
    try:
        data = client.property.get_properties(top=1)
        print(f"✅ Connected! Retrieved {len(data)} property")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    ```

---

## 🎯 What You'll Learn

### **🔧 Setup & Configuration**
- Installing the Python package
- Setting up authentication credentials
- Configuring environment variables
- Testing your connection

### **📖 Basic Usage**
- Creating your first client instance
- Making simple API requests
- Handling responses and errors
- Understanding pagination

### **🚀 Next Steps**
- Exploring advanced features
- Working with different data types
- Building real applications
- Following best practices

---

## 🏗️ Learning Path

Follow this recommended path to master the WFRMLS client:

### **1. Foundation (5 minutes)**
1. **[Install the client](installation.md)** - Get the package installed
2. **[Set up authentication](authentication.md)** - Configure your credentials
3. **[Test your setup](quickstart.md#testing-your-installation)** - Verify everything works

### **2. Basic Usage (10 minutes)**
1. **[Make your first request](quickstart.md#your-first-api-call)** - Get property data
2. **[Handle responses](quickstart.md#understanding-responses)** - Work with returned data
3. **[Try different endpoints](quickstart.md#exploring-other-endpoints)** - Members, offices, open houses

### **3. Practical Application (15 minutes)**
1. **[Property search](../guides/property-search.md)** - Build a property finder
2. **[Error handling](../guides/error-handling.md)** - Handle API errors gracefully
3. **[Rate limits](../guides/rate-limits.md)** - Manage API quotas

---

## 💡 Key Concepts

### **Client Architecture**
The WFRMLS client follows a modular design:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Each service has its own module
properties = client.property.get_properties()    # Properties
members = client.member.get_members()            # Real estate agents
offices = client.office.get_offices()           # Brokerages
open_houses = client.openhouse.get_open_houses() # Open houses
```

### **Response Format**
All API responses follow a consistent structure:

```python
# Typical response format
{
    "@odata.context": "...",
    "@odata.count": 1234,
    "value": [
        {
            "ListingId": "12345678",
            "ListPrice": 450000,
            "StandardStatus": "Active",
            # ... more fields
        }
    ]
}
```

### **Error Handling**
The client provides specific exception types:

```python
from wfrmls.exceptions import (
    AuthenticationError,
    NotFoundError, 
    RateLimitError,
    ValidationError
)
```

---

## 🔍 Quick Troubleshooting

### Common Issues

??? question "Import Error: 'No module named wfrmls'"
    **Solution**: Install the package with `pip install wfrmls`
    
    ```bash
    # Verify installation
    pip show wfrmls
    
    # Reinstall if needed
    pip uninstall wfrmls
    pip install wfrmls
    ```

??? question "Authentication Error: 'Invalid bearer token'"
    **Solution**: Check your token configuration
    
    ```python
    # Verify your token is set correctly
    import os
    print(f"Token set: {'WFRMLS_BEARER_TOKEN' in os.environ}")
    
    # Or pass explicitly
    client = WFRMLSClient(bearer_token="your_actual_token")
    ```

??? question "Rate Limit Error: 'Too many requests'"
    **Solution**: Implement proper rate limiting
    
    ```python
    import time
    from wfrmls.exceptions import RateLimitError
    
    try:
        data = client.property.get_properties()
    except RateLimitError:
        time.sleep(60)  # Wait 1 minute
        data = client.property.get_properties()  # Retry
    ```

---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[Installation Guide](installation.md)** - Detailed installation instructions
    - **[Authentication Setup](authentication.md)** - Complete auth configuration
    - **[Quick Start Tutorial](quickstart.md)** - Step-by-step first project
    - **[API Reference](../api/index.md)** - Complete method documentation

---

## 🚀 Ready to Start?

Choose your preferred starting point:

- **Never used the API before?** → [Installation Guide](installation.md)
- **Already have a token?** → [Quick Start Tutorial](quickstart.md)
- **Want to see examples first?** → [Code Examples](../examples/index.md)
- **Need help with auth?** → [Authentication Guide](authentication.md) 