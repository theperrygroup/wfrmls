# Geolocation Queries

This guide covers how to perform location-based searches using the WFRMLS API, including radius searches, polygon searches, and coordinate-based filtering.

## Overview

The WFRMLS API supports several types of geolocation queries:

- **Point radius searches** - Find properties within a certain distance of a point
- **Polygon searches** - Find properties within a defined geographic area
- **Coordinate filtering** - Filter by latitude/longitude ranges
- **Address-based searches** - Search by city, ZIP code, or address

## Point Radius Searches

Search for properties within a specified radius of a geographic point.

### Basic Radius Search

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")

# Search within 5 miles of downtown Salt Lake City
properties = client.property.get_properties(
    filter_query="""
        geo.distance(
            geography'POINT(-111.8910 40.7608)', 
            geography'POINT(' + cast(Longitude as Edm.String) + ' ' + cast(Latitude as Edm.String) + ')'
        ) le 5
    """,
    top=50
)

print(f"Found {len(properties)} properties within 5 miles")
```

### Using Helper Function

```python
def search_by_radius(client, center_lat, center_lon, radius_miles, max_results=50):
    """Search for properties within a radius of a center point."""
    
    filter_query = f"""
        geo.distance(
            geography'POINT({center_lon} {center_lat})', 
            geography'POINT(' + cast(Longitude as Edm.String) + ' ' + cast(Latitude as Edm.String) + ')'
        ) le {radius_miles}
    """
    
    return client.property.get_properties(
        filter_query=filter_query,
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "Latitude", "Longitude", "City"
        ],
        top=max_results,
        orderby="ListPrice asc"
    )

# Search near University of Utah
university_properties = search_by_radius(
    client, 
    center_lat=40.7649, 
    center_lon=-111.8421, 
    radius_miles=2
)
```

### Distance Calculation

```python
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in miles
    r = 3956
    
    return c * r

# Verify distances in results
center_lat, center_lon = 40.7608, -111.8910

for prop in properties:
    if prop.get('Latitude') and prop.get('Longitude'):
        distance = calculate_distance(
            center_lat, center_lon,
            prop['Latitude'], prop['Longitude']
        )
        print(f"Property {prop['ListingId']}: {distance:.2f} miles away")
```

## Polygon Searches

Search for properties within a defined polygon area.

### Simple Polygon Search

```python
def search_by_polygon(client, polygon_coords, max_results=100):
    """Search for properties within a polygon."""
    
    # Convert coordinates to WKT format
    coord_pairs = [f"{lon} {lat}" for lat, lon in polygon_coords]
    polygon_wkt = f"POLYGON(({', '.join(coord_pairs)}, {coord_pairs[0]}))"
    
    filter_query = f"""
        geo.intersects(
            geography'POINT(' + cast(Longitude as Edm.String) + ' ' + cast(Latitude as Edm.String) + ')',
            geography'{polygon_wkt}'
        )
    """
    
    return client.property.get_properties(
        filter_query=filter_query,
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "Latitude", "Longitude"
        ],
        top=max_results
    )

# Define a polygon around downtown Salt Lake City
downtown_polygon = [
    (40.7500, -111.9200),  # Southwest corner
    (40.7500, -111.8600),  # Southeast corner
    (40.7800, -111.8600),  # Northeast corner
    (40.7800, -111.9200),  # Northwest corner
]

downtown_properties = search_by_polygon(client, downtown_polygon)
print(f"Found {len(downtown_properties)} properties in downtown area")
```

### Complex Polygon Areas

```python
# Define irregular polygon for specific neighborhood
avenues_polygon = [
    (40.7850, -111.8750),
    (40.7900, -111.8650),
    (40.7950, -111.8700),
    (40.7920, -111.8800),
    (40.7880, -111.8820),
]

avenues_properties = search_by_polygon(client, avenues_polygon)

# Filter by additional criteria
luxury_avenues = [
    prop for prop in avenues_properties 
    if prop.get('ListPrice', 0) > 1000000
]

print(f"Found {len(luxury_avenues)} luxury properties in The Avenues")
```

## Coordinate Range Filtering

Filter properties by latitude and longitude ranges.

### Bounding Box Search

```python
def search_by_bounding_box(client, north, south, east, west, max_results=100):
    """Search within a rectangular bounding box."""
    
    filter_query = f"""
        Latitude ge {south} and Latitude le {north} and
        Longitude ge {west} and Longitude le {east}
    """
    
    return client.property.get_properties(
        filter_query=filter_query,
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "Latitude", "Longitude", "City"
        ],
        top=max_results,
        orderby="Latitude asc, Longitude asc"
    )

# Search in Salt Lake Valley
valley_properties = search_by_bounding_box(
    client,
    north=40.8000,   # Northern boundary
    south=40.5000,   # Southern boundary  
    east=-111.7000,  # Eastern boundary
    west=-112.0000   # Western boundary
)
```

### Coordinate Validation

```python
def validate_coordinates(lat, lon):
    """Validate latitude and longitude values."""
    
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90")
    
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180")
    
    return True

def safe_coordinate_search(client, lat, lon, radius):
    """Perform coordinate search with validation."""
    
    try:
        validate_coordinates(lat, lon)
        return search_by_radius(client, lat, lon, radius)
    except ValueError as e:
        print(f"Coordinate validation error: {e}")
        return []
```

## Address-Based Searches

Search using addresses, cities, and ZIP codes.

### City-Based Search

```python
def search_by_city(client, city_name, max_results=100):
    """Search for properties in a specific city."""
    
    return client.property.get_properties(
        filter_query=f"City eq '{city_name}'",
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "City", "PostalCode"
        ],
        top=max_results,
        orderby="ListPrice asc"
    )

# Search in Park City
park_city_properties = search_by_city(client, "Park City")
```

### ZIP Code Search

```python
def search_by_zip_codes(client, zip_codes, max_results=200):
    """Search for properties in multiple ZIP codes."""
    
    zip_filter = " or ".join([f"PostalCode eq '{zip_code}'" for zip_code in zip_codes])
    
    return client.property.get_properties(
        filter_query=f"({zip_filter})",
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "City", "PostalCode"
        ],
        top=max_results,
        orderby="PostalCode asc, ListPrice asc"
    )

# Search in multiple Salt Lake City ZIP codes
slc_zip_codes = ["84101", "84102", "84103", "84105", "84106"]
slc_properties = search_by_zip_codes(client, slc_zip_codes)
```

### Address Proximity Search

```python
def search_near_address(client, address, radius_miles=1):
    """Search for properties near a specific address."""
    
    # First, geocode the address (you'll need a geocoding service)
    lat, lon = geocode_address(address)
    
    if lat and lon:
        return search_by_radius(client, lat, lon, radius_miles)
    else:
        print(f"Could not geocode address: {address}")
        return []

def geocode_address(address):
    """Geocode an address to coordinates (implement with your preferred service)."""
    # Example using a geocoding service
    # This is a placeholder - implement with your preferred geocoding API
    
    # Common Utah addresses for example
    utah_addresses = {
        "Temple Square, Salt Lake City, UT": (40.7701, -111.8910),
        "University of Utah, Salt Lake City, UT": (40.7649, -111.8421),
        "Park City Main Street, Park City, UT": (40.6461, -111.4980),
    }
    
    return utah_addresses.get(address, (None, None))

# Search near Temple Square
temple_square_properties = search_near_address(
    client, 
    "Temple Square, Salt Lake City, UT", 
    radius_miles=0.5
)
```

## Advanced Geolocation Techniques

### Multi-Point Search

```python
def search_multiple_locations(client, locations, radius_miles=2):
    """Search around multiple locations and combine results."""
    
    all_properties = []
    seen_ids = set()
    
    for location in locations:
        lat, lon = location['lat'], location['lon']
        name = location.get('name', f"{lat},{lon}")
        
        print(f"Searching near {name}...")
        
        properties = search_by_radius(client, lat, lon, radius_miles, max_results=50)
        
        # Avoid duplicates
        for prop in properties:
            listing_id = prop['ListingId']
            if listing_id not in seen_ids:
                prop['nearest_location'] = name
                all_properties.append(prop)
                seen_ids.add(listing_id)
    
    return all_properties

# Search near multiple ski resorts
ski_resorts = [
    {"name": "Park City Mountain Resort", "lat": 40.6516, "lon": -111.5081},
    {"name": "Deer Valley Resort", "lat": 40.6374, "lon": -111.4783},
    {"name": "Alta Ski Area", "lat": 40.5885, "lon": -111.6387},
]

ski_properties = search_multiple_locations(client, ski_resorts, radius_miles=5)
```

### Geographic Clustering

```python
def cluster_properties_by_location(properties, cluster_radius_miles=1):
    """Group properties into geographic clusters."""
    
    clusters = []
    unclustered = properties.copy()
    
    while unclustered:
        # Start new cluster with first property
        seed = unclustered.pop(0)
        cluster = [seed]
        
        # Find nearby properties
        remaining = []
        for prop in unclustered:
            if (prop.get('Latitude') and prop.get('Longitude') and
                seed.get('Latitude') and seed.get('Longitude')):
                
                distance = calculate_distance(
                    seed['Latitude'], seed['Longitude'],
                    prop['Latitude'], prop['Longitude']
                )
                
                if distance <= cluster_radius_miles:
                    cluster.append(prop)
                else:
                    remaining.append(prop)
            else:
                remaining.append(prop)
        
        unclustered = remaining
        clusters.append(cluster)
    
    return clusters

# Cluster properties and analyze
properties = search_by_city(client, "Salt Lake City", max_results=200)
clusters = cluster_properties_by_location(properties, cluster_radius_miles=0.5)

print(f"Found {len(clusters)} property clusters:")
for i, cluster in enumerate(clusters):
    avg_price = sum(prop.get('ListPrice', 0) for prop in cluster) / len(cluster)
    print(f"  Cluster {i+1}: {len(cluster)} properties, avg price: ${avg_price:,.0f}")
```

## Performance Optimization

### Efficient Coordinate Queries

```python
def optimized_radius_search(client, center_lat, center_lon, radius_miles, 
                          property_type=None, price_range=None):
    """Optimized radius search with additional filters."""
    
    # Start with bounding box for efficiency
    lat_delta = radius_miles / 69.0  # Approximate miles per degree latitude
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(center_lat)))
    
    bbox_filter = f"""
        Latitude ge {center_lat - lat_delta} and Latitude le {center_lat + lat_delta} and
        Longitude ge {center_lon - lon_delta} and Longitude le {center_lon + lon_delta}
    """
    
    # Add additional filters
    filters = [bbox_filter]
    
    if property_type:
        filters.append(f"PropertyType eq '{property_type}'")
    
    if price_range:
        if price_range.get('min'):
            filters.append(f"ListPrice ge {price_range['min']}")
        if price_range.get('max'):
            filters.append(f"ListPrice le {price_range['max']}")
    
    # Add precise radius filter
    radius_filter = f"""
        geo.distance(
            geography'POINT({center_lon} {center_lat})', 
            geography'POINT(' + cast(Longitude as Edm.String) + ' ' + cast(Latitude as Edm.String) + ')'
        ) le {radius_miles}
    """
    filters.append(radius_filter)
    
    combined_filter = " and ".join(filters)
    
    return client.property.get_properties(
        filter_query=combined_filter,
        select=[
            "ListingId", "ListPrice", "PropertyType", "StandardStatus",
            "UnparsedAddress", "Latitude", "Longitude", "City"
        ],
        top=100,
        orderby="ListPrice asc"
    )

# Optimized search for residential properties under $500K
affordable_homes = optimized_radius_search(
    client,
    center_lat=40.7608,
    center_lon=-111.8910,
    radius_miles=10,
    property_type="RES",
    price_range={"max": 500000}
)
```

### Caching Strategies

```python
import hashlib
import json
from datetime import datetime, timedelta

class GeolocationCache:
    def __init__(self, cache_duration_hours=1):
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
    
    def _generate_key(self, lat, lon, radius, filters=None):
        """Generate cache key for search parameters."""
        key_data = {
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "radius": radius,
            "filters": filters or {}
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, lat, lon, radius, filters=None):
        """Get cached results if available and not expired."""
        key = self._generate_key(lat, lon, radius, filters)
        
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data
            else:
                del self.cache[key]
        
        return None
    
    def set(self, lat, lon, radius, results, filters=None):
        """Cache search results."""
        key = self._generate_key(lat, lon, radius, filters)
        self.cache[key] = (results, datetime.now())
    
    def clear_expired(self):
        """Remove expired cache entries."""
        now = datetime.now()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if now - timestamp >= self.cache_duration
        ]
        for key in expired_keys:
            del self.cache[key]

# Usage with caching
geo_cache = GeolocationCache(cache_duration_hours=2)

def cached_radius_search(client, lat, lon, radius, **filters):
    """Radius search with caching."""
    
    # Check cache first
    cached_results = geo_cache.get(lat, lon, radius, filters)
    if cached_results:
        print("Returning cached results")
        return cached_results
    
    # Perform search
    results = optimized_radius_search(client, lat, lon, radius, **filters)
    
    # Cache results
    geo_cache.set(lat, lon, radius, results, filters)
    
    return results
```

## Best Practices

### Coordinate Precision

1. **Round coordinates** appropriately for your use case
2. **Validate input ranges** to prevent invalid queries
3. **Use appropriate radius sizes** for performance
4. **Consider coordinate system differences** (WGS84 vs others)

### Query Optimization

1. **Use bounding boxes** before precise distance calculations
2. **Combine geographic and attribute filters** efficiently
3. **Limit result sets** with appropriate `top` values
4. **Cache frequently used searches**

### Error Handling

```python
def safe_geolocation_search(client, lat, lon, radius):
    """Geolocation search with comprehensive error handling."""
    
    try:
        # Validate inputs
        validate_coordinates(lat, lon)
        
        if radius <= 0 or radius > 100:
            raise ValueError("Radius must be between 0 and 100 miles")
        
        # Perform search
        return search_by_radius(client, lat, lon, radius)
        
    except ValueError as e:
        print(f"Input validation error: {e}")
        return []
    
    except Exception as e:
        print(f"Search error: {e}")
        return []
```

## Related Resources

- [OData Queries Guide](odata-queries.md) - Advanced filtering techniques
- [Property Search Guide](property-search.md) - Property-specific search strategies
- [Error Handling Guide](error-handling.md) - Handling API errors