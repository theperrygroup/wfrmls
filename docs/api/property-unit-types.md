# Property Unit Types API

Complete reference for the Property Unit Types endpoint of the WFRMLS Python client.

---

## 🏢 Overview

The Property Unit Types API provides detailed information about individual rental units within multi-unit properties. This endpoint is essential for analyzing investment properties, apartment buildings, and other multi-unit residential or commercial properties.

### Key Features

- **Unit details** - Access bedroom/bathroom counts per unit type
- **Rental income** - Get actual rent amounts for each unit type
- **Unit counts** - See how many units of each type exist
- **Property association** - Link unit types to property listings
- **Investment analysis** - Calculate rental income potential

---

## 📚 Methods

### `get_property_unit_types()`

Retrieve property unit type records with optional filtering and pagination.

```python
def get_property_unit_types(
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
- `Dict[str, Any]` - Response dictionary with unit type data

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get all unit types
unit_types = client.property_unit_types.get_property_unit_types()

# Get unit types for a specific property
property_units = client.property_unit_types.get_property_unit_types(
    filter_query="ListingKey eq '12345'"
)

# Get unit types with rental income > $1000
high_rent_units = client.property_unit_types.get_property_unit_types(
    filter_query="UnitTypeActualRent gt 1000",
    orderby="UnitTypeActualRent desc"
)
```

### `get_unit_types_by_listing()`

Get all unit types for a specific property listing.

```python
def get_unit_types_by_listing(
    listing_key: str
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|----------|------|-------------|
| `listing_key` | `str` | The ListingKey of the property |

**Returns:**
- `Dict[str, Any]` - Unit types for the specified listing

**Examples:**

```python
# Get unit types for a property
units = client.property_unit_types.get_unit_types_by_listing("12345")

# Calculate total rental income
total_income = 0
for unit in units["value"]:
    units_count = unit.get("UnitTypeUnitsTotal", 0)
    rent = unit.get("UnitTypeActualRent", 0)
    total_income += units_count * rent

print(f"Total Monthly Income: ${total_income:,.2f}")
```

### `get_residential_unit_types()`

Get unit types for residential properties only.

```python
def get_residential_unit_types(
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
- `Dict[str, Any]` - Residential unit type records

---

## 🏷️ Field Reference

Each unit type record contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **UnitTypeKey** | `string` | Unique identifier | `"1000063-1"` |
| **ListingKey** | `string` | Parent property ID | `"1000063"` |
| **ListingId** | `string` | MLS listing number | `"1000063"` |
| **ListingKeyNumeric** | `integer` | Numeric listing key | `1000063` |
| **UnitTypeUnitsTotal** | `integer` | Number of units of this type | `1` |
| **UnitTypeActualRent** | `decimal` | Monthly rent amount | `600.0` |
| **UnitTypeBedsTotal** | `integer` | Number of bedrooms | `2` |
| **UnitTypeBathsTotal** | `decimal` | Number of bathrooms | `1` |
| **UnitTypeDescription** | `string` | Unit description | `"Square Feet: 780"` |

---

## 🔍 Common Usage Patterns

### Investment Property Analysis

```python
def analyze_investment_property(listing_key: str):
    """Comprehensive analysis of rental income potential."""
    
    # Get unit types
    units_response = client.property_unit_types.get_unit_types_by_listing(listing_key)
    units = units_response["value"]
    
    # Get property details
    property_response = client.property.get_property_by_listing_key(listing_key)
    property_data = property_response
    
    # Calculate income metrics
    analysis = {
        "property_address": property_data.get("UnparsedAddress"),
        "list_price": property_data.get("ListPrice", 0),
        "unit_summary": [],
        "total_units": 0,
        "total_monthly_income": 0,
        "total_annual_income": 0,
        "gross_rent_multiplier": 0,
        "cap_rate": 0
    }
    
    # Analyze each unit type
    for unit in units:
        unit_count = unit.get("UnitTypeUnitsTotal", 0)
        rent = unit.get("UnitTypeActualRent", 0)
        beds = unit.get("UnitTypeBedsTotal", 0)
        baths = unit.get("UnitTypeBathsTotal", 0)
        
        monthly_income = unit_count * rent
        
        unit_info = {
            "type": f"{beds}BR/{baths}BA",
            "units": unit_count,
            "rent_per_unit": rent,
            "monthly_income": monthly_income,
            "description": unit.get("UnitTypeDescription", "")
        }
        
        analysis["unit_summary"].append(unit_info)
        analysis["total_units"] += unit_count
        analysis["total_monthly_income"] += monthly_income
    
    # Calculate investment metrics
    analysis["total_annual_income"] = analysis["total_monthly_income"] * 12
    
    if analysis["total_annual_income"] > 0:
        analysis["gross_rent_multiplier"] = (
            analysis["list_price"] / analysis["total_annual_income"]
        )
    
    # Estimate cap rate (simplified - doesn't include expenses)
    if analysis["list_price"] > 0:
        analysis["cap_rate"] = (
            (analysis["total_annual_income"] / analysis["list_price"]) * 100
        )
    
    return analysis

# Analyze a property
investment_analysis = analyze_investment_property("12345")
```

### Unit Mix Report

```python
def generate_unit_mix_report(listing_keys: List[str]):
    """Generate report showing unit mix across multiple properties."""
    
    # Build filter for multiple properties
    filters = [f"ListingKey eq '{key}'" for key in listing_keys]
    filter_query = " or ".join(filters)
    
    # Get all unit types
    response = client.property_unit_types.get_property_unit_types(
        filter_query=f"({filter_query})"
    )
    
    # Aggregate by unit configuration
    unit_mix = {}
    property_summaries = {}
    
    for unit in response["value"]:
        listing_key = unit["ListingKey"]
        beds = unit.get("UnitTypeBedsTotal", 0)
        baths = unit.get("UnitTypeBathsTotal", 0)
        unit_config = f"{beds}BR/{baths}BA"
        
        # Update unit mix totals
        if unit_config not in unit_mix:
            unit_mix[unit_config] = {
                "total_units": 0,
                "avg_rent": 0,
                "rent_sum": 0,
                "properties": set()
            }
        
        units_count = unit.get("UnitTypeUnitsTotal", 0)
        rent = unit.get("UnitTypeActualRent", 0)
        
        unit_mix[unit_config]["total_units"] += units_count
        unit_mix[unit_config]["rent_sum"] += rent * units_count
        unit_mix[unit_config]["properties"].add(listing_key)
        
        # Track per property
        if listing_key not in property_summaries:
            property_summaries[listing_key] = {
                "total_units": 0,
                "total_income": 0
            }
        
        property_summaries[listing_key]["total_units"] += units_count
        property_summaries[listing_key]["total_income"] += rent * units_count
    
    # Calculate averages
    for config, data in unit_mix.items():
        if data["total_units"] > 0:
            data["avg_rent"] = data["rent_sum"] / data["total_units"]
        data["properties"] = len(data["properties"])
        del data["rent_sum"]  # Remove intermediate calculation
    
    return {
        "unit_mix": unit_mix,
        "property_summaries": property_summaries
    }

# Generate report for multiple properties
properties = ["12345", "67890", "11111"]
report = generate_unit_mix_report(properties)
```

### Rental Rate Comparison

```python
def compare_rental_rates(bedroom_count: int, bathroom_count: int = None):
    """Compare rental rates for similar unit types."""
    
    # Build filter
    filters = [f"UnitTypeBedsTotal eq {bedroom_count}"]
    if bathroom_count:
        filters.append(f"UnitTypeBathsTotal eq {bathroom_count}")
    
    response = client.property_unit_types.get_property_unit_types(
        filter_query=" and ".join(filters),
        orderby="UnitTypeActualRent desc",
        top=100
    )
    
    # Calculate statistics
    rents = []
    for unit in response["value"]:
        rent = unit.get("UnitTypeActualRent", 0)
        if rent > 0:
            rents.append(rent)
    
    if rents:
        avg_rent = sum(rents) / len(rents)
        median_rent = sorted(rents)[len(rents) // 2]
        
        return {
            "bedroom_count": bedroom_count,
            "bathroom_count": bathroom_count,
            "sample_size": len(rents),
            "average_rent": avg_rent,
            "median_rent": median_rent,
            "min_rent": min(rents),
            "max_rent": max(rents),
            "rent_range": max(rents) - min(rents)
        }
    
    return None

# Compare 2-bedroom unit rates
comparison = compare_rental_rates(bedroom_count=2)
```

### Portfolio Income Summary

```python
def calculate_portfolio_income(listing_keys: List[str]):
    """Calculate total income across a portfolio of properties."""
    
    portfolio = {
        "properties": {},
        "total_units": 0,
        "total_monthly_income": 0,
        "total_annual_income": 0,
        "unit_breakdown": {}
    }
    
    for listing_key in listing_keys:
        # Get units for this property
        units = client.property_unit_types.get_unit_types_by_listing(listing_key)
        
        property_income = 0
        property_units = 0
        
        for unit in units["value"]:
            units_count = unit.get("UnitTypeUnitsTotal", 0)
            rent = unit.get("UnitTypeActualRent", 0)
            beds = unit.get("UnitTypeBedsTotal", 0)
            
            income = units_count * rent
            property_income += income
            property_units += units_count
            
            # Track unit breakdown
            unit_type = f"{beds}BR"
            if unit_type not in portfolio["unit_breakdown"]:
                portfolio["unit_breakdown"][unit_type] = 0
            portfolio["unit_breakdown"][unit_type] += units_count
        
        # Store property summary
        portfolio["properties"][listing_key] = {
            "units": property_units,
            "monthly_income": property_income,
            "annual_income": property_income * 12
        }
        
        portfolio["total_units"] += property_units
        portfolio["total_monthly_income"] += property_income
    
    portfolio["total_annual_income"] = portfolio["total_monthly_income"] * 12
    
    return portfolio

# Calculate portfolio income
my_properties = ["12345", "67890", "11111"]
portfolio_summary = calculate_portfolio_income(my_properties)
```

---

## ⚡ Performance Tips

1. **Batch property requests** - Get unit types for multiple properties in one call
2. **Use field selection** - Only request needed fields to reduce response size
3. **Cache unit configurations** - Store common unit type lookups
4. **Implement pagination** - Handle large portfolios efficiently
5. **Index by listing key** - Create lookup maps for faster access

---

## 📊 Integration Examples

### With Property Data

```python
def get_investment_properties_with_units():
    """Find investment properties with full unit details."""
    
    # Get multi-family properties
    properties = client.property.get_properties(
        filter_query="PropertySubType eq 'MultiFamily'",
        select=["ListingKey", "UnparsedAddress", "ListPrice", "UnitsTotal"],
        top=10
    )
    
    # Get unit types for all properties
    listing_keys = [p["ListingKey"] for p in properties["value"]]
    
    if listing_keys:
        filters = [f"ListingKey eq '{key}'" for key in listing_keys]
        units = client.property_unit_types.get_property_unit_types(
            filter_query=" or ".join(filters)
        )
        
        # Group units by property
        units_by_property = {}
        for unit in units["value"]:
            key = unit["ListingKey"]
            if key not in units_by_property:
                units_by_property[key] = []
            units_by_property[key].append(unit)
        
        # Combine data
        for prop in properties["value"]:
            prop["unit_types"] = units_by_property.get(prop["ListingKey"], [])
        
        return properties["value"]
    
    return []
```

---

## 🚨 Important Notes

- Not all properties have unit type data - primarily for multi-unit properties
- Rental amounts may be actual or projected rents
- Unit counts should match the property's total units
- Some MLSs may have limited unit type information
- Always verify rental income data independently