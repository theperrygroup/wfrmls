"""Accessory dwelling unit query helpers for the WFRMLS client."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class AduType(Enum):
    """ADU type options."""

    DETACHED = "Detached"
    ATTACHED = "Attached"
    GARAGE_CONVERSION = "Garage Conversion"
    BASEMENT = "Basement"
    INTERIOR = "Interior"


class AduStatus(Enum):
    """ADU status options."""

    EXISTING = "Existing"
    PERMITTED = "Permitted"
    PLANNED = "Planned"
    UNDER_CONSTRUCTION = "Under Construction"


class AduClient(BaseClient):
    """Query the Adu resource with optional OData parameters.

    The client returns provider JSON unchanged and does not define an exhaustive
    field schema or verify the resource's current availability. It is available
    through WFRMLSClient.adu, which constructs the service lazily.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize a service client and require credentials immediately.

        Args:
            bearer_token: Token, or None to read WFRMLS_BEARER_TOKEN.
            base_url: API base URL. None uses
                https://resoapi.utahrealestate.com/reso/odata.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_adus(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Query one page of Adu records.

        Query expressions, fields, and relationships are sent to the provider without
        local schema validation. No default $count is sent.

        Args:
            top: Page size; the client sends min(top, 200) when provided.
            skip: Number of records to skip, passed unchanged.
            filter_query: OData filter string, passed unchanged.
            select: Field list or comma-separated string; lists are joined with commas.
            orderby: OData ordering string, passed unchanged.
            expand: Relationship list or string; lists are joined with commas.
            count: True or False sends the corresponding $count value. None omits it.

        Returns:
            The server's JSON dictionary unchanged. Collection responses usually
            contain value; OData metadata is included only when supplied by the server.
            This method neither follows pagination links nor retries requests.

        Raises:
            WFRMLSError: For request failures through the shared HTTP client.

        Example:
            ```python
            from wfrmls import AduStatus, WFRMLSClient

            client = WFRMLSClient()  # Requires WFRMLS_BEARER_TOKEN.
            response = client.adu.get_adus(
                top=25,
                filter_query=f"AduStatus eq '{AduStatus.EXISTING.value}'",
                select=["AduKey", "ListingKey", "AduType", "AduStatus"],
                count=True,
            )
            for record in response.get("value", []):
                print(record.get("AduKey"), record.get("AduType"))
            ```
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

        return self.get("Adu", params=params)

    def get_adu(self, adu_key: str) -> Dict[str, Any]:
        """Request a single record at Adu('<adu_key>').

        Args:
            adu_key: Trusted key string, interpolated without escaping.

        Returns:
            The server's single-record JSON dictionary; no value wrapper is added.

        Raises:
            NotFoundError: For a 404 response.
            WFRMLSError: For other request failures.
        """
        return self.get(f"Adu('{adu_key}')")

    def get_adus_for_property(self, listing_key: str, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with the filter ListingKey eq '<listing_key>'.

        Args:
            listing_key: Trusted listing key string, interpolated without escaping.
            **kwargs: Query options for get_adus. A supplied filter_query
                is appended with and without extra parentheses. Group expressions
                containing or when they should apply together.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        property_filter = f"ListingKey eq '{listing_key}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{property_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = property_filter

        return self.get_adus(**kwargs)

    def get_adus_by_type(self, adu_type: str, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with the filter AduType eq '<adu_type>'.

        Args:
            adu_type: Trusted ADU type string, interpolated without escaping.
            **kwargs: Query options for get_adus. A supplied filter_query
                is appended with and without extra parentheses. Group expressions
                containing or when they should apply together.

        Returns:
            The server response page unchanged, without automatic pagination.

        Pass AduType members as .value; this helper does not unwrap enums.
        """
        type_filter = f"AduType eq '{adu_type}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{type_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = type_filter

        return self.get_adus(**kwargs)

    def get_adus_by_status(self, adu_status: str, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with the filter AduStatus eq '<adu_status>'.

        Args:
            adu_status: Trusted ADU status string, interpolated without escaping.
            **kwargs: Query options for get_adus. A supplied filter_query
                is appended with and without extra parentheses. Group expressions
                containing or when they should apply together.

        Returns:
            The server response page unchanged, without automatic pagination.

        Pass AduStatus members as .value; this helper does not unwrap enums.
        """
        status_filter = f"AduStatus eq '{adu_status}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{status_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = status_filter

        return self.get_adus(**kwargs)

    def get_existing_adus(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one page using AduStatus eq 'Existing'.

        Args:
            **kwargs: Query options for get_adus. An additional filter_query is
                appended with and by get_adus_by_status.

        Returns:
            The server response page unchanged; provider status semantics are not
            validated and subsequent pages are not fetched.
        """
        return self.get_adus_by_status("Existing", **kwargs)

    def get_permitted_adus(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one page using AduStatus eq 'Permitted'.

        Args:
            **kwargs: Query options for get_adus. An additional filter_query is
                appended with and by get_adus_by_status.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_adus_by_status("Permitted", **kwargs)

    def get_adus_with_property(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with expand="Property".

        The provider determines whether the Property relationship is supported.

        Args:
            **kwargs: Query options for get_adus, excluding expand. Passing expand
                also raises TypeError because the helper supplies it explicitly.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_adus(expand="Property", **kwargs)

    def get_modified_adus(
        self, since: Union[str, date, datetime], **kwargs: Any
    ) -> Dict[str, Any]:
        """Query one page of records modified after a cutoff.

        The generated filter is ModificationTimestamp gt '<timestamp>'. String
        inputs are used unchanged. A date becomes YYYY-MM-DDT00:00:00Z; a datetime
        becomes isoformat() + "Z" without time-zone conversion. An aware datetime
        therefore produces an offset-plus-Z combination. Prefer a normalized UTC
        string, as in the example.

        Args:
            since: Cutoff string, date, or datetime.
            **kwargs: Query options for get_adus. Do not pass filter_query:
                the helper supplies it and a duplicate raises TypeError.

        Returns:
            One server response page unchanged, without automatic pagination.

        Example:
            ```python
            from datetime import datetime, timedelta, timezone

            from wfrmls import WFRMLSClient

            client = WFRMLSClient()  # Requires WFRMLS_BEARER_TOKEN.
            cutoff = datetime.now(timezone.utc) - timedelta(days=1)
            cutoff_utc = cutoff.isoformat().replace("+00:00", "Z")
            response = client.adu.get_modified_adus(
                since=cutoff_utc, top=200, orderby="ModificationTimestamp asc"
            )
            print(len(response.get("value", [])))
            ```
        """
        if isinstance(since, datetime):
            since_str = since.isoformat() + "Z"
        elif isinstance(since, date):
            since_str = since.isoformat() + "T00:00:00Z"
        else:
            since_str = since

        filter_query = f"ModificationTimestamp gt '{since_str}'"
        return self.get_adus(filter_query=filter_query, **kwargs)
