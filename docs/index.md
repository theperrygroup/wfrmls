# WFRMLS Python Client

A comprehensive Python wrapper for the Wasatch Front Regional MLS (WFRMLS) API, providing easy access to all RESO-certified endpoints for real estate data integration.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Install the client and make your first API call in under 5 minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete method documentation with examples and parameters

    [:octicons-arrow-right-24: View API Docs](api/index.md)

-   :material-code-braces:{ .lg .middle } **Code Examples**

    ---

    Real-world usage examples for common real estate applications

    [:octicons-arrow-right-24: Browse Examples](examples/index.md)

-   :material-book-open-page-variant:{ .lg .middle } **User Guides**

    ---

    Comprehensive guides for advanced features and best practices

    [:octicons-arrow-right-24: Read Guides](guides/index.md)

</div>

---

## 📋 Quick Reference

### Core Components

!!! abstract "Main Client"
    The **`WFRMLSClient`** serves as the main entry point, providing access to all API modules through a unified interface.

!!! abstract "Service Modules"
    - **Property**: Real estate listings and property data
    - **Member**: Real estate agent information
    - **Office**: Brokerage and office details
    - **OpenHouse**: Open house schedules and events
    - **Analytics**: Data insights and market analytics
    - **Lookup**: Reference data and code tables

### Common Patterns

=== ":material-rocket-launch: Basic Operation"

    ```python
    from wfrmls import WFRMLSClient

    # Initialize client
    client = WFRMLSClient(bearer_token="your_token")

    # Get active properties
    properties = client.property.get_properties(
        top=10,
        filter_query="StandardStatus eq 'Active'"
    )
    ```

=== ":material-shield-check: Error Handling"

    ```python
    from wfrmls.exceptions import WFRMLSError, NotFoundError

    try:
        property_data = client.property.get_property("12345678")
    except NotFoundError:
        print("Property not found")
    except WFRMLSError as e:
        print(f"API error: {e}")
    ```

=== ":material-cog: Advanced Configuration"

    ```python
    # Complex queries with filtering and sorting
    properties = client.property.get_properties(
        select=["ListingId", "ListPrice", "StandardStatus"],
        filter_query="ListPrice ge 200000 and ListPrice le 500000",
        orderby="ListPrice desc",
        top=50
    )
    ```

---

## 🔧 Installation

!!! info "Prerequisites"
    - Python 3.8 or higher
    - Valid WFRMLS API bearer token

### Quick Setup

```bash
# Install via pip
pip install wfrmls

# Set up environment variable
export WFRMLS_BEARER_TOKEN="your_bearer_token_here"
```

### First API Call

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()  # Uses environment variable
data = client.property.get_properties(top=5)
print(f"Retrieved {len(data)} properties")
```

---

## 🎯 Key Features

### **🏗️ Core Resources**
Complete access to primary MLS data:

- **[Properties](api/properties.md)** - Residential and commercial listings with full details
- **[Members](api/members.md)** - Real estate agent profiles and contact information
- **[Offices](api/offices.md)** - Brokerage data and office locations
- **[Open Houses](api/openhouses.md)** - Scheduled showings and events

### **🔍 Advanced Queries**
Powerful search and filtering capabilities:

- **[Geolocation Search](guides/geolocation.md)** - Radius and polygon-based property searches
- **[OData Queries](guides/odata-queries.md)** - Complex filtering, sorting, and field selection
- **[Data Synchronization](guides/data-sync.md)** - Incremental updates and change tracking

### **⚡ Developer Experience**
Built for production use:

- **Type Safety**: Full type hints and modern Python practices
- **Error Handling**: Comprehensive exception handling with clear messages
- **Rate Limiting**: Built-in handling for API rate limits and quotas
- **Testing**: 100% test coverage with comprehensive test suite

---

## 🌟 Real-World Applications

### **Property Search Portals**
- Build consumer-facing property search websites
- Implement map-based property discovery
- Create advanced filtering and sorting interfaces

### **Market Analytics Dashboards**
- Track market trends and pricing patterns
- Generate automated market reports
- Monitor inventory levels and days on market

### **CRM Integration**
- Sync agent and office data with customer management systems
- Track open house attendance and lead generation
- Automate client communication workflows

### **Data Warehousing**
- Extract property data for business intelligence
- Maintain synchronized local databases
- Generate custom reports and analytics

---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[RESO Standards](reference/reso-standards.md)** - Industry standards compliance
    - **[Utah Grid System](reference/utah-grid.md)** - Local address conventions
    - **[Field Reference](reference/fields.md)** - Complete data dictionary
    - **[Status Codes](reference/status-codes.md)** - API response reference

---

## 🚀 Quick Start

New to the WFRMLS API? Start here:

1. **[Install the client](getting-started/installation.md)** - Get up and running in minutes
2. **[Configure authentication](getting-started/authentication.md)** - Set up your API credentials
3. **[Try the quick start](getting-started/quickstart.md)** - Make your first API call
4. **[Explore examples](examples/index.md)** - See real-world use cases

---

## 🆘 Support & Community

### Getting Help

- **API Issues**: Contact [UtahRealEstate.com Support](https://vendor.utahrealestate.com)
- **Library Issues**: [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/theperrygroup/wfrmls/discussions)

### Contributing

We welcome contributions! See our **[Contributing Guide](development/contributing.md)** for details on:

- Setting up the development environment
- Running tests and quality checks
- Submitting pull requests
- Following coding standards

### License

This project is licensed under the **MIT License** - see the [license details](legal/license.md) for more information.

---

*Ready to get started? Jump to the [Quick Start Guide](getting-started/quickstart.md) or explore the [API Reference](api/index.md).* 