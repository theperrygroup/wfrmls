# Members API

Complete reference for the Members endpoint of the WFRMLS Python client.

---

## 👥 Overview

The Members API provides access to real estate agent and broker information, including contact details, office affiliations, and licensing data.

### Key Features

- **Agent profiles** - Access detailed agent information
- **Office associations** - View agent office affiliations
- **Contact information** - Get phone, email, and address details
- **License verification** - Access state license information
- **Status filtering** - Filter by active/inactive status

---

## 📚 Methods

### `get_members()`

Retrieve multiple member (agent/broker) records with optional filtering and pagination.

```python
def get_members(
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
- `Dict[str, Any]` - Response dictionary containing:
  - `@odata.context`: OData context URL
  - `value`: List of member dictionaries
  - `@odata.count`: Total count (if requested)
  - `@odata.nextLink`: URL for next page of results

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get first 10 members
response = client.member.get_members(top=10)
members = response["value"]

# Get active members only
active_response = client.member.get_active_members(top=20)

# Search by name
smith_agents = client.member.get_members(
    filter_query="contains(MemberLastName, 'Smith')",
    select=["MemberKey", "MemberFullName", "MemberStatus", "OfficeName"],
    orderby="MemberLastName asc"
)

# Get members with count
result_with_count = client.member.get_members(
    filter_query="MemberStatus eq 'Active'",
    count=True,
    top=1
)
total_active = result_with_count.get("@odata.count", 0)
```

### `get_member()`

Retrieve detailed information for a specific member by member key.

```python
def get_member(member_key: str) -> Optional[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `member_key` | `str` | Unique member identifier |

**Returns:**
- `Optional[Dict[str, Any]]` - Member dictionary or `None` if not found

**Examples:**

```python
# Get specific member
member = client.member.get_member("40")

if member:
    print(f"Agent: {member['MemberFullName']}")
    print(f"Office: {member['OfficeName']}")
    print(f"Phone: {member['MemberPreferredPhone']}")
```

---

## 🏷️ Field Reference

### Core Identification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberKeyNumeric** | `integer` | Numeric member key | `40` |
| **MemberKey** | `string` | Unique member identifier | `"40"` |
| **MemberMlsId** | `string` | MLS member ID | `"40"` |
| **MemberNationalAssociationId** | `string` | National association ID | `"835504500"` |
| **OriginatingSystemMemberKey** | `string` | Source system key | `"993c6306..."` |
| **OriginatingSystemName** | `string` | Source system name | `"UtahRealEstate.com"` |

### Personal Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberFirstName** | `string` | First name | `"Liz"` |
| **MemberLastName** | `string` | Last name | `"Memmott"` |
| **MemberMiddleName** | `string` | Middle name | `""` |
| **MemberFullName** | `string` | Full name | `"Liz Memmott"` |

### Contact Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberAddress1** | `string` | Primary address | `"3527 Summeroaks Circle"` |
| **MemberAddress2** | `string` | Secondary address | `""` |
| **MemberCity** | `string` | City | `"Salt Lake City"` |
| **MemberStateOrProvince** | `string` | State | `"UT"` |
| **MemberPostalCode** | `string` | ZIP code | `"84121"` |
| **MemberCountry** | `string` | Country | `""` |
| **MemberCountyOrParish** | `string` | County | `""` |

### Phone & Communication

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberPreferredPhone** | `string` | Preferred phone | `"801-231-1705"` |
| **MemberOfficePhone** | `string` | Office phone | `"801-567-4000"` |
| **MemberMobilePhone** | `string` | Mobile phone | `"801-231-1705"` |
| **MemberFax** | `string` | Fax number | `"801-567-4001"` |

### Office Association

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficeKeyNumeric** | `integer` | Office numeric key | `69433` |
| **OfficeKey** | `string` | Office identifier | `"69433"` |
| **OfficeMlsId** | `string` | Office MLS ID | `"69433"` |
| **OfficeName** | `string` | Office name | `"Coldwell Banker Realty (Union Heights)"` |

### Professional Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberStatus** | `string` | Member status | `"Active"`, `"Inactive"` |
| **MemberType** | `string` | Member type | `"MLS Only Salesperson"`, `"MLS Only Broker"` |
| **MemberAOR** | `string` | Association of Realtors | `"Salt Lake Board"` |
| **MemberAORkey** | `string` | AOR key | `"M00000628"` |
| **MemberStateLicense** | `string` | State license number | `"5452690"` |
| **MemberStateLicenseState** | `string` | License state | `"UT"` |
| **MemberDesignation** | `string` | Professional designations | `"Associate Broker (AB),Accredited Buyer's Representative / ABR"` |

### System Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MemberMlsAccessYN** | `boolean` | Has MLS access | `true` |
| **ModificationTimestamp** | `datetime` | Last modified | `"2025-05-27T17:11:03Z"` |
| **OriginalEntryTimestamp** | `datetime` | Original entry date | `null` |

---

## 🔍 Common Query Patterns

### Status Filtering

```python
# Active members only
active_members = client.member.get_active_members(top=50)

# Inactive members
inactive = client.member.get_members(
    filter_query="MemberStatus eq 'Inactive'",
    select=["MemberKey", "MemberFullName", "MemberStatus"]
)
```

### Name Searches

```python
# Search by last name
smiths = client.member.search_members_by_name(last_name="Smith")

# Search by first name
johns = client.member.get_members(
    filter_query="startswith(MemberFirstName, 'John')"
)

# Full name contains
client.member.get_members(
    filter_query="contains(MemberFullName, 'Williams')"
)
```

### Office Queries

```python
# Members from specific office
office_members = client.member.get_members(
    filter_query="OfficeKey eq '69433'",
    select=["MemberFullName", "MemberType", "MemberStatus"]
)

# Members by office name
coldwell_agents = client.member.get_members(
    filter_query="contains(OfficeName, 'Coldwell')"
)
```

### Professional Filters

```python
# Brokers only
brokers = client.member.get_members(
    filter_query="MemberType eq 'MLS Only Broker'"
)

# Members with specific designations
abr_agents = client.member.get_members(
    filter_query="contains(MemberDesignation, 'ABR')"
)

# Members by AOR
salt_lake_members = client.member.get_members(
    filter_query="MemberAOR eq 'Salt Lake Board'"
)
```

### Contact Information

```python
# Members with mobile phones
with_mobile = client.member.get_members(
    filter_query="MemberMobilePhone ne null",
    select=["MemberFullName", "MemberMobilePhone"]
)

# Members in specific city
salt_lake_agents = client.member.get_members(
    filter_query="MemberCity eq 'Salt Lake City'"
)
```

---

## 📊 Pagination Examples

### Iterating Through All Members

```python
def get_all_active_members():
    """Retrieve all active members using pagination."""
    all_members = []
    skip = 0
    page_size = 200  # Maximum allowed
    
    while True:
        response = client.member.get_members(
            filter_query="MemberStatus eq 'Active'",
            top=page_size,
            skip=skip,
            orderby="MemberKey asc"
        )
        
        members = response.get("value", [])
        if not members:
            break
            
        all_members.extend(members)
        
        # Check for next page
        if "@odata.nextLink" not in response:
            break
            
        skip += page_size
    
    return all_members
```

### Member Directory

```python
def create_member_directory(letter: str):
    """Create alphabetical directory for members."""
    
    members = client.member.get_members(
        filter_query=f"startswith(MemberLastName, '{letter}')",
        select=[
            "MemberKey", "MemberFullName", "MemberPreferredPhone",
            "OfficeName", "MemberStatus"
        ],
        orderby="MemberLastName asc, MemberFirstName asc"
    )
    
    return members["value"]

# Get all members with last names starting with 'A'
a_members = create_member_directory('A')
```

---

## ⚡ Performance Tips

### Optimize Field Selection

```python
# ❌ Inefficient - retrieves all fields
all_fields = client.member.get_members(top=100)

# ✅ Efficient - only needed fields
contact_list = client.member.get_members(
    select=["MemberKey", "MemberFullName", "MemberPreferredPhone"],
    top=100
)
```

### Efficient Filtering

```python
# Combine filters to reduce result set
active_brokers_in_salt_lake = client.member.get_members(
    filter_query=(
        "MemberStatus eq 'Active' and "
        "MemberType eq 'MLS Only Broker' and "
        "MemberCity eq 'Salt Lake City'"
    ),
    select=["MemberKey", "MemberFullName", "OfficeName"]
)
```

### Batch Operations

```python
# Get multiple members by keys efficiently
member_keys = ["40", "75", "13", "34"]
filter_parts = [f"MemberKey eq '{key}'" for key in member_keys]
filter_query = " or ".join(filter_parts)

members = client.member.get_members(
    filter_query=f"({filter_query})"
)