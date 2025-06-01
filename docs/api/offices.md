# Office API Reference

The Office module provides access to real estate brokerage and office information in the WFRMLS system. This includes office details, contact information, licensing, and associated member data.

---

## Overview

The `OfficeService` class handles all office-related operations through the WFRMLS API. Offices represent real estate brokerages, branch offices, and other business entities in the MLS system.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
office_service = client.office
```

---

## Methods

### get_offices()

Retrieve a list of offices with optional filtering, sorting, and pagination.

```python
offices = client.office.get_offices(
    top=50,
    filter_query="OfficeStatus eq 'Active'",
    orderby="OfficeName asc"
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

`List[Dict[str, Any]]`: List of office records matching the query criteria.

#### Example

```python
# Get active offices with specific fields
active_offices = client.office.get_offices(
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail"],
    filter_query="OfficeStatus eq 'Active'",
    orderby="OfficeName asc",
    top=100
)

# Get offices in a specific city
city_offices = client.office.get_offices(
    filter_query="OfficeCity eq 'Salt Lake City'",
    orderby="OfficeName asc"
)

# Search offices by name
search_offices = client.office.get_offices(
    filter_query="contains(OfficeName, 'Realty')",
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeAddress"]
)
```

---

### get_office()

Retrieve a specific office by its unique identifier.

```python
office = client.office.get_office("OFFICE123")
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `office_key` | `str` | Yes | - | The unique identifier for the office. |
| `select` | `Optional[List[str]]` | No | `None` | Specific fields to return. If not provided, returns all available fields. |

#### Returns

`Dict[str, Any]`: Complete office record for the specified office.

#### Raises

- `NotFoundError`: If the office with the specified key is not found.
- `WFRMLSError`: For other API-related errors.

#### Example

```python
# Get complete office record
office = client.office.get_office("OFFICE123")

# Get specific fields only
office_contact = client.office.get_office(
    "OFFICE123",
    select=["OfficeName", "OfficePhone", "OfficeEmail", "OfficeAddress"]
)
```

---

## Common Use Cases

### Active Office Directory

```python
# Get all active offices with contact information
active_offices = client.office.get_offices(
    filter_query="OfficeStatus eq 'Active'",
    select=[
        "OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail",
        "OfficeAddress", "OfficeCity", "OfficeStateOrProvince", "OfficePostalCode"
    ],
    orderby="OfficeName asc"
)

for office in active_offices:
    print(f"{office['OfficeName']} - {office['OfficePhone']}")
    print(f"  {office['OfficeAddress']}, {office['OfficeCity']}, {office['OfficeStateOrProvince']}")
```

### Office Location Search

```python
# Find offices in a specific geographic area
utah_offices = client.office.get_offices(
    filter_query="OfficeStateOrProvince eq 'UT' and OfficeStatus eq 'Active'",
    select=[
        "OfficeKey", "OfficeName", "OfficeCity", 
        "OfficeAddress", "OfficePhone", "OfficeEmail"
    ],
    orderby="OfficeCity asc, OfficeName asc"
)

# Group by city
from collections import defaultdict
offices_by_city = defaultdict(list)

for office in utah_offices:
    offices_by_city[office['OfficeCity']].append(office)

for city, offices in offices_by_city.items():
    print(f"\n{city}:")
    for office in offices:
        print(f"  - {office['OfficeName']}")
```

### Office Verification

```python
# Verify office licensing and status
try:
    office = client.office.get_office(
        "OFFICE456",
        select=[
            "OfficeName", "OfficeStatus", "OfficeLicenseNumber",
            "OfficeNationalAssociationId", "OfficePhone", "OfficeEmail"
        ]
    )
    
    print(f"Office: {office['OfficeName']}")
    print(f"Status: {office['OfficeStatus']}")
    print(f"License: {office.get('OfficeLicenseNumber', 'Not provided')}")
    print(f"Contact: {office['OfficePhone']} / {office['OfficeEmail']}")
    
except NotFoundError:
    print("Office not found")
```

---

## Key Fields

### Identification Fields

| Field | Type | Description |
|-------|------|-------------|
| `OfficeKey` | `str` | Unique identifier for the office |
| `OfficeMlsId` | `str` | MLS-specific office identifier |
| `OfficeNationalAssociationId` | `str` | National association identifier |
| `OfficeLicenseNumber` | `str` | Business license number |

### Basic Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficeName` | `str` | Official name of the office/brokerage |
| `OfficeStatus` | `str` | Current status (Active, Inactive, etc.) |
| `OfficeType` | `str` | Type of office (Main, Branch, etc.) |
| `OfficeCorporateLicense` | `str` | Corporate license identifier |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficePhone` | `str` | Primary phone number |
| `OfficeFax` | `str` | Fax number |
| `OfficeEmail` | `str` | Primary email address |
| `OfficeWebsiteURL` | `str` | Office website URL |
| `OfficeAddress` | `str` | Street address |
| `OfficeCity` | `str` | City |
| `OfficeStateOrProvince` | `str` | State or province |
| `OfficePostalCode` | `str` | ZIP/postal code |
| `OfficeCountry` | `str` | Country |

### Management Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficeManager` | `str` | Name of office manager |
| `OfficeManagerKey` | `str` | Member key of office manager |
| `OfficeManagerEmail` | `str` | Office manager email |
| `OfficeManagerPhone` | `str` | Office manager phone |

### Association Information

| Field | Type | Description |
|-------|------|-------------|
| `OfficeAssociationComments` | `str` | Association-related comments |
| `OfficeAOR` | `str` | Area of Responsibility |
| `OfficeAORkey` | `str` | AOR identifier key |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `ModificationTimestamp` | `datetime` | Last modification date/time |
| `OriginalEntryTimestamp` | `datetime` | Original creation date/time |
| `OfficeLoginId` | `str` | System login identifier |

---

## Advanced Queries

### Geographic Filtering

```python
# Find offices within a specific postal code range
offices_in_area = client.office.get_offices(
    filter_query="OfficePostalCode ge '84000' and OfficePostalCode le '84999'",
    select=["OfficeKey", "OfficeName", "OfficeCity", "OfficePostalCode"],
    orderby="OfficePostalCode asc"
)

# Find offices in multiple cities
multi_city_offices = client.office.get_offices(
    filter_query="OfficeCity in ('Salt Lake City', 'Provo', 'Ogden')",
    orderby="OfficeCity asc, OfficeName asc"
)
```

### Status and Type Filtering

```python
# Get main offices only
main_offices = client.office.get_offices(
    filter_query="OfficeType eq 'Main' and OfficeStatus eq 'Active'",
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail"]
)

# Find recently modified offices
recent_updates = client.office.get_offices(
    filter_query="ModificationTimestamp ge 2024-01-01T00:00:00Z",
    orderby="ModificationTimestamp desc",
    top=50
)
```

### Contact Information Queries

```python
# Find offices with websites
offices_with_websites = client.office.get_offices(
    filter_query="OfficeWebsiteURL ne null and OfficeStatus eq 'Active'",
    select=["OfficeKey", "OfficeName", "OfficeWebsiteURL", "OfficeEmail"]
)

# Find offices with specific manager
managed_offices = client.office.get_offices(
    filter_query="OfficeManagerKey eq 'MANAGER123'",
    select=["OfficeKey", "OfficeName", "OfficeManager", "OfficePhone"]
)
```

---

## Error Handling

```python
from wfrmls.exceptions import WFRMLSError, NotFoundError, ValidationError

try:
    # Attempt to get office
    office = client.office.get_office("INVALID_KEY")
    
except NotFoundError:
    print("Office not found")
    
except ValidationError as e:
    print(f"Invalid request: {e}")
    
except WFRMLSError as e:
    print(f"API error: {e}")
```

---

## Best Practices

### Efficient Data Retrieval

```python
# Use select to limit returned fields for better performance
offices = client.office.get_offices(
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeEmail"],
    filter_query="OfficeStatus eq 'Active'",
    top=100
)

# Use specific filters to reduce data transfer
local_offices = client.office.get_offices(
    filter_query="OfficeCity eq 'Salt Lake City' and OfficeStatus eq 'Active'",
    orderby="OfficeName asc"
)
```

### Pagination for Large Datasets

```python
def get_all_active_offices():
    """Get all active offices using pagination."""
    all_offices = []
    skip = 0
    batch_size = 100
    
    while True:
        batch = client.office.get_offices(
            filter_query="OfficeStatus eq 'Active'",
            top=batch_size,
            skip=skip,
            count=True
        )
        
        if not batch:
            break
            
        all_offices.extend(batch)
        skip += batch_size
        
        # Check if we've retrieved all records
        if len(batch) < batch_size:
            break
    
    return all_offices
```

### Office Directory Builder

```python
def build_office_directory():
    """Build a comprehensive office directory."""
    offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select=[
            "OfficeKey", "OfficeName", "OfficeType", "OfficePhone", 
            "OfficeEmail", "OfficeWebsiteURL", "OfficeAddress", 
            "OfficeCity", "OfficeStateOrProvince", "OfficePostalCode"
        ],
        orderby="OfficeCity asc, OfficeName asc"
    )
    
    directory = {}
    for office in offices:
        city = office['OfficeCity']
        if city not in directory:
            directory[city] = []
        
        directory[city].append({
            'name': office['OfficeName'],
            'type': office.get('OfficeType', 'Unknown'),
            'phone': office.get('OfficePhone', ''),
            'email': office.get('OfficeEmail', ''),
            'website': office.get('OfficeWebsiteURL', ''),
            'address': f"{office.get('OfficeAddress', '')}, {office['OfficeCity']}, {office['OfficeStateOrProvince']} {office.get('OfficePostalCode', '')}"
        })
    
    return directory
```

### Office Validation

```python
def validate_office_data(office_key):
    """Validate office data completeness."""
    try:
        office = client.office.get_office(office_key)
        
        required_fields = ['OfficeName', 'OfficePhone', 'OfficeEmail', 'OfficeAddress']
        missing_fields = []
        
        for field in required_fields:
            if not office.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Office {office_key} missing: {', '.join(missing_fields)}")
            return False
        
        print(f"Office {office_key} data is complete")
        return True
        
    except NotFoundError:
        print(f"Office {office_key} not found")
        return False
```

---

## Integration Examples

### Office-Member Relationship

```python
def get_office_with_members(office_key):
    """Get office details along with associated members."""
    try:
        # Get office information
        office = client.office.get_office(office_key)
        
        # Get members associated with this office
        members = client.member.get_members(
            filter_query=f"OfficeKey eq '{office_key}' and MemberStatus eq 'Active'",
            select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail"],
            orderby="MemberLastName asc"
        )
        
        return {
            'office': office,
            'members': members,
            'member_count': len(members)
        }
        
    except NotFoundError:
        return None
```

### Office Performance Metrics

```python
def get_office_metrics(office_key):
    """Get performance metrics for an office."""
    try:
        office = client.office.get_office(office_key)
        
        # Get active listings for this office's agents
        office_members = client.member.get_members(
            filter_query=f"OfficeKey eq '{office_key}'",
            select=["MemberKey"]
        )
        
        member_keys = [m['MemberKey'] for m in office_members]
        
        if member_keys:
            # Get active properties listed by office members
            member_filter = " or ".join([f"ListAgentKey eq '{key}'" for key in member_keys[:10]])  # Limit for query length
            
            active_listings = client.property.get_properties(
                filter_query=f"StandardStatus eq 'Active' and ({member_filter})",
                select=["PropertyKey", "ListPrice", "ListAgentKey"],
                count=True
            )
            
            return {
                'office_name': office['OfficeName'],
                'active_agents': len(member_keys),
                'active_listings': len(active_listings),
                'total_listing_value': sum(float(p.get('ListPrice', 0)) for p in active_listings)
            }
    
    except Exception as e:
        print(f"Error getting office metrics: {e}")
        return None
```

---

## Related Resources

- **[Member API](members.md)** - For agent information associated with offices
- **[Property API](properties.md)** - For properties listed by office members
- **[OData Queries Guide](../guides/odata-queries.md)** - Advanced filtering and querying
- **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling strategies