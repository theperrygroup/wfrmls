"""Main WFRMLS client."""

from builtins import property as property_decorator
from typing import Optional, TYPE_CHECKING

# Use TYPE_CHECKING to avoid import cycles and property conflicts
if TYPE_CHECKING:
    from .properties import PropertyClient
    from .member import MemberClient  
    from .office import OfficeClient


class WFRMLSClient:
    """Main client for WFRMLS API.

    This is the primary entry point for accessing the WFRMLS API. It provides
    access to all available resources through service-specific client properties.
    The client uses lazy initialization to create service clients only when accessed.

    Example:
        ```python
        from wfrmls import WFRMLSClient

        # Initialize with bearer token from environment variable
        client = WFRMLSClient()

        # Or provide bearer token directly
        client = WFRMLSClient(bearer_token="your_bearer_token_here")

        # Use service endpoints
        properties = client.property.get_properties(top=10)
        property_detail = client.property.get_property("12345678")
        
        # Search properties by location
        properties = client.property.search_properties_by_radius(
            latitude=40.7608, longitude=-111.8910, radius_miles=10
        )
        ```
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the client.

        Args:
            bearer_token: Bearer token for authentication. If not provided,
                will attempt to load from WFRMLS_BEARER_TOKEN environment variable.
            base_url: Base URL for the API. Defaults to the production WFRMLS API.

        Raises:
            AuthenticationError: If no bearer token is provided or found in environment.
        """
        self._bearer_token = bearer_token
        self._base_url = base_url
        
        # Service clients - lazily initialized
        self._property: Optional["PropertyClient"] = None
        self._member: Optional["MemberClient"] = None
        self._office: Optional["OfficeClient"] = None

    @property_decorator
    def property(self) -> "PropertyClient":
        """Access to property endpoints.

        Provides access to property listings, search functionality, and property details.
        This is the primary resource for real estate data in the WFRMLS system.

        Returns:
            PropertyClient instance for property operations

        Example:
            ```python
            # Get active properties
            properties = client.property.get_active_properties(top=50)
            
            # Get property with photos
            property_with_media = client.property.get_properties_with_media(
                filter_query="ListingId eq '12345678'"
            )
            ```
        """
        if self._property is None:
            from .properties import PropertyClient
            self._property = PropertyClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property

    @property_decorator
    def member(self) -> "MemberClient":
        """Access to member (agent/broker) endpoints.

        Provides access to real estate agent and broker information,
        including contact details, office affiliations, and licensing data.

        Returns:
            MemberClient instance for member operations

        Example:
            ```python
            # Get active members
            members = client.member.get_active_members(top=50)
            
            # Get member with office info
            member_with_office = client.member.get_members_with_office(
                filter_query="MemberKey eq '12345'"
            )
            ```
        """
        if self._member is None:
            from .member import MemberClient
            self._member = MemberClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._member

    @property_decorator
    def office(self) -> "OfficeClient":
        """Access to office (brokerage) endpoints.

        Provides access to real estate office and brokerage information,
        including contact details, addresses, and licensing information.

        Returns:
            OfficeClient instance for office operations

        Example:
            ```python
            # Get active offices
            offices = client.office.get_active_offices(top=50)
            
            # Get office with members
            office_with_members = client.office.get_offices_with_members(
                filter_query="OfficeKey eq '12345'"
            )
            ```
        """
        if self._office is None:
            from .office import OfficeClient
            self._office = OfficeClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._office 