# Geolocation Search Guide

This guide covers how to perform location-based property searches using the WFRMLS API, including radius searches, polygon boundaries, and coordinate-based filtering.

---

## Overview

The WFRMLS API supports several types of geolocation searches:

- **Radius searches** - Find properties within a specific distance from a point
- **Polygon searches** - Find properties within custom boundary shapes
- **Coordinate filtering** - Filter by latitude/longitude ranges
- **Address-based searches** - Search by city, ZIP code, or address components

---

## Coordinate System

The WFRMLS system uses the **WGS84** coordinate system (EPSG:4326) with:

- **Latitude**: North-South position (-90 to +90 degrees)
- **Longitude**: East-West position (-180 to +180 degrees)

### Utah Coordinate Ranges

| Region | Latitude Range | Longitude Range |
|--------|----------------|-----------------|
| **Northern Utah** | 41.0° to 42.0° | -112.1° to -111.0° |
| **Salt Lake Valley** | 40.5° to 40.8° | -112.0° to -111.7° |
| **Utah Valley** | 40.2° to 40.5° | -111.9° to -111.5° |
| **Southern Utah** | 37.0° to 40.2° | -114.0° to -109.0° |

---

## Radius Searches

### Basic Radius Search

Find properties within a specific distance from a center point:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Search within 5 miles of downtown Salt Lake City
center_lat = 40.7608
center_lon = -111.8910
radius_miles = 5

properties = client.property.get_properties(
    filter_query=f"geo.distance(Latitude, Longitude, {center_lat}, {center_lon}) le {radius_miles}",
    select=[
        "ListingId", "ListPrice", "PropertyAddress", "PropertyCity",
        "Latitude", "Longitude", "BedroomsTotal", "BathroomsTotalInteger"
    ],
    orderby="ListPrice asc",
    top=50
)

for prop in properties:
    print(f"{prop['PropertyAddress']}, {prop['PropertyCity']} - ${prop['ListPrice']:,}")
```

### Distance Calculation

Calculate the actual distance from your search center:

```python
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in miles using Haversine formula."""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    
    return c * r

# Example usage with search results
center_lat, center_lon = 40.7608, -111.8910

for prop in properties:
    if prop.get('Latitude') and prop.get('Longitude'):
        distance = calculate_distance(
            center_lat, center_lon,
            float(prop['Latitude']), float(prop['Longitude'])
        )
        print(f"{prop['PropertyAddress']} - {distance:.2f} miles away")
```

### Multiple Radius Searches

Search multiple areas simultaneously:

```python
# Define multiple search centers
search_areas = [
    {"name": "Downtown SLC", "lat": 40.7608, "lon": -111.8910, "radius": 3},
    {"name": "University of Utah", "lat": 40.7649, "lon": -111.8421, "radius": 2},
    {"name": "Sugar House", "lat": 40.7141, "lon": -111.8538, "radius": 2.5}
]

all_properties = []

for area in search_areas:
    area_properties = client.property.get_properties(
        filter_query=f"geo.distance(Latitude, Longitude, {area['lat']}, {area['lon']}) le {area['radius']} and StandardStatus eq 'Active'",
        select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
        top=100
    )
    
    # Add area information to each property
    for prop in area_properties:
        prop['SearchArea'] = area['name']
        prop['SearchRadius'] = area['radius']
    
    all_properties.extend(area_properties)

# Remove duplicates (properties that appear in multiple search areas)
unique_properties = {}
for prop in all_properties:
    listing_id = prop['ListingId']
    if listing_id not in unique_properties:
        unique_properties[listing_id] = prop

print(f"Found {len(unique_properties)} unique properties across all search areas")
```

---

## Polygon Searches

### Custom Boundary Search

Define a custom polygon boundary and find properties within it:

```python
def point_in_polygon(lat, lon, polygon_coords):
    """Check if a point is inside a polygon using ray casting algorithm."""
    x, y = lon, lat
    n = len(polygon_coords)
    inside = False
    
    p1x, p1y = polygon_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

# Define a polygon around downtown Salt Lake City
downtown_polygon = [
    (-111.9100, 40.7500),  # Southwest corner
    (-111.8700, 40.7500),  # Southeast corner
    (-111.8700, 40.7700),  # Northeast corner
    (-111.9100, 40.7700),  # Northwest corner
]

# Get properties in a broader area first
broad_search = client.property.get_properties(
    filter_query="Latitude ge 40.7400 and Latitude le 40.7800 and Longitude ge -111.9200 and Longitude le -111.8600",
    select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
    top=500
)

# Filter to only properties within the polygon
polygon_properties = []
for prop in broad_search:
    if prop.get('Latitude') and prop.get('Longitude'):
        lat, lon = float(prop['Latitude']), float(prop['Longitude'])
        if point_in_polygon(lat, lon, downtown_polygon):
            polygon_properties.append(prop)

print(f"Found {len(polygon_properties)} properties within the downtown polygon")
```

### School District Boundaries

Search within specific school district boundaries:

```python
# Example: Search within a specific school district
# (You would need actual boundary coordinates for real implementation)

def search_by_school_district(district_name, boundary_coords):
    """Search for properties within a school district boundary."""
    
    # Get bounding box for initial filter
    lats = [coord[1] for coord in boundary_coords]
    lons = [coord[0] for coord in boundary_coords]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Initial broad search within bounding box
    properties = client.property.get_properties(
        filter_query=f"Latitude ge {min_lat} and Latitude le {max_lat} and Longitude ge {min_lon} and Longitude le {max_lon} and StandardStatus eq 'Active'",
        select=[
            "ListingId", "PropertyAddress", "PropertyCity", "ListPrice",
            "Latitude", "Longitude", "BedroomsTotal", "PublicSchoolDistrict"
        ],
        top=1000
    )
    
    # Filter to properties within the actual boundary
    district_properties = []
    for prop in properties:
        if prop.get('Latitude') and prop.get('Longitude'):
            lat, lon = float(prop['Latitude']), float(prop['Longitude'])
            if point_in_polygon(lat, lon, boundary_coords):
                district_properties.append(prop)
    
    return district_properties

# Example usage (with hypothetical boundary coordinates)
granite_district_boundary = [
    (-111.9500, 40.6000),
    (-111.8000, 40.6000),
    (-111.8000, 40.7500),
    (-111.9500, 40.7500),
]

granite_properties = search_by_school_district("Granite School District", granite_district_boundary)
```

---

## Coordinate Range Filtering

### Bounding Box Search

Search within a rectangular area defined by coordinate ranges:

```python
# Define bounding box for Salt Lake Valley
north_lat = 40.8000
south_lat = 40.6000
east_lon = -111.7000
west_lon = -111.9500

valley_properties = client.property.get_properties(
    filter_query=f"Latitude ge {south_lat} and Latitude le {north_lat} and Longitude ge {west_lon} and Longitude le {east_lon} and StandardStatus eq 'Active'",
    select=[
        "ListingId", "PropertyAddress", "PropertyCity", "PropertyStateOrProvince",
        "ListPrice", "Latitude", "Longitude", "LivingArea"
    ],
    orderby="ListPrice desc",
    top=200
)

print(f"Found {len(valley_properties)} properties in Salt Lake Valley")

# Group by city
from collections import defaultdict
properties_by_city = defaultdict(list)

for prop in valley_properties:
    city = prop.get('PropertyCity', 'Unknown')
    properties_by_city[city].append(prop)

for city, props in properties_by_city.items():
    avg_price = sum(float(p.get('ListPrice', 0)) for p in props) / len(props)
    print(f"{city}: {len(props)} properties, avg price: ${avg_price:,.0f}")
```

### Grid-Based Search

Divide an area into a grid and search each cell:

```python
def grid_search(north_lat, south_lat, east_lon, west_lon, grid_size=5):
    """Divide area into grid and search each cell."""
    
    lat_step = (north_lat - south_lat) / grid_size
    lon_step = (east_lon - west_lon) / grid_size
    
    grid_results = []
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate cell boundaries
            cell_south = south_lat + (i * lat_step)
            cell_north = south_lat + ((i + 1) * lat_step)
            cell_west = west_lon + (j * lon_step)
            cell_east = west_lon + ((j + 1) * lon_step)
            
            # Search this grid cell
            cell_properties = client.property.get_properties(
                filter_query=f"Latitude ge {cell_south} and Latitude le {cell_north} and Longitude ge {cell_west} and Longitude le {cell_east} and StandardStatus eq 'Active'",
                select=["ListingId", "ListPrice", "Latitude", "Longitude"],
                top=100
            )
            
            if cell_properties:
                grid_results.append({
                    'grid_cell': f"{i},{j}",
                    'bounds': {
                        'north': cell_north, 'south': cell_south,
                        'east': cell_east, 'west': cell_west
                    },
                    'property_count': len(cell_properties),
                    'properties': cell_properties
                })
    
    return grid_results

# Search Salt Lake Valley in a 5x5 grid
grid_results = grid_search(40.8000, 40.6000, -111.7000, -111.9500, 5)

for cell in grid_results:
    print(f"Grid cell {cell['grid_cell']}: {cell['property_count']} properties")
```

---

## Address-Based Searches

### City and ZIP Code Filtering

```python
# Search by city
salt_lake_properties = client.property.get_properties(
    filter_query="PropertyCity eq 'Salt Lake City' and StandardStatus eq 'Active'",
    select=["ListingId", "PropertyAddress", "ListPrice", "PropertyPostalCode"],
    orderby="ListPrice asc",
    top=100
)

# Search by ZIP code
zip_84102_properties = client.property.get_properties(
    filter_query="PropertyPostalCode eq '84102' and StandardStatus eq 'Active'",
    select=["ListingId", "PropertyAddress", "ListPrice", "PropertyCity"],
    top=50
)

# Search multiple ZIP codes
zip_codes = ['84102', '84103', '84105', '84106']
zip_filter = " or ".join([f"PropertyPostalCode eq '{zip_code}'" for zip_code in zip_codes])

multi_zip_properties = client.property.get_properties(
    filter_query=f"({zip_filter}) and StandardStatus eq 'Active'",
    select=["ListingId", "PropertyAddress", "ListPrice", "PropertyPostalCode"],
    orderby="PropertyPostalCode asc, ListPrice asc"
)
```

### Neighborhood Searches

```python
# Search by neighborhood or subdivision
def search_by_neighborhood(neighborhood_name):
    """Search for properties in a specific neighborhood."""
    
    # Try multiple fields that might contain neighborhood information
    neighborhood_filters = [
        f"contains(PropertySubdivisionName, '{neighborhood_name}')",
        f"contains(PropertyAddress, '{neighborhood_name}')",
        f"contains(PublicRemarks, '{neighborhood_name}')"
    ]
    
    filter_query = f"({' or '.join(neighborhood_filters)}) and StandardStatus eq 'Active'"
    
    properties = client.property.get_properties(
        filter_query=filter_query,
        select=[
            "ListingId", "PropertyAddress", "PropertyCity", "ListPrice",
            "PropertySubdivisionName", "Latitude", "Longitude"
        ],
        orderby="ListPrice asc"
    )
    
    return properties

# Search for properties in "Avenues" neighborhood
avenues_properties = search_by_neighborhood("Avenues")
print(f"Found {len(avenues_properties)} properties in Avenues neighborhood")

# Search for properties in "Sugar House"
sugar_house_properties = search_by_neighborhood("Sugar House")
print(f"Found {len(sugar_house_properties)} properties in Sugar House area")
```

---

## Advanced Geolocation Techniques

### Commute-Based Search

Find properties within a certain commute time/distance from a workplace:

```python
def commute_based_search(workplace_lat, workplace_lon, max_commute_miles=15):
    """Find properties within commuting distance of a workplace."""
    
    # Use radius search as a starting point
    commute_properties = client.property.get_properties(
        filter_query=f"geo.distance(Latitude, Longitude, {workplace_lat}, {workplace_lon}) le {max_commute_miles} and StandardStatus eq 'Active'",
        select=[
            "ListingId", "PropertyAddress", "PropertyCity", "ListPrice",
            "Latitude", "Longitude", "BedroomsTotal", "BathroomsTotalInteger"
        ],
        top=200
    )
    
    # Calculate actual distances and add commute information
    for prop in commute_properties:
        if prop.get('Latitude') and prop.get('Longitude'):
            distance = calculate_distance(
                workplace_lat, workplace_lon,
                float(prop['Latitude']), float(prop['Longitude'])
            )
            prop['CommuteDistance'] = round(distance, 2)
            
            # Estimate commute time (assuming average 30 mph in city)
            prop['EstimatedCommuteTime'] = round(distance * 2, 0)  # minutes
    
    # Sort by commute distance
    commute_properties.sort(key=lambda x: x.get('CommuteDistance', float('inf')))
    
    return commute_properties

# Find properties within 10 miles of downtown Salt Lake City
downtown_commute = commute_based_search(40.7608, -111.8910, 10)

print("Properties sorted by commute distance:")
for prop in downtown_commute[:10]:  # Show top 10
    print(f"{prop['PropertyAddress']} - {prop['CommuteDistance']} miles ({prop['EstimatedCommuteTime']} min)")
```

### Multi-Point Search

Find properties that are convenient to multiple important locations:

```python
def multi_point_search(important_locations, max_total_distance=20):
    """Find properties that are convenient to multiple locations."""
    
    # Calculate bounding box that encompasses all important locations
    lats = [loc['lat'] for loc in important_locations]
    lons = [loc['lon'] for loc in important_locations]
    
    min_lat, max_lat = min(lats) - 0.1, max(lats) + 0.1
    min_lon, max_lon = min(lons) - 0.1, max(lons) + 0.1
    
    # Get properties in the general area
    properties = client.property.get_properties(
        filter_query=f"Latitude ge {min_lat} and Latitude le {max_lat} and Longitude ge {min_lon} and Longitude le {max_lon} and StandardStatus eq 'Active'",
        select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
        top=500
    )
    
    # Calculate total distance to all important locations
    suitable_properties = []
    
    for prop in properties:
        if prop.get('Latitude') and prop.get('Longitude'):
            prop_lat, prop_lon = float(prop['Latitude']), float(prop['Longitude'])
            
            total_distance = 0
            distances = {}
            
            for location in important_locations:
                distance = calculate_distance(
                    prop_lat, prop_lon,
                    location['lat'], location['lon']
                )
                distances[location['name']] = distance
                total_distance += distance
            
            if total_distance <= max_total_distance:
                prop['TotalDistance'] = round(total_distance, 2)
                prop['DistancesToLocations'] = distances
                suitable_properties.append(prop)
    
    # Sort by total distance
    suitable_properties.sort(key=lambda x: x['TotalDistance'])
    
    return suitable_properties

# Example: Find properties convenient to work, school, and shopping
important_locations = [
    {"name": "Work", "lat": 40.7608, "lon": -111.8910},      # Downtown SLC
    {"name": "School", "lat": 40.7649, "lon": -111.8421},    # University of Utah
    {"name": "Shopping", "lat": 40.6892, "lon": -111.8447}   # Fashion Place Mall
]

convenient_properties = multi_point_search(important_locations, 25)

print("Properties convenient to all locations:")
for prop in convenient_properties[:5]:  # Show top 5
    print(f"\n{prop['PropertyAddress']} - Total distance: {prop['TotalDistance']} miles")
    for location, distance in prop['DistancesToLocations'].items():
        print(f"  {location}: {distance:.1f} miles")
```

---

## Performance Optimization

### Efficient Coordinate Queries

```python
# Use indexed fields for better performance
def optimized_geo_search(center_lat, center_lon, radius_miles):
    """Optimized geolocation search using bounding box pre-filter."""
    
    # Calculate approximate bounding box (1 degree ≈ 69 miles)
    lat_delta = radius_miles / 69.0
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(center_lat)))
    
    min_lat = center_lat - lat_delta
    max_lat = center_lat + lat_delta
    min_lon = center_lon - lon_delta
    max_lon = center_lon + lon_delta
    
    # First filter by bounding box (fast), then by exact distance
    properties = client.property.get_properties(
        filter_query=f"Latitude ge {min_lat} and Latitude le {max_lat} and Longitude ge {min_lon} and Longitude le {max_lon} and geo.distance(Latitude, Longitude, {center_lat}, {center_lon}) le {radius_miles}",
        select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
        top=100
    )
    
    return properties
```

### Caching Geolocation Results

```python
from functools import lru_cache
from datetime import datetime, timedelta

class GeoSearchCache:
    def __init__(self, client):
        self.client = client
        self._cache = {}
        self._cache_timeout = timedelta(hours=1)
    
    def _cache_key(self, lat, lon, radius, filters=""):
        """Generate cache key for search parameters."""
        return f"{lat:.4f},{lon:.4f},{radius},{hash(filters)}"
    
    def radius_search(self, center_lat, center_lon, radius_miles, additional_filters=""):
        """Cached radius search."""
        cache_key = self._cache_key(center_lat, center_lon, radius_miles, additional_filters)
        now = datetime.now()
        
        # Check cache
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if now - timestamp < self._cache_timeout:
                return cached_data
        
        # Perform search
        base_filter = f"geo.distance(Latitude, Longitude, {center_lat}, {center_lon}) le {radius_miles}"
        if additional_filters:
            filter_query = f"{base_filter} and {additional_filters}"
        else:
            filter_query = base_filter
        
        properties = self.client.property.get_properties(
            filter_query=filter_query,
            select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
            top=200
        )
        
        # Cache results
        self._cache[cache_key] = (properties, now)
        
        return properties

# Usage
geo_cache = GeoSearchCache(client)

# This will hit the API
properties1 = geo_cache.radius_search(40.7608, -111.8910, 5, "StandardStatus eq 'Active'")

# This will use cached results
properties2 = geo_cache.radius_search(40.7608, -111.8910, 5, "StandardStatus eq 'Active'")
```

---

## Error Handling and Validation

### Coordinate Validation

```python
def validate_coordinates(lat, lon):
    """Validate latitude and longitude values."""
    errors = []
    
    if not isinstance(lat, (int, float)):
        errors.append("Latitude must be a number")
    elif not -90 <= lat <= 90:
        errors.append("Latitude must be between -90 and 90 degrees")
    
    if not isinstance(lon, (int, float)):
        errors.append("Longitude must be a number")
    elif not -180 <= lon <= 180:
        errors.append("Longitude must be between -180 and 180 degrees")
    
    # Check if coordinates are within Utah bounds (rough check)
    if errors == []:  # Only check if basic validation passed
        if not (37.0 <= lat <= 42.0):
            errors.append("Latitude appears to be outside Utah")
        if not (-114.0 <= lon <= -109.0):
            errors.append("Longitude appears to be outside Utah")
    
    return errors

# Example usage
def safe_geo_search(center_lat, center_lon, radius_miles):
    """Perform geolocation search with validation."""
    
    # Validate coordinates
    coord_errors = validate_coordinates(center_lat, center_lon)
    if coord_errors:
        raise ValueError(f"Invalid coordinates: {', '.join(coord_errors)}")
    
    # Validate radius
    if not isinstance(radius_miles, (int, float)) or radius_miles <= 0:
        raise ValueError("Radius must be a positive number")
    
    if radius_miles > 50:
        raise ValueError("Radius cannot exceed 50 miles")
    
    try:
        properties = client.property.get_properties(
            filter_query=f"geo.distance(Latitude, Longitude, {center_lat}, {center_lon}) le {radius_miles}",
            select=["ListingId", "PropertyAddress", "ListPrice", "Latitude", "Longitude"],
            top=100
        )
        return properties
        
    except Exception as e:
        print(f"Geolocation search failed: {e}")
        return []

# Usage with error handling
try:
    results = safe_geo_search(40.7608, -111.8910, 5)
    print(f"Found {len(results)} properties")
except ValueError as e:
    print(f"Search parameter error: {e}")
```

---

## Related Resources

- **[Property API](../api/properties.md)** - Complete property search documentation
- **[OData Queries Guide](odata-queries.md)** - Advanced filtering syntax
- **[Property Search Guide](property-search.md)** - General property search techniques
- **[Error Handling Guide](error-handling.md)** - Robust error management