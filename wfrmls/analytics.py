"""Sampled listing and member analytics built on the resource clients.

Reports use fixed-size response pages and do not represent a complete market.
"""

from datetime import datetime, timedelta, timezone
from statistics import mean, median
from typing import Any, Dict, Optional


class WFRMLSAnalytics:
    """Calculate report dictionaries from sampled property and member responses.

    The helpers do not paginate. They generally catch exceptions and return an
    error dictionary rather than raising. Always check for error before reading
    report-specific fields. These summaries are not completed-sales, commission,
    or complete-market measurements.
    """

    def __init__(self, client: Any) -> None:
        """Store the client used to retrieve property/member samples.

        Args:
            client: WFRMLSClient or a compatible object exposing property and member clients.
        """
        self.client = client

    def get_market_summary(
        self,
        city: Optional[str] = None,
        days_back: int = 30,
        property_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Summarize up to 200 active and 200 recent-active property records.

        Args:
            city: Optional City filter, default None.
            days_back: Contract-date cutoff for the second request, default 30.
            property_type: Optional PropertyType filter, default None.

        Returns:
            Dictionary with inventory, pricing, activity, report labels, and timestamp;
            or a dictionary containing error if a request or calculation fails.

        Note:
            This uses active listings, not recent sales or a server-wide count. The
            contract-date filter currently appends Z to an offset-bearing UTC string
            such as ...+00:00Z, which a provider may reject. Prices/days on market
            reflect only records returned in these unpaginated samples.
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        cutoff_str = cutoff_date.isoformat() + "Z"

        # Build filters
        filters = ["StandardStatus eq 'Active'"]
        if city:
            filters.append(f"City eq '{city}'")
        if property_type:
            filters.append(f"PropertyType eq '{property_type}'")

        base_filter = " and ".join(filters)

        try:
            # Get active listings
            active_listings = self.client.property.get_properties(
                filter_query=base_filter, top=200
            )

            # Get recent new listings
            new_listing_filter = (
                f"{base_filter} and ListingContractDate gt {cutoff_str}"
            )
            new_listings = self.client.property.get_properties(
                filter_query=new_listing_filter, top=200
            )

            # Calculate summary statistics
            active_properties = active_listings.get("value", [])
            new_properties = new_listings.get("value", [])

            # Price analysis
            prices = [
                prop.get("ListPrice", 0)
                for prop in active_properties
                if prop.get("ListPrice")
            ]
            avg_price = mean(prices) if prices else 0
            median_price = median(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0

            # Days on market analysis
            dom_values = []
            for prop in active_properties:
                list_date = prop.get("ListingContractDate")
                if list_date:
                    try:
                        list_dt = datetime.fromisoformat(
                            list_date.replace("Z", "+00:00")
                        )
                        days_on_market = (
                            datetime.now(timezone.utc).replace(tzinfo=list_dt.tzinfo)
                            - list_dt
                        ).days
                        dom_values.append(days_on_market)
                    except (ValueError, TypeError):
                        continue

            avg_dom = mean(dom_values) if dom_values else 0

            return {
                "market_area": city or "All Areas",
                "property_type": property_type or "All Types",
                "analysis_period": f"{days_back} days",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "inventory": {
                    "active_listings": len(active_properties),
                    "new_listings": len(new_properties),
                    "new_listings_rate": (
                        len(new_properties) / days_back if days_back > 0 else 0
                    ),
                },
                "pricing": {
                    "average_price": avg_price,
                    "median_price": median_price,
                    "min_price": min_price,
                    "max_price": max_price,
                    "price_range": max_price - min_price if prices else 0,
                },
                "activity": {
                    "avg_days_on_market": avg_dom,
                    "properties_analyzed": len(dom_values),
                    "market_velocity": (
                        1 / (avg_dom / 30) if avg_dom > 0 else 0
                    ),  # Turnover per month
                },
            }

        except Exception as e:
            return {
                "error": f"Failed to generate market summary: {str(e)}",
                "market_area": city or "All Areas",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            }

    def analyze_price_trends(
        self,
        city: Optional[str] = None,
        days_back: int = 90,
        property_type: Optional[str] = None,
        price_segments: int = 5,
    ) -> Dict[str, Any]:
        """Segment positive prices from one Active-listing page of up to 200 records.

        Args:
            city: Optional City filter, default None.
            days_back: Report label only; it is not used in a date filter, default 90.
            property_type: Optional PropertyType filter, default None.
            price_segments: Positive segment count no larger than valid record count, default 5.

        Returns:
            Dictionary with overall_pricing, price_segments, market_insights, and sample
            labels/counts; or an error dictionary for missing prices or calculation errors.

        Note:
            This is a sampled price distribution, not historical appreciation or
            period-over-period price change. Empty segments cause an error result.
        """
        # Build filters
        filters = ["StandardStatus eq 'Active'"]
        if city:
            filters.append(f"City eq '{city}'")
        if property_type:
            filters.append(f"PropertyType eq '{property_type}'")

        base_filter = " and ".join(filters)

        try:
            # Get active listings
            properties = self.client.property.get_properties(
                filter_query=base_filter,
                top=200,
                select=[
                    "ListPrice",
                    "BedroomsTotal",
                    "BathroomsTotalInteger",
                    "LivingArea",
                    "ListingContractDate",
                ],
            )

            property_list = properties.get("value", [])

            # Extract prices and filter out invalid values
            valid_properties = [
                prop for prop in property_list if prop.get("ListPrice", 0) > 0
            ]
            prices = [prop["ListPrice"] for prop in valid_properties]

            if not prices:
                return {"error": "No valid property data found for analysis"}

            # Sort prices for segmentation
            prices.sort()

            # Create price segments
            segment_size = len(prices) // price_segments
            segments = []

            for i in range(price_segments):
                start_idx = i * segment_size
                end_idx = (
                    (i + 1) * segment_size if i < price_segments - 1 else len(prices)
                )

                segment_prices = prices[start_idx:end_idx]
                segment_name = (
                    f"Segment {i + 1}"
                    if price_segments > 3
                    else (
                        ["Budget", "Mid-Range", "Luxury"][i]
                        if i < 3
                        else f"Premium {i - 2}"
                    )
                )

                segments.append(
                    {
                        "name": segment_name,
                        "min_price": min(segment_prices),
                        "max_price": max(segment_prices),
                        "avg_price": mean(segment_prices),
                        "count": len(segment_prices),
                        "market_share": len(segment_prices) / len(prices) * 100,
                    }
                )

            # Calculate overall statistics
            avg_price = mean(prices)
            median_price = median(prices)

            # Price per square foot analysis
            sqft_data = []
            for prop in valid_properties:
                price = prop.get("ListPrice", 0)
                sqft = prop.get("LivingArea", 0)
                if price > 0 and sqft > 0:
                    sqft_data.append(price / sqft)

            avg_price_per_sqft = mean(sqft_data) if sqft_data else 0

            return {
                "market_area": city or "All Areas",
                "property_type": property_type or "All Types",
                "analysis_period": f"{days_back} days",
                "properties_analyzed": len(valid_properties),
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "overall_pricing": {
                    "average_price": avg_price,
                    "median_price": median_price,
                    "min_price": min(prices),
                    "max_price": max(prices),
                    "avg_price_per_sqft": avg_price_per_sqft,
                },
                "price_segments": segments,
                "market_insights": {
                    "luxury_threshold": (
                        prices[int(len(prices) * 0.8)]
                        if len(prices) > 5
                        else max(prices)
                    ),
                    "affordable_threshold": (
                        prices[int(len(prices) * 0.2)]
                        if len(prices) > 5
                        else min(prices)
                    ),
                    "price_diversity_score": (
                        (max(prices) - min(prices)) / avg_price if avg_price > 0 else 0
                    ),
                },
            }

        except Exception as e:
            return {
                "error": f"Failed to analyze price trends: {str(e)}",
                "market_area": city or "All Areas",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            }

    def generate_agent_performance_report(
        self, days_back: int = 90, min_listings: int = 5
    ) -> Dict[str, Any]:
        """Aggregate matched member listing activity from two unpaginated samples.

        Args:
            days_back: Contract-date lookback for properties, default 90.
            min_listings: Minimum sampled listing count for an included agent, default 5.

        Returns:
            Dictionary with summary, top_agents, labels, timestamp, and sample counts;
            or an error dictionary if requests or calculations fail.

        Note:
            Retrieves up to 200 properties with Member expansion and 200 active members.
            Aggregates by MemberFullName after matching MemberKey and returns the top
            ten by sampled listing count, total list value, and average list price.
            Duplicate display names can combine agents. The cutoff has the current
            ...+00:00Z formatting limitation. No commissions or full-market totals
            are calculated.
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        cutoff_str = cutoff_date.isoformat() + "Z"

        try:
            # Get recent listings with member information
            recent_listings = self.client.property.get_properties(
                filter_query=f"ListingContractDate gt {cutoff_str}",
                expand="Member",
                top=200,
                select=[
                    "ListingId",
                    "ListPrice",
                    "StandardStatus",
                    "ListingContractDate",
                ],
            )

            # Get active members
            members = self.client.member.get_members(
                filter_query="MemberStatus eq 'Active'",
                top=200,
                select=["MemberKey", "MemberFullName", "MemberEmail", "OfficeKey"],
            )

            listings = recent_listings.get("value", [])
            member_list = members.get("value", [])

            # Create member lookup
            member_lookup = {member.get("MemberKey"): member for member in member_list}

            # Analyze agent performance
            agent_stats = {}

            for listing in listings:
                member_info = listing.get("Member", {})
                member_key = (
                    member_info.get("MemberKey")
                    if isinstance(member_info, dict)
                    else None
                )

                if member_key and member_key in member_lookup:
                    agent = member_lookup[member_key]
                    agent_name = agent.get("MemberFullName", "Unknown")

                    if agent_name not in agent_stats:
                        agent_stats[agent_name] = {
                            "member_key": member_key,
                            "listing_count": 0,
                            "total_value": 0,
                            "avg_price": 0,
                            "active_listings": 0,
                            "pending_listings": 0,
                            "email": agent.get("MemberEmail", ""),
                            "office_key": agent.get("OfficeKey", ""),
                        }

                    stats = agent_stats[agent_name]
                    stats["listing_count"] += 1

                    list_price = listing.get("ListPrice", 0)
                    stats["total_value"] += list_price

                    status = listing.get("StandardStatus", "")
                    if status == "Active":
                        stats["active_listings"] += 1
                    elif status == "Pending":
                        stats["pending_listings"] += 1

            # Calculate averages and filter by minimum listings
            qualified_agents = []
            for agent_name, stats in agent_stats.items():
                if stats["listing_count"] >= min_listings:
                    stats["avg_price"] = (
                        stats["total_value"] / stats["listing_count"]
                        if stats["listing_count"] > 0
                        else 0
                    )
                    stats["name"] = agent_name
                    qualified_agents.append(stats)

            # Sort agents by different metrics
            top_by_listings = sorted(
                qualified_agents, key=lambda x: x["listing_count"], reverse=True
            )
            top_by_value = sorted(
                qualified_agents, key=lambda x: x["total_value"], reverse=True
            )
            top_by_avg_price = sorted(
                qualified_agents, key=lambda x: x["avg_price"], reverse=True
            )

            return {
                "analysis_period": f"{days_back} days",
                "min_listings_threshold": min_listings,
                "total_agents_analyzed": len(qualified_agents),
                "total_listings_analyzed": len(listings),
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "summary": {
                    "avg_listings_per_agent": (
                        mean([agent["listing_count"] for agent in qualified_agents])
                        if qualified_agents
                        else 0
                    ),
                    "avg_listing_value": (
                        mean([agent["avg_price"] for agent in qualified_agents])
                        if qualified_agents
                        else 0
                    ),
                    "total_market_value": sum(
                        [agent["total_value"] for agent in qualified_agents]
                    ),
                },
                "top_agents": {
                    "by_listings": top_by_listings[:10],
                    "by_total_value": top_by_value[:10],
                    "by_avg_price": top_by_avg_price[:10],
                },
            }

        except Exception as e:
            return {
                "error": f"Failed to generate agent performance report: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            }

    def get_data_quality_report(self) -> Dict[str, Any]:
        """Score selected fields in samples of up to 50 properties and 30 members.

        Returns:
            Dictionary with property_quality, member_quality, overall_quality_score,
            issues, recommendations, timestamp, and GOOD/FAIR/NEEDS_ATTENTION status;
            or an error dictionary if retrieval or calculations fail.

        Note:
            Falsey price, city, bedroom, size, and email values count as missing. An
            empty property sample causes a caught division-by-zero error. Office
            records, source accuracy, and complete datasets are not evaluated.
        """
        try:
            issues = []
            recommendations = []

            # Sample properties for analysis
            properties = self.client.property.get_properties(
                top=50,
                select=[
                    "ListingId",
                    "ListPrice",
                    "StandardStatus",
                    "City",
                    "BedroomsTotal",
                    "LivingArea",
                    "ListingContractDate",
                ],
            )

            property_list = properties.get("value", [])

            # Analyze property data quality
            total_properties = len(property_list)
            price_missing = sum(
                1 for prop in property_list if not prop.get("ListPrice")
            )
            city_missing = sum(1 for prop in property_list if not prop.get("City"))
            bedrooms_missing = sum(
                1 for prop in property_list if not prop.get("BedroomsTotal")
            )
            sqft_missing = sum(
                1 for prop in property_list if not prop.get("LivingArea")
            )

            property_completeness = 1 - (
                price_missing + city_missing + bedrooms_missing + sqft_missing
            ) / (total_properties * 4)

            if price_missing > total_properties * 0.1:
                issues.append(
                    f"High missing price data: {price_missing}/{total_properties} properties"
                )
                recommendations.append("Review price data entry processes")

            if city_missing > total_properties * 0.05:
                issues.append(
                    f"Missing city data: {city_missing}/{total_properties} properties"
                )
                recommendations.append("Improve location data validation")

            # Sample members for analysis
            members = self.client.member.get_members(
                top=30,
                select=["MemberKey", "MemberFullName", "MemberEmail", "MemberStatus"],
            )

            member_list = members.get("value", [])
            total_members = len(member_list)
            email_missing = sum(
                1 for member in member_list if not member.get("MemberEmail")
            )

            member_completeness = (
                1 - email_missing / total_members if total_members > 0 else 1
            )

            if email_missing > total_members * 0.2:
                issues.append(
                    f"High missing email data: {email_missing}/{total_members} members"
                )
                recommendations.append("Update member contact information requirements")

            # Overall quality score
            overall_score = (property_completeness + member_completeness) / 2

            return {
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "overall_quality_score": overall_score,
                "property_quality": {
                    "total_analyzed": total_properties,
                    "completeness_score": property_completeness,
                    "missing_data": {
                        "prices": price_missing,
                        "cities": city_missing,
                        "bedrooms": bedrooms_missing,
                        "square_footage": sqft_missing,
                    },
                },
                "member_quality": {
                    "total_analyzed": total_members,
                    "completeness_score": member_completeness,
                    "missing_data": {"emails": email_missing},
                },
                "issues": issues,
                "recommendations": recommendations,
                "status": (
                    "GOOD"
                    if overall_score > 0.9
                    else "FAIR" if overall_score > 0.7 else "NEEDS_ATTENTION"
                ),
            }

        except Exception as e:
            return {
                "error": f"Failed to generate data quality report: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            }
