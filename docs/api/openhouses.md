# Open House API Reference

The Open House module provides access to open house events and schedules in the WFRMLS system. This includes event details, timing, property associations, and agent information.

---

## Overview

The `OpenHouseService` class handles all open house-related operations through the WFRMLS API. Open houses represent scheduled property showings and events where potential buyers can view properties.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
openhouse_service = client.openhouse
```

---

## Methods

### get_openhouses()

Retrieve a list of open houses with optional filtering, sorting, and pagination.

```python
openhouses = client.openhouse.get_openhouses(
    top=50,
    filter_query="OpenHouseDate ge 2024-01-01T00:00:00Z",
    orderby="OpenHouseDate asc"
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

`List[Dict[str, Any]]`: List of open house records matching the query criteria.

#### Example

```python
# Get upcoming open houses
upcoming_openhouses = client.openhouse.get_openhouses(
    filter_query="OpenHouseDate ge 2024-01-01T00:00:00Z",
    select=["OpenHouseKey", "PropertyKey", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime"],
    orderby="OpenHouseDate asc",
    top=100
)

# Get open houses for a specific property
property_openhouses = client.openhouse.get_openhouses(
    filter_query="PropertyKey eq '12345678'",
    orderby="OpenHouseDate desc"
)

# Get open houses by agent
agent_openhouses = client.openhouse.get_openhouses(
    filter_query="OpenHouseAgentKey eq 'AGENT123'",
    select=["OpenHouseKey", "PropertyKey", "OpenHouseDate", "OpenHouseStartTime"]
)
```

---

### get_openhouse()

Retrieve a specific open house by its unique identifier.

```python
openhouse = client.openhouse.get_openhouse("OPENHOUSE123")
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `openhouse_key` | `str` | Yes | - | The unique identifier for the open house. |
| `select` | `Optional[List[str]]` | No | `None` | Specific fields to return. If not provided, returns all available fields. |

#### Returns

`Dict[str, Any]`: Complete open house record for the specified open house.

#### Raises

- `NotFoundError`: If the open house with the specified key is not found.
- `WFRMLSError`: For other API-related errors.

#### Example

```python
# Get complete open house record
openhouse = client.openhouse.get_openhouse("OPENHOUSE123")

# Get specific fields only
openhouse_schedule = client.openhouse.get_openhouse(
    "OPENHOUSE123",
    select=["OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime", "PropertyKey"]
)
```

---

## Common Use Cases

### Upcoming Open Houses

```python
from datetime import datetime, timedelta

# Get open houses for the next 7 days
next_week = datetime.now() + timedelta(days=7)
upcoming_openhouses = client.openhouse.get_openhouses(
    filter_query=f"OpenHouseDate ge {datetime.now().isoformat()}Z and OpenHouseDate le {next_week.isoformat()}Z",
    select=[
        "OpenHouseKey", "PropertyKey", "OpenHouseDate", 
        "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseAgentKey"
    ],
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)

for oh in upcoming_openhouses:
    print(f"Open House: {oh['PropertyKey']} on {oh['OpenHouseDate']}")
    print(f"  Time: {oh['OpenHouseStartTime']} - {oh['OpenHouseEndTime']}")
```

### Weekend Open House Schedule

```python
# Get all open houses for the upcoming weekend
from datetime import datetime, timedelta

# Find next Saturday and Sunday
today = datetime.now()
days_until_saturday = (5 - today.weekday()) % 7
if days_until_saturday == 0 and today.weekday() == 5:  # Today is Saturday
    saturday = today
else:
    saturday = today + timedelta(days=days_until_saturday)
sunday = saturday + timedelta(days=1)

weekend_openhouses = client.openhouse.get_openhouses(
    filter_query=f"OpenHouseDate ge {saturday.date().isoformat()}T00:00:00Z and OpenHouseDate le {sunday.date().isoformat()}T23:59:59Z",
    select=[
        "OpenHouseKey", "PropertyKey", "OpenHouseDate", "OpenHouseStartTime", 
        "OpenHouseEndTime", "OpenHouseAgentKey", "OpenHouseRemarks"
    ],
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)

print(f"Weekend Open Houses ({saturday.date()} - {sunday.date()}):")
for oh in weekend_openhouses:
    date_str = oh['OpenHouseDate'][:10]  # Extract date part
    print(f"  {date_str} {oh['OpenHouseStartTime']}-{oh['OpenHouseEndTime']}: Property {oh['PropertyKey']}")
```

### Agent Open House Schedule

```python
# Get an agent's open house schedule
def get_agent_openhouse_schedule(agent_key, days_ahead=30):
    """Get open house schedule for a specific agent."""
    end_date = datetime.now() + timedelta(days=days_ahead)
    
    agent_openhouses = client.openhouse.get_openhouses(
        filter_query=f"OpenHouseAgentKey eq '{agent_key}' and OpenHouseDate ge {datetime.now().isoformat()}Z and OpenHouseDate le {end_date.isoformat()}Z",
        select=[
            "OpenHouseKey", "PropertyKey", "OpenHouseDate", 
            "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseRemarks"
        ],
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    
    return agent_openhouses

# Usage
schedule = get_agent_openhouse_schedule("AGENT123")
for oh in schedule:
    print(f"{oh['OpenHouseDate']} {oh['OpenHouseStartTime']}: Property {oh['PropertyKey']}")
```

---

## Key Fields

### Identification Fields

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseKey` | `str` | Unique identifier for the open house |
| `PropertyKey` | `str` | Associated property identifier |
| `OpenHouseId` | `str` | Open house ID number |

### Scheduling Information

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseDate` | `date` | Date of the open house |
| `OpenHouseStartTime` | `time` | Start time of the open house |
| `OpenHouseEndTime` | `time` | End time of the open house |
| `OpenHouseTimeZone` | `str` | Time zone for the event |

### Agent Information

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseAgentKey` | `str` | Primary agent hosting the open house |
| `OpenHouseAgentName` | `str` | Name of the hosting agent |
| `OpenHouseAgentPhone` | `str` | Agent's contact phone number |
| `OpenHouseAgentEmail` | `str` | Agent's contact email |

### Event Details

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseType` | `str` | Type of open house (Public, Broker, etc.) |
| `OpenHouseMethod` | `str` | Method of showing (In-Person, Virtual, etc.) |
| `OpenHouseRemarks` | `str` | Additional comments or instructions |
| `OpenHouseRefreshments` | `str` | Information about refreshments |

### Status Information

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseStatus` | `str` | Current status (Active, Cancelled, etc.) |
| `OpenHouseAttendeeLimit` | `int` | Maximum number of attendees |
| `OpenHouseRegistrationRequired` | `bool` | Whether registration is required |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `ModificationTimestamp` | `datetime` | Last modification date/time |
| `OriginalEntryTimestamp` | `datetime` | Original creation date/time |

---

## Advanced Queries

### Date Range Filtering

```python
# Get open houses for a specific date range
from datetime import datetime, timedelta

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)

january_openhouses = client.openhouse.get_openhouses(
    filter_query=f"OpenHouseDate ge {start_date.isoformat()}Z and OpenHouseDate le {end_date.isoformat()}Z",
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)

# Get open houses for today
today = datetime.now().date()
today_openhouses = client.openhouse.get_openhouses(
    filter_query=f"OpenHouseDate eq {today.isoformat()}T00:00:00Z",
    orderby="OpenHouseStartTime asc"
)
```

### Time-Based Filtering

```python
# Get morning open houses (before noon)
morning_openhouses = client.openhouse.get_openhouses(
    filter_query="OpenHouseStartTime lt '12:00:00'",
    select=["OpenHouseKey", "PropertyKey", "OpenHouseDate", "OpenHouseStartTime"],
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)

# Get weekend open houses
weekend_openhouses = client.openhouse.get_openhouses(
    filter_query="day(OpenHouseDate) eq 0 or day(OpenHouseDate) eq 6",  # Sunday=0, Saturday=6
    orderby="OpenHouseDate asc"
)
```

### Property and Agent Filtering

```python
# Get open houses for multiple properties
property_keys = ["PROP123", "PROP456", "PROP789"]
property_filter = " or ".join([f"PropertyKey eq '{key}'" for key in property_keys])

multi_property_openhouses = client.openhouse.get_openhouses(
    filter_query=f"({property_filter})",
    orderby="OpenHouseDate asc"
)

# Get open houses by multiple agents
agent_keys = ["AGENT123", "AGENT456"]
agent_filter = " or ".join([f"OpenHouseAgentKey eq '{key}'" for key in agent_keys])

multi_agent_openhouses = client.openhouse.get_openhouses(
    filter_query=f"({agent_filter}) and OpenHouseDate ge {datetime.now().isoformat()}Z",
    orderby="OpenHouseDate asc"
)
```

---

## Integration Examples

### Open House with Property Details

```python
def get_openhouse_with_property(openhouse_key):
    """Get open house details along with property information."""
    try:
        # Get open house information
        openhouse = client.openhouse.get_openhouse(openhouse_key)
        
        # Get associated property details
        property_data = client.property.get_property(
            openhouse['PropertyKey'],
            select=[
                "PropertyKey", "ListPrice", "BedroomsTotal", "BathroomsTotalInteger",
                "LivingArea", "PropertyAddress", "PropertyCity", "PropertyStateOrProvince"
            ]
        )
        
        return {
            'openhouse': openhouse,
            'property': property_data
        }
        
    except NotFoundError:
        return None

# Usage
oh_details = get_openhouse_with_property("OPENHOUSE123")
if oh_details:
    oh = oh_details['openhouse']
    prop = oh_details['property']
    print(f"Open House: {oh['OpenHouseDate']} {oh['OpenHouseStartTime']}")
    print(f"Property: {prop['PropertyAddress']}, {prop['PropertyCity']}")
    print(f"Price: ${prop['ListPrice']:,}")
```

### Agent Open House Calendar

```python
def create_agent_calendar(agent_key, month=None, year=None):
    """Create a calendar view of an agent's open houses."""
    from datetime import datetime, timedelta
    import calendar
    
    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get open houses for the month
    openhouses = client.openhouse.get_openhouses(
        filter_query=f"OpenHouseAgentKey eq '{agent_key}' and OpenHouseDate ge {first_day.isoformat()}Z and OpenHouseDate le {last_day.isoformat()}Z",
        select=["OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime", "PropertyKey"],
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    
    # Group by date
    calendar_data = {}
    for oh in openhouses:
        date_str = oh['OpenHouseDate'][:10]
        if date_str not in calendar_data:
            calendar_data[date_str] = []
        calendar_data[date_str].append(oh)
    
    return calendar_data

# Usage
cal = create_agent_calendar("AGENT123", 1, 2024)
for date, openhouses in cal.items():
    print(f"\n{date}:")
    for oh in openhouses:
        print(f"  {oh['OpenHouseStartTime']}-{oh['OpenHouseEndTime']}: {oh['PropertyKey']}")
```

### Open House Analytics

```python
def analyze_openhouse_patterns():
    """Analyze open house scheduling patterns."""
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    # Get open houses for the last 90 days
    start_date = datetime.now() - timedelta(days=90)
    
    openhouses = client.openhouse.get_openhouses(
        filter_query=f"OpenHouseDate ge {start_date.isoformat()}Z",
        select=["OpenHouseDate", "OpenHouseStartTime", "OpenHouseAgentKey"],
        top=1000
    )
    
    # Analyze by day of week
    day_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    agent_counts = defaultdict(int)
    
    for oh in openhouses:
        # Parse date and time
        date_obj = datetime.fromisoformat(oh['OpenHouseDate'].replace('Z', '+00:00'))
        day_of_week = date_obj.strftime('%A')
        
        # Parse start time
        start_time = oh['OpenHouseStartTime']
        hour = int(start_time.split(':')[0])
        
        day_counts[day_of_week] += 1
        hour_counts[hour] += 1
        agent_counts[oh['OpenHouseAgentKey']] += 1
    
    return {
        'by_day': dict(day_counts),
        'by_hour': dict(hour_counts),
        'by_agent': dict(sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    }

# Usage
analytics = analyze_openhouse_patterns()
print("Open Houses by Day of Week:")
for day, count in analytics['by_day'].items():
    print(f"  {day}: {count}")
```

---

## Error Handling

```python
from wfrmls.exceptions import WFRMLSError, NotFoundError, ValidationError

try:
    # Attempt to get open house
    openhouse = client.openhouse.get_openhouse("INVALID_KEY")
    
except NotFoundError:
    print("Open house not found")
    
except ValidationError as e:
    print(f"Invalid request: {e}")
    
except WFRMLSError as e:
    print(f"API error: {e}")
```

---

## Best Practices

### Efficient Date Queries

```python
# Use specific date ranges to improve performance
from datetime import datetime, timedelta

# Get next 30 days of open houses
end_date = datetime.now() + timedelta(days=30)
upcoming_openhouses = client.openhouse.get_openhouses(
    filter_query=f"OpenHouseDate ge {datetime.now().isoformat()}Z and OpenHouseDate le {end_date.isoformat()}Z",
    select=["OpenHouseKey", "PropertyKey", "OpenHouseDate", "OpenHouseStartTime"],
    orderby="OpenHouseDate asc"
)
```

### Pagination for Large Datasets

```python
def get_all_openhouses_in_range(start_date, end_date):
    """Get all open houses in a date range using pagination."""
    all_openhouses = []
    skip = 0
    batch_size = 100
    
    while True:
        batch = client.openhouse.get_openhouses(
            filter_query=f"OpenHouseDate ge {start_date.isoformat()}Z and OpenHouseDate le {end_date.isoformat()}Z",
            top=batch_size,
            skip=skip,
            count=True
        )
        
        if not batch:
            break
            
        all_openhouses.extend(batch)
        skip += batch_size
        
        # Check if we've retrieved all records
        if len(batch) < batch_size:
            break
    
    return all_openhouses
```

### Caching Open House Data

```python
from functools import lru_cache
from datetime import datetime, timedelta

class OpenHouseCache:
    def __init__(self, client):
        self.client = client
        self._cache = {}
        self._cache_timeout = timedelta(minutes=30)  # Shorter timeout for time-sensitive data
    
    def get_upcoming_openhouses(self, days=7):
        """Get upcoming open houses with caching."""
        cache_key = f"upcoming_{days}"
        now = datetime.now()
        
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if now - timestamp < self._cache_timeout:
                return cached_data
        
        # Fetch fresh data
        end_date = now + timedelta(days=days)
        openhouses = self.client.openhouse.get_openhouses(
            filter_query=f"OpenHouseDate ge {now.isoformat()}Z and OpenHouseDate le {end_date.isoformat()}Z",
            orderby="OpenHouseDate asc, OpenHouseStartTime asc"
        )
        
        self._cache[cache_key] = (openhouses, now)
        return openhouses
```

### Open House Notifications

```python
def check_for_new_openhouses(last_check_time):
    """Check for newly added open houses since last check."""
    new_openhouses = client.openhouse.get_openhouses(
        filter_query=f"OriginalEntryTimestamp ge {last_check_time.isoformat()}Z",
        select=[
            "OpenHouseKey", "PropertyKey", "OpenHouseDate", 
            "OpenHouseStartTime", "OpenHouseAgentKey", "OriginalEntryTimestamp"
        ],
        orderby="OriginalEntryTimestamp desc"
    )
    
    return new_openhouses

# Usage
from datetime import datetime, timedelta

last_check = datetime.now() - timedelta(hours=1)
new_events = check_for_new_openhouses(last_check)

for event in new_events:
    print(f"New open house: Property {event['PropertyKey']} on {event['OpenHouseDate']}")
```

---

## Related Resources

- **[Property API](properties.md)** - For property information associated with open houses
- **[Member API](members.md)** - For agent information hosting open houses
- **[OData Queries Guide](../guides/odata-queries.md)** - Advanced filtering and querying
- **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling strategies