"""Office client for WFRMLS API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class OfficeStatus(Enum):
    """Library constants; these do not validate service lookup values."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"


class OfficeType(Enum):
    """Library constants; these do not validate service lookup values."""

    MAIN = "Main"
    BRANCH = "Branch"
    FRANCHISE = "Franchise"


class OfficeClient(BaseClient):
    """Client for HTTP queries on the Office resource.

    Returns service JSON without schema normalization. Metadata, fields,
    relationships, and permissions are determined by the configured service.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the Office resource client and validate credentials.

        Args:
            bearer_token: Token string, or WFRMLS_BEARER_TOKEN when omitted.
            base_url: Service URL; defaults to the UtahRealEstate.com OData URL.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_offices(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one page from the Office collection.

        Args:
            top: Optional record limit; values above 200 are capped at 200.
            skip: Optional number of records to skip.
            filter_query: OData filter expression, forwarded without schema validation.
            select: Field names as a list or comma-separated string.
            orderby: OData ordering expression.
            expand: Relationship names as a list or comma-separated string.
            count: Send $count=true or $count=false; None omits the option.

        Returns:
            Response dictionary unchanged. Collection responses normally contain
            a value list and may contain OData context, count, and continuation data.
            This method does not follow continuation links or retry requests.

        Raises:
            WFRMLSError: HTTP or network errors, through the BaseClient subclasses.

        Example:
            Set WFRMLS_BEARER_TOKEN before constructing the resource client::

                from wfrmls import WFRMLSClient

                client = WFRMLSClient()
                response = client.office.get_offices(top=10)
                for record in response.get("value", []):
                    print(record)
        """
        params: Dict[str, Any] = {}

        if top is not None:
            # Enforce 200 record limit as per API specification
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

        return self.get("Office", params=params)

    def get_office(self, office_key: str) -> Dict[str, Any]:
        """Request one Office record by key.

        Requests Office('<key>') without collection query options. Keys are
        interpolated directly; escape apostrophes as doubled quotes when needed.

        Args:
            office_key: Record key string.

        Returns:
            The record's response dictionary unchanged, not a collection or None.

        Raises:
            NotFoundError: If the service reports HTTP 404.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get(f"Office('{office_key}')")

    def get_active_offices(self, **kwargs: Any) -> Dict[str, Any]:
        """Request one page of offices with OfficeStatus equal to Active.

        Do not pass filter_query: the helper supplies it and duplicates raise
        TypeError. Use get_offices to build additional compound filters.

        Args:
            **kwargs: Other get_offices collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_offices(filter_query="OfficeStatus eq 'Active'", **kwargs)

    def get_offices_by_city(self, city: str, **kwargs: Any) -> Dict[str, Any]:
        """Request offices filtered by OfficeCity.

        An extra filter_query is appended with and without grouping. Parenthesize
        expressions containing or. Escape apostrophes in city as doubled quotes.

        Args:
            city: City string to match.
            **kwargs: get_offices collection options, including an additional filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        city_filter = f"OfficeCity eq '{city}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{city_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = city_filter

        return self.get_offices(**kwargs)

    def search_offices_by_name(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Request offices using contains(OfficeName, '<name>').

        An extra filter_query is appended with and without grouping. Parenthesize
        expressions containing or. Escape apostrophes in name as doubled quotes.

        Args:
            name: Office-name substring.
            **kwargs: get_offices collection options, including an additional filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        name_filter = f"contains(OfficeName, '{name}')"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{name_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = name_filter

        return self.get_offices(**kwargs)

    def get_offices_with_members(self, **kwargs: Any) -> Dict[str, Any]:
        """Request offices with expand set to Members.

        The relationship name is Members, not Member. Its schema and availability
        are service-defined. Do not pass expand; duplicates raise TypeError.

        Args:
            **kwargs: Other get_offices collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_offices(expand="Members", **kwargs)

    def get_offices_by_zipcode(self, zipcode: str, **kwargs: Any) -> Dict[str, Any]:
        """Request offices filtered by OfficePostalCode.

        An extra filter_query is appended with and without grouping. Use a string
        to retain leading zeros; escape apostrophes as doubled quotes.

        Args:
            zipcode: Postal-code string.
            **kwargs: get_offices collection options, including an additional filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        zipcode_filter = f"OfficePostalCode eq '{zipcode}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{zipcode_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = zipcode_filter

        return self.get_offices(**kwargs)

    def get_modified_offices(
        self, since: Union[str, date], **kwargs: Any
    ) -> Dict[str, Any]:
        """Request records with a ModificationTimestamp after the cutoff.

        Builds ModificationTimestamp gt <timestamp>. Strings pass through unchanged.
        A date becomes YYYY-MM-DDZ; datetime serialization appends Z to
        isoformat(), so aware datetimes can include both an offset and Z. Prefer
        an explicit UTC string such as 2026-01-01T00:00:00Z. The service determines
        accepted temporal literal syntax; use the collection method's filter_query
        for a different expression. Do not also pass filter_query here; duplicate
        keywords raise TypeError.

        Args:
            since: ISO UTC string or date.
            **kwargs: Other get_offices collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            since_str = since

        filter_query = f"ModificationTimestamp gt {since_str}"
        return self.get_offices(filter_query=filter_query, **kwargs)
