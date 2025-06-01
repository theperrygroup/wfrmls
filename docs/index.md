# WFRMLS Python API Wrapper

A comprehensive Python wrapper for the Wasatch Front Regional MLS (WFRMLS) API, providing easy access to MLS data including properties, agents, offices, media, and more.

## Features

- **Complete API Coverage**: Access to all WFRMLS endpoints including properties, agents, offices, analytics, and more
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Easy Authentication**: Simple API key-based authentication with environment variable support
- **Robust Error Handling**: Custom exceptions with meaningful error messages
- **Full Test Coverage**: 100% test coverage with comprehensive unit and integration tests
- **Modern Python**: Supports Python 3.8+ with modern async/await patterns where applicable

## Quick Start

```python
from wfrmls import WFRMLSClient

# Initialize client (uses WFRMLS_BEARER_TOKEN environment variable)
client = WFRMLSClient()

# Or provide API key directly
client = WFRMLSClient(api_key="your_api_key_here")

# Search properties
properties = client.properties.search_properties(
    city="Salt Lake City",
    property_type="Residential",
    max_list_price=500000
)

# Get property details
property_details = client.properties.get_property("12345")

# Search agents
agents = client.member.search_members(
    first_name="John",
    last_name="Smith"
)
```

## Installation

```bash
pip install wfrmls
```

For development installation:

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
pip install -e ".[dev]"
```

## Documentation Structure

- **[Installation Guide](installation.md)** - Setup and configuration
- **[Quick Start Guide](quickstart.md)** - Get up and running in 5 minutes
- **[API Reference](api-reference.md)** - Complete endpoint documentation
- **[Examples](examples.md)** - Comprehensive usage examples
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Contributing](contributing.md)** - Development guidelines
- **[Changelog](changelog.md)** - Version history and changes
- **[Deployment](deployment.md)** - Production deployment guidance

## Available Endpoints

The WFRMLS Python wrapper provides access to the following endpoint categories:

### Core Data Access
- **Properties**: Search, retrieve, and analyze property listings
- **Members**: Access agent and member information
- **Office**: Office and brokerage data
- **Media**: Property photos, documents, and media files

### Specialized Features
- **Analytics**: Market analytics and reporting data
- **Lookup**: Reference data and lookup tables  
- **History**: Property and listing history
- **Open House**: Open house event information
- **ADU**: Accessory Dwelling Unit data
- **Green Verification**: Green building certifications

### System Information
- **Resource**: API metadata and available resources
- **Data System**: System information and capabilities
- **Property Unit Types**: Property classification data

## Authentication

The WFRMLS API uses Bearer token authentication. Set your API key as an environment variable:

```bash
export WFRMLS_BEARER_TOKEN="your_api_key_here"
```

Or pass it directly when initializing the client:

```python
client = WFRMLSClient(api_key="your_api_key_here")
```

## Support

- **Documentation**: [https://wfrmls.readthedocs.io](https://wfrmls.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)
- **API Documentation**: Available in the `api_docs/` directory

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 