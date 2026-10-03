"""Main WFRMLS client."""

from builtins import property as property_decorator
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from .exceptions import WFRMLSError

# Use TYPE_CHECKING to avoid import cycles and property conflicts
if TYPE_CHECKING:
    from .adu import AduClient
    from .data_system import DataSystemClient
    from .deleted import DeletedClient
    from .lookup import LookupClient
    from .member import MemberClient
    from .office import OfficeClient
    from .openhouse import OpenHouseClient
    from .properties import PropertyClient
    from .property_unit_types import PropertyUnitTypesClient
    from .resource import ResourceClient


class WFRMLSClient:
    """Facade for lazy WFRMLS service access and schema discovery.

    Construction stores configuration without making requests or validating
    credentials. Service clients resolve credentials when first accessed and
    are cached independently. The facade does not expose media, history, or green
    attributes; separate exported classes are compatibility interfaces.

    Example:
        Configure WFRMLS_BEARER_TOKEN before the first service access.

        ```python
        from wfrmls import WFRMLSClient

        client = WFRMLSClient()
        listings = client.property.get_properties_by_city(
            "Salt Lake City", filter_query="StandardStatus eq 'Active'", top=10
        )
        print(len(listings.get("value", [])))
        ```
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Store client configuration for later service construction.

        Args:
            bearer_token: Token passed to service clients; None defers to their environment lookup.
            base_url: Service root override; None defers to the service default.

        Note:
            Missing credentials do not raise here. AuthenticationError is raised when
            a service or discovery BaseClient is first constructed without a token.
        """
        self._bearer_token = bearer_token
        self._base_url = base_url

        # Service clients - lazily initialized
        self._property: Optional["PropertyClient"] = None
        self._member: Optional["MemberClient"] = None
        self._office: Optional["OfficeClient"] = None
        self._openhouse: Optional["OpenHouseClient"] = None
        self._data_system: Optional["DataSystemClient"] = None
        self._resource: Optional["ResourceClient"] = None
        self._property_unit_types: Optional["PropertyUnitTypesClient"] = None
        self._lookup: Optional["LookupClient"] = None
        self._adu: Optional["AduClient"] = None
        self._deleted: Optional["DeletedClient"] = None

        # Base client for service discovery - lazily initialized
        self._base_client: Optional[Any] = None

    def _get_base_client(self) -> Any:
        """Get base client instance for service discovery."""
        if self._base_client is None:
            from .base_client import BaseClient

            self._base_client = BaseClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._base_client

    @property_decorator
    def bearer_token(self) -> Optional[str]:
        """Return the explicitly configured token, possibly None.

        This does not resolve or expose the environment token used by service clients.
        """
        return self._bearer_token

    @property_decorator
    def base_url(self) -> Optional[str]:
        """Return the explicitly configured service root, possibly None.

        A None value does not mean a constructed service lacks its default root.
        """
        return self._base_url

    def get_service_document(self) -> Dict[str, Any]:
        """Retrieve the service-root JSON document with one GET request.

        Returns:
            Parsed provider JSON, commonly containing a value list of entity sets.

        Raises:
            AuthenticationError: If the discovery client has no configured token.
            WFRMLSError: For shared HTTP or transport failures.

        Note:
            Entity-set discovery does not verify every field, query, or permission.
        """
        from typing import cast

        base_client = self._get_base_client()
        result = base_client.get("")  # Root endpoint returns service document
        return cast(Dict[str, Any], result)

    def get_metadata(self) -> str:
        """Return the raw XML metadata string from /$metadata.

        Returns:
            Response text for a 200 response; no XML parsing is performed.

        Raises:
            AuthenticationError: If the discovery client has no configured token.
            WFRMLSError: For any non-200 HTTP status, without shared response attributes.
            requests.exceptions.RequestException: For the direct metadata transport call.

        Note:
            This direct request has a 30-second timeout and does not use BaseClient's
            JSON response handler or exception mapping.
        """
        base_client = self._get_base_client()
        # For metadata, we need to handle the raw response since it's XML
        url = f"{base_client.base_url}/$metadata"
        headers = {
            "Authorization": f"Bearer {base_client.bearer_token}",
            "Accept": "application/xml",
        }
        response = base_client.session.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            raise WFRMLSError(f"Failed to fetch metadata: {response.status_code}")

        return cast(str, response.text)

    @property_decorator
    def property(self) -> "PropertyClient":
        """Access the cached client for property collection queries and numeric-key lookups.

        Returns:
            A PropertyClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._property is None:
            from .properties import PropertyClient

            self._property = PropertyClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property

    @property_decorator
    def member(self) -> "MemberClient":
        """Access the cached client for member collection queries and key lookups.

        Returns:
            A MemberClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._member is None:
            from .member import MemberClient

            self._member = MemberClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._member

    @property_decorator
    def office(self) -> "OfficeClient":
        """Access the cached client for office collection queries and key lookups.

        Returns:
            An OfficeClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._office is None:
            from .office import OfficeClient

            self._office = OfficeClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._office

    @property_decorator
    def openhouse(self) -> "OpenHouseClient":
        """Access the cached client for open-house collection and date queries.

        Returns:
            An OpenHouseClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._openhouse is None:
            from .openhouse import OpenHouseClient

            self._openhouse = OpenHouseClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._openhouse

    @property_decorator
    def open_house(self) -> "OpenHouseClient":
        """Return the same cached OpenHouseClient as openhouse.

        This is a compatibility alias, not a separate HTTP client.
        """
        return self.openhouse

    @property_decorator
    def data_system(self) -> "DataSystemClient":
        """Access the cached client for data-system collection queries.

        Returns:
            A DataSystemClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._data_system is None:
            from .data_system import DataSystemClient

            self._data_system = DataSystemClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._data_system

    @property_decorator
    def resource(self) -> "ResourceClient":
        """Access the cached client for resource metadata collection queries.

        Returns:
            A ResourceClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._resource is None:
            from .resource import ResourceClient

            self._resource = ResourceClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._resource

    @property_decorator
    def property_unit_types(self) -> "PropertyUnitTypesClient":
        """Access the cached client for property unit-record queries.

        Returns:
            A PropertyUnitTypesClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._property_unit_types is None:
            from .property_unit_types import PropertyUnitTypesClient

            self._property_unit_types = PropertyUnitTypesClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property_unit_types

    @property_decorator
    def lookup(self) -> "LookupClient":
        """Access the cached client for lookup collections and field-name discovery.

        Returns:
            A LookupClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._lookup is None:
            from .lookup import LookupClient

            self._lookup = LookupClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._lookup

    @property_decorator
    def adu(self) -> "AduClient":
        """Access the cached client for accessory dwelling unit queries.

        Returns:
            A AduClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._adu is None:
            from .adu import AduClient

            self._adu = AduClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._adu

    @property_decorator
    def deleted(self) -> "DeletedClient":
        """Access the cached client for deleted-record queries and sync helpers.

        Returns:
            A DeletedClient, created only on first access.

        Raises:
            AuthenticationError: If the service is first accessed without credentials.
        """
        if self._deleted is None:
            from .deleted import DeletedClient

            self._deleted = DeletedClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._deleted
