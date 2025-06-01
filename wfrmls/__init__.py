"""WFRMLS Python Client.

A comprehensive Python wrapper for the Wasatch Front Regional MLS (WFRMLS) API,
providing easy access to all RESO-certified endpoints.

Example:
    ```python
    from wfrmls import WFRMLSClient
    
    # Initialize client
    client = WFRMLSClient(bearer_token="your_token")
    
    # Get properties
    properties = client.property.get_properties(top=10)
    ```
"""

from .client import WFRMLSClient
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    WFRMLSError,
)
from .properties import PropertyClient, PropertyStatus, PropertyType
from .member import MemberClient, MemberStatus, MemberType
from .office import OfficeClient, OfficeStatus, OfficeType

__version__ = "1.0.0"
__all__ = [
    "WFRMLSClient",
    "PropertyClient",
    "PropertyStatus",
    "PropertyType",
    "MemberClient",
    "MemberStatus",
    "MemberType",
    "OfficeClient",
    "OfficeStatus",
    "OfficeType",
    "WFRMLSError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
] 