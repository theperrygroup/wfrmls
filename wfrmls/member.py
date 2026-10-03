"""Member client for WFRMLS API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class MemberStatus(Enum):
    """Library constants; these do not validate service lookup values."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"


class MemberType(Enum):
    """Library constants; these do not validate service lookup values."""

    AGENT = "Agent"
    BROKER = "Broker"
    ASSISTANT = "Assistant"


class MemberClient(BaseClient):
    """Client for HTTP queries on the Member resource.

    Returns service JSON without schema normalization. Metadata, fields,
    relationships, and permissions are determined by the configured service.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the Member resource client and validate credentials.

        Args:
            bearer_token: Token string, or WFRMLS_BEARER_TOKEN when omitted.
            base_url: Service URL; defaults to the UtahRealEstate.com OData URL.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_members(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one page from the Member collection.

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
                response = client.member.get_members(top=10)
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

        return self.get("Member", params=params)

    def get_member(self, member_key: str) -> Dict[str, Any]:
        """Request one Member record by key.

        Requests Member('<key>') without collection query options. Keys are
        interpolated directly; escape apostrophes as doubled quotes when needed.

        Args:
            member_key: Record key string.

        Returns:
            The record's response dictionary unchanged, not a collection or None.

        Raises:
            NotFoundError: If the service reports HTTP 404.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get(f"Member('{member_key}')")

    def get_member_by_mls_id(self, mls_id: str) -> Dict[str, Any]:
        """Return the first member matching an MLS ID.

        Requests get_members(filter_query="MemberMlsId eq '<id>'", expand="Office",
        top=1). It does not verify uniqueness or flatten the Office relationship.
        MLS IDs are interpolated directly; escape apostrophes as doubled quotes.

        Args:
            mls_id: MLS ID string to filter on.

        Returns:
            Dictionary copied from the first record in the collection response.

        Raises:
            NotFoundError: If the response has no member records.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        results = self.get_members(
            filter_query=f"MemberMlsId eq '{mls_id}'", expand="Office", top=1
        )

        values = results.get("value", [])
        if not values:
            from .exceptions import NotFoundError

            raise NotFoundError(f"No member found with MLS ID: {mls_id}")

        return dict(values[0])

    def get_active_members(self, **kwargs: Any) -> Dict[str, Any]:
        """Request one page of members with MemberStatus equal to Active.

        Do not pass filter_query: this helper supplies it and a duplicate raises
        TypeError. Use get_members for additional compound filters.

        Args:
            **kwargs: Other get_members collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_members(filter_query="MemberStatus eq 'Active'", **kwargs)

    def get_members_by_office(self, office_key: str, **kwargs: Any) -> Dict[str, Any]:
        """Request members filtered by OfficeKey.

        An additional filter_query is appended with and without grouping.
        Parenthesize expressions containing or. Escape apostrophes in office_key
        as doubled quotes; the helper interpolates the string directly.

        Args:
            office_key: Office key string.
            **kwargs: get_members collection options, including an additional filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        office_filter = f"OfficeKey eq '{office_key}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{office_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = office_filter

        return self.get_members(**kwargs)

    def search_members_by_name(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Search MemberFirstName and MemberLastName with contains expressions.

        Supplied names are combined with and. With neither name supplied, the
        helper calls get_members without adding a name filter. With a name supplied,
        do not also pass filter_query; duplicate keywords raise TypeError. Escape
        apostrophes in names as doubled quotes before passing them.

        Args:
            first_name: Optional first-name substring.
            last_name: Optional last-name substring.
            **kwargs: Other get_members collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        filters = []

        if first_name is not None:
            filters.append(f"contains(MemberFirstName, '{first_name}')")
        if last_name is not None:
            filters.append(f"contains(MemberLastName, '{last_name}')")

        if not filters:
            # No name filters, just get all members
            return self.get_members(**kwargs)

        filter_query = " and ".join(filters)
        return self.get_members(filter_query=filter_query, **kwargs)

    def get_members_with_office(self, **kwargs: Any) -> Dict[str, Any]:
        """Request members with expand set to Office.

        The service determines the relationship schema and availability.
        Do not pass expand in kwargs; duplicate keywords raise TypeError.

        Args:
            **kwargs: Other get_members collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_members(expand="Office", **kwargs)

    def get_modified_members(
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
            **kwargs: Other get_members collection options.

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
        return self.get_members(filter_query=filter_query, **kwargs)
