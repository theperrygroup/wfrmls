# Members API

The Members API provides access to real estate agent and member information within the WFRMLS system. This includes agent profiles, contact information, licensing details, and professional status.

## Overview

The `MemberClient` class handles all member-related operations, providing methods to search, retrieve, and filter real estate agent data.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
members = client.member.get_members(top=10)
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_members()` | Retrieve multiple members with filtering | `List[Dict[str, Any]]` |
| `get_member()` | Get a specific member by ID | `Dict[str, Any]` |
| `search_members()` | Search members by criteria | `List[Dict[str, Any]]` |
| `get_member_statistics()` | Get member performance statistics | `Dict[str, Any]` |

## Methods

### get_members()

Retrieve multiple members with optional filtering, sorting, and pagination.

```python
def get_members(
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
    # Get first 10 active members
    members = client.member.get_members(
        top=10,
        filter_query="MemberStatus eq 'Active'"
    )
    
    for member in members:
        print(f"{member['MemberFirstName']} {member['MemberLastName']}")
    ```

=== "Specific Fields"

    ```python
    # Get only specific fields
    members = client.member.get_members(
        select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail"],
        filter_query="MemberStatus eq 'Active'",
        orderby="MemberLastName"
    )
    ```

=== "Advanced Filtering"

    ```python
    # Find members by office
    members = client.member.get_members(
        filter_query="OfficeKey eq '12345' and MemberStatus eq 'Active'",
        orderby="MemberLastName asc, MemberFirstName asc"
    )
    ```

### get_member()

Retrieve a specific member by their unique identifier.

```python
def get_member(
    self,
    member_key: str,
    select: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `member_key` | `str` | Yes | Unique member identifier |
| `select` | `List[str]` | No | Specific fields to return |

#### Example

```python
# Get specific member details
member = client.member.get_member(
    member_key="12345",
    select=["MemberKey", "MemberFirstName", "MemberLastName", "MemberEmail", "MemberMobilePhone"]
)

print(f"Agent: {member['MemberFirstName']} {member['MemberLastName']}")
print(f"Email: {member['MemberEmail']}")
```

### search_members()

Search for members using various criteria with fuzzy matching capabilities.

```python
def search_members(
    self,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    office_key: Optional[str] = None,
    status: Optional[MemberStatus] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | No | Member name (first or last) |
| `email` | `str` | No | Email address |
| `phone` | `str` | No | Phone number |
| `office_key` | `str` | No | Office identifier |
| `status` | `MemberStatus` | No | Member status |

#### Example

```python
from wfrmls import MemberStatus

# Search by name
members = client.member.search_members(
    name="Smith",
    status=MemberStatus.ACTIVE
)

# Search by office
office_members = client.member.search_members(
    office_key="12345",
    status=MemberStatus.ACTIVE
)
```

## Enums and Constants

### MemberStatus

Enumeration of possible member statuses:

```python
from wfrmls import MemberStatus

class MemberStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    PENDING = "Pending"
```

### MemberType

Enumeration of member types:

```python
from wfrmls import MemberType

class MemberType(str, Enum):
    AGENT = "Agent"
    BROKER = "Broker"
    ASSISTANT = "Assistant"
    APPRAISER = "Appraiser"
```

## Common Use Cases

### Agent Directory

```python
# Build an agent directory
active_agents = client.member.get_members(
    filter_query="MemberStatus eq 'Active' and MemberType eq 'Agent'",
    select=[
        "MemberKey", "MemberFirstName", "MemberLastName", 
        "MemberEmail", "MemberMobilePhone", "OfficeKey"
    ],
    orderby="MemberLastName asc"
)

for agent in active_agents:
    print(f"{agent['MemberFirstName']} {agent['MemberLastName']}")
    print(f"  Email: {agent['MemberEmail']}")
    print(f"  Phone: {agent['MemberMobilePhone']}")
    print()
```

### Office Team Lookup

```python
# Get all members of a specific office
def get_office_team(office_key: str):
    return client.member.get_members(
        filter_query=f"OfficeKey eq '{office_key}' and MemberStatus eq 'Active'",
        select=[
            "MemberKey", "MemberFirstName", "MemberLastName",
            "MemberEmail", "MemberType", "MemberStateLicense"
        ],
        orderby="MemberType desc, MemberLastName asc"
    )

team = get_office_team("12345")
```

### Contact Information Sync

```python
# Sync member contact information
def sync_member_contacts():
    members = client.member.get_members(
        filter_query="MemberStatus eq 'Active'",
        select=[
            "MemberKey", "MemberFirstName", "MemberLastName",
            "MemberEmail", "MemberMobilePhone", "MemberDirectPhone",
            "ModificationTimestamp"
        ]
    )
    
    # Process for CRM integration
    for member in members:
        # Update your CRM system
        update_crm_contact(member)
```

## Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `MemberKey` | `str` | Unique member identifier |
| `MemberFirstName` | `str` | First name |
| `MemberLastName` | `str` | Last name |
| `MemberFullName` | `str` | Full name |
| `MemberEmail` | `str` | Primary email address |
| `MemberStatus` | `str` | Current status (Active, Inactive, etc.) |
| `MemberType` | `str` | Member type (Agent, Broker, etc.) |

### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `MemberMobilePhone` | `str` | Mobile phone number |
| `MemberDirectPhone` | `str` | Direct office phone |
| `MemberHomePhone` | `str` | Home phone number |
| `MemberFax` | `str` | Fax number |
| `MemberAddress1` | `str` | Primary address line 1 |
| `MemberAddress2` | `str` | Primary address line 2 |
| `MemberCity` | `str` | City |
| `MemberStateOrProvince` | `str` | State or province |
| `MemberPostalCode` | `str` | ZIP/postal code |

### Professional Information

| Field | Type | Description |
|-------|------|-------------|
| `MemberStateLicense` | `str` | State license number |
| `MemberNationalAssociationId` | `str` | NAR ID |
| `OfficeKey` | `str` | Associated office identifier |
| `MemberAOR` | `str` | Association of Realtors |
| `MemberDesignation` | `str` | Professional designations |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `OriginalEntryTimestamp` | `datetime` | When record was created |
| `ModificationTimestamp` | `datetime` | Last modification time |
| `MemberLoginId` | `str` | System login identifier |

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    member = client.member.get_member("invalid_key")
except NotFoundError:
    print("Member not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Best Practices

### Performance Optimization

1. **Use select parameter** to limit returned fields
2. **Implement pagination** for large result sets
3. **Cache frequently accessed data** like office teams
4. **Use specific filters** to reduce data transfer

### Data Synchronization

1. **Track ModificationTimestamp** for incremental updates
2. **Handle deleted/inactive members** appropriately
3. **Validate contact information** before use
4. **Respect rate limits** during bulk operations

### Security Considerations

1. **Protect member contact information** according to privacy laws
2. **Validate member permissions** before displaying data
3. **Use HTTPS** for all API communications
4. **Log access** for audit purposes

## Related Resources

- [Office API](offices.md) - For office information
- [Properties API](properties.md) - For agent listings
- [OData Queries Guide](../guides/odata-queries.md) - Advanced filtering
- [Error Handling Guide](../guides/error-handling.md) - Exception management