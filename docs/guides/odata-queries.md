# OData Queries Guide

Master complex filtering and querying using OData syntax with the WFRMLS Python client.

---

## 🎯 Overview

The WFRMLS API follows the OData (Open Data Protocol) v4 standard for querying and filtering data. This guide covers everything you need to know about building powerful queries to find exactly the data you need.

### What You'll Learn

- **OData fundamentals** - Understanding the query syntax and structure
- **Filtering operators** - All available comparison and logical operators
- **Advanced queries** - Complex multi-field filtering and nested conditions
- **Functions and expressions** - Built-in functions for string, date, and math operations
- **Performance optimization** - Writing efficient queries that minimize API usage

---

## 📚 OData Fundamentals

### Basic Query Structure

OData queries use URL parameters to specify what data to retrieve and how to filter it:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Basic structure
properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'",  # $filter
    select=["ListingId", "ListPrice"],          # $select
    orderby="ListPrice desc",                   # $orderby
    top=50,                                     # $top
    skip=100,                                   # $skip
    count=True                                  # $count
)
```

### Query Parameters

| Parameter | OData Name | Purpose | Example |
|-----------|------------|---------|---------|
| **`filter_query`** | `$filter` | Filter records | `"ListPrice gt 500000"` |
| **`select`** | `$select` | Choose specific fields | `["ListingId", "ListPrice"]` |
| **`orderby`** | `$orderby` | Sort results | `"ListPrice desc"` |
| **`top`** | `$top` | Limit number of results | `50` |
| **`skip`** | `$skip` | Skip first N results | `100` |
| **`count`** | `$count` | Include total count | `True` |

---

## 🔍 Filtering Operators

### Comparison Operators

```python
# Equal to
active_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'"
)

# Not equal to
non_pending = client.property.get_properties(
    filter_query="StandardStatus ne 'Pending'"
)

# Greater than
expensive_homes = client.property.get_properties(
    filter_query="ListPrice gt 750000"
)

# Greater than or equal
luxury_homes = client.property.get_properties(
    filter_query="ListPrice ge 1000000"
)

# Less than
affordable_homes = client.property.get_properties(
    filter_query="ListPrice lt 300000"
)

# Less than or equal
budget_homes = client.property.get_properties(
    filter_query="ListPrice le 250000"
)
```

### String Operators

```python
# Contains substring
lake_properties = client.property.get_properties(
    filter_query="contains(City, 'Lake')"
)

# Starts with
south_addresses = client.property.get_properties(
    filter_query="startswith(Address, 'South')"
)

# Ends with
street_addresses = client.property.get_properties(
    filter_query="endswith(Address, 'Street')"
)

# Case-insensitive contains
case_insensitive = client.property.get_properties(
    filter_query="contains(tolower(City), 'salt lake')"
)

# String length
short_cities = client.property.get_properties(
    filter_query="length(City) lt 10"
)
```

### Null Value Checks

```python
# Field is not null
with_coordinates = client.property.get_properties(
    filter_query="Latitude ne null and Longitude ne null"
)

# Field is null
no_garage = client.property.get_properties(
    filter_query="Garage eq null"
)

# Check for empty strings (not null but empty)
has_description = client.property.get_properties(
    filter_query="PublicRemarks ne null and PublicRemarks ne ''"
)
```

---

## 🧮 Logical Operators

### AND Operations

```python
# Multiple conditions must be true
family_homes = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "BedroomsTotal ge 3 and "
        "BathroomsTotalInteger ge 2 and "
        "ListPrice le 600000"
    )
)

# Complex AND with grouping
target_properties = client.property.get_properties(
    filter_query=(
        "(City eq 'Provo' or City eq 'Orem') and "
        "ListPrice ge 400000 and "
        "PropertyType eq 'Residential'"
    )
)
```

### OR Operations

```python
# Any condition can be true
multi_city = client.property.get_properties(
    filter_query=(
        "City eq 'Salt Lake City' or "
        "City eq 'Provo' or "
        "City eq 'Ogden'"
    )
)

# Complex OR with different field types
flexible_search = client.property.get_properties(
    filter_query=(
        "ListPrice le 300000 or "
        "BedroomsTotal ge 5 or "
        "contains(PublicRemarks, 'motivated seller')"
    )
)
```

### NOT Operations

```python
# Negation with parentheses
not_condo = client.property.get_properties(
    filter_query="not (PropertyType eq 'Condominium')"
)

# Multiple negations
exclusions = client.property.get_properties(
    filter_query=(
        "StandardStatus eq 'Active' and "
        "not (contains(City, 'West')) and "
        "not (ListPrice gt 1000000)"
    )
)
```

---

## 📅 Date and Time Queries

### Date Filtering

```python
from datetime import datetime, timedelta

# Recent listings (last 30 days)
thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

recent_listings = client.property.get_properties(
    filter_query=f"OnMarketDate ge {thirty_days_ago}"
)

# Specific date range
start_date = "2024-01-01T00:00:00Z"
end_date = "2024-01-31T23:59:59Z"

january_listings = client.property.get_properties(
    filter_query=f"OnMarketDate ge {start_date} and OnMarketDate le {end_date}"
)

# Properties modified today
today = datetime.now().date().isoformat()

today_updates = client.property.get_properties(
    filter_query=f"ModificationTimestamp ge {today}T00:00:00Z"
)
```

### Date Functions

```python
# Extract year from date
newer_homes = client.property.get_properties(
    filter_query="year(OnMarketDate) eq 2024"
)

# Extract month
spring_listings = client.property.get_properties(
    filter_query="month(OnMarketDate) ge 3 and month(OnMarketDate) le 5"
)

# Day of week (1=Sunday, 7=Saturday)
weekend_listings = client.property.get_properties(
    filter_query="day(OnMarketDate) eq 1 or day(OnMarketDate) eq 7"
)
```

---

## 🔢 Numeric Operations

### Mathematical Operations

```python
# Price per square foot calculation
good_value = client.property.get_properties(
    filter_query="(ListPrice div SquareFeet) le 200",
    select=["ListingId", "ListPrice", "SquareFeet"]
)

# Addition and subtraction
price_range = client.property.get_properties(
    filter_query="(OriginalListPrice sub ListPrice) gt 50000"
)

# Multiplication
total_rooms = client.property.get_properties(
    filter_query="(BedroomsTotal add BathroomsTotalInteger) ge 6"
)

# Modulo operation
even_bedrooms = client.property.get_properties(
    filter_query="(BedroomsTotal mod 2) eq 0"
)
```

### Numeric Functions

```python
# Round function
rounded_prices = client.property.get_properties(
    filter_query="round(ListPrice div 1000) eq 500"  # Around $500k
)

# Floor and ceiling
price_floor = client.property.get_properties(
    filter_query="floor(ListPrice div 100000) eq 4"  # $400k-$499k range
)

# Absolute value
price_difference = client.property.get_properties(
    filter_query="abs(ListPrice sub OriginalListPrice) gt 25000"
)
```

---

## 📊 Advanced Query Patterns

### Complex Multi-Field Searches

```python
def advanced_property_search():
    """Demonstrate complex multi-field search patterns."""
    
    # Investment property criteria
    investment_properties = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "PropertyType eq 'Multi-Family' and "
            "ListPrice le 800000 and "
            "YearBuilt ge 1990 and "
            "contains(tolower(PublicRemarks), 'rental') and "
            "Latitude ne null and "
            "Longitude ne null"
        ),
        select=[
            "ListingId", "ListPrice", "Address", "City",
            "YearBuilt", "PropertyType", "BedroomsTotal",
            "PublicRemarks", "Latitude", "Longitude"
        ],
        orderby="ListPrice asc"
    )
    
    # Luxury family homes with specific features
    luxury_family = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "PropertyType eq 'Residential' and "
            "ListPrice ge 750000 and "
            "BedroomsTotal ge 4 and "
            "BathroomsTotalInteger ge 3 and "
            "SquareFeet ge 3000 and "
            "YearBuilt ge 2000 and "
            "(contains(tolower(PublicRemarks), 'granite') or "
            " contains(tolower(PublicRemarks), 'hardwood') or "
            " contains(tolower(PublicRemarks), 'stainless'))"
        ),
        orderby="SquareFeet desc"
    )
    
    # Fixer-upper opportunities
    fixer_uppers = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "ListPrice le 400000 and "
            "YearBuilt le 1980 and "
            "DaysOnMarket ge 30 and "
            "(contains(tolower(PublicRemarks), 'tlc') or "
            " contains(tolower(PublicRemarks), 'handyman') or "
            " contains(tolower(PublicRemarks), 'investor') or "
            " contains(tolower(PublicRemarks), 'as is'))"
        ),
        orderby="ListPrice asc"
    )
    
    return {
        'investment': investment_properties,
        'luxury_family': luxury_family,
        'fixer_uppers': fixer_uppers
    }

# Execute the search
results = advanced_property_search()
print(f"Found {len(results['investment'])} investment properties")
print(f"Found {len(results['luxury_family'])} luxury family homes")
print(f"Found {len(results['fixer_uppers'])} fixer-upper opportunities")
```

### Geographic Proximity Searches

```python
def geographic_searches():
    """Geographic and location-based query examples."""
    
    # Properties within coordinate bounds (rough bounding box)
    salt_lake_valley = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "Latitude ge 40.5 and Latitude le 40.9 and "
            "Longitude ge -112.2 and Longitude le -111.6"
        ),
        select=["ListingId", "Address", "City", "ListPrice", "Latitude", "Longitude"]
    )
    
    # Properties near specific coordinates (simplified distance)
    # Note: This is approximate - real distance calculation is more complex
    downtown_slc_lat, downtown_slc_lon = 40.7589, -111.8883
    tolerance = 0.05  # Roughly 3-4 miles
    
    near_downtown = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            f"abs(Latitude sub {downtown_slc_lat}) le {tolerance} and "
            f"abs(Longitude sub {downtown_slc_lon}) le {tolerance}"
        )
    )
    
    # Properties in specific ZIP codes
    target_zips = ['84101', '84102', '84103', '84104', '84105']
    zip_filter = " or ".join([f"PostalCode eq '{zip_code}'" for zip_code in target_zips])
    
    target_zip_properties = client.property.get_properties(
        filter_query=f"StandardStatus eq 'Active' and ({zip_filter})"
    )
    
    return {
        'valley_properties': salt_lake_valley,
        'near_downtown': near_downtown,
        'target_zips': target_zip_properties
    }
```

### Time-Based Analysis Queries

```python
def time_based_analysis():
    """Time-based query patterns for market analysis."""
    
    from datetime import datetime, timedelta
    
    now = datetime.now()
    
    # Market velocity - properties by days on market
    quick_sales = client.property.get_properties(
        filter_query="StandardStatus eq 'Active' and DaysOnMarket le 7",
        orderby="OnMarketDate desc"
    )
    
    stale_listings = client.property.get_properties(
        filter_query="StandardStatus eq 'Active' and DaysOnMarket ge 90",
        orderby="DaysOnMarket desc"
    )
    
    # Price reduction analysis
    seven_days_ago = (now - timedelta(days=7)).isoformat()
    
    recent_price_drops = client.property.get_properties(
        filter_query=(
            f"PriceChangeTimestamp ge {seven_days_ago} and "
            "ListPrice lt OriginalListPrice"
        ),
        select=[
            "ListingId", "ListPrice", "OriginalListPrice", 
            "PriceChangeTimestamp", "DaysOnMarket"
        ],
        orderby="PriceChangeTimestamp desc"
    )
    
    # Seasonal patterns (example: spring listings)
    spring_listings = client.property.get_properties(
        filter_query=(
            "month(OnMarketDate) ge 3 and month(OnMarketDate) le 5 and "
            "year(OnMarketDate) eq 2024"
        )
    )
    
    return {
        'quick_sales': quick_sales,
        'stale_listings': stale_listings,
        'price_drops': recent_price_drops,
        'spring_listings': spring_listings
    }
```

---

## 🛠️ Query Builder Helper

### Dynamic Query Construction

```python
class ODataQueryBuilder:
    """Helper class for building complex OData queries."""
    
    def __init__(self):
        self.filters = []
        self.select_fields = []
        self.order_fields = []
        self._top = None
        self._skip = None
        self._count = False
    
    def filter(self, condition: str):
        """Add a filter condition."""
        self.filters.append(condition)
        return self
    
    def filter_equals(self, field: str, value):
        """Add equality filter."""
        if isinstance(value, str):
            self.filters.append(f"{field} eq '{value}'")
        else:
            self.filters.append(f"{field} eq {value}")
        return self
    
    def filter_in(self, field: str, values: list):
        """Add 'in' filter (multiple OR conditions)."""
        if isinstance(values[0], str):
            conditions = [f"{field} eq '{value}'" for value in values]
        else:
            conditions = [f"{field} eq {value}" for value in values]
        
        self.filters.append(f"({' or '.join(conditions)})")
        return self
    
    def filter_range(self, field: str, min_val=None, max_val=None):
        """Add range filter."""
        if min_val is not None:
            self.filters.append(f"{field} ge {min_val}")
        if max_val is not None:
            self.filters.append(f"{field} le {max_val}")
        return self
    
    def filter_contains(self, field: str, substring: str, case_sensitive=True):
        """Add contains filter."""
        if case_sensitive:
            self.filters.append(f"contains({field}, '{substring}')")
        else:
            self.filters.append(f"contains(tolower({field}), '{substring.lower()}')")
        return self
    
    def filter_not_null(self, field: str):
        """Add not null filter."""
        self.filters.append(f"{field} ne null")
        return self
    
    def filter_date_range(self, field: str, start_date=None, end_date=None):
        """Add date range filter."""
        if start_date:
            if isinstance(start_date, datetime):
                start_date = start_date.isoformat()
            self.filters.append(f"{field} ge {start_date}")
        
        if end_date:
            if isinstance(end_date, datetime):
                end_date = end_date.isoformat()
            self.filters.append(f"{field} le {end_date}")
        return self
    
    def select(self, *fields):
        """Add fields to select."""
        self.select_fields.extend(fields)
        return self
    
    def order_by(self, field: str, direction: str = "asc"):
        """Add ordering."""
        self.order_fields.append(f"{field} {direction}")
        return self
    
    def top(self, count: int):
        """Set top limit."""
        self._top = count
        return self
    
    def skip(self, count: int):
        """Set skip count."""
        self._skip = count
        return self
    
    def count(self, include_count: bool = True):
        """Include count in response."""
        self._count = include_count
        return self
    
    def build(self) -> dict:
        """Build the query parameters."""
        params = {}
        
        if self.filters:
            params['filter_query'] = ' and '.join(self.filters)
        
        if self.select_fields:
            params['select'] = self.select_fields
        
        if self.order_fields:
            params['orderby'] = ', '.join(self.order_fields)
        
        if self._top is not None:
            params['top'] = self._top
        
        if self._skip is not None:
            params['skip'] = self._skip
        
        if self._count:
            params['count'] = True
        
        return params

# Usage examples
def query_builder_examples():
    """Examples using the query builder."""
    
    # Example 1: Luxury homes in specific cities
    luxury_query = (ODataQueryBuilder()
        .filter_equals("StandardStatus", "Active")
        .filter_in("City", ["Salt Lake City", "Park City", "Draper"])
        .filter_range("ListPrice", min_val=750000)
        .filter_range("BedroomsTotal", min_val=4)
        .filter_not_null("Latitude")
        .select("ListingId", "ListPrice", "Address", "City", "BedroomsTotal")
        .order_by("ListPrice", "desc")
        .top(50)
        .count()
        .build()
    )
    
    luxury_homes = client.property.get_properties(**luxury_query)
    
    # Example 2: Recent listings with price drops
    from datetime import datetime, timedelta
    
    week_ago = datetime.now() - timedelta(days=7)
    
    price_drop_query = (ODataQueryBuilder()
        .filter_equals("StandardStatus", "Active")
        .filter_date_range("PriceChangeTimestamp", start_date=week_ago)
        .filter("ListPrice lt OriginalListPrice")
        .select("ListingId", "ListPrice", "OriginalListPrice", "DaysOnMarket")
        .order_by("PriceChangeTimestamp", "desc")
        .top(25)
        .build()
    )
    
    price_drops = client.property.get_properties(**price_drop_query)
    
    # Example 3: Investment properties
    investment_query = (ODataQueryBuilder()
        .filter_equals("StandardStatus", "Active")
        .filter_in("PropertyType", ["Multi-Family", "Commercial"])
        .filter_range("ListPrice", max_val=1000000)
        .filter_contains("PublicRemarks", "rental", case_sensitive=False)
        .order_by("ListPrice", "asc")
        .build()
    )
    
    investment_props = client.property.get_properties(**investment_query)
    
    return {
        'luxury_homes': luxury_homes,
        'price_drops': price_drops,
        'investment_properties': investment_props
    }

# Execute examples
examples = query_builder_examples()
for category, properties in examples.items():
    print(f"{category}: {len(properties)} properties found")
```

---

## ⚡ Performance Optimization

### Efficient Query Patterns

```python
def optimized_queries():
    """Examples of performance-optimized queries."""
    
    # 1. Use specific field selection
    minimal_query = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice", "City"],  # Only needed fields
        top=100
    )
    
    # 2. Use indexed fields for filtering when possible
    # (ListingId, StandardStatus are typically indexed)
    indexed_filter = client.property.get_properties(
        filter_query="StandardStatus eq 'Active' and ListPrice ge 500000",
        top=50
    )
    
    # 3. Avoid expensive string operations in large datasets
    # Instead of this (slow):
    # contains(tolower(PublicRemarks), 'pool')
    
    # Use exact matches when possible (faster):
    exact_status = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'"
    )
    
    # 4. Use date ranges efficiently
    from datetime import datetime, timedelta
    
    # Good: Specific date range
    last_month = datetime.now() - timedelta(days=30)
    recent_specific = client.property.get_properties(
        filter_query=f"OnMarketDate ge {last_month.isoformat()}",
        select=["ListingId", "OnMarketDate", "ListPrice"]
    )
    
    # 5. Limit result sets appropriately
    paginated_query = client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice"],
        orderby="ListingId asc",  # Consistent ordering for pagination
        top=100,
        skip=0
    )
    
    return {
        'minimal': minimal_query,
        'indexed': indexed_filter,
        'exact_status': exact_status,
        'recent_specific': recent_specific,
        'paginated': paginated_query
    }
```

### Query Performance Tips

```python
def performance_comparison():
    """Compare different query approaches for performance."""
    
    import time
    
    # Measure query performance
    def time_query(description, query_func):
        start = time.time()
        result = query_func()
        elapsed = time.time() - start
        print(f"{description}: {len(result)} results in {elapsed:.2f}s")
        return result, elapsed
    
    # Test 1: Field selection impact
    print("=== Field Selection Performance ===")
    
    all_fields_query = lambda: client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        top=100
    )
    
    minimal_fields_query = lambda: client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice", "City"],
        top=100
    )
    
    time_query("All fields", all_fields_query)
    time_query("Minimal fields", minimal_fields_query)
    
    # Test 2: Filter complexity impact
    print("\n=== Filter Complexity Performance ===")
    
    simple_filter = lambda: client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice"],
        top=50
    )
    
    complex_filter = lambda: client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "ListPrice ge 300000 and ListPrice le 800000 and "
            "BedroomsTotal ge 3 and "
            "contains(City, 'Salt')"
        ),
        select=["ListingId", "ListPrice"],
        top=50
    )
    
    time_query("Simple filter", simple_filter)
    time_query("Complex filter", complex_filter)
    
    # Test 3: Ordering impact
    print("\n=== Ordering Performance ===")
    
    no_order = lambda: client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice"],
        top=100
    )
    
    with_order = lambda: client.property.get_properties(
        filter_query="StandardStatus eq 'Active'",
        select=["ListingId", "ListPrice"],
        orderby="ListPrice desc",
        top=100
    )
    
    time_query("No ordering", no_order)
    time_query("With ordering", with_order)

# Run performance comparison
performance_comparison()
```

---

## 🔍 Query Examples by Use Case

### Real Estate Agent Queries

```python
def agent_queries():
    """Common queries for real estate agents."""
    
    # My active listings
    agent_key = "AGT123456"  # Replace with actual agent key
    
    my_listings = client.property.get_properties(
        filter_query=f"ListAgentKey eq '{agent_key}' and StandardStatus eq 'Active'",
        select=[
            "ListingId", "Address", "ListPrice", "StandardStatus",
            "DaysOnMarket", "OnMarketDate"
        ],
        orderby="OnMarketDate desc"
    )
    
    # Recent price changes on my listings
    from datetime import datetime, timedelta
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    my_price_changes = client.property.get_properties(
        filter_query=(
            f"ListAgentKey eq '{agent_key}' and "
            f"PriceChangeTimestamp ge {week_ago}"
        ),
        select=[
            "ListingId", "Address", "ListPrice", "OriginalListPrice",
            "PriceChangeTimestamp"
        ]
    )
    
    # Comparable properties for pricing
    def find_comps(subject_property):
        """Find comparable properties for a subject property."""
        
        return client.property.get_properties(
            filter_query=(
                f"City eq '{subject_property['City']}' and "
                f"PropertyType eq '{subject_property['PropertyType']}' and "
                f"BedroomsTotal eq {subject_property['BedroomsTotal']} and "
                f"BathroomsTotalInteger eq {subject_property['BathroomsTotalInteger']} and "
                f"SquareFeet ge {subject_property['SquareFeet'] * 0.8} and "
                f"SquareFeet le {subject_property['SquareFeet'] * 1.2} and "
                "StandardStatus eq 'Sold' and "
                f"CloseDate ge {(datetime.now() - timedelta(days=180)).isoformat()}"
            ),
            select=[
                "ListingId", "Address", "ListPrice", "ClosePrice",
                "CloseDate", "SquareFeet", "DaysOnMarket"
            ],
            orderby="CloseDate desc"
        )
    
    return {
        'my_listings': my_listings,
        'my_price_changes': my_price_changes,
        'find_comps': find_comps
    }
```

### Investor Queries

```python
def investor_queries():
    """Queries tailored for real estate investors."""
    
    # Cash flow analysis properties
    cash_flow_candidates = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "PropertyType eq 'Multi-Family' and "
            "ListPrice le 500000 and "
            "YearBuilt ge 1980 and "
            "BedroomsTotal ge 4"
        ),
        select=[
            "ListingId", "Address", "ListPrice", "PropertyType",
            "BedroomsTotal", "BathroomsTotalInteger", "SquareFeet",
            "YearBuilt", "PublicRemarks"
        ],
        orderby="ListPrice asc"
    )
    
    # Distressed sale indicators
    distressed_properties = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "DaysOnMarket ge 60 and "
            "(contains(tolower(PublicRemarks), 'motivated') or "
            " contains(tolower(PublicRemarks), 'as is') or "
            " contains(tolower(PublicRemarks), 'cash only') or "
            " contains(tolower(PublicRemarks), 'investor'))"
        ),
        orderby="DaysOnMarket desc"
    )
    
    # Price reduction opportunities
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    
    price_reductions = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            f"PriceChangeTimestamp ge {thirty_days_ago} and "
            "ListPrice lt OriginalListPrice and "
            "(OriginalListPrice sub ListPrice) ge 25000"
        ),
        select=[
            "ListingId", "Address", "ListPrice", "OriginalListPrice",
            "PriceChangeTimestamp", "DaysOnMarket"
        ],
        orderby="PriceChangeTimestamp desc"
    )
    
    # Wholesale opportunities
    wholesale_candidates = client.property.get_properties(
        filter_query=(
            "StandardStatus eq 'Active' and "
            "ListPrice le 300000 and "
            "YearBuilt le 1990 and "
            "DaysOnMarket ge 30"
        ),
        orderby="ListPrice asc"
    )
    
    return {
        'cash_flow': cash_flow_candidates,
        'distressed': distressed_properties,
        'price_reductions': price_reductions,
        'wholesale': wholesale_candidates
    }
```

---

## 📚 Next Steps

### **Related Guides**
- **[Property Search Guide](property-search.md)** - Advanced property search patterns using OData
- **[Error Handling Guide](error-handling.md)** - Handling query validation errors
- **[Rate Limits Guide](rate-limits.md)** - Optimizing queries to reduce API usage

### **API Reference**
- **[Properties API](../api/properties.md)** - Complete property API documentation
- **[Field Reference](../reference/fields.md)** - All available fields for queries

### **Examples**
- **[Advanced Queries](../examples/advanced-queries.md)** - Real-world query examples
- **[Basic Usage](../examples/basic-usage.md)** - Simple query patterns

---

*Ready to build complex queries? Check out our [Property Search Guide](property-search.md) for advanced search patterns.* 