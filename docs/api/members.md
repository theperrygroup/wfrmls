# Members API

The Members API provides access to real estate agent and broker information, including contact details, office affiliations, and licensing data. Members represent the professionals in the MLS system who list and sell properties.

!!! example "Quick Start"
    ```python
    # Get active members (agents/brokers)
    members = client.member.get_active_members(top=50)
    
    # Get a specific member with office info
    member_detail = client.member.get_member_with_office("12345")
    
    # Search for members by name
    agents = client.member.get_members(
        filter_query="contains(MemberFirstName, 'John')",
        top=25
    )
    ```

## Member Client

::: wfrmls.member.MemberClient
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## Common Usage Patterns

### Basic Member Retrieval

=== "Active Members"
    ```python
    # Get all active members
    active_members = client.member.get_active_members(top=100)
    
    # Get active members ordered by last name
    members_by_name = client.member.get_active_members(
        orderby="MemberLastName asc",
        top=50
    )
    ```

=== "Member Details"
    ```python
    # Get a specific member by key
    member = client.member.get_member("12345")
    
    # Get member with office information
    member_with_office = client.member.get_member_with_office("12345")
    
    # Get member with full expansion
    member_expanded = client.member.get_member_with_expansion(
        member_key="12345",
        expand="Office,Property"
    )
    ```

=== "Member Search"
    ```python
    # Search by name
    johns = client.member.get_members(
        filter_query="contains(MemberFirstName, 'John')",
        top=25
    )
    
    # Search by last name
    smiths = client.member.get_members(
        filter_query="contains(MemberLastName, 'Smith')",
        orderby="MemberFirstName asc"
    )
    ```

### Advanced Filtering

=== "Office Affiliation"
    ```python
    # Members from specific office
    office_members = client.member.get_members(
        filter_query="MemberOfficeKey eq '67890'",
        orderby="MemberLastName asc"
    )
    
    # Members with office information
    members_with_offices = client.member.get_members_with_office(
        filter_query="MemberStatus eq 'Active'",
        top=100
    )
    ```

=== "License and Status"
    ```python
    # Active licensed agents
    licensed_agents = client.member.get_members(
        filter_query="MemberStatus eq 'Active' and MemberStateLicense ne null",
        select="MemberKey,MemberFirstName,MemberLastName,MemberStateLicense,MemberType"
    )
    
    # Brokers only
    brokers = client.member.get_members(
        filter_query="MemberType eq 'Broker'",
        orderby="MemberLastName asc"
    )
    ```

=== "Contact Information"
    ```python
    # Members with email addresses
    members_with_email = client.member.get_members(
        filter_query="MemberEmail ne null",
        select="MemberKey,MemberFirstName,MemberLastName,MemberEmail"
    )
    
    # Members with direct phone numbers
    members_with_phone = client.member.get_members(
        filter_query="MemberDirectPhone ne null",
        select="MemberKey,MemberFirstName,MemberLastName,MemberDirectPhone"
    )
    ```

## Member Data Structure

Members in WFRMLS follow the RESO standard with comprehensive professional information:

??? info "Key Member Fields"
    **Identification**
    
    - `MemberKey` - Unique member identifier
    - `MemberMlsId` - MLS-specific member ID
    - `MemberNationalAssociationId` - National association ID
    - `MemberStateLicense` - State license number

    **Personal Information**
    
    - `MemberFirstName`, `MemberLastName` - Agent's name
    - `MemberFullName` - Complete name
    - `MemberNickname` - Preferred name
    - `MemberPreferredFirstName` - Preferred first name

    **Contact Details**
    
    - `MemberEmail` - Primary email address
    - `MemberDirectPhone` - Direct phone number
    - `MemberMobilePhone` - Mobile phone number
    - `MemberOfficePhone` - Office phone number
    - `MemberFax` - Fax number

    **Professional Information**
    
    - `MemberType` - Agent, Broker, Assistant, etc.
    - `MemberStatus` - Active, Inactive, Suspended, etc.
    - `MemberDesignation` - Professional designations (CRS, GRI, etc.)
    - `MemberOfficeKey` - Associated office identifier

    **System Information**
    
    - `ModificationTimestamp` - Last update time
    - `MemberLoginId` - Login identifier
    - `OriginalEntryTimestamp` - Initial creation time

## Integration Examples

### Agent Directory

```python
def create_agent_directory(client, office_key=None):
    """Create a directory of active agents."""
    
    # Build filter for active agents
    filters = ["MemberStatus eq 'Active'", "MemberType eq 'Agent'"]
    
    if office_key:
        filters.append(f"MemberOfficeKey eq '{office_key}'")
    
    filter_query = " and ".join(filters)
    
    # Get agents with office information
    agents = client.member.get_members_with_office(
        filter_query=filter_query,
        select="MemberKey,MemberFirstName,MemberLastName,MemberEmail,MemberDirectPhone,OfficeKey,OfficeName",
        orderby="MemberLastName asc, MemberFirstName asc",
        top=500
    )
    
    # Organize by office
    directory = {}
    for agent in agents.get('value', []):
        office_name = agent.get('OfficeName', 'Unknown Office')
        if office_name not in directory:
            directory[office_name] = []
        
        directory[office_name].append({
            'name': f"{agent.get('MemberFirstName', '')} {agent.get('MemberLastName', '')}".strip(),
            'email': agent.get('MemberEmail'),
            'phone': agent.get('MemberDirectPhone'),
            'member_key': agent.get('MemberKey')
        })
    
    return directory

# Usage
agent_directory = create_agent_directory(client)
for office, agents in agent_directory.items():
    print(f"\n🏢 {office} ({len(agents)} agents)")
    for agent in agents[:5]:  # Show first 5 agents
        print(f"   👤 {agent['name']} - {agent['email']}")
```

### Top Producers Report

```python
def get_top_producers(client, days_back=30):
    """Get top producing agents based on recent listings."""
    
    from datetime import datetime, timedelta
    cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Get recent listings with agent info
    recent_listings = client.property.get_properties(
        filter_query=f"ListingContractDate ge {cutoff_date}",
        select="ListingId,ListAgentKey,ListPrice,ListingContractDate",
        top=1000
    )
    
    # Count listings per agent
    agent_stats = {}
    for listing in recent_listings.get('value', []):
        agent_key = listing.get('ListAgentKey')
        if agent_key:
            if agent_key not in agent_stats:
                agent_stats[agent_key] = {
                    'listing_count': 0,
                    'total_volume': 0,
                    'avg_price': 0
                }
            
            agent_stats[agent_key]['listing_count'] += 1
            list_price = listing.get('ListPrice', 0)
            agent_stats[agent_key]['total_volume'] += list_price
    
    # Calculate averages and get agent details
    top_producers = []
    for agent_key, stats in agent_stats.items():
        if stats['listing_count'] >= 2:  # Minimum 2 listings
            stats['avg_price'] = stats['total_volume'] / stats['listing_count']
            
            # Get agent details
            try:
                agent_detail = client.member.get_member_with_office(agent_key)
                if agent_detail:
                    top_producers.append({
                        'agent_key': agent_key,
                        'name': f"{agent_detail.get('MemberFirstName', '')} {agent_detail.get('MemberLastName', '')}".strip(),
                        'office': agent_detail.get('OfficeName', 'Unknown'),
                        'listings': stats['listing_count'],
                        'volume': stats['total_volume'],
                        'avg_price': stats['avg_price']
                    })
            except:
                continue
    
    # Sort by listing count
    top_producers.sort(key=lambda x: x['listings'], reverse=True)
    return top_producers[:20]  # Top 20

# Usage
top_agents = get_top_producers(client, days_back=30)
print("🏆 Top Producers (Last 30 Days)")
for i, agent in enumerate(top_agents, 1):
    print(f"{i:2d}. {agent['name']} ({agent['office']})")
    print(f"    📋 {agent['listings']} listings | 💰 ${agent['volume']:,.0f} volume | 📊 ${agent['avg_price']:,.0f} avg")
```

### Member Contact Validation

```python
def validate_member_contacts(client, office_key=None):
    """Validate member contact information completeness."""
    
    # Get members with contact fields
    filter_query = "MemberStatus eq 'Active'"
    if office_key:
        filter_query += f" and MemberOfficeKey eq '{office_key}'"
    
    members = client.member.get_members(
        filter_query=filter_query,
        select="MemberKey,MemberFirstName,MemberLastName,MemberEmail,MemberDirectPhone,MemberMobilePhone",
        top=500
    )
    
    validation_report = {
        'total_members': 0,
        'missing_email': [],
        'missing_phone': [],
        'complete_profiles': 0
    }
    
    for member in members.get('value', []):
        validation_report['total_members'] += 1
        
        name = f"{member.get('MemberFirstName', '')} {member.get('MemberLastName', '')}".strip()
        email = member.get('MemberEmail')
        direct_phone = member.get('MemberDirectPhone')
        mobile_phone = member.get('MemberMobilePhone')
        
        missing_info = []
        
        if not email:
            missing_info.append('email')
            validation_report['missing_email'].append(name)
        
        if not direct_phone and not mobile_phone:
            missing_info.append('phone')
            validation_report['missing_phone'].append(name)
        
        if not missing_info:
            validation_report['complete_profiles'] += 1
    
    return validation_report

# Usage
contact_report = validate_member_contacts(client)
print(f"📊 Contact Validation Report")
print(f"   Total Active Members: {contact_report['total_members']}")
print(f"   Complete Profiles: {contact_report['complete_profiles']} ({contact_report['complete_profiles']/contact_report['total_members']*100:.1f}%)")
print(f"   Missing Email: {len(contact_report['missing_email'])} members")
print(f"   Missing Phone: {len(contact_report['missing_phone'])} members")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    # Try to get a member
    member = client.member.get_member("12345")
    
except NotFoundError:
    print("❌ Member not found - the member key may be incorrect or the member may be inactive")
    
except ValidationError as e:
    print(f"📝 Invalid search parameters: {e}")
    
except Exception as e:
    print(f"🚨 Unexpected error: {e}")
```

## Performance Tips

!!! tip "Optimization Strategies"
    **Efficient Queries**
    
    - Filter by `MemberStatus eq 'Active'` to get only current members
    - Use `select` to limit fields when you don't need full member details
    - Order by `MemberLastName` for alphabetical sorting
    
    **Common Patterns**
    
    ```python
    # Get essential member info only
    basic_members = client.member.get_members(
        filter_query="MemberStatus eq 'Active'",
        select="MemberKey,MemberFirstName,MemberLastName,MemberEmail",
        orderby="MemberLastName asc"
    )
    
    # Search members efficiently
    member_search = client.member.get_members(
        filter_query="contains(tolower(MemberLastName), 'smith')",
        select="MemberKey,MemberFirstName,MemberLastName,MemberOfficeKey"
    )
    ```
    
    **Caching Considerations**
    
    - Member data changes less frequently than property data
    - Cache member details for frequently accessed agents
    - Use `ModificationTimestamp` to detect member profile changes 