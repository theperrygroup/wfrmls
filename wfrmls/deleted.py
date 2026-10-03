"""Deletion-record query and page-summary helpers for the WFRMLS client."""

from datetime import date, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class ResourceName(Enum):
    """Filter string constants for deletion records.

    A constant does not verify provider availability of the corresponding resource.
    """

    PROPERTY = "Property"
    MEMBER = "Member"
    OFFICE = "Office"
    OPENHOUSE = "OpenHouse"
    MEDIA = "Media"
    HISTORY_TRANSACTIONAL = "HistoryTransactional"
    PROPERTY_GREEN_VERIFICATION = "PropertyGreenVerification"
    PROPERTY_UNIT_TYPES = "PropertyUnitTypes"
    ADU = "Adu"


class DeletedClient(BaseClient):
    """Read the Deleted resource and summarize returned pages.

    Helpers use ResourceName, ResourceRecordKey, and DeletedDateTime. Provider
    JSON is not renamed or normalized. The client does not remove local records,
    restore deleted records, or implement a complete synchronization workflow.
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

    def get_deleted(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Query one page of Deleted records.

        Query expressions, fields, and relationships are sent to the provider without
        local schema validation. No default $count is sent. Examples and mocked tests
        should not be treated as a guarantee of the current provider schema.

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
            response = client.deleted.get_deleted(
                top=25,
                filter_query="ResourceName eq 'Property'",
                select=["ResourceName", "ResourceRecordKey", "DeletedDateTime"],
                orderby="DeletedDateTime asc",
            )
            for record in response.get("value", []):
                print(record.get("ResourceName"), record.get("ResourceRecordKey"))
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

        return self.get("Deleted", params=params)

    def get_deleted_by_resource(
        self, resource_name: Union[ResourceName, str], **kwargs: Any
    ) -> Dict[str, Any]:
        """Query one page using ResourceName eq '<resource_name>'.

        Args:
            resource_name: ResourceName enum member or trusted string. Enum values
                are unwrapped; strings are interpolated without escaping.
            **kwargs: Query options for get_deleted. A supplied filter_query is
                appended with and without extra parentheses.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        if isinstance(resource_name, ResourceName):
            resource_value = resource_name.value
        else:
            resource_value = resource_name

        filter_query = f"ResourceName eq '{resource_value}'"

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_deleted(**kwargs)

    def get_deleted_since(
        self,
        since: Union[str, date],
        resource_name: Optional[Union[ResourceName, str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Query one page deleted after a cutoff, optionally for one resource.

        The filter is DeletedDateTime gt <timestamp>, without timestamp quotes.
        Strings are used unchanged. A date becomes YYYY-MM-DDZ without midnight.
        Datetime is not a declared input type, but date-subclass handling would append
        Z to its isoformat() value without time-zone conversion. Prefer a full UTC
        string normalized to one trailing Z.

        Args:
            since: Timestamp string or date.
            resource_name: Optional ResourceName enum member or trusted string.
                Adds ResourceName eq '<value>'; strings are not escaped.
            **kwargs: Query options for get_deleted. A supplied filter_query is
                appended with and without grouping that expression.

        Returns:
            The server response page unchanged, without automatic pagination.

        Example:
            ```python
            from datetime import datetime, timedelta, timezone

            from wfrmls import ResourceName, WFRMLSClient

            client = WFRMLSClient()  # Requires WFRMLS_BEARER_TOKEN.
            cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
            cutoff_utc = cutoff.isoformat().replace("+00:00", "Z")
            response = client.deleted.get_deleted_since(
                since=cutoff_utc, resource_name=ResourceName.PROPERTY, top=200
            )
            print(len(response.get("value", [])))
            print(response.get("@odata.nextLink"))
            ```
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            since_str = since

        filters = [f"DeletedDateTime gt {since_str}"]

        if resource_name is not None:
            if isinstance(resource_name, ResourceName):
                resource_value = resource_name.value
            else:
                resource_value = resource_name
            filters.append(f"ResourceName eq '{resource_value}'")

        filter_query = " and ".join(filters)

        # If additional filter_query provided, combine them
        existing_filter = kwargs.get("filter_query")
        if existing_filter:
            kwargs["filter_query"] = f"{filter_query} and {existing_filter}"
        else:
            kwargs["filter_query"] = filter_query

        return self.get_deleted(**kwargs)

    def get_deleted_property_records(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one deletion page for Property records.

        Args:
            **kwargs: Query options for get_deleted, forwarded through get_deleted_by_resource.
                A supplied filter_query is appended to the resource filter with and.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_by_resource(ResourceName.PROPERTY, **kwargs)

    def get_deleted_properties(self, **kwargs: Any) -> Dict[str, Any]:
        """Call get_deleted_property_records using a legacy method name.

        Args:
            **kwargs: Arguments forwarded unchanged to get_deleted_property_records.

        Returns:
            One server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_property_records(**kwargs)

    def get_deleted_member_records(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one deletion page for Member records.

        Args:
            **kwargs: Query options for get_deleted, forwarded through get_deleted_by_resource.
                A supplied filter_query is appended to the resource filter with and.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_by_resource(ResourceName.MEMBER, **kwargs)

    def get_deleted_members(self, **kwargs: Any) -> Dict[str, Any]:
        """Call get_deleted_member_records using a legacy method name.

        Args:
            **kwargs: Arguments forwarded unchanged to get_deleted_member_records.

        Returns:
            One server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_member_records(**kwargs)

    def get_deleted_office_records(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one deletion page for Office records.

        Args:
            **kwargs: Query options for get_deleted, forwarded through get_deleted_by_resource.
                A supplied filter_query is appended to the resource filter with and.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_by_resource(ResourceName.OFFICE, **kwargs)

    def get_deleted_offices(self, **kwargs: Any) -> Dict[str, Any]:
        """Call get_deleted_office_records using a legacy method name.

        Args:
            **kwargs: Arguments forwarded unchanged to get_deleted_office_records.

        Returns:
            One server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_office_records(**kwargs)

    def get_deleted_open_houses(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one deletion page for OpenHouse records.

        Args:
            **kwargs: Query options for get_deleted, forwarded through get_deleted_by_resource.
                A supplied filter_query is appended to the resource filter with and.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_by_resource(ResourceName.OPENHOUSE, **kwargs)

    def get_deleted_media_records(self, **kwargs: Any) -> Dict[str, Any]:
        """Query one deletion page for Media records.

        Args:
            **kwargs: Query options for get_deleted, forwarded through get_deleted_by_resource.
                A supplied filter_query is appended to the resource filter with and.

        Returns:
            The server response page unchanged, without automatic pagination.
        """
        return self.get_deleted_by_resource(ResourceName.MEDIA, **kwargs)

    def get_all_deleted_for_sync(
        self,
        since: Union[str, date],
        resource_types: Optional[List[Union[ResourceName, str]]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Aggregate one deletion page per requested resource.

        The default resource list is Property, Member, Office, Media, and OpenHouse.
        Despite the method name, this is not a complete sync: it ignores pagination
        and count metadata. Every per-resource exception is suppressed and represented
        by an empty list, without an error indicator. Use get_deleted_since directly
        when request failures must be distinguishable from no deletions.

        Args:
            since: Timestamp string or date; date becomes YYYY-MM-DDZ.
            resource_types: List of ResourceName members or strings. None uses the
                five defaults; an empty list makes no requests.
            **kwargs: Query options passed to each get_deleted_since call. Do not
                pass resource_name, which the helper supplies itself.

        Returns:
            Dictionary with @odata.context='Comprehensive deletion sync', concatenated
            value records, and by_resource page lists. sync_info contains the local
            total_deleted_records, resource_types_checked, since_timestamp, and
            resources_with_deletions. These counts do not establish provider totals
            or successful completion of every resource request.
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            since_str = since

        # If no resource types specified, get all major types
        if resource_types is None:
            resource_types = [
                ResourceName.PROPERTY,
                ResourceName.MEMBER,
                ResourceName.OFFICE,
                ResourceName.MEDIA,
                ResourceName.OPENHOUSE,
            ]

        all_results = []
        by_resource = {}
        total_count = 0

        for resource_type in resource_types:
            try:
                # Get deleted records for this resource type
                resource_results = self.get_deleted_since(
                    since=since_str, resource_name=resource_type, **kwargs
                )

                resource_records = resource_results.get("value", [])
                resource_name = (
                    resource_type.value
                    if isinstance(resource_type, ResourceName)
                    else resource_type
                )
                by_resource[resource_name] = resource_records
                all_results.extend(resource_records)
                total_count += len(resource_records)

            except Exception:
                # If one resource type fails, continue with others
                resource_name = (
                    resource_type.value
                    if isinstance(resource_type, ResourceName)
                    else resource_type
                )
                by_resource[resource_name] = []

        return {
            "@odata.context": "Comprehensive deletion sync",
            "value": all_results,
            "by_resource": by_resource,
            "sync_info": {
                "total_deleted_records": total_count,
                "resource_types_checked": len(resource_types),
                "since_timestamp": since_str,
                "resources_with_deletions": len([r for r in by_resource.values() if r]),
            },
        }

    def get_deletion_summary(
        self, since: Union[str, date], **kwargs: Any
    ) -> Dict[str, Any]:
        """Summarize one page returned by get_deleted_since.

        Args:
            since: Timestamp string or date; date becomes YYYY-MM-DDZ.
            **kwargs: Arguments forwarded to get_deleted_since, including optional
                resource_name and query options for get_deleted.

        Returns:
            Dictionary with @odata.context='Deletion summary', value records, and
            summary. The summary includes total_deletions, resource_types_affected,
            by_resource_count, by_resource_latest, and analysis_period. Missing
            ResourceName defaults to Unknown. DeletedDateTime values are compared as
            strings, not parsed dates. analysis_period contains since and the local
            date with an appended Z as analysis_timestamp. Pagination metadata is
            discarded; totals describe only the returned page.

        Raises:
            WFRMLSError: For request failures; they are not suppressed here.
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            since_str = since

        # Get all deleted records since the specified time
        all_deletions = self.get_deleted_since(since=since_str, **kwargs)
        deleted_records = all_deletions.get("value", [])

        # Organize by resource type
        by_resource_count: Dict[str, int] = {}
        by_resource_latest: Dict[str, str] = {}

        for record in deleted_records:
            resource_name = record.get("ResourceName", "Unknown")

            # Count by resource type
            if resource_name in by_resource_count:
                by_resource_count[resource_name] += 1
            else:
                by_resource_count[resource_name] = 1

            # Track latest deletion time by resource
            deleted_time = record.get("DeletedDateTime")
            if deleted_time:
                if (
                    resource_name not in by_resource_latest
                    or deleted_time > by_resource_latest[resource_name]
                ):
                    by_resource_latest[resource_name] = deleted_time

        return {
            "@odata.context": "Deletion summary",
            "value": deleted_records,
            "summary": {
                "total_deletions": len(deleted_records),
                "resource_types_affected": len(by_resource_count),
                "by_resource_count": by_resource_count,
                "by_resource_latest": by_resource_latest,
                "analysis_period": {
                    "since": since_str,
                    "analysis_timestamp": f"{date.today().isoformat()}Z",
                },
            },
        }

    def monitor_deletion_activity(
        self, hours_back: int = 24, alert_threshold: int = 100, **kwargs: Any
    ) -> Dict[str, Any]:
        """Compute synchronous alerts from one deletion-page summary.

        This method does not schedule monitoring, send messages, retry, or paginate.
        It currently appends Z to timezone-aware ISO values, producing offset-plus-Z
        cutoff and monitoring timestamps. The provider may reject the generated
        cutoff. Use get_deletion_summary with a normalized UTC string when an explicit
        valid cutoff is required.

        Args:
            hours_back: Hours subtracted from the current UTC time, default 24.
            alert_threshold: Total-count alert threshold, default 100. The method
                also compares each resource count against this threshold divided by
                the number of resource types, using integer division. Comparisons
                are strictly greater than their thresholds.
            **kwargs: Arguments forwarded through get_deletion_summary.

        Returns:
            Dictionary with @odata.context='Deletion monitoring', monitoring_period,
            summary, alerts, recommendations, status, and monitoring_timestamp.
            Status is ALERT if any alert string exists, otherwise NORMAL.
            Recommendations are strings and do not execute cleanup.
        """
        from datetime import datetime, timedelta

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        since_str = cutoff_time.isoformat() + "Z"

        # Get deletion summary for the period
        summary = self.get_deletion_summary(since=since_str, **kwargs)

        alerts = []
        recommendations = []

        total_deletions = summary["summary"]["total_deletions"]
        by_resource_count = summary["summary"]["by_resource_count"]

        # Check for high deletion volumes
        if total_deletions > alert_threshold:
            alerts.append(
                f"High deletion volume: {total_deletions} records deleted in {hours_back} hours"
            )

        # Check for resource-specific alerts
        for resource_type, count in by_resource_count.items():
            resource_threshold = (
                alert_threshold // len(by_resource_count)
                if by_resource_count
                else alert_threshold
            )
            if count > resource_threshold:
                alerts.append(f"High {resource_type} deletions: {count} records")

        # Generate recommendations
        if total_deletions > 0:
            recommendations.append(
                "Consider running data integrity checks after bulk deletions"
            )

        if "Property" in by_resource_count and by_resource_count["Property"] > 10:
            recommendations.append(
                "Review property deletion patterns for market analysis"
            )

        if "Media" in by_resource_count and by_resource_count["Media"] > 50:
            recommendations.append("Check for orphaned media cleanup processes")

        return {
            "@odata.context": "Deletion monitoring",
            "monitoring_period": f"{hours_back} hours",
            "summary": summary["summary"],
            "alerts": alerts,
            "recommendations": recommendations,
            "status": "ALERT" if alerts else "NORMAL",
            "monitoring_timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        }
