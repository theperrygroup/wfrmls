# Property Search Guide

Master advanced property filtering, sorting, and search techniques with the WFRMLS Python client.

---

## 🎯 Overview

This guide covers everything you need to know about searching for properties using the WFRMLS API, from basic queries to advanced filtering and geolocation searches.

### What You'll Learn

- **Basic property retrieval** - Getting started with simple queries
- **Advanced filtering** - Complex search criteria and combinations
- **Sorting and pagination** - Organizing and managing large result sets
- **Field selection** - Optimizing performance by requesting specific fields
- **Common search patterns** - Real-world use cases and examples

---

## 🚀 Basic Property Search

### Simple Property Retrieval

```python
from wfrmls import WFRMLSClient

# Initialize client
client = WFRMLSClient()

# Get first 10 active properties
properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    top=10
)

print(f"Found {len(properties)} active properties")
for prop in properties:
    print(f"  {prop['ListingId']}: ${prop['ListPrice']:,} in {prop.get('City', 'Unknown')}")
```

### Basic Filtering

```python
# Properties under $500,000
affordable_homes = client.property.get_properties(
    filter_query="ListPrice le 500000 and StandardStatus eq 'Active'",
    top=20,
    orderby="ListPrice asc"
)

# Properties with 3+ bedrooms
family_homes = client.property.get_properties(
    filter_query="BedroomsTotal ge 3 and StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "BedroomsTotal", "City"],
    top=15
)
```

---

## 🔍 Advanced Filtering

### Price Range Searches

```python
def search_by_price_range(min_price=None, max_price=None):
    """Search properties within a specific price range."""
    
    filters = ["StandardStatus eq 'Active'"]
    
    if min_price:
        filters.append(f"ListPrice ge {min_price}")
    if max_price:
        filters.append(f"ListPrice le {max_price}")
    
    filter_query = " and ".join(filters)
    
    return client.property.get_properties(
        filter_query=filter_query,
        select=["ListingId", "ListPrice", "City", "BedroomsTotal"],
        orderby="ListPrice asc"
    )

# Usage examples
luxury_homes = search_by_price_range(min_price=750000)
mid_range = search_by_price_range(min_price=300000, max_price=600000)
affordable = search_by_price_range(max_price=250000)
```

### Location-Based Searches

```python
# Properties in specific cities
salt_lake_properties = client.property.get_properties(
    filter_query="City eq 'Salt Lake City' and StandardStatus eq 'Active'",
    select=["ListingId", "Address", "ListPrice", "BedroomsTotal"],
    orderby="ListPrice desc"
)

# Multiple cities
utah_county_cities = client.property.get_properties(
    filter_query=(
        "(City eq 'Provo' or City eq 'Orem' or City eq 'American Fork') "
        "and StandardStatus eq 'Active'"
    ),
    top=50
)

# Zip code searches
specific_zip = client.property.get_properties(
    filter_query="PostalCode eq '84604' and StandardStatus eq 'Active'"
)
```

### Property Type and Features

```python
# Single-family homes only
single_family = client.property.get_properties(
    filter_query=(
        "PropertyType eq 'Residential' "
        "and StandardStatus eq 'Active'"
    )
)

# Condos and townhomes
condos = client.property.get_properties(
    filter_query=(
        "PropertyType eq 'Condominium' "
        "and StandardStatus eq 'Active'"
    )
)

# New construction
new_homes = client.property.get_properties(
    filter_query=(
        "YearBuilt ge 2020 "
        "and StandardStatus eq 'Active'"
    ),
    orderby="YearBuilt desc"
)

# Properties with garages
with_garage = client.property.get_properties(
    filter_query=(
        "Garage ne null "
        "and StandardStatus eq 'Active'"
    )
)
```

### Time-Based Searches

```python
from datetime import datetime, timedelta

# Recently listed properties (last 7 days)
week_ago = (datetime.now() - timedelta(days=7)).isoformat()

recent_listings = client.property.get_properties(
    filter_query=f"OnMarketDate ge {week_ago}",
    orderby="OnMarketDate desc",
    top=25
)

# Properties with recent price changes
price_reductions = client.property.get_properties(
    filter_query=(
        f"PriceChangeTimestamp ge {week_ago} "
        "and ListPrice lt OriginalListPrice"
    ),
    select=["ListingId", "ListPrice", "OriginalListPrice", "PriceChangeTimestamp"],
    orderby="PriceChangeTimestamp desc"
)

# Properties on market for extended period
thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

stale_listings = client.property.get_properties(
    filter_query=f"OnMarketDate le {thirty_days_ago} and StandardStatus eq 'Active'",
    orderby="OnMarketDate asc"
)
```

---

## 📊 Sorting and Pagination

### Custom Sorting

```python
# Sort by price (ascending)
by_price_low = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="ListPrice asc",
    top=20
)

# Sort by price (descending)
by_price_high = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="ListPrice desc",
    top=20
)

# Multiple sort criteria
multi_sort = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="City asc, ListPrice desc",
    top=50
)

# Sort by recently updated
recently_updated = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    orderby="ModificationTimestamp desc",
    top=30
)
```

### Pagination Patterns

```python
def paginate_all_properties(page_size=100):
    """Retrieve all active properties using pagination."""
    
    all_properties = []
    skip = 0
    
    while True:
        # Get next page
        page = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            top=page_size,
            skip=skip,
            orderby="ListingId asc"  # Consistent ordering
        )
        
        if not page:
            break
            
        all_properties.extend(page)
        skip += page_size
        
        print(f"Retrieved {len(all_properties)} properties so far...")
        
        # Rate limiting
        import time
        time.sleep(0.1)
    
    return all_properties

# Get specific page
def get_property_page(page_number, page_size=50):
    """Get a specific page of properties."""
    skip = (page_number - 1) * page_size
    
    return client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        top=page_size,
        skip=skip,
        orderby="ListPrice desc"
    )

# Usage
page_1 = get_property_page(1)
page_2 = get_property_page(2)
page_3 = get_property_page(3)
```

---

## ⚡ Performance Optimization

### Field Selection

```python
# Request only needed fields for better performance
minimal_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    select=[
        "ListingId",
        "ListPrice", 
        "City",
        "BedroomsTotal",
        "BathroomsTotalInteger"
    ],
    top=100
)

# For map displays
map_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and Latitude ne null and Longitude ne null",
    select=[
        "ListingId",
        "ListPrice",
        "Address",
        "Latitude",
        "Longitude"
    ],
    top=200
)

# For detailed listings
detailed_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",
    select=[
        "ListingId", "ListPrice", "Address", "City", "PostalCode",
        "BedroomsTotal", "BathroomsTotalInteger", "SquareFeet",
        "YearBuilt", "PropertyType", "Garage", "ListAgentKey"
    ],
    top=25
)
```

### Caching Strategies

```python
import time
from functools import lru_cache

class PropertySearchCache:
    """Cache property searches for better performance."""
    
    def __init__(self, client, cache_duration=300):  # 5 minutes
        self.client = client
        self.cache_duration = cache_duration
        self._cache = {}
    
    def search_properties(self, filter_query, **kwargs):
        """Search with caching."""
        cache_key = f"{filter_query}_{hash(str(sorted(kwargs.items())))}"
        
        # Check cache
        if cache_key in self._cache:
            result, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return result
        
        # Fetch fresh data
        result = self.client.property.get_properties(
            filter_query=filter_query,
            **kwargs
        )
        
        # Cache result
        self._cache[cache_key] = (result, time.time())
        
        return result

# Usage
cached_search = PropertySearchCache(client)

# These will be cached
results1 = cached_search.search_properties("StandardStatus eq 'Active'", top=50)
results2 = cached_search.search_properties("StandardStatus eq 'Active'", top=50)  # From cache
```

---

## 🎯 Common Search Patterns

### Property Finder Interface

```python
class PropertyFinder:
    """Advanced property search interface."""
    
    def __init__(self, client):
        self.client = client
    
    def search(self, criteria):
        """Search with flexible criteria dictionary."""
        filters = ["StandardStatus eq 'Active'"]
        
        # Price range
        if criteria.get('min_price'):
            filters.append(f"ListPrice ge {criteria['min_price']}")
        if criteria.get('max_price'):
            filters.append(f"ListPrice le {criteria['max_price']}")
        
        # Location
        if criteria.get('city'):
            filters.append(f"City eq '{criteria['city']}'")
        if criteria.get('zip_code'):
            filters.append(f"PostalCode eq '{criteria['zip_code']}'")
        
        # Property details
        if criteria.get('min_bedrooms'):
            filters.append(f"BedroomsTotal ge {criteria['min_bedrooms']}")
        if criteria.get('min_bathrooms'):
            filters.append(f"BathroomsTotalInteger ge {criteria['min_bathrooms']}")
        
        # Property type
        if criteria.get('property_type'):
            filters.append(f"PropertyType eq '{criteria['property_type']}'")
        
        # Age restrictions
        if criteria.get('max_age_years'):
            min_year = datetime.now().year - criteria['max_age_years']
            filters.append(f"YearBuilt ge {min_year}")
        
        filter_query = " and ".join(filters)
        
        return self.client.property.get_properties(
            filter_query=filter_query,
            orderby=criteria.get('sort_by', 'ListPrice asc'),
            top=criteria.get('limit', 50),
            select=criteria.get('fields')
        )

# Usage
finder = PropertyFinder(client)

# Family home search
family_criteria = {
    'min_price': 300000,
    'max_price': 600000,
    'min_bedrooms': 3,
    'min_bathrooms': 2,
    'city': 'Provo',
    'property_type': 'Residential',
    'max_age_years': 20,
    'sort_by': 'ListPrice asc',
    'limit': 25
}

family_homes = finder.search(family_criteria)
```

### Investment Property Search

```python
def find_investment_properties():
    """Find properties suitable for investment."""
    
    # Multi-family properties
    multi_family = client.property.get_properties(
        filter_query=(
            "PropertyType eq 'Multi-Family' "
            "and StandardStatus eq 'Active'"
        ),
        select=[
            "ListingId", "ListPrice", "Address", "City",
            "PropertyType", "YearBuilt", "SquareFeet"
        ]
    )
    
    # Fixer-uppers (older properties, lower price)
    fixers = client.property.get_properties(
        filter_query=(
            "YearBuilt le 1980 "
            "and ListPrice le 300000 "
            "and StandardStatus eq 'Active'"
        ),
        orderby="ListPrice asc"
    )
    
    # Cash flow analysis
    def estimate_cash_flow(property_data):
        """Rough cash flow estimation."""
        price = property_data.get('ListPrice', 0)
        
        # Rule of thumb: 1% rule
        monthly_rent_estimate = price * 0.01
        monthly_payment_estimate = price * 0.006  # Rough mortgage payment
        
        return {
            'property_id': property_data['ListingId'],
            'price': price,
            'estimated_rent': monthly_rent_estimate,
            'estimated_payment': monthly_payment_estimate,
            'estimated_cash_flow': monthly_rent_estimate - monthly_payment_estimate
        }
    
    # Analyze potential investments
    for prop in multi_family[:5]:
        analysis = estimate_cash_flow(prop)
        print(f"Property {analysis['property_id']}: "
              f"${analysis['estimated_cash_flow']:,.0f}/month cash flow")
    
    return {
        'multi_family': multi_family,
        'fixers': fixers
    }
```

### Market Analysis Search

```python
def analyze_market_trends(city_name):
    """Analyze market trends for a specific city."""
    
    # Current active listings
    active_listings = client.property.get_properties(
        filter_query=f"City eq '{city_name}' and StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice", "BedroomsTotal", "SquareFeet", "OnMarketDate"]
    )
    
    # Recently sold (if available)
    # Note: Adjust date range as needed
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    
    recent_sales = client.property.get_properties(
        filter_query=(
            f"City eq '{city_name}' "
            f"and StandardStatus eq 'Sold' "
            f"and ModificationTimestamp ge {thirty_days_ago}"
        ),
        select=["ListingId", "ListPrice", "BedroomsTotal", "SquareFeet"]
    )
    
    # Analysis
    if active_listings:
        prices = [p['ListPrice'] for p in active_listings if p.get('ListPrice')]
        
        analysis = {
            'city': city_name,
            'active_count': len(active_listings),
            'recent_sales_count': len(recent_sales),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'median_price': sorted(prices)[len(prices)//2] if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'price_per_sqft': 0  # Calculate if square footage available
        }
        
        # Price per square foot
        sqft_data = [(p['ListPrice'], p['SquareFeet']) 
                     for p in active_listings 
                     if p.get('ListPrice') and p.get('SquareFeet')]
        
        if sqft_data:
            price_per_sqft = [price / sqft for price, sqft in sqft_data]
            analysis['price_per_sqft'] = sum(price_per_sqft) / len(price_per_sqft)
        
        return analysis
    
    return None

# Analyze multiple markets
cities = ['Salt Lake City', 'Provo', 'Ogden', 'West Jordan']
for city in cities:
    stats = analyze_market_trends(city)
    if stats:
        print(f"\n{city} Market Analysis:")
        print(f"  Active Listings: {stats['active_count']}")
        print(f"  Average Price: ${stats['avg_price']:,.0f}")
        print(f"  Median Price: ${stats['median_price']:,.0f}")
        if stats['price_per_sqft']:
            print(f"  Price/SqFt: ${stats['price_per_sqft']:.0f}")
```

---

## 📚 Next Steps

### **Advanced Topics**
- **[Geolocation Queries](geolocation.md)** - Location-based searches with coordinates
- **[OData Queries](odata-queries.md)** - Master complex query syntax
- **[Data Synchronization](data-sync.md)** - Keep your data up to date

### **Related Examples**
- **[Advanced Queries](../examples/advanced-queries.md)** - Complex search examples
- **[Real Estate Apps](../examples/real-estate-apps.md)** - Complete applications
- **[Data Integration](../examples/data-integration.md)** - Database integration

### **API Reference**
- **[Properties API](../api/properties.md)** - Complete method documentation
- **[Field Reference](../reference/fields.md)** - Available property fields
- **[Status Codes](../reference/status-codes.md)** - Response codes and meanings

---

*Ready to dive deeper? Try our [Geolocation Queries](geolocation.md) guide for location-based searches.* 