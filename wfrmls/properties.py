"""Property client for WFRMLS API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


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
    """Client for property API endpoints.
    
    The Property resource is the primary resource in the WFRMLS API, containing
    real estate listing data including property details, pricing, and location
    information. This client provides access to all property-related endpoints
    with comprehensive OData query support.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property client.

        Args:
            bearer_token: Bearer token for authentication
            base_url: Base URL for the API
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

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
        """Get properties with optional OData filtering.

        This method retrieves property listings with full OData v4.0 query support.
        It's the primary method for accessing property data in the WFRMLS system.

        Args:
            top: Number of results to return (OData $top, max 200 per API limit)
            skip: Number of results to skip (OData $skip) - use with caution for large datasets,
                prefer NextLink pagination instead
            filter_query: OData filter query string for complex filtering
            select: Fields to select (OData $select) - can be list or comma-separated string
            orderby: Order by clause (OData $orderby) for result sorting
            expand: Related resources to include (OData $expand) - can be list or comma-separated string
            count: Include total count in results (OData $count)

        Returns:
            Dictionary containing property data with structure:
                - @odata.context: Metadata URL
                - @odata.count: Total count (if requested)
                - @odata.nextLink: Next page URL (if more results available)
                - value: List of property records

        Raises:
            WFRMLSError: If the API request fails
            ValidationError: If OData query parameters are invalid
            RateLimitError: If the rate limit is exceeded

        Example:
            ```python
            # Get first 10 active properties
            properties = client.property.get_properties(
                top=10,
                filter_query="StandardStatus eq 'Active'"
            )

            # Get properties with photos and agent info
            properties = client.property.get_properties(
                expand=["Media", "Member"],
                top=50
            )

            # Get properties in price range with sorting
            properties = client.property.get_properties(
                filter_query="ListPrice ge 200000 and ListPrice le 500000",
                orderby="ListPrice desc",
                top=100
            )

            # Get properties with specific fields only
            properties = client.property.get_properties(
                select=["ListingId", "ListPrice", "StandardStatus", "City"],
                top=50
            )
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

        return self.get("Property", params=params)

    def get_property(self, listing_id: str) -> Dict[str, Any]:
        """Get property by listing ID.

        Retrieves a single property record by its unique listing ID.
        This is the most efficient way to get detailed information about
        a specific property.

        Args:
            listing_id: Listing ID to retrieve (ResourceRecordKey)

        Returns:
            Dictionary containing property data for the specified listing

        Raises:
            NotFoundError: If the property with the given ID is not found
            WFRMLSError: If the API request fails

        Example:
            ```python
            # Get specific property by listing ID
            property = client.property.get_property("12345678")
            
            print(f"Property: {property['ListPrice']}")
            print(f"Address: {property['UnparsedAddress']}")
            ```
        """
        return self.get(f"Property('{listing_id}')")

    def search_properties_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_miles: float,
        additional_filters: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Search properties within a radius of given coordinates.

        Uses geospatial queries to find properties within a specified distance
        from a center point. This is ideal for location-based property searches.

        Args:
            latitude: Latitude coordinate for center point
            longitude: Longitude coordinate for center point
            radius_miles: Search radius in miles
            additional_filters: Additional OData filter query to combine with geo filter
            **kwargs: Additional OData parameters (top, select, orderby, etc.)

        Returns:
            Dictionary containing property data within the specified radius

        Raises:
            ValidationError: If coordinates are invalid
            WFRMLSError: If the API request fails

        Example:
            ```python
            # Find properties within 10 miles of Salt Lake City
            properties = client.property.search_properties_by_radius(
                latitude=40.7608,
                longitude=-111.8910,
                radius_miles=10,
                additional_filters="StandardStatus eq 'Active'",
                top=50
            )

            # Find expensive properties near downtown
            properties = client.property.search_properties_by_radius(
                latitude=40.7608,
                longitude=-111.8910,
                radius_miles=5,
                additional_filters="ListPrice ge 500000 and StandardStatus eq 'Active'",
                orderby="ListPrice desc"
            )
            ```
        """
        geo_filter = f"geo.distance(Latitude, Longitude, {latitude}, {longitude}) le {radius_miles}"
        
        if additional_filters:
            filter_query = f"{geo_filter} and {additional_filters}"
        else:
            filter_query = geo_filter
            
        return self.get_properties(filter_query=filter_query, **kwargs)

    def search_properties_by_polygon(
        self,
        polygon_coordinates: List[Dict[str, float]],
        additional_filters: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Search properties within a polygon area.

        Uses geospatial polygon intersection to find properties within
        a defined boundary. Useful for searching within specific
        neighborhoods, districts, or custom geographic areas.

        Args:
            polygon_coordinates: List of coordinate dicts with 'lat' and 'lng' keys.
                Must have at least 3 points and should be closed (first == last).
            additional_filters: Additional OData filter query to combine with geo filter
            **kwargs: Additional OData parameters (top, select, orderby, etc.)

        Returns:
            Dictionary containing property data within the polygon

        Raises:
            ValidationError: If polygon coordinates are invalid
            WFRMLSError: If the API request fails

        Example:
            ```python
            # Define polygon around downtown area
            polygon = [
                {"lat": 40.7608, "lng": -111.8910},
                {"lat": 40.7708, "lng": -111.8810},
                {"lat": 40.7508, "lng": -111.8710},
                {"lat": 40.7608, "lng": -111.8910}  # Close polygon
            ]
            
            properties = client.property.search_properties_by_polygon(
                polygon_coordinates=polygon,
                additional_filters="PropertyType eq 'Residential'",
                top=100
            )
            ```
        """
        # Build polygon string for geo.intersects function
        coords_str = ",".join([f"{coord['lat']} {coord['lng']}" for coord in polygon_coordinates])
        geo_filter = f"geo.intersects(Latitude, Longitude, geography'POLYGON(({coords_str}))')"
        
        if additional_filters:
            filter_query = f"{geo_filter} and {additional_filters}"
        else:
            filter_query = geo_filter
            
        return self.get_properties(filter_query=filter_query, **kwargs)

    def get_properties_with_media(
        self,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get properties with their associated media/photos.

        This is a convenience method that automatically expands the Media
        relationship to include property photos in the response. More efficient
        than making separate requests for properties and their media.

        Args:
            **kwargs: OData parameters (top, filter_query, select, etc.)

        Returns:
            Dictionary containing property data with expanded Media relationships

        Example:
            ```python
            # Get active properties with photos
            properties = client.property.get_properties_with_media(
                filter_query="StandardStatus eq 'Active'",
                top=25
            )
            
            # Access photos for first property
            first_property = properties['value'][0]
            if 'Media' in first_property:
                photos = first_property['Media']
                print(f"Property has {len(photos)} photos")
            ```
        """
        return self.get_properties(expand="Media", **kwargs)

    def get_active_properties(
        self,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get properties with Active status.

        Convenience method to retrieve only active property listings.
        This is one of the most common queries for real estate applications.

        Args:
            **kwargs: Additional OData parameters (top, select, orderby, etc.)

        Returns:
            Dictionary containing active property listings

        Example:
            ```python
            # Get all active properties
            active_properties = client.property.get_active_properties(top=100)

            # Get active properties with specific fields
            active_properties = client.property.get_active_properties(
                select=["ListingId", "ListPrice", "UnparsedAddress"],
                orderby="ListPrice"
            )
            ```
        """
        return self.get_properties(filter_query="StandardStatus eq 'Active'", **kwargs)

    def get_properties_by_price_range(
        self,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get properties within a price range.

        Convenience method to filter properties by listing price range.
        Commonly used for buyer searches and market analysis.

        Args:
            min_price: Minimum listing price (inclusive)
            max_price: Maximum listing price (inclusive)
            **kwargs: Additional OData parameters

        Returns:
            Dictionary containing properties within the price range

        Example:
            ```python
            # Properties between $200K and $500K
            properties = client.property.get_properties_by_price_range(
                min_price=200000,
                max_price=500000,
                top=50
            )

            # Properties under $300K
            properties = client.property.get_properties_by_price_range(
                max_price=300000
            )

            # Properties over $1M
            properties = client.property.get_properties_by_price_range(
                min_price=1000000
            )
            ```
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

    def get_properties_by_city(
        self,
        city: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get properties in a specific city.

        Convenience method to filter properties by city name.
        Useful for location-specific searches.

        Args:
            city: City name to filter by
            **kwargs: Additional OData parameters

        Returns:
            Dictionary containing properties in the specified city

        Example:
            ```python
            # Get properties in Salt Lake City
            properties = client.property.get_properties_by_city(
                city="Salt Lake City",
                top=100
            )
            
            # Get active properties in Provo
            properties = client.property.get_properties_by_city(
                city="Provo",
                filter_query="StandardStatus eq 'Active'",
                orderby="ListPrice"
            )
            ```
        """
        city_filter = f"City eq '{city}'"
        
        # If additional filter_query provided, combine them
        existing_filter = kwargs.get('filter_query')
        if existing_filter:
            kwargs['filter_query'] = f"{city_filter} and {existing_filter}"
        else:
            kwargs['filter_query'] = city_filter
            
        return self.get_properties(**kwargs)

    def get_modified_properties(
        self,
        since: Union[str, date],
        **kwargs
    ) -> Dict[str, Any]:
        """Get properties modified since a specific date/time.

        Used for incremental data synchronization to get only properties
        that have been updated since the last sync. Essential for maintaining
        up-to-date property data.

        Args:
            since: ISO format datetime string or date object for cutoff time
            **kwargs: Additional OData parameters

        Returns:
            Dictionary containing properties modified since the specified time

        Example:
            ```python
            from datetime import datetime, timedelta
            
            # Get properties modified in last 15 minutes (recommended sync interval)
            cutoff_time = datetime.utcnow() - timedelta(minutes=15)
            updates = client.property.get_modified_properties(
                since=cutoff_time.isoformat() + "Z"
            )

            # Get properties modified since yesterday
            yesterday = datetime.utcnow() - timedelta(days=1)
            updates = client.property.get_modified_properties(
                since=yesterday.isoformat() + "Z"
            )
            ```
        """
        if isinstance(since, date):
            since_str = since.isoformat() + "Z"
        else:
            since_str = since
            
        filter_query = f"ModificationTimestamp gt {since_str}"
        return self.get_properties(filter_query=filter_query, **kwargs) 