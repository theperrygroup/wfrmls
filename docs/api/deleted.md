# Deleted API

Complete reference for the Deleted endpoint of the WFRMLS Python client.

---

## 🗑️ Overview

The Deleted API provides access to records that have been deleted from the MLS system. This endpoint is crucial for maintaining data synchronization and tracking removed listings, members, offices, and other resources.

### Key Features

- **Deletion tracking** - Monitor removed records across all resources
- **Timestamp filtering** - Find deletions within specific time ranges
- **Resource identification** - Identify what type of record was deleted
- **Synchronization support** - Keep local databases in sync
- **Audit trail** - Track when records were removed

---

## 📚 Methods

### `get_deleted()`

Retrieve deleted record information with optional filtering and pagination.

```python
def get_deleted(
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
| `orderby` | `Optional[str]` | `None` | Field(s) to sort by (use 'ts' for timestamp) |
| `count` | `bool` | `False` | Include total count in response metadata |

**Returns:**
- `Dict[str, Any]` - Response dictionary with deleted record data

**Examples:**

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()

# Get recent deletions
deletions = client.deleted.get_deleted(top=10)

# Get deletions for specific resource type
property_deletions = client.deleted.get_deleted(
    filter_query="resource eq 'Property'"
)

# Get deletions after a specific date
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
recent_deletions = client.deleted.get_deleted(
    filter_query=f"ts gt {yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')}"
)
```

### `get_recent_deletions()`

Get deletions from the last N days.

```python
def get_recent_deletions(
    days: int = 7,
    resource_type: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days` | `int` | `7` | Number of days to look back |
| `resource_type` | `Optional[str]` | `None` | Filter by resource type |

**Returns:**
- `Dict[str, Any]` - Recent deletion records

**Examples:**

```python
# Get deletions from last 7 days
recent = client.deleted.get_recent_deletions()

# Get property deletions from last 30 days
property_deletions = client.deleted.get_recent_deletions(
    days=30,
    resource_type="Property"
)
```

### `get_deletions_by_resource()`

Get all deletions for a specific resource type.

```python
def get_deletions_by_resource(
    resource_type: str,
    top: Optional[int] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Description |
|----------|------|-------------|
| `resource_type` | `str` | Resource type (e.g., "Property", "Member") |
| `top` | `Optional[int]` | Maximum number of results |

**Returns:**
- `Dict[str, Any]` - Deletions for the specified resource

---

## 🏷️ Field Reference

Each deleted record contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **resource** | `string` | Type of deleted resource | `"OpenHouse"` |
| **primary_key** | `string` | ID of deleted record | `"337211"` |
| **ts** | `datetime` | Deletion timestamp | `"2020-07-30T08:55:07Z"` |

**Important Note:** The timestamp field is named `ts`, not `ModificationTimestamp` or `DeletedTimestamp`.

---

## 🔍 Common Usage Patterns

### Synchronization Process

```python
from datetime import datetime, timedelta

def sync_deletions(last_sync_time: datetime):
    """Synchronize deletions since last sync."""
    
    # Format timestamp for filter
    sync_time_str = last_sync_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Get all deletions since last sync
    deletions = client.deleted.get_deleted(
        filter_query=f"ts gt {sync_time_str}",
        orderby="ts asc"
    )
    
    # Group by resource type
    deleted_by_type = {}
    
    for deletion in deletions["value"]:
        resource_type = deletion["resource"]
        if resource_type not in deleted_by_type:
            deleted_by_type[resource_type] = []
        
        deleted_by_type[resource_type].append({
            "id": deletion["primary_key"],
            "deleted_at": deletion["ts"]
        })
    
    # Process deletions
    sync_results = {
        "sync_time": datetime.now(),
        "total_deletions": len(deletions["value"]),
        "by_resource": {}
    }
    
    for resource_type, records in deleted_by_type.items():
        sync_results["by_resource"][resource_type] = {
            "count": len(records),
            "ids": [r["id"] for r in records]
        }
        
        # Here you would actually delete from your database
        # delete_from_database(resource_type, records)
    
    return sync_results

# Sync deletions from last hour
last_sync = datetime.now() - timedelta(hours=1)
sync_result = sync_deletions(last_sync)
```

### Audit Trail Creation

```python
def create_deletion_audit_trail(days_back: int = 30):
    """Create an audit trail of deletions."""
    
    # Calculate start date
    start_date = datetime.now() - timedelta(days=days_back)
    
    # Get all deletions
    deletions = client.deleted.get_deleted(
        filter_query=f"ts gt {start_date.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        orderby="ts desc"
    )
    
    # Create audit entries
    audit_trail = []
    
    for deletion in deletions["value"]:
        # Parse timestamp
        deleted_at = datetime.fromisoformat(deletion["ts"].replace("Z", "+00:00"))
        
        audit_entry = {
            "timestamp": deleted_at.isoformat(),
            "action": "DELETE",
            "resource_type": deletion["resource"],
            "resource_id": deletion["primary_key"],
            "date": deleted_at.date().isoformat(),
            "time": deleted_at.time().isoformat()
        }
        
        audit_trail.append(audit_entry)
    
    # Group by date for summary
    deletions_by_date = {}
    for entry in audit_trail:
        date = entry["date"]
        if date not in deletions_by_date:
            deletions_by_date[date] = {
                "total": 0,
                "by_resource": {}
            }
        
        deletions_by_date[date]["total"] += 1
        
        resource = entry["resource_type"]
        if resource not in deletions_by_date[date]["by_resource"]:
            deletions_by_date[date]["by_resource"][resource] = 0
        deletions_by_date[date]["by_resource"][resource] += 1
    
    return {
        "audit_trail": audit_trail,
        "summary_by_date": deletions_by_date
    }

# Create audit trail
audit = create_deletion_audit_trail(days_back=7)
```

### Monitoring Deletions

```python
def monitor_deletion_activity():
    """Monitor deletion patterns and anomalies."""
    
    # Get recent deletions
    recent = client.deleted.get_deleted(top=100, orderby="ts desc")
    
    if not recent["value"]:
        return {"status": "No recent deletions"}
    
    # Analyze patterns
    analysis = {
        "total_recent": len(recent["value"]),
        "by_resource": {},
        "time_range": {
            "oldest": None,
            "newest": None
        },
        "deletion_rate": {}
    }
    
    # Parse timestamps
    timestamps = []
    for deletion in recent["value"]:
        resource = deletion["resource"]
        timestamp = datetime.fromisoformat(deletion["ts"].replace("Z", "+00:00"))
        timestamps.append(timestamp)
        
        if resource not in analysis["by_resource"]:
            analysis["by_resource"][resource] = {
                "count": 0,
                "recent_ids": []
            }
        
        analysis["by_resource"][resource]["count"] += 1
        if len(analysis["by_resource"][resource]["recent_ids"]) < 5:
            analysis["by_resource"][resource]["recent_ids"].append(
                deletion["primary_key"]
            )
    
    # Time range
    if timestamps:
        analysis["time_range"]["oldest"] = min(timestamps).isoformat()
        analysis["time_range"]["newest"] = max(timestamps).isoformat()
        
        # Calculate deletion rate
        time_span = max(timestamps) - min(timestamps)
        if time_span.total_seconds() > 0:
            hours = time_span.total_seconds() / 3600
            analysis["deletion_rate"]["per_hour"] = round(
                len(timestamps) / hours, 2
            )
    
    # Flag anomalies
    analysis["anomalies"] = []
    
    # Check for mass deletions
    for resource, data in analysis["by_resource"].items():
        if data["count"] > 50:
            analysis["anomalies"].append({
                "type": "mass_deletion",
                "resource": resource,
                "count": data["count"]
            })
    
    return analysis

# Monitor deletions
monitoring_report = monitor_deletion_activity()
```

### Recovery Information

```python
def get_deletion_recovery_info(resource_type: str, record_id: str):
    """Get information about a specific deletion for recovery purposes."""
    
    # Search for the deletion
    result = client.deleted.get_deleted(
        filter_query=f"resource eq '{resource_type}' and primary_key eq '{record_id}'"
    )
    
    if result["value"]:
        deletion = result["value"][0]
        
        # Parse deletion time
        deleted_at = datetime.fromisoformat(
            deletion["ts"].replace("Z", "+00:00")
        )
        
        recovery_info = {
            "found": True,
            "resource_type": deletion["resource"],
            "record_id": deletion["primary_key"],
            "deleted_at": deleted_at.isoformat(),
            "deleted_ago": str(datetime.now(deleted_at.tzinfo) - deleted_at),
            "recovery_notes": []
        }
        
        # Add recovery suggestions based on age
        days_ago = (datetime.now(deleted_at.tzinfo) - deleted_at).days
        
        if days_ago < 7:
            recovery_info["recovery_notes"].append(
                "Recent deletion - may be recoverable through support"
            )
        elif days_ago < 30:
            recovery_info["recovery_notes"].append(
                "Deletion within 30 days - contact support for options"
            )
        else:
            recovery_info["recovery_notes"].append(
                "Deletion over 30 days old - recovery unlikely"
            )
        
        return recovery_info
    
    return {
        "found": False,
        "resource_type": resource_type,
        "record_id": record_id,
        "message": "No deletion record found"
    }

# Check deletion info
recovery = get_deletion_recovery_info("Property", "12345")
```

### Batch Cleanup

```python
def process_deletion_batch(batch_size: int = 100):
    """Process deletions in batches for cleanup."""
    
    processed = 0
    has_more = True
    
    while has_more:
        # Get next batch
        batch = client.deleted.get_deleted(
            top=batch_size,
            skip=processed,
            orderby="ts asc"
        )
        
        if not batch["value"]:
            has_more = False
            break
        
        # Process batch
        for deletion in batch["value"]:
            # Your cleanup logic here
            print(f"Processing deletion: {deletion['resource']} - {deletion['primary_key']}")
            
            # Example: Remove from cache, update indexes, etc.
            # cleanup_record(deletion['resource'], deletion['primary_key'])
        
        processed += len(batch["value"])
        
        # Check if we have more
        if len(batch["value"]) < batch_size:
            has_more = False
        
        # Add delay to avoid overwhelming the system
        time.sleep(0.1)
    
    return {
        "total_processed": processed,
        "status": "completed"
    }

# Process deletions
cleanup_result = process_deletion_batch()
```

---

## ⚡ Performance Tips

1. **Use timestamp filtering** - Always filter by `ts` to limit results
2. **Implement pagination** - Process large deletion sets in batches
3. **Cache deletion data** - Store processed deletions to avoid reprocessing
4. **Index by resource type** - Organize deletions by resource for efficiency
5. **Regular cleanup** - Process deletions regularly to avoid large backlogs

---

## 🚨 Important Notes

- The timestamp field is `ts`, not `ModificationTimestamp`
- Deletion records are typically retained for a limited time (varies by MLS)
- Primary keys may be reused after deletion
- Not all resource types may appear in deletion records
- Always handle pagination for large deletion sets
- Consider implementing retry logic for synchronization