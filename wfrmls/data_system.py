"""DataSystem client for WFRMLS API."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class DataSystemClient(BaseClient):
    """Client for HTTP queries on the DataSystem resource.

    Returns service JSON without schema normalization. Metadata, fields,
    relationships, and permissions are determined by the configured service.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the DataSystem resource client and validate credentials.

        Args:
            bearer_token: Token string, or WFRMLS_BEARER_TOKEN when omitted.
            base_url: Service URL; defaults to the UtahRealEstate.com OData URL.

        Raises:
            AuthenticationError: If no token is supplied or found in the environment.
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_data_systems(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one page from the DataSystem collection.

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
                response = client.data_system.get_data_systems(top=10)
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

        return self.get("DataSystem", params=params)

    def get_data_system(self, data_system_key: str) -> Dict[str, Any]:
        """Request one DataSystem record by key.

        Requests DataSystem('<key>') without collection query options. Keys are
        interpolated directly; escape apostrophes as doubled quotes when needed.

        Args:
            data_system_key: Record key string.

        Returns:
            The record's response dictionary unchanged, not a collection or None.

        Raises:
            NotFoundError: If the service reports HTTP 404.
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get(f"DataSystem('{data_system_key}')")

    def get_system_info(self) -> Dict[str, Any]:
        """Request a DataSystem collection page with top=10.

        Calls get_data_systems(top=10). It does not choose a current system, return
        one record directly, fetch all pages, or perform a health/version check.
        Use get_data_systems for filters, field selection, and other query options.

        Returns:
            Collection response dictionary unchanged, normally containing a value list.

        Raises:
            WFRMLSError: If the HTTP request or network operation fails.
        """
        return self.get_data_systems(top=10)

    def get_modified_data_systems(
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
            **kwargs: Other get_data_systems collection options.

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
        return self.get_data_systems(filter_query=filter_query, **kwargs)
