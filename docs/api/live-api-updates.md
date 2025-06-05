# Live API Testing Updates

This document summarizes the key updates made to the WFRMLS API documentation based on live API testing performed on January 31, 2025.

---

## 🔍 Overview

The documentation has been updated to reflect the actual response structures and field names returned by the live WFRMLS API. Testing revealed several important differences between the expected and actual API responses.

---

## 📊 Key Findings

### Response Structure

All API endpoints return a consistent OData response structure:

```json
{
  "@odata.context": "$metadata#EntityType",
  "value": [...],
  "@odata.count": 12345,  // When count=true
  "@odata.nextLink": "https://..."  // When more pages available
}
```

**Important**: The main data is always in the `value` array, not returned directly as a list.

### Field Naming Conventions

The API uses several naming patterns:
- **Numeric Keys**: Most entities have both string and numeric key fields (e.g., `ListingKey` and `ListingKeyNumeric`)
- **YN Suffix**: Boolean fields use `YN` suffix (e.g., `AttachedGarageYN`, `FireplaceYN`)
- **Full Names**: Many fields include full descriptive names (e.g., `CountyOrParish` not just `County`)

---

## 🏠 Property Endpoint Updates

### Corrected Field Names

| Old Documentation | Actual Field Name | Type |
|-------------------|-------------------|------|
| `ListingId` (primary) | `ListingKeyNumeric` | `integer` |
| `Address` | `UnparsedAddress` | `string` |
| `County` | `CountyOrParish` | `string` |
| `SquareFeet` | `LivingArea` | `decimal` |
| `BathroomsTotal` | `BathroomsTotalInteger` | `integer` |

### New Important Fields

- **Address Components**: `StreetDirPrefix`, `StreetDirSuffix`, `StreetNumber`, `StreetNumberNumeric`
- **Status Fields**: Both `StandardStatus` and `MlsStatus` are available
- **Timestamps**: Multiple timestamp fields for tracking changes
- **Property Types**: `PropertyType`, `PropertySubType`, and `CurrentUse`

### Example Response

```json
{
  "@odata.context": "$metadata#Property",
  "value": [
    {
      "ListingKeyNumeric": 1611952,
      "StandardStatus": "Active",
      "ListPrice": 1600.0,
      "City": "Salt Lake City",
      "UnparsedAddress": "1611 S MAIN ST 200",
      // ... many more fields
    }
  ]
}
```

---

## 👥 Member Endpoint Updates

### Key Fields

- **Identification**: `MemberKeyNumeric`, `MemberKey`, `MemberMlsId`
- **Contact**: `MemberPreferredPhone`, `MemberMobilePhone`, `MemberOfficePhone`
- **Professional**: `MemberStatus`, `MemberType`, `MemberDesignation`
- **Association**: `MemberAOR`, `MemberAORkey`

### Member Types
- `"MLS Only Salesperson"`
- `"MLS Only Broker"`

### Total Count
- Approximately 60,261 members in the system

---

## 🏢 Office Endpoint Updates

### Key Fields

- **Identification**: `OfficeKeyNumeric`, `OfficeKey`, `OfficeMlsId`
- **Details**: `OfficeName`, `OfficeStatus`, `OfficeBranchType`
- **Contact**: `OfficePhone`, `OfficeFax`
- **Location**: Full address fields including `OfficeStateOrProvince`

### Special Offices
- Office ID `1` is reserved for "NON-MLS"
- Office ID `3` is "Federal Housing Agency FHA"

---

## 🏘️ ADU Endpoint

Successfully documented with actual fields:
- `AduKeyNumeric` - Primary identifier
- `AttachedYN`, `SeparateEntranceYN`, `KitchenYN` - Boolean features
- `BedroomsTotal`, `BathroomsTotal`, `SquareFeet` - Unit specifications
- `CurrentlyRentedYN`, `Rent` - Rental information

---

## 🔍 Lookup Endpoint

Returns enumeration values for various fields:
- Property types
- Architectural styles
- Appliances
- And many more lookup categories

Response includes:
- `LookupKey`
- `LookupName` (category)
- `LookupValue` (display value)
- `StandardLookupValue`
- `LegacyODataValue`

---

## ❌ Issues Discovered

### Deleted Endpoint
The Deleted endpoint returned an error: "Bad request: Unknown property" when trying to use `DeletedDateTime` for ordering. This endpoint may need further investigation.

### Unavailable Endpoints
As documented in the README, the following endpoints remain unavailable:
- Media
- History  
- Green Verification

---

## 📝 Documentation Updates Made

1. **Field Reference Tables**: Updated all field names, types, and examples based on actual responses
2. **Code Examples**: Modified to use correct field names and response structure
3. **Response Structure**: Clarified that all endpoints return OData response objects
4. **Pagination**: Updated to show usage of `@odata.nextLink`
5. **New Documentation**: Created comprehensive docs for Member, Office, and ADU endpoints

---

## 🚀 Next Steps

1. Investigate the Deleted endpoint issue
2. Monitor for when Media, History, and Green Verification endpoints become available
3. Add more complex query examples based on actual field relationships
4. Consider adding response transformation utilities to simplify data access