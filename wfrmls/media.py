"""Media client for WFRMLS API."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class MediaType(Enum):
    """Media type options."""

    PHOTO = "Photo"
    VIDEO = "Video"
    DOCUMENT = "Document"
    VIRTUAL_TOUR = "VirtualTour"


class MediaCategory(Enum):
    """Media category options."""

    EXTERIOR = "Exterior"
    INTERIOR = "Interior"
    KITCHEN = "Kitchen"
    BATHROOM = "Bathroom"
    BEDROOM = "Bedroom"
    LIVING_ROOM = "LivingRoom"
    DINING_ROOM = "DiningRoom"
    GARAGE = "Garage"
    YARD = "Yard"
    POOL = "Pool"


class MediaClient(BaseClient):
    """Standalone compatibility interface for Media request construction.

    WFRMLSClient has no media attribute. This exported class requires credentials;
    its existence and mocked tests do not verify current provider availability.
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

    def get_media(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one Media collection page with named OData parameters.

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

        return self.get("Media", params=params)

    def get_media_item(self, media_key: str) -> Dict[str, Any]:
        """Request Media('<key>') and return the handled provider JSON.

        Args:
            media_key: String key inserted without escaping into a quoted key path.

        Returns:
            Parsed provider JSON; no single-record normalization is performed.
        """
        return self.get(f"Media('{media_key}')")

    def get_media_for_property(
        self, listing_key: Union[str, int], **kwargs: Any
    ) -> Dict[str, Any]:
        """Query ResourceRecordKeyNumeric for one property.

        Args:
            listing_key: Numeric string or integer inserted without quotes.
            **kwargs: get_media parameters, including optional filter_query.

        Returns:
            Provider collection JSON from one request; an existing filter is joined with and.
        """
        property_filter = f"ResourceRecordKeyNumeric eq {listing_key}"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{property_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = property_filter

        return self.get_media(**kwargs)

    def get_photos_for_property(
        self, listing_key: Union[str, int], **kwargs: Any
    ) -> Dict[str, Any]:
        """Query ResourceRecordKeyNumeric for one property and MediaType eq 'Photo'.

        Args:
            listing_key: Numeric string or integer inserted without quotes.
            **kwargs: get_media parameters, including optional filter_query.

        Returns:
            Provider collection JSON from one request; an existing filter is joined with and.
        """
        photo_filter = (
            f"ResourceRecordKeyNumeric eq {listing_key} and MediaType eq 'Photo'"
        )

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{photo_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = photo_filter

        return self.get_media(**kwargs)

    def get_primary_photo(
        self, listing_key: Union[str, int]
    ) -> Optional[Dict[str, Any]]:
        """Return the first photo with Order eq 1, or None if value is empty.

        Args:
            listing_key: Numeric property key inserted into ResourceRecordKeyNumeric.

        Returns:
            First object from the one-page photo response, or None.
        """
        response = self.get_photos_for_property(
            listing_key=listing_key, filter_query="Order eq 1", top=1
        )

        value_list: List[Dict[str, Any]] = response.get("value", [])
        if value_list:
            return value_list[0]
        return None

    def get_media_urls_for_property(
        self, listing_key: Union[str, int], media_type: Optional[str] = None
    ) -> List[str]:
        """Extract MediaURL strings from one page of at most 200 media records.

        Args:
            listing_key: Numeric property key inserted into ResourceRecordKeyNumeric.
            media_type: Optional MediaType string, default None for all types.

        Returns:
            List of MediaURL values from a page requested in Order asc order;
            records missing that key are skipped. Values are not validated.
            This does not paginate or download media.
        """
        filter_parts = [f"ResourceRecordKeyNumeric eq {listing_key}"]

        if media_type:
            filter_parts.append(f"MediaType eq '{media_type}'")

        filter_query = " and ".join(filter_parts)

        response = self.get_media(
            filter_query=filter_query,
            select=["MediaURL"],
            orderby="Order asc",
            top=200,  # Get up to the max limit
        )

        urls = []
        for item in response.get("value", []):
            if "MediaURL" in item:
                urls.append(item["MediaURL"])

        return urls

    def get_media_by_category(
        self, listing_key: Union[str, int], category: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Query a numeric property key with an additional MediaCategory condition.

        Args:
            listing_key: Numeric string or integer, interpolated without quotes.
            category: Category text inserted without escaping into a quoted literal.
            **kwargs: get_media parameters, including optional filter_query.

        Returns:
            Provider collection JSON; an existing filter is joined with and.
        """
        category_filter = f"ResourceRecordKeyNumeric eq {listing_key} and MediaCategory eq '{category}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{category_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = category_filter

        return self.get_media(**kwargs)

    def get_media_with_property(self, **kwargs: Any) -> Dict[str, Any]:
        """Query Media with $expand=Property.

        Args:
            **kwargs: get_media parameters, excluding expand.

        Returns:
            Provider collection JSON if the relationship is accepted by the server.
        """
        return self.get_media(expand="Property", **kwargs)

    def get_modified_media(
        self, since: Union[str, date, datetime], **kwargs: Any
    ) -> Dict[str, Any]:
        """Query ModificationTimestamp after a quoted cutoff.

        Args:
            since: String sent unchanged, date expanded to midnight Z, or datetime
                serialized with isoformat() plus Z without timezone conversion.
            **kwargs: get_media parameters, excluding filter_query.

        Returns:
            Provider collection JSON. Prefer an already-normalized UTC string.
        """
        if isinstance(since, datetime):
            since_str = since.isoformat() + "Z"
        elif isinstance(since, date):
            since_str = since.isoformat() + "T00:00:00Z"
        else:
            since_str = since

        filter_query = f"ModificationTimestamp gt '{since_str}'"
        return self.get_media(filter_query=filter_query, **kwargs)
