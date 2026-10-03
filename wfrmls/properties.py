"""Property client for WFRMLS API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient
from .exceptions import NotFoundError, ValidationError, WFRMLSError


class PropertyStatus(Enum):
    """Property status options."""

    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"
    EXPIRED = "Expired"
    WITHDRAWN = "Withdrawn"
    CANCELLED = "Cancelled"


class PropertyType(Enum):
    """Property type options."""

    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    LAND = "Land"
    RENTAL = "Rental"


class PropertyClient(BaseClient):
    """Build Property collection queries and numeric-key lookups.

    Collection queries return provider JSON without pagination or schema validation.
    Single-property lookups normalize a wrapped value array to its first object.
    Radius/polygon methods are disabled; address search only extracts a city.
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

    def _normalize_property_response(
        self, response_data: Dict[str, Any], listing_id: str
    ) -> Dict[str, Any]:
        """Normalize single-property lookups to one property dictionary.

        Args:
            response_data: Raw API response from the property lookup endpoint.
            listing_id: Listing ID requested by the caller.

        Returns:
            A single property entity dictionary.

        Raises:
            NotFoundError: If the API returns an empty OData wrapper.
            WFRMLSError: If the API returns an unexpected response shape.
        """
        if "value" not in response_data:
            return response_data

        properties = response_data["value"]
        if not isinstance(properties, list):
            raise WFRMLSError(
                "Unexpected Property lookup response shape: 'value' must be a list."
            )

        if not properties:
            raise NotFoundError(
                f"Resource not found: Property {listing_id} was not found."
            )

        property_record = properties[0]
        if not isinstance(property_record, dict):
            raise WFRMLSError(
                "Unexpected Property lookup response shape: "
                "first 'value' item must be an object."
            )

        return property_record

    def get_properties(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one Property collection page with named OData parameters.

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

        return self.get("Property", params=params)

    def get_property(self, listing_id: str) -> Dict[str, Any]:
        """Retrieve one Property record using a numeric key URL.

        Args:
            listing_id: Numeric string converted with int() for Property(<number>).

        Returns:
            Direct object response, or the first object in a wrapped value array.

        Raises:
            ValidationError: If listing_id is a nonnumeric string.
            NotFoundError: If the provider returns 404 or a wrapped empty array.
            WFRMLSError: For HTTP failures or malformed wrapped response shapes.
        """
        # Ensure listing_id is numeric (API requires numeric keys without quotes)
        try:
            numeric_id = int(listing_id)
        except ValueError:
            raise ValidationError(f"Listing ID must be numeric, got: {listing_id}")

        response_data = self.get(f"Property({numeric_id})")
        return self._normalize_property_response(
            response_data=response_data, listing_id=str(numeric_id)
        )

    def search_properties(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Alias of get_properties with the same explicit OData parameters.

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
        return self.get_properties(
            top=top,
            skip=skip,
            filter_query=filter_query,
            select=select,
            orderby=orderby,
            expand=expand,
            count=count,
        )

    def search_properties_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_miles: float,
        additional_filters: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reject unsupported geospatial radius searches locally.

        Args:
            latitude: Compatibility latitude argument.
            longitude: Compatibility longitude argument.
            radius_miles: Compatibility distance argument.
            additional_filters: Compatibility argument; no filter is sent.
            **kwargs: Compatibility arguments; no request is made.

        Raises:
            ValidationError: Always, before an HTTP request.

        Note:
            Use get_properties_by_city(city, filter_query=...) for supported
            server-side field filtering. This method does not verify current
            provider coordinate fields or calculate geographic matches.
        """
        raise ValidationError(
            "Geospatial radius search is not supported by the WFRMLS API. "
            "Property records do not contain latitude/longitude coordinates. "
            "Use city-based searches like get_properties_by_city() instead."
        )

    def search_properties_by_polygon(
        self,
        polygon_coordinates: List[Dict[str, float]],
        additional_filters: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reject unsupported geospatial polygon searches locally.

        Args:
            polygon_coordinates: Compatibility polygon coordinate argument.
            additional_filters: Compatibility argument; no filter is sent.
            **kwargs: Compatibility arguments; no request is made.

        Raises:
            ValidationError: Always, before an HTTP request.

        Note:
            Use get_properties_by_city(city, filter_query=...) for supported
            server-side field filtering. This method does not verify current
            provider coordinate fields or calculate geographic matches.
        """
        raise ValidationError(
            "Geospatial polygon search is not supported by the WFRMLS API. "
            "Property records do not contain latitude/longitude coordinates. "
            "Use city-based searches like get_properties_by_city() instead."
        )

    def get_properties_with_media(self, **kwargs: Any) -> Dict[str, Any]:
        """Request a Property collection page with $expand=Media.

        Args:
            **kwargs: get_properties parameters, excluding expand.

        Returns:
            Provider JSON from one page; acceptance of Media expansion is server-specific.
        """
        return self.get_properties(expand="Media", **kwargs)

    def get_active_properties(self, **kwargs: Any) -> Dict[str, Any]:
        """Request a Property page filtered by StandardStatus eq 'Active'.

        Args:
            **kwargs: get_properties parameters, excluding filter_query.

        Returns:
            Provider collection JSON. Use get_properties for a combined custom filter.
        """
        return self.get_properties(filter_query="StandardStatus eq 'Active'", **kwargs)

    def get_properties_by_price_range(
        self,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Filter ListPrice by optional inclusive lower and upper bounds.

        Args:
            min_price: Inclusive minimum, or None to omit it.
            max_price: Inclusive maximum, or None to omit it.
            **kwargs: get_properties parameters. Do not supply filter_query when a bound is set.

        Returns:
            Provider JSON from one page. With no bounds, forwards kwargs unchanged.
        """
        filters = []

        if min_price is not None:
            filters.append(f"ListPrice ge {min_price}")
        if max_price is not None:
            filters.append(f"ListPrice le {max_price}")

        if not filters:
            # No price filters, just get all properties
            return self.get_properties(**kwargs)

        filter_query = " and ".join(filters)
        return self.get_properties(filter_query=filter_query, **kwargs)

    def get_properties_by_city(self, city: str, **kwargs: Any) -> Dict[str, Any]:
        """Filter by City and combine an optional filter_query with and.

        Args:
            city: City text inserted without escaping into a quoted OData literal.
            **kwargs: get_properties parameters, including optional filter_query.

        Returns:
            Provider collection JSON. The combined filter adds no grouping parentheses.

        Example:
            ```python
            from wfrmls import WFRMLSClient

            client = WFRMLSClient()
            response = client.property.get_properties_by_city(
                "Salt Lake City", filter_query="StandardStatus eq 'Active'", top=25
            )
            print(len(response.get("value", [])))
            ```
        """
        city_filter = f"City eq '{city}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{city_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = city_filter

        return self.get_properties(**kwargs)

    def get_modified_properties(
        self, since: Union[str, date], **kwargs: Any
    ) -> Dict[str, Any]:
        """Filter ModificationTimestamp with a strict greater-than cutoff.

        Args:
            since: UTC datetime string or date. Strings strip +00:00/trailing Z and append Z.
            **kwargs: get_properties parameters, excluding filter_query.

        Returns:
            Provider collection JSON from one page.

        Note:
            A date becomes date-only text followed by Z. Other timezone offsets are
            not converted to UTC; prefer an explicit normalized UTC datetime string.
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            # Ensure proper Z format (remove +00:00 if present to avoid double timezone)
            since_str = since.replace("+00:00", "").rstrip("Z") + "Z"

        filter_query = f"ModificationTimestamp gt {since_str}"
        return self.get_properties(filter_query=filter_query, **kwargs)

    def get_all_properties_paginated(
        self, page_size: int = 200, max_pages: Optional[int] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Accumulate Property pages with repeated $top and $skip requests.

        Args:
            page_size: Positive page size; values above 200 are clamped to 200.
            max_pages: Positive page limit, or None/0 for no limit.
            **kwargs: get_properties parameters; supplied top and skip are replaced.

        Returns:
            Dictionary with combined value, @odata.context, and pagination_info containing
            pages_fetched, total_records, page_size, and last_skip. A count is copied
            only when present in the last response.

        Note:
            Any request exception stops pagination and returns accumulated records
            without an error marker. Empty or partial results do not prove a complete
            sync. The helper uses offsets, does not follow next links, and keeps all
            records in memory. Use explicit error-checked pages when completeness matters.
        """
        all_results = []
        pages_fetched = 0
        current_skip = 0
        page_size = min(page_size, 200)  # Enforce API limit

        # Store original top parameter
        original_top = kwargs.get("top")

        while True:
            # Set pagination parameters
            kwargs["top"] = page_size
            kwargs["skip"] = current_skip

            # Fetch current page
            try:
                response = self.get_properties(**kwargs)
                pages_fetched += 1

                # Extract results
                page_results = response.get("value", [])
                if not page_results:
                    break  # No more data

                all_results.extend(page_results)

                # Check if we should continue
                if max_pages and pages_fetched >= max_pages:
                    break

                if len(page_results) < page_size:
                    break  # Last page (partial results)

                # Prepare for next page
                current_skip += page_size

            except Exception:
                # If pagination fails, return what we have so far
                break

        # Build combined response
        combined_response = {
            "@odata.context": (
                response.get("@odata.context", "") if "response" in locals() else ""
            ),
            "value": all_results,
            "pagination_info": {
                "pages_fetched": pages_fetched,
                "total_records": len(all_results),
                "page_size": page_size,
                "last_skip": current_skip,
            },
        }

        # Add count if it was in the last response
        if "response" in locals() and "@odata.count" in response:
            combined_response["@odata.count"] = response["@odata.count"]

        return combined_response

    def search_properties_by_multiple_criteria(
        self, criteria: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        """Build a filter from the supported criteria dictionary keys.

        Args:
            criteria: status, min/max_price, city, zip_code, school_district,
                property_type, min/max_bedrooms, min/max_bathrooms, and min/max_sqft.
            **kwargs: get_properties parameters, including optional filter_query.

        Returns:
            Provider JSON from one filtered Property page.

        Note:
            Unknown keys and falsey values, including zero, are ignored. Text values
            are not escaped; filters are joined with and without extra parentheses.
        """
        filters = []

        # Status filter
        if "status" in criteria and criteria["status"]:
            filters.append(f"StandardStatus eq '{criteria['status']}'")

        # Price range filters
        if "min_price" in criteria and criteria["min_price"]:
            filters.append(f"ListPrice ge {criteria['min_price']}")
        if "max_price" in criteria and criteria["max_price"]:
            filters.append(f"ListPrice le {criteria['max_price']}")

        # Location filters
        if "city" in criteria and criteria["city"]:
            filters.append(f"City eq '{criteria['city']}'")
        if "zip_code" in criteria and criteria["zip_code"]:
            filters.append(f"PostalCode eq '{criteria['zip_code']}'")
        if "school_district" in criteria and criteria["school_district"]:
            filters.append(f"SchoolDistrict eq '{criteria['school_district']}'")

        # Property type filter
        if "property_type" in criteria and criteria["property_type"]:
            filters.append(f"PropertyType eq '{criteria['property_type']}'")

        # Bedroom filters
        if "min_bedrooms" in criteria and criteria["min_bedrooms"]:
            filters.append(f"BedroomsTotal ge {criteria['min_bedrooms']}")
        if "max_bedrooms" in criteria and criteria["max_bedrooms"]:
            filters.append(f"BedroomsTotal le {criteria['max_bedrooms']}")

        # Bathroom filters
        if "min_bathrooms" in criteria and criteria["min_bathrooms"]:
            filters.append(f"BathroomsTotalInteger ge {criteria['min_bathrooms']}")
        if "max_bathrooms" in criteria and criteria["max_bathrooms"]:
            filters.append(f"BathroomsTotalInteger le {criteria['max_bathrooms']}")

        # Square footage filters
        if "min_sqft" in criteria and criteria["min_sqft"]:
            filters.append(f"LivingArea ge {criteria['min_sqft']}")
        if "max_sqft" in criteria and criteria["max_sqft"]:
            filters.append(f"LivingArea le {criteria['max_sqft']}")

        # Combine all filters
        if filters:
            filter_query = " and ".join(filters)
            # If additional filter_query provided, combine them
            existing_filter = kwargs.get("filter_query")
            if existing_filter:
                kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
            else:
                kwargs["filter_query"] = filter_query

        return self.get_properties(**kwargs)

    def search_properties_near_address(
        self, address: str, radius_miles: float = 5.0, **kwargs: Any
    ) -> Dict[str, Any]:
        """Extract a city from a comma-delimited address and query that city.

        Args:
            address: Text whose second-to-last comma component is treated as the city.
            radius_miles: Compatibility parameter; no distance calculation is performed.
            **kwargs: get_properties parameters, including optional filter_query.

        Returns:
            Provider collection JSON for the city fallback, or an empty value list
            with an error string if the address has no comma.

        Note:
            This helper does not geocode or perform a radius search. Use
            get_properties_by_city(city, filter_query=...) for an explicit city query.
        """
        # This is a framework method that would need geocoding integration
        # For now, we'll search by address components if the address is structured

        # Basic implementation: try to extract city from address
        address_parts = address.split(",")
        if len(address_parts) >= 2:
            potential_city = address_parts[-2].strip()  # City is usually second to last

            # Search by city as a fallback
            city_filter = f"City eq '{potential_city}'"

            existing_filter = kwargs.get("filter_query")
            if existing_filter:
                kwargs["filter_query"] = f"{city_filter} and {existing_filter}"
            else:
                kwargs["filter_query"] = city_filter

            return self.get_properties(**kwargs)
        else:
            # If address can't be parsed, return empty results
            return {
                "@odata.context": "",
                "value": [],
                "error": "Address could not be parsed. Please provide city coordinates for radius search.",
            }

    def get_luxury_properties(
        self, min_price: float = 1000000, **kwargs: Any
    ) -> Dict[str, Any]:
        """Filter active properties with ListPrice at or above min_price.

        Args:
            min_price: Inclusive price threshold, default 1000000.
            **kwargs: get_properties parameters, including optional filter_query.

        Returns:
            Provider collection JSON from one page; additional filters are joined with and.
        """
        filter_query = f"ListPrice ge {min_price} and StandardStatus eq 'Active'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_properties(**kwargs)

    def get_new_listings(self, days_back: int = 7, **kwargs: Any) -> Dict[str, Any]:
        """Filter OnMarketDate after a UTC date computed from days_back.

        Args:
            days_back: Number of days subtracted from the current UTC datetime, default 7.
            **kwargs: get_properties parameters, including optional filter_query.

        Returns:
            Provider collection JSON from one page. The cutoff is date-only text.
        """
        from datetime import datetime, timedelta, timezone

        # Use timezone-aware datetime to avoid deprecation warning
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        # API expects date-only format (YYYY-MM-DD), not datetime format
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")

        # Use OnMarketDate for when property went on market
        filter_query = f"OnMarketDate gt {cutoff_str}"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_properties(**kwargs)
