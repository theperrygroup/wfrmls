# WFRMLS API Examples

This guide provides comprehensive examples for using the WFRMLS Python API wrapper in real-world scenarios.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Property Search Examples](#property-search-examples)
3. [Agent and Member Examples](#agent-and-member-examples)
4. [Office and Brokerage Examples](#office-and-brokerage-examples)
5. [Media and Photos](#media-and-photos)
6. [Analytics and Market Data](#analytics-and-market-data)
7. [Advanced Use Cases](#advanced-use-cases)
8. [Error Handling Patterns](#error-handling-patterns)

## Basic Setup

### Client Initialization

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError, AuthenticationError

# Initialize with environment variable (recommended)
client = WFRMLSClient()

# Or with explicit API key
client = WFRMLSClient(api_key="your_api_key_here")

# Test connection
try:
    resources = client.resource.get_resources()
    print("✅ Connected to WFRMLS API")
    print(f"Available resources: {[r['resourceName'] for r in resources]}")
except AuthenticationError:
    print("❌ Authentication failed - check your API key")
except WFRMLSError as e:
    print(f"❌ API error: {e}")
```

### Environment Configuration

```python
# .env file
WFRMLS_BEARER_TOKEN=your_api_key_here

# In your code
from dotenv import load_dotenv
load_dotenv()

client = WFRMLSClient()  # Will automatically use environment variable
```

## Property Search Examples

### Basic Property Search

```python
# Search for all active residential properties in Salt Lake City
properties = client.properties.search_properties(
    city="Salt Lake City",
    property_type="Residential",
    listing_status="Active"
)

print(f"Found {len(properties)} active residential properties")
for prop in properties[:5]:  # Show first 5
    print(f"${prop['ListPrice']:,} - {prop['UnparsedAddress']}")
```

### Price Range Filtering

```python
# Find homes between $300k and $600k
affordable_homes = client.properties.search_properties(
    city="Salt Lake City",
    min_list_price=300000,
    max_list_price=600000,
    property_type="Residential",
    listing_status="Active"
)

print(f"Found {len(affordable_homes)} homes in price range")

# Calculate average price
if affordable_homes:
    avg_price = sum(prop['ListPrice'] for prop in affordable_homes) / len(affordable_homes)
    print(f"Average price: ${avg_price:,.0f}")
```

### Bedroom and Bathroom Filtering

```python
# Find 3+ bedroom, 2+ bathroom homes
family_homes = client.properties.search_properties(
    city="Salt Lake City",
    bedrooms_total=3,  # Minimum 3 bedrooms
    bathrooms_total_integer=2,  # Minimum 2 full bathrooms
    property_type="Residential",
    listing_status="Active",
    page_size=50
)

for home in family_homes:
    bedrooms = home.get('BedroomsTotal', 'N/A')
    bathrooms = home.get('BathroomsTotalInteger', 'N/A')
    print(f"{bedrooms}BR/{bathrooms}BA - ${home['ListPrice']:,} - {home['UnparsedAddress']}")
```

### Recently Listed Properties

```python
from datetime import date, timedelta

# Find properties listed in the last 7 days
recent_date = date.today() - timedelta(days=7)
recent_listings = client.properties.search_properties(
    modification_timestamp_from=recent_date,
    listing_status="Active",
    city="Salt Lake City",
    page_size=25
)

print(f"Found {len(recent_listings)} properties listed in the last 7 days")
for prop in recent_listings:
    list_date = prop.get('ListingContractDate', 'Unknown')
    print(f"Listed {list_date}: ${prop['ListPrice']:,} - {prop['UnparsedAddress']}")
```

### Property Details

```python
# Get detailed information for a specific property
property_id = "your_property_id_here"

try:
    property_details = client.properties.get_property(property_id)
    
    print(f"Property Details for {property_id}:")
    print(f"Address: {property_details.get('UnparsedAddress')}")
    print(f"Price: ${property_details.get('ListPrice', 0):,}")
    print(f"Bedrooms: {property_details.get('BedroomsTotal', 'N/A')}")
    print(f"Bathrooms: {property_details.get('BathroomsTotalInteger', 'N/A')}")
    print(f"Square Feet: {property_details.get('LivingArea', 'N/A')}")
    print(f"Lot Size: {property_details.get('LotSizeAcres', 'N/A')} acres")
    print(f"Year Built: {property_details.get('YearBuilt', 'N/A')}")
    print(f"Property Type: {property_details.get('PropertyType', 'N/A')}")
    
except WFRMLSError as e:
    print(f"Error retrieving property {property_id}: {e}")
```

## Agent and Member Examples

### Agent Search

```python
# Search for agents by name
agents = client.member.search_members(
    first_name="John",
    last_name="Smith"
)

print(f"Found {len(agents)} agents named John Smith")
for agent in agents:
    print(f"{agent.get('MemberFullName')} - {agent.get('OfficePhoneNumber')}")
```

### Agent Details and Listings

```python
# Get agent details and their recent listings
agent_id = "agent_key_here"

try:
    # Get agent information
    agent_details = client.member.get_member(agent_id)
    print(f"Agent: {agent_details.get('MemberFullName')}")
    print(f"Office: {agent_details.get('OfficeName')}")
    print(f"Phone: {agent_details.get('OfficePhoneNumber')}")
    
    # Find their recent listings
    agent_listings = client.properties.search_properties(
        listing_agent_key=agent_id,
        listing_status="Active",
        page_size=20
    )
    
    print(f"\nCurrent Listings ({len(agent_listings)}):")
    for listing in agent_listings:
        print(f"${listing['ListPrice']:,} - {listing['UnparsedAddress']}")
        
except WFRMLSError as e:
    print(f"Error retrieving agent data: {e}")
```

### Top Agents by Listings

```python
# Find agents with the most active listings
from collections import Counter

# Get recent listings
all_listings = client.properties.search_properties(
    listing_status="Active",
    city="Salt Lake City",
    page_size=200
)

# Count listings per agent
agent_counts = Counter()
for listing in all_listings:
    agent_key = listing.get('ListAgentKey')
    if agent_key:
        agent_counts[agent_key] += 1

# Get details for top 10 agents
print("Top 10 Agents by Active Listings:")
for agent_key, count in agent_counts.most_common(10):
    try:
        agent = client.member.get_member(agent_key)
        print(f"{agent.get('MemberFullName', 'Unknown')}: {count} listings")
    except WFRMLSError:
        print(f"Agent {agent_key}: {count} listings")
```

## Office and Brokerage Examples

### Office Search

```python
# Find offices in specific cities
offices = client.office.search_offices(
    office_city="Salt Lake City"
)

print(f"Found {len(offices)} offices in Salt Lake City")
for office in offices:
    print(f"{office.get('OfficeName')} - {office.get('OfficePhoneNumber')}")
```

### Office Performance Analysis

```python
# Analyze office performance by listings
office_performance = {}

# Get all active listings
listings = client.properties.search_properties(
    listing_status="Active",
    city="Salt Lake City",
    page_size=500
)

# Group by office
for listing in listings:
    office_key = listing.get('ListOfficeKey')
    if office_key:
        if office_key not in office_performance:
            office_performance[office_key] = {
                'listing_count': 0,
                'total_value': 0,
                'avg_price': 0
            }
        
        office_performance[office_key]['listing_count'] += 1
        office_performance[office_key]['total_value'] += listing.get('ListPrice', 0)

# Calculate averages and get office details
for office_key, stats in office_performance.items():
    if stats['listing_count'] > 0:
        stats['avg_price'] = stats['total_value'] / stats['listing_count']
    
    try:
        office_details = client.office.get_office(office_key)
        office_name = office_details.get('OfficeName', 'Unknown Office')
        
        print(f"{office_name}:")
        print(f"  Active Listings: {stats['listing_count']}")
        print(f"  Total Value: ${stats['total_value']:,}")
        print(f"  Average Price: ${stats['avg_price']:,.0f}\n")
        
    except WFRMLSError:
        continue
```

## Media and Photos

### Property Photos

```python
# Get all media for a property
property_id = "your_property_id_here"

try:
    media_items = client.media.search_media(
        resource_name="Property",
        resource_record_key=property_id
    )
    
    print(f"Found {len(media_items)} media items for property {property_id}")
    
    # Download first photo
    if media_items:
        first_photo = media_items[0]
        photo_url = first_photo['MediaURL']
        
        # Download the photo
        photo_data = client.media.get_media_object(photo_url)
        
        # Save to file
        filename = f"property_{property_id}_photo_1.jpg"
        with open(filename, "wb") as f:
            f.write(photo_data)
        
        print(f"Downloaded photo: {filename}")
        print(f"Photo details: {first_photo.get('MediaDescription', 'No description')}")
    
except WFRMLSError as e:
    print(f"Error retrieving media: {e}")
```

### Bulk Photo Download

```python
import os
from pathlib import Path

def download_property_photos(property_id, max_photos=5):
    """Download up to max_photos for a property."""
    
    # Create directory for this property
    photo_dir = Path(f"property_photos/{property_id}")
    photo_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        media_items = client.media.search_media(
            resource_name="Property",
            resource_record_key=property_id
        )
        
        # Filter for images only
        photos = [item for item in media_items if 'image' in item.get('MediaType', '').lower()]
        
        downloaded = 0
        for i, photo in enumerate(photos[:max_photos]):
            try:
                photo_data = client.media.get_media_object(photo['MediaURL'])
                filename = photo_dir / f"photo_{i+1}.jpg"
                
                with open(filename, "wb") as f:
                    f.write(photo_data)
                
                downloaded += 1
                print(f"Downloaded: {filename}")
                
            except Exception as e:
                print(f"Error downloading photo {i+1}: {e}")
        
        print(f"Downloaded {downloaded} photos for property {property_id}")
        
    except WFRMLSError as e:
        print(f"Error retrieving media for property {property_id}: {e}")

# Usage
property_ids = ["123456", "789012", "345678"]
for prop_id in property_ids:
    download_property_photos(prop_id)
```

## Analytics and Market Data

### Market Statistics

```python
# Get market analytics for different areas
areas = ["Salt Lake City", "West Valley City", "Sandy", "Provo"]

for area in areas:
    properties = client.properties.search_properties(
        city=area,
        listing_status="Active",
        property_type="Residential",
        page_size=100
    )
    
    if properties:
        prices = [prop['ListPrice'] for prop in properties]
        
        print(f"\n{area} Market Analysis:")
        print(f"Active Listings: {len(properties)}")
        print(f"Average Price: ${sum(prices) / len(prices):,.0f}")
        print(f"Median Price: ${sorted(prices)[len(prices)//2]:,.0f}")
        print(f"Price Range: ${min(prices):,} - ${max(prices):,}")
```

### Days on Market Analysis

```python
from datetime import date, datetime

def calculate_days_on_market(properties):
    """Calculate days on market for a list of properties."""
    dom_data = []
    
    for prop in properties:
        list_date_str = prop.get('ListingContractDate')
        if list_date_str:
            try:
                # Parse date (adjust format as needed)
                list_date = datetime.strptime(list_date_str[:10], '%Y-%m-%d').date()
                days_on_market = (date.today() - list_date).days
                dom_data.append(days_on_market)
            except (ValueError, TypeError):
                continue
    
    return dom_data

# Analyze days on market by price range
price_ranges = [
    (0, 300000, "Under $300k"),
    (300000, 500000, "$300k-$500k"),
    (500000, 750000, "$500k-$750k"),
    (750000, float('inf'), "Over $750k")
]

for min_price, max_price, label in price_ranges:
    properties = client.properties.search_properties(
        city="Salt Lake City",
        min_list_price=min_price if min_price > 0 else None,
        max_list_price=max_price if max_price < float('inf') else None,
        listing_status="Active",
        property_type="Residential",
        page_size=100
    )
    
    dom_data = calculate_days_on_market(properties)
    
    if dom_data:
        avg_dom = sum(dom_data) / len(dom_data)
        print(f"{label}: {len(properties)} properties, {avg_dom:.0f} avg days on market")
```

## Advanced Use Cases

### Property Investment Analysis

```python
def analyze_investment_properties(city, max_price=500000):
    """Find and analyze potential investment properties."""
    
    properties = client.properties.search_properties(
        city=city,
        max_list_price=max_price,
        property_type="Residential",
        listing_status="Active",
        page_size=100
    )
    
    investment_candidates = []
    
    for prop in properties:
        # Basic investment metrics
        price = prop.get('ListPrice', 0)
        bedrooms = prop.get('BedroomsTotal', 0)
        bathrooms = prop.get('BathroomsTotalInteger', 0)
        sqft = prop.get('LivingArea', 0)
        
        # Calculate price per square foot
        price_per_sqft = price / sqft if sqft > 0 else 0
        
        # Simple investment score (customize based on your criteria)
        score = 0
        if bedrooms >= 3: score += 10
        if bathrooms >= 2: score += 10
        if price_per_sqft > 0 and price_per_sqft < 200: score += 20
        if price < 400000: score += 15
        
        if score >= 30:  # Threshold for consideration
            investment_candidates.append({
                'property': prop,
                'score': score,
                'price_per_sqft': price_per_sqft
            })
    
    # Sort by score
    investment_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"Top Investment Candidates in {city}:")
    for i, candidate in enumerate(investment_candidates[:10]):
        prop = candidate['property']
        print(f"{i+1}. ${prop['ListPrice']:,} - {prop['UnparsedAddress']}")
        print(f"   Score: {candidate['score']}, ${candidate['price_per_sqft']:.0f}/sqft")
        print()

# Usage
analyze_investment_properties("Salt Lake City")
```

### Market Comparison Tool

```python
def compare_markets(cities):
    """Compare market conditions across multiple cities."""
    
    comparison_data = {}
    
    for city in cities:
        properties = client.properties.search_properties(
            city=city,
            listing_status="Active",
            property_type="Residential",
            page_size=200
        )
        
        if properties:
            prices = [prop['ListPrice'] for prop in properties]
            sqft_data = [prop.get('LivingArea', 0) for prop in properties if prop.get('LivingArea', 0) > 0]
            
            comparison_data[city] = {
                'count': len(properties),
                'avg_price': sum(prices) / len(prices),
                'median_price': sorted(prices)[len(prices)//2],
                'avg_sqft': sum(sqft_data) / len(sqft_data) if sqft_data else 0,
                'avg_price_per_sqft': (sum(prices) / len(prices)) / (sum(sqft_data) / len(sqft_data)) if sqft_data else 0
            }
    
    # Print comparison
    print("Market Comparison:")
    print(f"{'City':<20} {'Count':<8} {'Avg Price':<12} {'Med Price':<12} {'$/SqFt':<8}")
    print("-" * 70)
    
    for city, data in comparison_data.items():
        print(f"{city:<20} {data['count']:<8} ${data['avg_price']:<11,.0f} ${data['median_price']:<11,.0f} ${data['avg_price_per_sqft']:<7.0f}")

# Usage
cities = ["Salt Lake City", "Provo", "Ogden", "West Valley City"]
compare_markets(cities)
```

## Error Handling Patterns

### Robust API Calls

```python
import time
import logging
from wfrmls.exceptions import WFRMLSError, AuthenticationError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(func, *args, **kwargs):
    """Execute API call with error handling and retries."""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise  # Don't retry auth errors
            
        except WFRMLSError as e:
            if "429" in str(e):  # Rate limit
                wait_time = retry_delay * (2 ** attempt)
                logger.warning(f"Rate limited, waiting {wait_time}s before retry")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"API error: {e}")
                if attempt == max_retries - 1:
                    raise
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if attempt == max_retries - 1:
                raise
    
    return None

# Usage
properties = safe_api_call(
    client.properties.search_properties,
    city="Salt Lake City",
    page_size=50
)
```

### Batch Processing with Error Handling

```python
def process_properties_batch(property_ids, batch_size=10):
    """Process multiple properties with error handling."""
    
    results = []
    failed = []
    
    for i in range(0, len(property_ids), batch_size):
        batch = property_ids[i:i + batch_size]
        
        for property_id in batch:
            try:
                property_data = safe_api_call(
                    client.properties.get_property,
                    property_id
                )
                
                if property_data:
                    results.append(property_data)
                    logger.info(f"Processed property {property_id}")
                    
            except Exception as e:
                logger.error(f"Failed to process property {property_id}: {e}")
                failed.append(property_id)
            
            # Small delay to respect rate limits
            time.sleep(0.1)
    
    logger.info(f"Processed {len(results)} properties, {len(failed)} failed")
    return results, failed

# Usage
property_list = ["123456", "789012", "345678", "901234"]
successful, failed = process_properties_batch(property_list)
```

### Validation Helpers

```python
def validate_search_params(**params):
    """Validate search parameters before API call."""
    
    errors = []
    
    # Price validation
    min_price = params.get('min_list_price')
    max_price = params.get('max_list_price')
    
    if min_price is not None and min_price < 0:
        errors.append("min_list_price must be positive")
    
    if max_price is not None and max_price < 0:
        errors.append("max_list_price must be positive")
    
    if min_price and max_price and min_price > max_price:
        errors.append("min_list_price cannot be greater than max_list_price")
    
    # Page size validation
    page_size = params.get('page_size')
    if page_size is not None and (page_size < 1 or page_size > 500):
        errors.append("page_size must be between 1 and 500")
    
    if errors:
        raise ValueError(f"Validation errors: {', '.join(errors)}")

# Usage
try:
    validate_search_params(
        min_list_price=200000,
        max_list_price=500000,
        page_size=50
    )
    
    properties = client.properties.search_properties(
        min_list_price=200000,
        max_list_price=500000,
        page_size=50
    )
    
except ValueError as e:
    print(f"Parameter validation failed: {e}")
except WFRMLSError as e:
    print(f"API error: {e}")
```

These examples demonstrate comprehensive usage patterns for the WFRMLS API wrapper. Remember to:

1. **Always handle errors appropriately** using the custom exception types
2. **Respect rate limits** by adding delays between requests
3. **Validate parameters** before making API calls
4. **Use pagination** for large result sets
5. **Cache results** when appropriate to minimize API calls
6. **Log operations** for debugging and monitoring

For more specific use cases or questions, refer to the [API Reference](api-reference.md) or [Troubleshooting Guide](troubleshooting.md). 