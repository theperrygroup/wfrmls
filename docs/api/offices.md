# Offices API

The Offices API provides access to real estate brokerage and office information within the WFRMLS system. This includes office details, contact information, location data, and associated member listings.

## Overview

The `OfficeClient` class handles all office-related operations, providing methods to search, retrieve, and filter real estate office data.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
offices = client.office.get_offices(top=10)
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_offices()` | Retrieve multiple offices with filtering | `List[Dict[str, Any]]` |
| `get_office()` | Get a specific office by ID | `Dict[str, Any]` |
| `search_offices()` | Search offices by criteria | `List[Dict[str, Any]]` |
| `get_office_members()` | Get members associated with an office | `List[Dict[str, Any]]` |

## Methods

### get_offices()

Retrieve multiple offices with optional filtering, sorting, and pagination.

```python
def get_offices(
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
    # Get first 10 active offices
    offices = client.office.get_offices(
        top=10,
        filter_query="OfficeStatus eq 'Active'"
    )
    
    for office in offices:
        print(f"{office['OfficeName']} - {office['OfficeCity']}")
    ```

=== "Specific Fields"

    ```python
    # Get only specific fields
    offices = client.office.get_offices(
        select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail"],
        filter_query="OfficeStatus eq 'Active'",
        orderby="OfficeName"
    )
    ```

=== "Geographic Filtering"

    ```python
    # Find offices in specific cities
    offices = client.office.get_offices(
        filter_query="OfficeCity eq 'Salt Lake City' or OfficeCity eq 'Provo'",
        orderby="OfficeName asc"
    )
    ```

### get_office()

Retrieve a specific office by its unique identifier.

```python
def get_office(
    self,
    office_key: str,
    select: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `office_key` | `str` | Yes | Unique office identifier |
| `select` | `List[str]` | No | Specific fields to return |

#### Example

```python
# Get specific office details
office = client.office.get_office(
    office_key="12345",
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail", "OfficeAddress1"]
)

print(f"Office: {office['OfficeName']}")
print(f"Phone: {office['OfficePhone']}")
print(f"Address: {office['OfficeAddress1']}")
```

### search_offices()

Search for offices using various criteria with fuzzy matching capabilities.

```python
def search_offices(
    self,
    name: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    status: Optional[OfficeStatus] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | No | Office name (partial match) |
| `city` | `str` | No | City name |
| `state` | `str` | No | State abbreviation |
| `zip_code` | `str` | No | ZIP code |
| `status` | `OfficeStatus` | No | Office status |

#### Example

```python
from wfrmls import OfficeStatus

# Search by name
offices = client.office.search_offices(
    name="Realty",
    status=OfficeStatus.ACTIVE
)

# Search by location
local_offices = client.office.search_offices(
    city="Salt Lake City",
    state="UT"
)
```

### get_office_members()

Retrieve all members associated with a specific office.

```python
def get_office_members(
    self,
    office_key: str,
    select: Optional[List[str]] = None,
    filter_query: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `office_key` | `str` | Yes | Office identifier |
| `select` | `List[str]` | No | Specific member fields to return |
| `filter_query` | `str` | No | Additional member filtering |

#### Example

```python
# Get all active agents in an office
agents = client.office.get_office_members(
    office_key="12345",
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail"],
    filter_query="MemberStatus eq 'Active' and MemberType eq 'Agent'"
)

print(f"Found {len(agents)} active agents")
for agent in agents:
    print(f"  {agent['MemberFirstName']} {agent['MemberLastName']}")
```

## Enums and Constants

### OfficeStatus

Enumeration of possible office statuses:

```python
from wfrmls import OfficeStatus

class OfficeStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    PENDING = "Pending"
```

### OfficeType

Enumeration of office types:

```python
from wfrmls import OfficeType

class OfficeType(str, Enum):
    MAIN = "Main"
    BRANCH = "Branch"
    FRANCHISE = "Franchise"
    INDEPENDENT = "Independent"
```

## Common Use Cases

### Office Directory

```python
# Build an office directory
active_offices = client.office.get_offices(
    filter_query="OfficeStatus eq 'Active'",
    select=[
        "OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail",
        "OfficeAddress1", "OfficeCity", "OfficeStateOrProvince", "OfficePostalCode"
    ],
    orderby="OfficeName asc"
)

for office in active_offices:
    print(f"{office['OfficeName']}")
    print(f"  {office['OfficeAddress1']}")
    print(f"  {office['OfficeCity']}, {office['OfficeStateOrProvince']} {office['OfficePostalCode']}")
    print(f"  Phone: {office['OfficePhone']}")
    print(f"  Email: {office['OfficeEmail']}")
    print()
```

### Market Coverage Analysis

```python
# Analyze office coverage by city
def analyze_market_coverage():
    offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select=["OfficeKey", "OfficeName", "OfficeCity", "OfficeStateOrProvince"]
    )
    
    # Group by city
    city_coverage = {}
    for office in offices:
        city = office['OfficeCity']
        if city not in city_coverage:
            city_coverage[city] = []
        city_coverage[city].append(office['OfficeName'])
    
    # Display results
    for city, office_names in sorted(city_coverage.items()):
        print(f"{city}: {len(office_names)} offices")
        for name in office_names:
            print(f"  - {name}")

analyze_market_coverage()
```

### Office Team Management

```python
# Get complete office information including team
def get_office_profile(office_key: str):
    # Get office details
    office = client.office.get_office(office_key)
    
    # Get office team
    team = client.office.get_office_members(
        office_key,
        select=[
            "MemberKey", "MemberFirstName", "MemberLastName",
            "MemberType", "MemberEmail", "MemberMobilePhone"
        ],
        filter_query="MemberStatus eq 'Active'"
    )
    
    return {
        "office": office,
        "team": team,
        "team_count": len(team)
    }

profile = get_office_profile("12345")
print(f"Office: {profile['office']['OfficeName']}")
print(f"Team Size: {profile['team_count']} members")
```

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `OfficeKey` | `str` | Unique office identifier |
| `OfficeName` | `str` | Office name |
| `OfficeStatus` | `str` | Current status (Active, Inactive, etc.) |
| `OfficeType` | `str` | Office type (Main, Branch, etc.) |
| `OfficeMlsId` | `str` | MLS-specific office ID |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficePhone` | `str` | Main phone number |
| `OfficeFax` | `str` | Fax number |
| `OfficeEmail` | `str` | Primary email address |
| `OfficeWebsiteURL` | `str` | Website URL |

### Address Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficeAddress1` | `str` | Primary address line 1 |
| `OfficeAddress2` | `str` | Primary address line 2 |
| `OfficeCity` | `str` | City |
| `OfficeStateOrProvince` | `str` | State or province |
| `OfficePostalCode` | `str` | ZIP/postal code |
| `OfficeCountry` | `str` | Country |

### Geographic Data

| Field | Type | Description |
|-------|------|-------------|
| `OfficeLatitude` | `float` | Latitude coordinate |
| `OfficeLongitude` | `float` | Longitude coordinate |
| `OfficeCounty` | `str` | County name |

### Business Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficeBrokerKey` | `str` | Primary broker identifier |
| `OfficeBrokerMlsId` | `str` | Broker MLS ID |
| `OfficeNationalAssociationId` | `str` | NAR office ID |
| `OfficeCorporateLicense` | `str` | Corporate license number |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `OriginalEntryTimestamp` | `datetime` | When record was created |
| `ModificationTimestamp` | `datetime` | Last modification time |

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    office = client.office.get_office("invalid_key")
except NotFoundError:
    print("Office not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Use select parameter** to limit returned fields
2. **Cache office data** as it changes infrequently
3. **Use geographic filtering** for location-based queries
4. **Implement pagination** for large result sets

### Data Management

1. **Track ModificationTimestamp** for incremental updates
2. **Validate contact information** before use
3. **Handle inactive offices** appropriately
4. **Maintain office-member relationships**

### Geographic Queries

1. **Use city/state filters** for regional searches
2. **Leverage latitude/longitude** for proximity searches
3. **Consider county boundaries** for market analysis
4. **Validate ZIP codes** for accuracy

## Integration Examples

### CRM Synchronization

```python
# Sync office data with CRM
def sync_offices_to_crm():
    offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select=[
            "OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail",
            "OfficeAddress1", "OfficeCity", "OfficeStateOrProvince",
            "ModificationTimestamp"
        ]
    )
    
    for office in offices:
        # Update CRM system
        update_crm_office(office)
        
        # Get office team
        team = client.office.get_office_members(
            office['OfficeKey'],
            filter_query="MemberStatus eq 'Active'"
        )
        
        # Update team associations
        update_crm_office_team(office['OfficeKey'], team)
```

### Market Analysis

```python
# Generate market coverage report
def generate_market_report():
    offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select=["OfficeKey", "OfficeName", "OfficeCity", "OfficeCounty"]
    )
    
    # Analyze by county
    county_stats = {}
    for office in offices:
        county = office.get('OfficeCounty', 'Unknown')
        if county not in county_stats:
            county_stats[county] = 0
        county_stats[county] += 1
    
    # Generate report
    print("Market Coverage by County:")
    for county, count in sorted(county_stats.items()):
        print(f"  {county}: {count} offices")
```

## Related Resources

- [Members API](members.md) - For office team information
- [Properties API](properties.md) - For office listings
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management