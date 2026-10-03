"""HistoryTransactional client for WFRMLS API."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class HistoryTransactionType(Enum):
    """History transaction type options."""

    SALE = "Sale"
    LEASE = "Lease"
    RENTAL = "Rental"
    AUCTION = "Auction"


class HistoryStatus(Enum):
    """History status options."""

    CLOSED = "Closed"
    SOLD = "Sold"
    LEASED = "Leased"
    EXPIRED = "Expired"
    WITHDRAWN = "Withdrawn"


class HistoryTransactionalClient(BaseClient):
    """Standalone compatibility interface for HistoryTransactional requests.

    WFRMLSClient has no history attribute. Exported methods and mocked tests
    establish request behavior, not current provider availability or permissions.
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

    def get_history_transactions(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Request one HistoryTransactional page with named OData parameters.

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

        return self.get("HistoryTransactional", params=params)

    def get_history_transaction(self, transaction_key: str) -> Dict[str, Any]:
        """Request HistoryTransactional('<key>') without response normalization.

        Args:
            transaction_key: String inserted without escaping into a quoted key URL.

        Returns:
            Handled provider JSON.
        """
        return self.get(f"HistoryTransactional('{transaction_key}')")

    def get_transactions_for_property(
        self, listing_key: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Filter a history collection by quoted ListingKey.

        Args:
            listing_key: String inserted without escaping into a quoted literal.
            **kwargs: get_history_transactions parameters, including optional filter_query.

        Returns:
            Provider collection JSON; additional filters are joined with and.
        """
        property_filter = f"ListingKey eq '{listing_key}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{property_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = property_filter

        return self.get_history_transactions(**kwargs)

    def get_sales_by_price_range(
        self,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Filter Sale transactions by optional inclusive ClosePrice bounds.

        Args:
            min_price: Inclusive minimum, default None.
            max_price: Inclusive maximum, default None.
            **kwargs: Collection parameters, including optional filter_query.

        Returns:
            Provider JSON from one page; combines an existing filter with and.
        """
        filters = ["TransactionType eq 'Sale'"]

        if min_price is not None:
            filters.append(f"ClosePrice ge {min_price}")
        if max_price is not None:
            filters.append(f"ClosePrice le {max_price}")

        price_filter = " and ".join(filters)

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{price_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = price_filter

        return self.get_history_transactions(**kwargs)

    def get_sales_by_date_range(
        self,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Filter Sale transactions by inclusive quoted CloseDate bounds.

        Args:
            start_date: String or date/datetime serialized with isoformat().
            end_date: String or date/datetime serialized with isoformat().
            **kwargs: Collection parameters, including optional filter_query.

        Returns:
            Provider JSON from one page; no timezone conversion or date validation occurs.
        """
        # Convert dates to ISO format
        if isinstance(start_date, (date, datetime)):
            start_str = start_date.isoformat()
        else:
            start_str = start_date

        if isinstance(end_date, (date, datetime)):
            end_str = end_date.isoformat()
        else:
            end_str = end_date

        date_filter = f"TransactionType eq 'Sale' and CloseDate ge '{start_str}' and CloseDate le '{end_str}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{date_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = date_filter

        return self.get_history_transactions(**kwargs)

    def get_recent_sales(self, days_back: int = 30, **kwargs: Any) -> Dict[str, Any]:
        """Filter Sale transactions since a local naive datetime cutoff.

        Args:
            days_back: Number of days subtracted from datetime.now(), default 30.
            **kwargs: Collection parameters, including optional filter_query.

        Returns:
            Provider JSON from one page; this does not retrieve all sales or use UTC.
        """
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days_back)
        cutoff_str = cutoff_date.isoformat()

        recent_filter = f"TransactionType eq 'Sale' and CloseDate ge '{cutoff_str}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{recent_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = recent_filter

        return self.get_history_transactions(**kwargs)

    def get_transactions_by_city(self, city: str, **kwargs: Any) -> Dict[str, Any]:
        """Filter City and combine optional filter_query with and.

        Args:
            city: City text interpolated without escaping into a quoted literal.
            **kwargs: Collection parameters, including optional filter_query.

        Returns:
            Provider collection JSON from one page.
        """
        city_filter = f"City eq '{city}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{city_filter} and {existing_filter}"
        else:
            kwargs["filter_query"] = city_filter

        return self.get_history_transactions(**kwargs)

    def get_closed_transactions(self, **kwargs: Any) -> Dict[str, Any]:
        """Filter Status eq 'Closed' on a history collection page.

        Args:
            **kwargs: Collection parameters, excluding filter_query.

        Returns:
            Provider JSON; use the collection method for a combined custom filter.
        """
        return self.get_history_transactions(
            filter_query="Status eq 'Closed'", **kwargs
        )

    def get_transactions_with_property(self, **kwargs: Any) -> Dict[str, Any]:
        """Query history with $expand=Property.

        Args:
            **kwargs: Collection parameters, excluding expand.

        Returns:
            Provider JSON if the server accepts the relationship.
        """
        return self.get_history_transactions(expand="Property", **kwargs)

    def get_modified_transactions(
        self, since: Union[str, date, datetime], **kwargs: Any
    ) -> Dict[str, Any]:
        """Filter ModificationTimestamp after a quoted cutoff.

        Args:
            since: String sent unchanged; date becomes midnight Z; datetime becomes
                isoformat() plus Z without converting its timezone.
            **kwargs: Collection parameters, excluding filter_query.

        Returns:
            Provider JSON from one page. Prefer a normalized UTC string.
        """
        if isinstance(since, datetime):
            since_str = since.isoformat() + "Z"
        elif isinstance(since, date):
            since_str = since.isoformat() + "T00:00:00Z"
        else:
            since_str = since

        filter_query = f"ModificationTimestamp gt '{since_str}'"
        return self.get_history_transactions(filter_query=filter_query, **kwargs)
