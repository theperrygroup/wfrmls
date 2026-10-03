"""OpenHouse client for WFRMLS API."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class OpenHouseStatus(Enum):
    """Library constants; these do not validate service lookup values."""

    ACTIVE = "Active"
    ENDED = "Ended"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class OpenHouseType(Enum):
    """Library constants; these do not validate service lookup values."""

    PUBLIC = "Public"
    PRIVATE = "Private"
    BROKER = "Broker"


class OpenHouseAttendedBy(Enum):
    """Library constants; these do not validate service lookup values."""

    AGENT = "Agent"
    OWNER = "Owner"
    NONE = "None"
    LISTING_AGENT = "ListingAgent"
    BUYER_AGENT = "BuyerAgent"


class OpenHouseClient(BaseClient):
    """Client for HTTP queries on the OpenHouse resource.

    Returns service JSON without schema normalization. Metadata, fields,
    relationships, and permissions are determined by the configured service.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the OpenHouse resource client and validate credentials.

        Args:
            bearer_token: Token string, or WFRMLS_BEARER_TOKEN when omitted.
            base_url: Service URL; defaults to the UtahRealEstate.com OData URL.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_open_houses(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one page from the OpenHouse collection.

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
                response = client.openhouse.get_open_houses(top=10)
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

        return self.get("OpenHouse", params=params)

    def get_open_house(self, open_house_key: str) -> Dict[str, Any]:
        """Request one OpenHouse record by key.

        Requests OpenHouse('<key>') without collection query options. Keys are
        interpolated directly; escape apostrophes as doubled quotes when needed.

        Args:
            open_house_key: Record key string.

        Returns:
            The record's response dictionary unchanged, not a collection or None.

        Raises:
            NotFoundError: If the service reports HTTP 404.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get(f"OpenHouse('{open_house_key}')")

    def get_upcoming_open_houses(
        self,
        days_ahead: Optional[int] = 7,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Request open houses on or after the machine's local date.

        Any non-None days_ahead value adds only OpenHouseDate ge <today>. It does
        not impose an upper bound or active-status filter. None suppresses the added
        date condition. An extra filter_query is appended with and. Use
        get_open_houses_by_date_range for a bounded schedule.

        Args:
            days_ahead: Optional integer; its magnitude is not used. Defaults to 7.
            **kwargs: get_open_houses collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        # Remove days_ahead from kwargs if it exists to avoid conflicts
        kwargs.pop("days_ahead", None)

        if days_ahead is not None:
            from datetime import datetime

            start_date = datetime.now().date()
            filter_query = f"OpenHouseDate ge {start_date.isoformat()}"

            # If additional filter_query provided, combine them
            existing_filter = kwargs.get("filter_query")
            if existing_filter:
                kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
            else:
                kwargs["filter_query"] = filter_query

        return self.get_open_houses(**kwargs)

    def get_open_houses_for_property(
        self, listing_key: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Request open houses filtered by ListingKey.

        An extra filter_query is appended with and without grouping. Parenthesize
        expressions containing or; escape apostrophes in keys as doubled quotes.

        Args:
            listing_key: Listing key string.
            **kwargs: get_open_houses collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        property_filter = f"ListingKey eq '{listing_key}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{property_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = property_filter

        return self.get_open_houses(**kwargs)

    def get_open_houses_by_agent(self, agent_key: str, **kwargs: Any) -> Dict[str, Any]:
        """Request open houses filtered by ShowingAgentKey.

        An extra filter_query is appended with and without grouping. Parenthesize
        expressions containing or; escape apostrophes in keys as doubled quotes.

        Args:
            agent_key: Showing-agent key string.
            **kwargs: get_open_houses collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        agent_filter = f"ShowingAgentKey eq '{agent_key}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{agent_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = agent_filter

        return self.get_open_houses(**kwargs)

    def get_active_open_houses(self, **kwargs: Any) -> Dict[str, Any]:
        """Request open houses with OpenHouseStatus equal to Active.

        Do not pass filter_query: the helper supplies it and duplicates raise
        TypeError. Use get_open_houses for additional compound filters.

        Args:
            **kwargs: Other get_open_houses collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_open_houses(
            filter_query="OpenHouseStatus eq 'Active'", **kwargs
        )

    def get_open_houses_with_property(self, **kwargs: Any) -> Dict[str, Any]:
        """Request open houses with expand set to Property.

        Relationship schema and availability are service-defined. Do not pass
        expand in kwargs; duplicate keywords raise TypeError.

        Args:
            **kwargs: Other get_open_houses collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_open_houses(expand="Property", **kwargs)

    def get_modified_open_houses(
        self, since: Union[str, date, datetime], **kwargs: Any
    ) -> Dict[str, Any]:
        """Request records with a ModificationTimestamp after the cutoff.

        Builds ModificationTimestamp gt '<timestamp>'. Strings pass through unchanged.
        A date becomes YYYY-MM-DDT00:00:00Z; datetime serialization appends Z to
        isoformat(), so aware datetimes can include both an offset and Z. Prefer
        an explicit UTC string such as 2026-01-01T00:00:00Z. The service determines
        accepted temporal literal syntax; use the collection method's filter_query
        for a different expression. Do not also pass filter_query here; duplicate
        keywords raise TypeError.

        Args:
            since: ISO UTC string, date, or datetime.
            **kwargs: Other get_open_houses collection options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        if isinstance(since, datetime):
            since_str = since.isoformat() + "Z"
        elif isinstance(since, date):
            since_str = since.isoformat() + "T00:00:00Z"
        else:
            since_str = since

        filter_query = f"ModificationTimestamp gt '{since_str}'"
        return self.get_open_houses(filter_query=filter_query, **kwargs)

    def get_open_houses_by_date_range(
        self,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Request an inclusive OpenHouseDate range.

        Builds OpenHouseDate ge <start> and OpenHouseDate le <end>. Datetime
        objects are reduced to their dates; date objects use ISO dates; strings pass
        through unchanged. Date ordering and string formats are not validated.
        An extra filter_query is appended with and without grouping.

        Args:
            start_date: ISO date string, date, or datetime for the lower bound.
            end_date: ISO date string, date, or datetime for the upper bound.
            **kwargs: get_open_houses collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        if isinstance(start_date, datetime):
            start_str = start_date.date().isoformat()
        elif isinstance(start_date, date):
            start_str = start_date.isoformat()
        else:
            start_str = start_date

        if isinstance(end_date, datetime):
            end_str = end_date.date().isoformat()
        elif isinstance(end_date, date):
            end_str = end_date.isoformat()
        else:
            end_str = end_date

        filter_query = f"OpenHouseDate ge {start_str} and OpenHouseDate le {end_str}"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_open_houses(**kwargs)

    def get_weekend_open_houses(
        self, weeks_ahead: Optional[int] = 2, **kwargs: Any
    ) -> Dict[str, Any]:
        """Request open houses on or after the machine's local date.

        This helper does not restrict results to weekends. weeks_ahead is ignored;
        there is no upper bound or active-status filter. An extra filter_query is
        appended with and. Use get_open_houses_by_date_range for a chosen weekend.

        Args:
            weeks_ahead: Optional integer, currently ignored; defaults to 2.
            **kwargs: get_open_houses collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        from datetime import datetime

        # Calculate the date range for weekends
        start_date = datetime.now().date()

        # For simplicity, we'll get all open houses in the range and let the user filter weekends
        # A more sophisticated implementation would filter by day of week
        filter_query = f"OpenHouseDate ge {start_date.isoformat()}"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_open_houses(**kwargs)
