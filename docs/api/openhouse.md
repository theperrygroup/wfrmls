# OpenHouse API

Complete reference for the OpenHouse endpoint of the WFRMLS Python client.

---

## 🏠 Overview

The OpenHouse API provides access to scheduled open house events for property listings. This endpoint allows you to find upcoming open houses, get details about scheduled showings, and filter by various criteria.

### Key Features

- **Event scheduling** - Access open house dates and times
- **Property association** - Link open houses to property listings
- **Agent information** - See hosting agent details
- **Time filtering** - Find upcoming or active open houses
- **Location details** - Get addresses and directions

---

## 📚 Methods

### `get_open_houses()`

Retrieve open house records with optional filtering and pagination.

```python
def get_open_houses(
    top: Optional[int] = None,
    skip: Optional[int] = None,
    filter_query: Optional[str] = None,
    select: Optional[List[str]] = None,
    orderby: Optional[str] = None,
    count: bool = False
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top` | `Optional[int]` | `None` | Maximum number of results to return (max 200) |
| `skip` | `Optional[int]` | `None` | Number of results to skip (for pagination) |
| `filter_query` | `Optional[str]` | `None` | OData filter expression |
| `select` | `Optional[List[str]]` | `None` | List of fields to include in response |
| `orderby` | `Optional[str]` | `None` | Field(s) to sort by with optional direction |
| `count` | `bool` | `False` | Include total count in response metadata |

**Returns:**
- `Dict[str, Any]` - Response dictionary with open house data

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get all open houses
open_houses = client.openhouse.get_open_houses()

# Get open houses for a specific date
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
todays_open_houses = client.openhouse.get_open_houses(
    filter_query=f"OpenHouseDate eq {today}"
)

# Get open houses with property details
detailed_open_houses = client.openhouse.get_open_houses(
    select=["OpenHouseKey", "ListingKey", "OpenHouseDate", 
            "OpenHouseStartTime", "OpenHouseEndTime", "OpenHouseRemarks"],
    orderby="OpenHouseDate desc"
)
```

### `get_active_open_houses()`

Get currently active open houses.

```python
def get_active_open_houses(
    top: Optional[int] = None,
    skip: Optional[int] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top` | `Optional[int]` | `None` | Maximum number of results |
| `skip` | `Optional[int]` | `None` | Number of results to skip |

**Returns:**
- `Dict[str, Any]` - Active open house records

**Examples:**

```python
# Get currently active open houses
active = client.openhouse.get_active_open_houses()

# Get first 10 active open houses
active_limited = client.openhouse.get_active_open_houses(top=10)
```

### `get_upcoming_open_houses()`

Get open houses scheduled for the future.

```python
def get_upcoming_open_houses(
    days_ahead: int = 7,
    top: Optional[int] = None,
    skip: Optional[int] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days_ahead` | `int` | `7` | Number of days to look ahead |
| `top` | `Optional[int]` | `None` | Maximum number of results |
| `skip` | `Optional[int]` | `None` | Number of results to skip |

**Returns:**
- `Dict[str, Any]` - Upcoming open house records

**Examples:**

```python
# Get open houses for next 7 days
upcoming = client.openhouse.get_upcoming_open_houses()

# Get open houses for next 30 days
month_ahead = client.openhouse.get_upcoming_open_houses(days_ahead=30)

# Get next 5 upcoming open houses
next_five = client.openhouse.get_upcoming_open_houses(
    days_ahead=30,
    top=5
)
```

### `get_open_houses_by_listing()`

Get all open houses for a specific property listing.

```python
def get_open_houses_by_listing(
    listing_key: str
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|----------|------|-------------|
| `listing_key` | `str` | The ListingKey of the property |

**Returns:**
- `Dict[str, Any]` - Open houses for the specified listing

**Examples:**

```python
# Get open houses for a specific property
listing_open_houses = client.openhouse.get_open_houses_by_listing("12345678")

# Process results
for oh in listing_open_houses["value"]:
    print(f"Date: {oh['OpenHouseDate']}")
    print(f"Time: {oh['OpenHouseStartTime']} - {oh['OpenHouseEndTime']}")
```

---

## 🏷️ Field Reference

**Note:** Field availability may vary based on MLS configuration and data availability. The following fields are commonly available:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OpenHouseKey** | `string` | Unique identifier | `"OH123456"` |
| **ListingKey** | `string` | Associated property ID | `"12345678"` |
| **ListingId** | `string` | MLS listing number | `"12345678"` |
| **OpenHouseDate** | `date` | Date of open house | `"2024-02-15"` |
| **OpenHouseStartTime** | `time` | Start time | `"10:00:00"` |
| **OpenHouseEndTime** | `time` | End time | `"14:00:00"` |
| **OpenHouseRemarks** | `string` | Additional information | `"Refreshments served"` |
| **OpenHouseType** | `string` | Type of open house | `"Public"` |
| **OpenHouseStatus** | `string` | Status | `"Active"` |
| **ShowingAgentKey** | `string` | Hosting agent ID | `"AG123456"` |
| **ShowingAgentMlsId** | `string` | Agent MLS ID | `"123456"` |
| **ShowingAgentFirstName** | `string` | Agent first name | `"John"` |
| **ShowingAgentLastName** | `string` | Agent last name | `"Doe"` |
| **ShowingAgentPhone** | `string` | Agent phone | `"(555) 123-4567"` |
| **AppointmentRequiredYN** | `boolean` | Appointment needed | `false` |
| **ModificationTimestamp** | `datetime` | Last modified | `"2024-01-31T10:30:00Z"` |

---

## 🔍 Common Usage Patterns

### Weekend Open House Schedule

```python
from datetime import datetime, timedelta

def get_weekend_open_houses():
    """Get open houses for the upcoming weekend."""
    
    # Calculate next Saturday and Sunday
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:  # Today is Saturday
        saturday = today
    else:
        saturday = today + timedelta(days=days_until_saturday)
    
    sunday = saturday + timedelta(days=1)
    
    # Format dates for filter
    sat_date = saturday.strftime("%Y-%m-%d")
    sun_date = sunday.strftime("%Y-%m-%d")
    
    # Get open houses for both days
    response = client.openhouse.get_open_houses(
        filter_query=f"OpenHouseDate eq {sat_date} or OpenHouseDate eq {sun_date}",
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    
    return response

# Get weekend schedule
weekend_schedule = get_weekend_open_houses()
```

### Open House Calendar View

```python
def get_open_house_calendar(start_date: datetime, end_date: datetime):
    """Get open houses for calendar display."""
    
    # Format dates
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    
    # Get open houses in date range
    response = client.openhouse.get_open_houses(
        filter_query=f"OpenHouseDate ge {start} and OpenHouseDate le {end}",
        orderby="OpenHouseDate asc, OpenHouseStartTime asc",
        select=["OpenHouseKey", "ListingKey", "OpenHouseDate", 
                "OpenHouseStartTime", "OpenHouseEndTime", "ShowingAgentFirstName",
                "ShowingAgentLastName"]
    )
    
    # Group by date
    calendar = {}
    for oh in response["value"]:
        date = oh["OpenHouseDate"]
        if date not in calendar:
            calendar[date] = []
        calendar[date].append(oh)
    
    return calendar

# Get calendar for next month
start = datetime.now()
end = start + timedelta(days=30)
calendar = get_open_house_calendar(start, end)
```

### Agent Open House Report

```python
def get_agent_open_houses(agent_key: str, include_past: bool = False):
    """Get all open houses for a specific agent."""
    
    # Base filter for agent
    filter_parts = [f"ShowingAgentKey eq '{agent_key}'"]
    
    # Add date filter if not including past
    if not include_past:
        today = datetime.now().strftime("%Y-%m-%d")
        filter_parts.append(f"OpenHouseDate ge {today}")
    
    response = client.openhouse.get_open_houses(
        filter_query=" and ".join(filter_parts),
        orderby="OpenHouseDate asc, OpenHouseStartTime asc"
    )
    
    # Create summary
    summary = {
        "total": len(response["value"]),
        "by_date": {}
    }
    
    for oh in response["value"]:
        date = oh["OpenHouseDate"]
        if date not in summary["by_date"]:
            summary["by_date"][date] = []
        summary["by_date"][date].append({
            "listing": oh["ListingKey"],
            "time": f"{oh['OpenHouseStartTime']} - {oh['OpenHouseEndTime']}"
        })
    
    return summary

# Get agent's open houses
agent_report = get_agent_open_houses("AG123456")
```

### Open House Notifications

```python
def find_new_open_houses(last_check: datetime):
    """Find open houses added since last check."""
    
    # Format timestamp
    last_check_str = last_check.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Get recently added open houses
    response = client.openhouse.get_open_houses(
        filter_query=f"ModificationTimestamp gt {last_check_str}",
        orderby="ModificationTimestamp desc"
    )
    
    # Group by listing
    new_by_listing = {}
    for oh in response["value"]:
        listing = oh["ListingKey"]
        if listing not in new_by_listing:
            new_by_listing[listing] = []
        new_by_listing[listing].append(oh)
    
    return new_by_listing

# Check for new open houses
last_check = datetime.now() - timedelta(hours=24)
new_open_houses = find_new_open_houses(last_check)
```

### Integration with Property Data

```python
def get_open_houses_with_property_details():
    """Get open houses with full property information."""
    
    # Get upcoming open houses
    open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=7)
    
    # Extract unique listing keys
    listing_keys = set()
    for oh in open_houses["value"]:
        listing_keys.add(oh["ListingKey"])
    
    # Get property details
    if listing_keys:
        filter_parts = [f"ListingKey eq '{key}'" for key in listing_keys]
        properties = client.property.get_properties(
            filter_query=" or ".join(filter_parts),
            select=["ListingKey", "UnparsedAddress", "ListPrice", 
                    "BedroomsTotal", "BathroomsFull", "BathroomsHalf"]
        )
        
        # Create lookup map
        property_map = {p["ListingKey"]: p for p in properties["value"]}
        
        # Combine data
        enriched = []
        for oh in open_houses["value"]:
            listing_key = oh["ListingKey"]
            if listing_key in property_map:
                combined = {**oh, "property": property_map[listing_key]}
                enriched.append(combined)
        
        return enriched
    
    return []

# Get enriched open house data
detailed_open_houses = get_open_houses_with_property_details()
```

---

## ⚡ Performance Tips

1. **Use field selection** - Only request fields you need
2. **Implement pagination** - Handle large result sets efficiently
3. **Cache agent/property data** - Avoid repeated lookups
4. **Use date filters** - Limit results to relevant time periods
5. **Batch property lookups** - Get all properties in one request

---

## 🚨 Important Notes

- Open house data availability depends on MLS practices and agent participation
- Times are typically in the MLS's local timezone
- Some MLSs may have restrictions on displaying open house information
- Always verify open house details as schedules can change
- Consider implementing refresh mechanisms for real-time applications