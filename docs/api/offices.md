# Offices API

The Offices API provides access to real estate office and brokerage information, including contact details, addresses, and licensing information. Offices represent the companies and brokerages that members (agents/brokers) work for.

!!! example "Quick Start"
    ```python
    # Get active offices
    offices = client.office.get_active_offices(top=50)
    
    # Get a specific office with member info
    office_detail = client.office.get_office_with_members("67890")
    
    # Search for offices by name
    offices = client.office.get_offices(
        filter_query="contains(OfficeName, 'Realty')",
        top=25
    )
    ```

## Office Client

::: wfrmls.office.OfficeClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### Basic Office Retrieval

=== "Active Offices"
    ```python
    # Get all active offices
    active_offices = client.office.get_active_offices(top=100)
    
    # Get active offices ordered by name
    offices_by_name = client.office.get_active_offices(
        orderby="OfficeName asc",
        top=50
    )
    ```

=== "Office Details"
    ```python
    # Get a specific office by key
    office = client.office.get_office("67890")
    
    # Get office with member information
    office_with_members = client.office.get_office_with_members("67890")
    
    # Get office with full expansion
    office_expanded = client.office.get_office_with_expansion(
        office_key="67890",
        expand="Member,Property"
    )
    ```

=== "Office Search"
    ```python
    # Search by office name
    realty_offices = client.office.get_offices(
        filter_query="contains(OfficeName, 'Realty')",
        orderby="OfficeName asc"
    )
    
    # Search by city
    slc_offices = client.office.get_offices(
        filter_query="contains(OfficeCity, 'Salt Lake')",
        orderby="OfficeName asc"
    )
    ```

### Advanced Filtering

=== "Location-Based"
    ```python
    # Offices in specific city
    park_city_offices = client.office.get_offices(
        filter_query="OfficeCity eq 'Park City'",
        orderby="OfficeName asc"
    )
    
    # Offices by state/province
    utah_offices = client.office.get_offices(
        filter_query="OfficeStateOrProvince eq 'UT'",
        select="OfficeKey,OfficeName,OfficeCity,OfficePhone"
    )
    
    # Offices by postal code
    downtown_offices = client.office.get_offices(
        filter_query="startswith(OfficePostalCode, '84101')",
        top=25
    )
    ```

=== "Contact Information"
    ```python
    # Offices with email addresses
    offices_with_email = client.office.get_offices(
        filter_query="OfficeEmail ne null",
        select="OfficeKey,OfficeName,OfficeEmail,OfficePhone"
    )
    
    # Offices with websites
    offices_with_web = client.office.get_offices(
        filter_query="OfficeURL ne null",
        select="OfficeKey,OfficeName,OfficeURL"
    )
    ```

=== "Office Status and Type"
    ```python
    # Active offices only
    active_offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        orderby="OfficeName asc"
    )
    
    # Offices by type (if available)
    franchise_offices = client.office.get_offices(
        filter_query="contains(OfficeName, 'Realty') or contains(OfficeName, 'Century')",
        top=50
    )
    ```

## Office Data Structure

Offices in WFRMLS follow the RESO standard with comprehensive business information:

??? info "Key Office Fields"
    **Identification**
    
    - `OfficeKey` - Unique office identifier
    - `OfficeMlsId` - MLS-specific office ID
    - `OfficeNationalAssociationId` - National association ID
    - `OfficeBrokerLicense` - Broker license number

    **Business Information**
    
    - `OfficeName` - Office/brokerage name
    - `OfficeStatus` - Active, Inactive, etc.
    - `OfficeType` - Office classification
    - `FranchiseAffiliation` - Franchise information

    **Contact Details**
    
    - `OfficePhone` - Main phone number
    - `OfficeFax` - Fax number
    - `OfficeEmail` - Primary email address
    - `OfficeURL` - Website URL

    **Address Information**
    
    - `OfficeAddress1`, `OfficeAddress2` - Street address
    - `OfficeCity` - City name
    - `OfficeStateOrProvince` - State/province
    - `OfficePostalCode` - Postal/ZIP code
    - `OfficeCountry` - Country code

    **System Information**
    
    - `ModificationTimestamp` - Last update time
    - `OriginalEntryTimestamp` - Initial creation time

## Integration Examples

### Office Directory with Agent Counts

```python
def create_office_directory(client):
    """Create a comprehensive office directory with agent counts."""
    
    # Get active offices
    offices = client.office.get_active_offices(
        select="OfficeKey,OfficeName,OfficePhone,OfficeEmail,OfficeCity,OfficeStateOrProvince",
        orderby="OfficeName asc",
        top=500
    )
    
    # Get member counts per office
    members = client.member.get_active_members(
        select="MemberKey,MemberOfficeKey",
        top=2000
    )
    
    # Count members per office
    member_counts = {}
    for member in members.get('value', []):
        office_key = member.get('MemberOfficeKey')
        if office_key:
            member_counts[office_key] = member_counts.get(office_key, 0) + 1
    
    # Build directory
    directory = []
    for office in offices.get('value', []):
        office_key = office.get('OfficeKey')
        agent_count = member_counts.get(office_key, 0)
        
        directory.append({
            'office_key': office_key,
            'name': office.get('OfficeName', 'Unknown'),
            'phone': office.get('OfficePhone'),
            'email': office.get('OfficeEmail'),
            'city': office.get('OfficeCity'),
            'state': office.get('OfficeStateOrProvince'),
            'agent_count': agent_count
        })
    
    # Sort by agent count (largest first)
    directory.sort(key=lambda x: x['agent_count'], reverse=True)
    return directory

# Usage
office_directory = create_office_directory(client)
print("🏢 Office Directory (by agent count)")
for i, office in enumerate(office_directory[:20], 1):
    print(f"{i:2d}. {office['name']} ({office['city']}, {office['state']})")
    print(f"    👥 {office['agent_count']} agents | 📞 {office['phone']} | 📧 {office['email']}")
```

### Market Coverage Analysis

```python
def analyze_market_coverage(client):
    """Analyze office coverage across different markets."""
    
    # Get all active offices with location info
    offices = client.office.get_active_offices(
        select="OfficeKey,OfficeName,OfficeCity,OfficeStateOrProvince,OfficePostalCode",
        top=1000
    )
    
    # Analyze by city
    city_coverage = {}
    zip_coverage = {}
    
    for office in offices.get('value', []):
        city = office.get('OfficeCity', 'Unknown')
        zip_code = office.get('OfficePostalCode', 'Unknown')[:5]  # First 5 digits
        
        # Count by city
        if city not in city_coverage:
            city_coverage[city] = {'office_count': 0, 'offices': []}
        city_coverage[city]['office_count'] += 1
        city_coverage[city]['offices'].append(office.get('OfficeName', 'Unknown'))
        
        # Count by ZIP code
        if zip_code not in zip_coverage:
            zip_coverage[zip_code] = {'office_count': 0, 'city': city}
        zip_coverage[zip_code]['office_count'] += 1
    
    # Sort results
    top_cities = sorted(city_coverage.items(), key=lambda x: x[1]['office_count'], reverse=True)
    top_zips = sorted(zip_coverage.items(), key=lambda x: x[1]['office_count'], reverse=True)
    
    return {
        'cities': top_cities[:15],
        'zip_codes': top_zips[:15],
        'total_offices': len(offices.get('value', []))
    }

# Usage
market_analysis = analyze_market_coverage(client)
print(f"📊 Market Coverage Analysis ({market_analysis['total_offices']} offices)")

print("\n🏙️ Top Cities by Office Count:")
for city, data in market_analysis['cities']:
    print(f"   {city}: {data['office_count']} offices")

print("\n📮 Top ZIP Codes by Office Count:")
for zip_code, data in market_analysis['zip_codes']:
    print(f"   {zip_code} ({data['city']}): {data['office_count']} offices")
```

### Office Contact Audit

```python
def audit_office_contacts(client):
    """Audit office contact information completeness."""
    
    # Get all active offices with contact fields
    offices = client.office.get_active_offices(
        select="OfficeKey,OfficeName,OfficePhone,OfficeEmail,OfficeURL,OfficeCity",
        top=500
    )
    
    audit_results = {
        'total_offices': 0,
        'complete_contacts': 0,
        'missing_phone': [],
        'missing_email': [],
        'missing_website': [],
        'no_contact_info': []
    }
    
    for office in offices.get('value', []):
        audit_results['total_offices'] += 1
        
        name = office.get('OfficeName', 'Unknown')
        city = office.get('OfficeCity', 'Unknown')
        office_display = f"{name} ({city})"
        
        phone = office.get('OfficePhone')
        email = office.get('OfficeEmail')
        website = office.get('OfficeURL')
        
        missing_contacts = []
        
        if not phone:
            missing_contacts.append('phone')
            audit_results['missing_phone'].append(office_display)
        
        if not email:
            missing_contacts.append('email')
            audit_results['missing_email'].append(office_display)
        
        if not website:
            missing_contacts.append('website')
            audit_results['missing_website'].append(office_display)
        
        if len(missing_contacts) == 3:  # Missing all contact info
            audit_results['no_contact_info'].append(office_display)
        elif len(missing_contacts) == 0:  # Has all contact info
            audit_results['complete_contacts'] += 1
    
    return audit_results

# Usage
contact_audit = audit_office_contacts(client)
print("📋 Office Contact Information Audit")
print(f"   Total Offices: {contact_audit['total_offices']}")
print(f"   Complete Contact Info: {contact_audit['complete_contacts']} ({contact_audit['complete_contacts']/contact_audit['total_offices']*100:.1f}%)")
print(f"   Missing Phone: {len(contact_audit['missing_phone'])} offices")
print(f"   Missing Email: {len(contact_audit['missing_email'])} offices")
print(f"   Missing Website: {len(contact_audit['missing_website'])} offices")
print(f"   No Contact Info: {len(contact_audit['no_contact_info'])} offices")

if contact_audit['no_contact_info']:
    print(f"\n⚠️  Offices with no contact information:")
    for office in contact_audit['no_contact_info'][:10]:
        print(f"   - {office}")
```

### Office Performance Metrics

```python
def calculate_office_metrics(client, days_back=30):
    """Calculate performance metrics for offices based on listings."""
    
    from datetime import datetime, timedelta
    cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Get recent listings
    recent_listings = client.property.get_properties(
        filter_query=f"ListingContractDate ge {cutoff_date}",
        select="ListingId,ListOfficeKey,ListPrice,PropertySubType",
        top=2000
    )
    
    # Calculate metrics per office
    office_metrics = {}
    for listing in recent_listings.get('value', []):
        office_key = listing.get('ListOfficeKey')
        if office_key:
            if office_key not in office_metrics:
                office_metrics[office_key] = {
                    'listing_count': 0,
                    'total_volume': 0,
                    'property_types': {}
                }
            
            office_metrics[office_key]['listing_count'] += 1
            
            list_price = listing.get('ListPrice', 0)
            office_metrics[office_key]['total_volume'] += list_price
            
            prop_type = listing.get('PropertySubType', 'Unknown')
            office_metrics[office_key]['property_types'][prop_type] = office_metrics[office_key]['property_types'].get(prop_type, 0) + 1
    
    # Get office details and combine with metrics
    office_performance = []
    for office_key, metrics in office_metrics.items():
        if metrics['listing_count'] >= 3:  # Minimum 3 listings
            try:
                office_detail = client.office.get_office(office_key)
                if office_detail:
                    avg_price = metrics['total_volume'] / metrics['listing_count']
                    
                    office_performance.append({
                        'office_key': office_key,
                        'name': office_detail.get('OfficeName', 'Unknown'),
                        'city': office_detail.get('OfficeCity', 'Unknown'),
                        'listings': metrics['listing_count'],
                        'volume': metrics['total_volume'],
                        'avg_price': avg_price,
                        'property_types': metrics['property_types']
                    })
            except:
                continue
    
    # Sort by listing volume
    office_performance.sort(key=lambda x: x['volume'], reverse=True)
    return office_performance[:25]  # Top 25

# Usage
office_metrics = calculate_office_metrics(client, days_back=30)
print("📈 Top Performing Offices (Last 30 Days)")
for i, office in enumerate(office_metrics, 1):
    print(f"{i:2d}. {office['name']} ({office['city']})")
    print(f"    📋 {office['listings']} listings | 💰 ${office['volume']:,.0f} volume | 📊 ${office['avg_price']:,.0f} avg")
    
    # Show top property types
    top_types = sorted(office['property_types'].items(), key=lambda x: x[1], reverse=True)[:3]
    type_summary = ", ".join([f"{ptype} ({count})" for ptype, count in top_types])
    print(f"    🏠 Top types: {type_summary}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    # Try to get an office
    office = client.office.get_office("67890")
    
except NotFoundError:
    print("❌ Office not found - the office key may be incorrect or the office may be inactive")
    
except ValidationError as e:
    print(f"📝 Invalid search parameters: {e}")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Performance Tips

!!! tip "Optimization Strategies"
    **Efficient Queries**
    
    - Filter by `OfficeStatus eq 'Active'` to get only current offices
    - Use `select` to limit fields when you don't need full office details
    - Order by `OfficeName` for alphabetical sorting
    
    **Common Patterns**
    
    ```python
    # Get essential office info only
    basic_offices = client.office.get_offices(
        filter_query="OfficeStatus eq 'Active'",
        select="OfficeKey,OfficeName,OfficeCity,OfficePhone",
        orderby="OfficeName asc"
    )
    
    # Search offices efficiently
    office_search = client.office.get_offices(
        filter_query="contains(tolower(OfficeName), 'realty')",
        select="OfficeKey,OfficeName,OfficeCity,OfficeStateOrProvince"
    )
    ```
    
    **Caching Considerations**
    
    - Office data changes infrequently
    - Cache office directories for extended periods
    - Use `ModificationTimestamp` to detect office information changes 