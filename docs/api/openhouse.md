# Open Houses API

The Open Houses API provides access to open house schedules, events, and showing information. This is essential for finding upcoming open houses, managing showing schedules, and tracking property viewing events.

!!! example "Quick Start"
    ```python
    # Get upcoming open houses
    open_houses = client.openhouse.get_upcoming_open_houses(days_ahead=7)
    
    # Get open houses for a specific property
    property_opens = client.openhouse.get_open_houses_for_property("1611952")
    
    # Get open houses by agent
    agent_opens = client.openhouse.get_open_houses_by_agent("96422")
    ```

## Open House Client

::: wfrmls.openhouse.OpenHouseClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### Basic Open House Retrieval

=== "Upcoming Events"
    ```python
    # Get open houses for the next 7 days
    upcoming = client.openhouse.get_upcoming_open_houses(days_ahead=7)
    
    # Get this weekend's open houses
    weekend = client.openhouse.get_upcoming_open_houses(
        days_ahead=7,
        orderby="OpenHouseStartTime asc"
    )
    
    # Get today's open houses
    today = client.openhouse.get_todays_open_houses()
    ```

=== "Property-Specific"
    ```python
    # Get all open houses for a property
    property_opens = client.openhouse.get_open_houses_for_property("1611952")
    
    # Get future open houses for a property
    future_opens = client.openhouse.get_open_houses(
        filter_query=f"ListingId eq '1611952' and OpenHouseStartTime ge {datetime.utcnow().isoformat()}Z",
        orderby="OpenHouseStartTime asc"
    )
    ```

=== "Agent-Specific"
    ```python
    # Get open houses by agent
    agent_opens = client.openhouse.get_open_houses_by_agent("96422")
    
    # Get agent's upcoming open houses
    agent_upcoming = client.openhouse.get_open_houses(
        filter_query="ListAgentKey eq '96422' and OpenHouseStartTime ge now()",
        orderby="OpenHouseStartTime asc"
    )
    ```

### Advanced Filtering

=== "Date and Time Filters"
    ```python
    from datetime import datetime, timedelta
    
    # Open houses this weekend (Saturday-Sunday)
    saturday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    while saturday.weekday() != 5:  # Find next Saturday
        saturday += timedelta(days=1)
    sunday = saturday + timedelta(days=1)
    
    weekend_opens = client.openhouse.get_open_houses(
        filter_query=f"OpenHouseStartTime ge {saturday.isoformat()}Z and OpenHouseStartTime le {sunday.isoformat()}Z",
        orderby="OpenHouseStartTime asc"
    )
    
    # Morning open houses (before noon)
    morning_opens = client.openhouse.get_open_houses(
        filter_query="hour(OpenHouseStartTime) lt 12",
        orderby="OpenHouseStartTime asc"
    )
    ```

=== "Location-Based"
    ```python
    # Open houses in specific city
    slc_opens = client.openhouse.get_open_houses_with_property(
        filter_query="City eq 'Salt Lake City'",
        orderby="OpenHouseStartTime asc"
    )
    
    # Open houses in price range
    luxury_opens = client.openhouse.get_open_houses_with_property(
        filter_query="ListPrice ge 1000000",
        orderby="ListPrice desc"
    )
    ```

=== "Property Type Filters"
    ```python
    # Single family home open houses
    sfh_opens = client.openhouse.get_open_houses_with_property(
        filter_query="PropertySubType eq 'Single Family Residence'",
        orderby="OpenHouseStartTime asc"
    )
    
    # Condo open houses
    condo_opens = client.openhouse.get_open_houses_with_property(
        filter_query="PropertySubType eq 'Condominium'",
        orderby="ListPrice asc"
    )
    ```

## Open House Data Structure

Open Houses in WFRMLS follow the RESO standard with comprehensive event information:

??? info "Key Open House Fields"
    **Event Information**
    
    - `OpenHouseKey` - Unique open house identifier
    - `OpenHouseStartTime` - Start date and time
    - `OpenHouseEndTime` - End date and time
    - `OpenHouseDate` - Date of the open house
    - `OpenHouseStartDateTime` - Combined start date/time
    - `OpenHouseEndDateTime` - Combined end date/time

    **Property Association**
    
    - `ListingId` - Associated property listing ID
    - `ListingKey` - Associated property key
    - `PropertyKey` - Property identifier

    **Agent/Office Information**
    
    - `ListAgentKey` - Listing agent identifier
    - `ListOfficeKey` - Listing office identifier
    - `ShowingAgentKey` - Showing agent (if different)
    - `ShowingOfficeKey` - Showing office (if different)

    **Event Details**
    
    - `OpenHouseType` - Type of open house event
    - `OpenHouseRemarks` - Special instructions or notes
    - `ShowingContactType` - Contact method for showing
    - `ShowingInstructions` - Instructions for attendees

    **System Information**
    
    - `ModificationTimestamp` - Last update time
    - `OriginalEntryTimestamp` - Initial creation time

## Integration Examples

### Weekend Open House Schedule

```python
def get_weekend_open_house_schedule(client):
    """Generate a weekend open house schedule organized by time and location."""
    
    from datetime import datetime, timedelta
    
    # Find next Saturday and Sunday
    today = datetime.now()
    saturday = today.replace(hour=0, minute=0, second=0, microsecond=0)
    while saturday.weekday() != 5:  # Find next Saturday
        saturday += timedelta(days=1)
    sunday = saturday + timedelta(days=1)
    monday = sunday + timedelta(days=1)
    
    # Get weekend open houses with property info
    weekend_opens = client.openhouse.get_open_houses_with_property(
        filter_query=f"OpenHouseStartTime ge {saturday.isoformat()}Z and OpenHouseStartTime lt {monday.isoformat()}Z",
        select="OpenHouseKey,OpenHouseStartTime,OpenHouseEndTime,ListingId,Address,City,ListPrice,BedroomsTotal,BathroomsTotalInteger,PropertySubType",
        orderby="OpenHouseStartTime asc, City asc"
    )
    
    # Organize by day and time
    schedule = {
        'Saturday': [],
        'Sunday': []
    }
    
    for open_house in weekend_opens.get('value', []):
        start_time = datetime.fromisoformat(open_house.get('OpenHouseStartTime', '').replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(open_house.get('OpenHouseEndTime', '').replace('Z', '+00:00'))
        
        day = 'Saturday' if start_time.weekday() == 5 else 'Sunday'
        
        schedule[day].append({
            'time': f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
            'address': open_house.get('Address', 'Unknown Address'),
            'city': open_house.get('City', 'Unknown City'),
            'price': open_house.get('ListPrice', 0),
            'bedrooms': open_house.get('BedroomsTotal', 0),
            'bathrooms': open_house.get('BathroomsTotalInteger', 0),
            'property_type': open_house.get('PropertySubType', 'Unknown'),
            'listing_id': open_house.get('ListingId', '')
        })
    
    return schedule

# Usage
weekend_schedule = get_weekend_open_house_schedule(client)
for day, opens in weekend_schedule.items():
    print(f"\n📅 {day} Open Houses ({len(opens)} events)")
    for open_house in opens:
        print(f"⏰ {open_house['time']}")
        print(f"   🏠 {open_house['address']}, {open_house['city']}")
        print(f"   💰 ${open_house['price']:,} | 🛏️ {open_house['bedrooms']} bed | 🛁 {open_house['bathrooms']} bath")
        print(f"   📋 {open_house['property_type']} | ID: {open_house['listing_id']}")
```

### Agent Open House Management

```python
def get_agent_open_house_dashboard(client, agent_key):
    """Create an open house management dashboard for an agent."""
    
    from datetime import datetime, timedelta
    
    # Get agent's upcoming open houses
    upcoming_opens = client.openhouse.get_open_houses_by_agent(
        agent_key,
        filter_query=f"OpenHouseStartTime ge {datetime.utcnow().isoformat()}Z",
        orderby="OpenHouseStartTime asc"
    )
    
    # Get agent's past open houses (last 30 days)
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    past_opens = client.openhouse.get_open_houses_by_agent(
        agent_key,
        filter_query=f"OpenHouseStartTime ge {thirty_days_ago} and OpenHouseStartTime lt {datetime.utcnow().isoformat()}Z",
        orderby="OpenHouseStartTime desc"
    )
    
    # Get agent details
    try:
        agent_detail = client.member.get_member(agent_key)
        agent_name = f"{agent_detail.get('MemberFirstName', '')} {agent_detail.get('MemberLastName', '')}".strip()
    except:
        agent_name = f"Agent {agent_key}"
    
    dashboard = {
        'agent_name': agent_name,
        'upcoming_count': len(upcoming_opens.get('value', [])),
        'past_count': len(past_opens.get('value', [])),
        'upcoming_events': [],
        'past_events': []
    }
    
    # Process upcoming events
    for event in upcoming_opens.get('value', []):
        start_time = datetime.fromisoformat(event.get('OpenHouseStartTime', '').replace('Z', '+00:00'))
        dashboard['upcoming_events'].append({
            'date': start_time.strftime('%A, %B %d'),
            'time': start_time.strftime('%I:%M %p'),
            'listing_id': event.get('ListingId', ''),
            'days_from_now': (start_time.date() - datetime.now().date()).days
        })
    
    # Process past events
    for event in past_opens.get('value', []):
        start_time = datetime.fromisoformat(event.get('OpenHouseStartTime', '').replace('Z', '+00:00'))
        dashboard['past_events'].append({
            'date': start_time.strftime('%B %d'),
            'listing_id': event.get('ListingId', ''),
            'days_ago': (datetime.now().date() - start_time.date()).days
        })
    
    return dashboard

# Usage
agent_dashboard = get_agent_open_house_dashboard(client, "96422")
print(f"🏠 Open House Dashboard for {agent_dashboard['agent_name']}")
print(f"   📅 Upcoming: {agent_dashboard['upcoming_count']} events")
print(f"   📈 Past 30 days: {agent_dashboard['past_count']} events")

print(f"\n🔮 Upcoming Open Houses:")
for event in agent_dashboard['upcoming_events'][:5]:
    urgency = "🚨" if event['days_from_now'] <= 1 else "⏰"
    print(f"   {urgency} {event['date']} at {event['time']} - Property {event['listing_id']}")
```

### Open House Performance Analytics

```python
def analyze_open_house_patterns(client, days_back=90):
    """Analyze open house patterns and performance."""
    
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + "Z"
    
    # Get recent open houses with property info
    recent_opens = client.openhouse.get_open_houses_with_property(
        filter_query=f"OpenHouseStartTime ge {cutoff_date}",
        select="OpenHouseKey,OpenHouseStartTime,ListingId,City,ListPrice,PropertySubType,ListAgentKey",
        top=1000
    )
    
    analysis = {
        'total_events': 0,
        'by_day_of_week': defaultdict(int),
        'by_hour': defaultdict(int),
        'by_city': defaultdict(int),
        'by_price_range': defaultdict(int),
        'by_property_type': defaultdict(int),
        'top_agents': defaultdict(int)
    }
    
    price_ranges = [
        (0, 300000, "Under $300K"),
        (300000, 500000, "$300K-$500K"),
        (500000, 750000, "$500K-$750K"),
        (750000, 1000000, "$750K-$1M"),
        (1000000, 2000000, "$1M-$2M"),
        (2000000, float('inf'), "Over $2M")
    ]
    
    for event in recent_opens.get('value', []):
        analysis['total_events'] += 1
        
        # Parse start time
        start_time = datetime.fromisoformat(event.get('OpenHouseStartTime', '').replace('Z', '+00:00'))
        
        # Day of week analysis
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = day_names[start_time.weekday()]
        analysis['by_day_of_week'][day_name] += 1
        
        # Hour analysis
        hour = start_time.hour
        time_period = f"{hour:02d}:00"
        analysis['by_hour'][time_period] += 1
        
        # City analysis
        city = event.get('City', 'Unknown')
        analysis['by_city'][city] += 1
        
        # Price range analysis
        list_price = event.get('ListPrice', 0)
        for min_price, max_price, range_label in price_ranges:
            if min_price <= list_price < max_price:
                analysis['by_price_range'][range_label] += 1
                break
        
        # Property type analysis
        prop_type = event.get('PropertySubType', 'Unknown')
        analysis['by_property_type'][prop_type] += 1
        
        # Agent analysis
        agent_key = event.get('ListAgentKey')
        if agent_key:
            analysis['top_agents'][agent_key] += 1
    
    # Sort results
    analysis['by_day_of_week'] = dict(sorted(analysis['by_day_of_week'].items(), key=lambda x: x[1], reverse=True))
    analysis['by_hour'] = dict(sorted(analysis['by_hour'].items()))
    analysis['by_city'] = dict(sorted(analysis['by_city'].items(), key=lambda x: x[1], reverse=True)[:10])
    analysis['by_price_range'] = dict(sorted(analysis['by_price_range'].items(), key=lambda x: x[1], reverse=True))
    analysis['by_property_type'] = dict(sorted(analysis['by_property_type'].items(), key=lambda x: x[1], reverse=True))
    analysis['top_agents'] = dict(sorted(analysis['top_agents'].items(), key=lambda x: x[1], reverse=True)[:10])
    
    return analysis

# Usage
oh_analysis = analyze_open_house_patterns(client, days_back=90)
print(f"📊 Open House Analysis (Last 90 Days) - {oh_analysis['total_events']} events")

print(f"\n📅 Popular Days:")
for day, count in oh_analysis['by_day_of_week'].items():
    percentage = (count / oh_analysis['total_events']) * 100
    print(f"   {day}: {count} events ({percentage:.1f}%)")

print(f"\n⏰ Popular Times:")
for hour, count in list(oh_analysis['by_hour'].items())[:10]:
    print(f"   {hour}: {count} events")

print(f"\n🏙️ Top Cities:")
for city, count in oh_analysis['by_city'].items():
    print(f"   {city}: {count} events")
```

### Open House Reminder System

```python
def get_open_house_reminders(client, agent_key=None, days_ahead=3):
    """Get open house reminders for upcoming events."""
    
    from datetime import datetime, timedelta
    
    end_date = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
    
    # Build filter
    filter_parts = [f"OpenHouseStartTime ge {datetime.utcnow().isoformat()}Z"]
    filter_parts.append(f"OpenHouseStartTime le {end_date}")
    
    if agent_key:
        filter_parts.append(f"ListAgentKey eq '{agent_key}'")
    
    filter_query = " and ".join(filter_parts)
    
    # Get upcoming open houses with property details
    upcoming_opens = client.openhouse.get_open_houses_with_property(
        filter_query=filter_query,
        select="OpenHouseKey,OpenHouseStartTime,OpenHouseEndTime,ListingId,Address,City,ListAgentKey,PropertySubType",
        orderby="OpenHouseStartTime asc"
    )
    
    reminders = []
    for event in upcoming_opens.get('value', []):
        start_time = datetime.fromisoformat(event.get('OpenHouseStartTime', '').replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(event.get('OpenHouseEndTime', '').replace('Z', '+00:00'))
        
        hours_until = (start_time - datetime.now()).total_seconds() / 3600
        
        # Determine urgency
        if hours_until <= 2:
            urgency = "🚨 IMMEDIATE"
        elif hours_until <= 24:
            urgency = "⚠️ TODAY"
        elif hours_until <= 48:
            urgency = "📅 TOMORROW"
        else:
            urgency = "🔔 UPCOMING"
        
        reminders.append({
            'urgency': urgency,
            'hours_until': hours_until,
            'start_time': start_time.strftime('%A, %B %d at %I:%M %p'),
            'duration': f"{(end_time - start_time).seconds // 3600}h {((end_time - start_time).seconds % 3600) // 60}m",
            'address': event.get('Address', 'Unknown Address'),
            'city': event.get('City', 'Unknown City'),
            'listing_id': event.get('ListingId', ''),
            'property_type': event.get('PropertySubType', 'Unknown'),
            'agent_key': event.get('ListAgentKey', '')
        })
    
    return sorted(reminders, key=lambda x: x['hours_until'])

# Usage
reminders = get_open_house_reminders(client, days_ahead=3)
print(f"🔔 Open House Reminders ({len(reminders)} upcoming events)")

for reminder in reminders:
    print(f"\n{reminder['urgency']}")
    print(f"   📅 {reminder['start_time']} ({reminder['duration']})")
    print(f"   🏠 {reminder['address']}, {reminder['city']}")
    print(f"   📋 {reminder['property_type']} | ID: {reminder['listing_id']}")
    print(f"   ⏱️ In {reminder['hours_until']:.1f} hours")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    # Try to get open houses for a property
    open_houses = client.openhouse.get_open_houses_for_property("1611952")
    
except NotFoundError:
    print("❌ Property not found or has no open houses scheduled")
    
except ValidationError as e:
    print(f"📝 Invalid search parameters: {e}")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Performance Tips

!!! tip "Optimization Strategies"
    **Efficient Queries**
    
    - Use date range filters to limit results to relevant time periods
    - Filter by agent or property to get targeted results
    - Use `select` to limit fields when you don't need full event details
    
    **Common Patterns**
    
    ```python
    # Get essential open house info only
    basic_opens = client.openhouse.get_open_houses(
        filter_query="OpenHouseStartTime ge now()",
        select="OpenHouseKey,OpenHouseStartTime,ListingId,ListAgentKey",
        orderby="OpenHouseStartTime asc"
    )
    
    # Search efficiently by time range
    weekend_opens = client.openhouse.get_open_houses(
        filter_query="OpenHouseStartTime ge '2024-01-20T00:00:00Z' and OpenHouseStartTime le '2024-01-21T23:59:59Z'",
        orderby="OpenHouseStartTime asc"
    )
    ```
    
    **Caching Considerations**
    
    - Open house schedules change frequently
    - Cache upcoming events for short periods (1-4 hours)
    - Refresh data more frequently as event time approaches 