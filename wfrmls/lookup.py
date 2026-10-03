"""Lookup client for WFRMLS API."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class LookupClient(BaseClient):
    """Client for HTTP queries on the Lookup resource.

    Returns service JSON without schema normalization. Metadata, fields,
    relationships, and permissions are determined by the configured service.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the Lookup resource client and validate credentials.

        Args:
            bearer_token: Token string, or WFRMLS_BEARER_TOKEN when omitted.
            base_url: Service URL; defaults to the UtahRealEstate.com OData URL.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_lookups(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one page from the Lookup collection.

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
                response = client.lookup.get_lookups(top=10)
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

        return self.get("Lookup", params=params)

    def get_lookup(self, lookup_key: str) -> Dict[str, Any]:
        """Request one Lookup record by key.

        Requests Lookup('<key>') without collection query options. Keys are
        interpolated directly; escape apostrophes as doubled quotes when needed.

        Args:
            lookup_key: Record key string.

        Returns:
            The record's response dictionary unchanged, not a collection or None.

        Raises:
            NotFoundError: If the service reports HTTP 404.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get(f"Lookup('{lookup_key}')")

    def get_lookups_by_name(self, lookup_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Request lookups filtered by LookupName.

        An extra filter_query is appended with and without grouping. Parenthesize
        expressions containing or; escape apostrophes in lookup names as doubled quotes.

        Args:
            lookup_name: Service lookup category string.
            **kwargs: get_lookups collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        name_filter = f"LookupName eq '{lookup_name}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{name_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = name_filter

        return self.get_lookups(**kwargs)

    def get_property_type_lookups(self, **kwargs: Any) -> Dict[str, Any]:
        """Request lookups with LookupName equal to PropertyType.

        Calls get_lookups_by_name with the literal PropertyType category.
        The service determines whether the category and its values are available.

        Args:
            **kwargs: get_lookups collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_lookups_by_name("PropertyType", **kwargs)

    def get_property_status_lookups(self, **kwargs: Any) -> Dict[str, Any]:
        """Request lookups with LookupName equal to PropertyStatus.

        The literal category is PropertyStatus, not StandardStatus or MlsStatus.
        Use get_lookups_by_name for another service-defined status category.

        Args:
            **kwargs: get_lookups collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_lookups_by_name("PropertyStatus", **kwargs)

    def get_standard_lookups(self, **kwargs: Any) -> Dict[str, Any]:
        """Request lookups where StandardLookupValue is not null.

        An extra filter_query is appended with and. This filter does not verify
        standards compliance or completeness of the returned category values.

        Args:
            **kwargs: get_lookups collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        # Filter for lookups that have a StandardLookupValue (RESO standard lookups)
        standard_filter = "StandardLookupValue ne null"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{standard_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = standard_filter

        return self.get_lookups(**kwargs)

    def get_active_lookups(self, **kwargs: Any) -> Dict[str, Any]:
        """Request lookups where IsActive is true.

        An extra filter_query is appended with and. The service must expose the
        IsActive field for this filter to be accepted.

        Args:
            **kwargs: get_lookups collection options, including an extra filter.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        # Filter for active lookups (assuming IsActive field exists)
        active_filter = "IsActive eq true"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{active_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = active_filter

        return self.get_lookups(**kwargs)

    def get_lookup_names(self) -> Dict[str, Any]:
        """Request one collection page of lookup names.

        Calls get_lookups(select=["LookupName"], orderby="LookupName asc"). It does not
        deduplicate names, fetch all pages, or accept pagination arguments.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_lookups(select=["LookupName"], orderby="LookupName asc")

    def get_modified_lookups(
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
            **kwargs: Other get_lookups collection options.

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
        return self.get_lookups(filter_query=filter_query, **kwargs)
