# Deleted Records API

The Deleted Records API provides access to records that have been removed from the WFRMLS system. This is essential for maintaining data synchronization and tracking changes in external systems.

## Overview

The `DeletedClient` class handles all deleted record operations, providing methods to retrieve and track deleted records across different resource types.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="your_token")
deleted_properties = client.deleted.get_deleted_records("Property")
```

## Quick Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `get_deleted_records()` | Get deleted records for a resource type | `List[Dict[str, Any]]` |
| `get_deleted_since()` | Get records deleted since a specific date | `List[Dict[str, Any]]` |
| `get_all_deleted()` | Get all deleted records across all resources | `Dict[str, List[Dict[str, Any]]]` |

## Methods

### get_deleted_records()

Retrieve deleted records for a specific resource type.

```python
def get_deleted_records(
    self,
    resource_name: ResourceName,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resource_name` | `ResourceName` | Yes | Type of resource (Property, Member, Office, etc.) |
| `date_from` | `datetime` | No | Start date for deletion period |
| `date_to` | `datetime` | No | End date for deletion period |
| `top` | `int` | No | Maximum number of records to return |
| `skip` | `int` | No | Number of records to skip |

#### Examples

=== "Basic Usage"

    ```python
    from wfrmls import ResourceName
    
    # Get deleted properties
    deleted_properties = client.deleted.get_deleted_records(
        ResourceName.PROPERTY,
        top=100
    )
    
    for record in deleted_properties:
        print(f"Deleted Property: {record['ResourceRecordKey']} on {record['DeletedDateTime']}")
    ```

=== "Date Range Filtering"

    ```python
    from datetime import datetime, timedelta
    
    # Get properties deleted in the last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_deletions = client.deleted.get_deleted_records(
        ResourceName.PROPERTY,
        date_from=week_ago
    )
    
    print(f"Found {len(recent_deletions)} properties deleted in the last week")
    ```

=== "Multiple Resource Types"

    ```python
    # Get deleted records for different resource types
    resource_types = [
        ResourceName.PROPERTY,
        ResourceName.MEMBER,
        ResourceName.OFFICE,
        ResourceName.OPENHOUSE
    ]
    
    for resource_type in resource_types:
        deleted = client.deleted.get_deleted_records(resource_type, top=10)
        print(f"{resource_type}: {len(deleted)} deleted records")
    ```

### get_deleted_since()

Retrieve all deleted records since a specific timestamp across all resource types.

```python
def get_deleted_since(
    self,
    since_datetime: datetime,
    resource_name: Optional[ResourceName] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `since_datetime` | `datetime` | Yes | Timestamp to check deletions since |
| `resource_name` | `ResourceName` | No | Specific resource type (optional) |

#### Example

```python
from datetime import datetime, timedelta

# Get all deletions since yesterday
yesterday = datetime.now() - timedelta(days=1)
recent_deletions = client.deleted.get_deleted_since(yesterday)

# Group by resource type
deletions_by_type = {}
for record in recent_deletions:
    resource_type = record['ResourceName']
    if resource_type not in deletions_by_type:
        deletions_by_type[resource_type] = []
    deletions_by_type[resource_type].append(record)

for resource_type, records in deletions_by_type.items():
    print(f"{resource_type}: {len(records)} deletions")
```

### get_all_deleted()

Retrieve deleted records for all resource types.

```python
def get_all_deleted(
    self,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    **kwargs
) -> Dict[str, List[Dict[str, Any]]]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | `datetime` | No | Start date for deletion period |
| `date_to` | `datetime` | No | End date for deletion period |

#### Example

```python
# Get all deleted records from the last month
last_month = datetime.now() - timedelta(days=30)
all_deletions = client.deleted.get_all_deleted(date_from=last_month)

print("Deletion Summary:")
for resource_type, records in all_deletions.items():
    print(f"  {resource_type}: {len(records)} records")
```

## Enums and Constants

### ResourceName

Enumeration of available resource types:

```python
from wfrmls import ResourceName

class ResourceName(str, Enum):
    PROPERTY = "Property"
    MEMBER = "Member"
    OFFICE = "Office"
    OPENHOUSE = "OpenHouse"
    MEDIA = "Media"
    HISTORY = "History"
    ADU = "Adu"
    LOOKUP = "Lookup"
```

## Common Use Cases

### Data Synchronization

```python
# Synchronize deleted records with external system
def sync_deleted_records(last_sync_time: datetime):
    """Sync deleted records since last synchronization."""
    
    # Get all deletions since last sync
    deleted_records = client.deleted.get_deleted_since(last_sync_time)
    
    # Group by resource type for processing
    deletions_by_type = {}
    for record in deleted_records:
        resource_type = record['ResourceName']
        if resource_type not in deletions_by_type:
            deletions_by_type[resource_type] = []
        deletions_by_type[resource_type].append(record)
    
    # Process each resource type
    sync_results = {}
    for resource_type, records in deletions_by_type.items():
        try:
            # Delete from external system
            deleted_count = delete_from_external_system(resource_type, records)
            sync_results[resource_type] = {
                "success": True,
                "deleted_count": deleted_count,
                "records": len(records)
            }
        except Exception as e:
            sync_results[resource_type] = {
                "success": False,
                "error": str(e),
                "records": len(records)
            }
    
    return sync_results

def delete_from_external_system(resource_type: str, records: List[Dict]):
    """Delete records from external system (implement based on your system)."""
    deleted_count = 0
    
    for record in records:
        record_key = record['ResourceRecordKey']
        
        # Example: Delete from database
        # db.execute(f"DELETE FROM {resource_type} WHERE id = ?", (record_key,))
        
        # Example: Delete from search index
        # search_index.delete(resource_type, record_key)
        
        deleted_count += 1
        print(f"Deleted {resource_type} record: {record_key}")
    
    return deleted_count

# Usage
last_sync = datetime(2024, 1, 1, 12, 0, 0)  # Your last sync timestamp
sync_results = sync_deleted_records(last_sync)
```

### Cleanup Operations

```python
# Clean up orphaned data based on deletions
def cleanup_orphaned_data():
    """Clean up data that references deleted records."""
    
    # Get recent deletions
    week_ago = datetime.now() - timedelta(days=7)
    
    # Check for deleted properties
    deleted_properties = client.deleted.get_deleted_records(
        ResourceName.PROPERTY,
        date_from=week_ago
    )
    
    # Clean up related data
    cleanup_results = {
        "deleted_properties": len(deleted_properties),
        "cleaned_photos": 0,
        "cleaned_favorites": 0,
        "cleaned_searches": 0
    }
    
    for property_record in deleted_properties:
        property_id = property_record['ResourceRecordKey']
        
        # Clean up photos
        # photos_deleted = cleanup_property_photos(property_id)
        # cleanup_results["cleaned_photos"] += photos_deleted
        
        # Clean up user favorites
        # favorites_deleted = cleanup_user_favorites(property_id)
        # cleanup_results["cleaned_favorites"] += favorites_deleted
        
        # Clean up saved searches
        # searches_updated = update_saved_searches(property_id)
        # cleanup_results["cleaned_searches"] += searches_updated
    
    return cleanup_results

cleanup_results = cleanup_orphaned_data()
print(f"Cleanup completed: {cleanup_results}")
```

### Audit Trail

```python
# Create audit trail of deletions
def create_deletion_audit_trail(days_back: int = 30):
    """Create an audit trail of all deletions."""
    
    start_date = datetime.now() - timedelta(days=days_back)
    all_deletions = client.deleted.get_all_deleted(date_from=start_date)
    
    audit_trail = []
    
    for resource_type, records in all_deletions.items():
        for record in records:
            audit_entry = {
                "resource_type": resource_type,
                "record_key": record['ResourceRecordKey'],
                "deleted_datetime": record['DeletedDateTime'],
                "deleted_by": record.get('DeletedBy', 'Unknown'),
                "deletion_reason": record.get('DeletionReason', 'Not specified')
            }
            audit_trail.append(audit_entry)
    
    # Sort by deletion time
    audit_trail.sort(key=lambda x: x['deleted_datetime'], reverse=True)
    
    return audit_trail

# Generate audit report
audit_trail = create_deletion_audit_trail(30)

print(f"Deletion Audit Trail (Last 30 Days):")
print(f"Total Deletions: {len(audit_trail)}")

# Group by resource type
by_type = {}
for entry in audit_trail:
    resource_type = entry['resource_type']
    if resource_type not in by_type:
        by_type[resource_type] = 0
    by_type[resource_type] += 1

print("\nDeletions by Resource Type:")
for resource_type, count in sorted(by_type.items()):
    print(f"  {resource_type}: {count}")
```

## Field Reference

### Standard Fields

| Field | Type | Description |
|-------|------|-------------|
| `ResourceName` | `str` | Type of resource that was deleted |
| `ResourceRecordKey` | `str` | Unique identifier of the deleted record |
| `DeletedDateTime` | `datetime` | When the record was deleted |
| `DeletedBy` | `str` | User or system that deleted the record |

### Extended Fields

| Field | Type | Description |
|-------|------|-------------|
| `DeletionReason` | `str` | Reason for deletion |
| `OriginalEntryTimestamp` | `datetime` | When the record was originally created |
| `LastModificationTimestamp` | `datetime` | Last modification before deletion |

## Advanced Usage

### Incremental Sync Pattern

```python
import json
from pathlib import Path

class DeletionSyncManager:
    def __init__(self, client, sync_state_file="deletion_sync_state.json"):
        self.client = client
        self.sync_state_file = Path(sync_state_file)
        self.load_sync_state()
    
    def load_sync_state(self):
        """Load the last sync timestamp from file."""
        if self.sync_state_file.exists():
            with open(self.sync_state_file, 'r') as f:
                state = json.load(f)
                self.last_sync = datetime.fromisoformat(state['last_sync'])
        else:
            # First sync - start from 30 days ago
            self.last_sync = datetime.now() - timedelta(days=30)
    
    def save_sync_state(self):
        """Save the current sync timestamp to file."""
        state = {
            'last_sync': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        with open(self.sync_state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def sync_deletions(self):
        """Perform incremental sync of deletions."""
        print(f"Syncing deletions since: {self.last_sync}")
        
        # Get deletions since last sync
        deleted_records = self.client.deleted.get_deleted_since(self.last_sync)
        
        if not deleted_records:
            print("No new deletions found")
            return {"total_processed": 0}
        
        # Process deletions
        processed = 0
        errors = []
        
        for record in deleted_records:
            try:
                self.process_deletion(record)
                processed += 1
            except Exception as e:
                errors.append({
                    "record": record['ResourceRecordKey'],
                    "error": str(e)
                })
        
        # Update sync state
        self.save_sync_state()
        
        result = {
            "total_processed": processed,
            "errors": errors,
            "sync_timestamp": datetime.now().isoformat()
        }
        
        print(f"Sync completed: {processed} records processed, {len(errors)} errors")
        return result
    
    def process_deletion(self, record):
        """Process a single deletion record."""
        resource_type = record['ResourceName']
        record_key = record['ResourceRecordKey']
        
        print(f"Processing deletion: {resource_type} {record_key}")
        
        # Implement your deletion logic here
        # Example: Remove from database, search index, cache, etc.
        pass

# Usage
sync_manager = DeletionSyncManager(client)
sync_result = sync_manager.sync_deletions()
```

### Deletion Monitoring

```python
# Monitor deletion patterns for anomalies
def monitor_deletion_patterns():
    """Monitor for unusual deletion patterns."""
    
    # Get deletions from last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    recent_deletions = client.deleted.get_deleted_since(yesterday)
    
    # Analyze patterns
    analysis = {
        "total_deletions": len(recent_deletions),
        "by_resource_type": {},
        "by_hour": {},
        "unusual_patterns": []
    }
    
    # Group by resource type
    for record in recent_deletions:
        resource_type = record['ResourceName']
        if resource_type not in analysis["by_resource_type"]:
            analysis["by_resource_type"][resource_type] = 0
        analysis["by_resource_type"][resource_type] += 1
        
        # Group by hour
        hour = datetime.fromisoformat(record['DeletedDateTime']).hour
        if hour not in analysis["by_hour"]:
            analysis["by_hour"][hour] = 0
        analysis["by_hour"][hour] += 1
    
    # Check for unusual patterns
    total = analysis["total_deletions"]
    
    # Alert if too many deletions
    if total > 1000:  # Threshold
        analysis["unusual_patterns"].append(
            f"High deletion volume: {total} records in 24 hours"
        )
    
    # Alert if one resource type dominates
    for resource_type, count in analysis["by_resource_type"].items():
        if count > total * 0.8:  # 80% of all deletions
            analysis["unusual_patterns"].append(
                f"High {resource_type} deletion rate: {count}/{total} records"
            )
    
    return analysis

# Run monitoring
patterns = monitor_deletion_patterns()
if patterns["unusual_patterns"]:
    print("⚠️  Unusual deletion patterns detected:")
    for pattern in patterns["unusual_patterns"]:
        print(f"  - {pattern}")
```

## Error Handling

```python
from wfrmls.exceptions import NotFoundError, ValidationError

try:
    deleted_records = client.deleted.get_deleted_records(
        ResourceName.PROPERTY,
        date_from=datetime.now() - timedelta(days=1)
    )
except ValidationError as e:
    print(f"Invalid request: {e}")
except Exception as e:
    print(f"Error retrieving deleted records: {e}")
```

## Best Practices

### Performance Optimization

1. **Use date ranges** to limit result sets
2. **Process deletions in batches** for large volumes
3. **Cache deletion state** to avoid reprocessing
4. **Use pagination** for large deletion sets

### Data Integrity

1. **Verify record existence** before deletion processing
2. **Handle cascading deletions** appropriately
3. **Maintain referential integrity** in external systems
4. **Log all deletion operations** for audit purposes

### Synchronization

1. **Track sync timestamps** accurately
2. **Handle clock skew** between systems
3. **Implement retry logic** for failed deletions
4. **Validate sync completeness** regularly

## Related Resources

- [Properties API](properties.md) - For property data
- [Members API](members.md) - For member data
- [Error Handling Guide](../guides/error-handling.md) - Exception management
- [Data Synchronization Guide](../guides/data-sync.md) - Sync strategies