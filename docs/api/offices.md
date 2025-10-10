# Offices API

Complete reference for the Offices endpoint of the WFRMLS Python client.

---

## 🏢 Overview

The Offices API provides access to real estate brokerage and office information, including contact details, addresses, and licensing information.

### Key Features

- **Office profiles** - Access brokerage and office information
- **Contact details** - Get phone, fax, and address information
- **Branch relationships** - View main office associations
- **Status filtering** - Filter by active/inactive status
- **Broker information** - Access managing broker details

---

## 📚 Methods

### `get_offices()`

Retrieve multiple office records with optional filtering and pagination.

```python
def get_offices(
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
  - `value`: List of office dictionaries
  - `@odata.count`: Total count (if requested)
  - `@odata.nextLink`: URL for next page of results

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get first 10 offices
response = client.office.get_offices(top=10)
offices = response["value"]

# Get active offices only
active_response = client.office.get_active_offices(top=20)

# Search by office name
realty_offices = client.office.get_offices(
    filter_query="contains(OfficeName, 'Realty')",
    select=["OfficeKey", "OfficeName", "OfficeCity", "OfficeStatus"],
    orderby="OfficeName asc"
)

# Get offices with count
result_with_count = client.office.get_offices(
    filter_query="OfficeStatus eq 'Active'",
    count=True,
    top=1
)
total_active = result_with_count.get("@odata.count", 0)
```

### `get_office()`

Retrieve detailed information for a specific office by office key.

```python
def get_office(office_key: str) -> Optional[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `office_key` | `str` | Unique office identifier |

**Returns:**
- `Optional[Dict[str, Any]]` - Office dictionary or `None` if not found

**Examples:**

```python
# Get specific office
office = client.office.get_office("3")

if office:
    print(f"Office: {office['OfficeName']}")
    print(f"Phone: {office['OfficePhone']}")
    print(f"Status: {office['OfficeStatus']}")
```

---

## 🏷️ Field Reference

### Core Identification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficeKeyNumeric** | `integer` | Numeric office key | `3` |
| **OfficeKey** | `string` | Unique office identifier | `"3"` |
| **OfficeMlsId** | `string` | MLS office ID | `"3"` |
| **OriginatingSystemOfficeKey** | `string` | Source system key | `"fcd99ec6..."` |
| **OriginatingSystemName** | `string` | Source system name | `"UtahRealEstate.com"` |

### Office Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficeName** | `string` | Office/brokerage name | `"Federal Housing Agency FHA"` |
| **OfficeBranchType** | `string` | Branch type | `"Branch"` |
| **OfficeStatus** | `string` | Office status | `"Active"` |
| **OfficeCorporateLicense** | `string` | Corporate license | `"-1"` |

### Contact Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficeAddress1** | `string` | Primary address | `"125 south state street suite 3001"` |
| **OfficeAddress2** | `string` | Secondary address | `""` |
| **OfficeCity** | `string` | City | `"Salt Lake City"` |
| **OfficeStateOrProvince** | `string` | State | `"UT"` |
| **OfficePostalCode** | `string` | ZIP code | `"84138"` |
| **OfficeCountyOrParish** | `string` | County | `""` |

### Communication

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficePhone** | `string` | Main phone number | `"801-524-6413"` |
| **OfficeFax** | `string` | Fax number | `""` |

### Broker Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **OfficeBrokerKey** | `string` | Managing broker key | `"44002406"` |
| **OfficeBrokerMlsId** | `string` | Broker MLS ID | `"44002406"` |

### Branch Relationships

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **MainOfficeKeyNumeric** | `integer` | Main office numeric key | `null` |
| **MainOfficeMlsId** | `string` | Main office MLS ID | `""` |

### System Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ModificationTimestamp** | `datetime` | Last modified | `"2016-02-18T18:10:04Z"` |
| **OriginalEntryTimestamp** | `datetime` | Original entry date | `"1998-06-19T15:09:00Z"` |

---

## 🔍 Common Query Patterns

### Status Filtering

```python
# Active offices only
active_offices = client.office.get_active_offices(top=50)

# All offices (including inactive)
all_offices = client.office.get_offices(
    select=["OfficeKey", "OfficeName", "OfficeStatus"],
    orderby="OfficeStatus desc, OfficeName asc"
)
```

### Name Searches

```python
# Search by office name contains
realty_offices = client.office.search_offices_by_name("Realty")

# Offices starting with specific letter
c_offices = client.office.get_offices(
    filter_query="startswith(OfficeName, 'C')"
)

# Exact name match
coldwell = client.office.get_offices(
    filter_query="OfficeName eq 'Coldwell Banker Realty'"
)
```

### Location Queries

```python
# Offices in specific city
salt_lake_offices = client.office.get_offices(
    filter_query="OfficeCity eq 'Salt Lake City'",
    select=["OfficeName", "OfficeAddress1", "OfficePhone"]
)

# Offices by ZIP code
zip_offices = client.office.get_offices(
    filter_query="OfficePostalCode eq '84101'"
)

# Offices in multiple cities
cities = ['Salt Lake City', 'Park City', 'Provo']
city_filter = " or ".join([f"OfficeCity eq '{city}'" for city in cities])
multi_city_offices = client.office.get_offices(
    filter_query=f"({city_filter})"
)
```

### Branch Relationships

```python
# Branch offices only
branches = client.office.get_offices(
    filter_query="OfficeBranchType eq 'Branch'"
)

# Offices with main office
with_main = client.office.get_offices(
    filter_query="MainOfficeKeyNumeric ne null"
)
```

### Broker Queries

```python
# Offices by broker
broker_offices = client.office.get_offices(
    filter_query="OfficeBrokerKey eq '44002406'",
    select=["OfficeName", "OfficeCity", "OfficeBrokerMlsId"]
)
```

---

## 📊 Pagination Examples

### Iterating Through All Offices

```python
def get_all_offices():
    """Retrieve all offices using pagination."""
    all_offices = []
    skip = 0
    page_size = 200  # Maximum allowed
    
    while True:
        response = client.office.get_offices(
            top=page_size,
            skip=skip,
            orderby="OfficeKey asc"
        )
        
        offices = response.get("value", [])
        if not offices:
            break
            
        all_offices.extend(offices)
        
        # Check for next page
        if "@odata.nextLink" not in response:
            break
            
        skip += page_size
        print(f"Retrieved {len(all_offices)} offices...")
    
    return all_offices
```

### Office Directory by Location

```python
def create_office_directory_by_city():
    """Create directory of offices grouped by city."""
    
    # Get all active offices with location info
    response = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select=["OfficeKey", "OfficeName", "OfficeCity", "OfficePhone"],
        orderby="OfficeCity asc, OfficeName asc"
    )
    
    # Group by city
    directory = {}
    for office in response.get("value", []):
        city = office.get("OfficeCity", "Unknown")
        if city not in directory:
            directory[city] = []
        directory[city].append(office)
    
    return directory
```

---

## ⚡ Performance Tips

### Optimize Field Selection

```python
# ❌ Inefficient - retrieves all fields
all_fields = client.office.get_offices(top=100)

# ✅ Efficient - only needed fields
office_list = client.office.get_offices(
    select=["OfficeKey", "OfficeName", "OfficePhone", "OfficeCity"],
    top=100
)
```

### Efficient Status Checks

```python
# Count offices by status efficiently
active_count = client.office.get_offices(
    filter_query="OfficeStatus eq 'Active'",
    top=0,  # Don't need actual records
    count=True
)["@odata.count"]

print(f"Active offices: {active_count}")
```

### Batch Office Lookups

```python
# Get multiple offices by keys efficiently
office_keys = ["1", "3", "100", "200"]
filter_parts = [f"OfficeKey eq '{key}'" for key in office_keys]
filter_query = " or ".join(filter_parts)

offices = client.office.get_offices(
    filter_query=f"({filter_query})",
    select=["OfficeKey", "OfficeName", "OfficePhone"]
)