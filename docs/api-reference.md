# API Reference

This section will contain the complete API reference for the WFRMLS Python wrapper.

!!! info "Under Development"
    The API reference documentation will be automatically generated from code docstrings when the API implementation is complete. This ensures the documentation stays current with the actual code.

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

## Quick Reference

```python
from wfrmls import WFRMLSClient

# Initialize client
client = WFRMLSClient(bearer_token="your_token")

# Properties
properties = client.property.get_properties(top=10)
property_detail = client.property.get_property("listing_id")

# Members (Agents)
members = client.member.get_members(top=10)
member_detail = client.member.get_member("member_id")

# Offices
offices = client.office.get_offices(top=10)
office_detail = client.office.get_office("office_id")

# Media
media = client.media.get_media(top=10)
property_photos = client.media.get_media_for_property("property_id")
```

## Detailed Documentation

!!! note "Coming Soon"
    Detailed API documentation with all parameters, return types, and examples will be automatically generated from the codebase docstrings.

For now, please refer to:
- [Examples](examples.md) for comprehensive usage examples
- [Quick Start Guide](quickstart.md) for getting started
- The source code docstrings for detailed parameter information

## Error Handling

All API methods use the custom exception hierarchy:

```python
from wfrmls.exceptions import (
    WFRMLSError,
    AuthenticationError, 
    NotFoundError,
    RateLimitError,
    ValidationError
)

try:
    properties = client.property.get_properties()
except AuthenticationError:
    print("Invalid API credentials")
except RateLimitError:
    print("Rate limit exceeded")
except NotFoundError:
    print("Resource not found")
except WFRMLSError as e:
    print(f"General API error: {e}")
``` 