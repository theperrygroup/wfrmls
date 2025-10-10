# Analytics API Reference

The Analytics module provides access to market data insights and statistical information in the WFRMLS system. This includes market trends, pricing analytics, inventory statistics, and performance metrics.

---

## Overview

The `AnalyticsService` class handles all analytics-related operations through the WFRMLS API. Analytics provide aggregated data and insights for market analysis, reporting, and business intelligence.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
analytics_service = client.analytics
```

---

## Methods

### get_analytics()

Retrieve analytics data with optional filtering, sorting, and pagination.

```python
analytics = client.analytics.get_analytics(
    top=50,
    filter_query="AnalyticsDate ge 2024-01-01T00:00:00Z",
    orderby="AnalyticsDate desc"
)
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `select` | `Optional[List[str]]` | No | `None` | Specific fields to return. If not provided, returns all available fields. |
| `filter_query` | `Optional[str]` | No | `None` | OData filter expression to limit results. |
| `orderby` | `Optional[str]` | No | `None` | OData orderby expression for sorting results. |
| `top` | `Optional[int]` | No | `None` | Maximum number of records to return. |
| `skip` | `Optional[int]` | No | `None` | Number of records to skip for pagination. |
| `count` | `Optional[bool]` | No | `False` | Include total count of matching records in response. |

#### Returns

`List[Dict[str, Any]]`: List of analytics records matching the query criteria.

#### Example

```python
# Get recent market analytics
recent_analytics = client.analytics.get_analytics(
    filter_query="AnalyticsDate ge 2024-01-01T00:00:00Z",
    select=["AnalyticsKey", "AnalyticsDate", "MarketArea", "MedianPrice", "InventoryCount"],
    orderby="AnalyticsDate desc",
    top=100
)

# Get analytics for specific market area
area_analytics = client.analytics.get_analytics(
    filter_query="MarketArea eq 'Salt Lake County'",
    orderby="AnalyticsDate desc"
)

# Get price trend data
price_trends = client.analytics.get_analytics(
    filter_query="AnalyticsType eq 'PriceTrend'",
    select=["AnalyticsDate", "MarketArea", "MedianPrice", "AveragePrice"]
)
```

---

### get_analytic()

Retrieve a specific analytics record by its unique identifier.

```python
analytic = client.analytics.get_analytic("ANALYTICS123")
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analytics_key` | `str` | Yes | - | The unique identifier for the analytics record. |
| `select` | `Optional[List[str]]` | No | `None` | Specific fields to return. If not provided, returns all available fields. |

#### Returns

`Dict[str, Any]`: Complete analytics record for the specified key.

#### Raises

- `NotFoundError`: If the analytics record with the specified key is not found.
- `WFRMLSError`: For other API-related errors.

#### Example

```python
# Get complete analytics record
analytic = client.analytics.get_analytic("ANALYTICS123")

# Get specific fields only
price_data = client.analytics.get_analytic(
    "ANALYTICS123",
    select=["AnalyticsDate", "MarketArea", "MedianPrice", "AveragePrice", "InventoryCount"]
)
```

---

## Common Use Cases

### Market Trend Analysis

```python
from datetime import datetime, timedelta

# Get 12 months of market data for trend analysis
start_date = datetime.now() - timedelta(days=365)
market_trends = client.analytics.get_analytics(
    filter_query=f"AnalyticsDate ge {start_date.isoformat()}Z and AnalyticsType eq 'MarketSummary'",
    select=[
        "AnalyticsDate", "MarketArea", "MedianPrice", "AveragePrice",
        "InventoryCount", "DaysOnMarket", "SalesVolume"
    ],
    orderby="AnalyticsDate asc"
)

# Calculate price appreciation
price_data = {}
for record in market_trends:
    area = record['MarketArea']
    if area not in price_data:
        price_data[area] = []
    price_data[area].append({
        'date': record['AnalyticsDate'],
        'median_price': record['MedianPrice']
    })

for area, data in price_data.items():
    if len(data) >= 2:
        latest = data[-1]['median_price']
        earliest = data[0]['median_price']
        appreciation = ((latest - earliest) / earliest) * 100
        print(f"{area}: {appreciation:.2f}% price appreciation")
```

### Inventory Analysis

```python
# Analyze current inventory levels by market area
current_inventory = client.analytics.get_analytics(
    filter_query="AnalyticsType eq 'Inventory' and AnalyticsDate ge 2024-01-01T00:00:00Z",
    select=[
        "MarketArea", "InventoryCount", "MonthsOfSupply", 
        "NewListings", "PendingSales", "ClosedSales"
    ],
    orderby="MarketArea asc"
)

print("Current Market Inventory:")
for record in current_inventory:
    print(f"{record['MarketArea']}:")
    print(f"  Active Listings: {record['InventoryCount']}")
    print(f"  Months of Supply: {record['MonthsOfSupply']}")
    print(f"  New Listings: {record['NewListings']}")
    print(f"  Pending Sales: {record['PendingSales']}")
```

### Price Point Analysis

```python
# Analyze sales by price range
price_analytics = client.analytics.get_analytics(
    filter_query="AnalyticsType eq 'PriceRange'",
    select=[
        "PriceRangeLow", "PriceRangeHigh", "SalesCount", 
        "MarketShare", "AverageDaysOnMarket"
    ],
    orderby="PriceRangeLow asc"
)

print("Sales by Price Range:")
for record in price_analytics:
    price_range = f"${record['PriceRangeLow']:,} - ${record['PriceRangeHigh']:,}"
    print(f"{price_range}: {record['SalesCount']} sales ({record['MarketShare']:.1f}% market share)")
```

---

## Key Fields

### Identification Fields

| Field | Type | Description |
|-------|------|-------------|
| `AnalyticsKey` | `str` | Unique identifier for the analytics record |
| `AnalyticsId` | `str` | Analytics record ID |
| `AnalyticsType` | `str` | Type of analytics (MarketSummary, Inventory, PriceTrend, etc.) |

### Date and Geography

| Field | Type | Description |
|-------|------|-------------|
| `AnalyticsDate` | `datetime` | Date of the analytics data |
| `AnalyticsPeriod` | `str` | Time period (Monthly, Quarterly, Annual) |
| `MarketArea` | `str` | Geographic market area |
| `MarketAreaCode` | `str` | Market area code identifier |
| `County` | `str` | County name |
| `City` | `str` | City name |

### Price Metrics

| Field | Type | Description |
|-------|------|-------------|
| `MedianPrice` | `decimal` | Median sale price |
| `AveragePrice` | `decimal` | Average sale price |
| `PricePerSquareFoot` | `decimal` | Average price per square foot |
| `PriceAppreciation` | `decimal` | Price appreciation percentage |
| `PriceRangeLow` | `decimal` | Lower bound of price range |
| `PriceRangeHigh` | `decimal` | Upper bound of price range |

### Inventory Metrics

| Field | Type | Description |
|-------|------|-------------|
| `InventoryCount` | `int` | Number of active listings |
| `MonthsOfSupply` | `decimal` | Months of inventory supply |
| `NewListings` | `int` | New listings added |
| `ExpiredListings` | `int` | Listings that expired |
| `WithdrawnListings` | `int` | Listings withdrawn from market |

### Sales Metrics

| Field | Type | Description |
|-------|------|-------------|
| `SalesCount` | `int` | Number of closed sales |
| `SalesVolume` | `decimal` | Total dollar volume of sales |
| `PendingSales` | `int` | Number of pending sales |
| `DaysOnMarket` | `decimal` | Average days on market |
| `MarketShare` | `decimal` | Market share percentage |

### Performance Metrics

| Field | Type | Description |
|-------|------|-------------|
| `AbsorptionRate` | `decimal` | Rate of inventory absorption |
| `ListToSaleRatio` | `decimal` | Ratio of list price to sale price |
| `PriceReductions` | `int` | Number of price reductions |
| `CancellationRate` | `decimal` | Listing cancellation rate |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `ModificationTimestamp` | `datetime` | Last modification date/time |
| `OriginalEntryTimestamp` | `datetime` | Original creation date/time |

---

## Advanced Analytics Queries

### Time Series Analysis

```python
def get_market_time_series(market_area, start_date, end_date):
    """Get time series data for market analysis."""
    time_series = client.analytics.get_analytics(
        filter_query=f"MarketArea eq '{market_area}' and AnalyticsDate ge {start_date.isoformat()}Z and AnalyticsDate le {end_date.isoformat()}Z",
        select=[
            "AnalyticsDate", "MedianPrice", "AveragePrice", "InventoryCount",
            "SalesCount", "DaysOnMarket", "MonthsOfSupply"
        ],
        orderby="AnalyticsDate asc"
    )
    
    return time_series

# Usage
from datetime import datetime, timedelta

start = datetime.now() - timedelta(days=365)
end = datetime.now()
slc_data = get_market_time_series("Salt Lake County", start, end)

# Calculate moving averages
def calculate_moving_average(data, field, window=3):
    """Calculate moving average for a field."""
    result = []
    for i in range(len(data)):
        if i >= window - 1:
            values = [data[j][field] for j in range(i - window + 1, i + 1)]
            avg = sum(values) / len(values)
            result.append(avg)
        else:
            result.append(None)
    return result

price_ma = calculate_moving_average(slc_data, 'MedianPrice', 3)
```

### Comparative Market Analysis

```python
def compare_markets(market_areas, metric='MedianPrice'):
    """Compare multiple market areas on a specific metric."""
    comparison_data = {}
    
    for area in market_areas:
        area_data = client.analytics.get_analytics(
            filter_query=f"MarketArea eq '{area}' and AnalyticsDate ge 2024-01-01T00:00:00Z",
            select=["AnalyticsDate", metric],
            orderby="AnalyticsDate desc",
            top=12  # Last 12 months
        )
        comparison_data[area] = area_data
    
    return comparison_data

# Usage
markets = ["Salt Lake County", "Utah County", "Davis County"]
price_comparison = compare_markets(markets, 'MedianPrice')

for market, data in price_comparison.items():
    if data:
        latest_price = data[0]['MedianPrice']
        print(f"{market}: ${latest_price:,}")
```

### Market Health Indicators

```python
def calculate_market_health(market_area):
    """Calculate market health indicators."""
    latest_data = client.analytics.get_analytics(
        filter_query=f"MarketArea eq '{market_area}'",
        orderby="AnalyticsDate desc",
        top=1
    )
    
    if not latest_data:
        return None
    
    data = latest_data[0]
    
    # Calculate health score based on multiple factors
    health_score = 0
    factors = []
    
    # Inventory levels (healthy: 4-6 months)
    months_supply = data.get('MonthsOfSupply', 0)
    if 4 <= months_supply <= 6:
        inventory_score = 100
    elif months_supply < 4:
        inventory_score = max(0, 100 - (4 - months_supply) * 20)
    else:
        inventory_score = max(0, 100 - (months_supply - 6) * 15)
    
    factors.append(('Inventory Balance', inventory_score))
    
    # Days on market (healthy: < 60 days)
    dom = data.get('DaysOnMarket', 0)
    dom_score = max(0, 100 - max(0, dom - 60) * 2)
    factors.append(('Days on Market', dom_score))
    
    # Price appreciation (healthy: 3-7% annually)
    appreciation = data.get('PriceAppreciation', 0)
    if 3 <= appreciation <= 7:
        price_score = 100
    else:
        price_score = max(0, 100 - abs(appreciation - 5) * 10)
    
    factors.append(('Price Appreciation', price_score))
    
    # Calculate overall score
    health_score = sum(score for _, score in factors) / len(factors)
    
    return {
        'market_area': market_area,
        'health_score': health_score,
        'factors': factors,
        'data': data
    }

# Usage
health = calculate_market_health("Salt Lake County")
if health:
    print(f"Market Health Score: {health['health_score']:.1f}/100")
    for factor, score in health['factors']:
        print(f"  {factor}: {score:.1f}")
```

---

## Reporting and Visualization

### Market Report Generation

```python
def generate_market_report(market_area, months=12):
    """Generate comprehensive market report."""
    from datetime import datetime, timedelta
    
    start_date = datetime.now() - timedelta(days=months * 30)
    
    # Get historical data
    historical_data = client.analytics.get_analytics(
        filter_query=f"MarketArea eq '{market_area}' and AnalyticsDate ge {start_date.isoformat()}Z",
        orderby="AnalyticsDate desc"
    )
    
    if not historical_data:
        return None
    
    latest = historical_data[0]
    oldest = historical_data[-1] if len(historical_data) > 1 else latest
    
    # Calculate changes
    price_change = ((latest['MedianPrice'] - oldest['MedianPrice']) / oldest['MedianPrice']) * 100
    inventory_change = latest['InventoryCount'] - oldest['InventoryCount']
    
    report = {
        'market_area': market_area,
        'report_date': datetime.now().isoformat(),
        'period_months': months,
        'current_metrics': {
            'median_price': latest['MedianPrice'],
            'inventory_count': latest['InventoryCount'],
            'months_of_supply': latest.get('MonthsOfSupply'),
            'days_on_market': latest.get('DaysOnMarket'),
            'sales_count': latest.get('SalesCount')
        },
        'changes': {
            'price_change_percent': price_change,
            'inventory_change': inventory_change
        },
        'historical_data': historical_data
    }
    
    return report

# Usage
report = generate_market_report("Salt Lake County", 12)
if report:
    print(f"Market Report: {report['market_area']}")
    print(f"Median Price: ${report['current_metrics']['median_price']:,}")
    print(f"Price Change: {report['changes']['price_change_percent']:.2f}%")
    print(f"Active Inventory: {report['current_metrics']['inventory_count']}")
```

### Export Analytics Data

```python
def export_analytics_to_csv(market_areas, start_date, end_date, filename):
    """Export analytics data to CSV file."""
    import csv
    from datetime import datetime
    
    all_data = []
    
    for area in market_areas:
        area_data = client.analytics.get_analytics(
            filter_query=f"MarketArea eq '{area}' and AnalyticsDate ge {start_date.isoformat()}Z and AnalyticsDate le {end_date.isoformat()}Z",
            orderby="AnalyticsDate asc"
        )
        all_data.extend(area_data)
    
    if not all_data:
        print("No data found for export")
        return
    
    # Get all unique field names
    fieldnames = set()
    for record in all_data:
        fieldnames.update(record.keys())
    
    fieldnames = sorted(list(fieldnames))
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Exported {len(all_data)} records to {filename}")

# Usage
from datetime import datetime, timedelta

start = datetime.now() - timedelta(days=90)
end = datetime.now()
markets = ["Salt Lake County", "Utah County"]

export_analytics_to_csv(markets, start, end, "market_analytics.csv")
```

---

## Error Handling

```python
from wfrmls.exceptions import WFRMLSError, NotFoundError, ValidationError

try:
    # Attempt to get analytics
    analytics = client.analytics.get_analytic("INVALID_KEY")
    
except NotFoundError:
    print("Analytics record not found")
    
except ValidationError as e:
    print(f"Invalid request: {e}")
    
except WFRMLSError as e:
    print(f"API error: {e}")
```

---

## Best Practices

### Efficient Data Retrieval

```python
# Use specific date ranges and select fields for better performance
analytics = client.analytics.get_analytics(
    filter_query="AnalyticsDate ge 2024-01-01T00:00:00Z and MarketArea eq 'Salt Lake County'",
    select=["AnalyticsDate", "MedianPrice", "InventoryCount", "SalesCount"],
    orderby="AnalyticsDate desc",
    top=50
)

# Cache frequently accessed data
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_cached_market_data(market_area, days_back=30):
    """Get market data with caching."""
    start_date = datetime.now() - timedelta(days=days_back)
    
    return client.analytics.get_analytics(
        filter_query=f"MarketArea eq '{market_area}' and AnalyticsDate ge {start_date.isoformat()}Z",
        orderby="AnalyticsDate desc"
    )
```

### Data Validation

```python
def validate_analytics_data(data):
    """Validate analytics data for completeness and accuracy."""
    issues = []
    
    for record in data:
        # Check for required fields
        required_fields = ['AnalyticsDate', 'MarketArea', 'MedianPrice']
        for field in required_fields:
            if field not in record or record[field] is None:
                issues.append(f"Missing {field} in record {record.get('AnalyticsKey', 'unknown')}")
        
        # Check for reasonable values
        if 'MedianPrice' in record and record['MedianPrice'] < 0:
            issues.append(f"Negative median price in record {record.get('AnalyticsKey')}")
        
        if 'InventoryCount' in record and record['InventoryCount'] < 0:
            issues.append(f"Negative inventory count in record {record.get('AnalyticsKey')}")
    
    return issues

# Usage
data = client.analytics.get_analytics(top=100)
validation_issues = validate_analytics_data(data)

if validation_issues:
    print("Data validation issues found:")
    for issue in validation_issues:
        print(f"  - {issue}")
```

---

## Related Resources

- **[Property API](properties.md)** - For detailed property data that feeds analytics
- **[OData Queries Guide](../guides/odata-queries.md)** - Advanced filtering and querying
- **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling strategies