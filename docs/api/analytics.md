# Analytics API

The Analytics API provides access to market insights, statistical data, and analytical reports within the WFRMLS system. This includes market trends, pricing analysis, inventory statistics, and performance metrics.

## Overview

The `WFRMLSAnalytics` class handles all analytics-related operations, providing methods to retrieve market data, generate reports, and analyze real estate trends.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
market_stats = client.analytics.get_market_statistics()
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_market_statistics()` | Get overall market statistics | `Dict[str, Any]` |
| `get_price_trends()` | Get pricing trend data | `List[Dict[str, Any]]` |
| `get_inventory_analysis()` | Get inventory level analysis | `Dict[str, Any]` |
| `get_days_on_market()` | Get days on market statistics | `Dict[str, Any]` |
| `get_sales_volume()` | Get sales volume data | `List[Dict[str, Any]]` |
| `get_area_statistics()` | Get statistics for specific areas | `Dict[str, Any]` |

## Methods

### get_market_statistics()

Retrieve overall market statistics and key performance indicators.

```python
def get_market_statistics(
    self,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    property_type: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | `datetime` | No | Start date for analysis |
| `date_to` | `datetime` | No | End date for analysis |
| `property_type` | `str` | No | Filter by property type |

#### Example

```python
from datetime import datetime, timedelta

# Get current market statistics
market_stats = client.analytics.get_market_statistics()

print(f"Active Listings: {market_stats['active_listings']}")
print(f"Average Price: ${market_stats['average_price']:,}")
print(f"Median Price: ${market_stats['median_price']:,}")
print(f"Days on Market: {market_stats['average_dom']}")

# Get statistics for specific period
last_month = datetime.now() - timedelta(days=30)
monthly_stats = client.analytics.get_market_statistics(
    date_from=last_month,
    property_type="RES"
)
```

### get_price_trends()

Retrieve pricing trend data over time periods.

```python
def get_price_trends(
    self,
    period: str = "monthly",
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    property_type: Optional[str] = None,
    area: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | `str` | No | Aggregation period (daily, weekly, monthly, yearly) |
| `date_from` | `datetime` | No | Start date for trends |
| `date_to` | `datetime` | No | End date for trends |
| `property_type` | `str` | No | Filter by property type |
| `area` | `str` | No | Filter by geographic area |

#### Example

```python
# Get monthly price trends for the last year
last_year = datetime.now() - timedelta(days=365)
price_trends = client.analytics.get_price_trends(
    period="monthly",
    date_from=last_year,
    property_type="RES"
)

for trend in price_trends:
    print(f"{trend['period']}: ${trend['average_price']:,} (±{trend['price_change_percent']:.1f}%)")
```

### get_inventory_analysis()

Retrieve inventory level analysis and absorption rates.

```python
def get_inventory_analysis(
    self,
    property_type: Optional[str] = None,
    price_range: Optional[Dict[str, int]] = None,
    area: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `property_type` | `str` | No | Filter by property type |
| `price_range` | `Dict[str, int]` | No | Price range filter (min, max) |
| `area` | `str` | No | Geographic area filter |

#### Example

```python
# Get overall inventory analysis
inventory = client.analytics.get_inventory_analysis()

print(f"Total Active Listings: {inventory['total_active']}")
print(f"New Listings (30 days): {inventory['new_listings_30d']}")
print(f"Months of Supply: {inventory['months_of_supply']:.1f}")
print(f"Absorption Rate: {inventory['absorption_rate']:.1f}%")

# Get inventory for specific price range
luxury_inventory = client.analytics.get_inventory_analysis(
    property_type="RES",
    price_range={"min": 1000000, "max": 5000000}
)
```

### get_days_on_market()

Retrieve days on market statistics and distribution.

```python
def get_days_on_market(
    self,
    property_type: Optional[str] = None,
    status: Optional[str] = None,
    area: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `property_type` | `str` | No | Filter by property type |
| `status` | `str` | No | Filter by property status |
| `area` | `str` | No | Geographic area filter |

#### Example

```python
# Get days on market analysis
dom_stats = client.analytics.get_days_on_market(
    property_type="RES",
    status="Sold"
)

print(f"Average DOM: {dom_stats['average_dom']}")
print(f"Median DOM: {dom_stats['median_dom']}")
print(f"DOM Distribution:")
for range_key, count in dom_stats['dom_distribution'].items():
    print(f"  {range_key}: {count} properties")
```

### get_sales_volume()

Retrieve sales volume data and trends.

```python
def get_sales_volume(
    self,
    period: str = "monthly",
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    property_type: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | `str` | No | Aggregation period |
| `date_from` | `datetime` | No | Start date |
| `date_to` | `datetime` | No | End date |
| `property_type` | `str` | No | Property type filter |

#### Example

```python
# Get monthly sales volume for the last year
sales_volume = client.analytics.get_sales_volume(
    period="monthly",
    date_from=datetime.now() - timedelta(days=365)
)

for month in sales_volume:
    print(f"{month['period']}: {month['units_sold']} units, ${month['total_volume']:,}")
```

### get_area_statistics()

Retrieve statistics for specific geographic areas.

```python
def get_area_statistics(
    self,
    area_type: str,
    area_value: str,
    property_type: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `area_type` | `str` | Yes | Type of area (city, county, zip, subdivision) |
| `area_value` | `str` | Yes | Area identifier |
| `property_type` | `str` | No | Property type filter |

#### Example

```python
# Get statistics for Salt Lake City
slc_stats = client.analytics.get_area_statistics(
    area_type="city",
    area_value="Salt Lake City",
    property_type="RES"
)

print(f"Salt Lake City Market:")
print(f"  Active Listings: {slc_stats['active_listings']}")
print(f"  Average Price: ${slc_stats['average_price']:,}")
print(f"  Price per Sq Ft: ${slc_stats['price_per_sqft']:.2f}")

# Get statistics by ZIP code
zip_stats = client.analytics.get_area_statistics(
    area_type="zip",
    area_value="84102"
)
```

## Common Use Cases

### Market Dashboard

```python
# Create a comprehensive market dashboard
def create_market_dashboard():
    # Get overall statistics
    market_stats = client.analytics.get_market_statistics()
    
    # Get price trends
    price_trends = client.analytics.get_price_trends(
        period="monthly",
        date_from=datetime.now() - timedelta(days=365)
    )
    
    # Get inventory analysis
    inventory = client.analytics.get_inventory_analysis()
    
    # Get DOM statistics
    dom_stats = client.analytics.get_days_on_market()
    
    dashboard = {
        "market_overview": market_stats,
        "price_trends": price_trends,
        "inventory_analysis": inventory,
        "days_on_market": dom_stats,
        "generated_at": datetime.now().isoformat()
    }
    
    return dashboard

dashboard_data = create_market_dashboard()
```

### Comparative Market Analysis

```python
# Compare multiple areas
def compare_market_areas(areas):
    comparison = {}
    
    for area_type, area_value in areas:
        stats = client.analytics.get_area_statistics(
            area_type=area_type,
            area_value=area_value,
            property_type="RES"
        )
        
        comparison[area_value] = {
            "active_listings": stats.get("active_listings", 0),
            "average_price": stats.get("average_price", 0),
            "median_price": stats.get("median_price", 0),
            "price_per_sqft": stats.get("price_per_sqft", 0),
            "average_dom": stats.get("average_dom", 0)
        }
    
    return comparison

# Compare different cities
areas_to_compare = [
    ("city", "Salt Lake City"),
    ("city", "Provo"),
    ("city", "Park City"),
    ("city", "Ogden")
]

market_comparison = compare_market_areas(areas_to_compare)

print("Market Comparison:")
for area, stats in market_comparison.items():
    print(f"\n{area}:")
    print(f"  Active Listings: {stats['active_listings']}")
    print(f"  Average Price: ${stats['average_price']:,}")
    print(f"  Price/Sq Ft: ${stats['price_per_sqft']:.2f}")
```

### Price Trend Analysis

```python
# Analyze price trends and calculate growth rates
def analyze_price_trends(months_back=12):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months_back * 30)
    
    trends = client.analytics.get_price_trends(
        period="monthly",
        date_from=start_date,
        date_to=end_date,
        property_type="RES"
    )
    
    if len(trends) < 2:
        return None
    
    # Calculate year-over-year growth
    latest = trends[-1]
    year_ago = trends[0] if len(trends) >= 12 else trends[0]
    
    price_growth = ((latest['average_price'] - year_ago['average_price']) / 
                   year_ago['average_price'] * 100)
    
    # Calculate monthly volatility
    monthly_changes = []
    for i in range(1, len(trends)):
        change = ((trends[i]['average_price'] - trends[i-1]['average_price']) / 
                 trends[i-1]['average_price'] * 100)
        monthly_changes.append(change)
    
    volatility = sum(abs(change) for change in monthly_changes) / len(monthly_changes)
    
    analysis = {
        "current_average_price": latest['average_price'],
        "year_over_year_growth": round(price_growth, 2),
        "monthly_volatility": round(volatility, 2),
        "trend_direction": "up" if price_growth > 0 else "down",
        "data_points": len(trends)
    }
    
    return analysis

trend_analysis = analyze_price_trends()
if trend_analysis:
    print(f"Price Trend Analysis:")
    print(f"  Current Average: ${trend_analysis['current_average_price']:,}")
    print(f"  YoY Growth: {trend_analysis['year_over_year_growth']}%")
    print(f"  Volatility: {trend_analysis['monthly_volatility']}%")
```

## Advanced Analytics

### Market Segmentation

```python
# Analyze market by price segments
def analyze_market_segments():
    segments = [
        {"name": "Entry Level", "min": 0, "max": 300000},
        {"name": "Mid-Range", "min": 300000, "max": 600000},
        {"name": "Upper Mid", "min": 600000, "max": 1000000},
        {"name": "Luxury", "min": 1000000, "max": None}
    ]
    
    segment_analysis = {}
    
    for segment in segments:
        price_range = {"min": segment["min"]}
        if segment["max"]:
            price_range["max"] = segment["max"]
        
        inventory = client.analytics.get_inventory_analysis(
            property_type="RES",
            price_range=price_range
        )
        
        segment_analysis[segment["name"]] = {
            "active_listings": inventory.get("total_active", 0),
            "months_of_supply": inventory.get("months_of_supply", 0),
            "absorption_rate": inventory.get("absorption_rate", 0),
            "price_range": f"${segment['min']:,}" + (f" - ${segment['max']:,}" if segment['max'] else "+")
        }
    
    return segment_analysis

segments = analyze_market_segments()
for segment_name, data in segments.items():
    print(f"\n{segment_name} ({data['price_range']}):")
    print(f"  Active Listings: {data['active_listings']}")
    print(f"  Months of Supply: {data['months_of_supply']:.1f}")
    print(f"  Absorption Rate: {data['absorption_rate']:.1f}%")
```

### Seasonal Analysis

```python
# Analyze seasonal patterns
def analyze_seasonal_patterns():
    # Get 2+ years of data for seasonal analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 years
    
    monthly_data = client.analytics.get_sales_volume(
        period="monthly",
        date_from=start_date,
        date_to=end_date
    )
    
    # Group by month
    seasonal_patterns = {}
    for data in monthly_data:
        month = datetime.fromisoformat(data['period']).month
        month_name = datetime.fromisoformat(data['period']).strftime('%B')
        
        if month_name not in seasonal_patterns:
            seasonal_patterns[month_name] = []
        
        seasonal_patterns[month_name].append(data['units_sold'])
    
    # Calculate averages
    seasonal_averages = {}
    for month, sales_list in seasonal_patterns.items():
        seasonal_averages[month] = sum(sales_list) / len(sales_list)
    
    # Find peak and low seasons
    peak_month = max(seasonal_averages, key=seasonal_averages.get)
    low_month = min(seasonal_averages, key=seasonal_averages.get)
    
    return {
        "monthly_averages": seasonal_averages,
        "peak_month": peak_month,
        "low_month": low_month,
        "seasonal_variation": (seasonal_averages[peak_month] - seasonal_averages[low_month]) / seasonal_averages[low_month] * 100
    }

seasonal_analysis = analyze_seasonal_patterns()
print(f"Seasonal Analysis:")
print(f"  Peak Month: {seasonal_analysis['peak_month']}")
print(f"  Low Month: {seasonal_analysis['low_month']}")
print(f"  Seasonal Variation: {seasonal_analysis['seasonal_variation']:.1f}%")
```

## Data Export and Reporting

### CSV Export

```python
import csv
from io import StringIO

def export_market_data_to_csv():
    # Get market statistics
    market_stats = client.analytics.get_market_statistics()
    
    # Get price trends
    price_trends = client.analytics.get_price_trends(
        period="monthly",
        date_from=datetime.now() - timedelta(days=365)
    )
    
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    
    # Write market statistics
    writer.writerow(["Market Statistics"])
    writer.writerow(["Metric", "Value"])
    for key, value in market_stats.items():
        writer.writerow([key, value])
    
    writer.writerow([])  # Empty row
    
    # Write price trends
    writer.writerow(["Price Trends"])
    writer.writerow(["Period", "Average Price", "Median Price", "Units Sold"])
    for trend in price_trends:
        writer.writerow([
            trend['period'],
            trend['average_price'],
            trend['median_price'],
            trend.get('units_sold', '')
        ])
    
    return output.getvalue()

csv_data = export_market_data_to_csv()
```

### JSON Report Generation

```python
import json

def generate_comprehensive_report():
    report = {
        "report_date": datetime.now().isoformat(),
        "market_overview": client.analytics.get_market_statistics(),
        "inventory_analysis": client.analytics.get_inventory_analysis(),
        "days_on_market": client.analytics.get_days_on_market(),
        "price_trends": client.analytics.get_price_trends(
            period="monthly",
            date_from=datetime.now() - timedelta(days=365)
        ),
        "area_comparisons": {}
    }
    
    # Add area comparisons
    major_cities = ["Salt Lake City", "Provo", "Park City", "Ogden"]
    for city in major_cities:
        try:
            city_stats = client.analytics.get_area_statistics(
                area_type="city",
                area_value=city
            )
            report["area_comparisons"][city] = city_stats
        except Exception as e:
            print(f"Could not get stats for {city}: {e}")
    
    return report

comprehensive_report = generate_comprehensive_report()

# Save to file
with open("market_report.json", "w") as f:
    json.dump(comprehensive_report, f, indent=2, default=str)
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    stats = client.analytics.get_area_statistics(
        area_type="city",
        area_value="NonexistentCity"
    )
except NotFoundError:
    print("Area not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Cache analytics data** as it's computationally expensive
2. **Use appropriate date ranges** to balance detail and performance
3. **Batch multiple analytics calls** when possible
4. **Consider data freshness** requirements

### Data Interpretation

1. **Understand seasonal patterns** in real estate markets
2. **Consider external factors** affecting market conditions
3. **Use multiple metrics** for comprehensive analysis
4. **Validate data quality** before making decisions

### Reporting

1. **Include data sources and timestamps** in reports
2. **Provide context** for statistical measures
3. **Use visualizations** for trend data
4. **Update reports regularly** for accuracy

## Related Resources

- [Properties API](properties.md) - For underlying property data
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management