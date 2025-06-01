# Code Examples

Real-world usage examples for common real estate applications using the WFRMLS Python client.

---

## 📂 Example Categories

<div class="grid cards" markdown>

-   :material-play-circle:{ .lg .middle } **Basic Usage**

    ---

    Simple examples to get you started with common operations

    [:octicons-arrow-right-24: View Basic Examples](basic-usage.md)

-   :material-database:{ .lg .middle } **Advanced Queries**

    ---

    Complex filtering, sorting, and data manipulation examples

    [:octicons-arrow-right-24: Advanced Examples](advanced-queries.md)

-   :material-home-city:{ .lg .middle } **Real Estate Apps**

    ---

    Complete application examples for property search and management

    [:octicons-arrow-right-24: App Examples](real-estate-apps.md)

-   :material-sync:{ .lg .middle } **Data Integration**

    ---

    Patterns for integrating WFRMLS data with other systems

    [:octicons-arrow-right-24: Integration Examples](data-integration.md)

-   :material-chart-line:{ .lg .middle } **Monitoring & Analytics**

    ---

    Examples for tracking performance and analyzing market data

    [:octicons-arrow-right-24: Analytics Examples](monitoring.md)

</div>

---

## 🚀 Quick Start Examples

### Property Search

```python
from wfrmls import WFRMLSClient

# Initialize client
client = WFRMLSClient()

# Get active properties under $500K
affordable_homes = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and ListPrice le 500000",
    select=["ListingId", "ListPrice", "City", "BedroomsTotal"],
    orderby="ListPrice asc",
    top=20
)

print(f"Found {len(affordable_homes)} affordable homes:")
for home in affordable_homes:
    print(f"  {home['ListingId']}: ${home['ListPrice']:,} in {home['City']}")
```

### Agent Lookup

```python
# Find agents in specific city
salt_lake_agents = client.member.get_members(
    filter_query="contains(MemberCity, 'Salt Lake') and MemberStatus eq 'Active'",
    select=["MemberKey", "MemberFullName", "MemberEmail", "MemberPhone"]
)

print(f"Found {len(salt_lake_agents)} agents in Salt Lake:")
for agent in salt_lake_agents:
    print(f"  {agent['MemberFullName']}: {agent.get('MemberEmail', 'No email')}")
```

### Office Information

```python
# Get office details
offices = client.office.get_offices(
    select=["OfficeKey", "OfficeName", "OfficeCity", "OfficePhone"],
    top=10
)

for office in offices:
    print(f"{office['OfficeName']} in {office.get('OfficeCity', 'Unknown')}")
```

---

## 📊 Use Case Examples

### **Property Portal Development**

??? example "Property Search Interface"
    ```python
    def search_properties(min_price=None, max_price=None, city=None, 
                         bedrooms=None, property_type=None):
        """Search properties with multiple filters."""
        
        filters = ["StandardStatus eq 'Active'"]
        
        if min_price:
            filters.append(f"ListPrice ge {min_price}")
        if max_price:
            filters.append(f"ListPrice le {max_price}")
        if city:
            filters.append(f"City eq '{city}'")
        if bedrooms:
            filters.append(f"BedroomsTotal ge {bedrooms}")
        if property_type:
            filters.append(f"PropertyType eq '{property_type}'")
        
        filter_query = " and ".join(filters)
        
        return client.property.get_properties(
            filter_query=filter_query,
            select=[
                "ListingId", "ListPrice", "City", "Address",
                "BedroomsTotal", "BathroomsTotalInteger",
                "PropertyType", "StandardStatus"
            ],
            orderby="ListPrice asc"
        )
    
    # Usage
    results = search_properties(
        min_price=300000,
        max_price=600000,
        city="Provo",
        bedrooms=3
    )
    ```

??? example "Map-Based Property Search"
    ```python
    def find_properties_near_location(latitude, longitude, radius_miles=5):
        """Find properties within a radius of coordinates."""
        
        # Convert miles to approximate degrees (rough approximation)
        # 1 degree ≈ 69 miles
        degree_radius = radius_miles / 69
        
        filter_query = (
            f"StandardStatus eq 'Active' and "
            f"Latitude ge {latitude - degree_radius} and "
            f"Latitude le {latitude + degree_radius} and "
            f"Longitude ge {longitude - degree_radius} and "
            f"Longitude le {longitude + degree_radius}"
        )
        
        return client.property.get_properties(
            filter_query=filter_query,
            select=[
                "ListingId", "Address", "City", "ListPrice",
                "Latitude", "Longitude", "BedroomsTotal"
            ]
        )
    
    # Find properties near Salt Lake City center
    nearby_properties = find_properties_near_location(40.7608, -111.8910, 10)
    ```

### **Market Analysis**

??? example "Price Analysis by City"
    ```python
    def analyze_market_by_city(city_name):
        """Analyze property market in a specific city."""
        
        active_properties = client.property.get_properties(
            filter_query=f"City eq '{city_name}' and StandardStatus eq 'Active'",
            select=[
                "ListingId", "ListPrice", "BedroomsTotal", 
                "BathroomsTotalInteger", "SquareFeet"
            ]
        )
        
        if not active_properties:
            return f"No active properties found in {city_name}"
        
        prices = [p['ListPrice'] for p in active_properties if p.get('ListPrice')]
        
        analysis = {
            'city': city_name,
            'total_listings': len(active_properties),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'median_price': sorted(prices)[len(prices)//2] if prices else 0
        }
        
        return analysis
    
    # Analyze multiple cities
    cities = ['Salt Lake City', 'Provo', 'Ogden', 'West Valley City']
    for city in cities:
        stats = analyze_market_by_city(city)
        print(f"{city}: {stats['total_listings']} listings, "
              f"avg ${stats['avg_price']:,.0f}")
    ```

### **Agent Management**

??? example "Agent Performance Dashboard"
    ```python
    def get_agent_listings(agent_key):
        """Get all active listings for a specific agent."""
        
        listings = client.property.get_properties(
            filter_query=f"ListAgentKey eq '{agent_key}' and StandardStatus eq 'Active'",
            select=[
                "ListingId", "ListPrice", "City", "DaysOnMarket",
                "StandardStatus", "ListAgentKey"
            ]
        )
        
        if not listings:
            return None
        
        total_value = sum(p.get('ListPrice', 0) for p in listings)
        avg_days_on_market = sum(p.get('DaysOnMarket', 0) for p in listings) / len(listings)
        
        return {
            'agent_key': agent_key,
            'active_listings': len(listings),
            'total_listing_value': total_value,
            'average_days_on_market': avg_days_on_market,
            'listings': listings
        }
    
    def get_top_agents_by_volume():
        """Find agents with highest listing volume."""
        
        # Get all active listings
        all_listings = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            select=["ListAgentKey", "ListPrice"]
        )
        
        # Group by agent
        agent_stats = {}
        for listing in all_listings:
            agent_key = listing.get('ListAgentKey')
            if agent_key:
                if agent_key not in agent_stats:
                    agent_stats[agent_key] = {'count': 0, 'total_value': 0}
                agent_stats[agent_key]['count'] += 1
                agent_stats[agent_key]['total_value'] += listing.get('ListPrice', 0)
        
        # Sort by listing count
        top_agents = sorted(
            agent_stats.items(), 
            key=lambda x: x[1]['count'], 
            reverse=True
        )[:10]
        
        return top_agents
    ```

---

## 🔧 Integration Patterns

### **Database Synchronization**

??? example "SQLite Integration"
    ```python
    import sqlite3
    from datetime import datetime
    
    def sync_properties_to_sqlite(db_path="properties.db"):
        """Sync WFRMLS properties to local SQLite database."""
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                listing_id TEXT PRIMARY KEY,
                list_price INTEGER,
                city TEXT,
                bedrooms INTEGER,
                bathrooms INTEGER,
                status TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        # Get recent properties
        properties = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            select=[
                "ListingId", "ListPrice", "City", 
                "BedroomsTotal", "BathroomsTotalInteger", "StandardStatus"
            ]
        )
        
        # Insert/update properties
        for prop in properties:
            cursor.execute('''
                INSERT OR REPLACE INTO properties 
                (listing_id, list_price, city, bedrooms, bathrooms, status, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                prop['ListingId'],
                prop.get('ListPrice'),
                prop.get('City'),
                prop.get('BedroomsTotal'),
                prop.get('BathroomsTotalInteger'),
                prop.get('StandardStatus'),
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
        
        print(f"Synchronized {len(properties)} properties to database")
    ```

### **CSV Export**

??? example "Export to CSV"
    ```python
    import csv
    from datetime import datetime
    
    def export_properties_to_csv(filename=None):
        """Export property data to CSV file."""
        
        if not filename:
            filename = f"properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Get property data
        properties = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            select=[
                "ListingId", "ListPrice", "City", "Address",
                "BedroomsTotal", "BathroomsTotalInteger", 
                "SquareFeet", "YearBuilt", "PropertyType"
            ]
        )
        
        if not properties:
            print("No properties to export")
            return
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ListingId', 'ListPrice', 'City', 'Address',
                'BedroomsTotal', 'BathroomsTotalInteger',
                'SquareFeet', 'YearBuilt', 'PropertyType'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for prop in properties:
                # Clean data for CSV
                clean_row = {}
                for field in fieldnames:
                    clean_row[field] = prop.get(field, '')
                writer.writerow(clean_row)
        
        print(f"Exported {len(properties)} properties to {filename}")
    ```

---

## 📈 Error Handling Examples

### **Robust API Calls**

??? example "Retry Logic with Backoff"
    ```python
    import time
    import random
    from wfrmls.exceptions import RateLimitError, WFRMLSError
    
    def robust_api_call(func, max_retries=3, **kwargs):
        """Make API call with retry logic and exponential backoff."""
        
        for attempt in range(max_retries):
            try:
                return func(**kwargs)
                
            except RateLimitError:
                if attempt < max_retries - 1:
                    # Exponential backoff with jitter
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited. Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
                    
            except WFRMLSError as e:
                print(f"API error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise
    
    # Usage
    properties = robust_api_call(
        client.property.get_properties,
        filter_query="StandardStatus eq 'Active'",
        top=100
    )
    ```

### **Batch Processing**

??? example "Process Large Datasets"
    ```python
    def process_all_properties_in_batches(batch_size=100):
        """Process all properties in manageable batches."""
        
        skip = 0
        total_processed = 0
        
        while True:
            try:
                # Get batch of properties
                batch = robust_api_call(
                    client.property.get_properties,
                    filter_query="StandardStatus eq 'Active'",
                    top=batch_size,
                    skip=skip
                )
                
                if not batch:
                    break
                
                # Process this batch
                for prop in batch:
                    # Your processing logic here
                    print(f"Processing {prop['ListingId']}")
                
                total_processed += len(batch)
                skip += batch_size
                
                print(f"Processed {total_processed} properties so far...")
                
                # Small delay to be respectful of API limits
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing batch starting at {skip}: {e}")
                break
        
        print(f"Finished processing {total_processed} total properties")
    ```

---

## 📚 More Examples

### **By Category**
- **[Basic Usage](basic-usage.md)** - Simple operations and common patterns
- **[Advanced Queries](advanced-queries.md)** - Complex filtering and data manipulation
- **[Real Estate Apps](real-estate-apps.md)** - Complete application examples
- **[Data Integration](data-integration.md)** - Database and system integration
- **[Monitoring & Analytics](monitoring.md)** - Performance tracking and analysis

### **By Use Case**
- **Property Search Portals** → [Real Estate Apps](real-estate-apps.md)
- **Market Analysis Tools** → [Analytics Examples](monitoring.md)
- **CRM Integration** → [Data Integration](data-integration.md)
- **Data Warehousing** → [Advanced Queries](advanced-queries.md)

---

## 🆘 Need Help?

### **Documentation**
- **[API Reference](../api/index.md)** - Complete method documentation
- **[User Guides](../guides/index.md)** - Step-by-step tutorials
- **[Getting Started](../getting-started/index.md)** - Setup and basics

### **Support**
- **[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)** - Report bugs
- **[GitHub Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Ask questions
- **[WFRMLS Support](https://vendor.utahrealestate.com)** - API access issues

---

*Looking for a specific example? Browse the categories above or use the search function.* 