"""WFRMLS Python API wrapper.

Set WFRMLS_BEARER_TOKEN before making requests. The main client exposes
implemented listing, directory, metadata, and deletion service clients.
MediaClient, HistoryTransactionalClient, and GreenVerificationClient remain
standalone exports; WFRMLSClient has no media, history, or green attributes.
Provider availability for those compatibility resources is not verified here.

Example:
    ```python
    from wfrmls import WFRMLSClient

    client = WFRMLSClient()
    response = client.property.get_properties(top=10)
    for listing in response.get("value", []):
        print(listing.get("ListingId"), listing.get("ListPrice"))
    ```
"""

from .adu import AduClient, AduStatus, AduType
from .analytics import WFRMLSAnalytics
from .client import WFRMLSClient
from .data_system import DataSystemClient
from .deleted import DeletedClient, ResourceName
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    WFRMLSError,
)
from .green_verification import GreenVerificationClient, GreenVerificationType
from .history import HistoryStatus, HistoryTransactionalClient, HistoryTransactionType
from .lookup import LookupClient
from .media import MediaCategory, MediaClient, MediaType
from .member import MemberClient, MemberStatus, MemberType
from .office import OfficeClient, OfficeStatus, OfficeType
from .openhouse import (
    OpenHouseAttendedBy,
    OpenHouseClient,
    OpenHouseStatus,
    OpenHouseType,
)
from .properties import PropertyClient, PropertyStatus, PropertyType
from .property_unit_types import PropertyUnitTypesClient
from .resource import ResourceClient

__version__ = "1.3.10"
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
    "OpenHouseClient",
    "OpenHouseStatus",
    "OpenHouseType",
    "OpenHouseAttendedBy",
    "MediaClient",
    "MediaType",
    "MediaCategory",
    "HistoryTransactionalClient",
    "HistoryTransactionType",
    "HistoryStatus",
    "GreenVerificationClient",
    "GreenVerificationType",
    "WFRMLSError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "DataSystemClient",
    "ResourceClient",
    "PropertyUnitTypesClient",
    "LookupClient",
    "AduClient",
    "AduType",
    "AduStatus",
    "DeletedClient",
    "ResourceName",
    "WFRMLSAnalytics",
]
