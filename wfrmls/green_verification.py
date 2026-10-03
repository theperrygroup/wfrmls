"""PropertyGreenVerification client for WFRMLS API."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class GreenVerificationType(Enum):
    """Green verification type options."""

    ENERGY_STAR = "Energy Star"
    LEED = "LEED"
    GREEN_BUILDING = "Green Building"
    HERS = "HERS"
    OTHER = "Other"


class GreenVerificationClient(BaseClient):
    """Standalone compatibility interface for PropertyGreenVerification requests.

    WFRMLSClient has no green attribute. Exported methods and mocked tests do
    not establish current provider availability or access permissions.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize a service client and resolve its credentials.

        Args:
            bearer_token: Explicit token, or None to use WFRMLS_BEARER_TOKEN.
            base_url: OData service root, or None for the package default.

        Raises:
            AuthenticationError: If neither an explicit nor environment token exists.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_green_verifications(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one PropertyGreenVerification page with named OData parameters.

        Args:
            top: Optional $top; values above 200 are clamped to 200.
            skip: Optional $skip offset, passed unchanged.
            filter_query: Optional raw $filter expression.
            select: Optional field list or comma-separated $select string.
            orderby: Optional raw $orderby expression.
            expand: Optional relationship list or comma-separated $expand string.
            count: Optional $count, converted to lowercase true or false.

        Returns:
            Parsed JSON dictionary from one request, commonly containing value.
            Counts, next links, and individual fields are server-provided and optional.

        Raises:
            WFRMLSError: For shared HTTP or transport failures.
        """
        params: Dict[str, Any] = {}

        if top is not None:
            params["$top"] = min(top, 200)
        if skip is not None:
            params["$skip"] = skip
        if filter_query is not None:
            params["$filter"] = filter_query
        if orderby is not None:
            params["$orderby"] = orderby
        if count is not None:
            params["$count"] = "true" if count else "false"

        if select is not None:
            if isinstance(select, list):
                params["$select"] = ",".join(select)
            else:
                params["$select"] = select

        if expand is not None:
            if isinstance(expand, list):
                params["$expand"] = ",".join(expand)
            else:
                params["$expand"] = expand

        return self.get("PropertyGreenVerification", params=params)

    def get_green_verification(self, verification_key: str) -> Dict[str, Any]:
        """Request PropertyGreenVerification('<key>') without normalization.

        Args:
            verification_key: String inserted without escaping into a quoted key URL.

        Returns:
            Handled provider JSON.
        """
        return self.get(f"PropertyGreenVerification('{verification_key}')")

    def get_verifications_for_property(
        self, listing_key: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Filter green-verification records by quoted ListingKey.

        Args:
            listing_key: Text inserted without escaping into a quoted literal.
            **kwargs: Collection parameters, including optional filter_query.

        Returns:
            Provider collection JSON; an existing filter is joined with and.
        """
        property_filter = f"ListingKey eq '{listing_key}'"

        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{property_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = property_filter

        return self.get_green_verifications(**kwargs)
