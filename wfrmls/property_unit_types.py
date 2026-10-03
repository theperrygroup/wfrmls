"""PropertyUnitTypes query helpers for the WFRMLS client."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class PropertyUnitTypesClient(BaseClient):
    """Query the PropertyUnitTypes resource with optional OData parameters.

    The client preserves provider JSON. It does not establish unit classifications,
    rental fields, or the complete provider schema. Access it through the lazy
    WFRMLSClient.property_unit_types service property or construct it directly.
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

    def get_property_unit_types(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Query one page of PropertyUnitTypes records.

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
            from wfrmls import WFRMLSClient

            client = WFRMLSClient()  # Requires WFRMLS_BEARER_TOKEN.
            response = client.property_unit_types.get_property_unit_types(
                top=25,
                filter_query="ListingKey eq '1611952'",
                select=["UnitTypeKey", "ListingKey", "UnitType"],
                count=True,
            )
            for record in response.get("value", []):
                print(record.get("UnitTypeKey"), record.get("UnitType"))
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

        return self.get("PropertyUnitTypes", params=params)

    def get_property_unit_type(self, unit_type_key: str) -> Dict[str, Any]:
        """Request a single record at PropertyUnitTypes('<unit_type_key>').

        Args:
            unit_type_key: Trusted key string, interpolated without escaping.

        Returns:
            The server's single-record JSON dictionary; no value wrapper is added.

        Raises:
            NotFoundError: For a 404 response.
            WFRMLSError: For other request failures.
        """
        return self.get(f"PropertyUnitTypes('{unit_type_key}')")

    def get_unit_types_for_property(
        self, listing_key: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Query one page with the filter ListingKey eq '<listing_key>'.

        Args:
            listing_key: Trusted listing key string, interpolated without escaping.
            **kwargs: Query options for get_property_unit_types. A supplied filter_query
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

        return self.get_property_unit_types(**kwargs)

    def get_unit_types_by_type(self, unit_type: str, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with the filter UnitType eq '<unit_type>'.

        Args:
            unit_type: Trusted unit type string, interpolated without escaping.
            **kwargs: Query options for get_property_unit_types. A supplied filter_query
                is appended with and without extra parentheses. Group expressions
                containing or when they should apply together.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        type_filter = f"UnitType eq '{unit_type}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{type_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = type_filter

        return self.get_property_unit_types(**kwargs)

    def get_residential_unit_types(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one page using a fixed list of unit-type filters.

        The parenthesized or expression includes Condo, Townhome, Apartment,
        Single Family, Duplex, Triplex, and Fourplex. It is not a provider-validated
        classification of all residential records.

        Args:
            **kwargs: Query options for get_property_unit_types. An additional
                filter_query is appended with and without grouping that expression.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        # Common residential unit type filters
        residential_types = [
            "UnitType eq 'Condo'",
            "UnitType eq 'Townhome'",
            "UnitType eq 'Apartment'",
            "UnitType eq 'Single Family'",
            "UnitType eq 'Duplex'",
            "UnitType eq 'Triplex'",
            "UnitType eq 'Fourplex'",
        ]

        residential_filter = " or ".join(residential_types)
        residential_filter = f"({residential_filter})"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{residential_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = residential_filter

        return self.get_property_unit_types(**kwargs)

    def get_unit_types_with_properties(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one page with expand="Properties".

        The provider determines whether the Properties relationship is supported.

        Args:
            **kwargs: Query options for get_property_unit_types, excluding expand.
                Passing expand also raises TypeError because the helper supplies it.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_property_unit_types(expand="Properties", **kwargs)

    def get_modified_unit_types(
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
            **kwargs: Query options for get_property_unit_types. Do not pass filter_query:
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
            response = client.property_unit_types.get_modified_unit_types(
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
        return self.get_property_unit_types(filter_query=filter_query, **kwargs)
