# Member API Reference

The Member module provides access to real estate agent and member information in the WFRMLS system. This includes agent profiles, contact information, licensing details, and professional associations.

---

## Overview

The `MemberService` class handles all member-related operations through the WFRMLS API. Members represent real estate agents, brokers, and other licensed professionals in the MLS system.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
member_service = client.member
```

---

## Methods

### get_members()

Retrieve a list of members with optional filtering, sorting, and pagination.

```python
members = client.member.get_members(
    top=50,
    filter_query="MemberStatus eq 'Active'",
    orderby="MemberLastName asc"
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

`List[Dict[str, Any]]`: List of member records matching the query criteria.

#### Example

```python
# Get active members with specific fields
active_members = client.member.get_members(
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail"],
    filter_query="MemberStatus eq 'Active'",
    orderby="MemberLastName asc",
    top=100
)

# Get members by office
office_members = client.member.get_members(
    filter_query="OfficeKey eq '12345'",
    orderby="MemberFirstName asc"
)

# Search members by name
search_members = client.member.get_members(
    filter_query="contains(MemberLastName, 'Smith')",
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberPhone"]
)
```

---

### get_member()

Retrieve a specific member by their unique identifier.

```python
member = client.member.get_member("MEMBER123")
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `member_key` | `str` | Yes | - | The unique identifier for the member. |
| `select` | `Optional[List[str]]` | No | `None` | Specific fields to return. If not provided, returns all available fields. |

#### Returns

`Dict[str, Any]`: Complete member record for the specified member.

#### Raises

- `NotFoundError`: If the member with the specified key is not found.
- `WFRMLSError`: For other API-related errors.

#### Example

```python
# Get complete member record
member = client.member.get_member("MEMBER123")

# Get specific fields only
member_contact = client.member.get_member(
    "MEMBER123",
    select=["MemberFirstName", "MemberLastName", "MemberEmail", "MemberPhone"]
)
```

---

## Common Use Cases

### Active Agent Search

```python
# Find all active agents in a specific office
active_agents = client.member.get_members(
    filter_query="MemberStatus eq 'Active' and OfficeKey eq 'OFFICE123'",
    select=[
        "MemberKey", "MemberFirstName", "MemberLastName", 
        "MemberEmail", "MemberPhone", "MemberLicenseNumber"
    ],
    orderby="MemberLastName asc"
)

for agent in active_agents:
    print(f"{agent['MemberFirstName']} {agent['MemberLastName']} - {agent['MemberEmail']}")
```

### Agent Contact Information

```python
# Get contact details for a specific agent
try:
    agent = client.member.get_member(
        "AGENT456",
        select=[
            "MemberFirstName", "MemberLastName", "MemberEmail", 
            "MemberPhone", "MemberMobilePhone", "MemberAddress",
            "MemberCity", "MemberStateOrProvince", "MemberPostalCode"
        ]
    )
    
    print(f"Agent: {agent['MemberFirstName']} {agent['MemberLastName']}")
    print(f"Email: {agent['MemberEmail']}")
    print(f"Phone: {agent['MemberPhone']}")
    
except NotFoundError:
    print("Agent not found")
```

### License Verification

```python
# Verify agent licensing information
licensed_agents = client.member.get_members(
    filter_query="MemberLicenseNumber ne null and MemberStatus eq 'Active'",
    select=[
        "MemberKey", "MemberFirstName", "MemberLastName",
        "MemberLicenseNumber", "MemberLicenseState"
    ]
)

for agent in licensed_agents:
    print(f"{agent['MemberFirstName']} {agent['MemberLastName']} - License: {agent['MemberLicenseNumber']}")
```

---

## Key Fields

### Identification Fields

| Field | Type | Description |
|-------|------|-------------|
| `MemberKey` | `str` | Unique identifier for the member |
| `MemberMlsId` | `str` | MLS-specific member identifier |
| `MemberNationalAssociationId` | `str` | National association identifier |

### Personal Information

| Field | Type | Description |
|-------|------|-------------|
| `MemberFirstName` | `str` | Member's first name |
| `MemberLastName` | `str` | Member's last name |
| `MemberMiddleName` | `str` | Member's middle name |
| `MemberNickname` | `str` | Member's preferred nickname |
| `MemberFullName` | `str` | Complete formatted name |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `MemberEmail` | `str` | Primary email address |
| `MemberPhone` | `str` | Primary phone number |
| `MemberMobilePhone` | `str` | Mobile phone number |
| `MemberFax` | `str` | Fax number |
| `MemberAddress` | `str` | Street address |
| `MemberCity` | `str` | City |
| `MemberStateOrProvince` | `str` | State or province |
| `MemberPostalCode` | `str` | ZIP/postal code |

### Professional Information

| Field | Type | Description |
|-------|------|-------------|
| `MemberStatus` | `str` | Current membership status (Active, Inactive, etc.) |
| `MemberType` | `str` | Type of membership (Agent, Broker, etc.) |
| `MemberLicenseNumber` | `str` | Real estate license number |
| `MemberLicenseState` | `str` | State where license is held |
| `OfficeKey` | `str` | Associated office identifier |
| `OfficeName` | `str` | Name of associated office |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `ModificationTimestamp` | `datetime` | Last modification date/time |
| `MemberLoginId` | `str` | System login identifier |
| `MemberPasswordModificationTimestamp` | `datetime` | Last password change |

---

## Error Handling

```python
from wfrmls.exceptions import WFRMLSError, NotFoundError, ValidationError

try:
    # Attempt to get member
    member = client.member.get_member("INVALID_KEY")
    
except NotFoundError:
    print("Member not found")
    
except ValidationError as e:
    print(f"Invalid request: {e}")
    
except WFRMLSError as e:
    print(f"API error: {e}")
```

---

## Best Practices

### Efficient Queries

```python
# Use select to limit returned fields
members = client.member.get_members(
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail"],
    filter_query="MemberStatus eq 'Active'",
    top=100
)

# Use specific filters to reduce data transfer
recent_members = client.member.get_members(
    filter_query="ModificationTimestamp ge 2024-01-01T00:00:00Z",
    orderby="ModificationTimestamp desc"
)
```

### Pagination for Large Datasets

```python
def get_all_active_members():
    """Get all active members using pagination."""
    all_members = []
    skip = 0
    batch_size = 100
    
    while True:
        batch = client.member.get_members(
            filter_query="MemberStatus eq 'Active'",
            top=batch_size,
            skip=skip,
            count=True
        )
        
        if not batch:
            break
            
        all_members.extend(batch)
        skip += batch_size
        
        # Check if we've retrieved all records
        if len(batch) < batch_size:
            break
    
    return all_members
```

### Caching Member Data

```python
from functools import lru_cache
from datetime import datetime, timedelta

class MemberCache:
    def __init__(self, client):
        self.client = client
        self._cache = {}
        self._cache_timeout = timedelta(hours=1)
    
    def get_member(self, member_key):
        """Get member with caching."""
        now = datetime.now()
        
        if member_key in self._cache:
            cached_data, timestamp = self._cache[member_key]
            if now - timestamp < self._cache_timeout:
                return cached_data
        
        # Fetch fresh data
        member = self.client.member.get_member(member_key)
        self._cache[member_key] = (member, now)
        
        return member
```

---

## Related Resources

- **[Office API](offices.md)** - For office information associated with members
- **[Property API](properties.md)** - For properties listed by members
- **[OData Queries Guide](../guides/odata-queries.md)** - Advanced filtering and querying
- **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling strategies