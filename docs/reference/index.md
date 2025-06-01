# Reference Documentation

Comprehensive reference materials for WFRMLS data structures, standards, and conventions.

---

## 📚 Reference Materials

<div class="grid cards" markdown>

-   :material-code-json:{ .lg .middle } **Data Types**

    ---

    Complete reference for all WFRMLS data types and structures

    [:octicons-arrow-right-24: View Data Types](data-types.md)

-   :material-table:{ .lg .middle } **Field Reference**

    ---

    Detailed documentation of all available fields and properties

    [:octicons-arrow-right-24: Browse Fields](fields.md)

-   :material-alert-circle:{ .lg .middle } **Status Codes**

    ---

    HTTP status codes and API response meanings

    [:octicons-arrow-right-24: Status Reference](status-codes.md)

-   :material-map:{ .lg .middle } **Utah Grid System**

    ---

    Local address conventions and coordinate systems

    [:octicons-arrow-right-24: Grid System](utah-grid.md)

-   :material-certificate:{ .lg .middle } **RESO Standards**

    ---

    Real Estate Standards Organization compliance information

    [:octicons-arrow-right-24: RESO Standards](reso-standards.md)

</div>

---

## 🔍 Quick Reference

### Common Field Names

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **ListingId** | `string` | Unique property identifier | `"12345678"` |
| **ListPrice** | `integer` | Current listing price | `450000` |
| **StandardStatus** | `string` | Property status | `"Active"`, `"Pending"` |
| **City** | `string` | Property city | `"Salt Lake City"` |
| **BedroomsTotal** | `integer` | Total bedrooms | `3` |
| **BathroomsTotalInteger** | `integer` | Total bathrooms | `2` |
| **SquareFeet** | `integer` | Living area square footage | `2150` |
| **YearBuilt** | `integer` | Year property was built | `1998` |

### Standard Status Values

| Status | Description | Searchable |
|--------|-------------|------------|
| **Active** | Available for sale | ✅ |
| **Pending** | Under contract | ✅ |
| **Sold** | Sale completed | ✅ |
| **Expired** | Listing expired | ✅ |
| **Withdrawn** | Withdrawn from market | ✅ |
| **Cancelled** | Listing cancelled | ⚠️ |

### Property Types

| Type | Description | Common Use |
|------|-------------|------------|
| **Residential** | Single-family homes | Most common searches |
| **Condominium** | Condos and townhomes | Urban properties |
| **Land** | Vacant land/lots | Development opportunities |
| **Commercial** | Commercial properties | Investment searches |
| **Multi-Family** | Duplexes, apartments | Investment properties |

---

## 📊 Data Structure Reference

### OData Response Format

All WFRMLS API responses follow the OData v4 standard:

```json
{
  "@odata.context": "https://api.wfrmls.com/reso/odata/$metadata#Property",
  "@odata.count": 1234,
  "value": [
    {
      "ListingId": "12345678",
      "ListPrice": 450000,
      "StandardStatus": "Active",
      "City": "Salt Lake City",
      "BedroomsTotal": 3,
      "BathroomsTotalInteger": 2,
      "SquareFeet": 2150,
      "YearBuilt": 1998,
      "ModificationTimestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Filter Query Syntax

| Operation | Operator | Example | Description |
|-----------|----------|---------|-------------|
| **Equal** | `eq` | `City eq 'Provo'` | Exact match |
| **Not Equal** | `ne` | `ListPrice ne 0` | Not equal |
| **Greater Than** | `gt` | `ListPrice gt 500000` | Numeric comparison |
| **Greater/Equal** | `ge` | `BedroomsTotal ge 3` | Inclusive comparison |
| **Less Than** | `lt` | `DaysOnMarket lt 30` | Numeric comparison |
| **Less/Equal** | `le` | `ListPrice le 1000000` | Inclusive comparison |
| **Contains** | `contains()` | `contains(City, 'Lake')` | String search |
| **Starts With** | `startswith()` | `startswith(Address, '123')` | String prefix |
| **Logical AND** | `and` | `Active and Price gt 300000` | Combine conditions |
| **Logical OR** | `or` | `City eq 'Provo' or City eq 'Orem'` | Alternative conditions |

---

## 🏠 Property Reference

### Required Fields

These fields are always present in property responses:

- **ListingId** - Unique identifier
- **StandardStatus** - Current status
- **ModificationTimestamp** - Last update time

### Core Property Fields

??? info "Basic Information"
    - `ListingId` - Unique property identifier
    - `ListPrice` - Current asking price
    - `StandardStatus` - Active, Pending, Sold, etc.
    - `City` - Property city
    - `StateOrProvince` - State (typically "UT")
    - `PostalCode` - ZIP code
    - `County` - County name

??? info "Physical Characteristics"
    - `BedroomsTotal` - Total bedrooms
    - `BathroomsTotalInteger` - Total bathrooms
    - `SquareFeet` - Living area square footage
    - `LotSizeSquareFeet` - Lot size
    - `YearBuilt` - Construction year
    - `Stories` - Number of stories
    - `Garage` - Garage description

??? info "Location Data"
    - `Latitude` - GPS latitude
    - `Longitude` - GPS longitude
    - `Address` - Street address
    - `StreetName` - Street name only
    - `StreetNumber` - House number
    - `UnitNumber` - Unit/apartment number

??? info "Listing Details"
    - `ListAgentKey` - Listing agent identifier
    - `ListOfficeKey` - Listing office identifier
    - `OnMarketDate` - Date listed
    - `DaysOnMarket` - Days since listing
    - `OriginalListPrice` - Initial asking price
    - `PriceChangeTimestamp` - Last price change

---

## 👥 Member Reference

### Agent Information Fields

| Field | Type | Description |
|-------|------|-------------|
| **MemberKey** | `string` | Unique agent identifier |
| **MemberFullName** | `string` | Agent's full name |
| **MemberFirstName** | `string` | First name |
| **MemberLastName** | `string` | Last name |
| **MemberEmail** | `string` | Email address |
| **MemberMobilePhone** | `string` | Mobile phone number |
| **MemberOfficePhone** | `string` | Office phone number |
| **MemberStatus** | `string` | Active, Inactive, etc. |

### Member Status Values

- **Active** - Currently active agent
- **Inactive** - Temporarily inactive
- **Suspended** - Suspended membership
- **Terminated** - Membership terminated

---

## 🏢 Office Reference

### Brokerage Information Fields

| Field | Type | Description |
|-------|------|-------------|
| **OfficeKey** | `string` | Unique office identifier |
| **OfficeName** | `string` | Brokerage name |
| **OfficePhone** | `string` | Main phone number |
| **OfficeEmail** | `string` | Email address |
| **OfficeAddress1** | `string` | Street address |
| **OfficeCity** | `string` | City |
| **OfficeStateOrProvince** | `string` | State |
| **OfficePostalCode** | `string` | ZIP code |

---

## 🚪 Open House Reference

### Event Information Fields

| Field | Type | Description |
|-------|------|-------------|
| **OpenHouseKey** | `string` | Unique event identifier |
| **ListingId** | `string` | Associated property |
| **OpenHouseDate** | `datetime` | Event date |
| **OpenHouseStartTime** | `time` | Start time |
| **OpenHouseEndTime** | `time` | End time |
| **OpenHouseType** | `string` | Public, Broker, etc. |

---

## 📋 Lookup Tables

### Common Lookup Categories

??? info "Property Features"
    - Appliances included
    - Heating/cooling systems
    - Flooring types
    - Architectural styles
    - Special features

??? info "Financial Information"
    - Financing types available
    - Tax information
    - HOA details
    - Utilities included

??? info "Location Details"
    - School districts
    - Neighborhood names
    - Subdivisions
    - Development names

---

## 🔧 Technical Reference

### API Limits

| Limit Type | Value | Notes |
|------------|-------|-------|
| **Requests per minute** | 100 | Per IP address |
| **Requests per hour** | 6,000 | Per bearer token |
| **Response size** | 10 MB | Maximum response |
| **Query timeout** | 30 seconds | Maximum processing time |

### Supported Date Formats

- **ISO 8601**: `2024-01-15T10:30:00Z`
- **Date only**: `2024-01-15`
- **Relative**: `2024-01-15T10:30:00-07:00`

### Geographic Coordinate System

- **Datum**: WGS84
- **Format**: Decimal degrees
- **Precision**: 6 decimal places
- **Range**: Latitude: 36-42°N, Longitude: 109-114°W

---

## 📚 Related Documentation

### **Standards & Compliance**
- **[RESO Standards](reso-standards.md)** - Industry standard compliance
- **[Data Types](data-types.md)** - Complete type reference
- **[Status Codes](status-codes.md)** - HTTP response codes

### **Local Conventions**
- **[Utah Grid System](utah-grid.md)** - Address coordinate system
- **[Field Reference](fields.md)** - Complete field documentation

### **Development Resources**
- **[API Reference](../api/index.md)** - Method documentation
- **[User Guides](../guides/index.md)** - Implementation guides
- **[Examples](../examples/index.md)** - Code samples

---

## 🔍 Search Tips

### Finding Information

- **Data Types** → For field formats and validation rules
- **Field Reference** → For complete field documentation
- **Status Codes** → For API error troubleshooting
- **RESO Standards** → For industry compliance details
- **Utah Grid** → For local address conventions

### Common Lookups

- **What fields are available?** → [Field Reference](fields.md)
- **What status values exist?** → [Status Codes](status-codes.md)
- **How do coordinates work?** → [Utah Grid System](utah-grid.md)
- **What are the standards?** → [RESO Standards](reso-standards.md)
- **What data types exist?** → [Data Types](data-types.md)

---

*Looking for something specific? Use the search function or browse the detailed reference materials above.* 