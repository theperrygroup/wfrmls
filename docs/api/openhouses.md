# Open Houses API

The Open Houses API provides access to scheduled open house events within the WFRMLS system. This includes event details, scheduling information, attendance tracking, and associated property data.

## Overview

The `OpenHouseClient` class handles all open house-related operations, providing methods to search, retrieve, and filter open house event data.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
open_houses = client.openhouse.get_open_houses(top=10)
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_open_houses()` | Retrieve multiple open houses with filtering | `List[Dict[str, Any]]` |
| `get_open_house()` | Get a specific open house by ID | `Dict[str, Any]` |
| `get_upcoming_open_houses()` | Get upcoming open houses within date range | `List[Dict[str, Any]]` |
| `search_open_houses()` | Search open houses by criteria | `List[Dict[str, Any]]` |

## Methods

### get_open_houses()

Retrieve multiple open houses with optional filtering, sorting, and pagination.

```python
def get_open_houses(
    self,
    select: Optional[List[str]] = None,
    filter_query: Optional[str] = None,
    orderby: Optional[str] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    count: bool = False,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `select` | `List[str]` | No | Specific fields to return |
| `filter_query` | `str` | No | OData filter expression |
| `orderby` | `str` | No | Field(s) to sort by |
| `top` | `int` | No | Maximum number of records to return |
| `skip` | `int` | No | Number of records to skip |
| `count` | `bool` | No | Include total count in response |

#### Examples

=== "Basic Usage"

    ```python
    # Get first 10 upcoming open houses
    open_houses = client.openhouse.get_open_houses(
        top=10,
        filter_query="OpenHouseDate ge datetime'2024-01-01T00:00:00Z'",
        orderby="OpenHouseDate asc"
    )
    
    for oh in open_houses:
        print(f"{oh['OpenHouseDate']} - {oh['ListingId']}")
    ```

=== "Specific Fields"

    ```python
    # Get only specific fields
    open_houses = client.openhouse.get_open_houses(
        select=["OpenHouseKey", "ListingId", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime"],
        filter_query="OpenHouseDate ge datetime'2024-01-01T00:00:00Z'",
        orderby="OpenHouseDate asc"
    )
    ```

=== "Date Range Filtering"

    ```python
    # Find open houses in specific date range
    from datetime import datetime, timedelta
    
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    open_houses = client.openhouse.get_open_houses(
        filter_query=f"OpenHouseDate ge datetime'{start_date.isoformat()}Z' and OpenHouseDate le datetime'{end_date.isoformat()}Z'",
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    ```

### get_open_house()

Retrieve a specific open house by its unique identifier.

```python
def get_open_house(
    self,
    open_house_key: str,
    select: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `open_house_key` | `str` | Yes | Unique open house identifier |
| `select` | `List[str]` | No | Specific fields to return |

#### Example

```python
# Get specific open house details
open_house = client.openhouse.get_open_house(
    open_house_key="12345",
    select=["OpenHouseKey", "ListingId", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseRemarks"]
)

print(f"Open House: {open_house['ListingId']}")
print(f"Date: {open_house['OpenHouseDate']}")
print(f"Time: {open_house['OpenHouseStartTime']} - {open_house['OpenHouseEndTime']}")
```

### get_upcoming_open_houses()

Retrieve upcoming open houses within a specified number of days.

```python
def get_upcoming_open_houses(
    self,
    days_ahead: int = 7,
    select: Optional[List[str]] = None,
    filter_query: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `days_ahead` | `int` | No | Number of days to look ahead (default: 7) |
| `select` | `List[str]` | No | Specific fields to return |
| `filter_query` | `str` | No | Additional filtering criteria |

#### Example

```python
# Get open houses for the next 14 days
upcoming = client.openhouse.get_upcoming_open_houses(
    days_ahead=14,
    select=["OpenHouseKey", "ListingId", "OpenHouseDate", "OpenHouseStartTime", "OpenHouseEndTime"]
)

print(f"Found {len(upcoming)} upcoming open houses")
for oh in upcoming:
    print(f"  {oh['OpenHouseDate']} {oh['OpenHouseStartTime']}: {oh['ListingId']}")
```

### search_open_houses()

Search for open houses using various criteria.

```python
def search_open_houses(
    self,
    listing_id: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    agent_key: Optional[str] = None,
    office_key: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `listing_id` | `str` | No | Specific listing ID |
| `date_from` | `datetime` | No | Start date for search |
| `date_to` | `datetime` | No | End date for search |
| `agent_key` | `str` | No | Agent identifier |
| `office_key` | `str` | No | Office identifier |

#### Example

```python
from datetime import datetime, timedelta

# Search by agent
agent_open_houses = client.openhouse.search_open_houses(
    agent_key="12345",
    date_from=datetime.now(),
    date_to=datetime.now() + timedelta(days=30)
)

# Search by listing
listing_open_houses = client.openhouse.search_open_houses(
    listing_id="1611952"
)
```

## Enums and Constants

### OpenHouseStatus

Enumeration of possible open house statuses:

```python
from wfrmls import OpenHouseStatus

class OpenHouseStatus(str, Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    POSTPONED = "Postponed"
```

### OpenHouseType

Enumeration of open house types:

```python
from wfrmls import OpenHouseType

class OpenHouseType(str, Enum):
    PUBLIC = "Public"
    BROKER = "Broker"
    PRIVATE = "Private"
    VIRTUAL = "Virtual"
```

### OpenHouseAttendedBy

Enumeration of attendance types:

```python
from wfrmls import OpenHouseAttendedBy

class OpenHouseAttendedBy(str, Enum):
    AGENT = "Agent"
    UNACCOMPANIED = "Unaccompanied"
    BOTH = "Both"
```

## Common Use Cases

### Weekly Open House Schedule

```python
# Generate weekly open house schedule
from datetime import datetime, timedelta

def get_weekly_schedule():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    open_houses = client.openhouse.get_open_houses(
        filter_query=f"OpenHouseDate ge datetime'{start_date.isoformat()}Z' and OpenHouseDate le datetime'{end_date.isoformat()}Z'",
        select=[
            "OpenHouseKey", "ListingId", "OpenHouseDate", 
            "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseRemarks"
        ],
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    
    # Group by date
    schedule = {}
    for oh in open_houses:
        date = oh['OpenHouseDate'][:10]  # Extract date part
        if date not in schedule:
            schedule[date] = []
        schedule[date].append(oh)
    
    # Display schedule
    for date, events in sorted(schedule.items()):
        print(f"\n{date}:")
        for event in events:
            print(f"  {event['OpenHouseStartTime']}-{event['OpenHouseEndTime']}: {event['ListingId']}")

get_weekly_schedule()
```

### Agent Open House Management

```python
# Manage open houses for a specific agent
def manage_agent_open_houses(agent_key: str):
    # Get upcoming open houses
    upcoming = client.openhouse.search_open_houses(
        agent_key=agent_key,
        date_from=datetime.now()
    )
    
    print(f"Upcoming open houses for agent {agent_key}:")
    for oh in upcoming:
        print(f"  {oh['OpenHouseDate']} {oh['OpenHouseStartTime']}: {oh['ListingId']}")
    
    return upcoming

agent_events = manage_agent_open_houses("12345")
```

### Property Open House History

```python
# Get open house history for a property
def get_property_open_house_history(listing_id: str):
    open_houses = client.openhouse.search_open_houses(
        listing_id=listing_id
    )
    
    # Sort by date
    open_houses.sort(key=lambda x: x['OpenHouseDate'], reverse=True)
    
    print(f"Open house history for {listing_id}:")
    for oh in open_houses:
        status = oh.get('OpenHouseStatus', 'Unknown')
        print(f"  {oh['OpenHouseDate']} {oh['OpenHouseStartTime']}: {status}")
    
    return open_houses

history = get_property_open_house_history("1611952")
```

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseKey` | `str` | Unique open house identifier |
| `ListingId` | `str` | Associated property listing ID |
| `OpenHouseDate` | `date` | Date of open house |
| `OpenHouseStartTime` | `time` | Start time |
| `OpenHouseEndTime` | `time` | End time |
| `OpenHouseStatus` | `str` | Current status |
| `OpenHouseType` | `str` | Type of open house |

### Event Details

| Field | Type | Description |
|-------|------|-------------|
| `OpenHouseRemarks` | `str` | Additional notes or instructions |
| `OpenHouseAttendedBy` | `str` | Who can attend (Agent, Unaccompanied, Both) |
| `OpenHouseRefreshments` | `str` | Refreshment information |
| `OpenHouseMethod` | `str` | Method of showing |

### Agent Information

| Field | Type | Description |
|-------|------|-------------|
| `ListAgentKey` | `str` | Listing agent identifier |
| `ListAgentMlsId` | `str` | Listing agent MLS ID |
| `ShowingAgentKey` | `str` | Showing agent identifier |
| `ShowingAgentMlsId` | `str` | Showing agent MLS ID |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `ShowingContactName` | `str` | Contact person name |
| `ShowingContactPhone` | `str` | Contact phone number |
| `ShowingContactPhoneExt` | `str` | Phone extension |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `OriginalEntryTimestamp` | `datetime` | When record was created |
| `ModificationTimestamp` | `datetime` | Last modification time |

## Advanced Filtering

### Date and Time Queries

```python
# Find weekend open houses
weekend_filter = """
(
    (dayofweek(OpenHouseDate) eq 1) or  # Sunday
    (dayofweek(OpenHouseDate) eq 7)     # Saturday
) and OpenHouseDate ge datetime'2024-01-01T00:00:00Z'
"""

weekend_open_houses = client.openhouse.get_open_houses(
    filter_query=weekend_filter,
    orderby="OpenHouseDate asc"
)
```

### Multi-criteria Search

```python
# Find public open houses in the afternoon
afternoon_public = client.openhouse.get_open_houses(
    filter_query="""
        OpenHouseType eq 'Public' and
        OpenHouseStartTime ge time'12:00:00' and
        OpenHouseDate ge datetime'2024-01-01T00:00:00Z'
    """,
    orderby="OpenHouseDate asc, OpenHouseStartTime asc"
)
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    open_house = client.openhouse.get_open_house("invalid_key")
except NotFoundError:
    print("Open house not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Use date range filters** to limit result sets
2. **Select specific fields** to reduce data transfer
3. **Cache frequently accessed data** like weekly schedules
4. **Use pagination** for large date ranges

### Data Management

1. **Track ModificationTimestamp** for updates
2. **Handle cancelled/postponed events** appropriately
3. **Validate date/time formats** before filtering
4. **Consider time zones** in date calculations

### User Experience

1. **Sort by date and time** for chronological display
2. **Group events by date** for better organization
3. **Show status clearly** (Active, Cancelled, etc.)
4. **Provide contact information** for inquiries

## Integration Examples

### Calendar Integration

```python
# Export open houses to calendar format
def export_to_calendar(agent_key: str = None):
    if agent_key:
        open_houses = client.openhouse.search_open_houses(
            agent_key=agent_key,
            date_from=datetime.now()
        )
    else:
        open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=30)
    
    # Convert to calendar events
    events = []
    for oh in open_houses:
        event = {
            'title': f"Open House - {oh['ListingId']}",
            'start': f"{oh['OpenHouseDate']}T{oh['OpenHouseStartTime']}",
            'end': f"{oh['OpenHouseDate']}T{oh['OpenHouseEndTime']}",
            'description': oh.get('OpenHouseRemarks', ''),
            'location': oh.get('PropertyAddress', '')
        }
        events.append(event)
    
    return events

calendar_events = export_to_calendar("12345")
```

### Website Integration

```python
# Generate open house listings for website
def generate_open_house_listings():
    upcoming = client.openhouse.get_upcoming_open_houses(
        days_ahead=14,
        select=[
            "OpenHouseKey", "ListingId", "OpenHouseDate",
            "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseRemarks"
        ]
    )
    
    # Format for web display
    listings = []
    for oh in upcoming:
        listing = {
            'id': oh['OpenHouseKey'],
            'property_id': oh['ListingId'],
            'date': oh['OpenHouseDate'],
            'start_time': oh['OpenHouseStartTime'],
            'end_time': oh['OpenHouseEndTime'],
            'description': oh.get('OpenHouseRemarks', ''),
            'formatted_date': format_date(oh['OpenHouseDate']),
            'formatted_time': f"{oh['OpenHouseStartTime']} - {oh['OpenHouseEndTime']}"
        }
        listings.append(listing)
    
    return listings

def format_date(date_str):
    # Convert to user-friendly format
    from datetime import datetime
    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return date_obj.strftime('%A, %B %d, %Y')

web_listings = generate_open_house_listings()
```

## Related Resources

- [Properties API](properties.md) - For property details
- [Members API](members.md) - For agent information
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management