# Data Synchronization

This guide covers strategies and best practices for synchronizing data between the WFRMLS API and your local systems, including incremental updates, change tracking, and conflict resolution.

## Overview

Data synchronization is crucial for maintaining up-to-date information in your applications. The WFRMLS API provides several mechanisms to help you efficiently sync data:

- **Incremental updates** using modification timestamps
- **Deleted record tracking** for cleanup operations
- **Change detection** for conflict resolution
- **Batch processing** for efficient data transfer

## Synchronization Strategies

### Full Synchronization

Complete data refresh - useful for initial setup or recovery.

```python
from wfrmls import WFRMLSClient
from datetime import datetime
import json

class FullSyncManager:
    def __init__(self, client, local_storage):
        self.client = client
        self.storage = local_storage
    
    def full_sync_properties(self):
        """Perform a complete property synchronization."""
        
        print("Starting full property synchronization...")
        
        # Clear existing data
        self.storage.clear_properties()
        
        # Fetch all properties in batches
        batch_size = 1000
        skip = 0
        total_synced = 0
        
        while True:
            properties = self.client.property.get_properties(
                select=[
                    "ListingId", "ListPrice", "StandardStatus", "PropertyType",
                    "UnparsedAddress", "City", "PostalCode", "Latitude", "Longitude",
                    "ModificationTimestamp", "OriginalEntryTimestamp"
                ],
                top=batch_size,
                skip=skip,
                orderby="ListingId asc"
            )
            
            if not properties:
                break
            
            # Store batch
            self.storage.store_properties(properties)
            total_synced += len(properties)
            skip += batch_size
            
            print(f"Synced {total_synced} properties...")
            
            # Break if we got less than batch size (last batch)
            if len(properties) < batch_size:
                break
        
        # Update sync metadata
        sync_info = {
            "type": "full_sync",
            "timestamp": datetime.now().isoformat(),
            "total_records": total_synced,
            "resource": "properties"
        }
        self.storage.update_sync_metadata(sync_info)
        
        print(f"Full sync completed: {total_synced} properties")
        return total_synced

# Usage
client = WFRMLSClient(bearer_token="your_token")
storage = LocalStorage()  # Your storage implementation
sync_manager = FullSyncManager(client, storage)
sync_manager.full_sync_properties()
```

### Incremental Synchronization

Sync only changed records since last update.

```python
from datetime import datetime, timedelta

class IncrementalSyncManager:
    def __init__(self, client, local_storage):
        self.client = client
        self.storage = local_storage
    
    def incremental_sync_properties(self):
        """Perform incremental property synchronization."""
        
        # Get last sync timestamp
        last_sync = self.storage.get_last_sync_timestamp("properties")
        if not last_sync:
            print("No previous sync found, performing full sync")
            return FullSyncManager(self.client, self.storage).full_sync_properties()
        
        print(f"Starting incremental sync since {last_sync}")
        
        # Get modified properties
        modified_properties = self.client.property.get_properties(
            filter_query=f"ModificationTimestamp gt {last_sync.isoformat()}Z",
            select=[
                "ListingId", "ListPrice", "StandardStatus", "PropertyType",
                "UnparsedAddress", "City", "PostalCode", "Latitude", "Longitude",
                "ModificationTimestamp", "OriginalEntryTimestamp"
            ],
            orderby="ModificationTimestamp asc"
        )
        
        # Get deleted properties
        deleted_properties = self.client.deleted.get_deleted_records(
            "Property",
            date_from=last_sync
        )
        
        # Process updates
        updated_count = 0
        if modified_properties:
            self.storage.upsert_properties(modified_properties)
            updated_count = len(modified_properties)
        
        # Process deletions
        deleted_count = 0
        if deleted_properties:
            deleted_ids = [record['ResourceRecordKey'] for record in deleted_properties]
            self.storage.delete_properties(deleted_ids)
            deleted_count = len(deleted_ids)
        
        # Update sync metadata
        sync_info = {
            "type": "incremental_sync",
            "timestamp": datetime.now().isoformat(),
            "last_sync": last_sync.isoformat(),
            "updated_records": updated_count,
            "deleted_records": deleted_count,
            "resource": "properties"
        }
        self.storage.update_sync_metadata(sync_info)
        
        print(f"Incremental sync completed: {updated_count} updated, {deleted_count} deleted")
        return {"updated": updated_count, "deleted": deleted_count}

# Usage
incremental_sync = IncrementalSyncManager(client, storage)
result = incremental_sync.incremental_sync_properties()
```

### Multi-Resource Synchronization

Sync multiple resource types efficiently.

```python
class MultiResourceSyncManager:
    def __init__(self, client, local_storage):
        self.client = client
        self.storage = local_storage
        
        # Define resources to sync
        self.resources = {
            "properties": {
                "client_method": self.client.property.get_properties,
                "select_fields": [
                    "ListingId", "ListPrice", "StandardStatus", "PropertyType",
                    "UnparsedAddress", "City", "ModificationTimestamp"
                ]
            },
            "members": {
                "client_method": self.client.member.get_members,
                "select_fields": [
                    "MemberKey", "MemberFirstName", "MemberLastName",
                    "MemberEmail", "MemberStatus", "ModificationTimestamp"
                ]
            },
            "offices": {
                "client_method": self.client.office.get_offices,
                "select_fields": [
                    "OfficeKey", "OfficeName", "OfficePhone",
                    "OfficeEmail", "OfficeStatus", "ModificationTimestamp"
                ]
            }
        }
    
    def sync_all_resources(self, incremental=True):
        """Sync all configured resources."""
        
        results = {}
        
        for resource_name, config in self.resources.items():
            print(f"Syncing {resource_name}...")
            
            try:
                if incremental:
                    result = self._incremental_sync_resource(resource_name, config)
                else:
                    result = self._full_sync_resource(resource_name, config)
                
                results[resource_name] = result
                
            except Exception as e:
                print(f"Error syncing {resource_name}: {e}")
                results[resource_name] = {"error": str(e)}
        
        return results
    
    def _incremental_sync_resource(self, resource_name, config):
        """Perform incremental sync for a single resource."""
        
        last_sync = self.storage.get_last_sync_timestamp(resource_name)
        
        if not last_sync:
            return self._full_sync_resource(resource_name, config)
        
        # Get modified records
        modified_records = config["client_method"](
            filter_query=f"ModificationTimestamp gt {last_sync.isoformat()}Z",
            select=config["select_fields"],
            orderby="ModificationTimestamp asc"
        )
        
        # Get deleted records
        deleted_records = self.client.deleted.get_deleted_records(
            resource_name.title(),  # Capitalize for API
            date_from=last_sync
        )
        
        # Process updates
        updated_count = 0
        if modified_records:
            getattr(self.storage, f"upsert_{resource_name}")(modified_records)
            updated_count = len(modified_records)
        
        # Process deletions
        deleted_count = 0
        if deleted_records:
            deleted_ids = [record['ResourceRecordKey'] for record in deleted_records]
            getattr(self.storage, f"delete_{resource_name}")(deleted_ids)
            deleted_count = len(deleted_ids)
        
        # Update sync metadata
        sync_info = {
            "type": "incremental_sync",
            "timestamp": datetime.now().isoformat(),
            "updated_records": updated_count,
            "deleted_records": deleted_count,
            "resource": resource_name
        }
        self.storage.update_sync_metadata(sync_info)
        
        return {"updated": updated_count, "deleted": deleted_count}
    
    def _full_sync_resource(self, resource_name, config):
        """Perform full sync for a single resource."""
        
        # Clear existing data
        getattr(self.storage, f"clear_{resource_name}")()
        
        # Fetch all records in batches
        batch_size = 1000
        skip = 0
        total_synced = 0
        
        while True:
            records = config["client_method"](
                select=config["select_fields"],
                top=batch_size,
                skip=skip,
                orderby=f"{config['select_fields'][0]} asc"  # Order by first field
            )
            
            if not records:
                break
            
            # Store batch
            getattr(self.storage, f"store_{resource_name}")(records)
            total_synced += len(records)
            skip += batch_size
            
            if len(records) < batch_size:
                break
        
        # Update sync metadata
        sync_info = {
            "type": "full_sync",
            "timestamp": datetime.now().isoformat(),
            "total_records": total_synced,
            "resource": resource_name
        }
        self.storage.update_sync_metadata(sync_info)
        
        return {"total": total_synced}

# Usage
multi_sync = MultiResourceSyncManager(client, storage)
results = multi_sync.sync_all_resources(incremental=True)

for resource, result in results.items():
    if "error" in result:
        print(f"{resource}: Error - {result['error']}")
    elif "updated" in result:
        print(f"{resource}: {result['updated']} updated, {result['deleted']} deleted")
    else:
        print(f"{resource}: {result['total']} total records")
```

## Change Detection and Conflict Resolution

### Timestamp-Based Change Detection

```python
class ChangeDetector:
    def __init__(self, client, local_storage):
        self.client = client
        self.storage = local_storage
    
    def detect_changes(self, resource_type, record_id):
        """Detect changes between local and remote records."""
        
        # Get local record
        local_record = self.storage.get_record(resource_type, record_id)
        if not local_record:
            return {"status": "local_missing", "action": "create_local"}
        
        # Get remote record
        try:
            if resource_type == "property":
                remote_record = self.client.property.get_property(record_id)
            elif resource_type == "member":
                remote_record = self.client.member.get_member(record_id)
            elif resource_type == "office":
                remote_record = self.client.office.get_office(record_id)
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
        
        except NotFoundError:
            return {"status": "remote_missing", "action": "delete_local"}
        
        # Compare modification timestamps
        local_modified = datetime.fromisoformat(local_record['ModificationTimestamp'])
        remote_modified = datetime.fromisoformat(remote_record['ModificationTimestamp'])
        
        if remote_modified > local_modified:
            return {
                "status": "remote_newer",
                "action": "update_local",
                "local_timestamp": local_modified,
                "remote_timestamp": remote_modified
            }
        elif local_modified > remote_modified:
            return {
                "status": "local_newer",
                "action": "check_local_changes",
                "local_timestamp": local_modified,
                "remote_timestamp": remote_modified
            }
        else:
            return {"status": "synchronized", "action": "none"}
    
    def resolve_conflicts(self, resource_type, record_id, resolution_strategy="remote_wins"):
        """Resolve conflicts between local and remote records."""
        
        change_info = self.detect_changes(resource_type, record_id)
        
        if change_info["action"] == "none":
            return {"action": "none", "message": "Records are synchronized"}
        
        if resolution_strategy == "remote_wins":
            if change_info["action"] in ["update_local", "create_local"]:
                # Update local with remote data
                if resource_type == "property":
                    remote_record = self.client.property.get_property(record_id)
                elif resource_type == "member":
                    remote_record = self.client.member.get_member(record_id)
                elif resource_type == "office":
                    remote_record = self.client.office.get_office(record_id)
                
                self.storage.upsert_record(resource_type, remote_record)
                return {"action": "updated_local", "message": "Local record updated with remote data"}
            
            elif change_info["action"] == "delete_local":
                self.storage.delete_record(resource_type, record_id)
                return {"action": "deleted_local", "message": "Local record deleted"}
        
        elif resolution_strategy == "manual":
            return {
                "action": "manual_review_required",
                "change_info": change_info,
                "message": "Manual review required for conflict resolution"
            }
        
        return change_info

# Usage
detector = ChangeDetector(client, storage)

# Check for changes
change_info = detector.detect_changes("property", "1611952")
print(f"Change status: {change_info['status']}")

# Resolve conflicts
resolution = detector.resolve_conflicts("property", "1611952", "remote_wins")
print(f"Resolution: {resolution['message']}")
```

### Field-Level Change Tracking

```python
class FieldChangeTracker:
    def __init__(self):
        self.tracked_fields = {
            "property": [
                "ListPrice", "StandardStatus", "PropertyType",
                "UnparsedAddress", "City", "PostalCode"
            ],
            "member": [
                "MemberFirstName", "MemberLastName", "MemberEmail",
                "MemberStatus", "MemberMobilePhone"
            ]
        }
    
    def compare_records(self, resource_type, local_record, remote_record):
        """Compare records field by field."""
        
        if resource_type not in self.tracked_fields:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        changes = {}
        fields_to_check = self.tracked_fields[resource_type]
        
        for field in fields_to_check:
            local_value = local_record.get(field)
            remote_value = remote_record.get(field)
            
            if local_value != remote_value:
                changes[field] = {
                    "local": local_value,
                    "remote": remote_value,
                    "changed": True
                }
        
        return {
            "has_changes": len(changes) > 0,
            "changed_fields": list(changes.keys()),
            "field_changes": changes,
            "total_changes": len(changes)
        }
    
    def generate_change_summary(self, resource_type, record_id, local_record, remote_record):
        """Generate a human-readable change summary."""
        
        comparison = self.compare_records(resource_type, local_record, remote_record)
        
        if not comparison["has_changes"]:
            return f"No changes detected for {resource_type} {record_id}"
        
        summary = [f"Changes detected for {resource_type} {record_id}:"]
        
        for field, change_info in comparison["field_changes"].items():
            summary.append(
                f"  {field}: '{change_info['local']}' → '{change_info['remote']}'"
            )
        
        return "\n".join(summary)

# Usage
tracker = FieldChangeTracker()

# Compare records
local_property = storage.get_record("property", "1611952")
remote_property = client.property.get_property("1611952")

comparison = tracker.compare_records("property", local_property, remote_property)

if comparison["has_changes"]:
    summary = tracker.generate_change_summary(
        "property", "1611952", local_property, remote_property
    )
    print(summary)
```

## Batch Processing and Performance

### Batch Update Manager

```python
class BatchUpdateManager:
    def __init__(self, client, local_storage, batch_size=100):
        self.client = client
        self.storage = local_storage
        self.batch_size = batch_size
    
    def batch_sync_properties(self, property_ids):
        """Sync multiple properties in batches."""
        
        total_processed = 0
        total_updated = 0
        errors = []
        
        # Process in batches
        for i in range(0, len(property_ids), self.batch_size):
            batch_ids = property_ids[i:i + self.batch_size]
            
            try:
                batch_result = self._process_property_batch(batch_ids)
                total_processed += batch_result["processed"]
                total_updated += batch_result["updated"]
                
                print(f"Processed batch {i//self.batch_size + 1}: "
                      f"{batch_result['processed']} properties, "
                      f"{batch_result['updated']} updated")
                
            except Exception as e:
                error_info = {
                    "batch_start": i,
                    "batch_ids": batch_ids,
                    "error": str(e)
                }
                errors.append(error_info)
                print(f"Error processing batch {i//self.batch_size + 1}: {e}")
        
        return {
            "total_processed": total_processed,
            "total_updated": total_updated,
            "errors": errors,
            "success_rate": total_processed / len(property_ids) if property_ids else 0
        }
    
    def _process_property_batch(self, property_ids):
        """Process a single batch of properties."""
        
        # Build filter for batch
        id_filter = " or ".join([f"ListingId eq '{pid}'" for pid in property_ids])
        
        # Fetch batch from API
        remote_properties = self.client.property.get_properties(
            filter_query=f"({id_filter})",
            select=[
                "ListingId", "ListPrice", "StandardStatus", "PropertyType",
                "UnparsedAddress", "City", "ModificationTimestamp"
            ]
        )
        
        # Get local properties for comparison
        local_properties = self.storage.get_properties_by_ids(property_ids)
        local_by_id = {prop['ListingId']: prop for prop in local_properties}
        
        # Process updates
        updates = []
        for remote_prop in remote_properties:
            listing_id = remote_prop['ListingId']
            local_prop = local_by_id.get(listing_id)
            
            if not local_prop:
                # New property
                updates.append(remote_prop)
            else:
                # Check if update needed
                remote_modified = datetime.fromisoformat(remote_prop['ModificationTimestamp'])
                local_modified = datetime.fromisoformat(local_prop['ModificationTimestamp'])
                
                if remote_modified > local_modified:
                    updates.append(remote_prop)
        
        # Apply updates
        if updates:
            self.storage.upsert_properties(updates)
        
        return {
            "processed": len(property_ids),
            "updated": len(updates),
            "found_remote": len(remote_properties)
        }

# Usage
batch_manager = BatchUpdateManager(client, storage, batch_size=50)

# Get list of property IDs to sync
property_ids = storage.get_all_property_ids()

# Process in batches
result = batch_manager.batch_sync_properties(property_ids)
print(f"Batch sync completed: {result['total_updated']} of {result['total_processed']} updated")
```

### Parallel Processing

```python
import concurrent.futures
from threading import Lock

class ParallelSyncManager:
    def __init__(self, client, local_storage, max_workers=5):
        self.client = client
        self.storage = local_storage
        self.max_workers = max_workers
        self.lock = Lock()
        self.stats = {"processed": 0, "updated": 0, "errors": 0}
    
    def parallel_sync_properties(self, property_ids, chunk_size=20):
        """Sync properties using parallel processing."""
        
        # Split into chunks
        chunks = [
            property_ids[i:i + chunk_size]
            for i in range(0, len(property_ids), chunk_size)
        ]
        
        print(f"Processing {len(property_ids)} properties in {len(chunks)} chunks")
        
        # Process chunks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chunk = {
                executor.submit(self._sync_property_chunk, chunk): chunk
                for chunk in chunks
            }
            
            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    result = future.result()
                    
                    with self.lock:
                        self.stats["processed"] += result["processed"]
                        self.stats["updated"] += result["updated"]
                    
                    print(f"Chunk completed: {result['processed']} processed, {result['updated']} updated")
                    
                except Exception as e:
                    with self.lock:
                        self.stats["errors"] += len(chunk)
                    
                    print(f"Chunk failed: {e}")
        
        return self.stats.copy()
    
    def _sync_property_chunk(self, property_ids):
        """Sync a chunk of properties."""
        
        # Create a new client instance for thread safety
        thread_client = WFRMLSClient(bearer_token=self.client.bearer_token)
        
        # Build filter for chunk
        id_filter = " or ".join([f"ListingId eq '{pid}'" for pid in property_ids])
        
        # Fetch from API
        remote_properties = thread_client.property.get_properties(
            filter_query=f"({id_filter})",
            select=[
                "ListingId", "ListPrice", "StandardStatus", "PropertyType",
                "ModificationTimestamp"
            ]
        )
        
        # Process updates (with thread-safe storage operations)
        updates = []
        for remote_prop in remote_properties:
            # Check if update needed (simplified for thread safety)
            updates.append(remote_prop)
        
        # Apply updates with lock
        if updates:
            with self.lock:
                self.storage.upsert_properties(updates)
        
        return {
            "processed": len(property_ids),
            "updated": len(updates)
        }

# Usage
parallel_sync = ParallelSyncManager(client, storage, max_workers=3)
property_ids = storage.get_all_property_ids()[:1000]  # Limit for example

result = parallel_sync.parallel_sync_properties(property_ids)
print(f"Parallel sync completed: {result}")
```

## Error Handling and Recovery

### Robust Sync with Retry Logic

```python
import time
import random
from wfrmls.exceptions import RateLimitError, ServerError, NetworkError

class RobustSyncManager:
    def __init__(self, client, local_storage):
        self.client = client
        self.storage = local_storage
        self.max_retries = 3
        self.base_delay = 1.0
    
    def robust_incremental_sync(self, resource_type):
        """Perform incremental sync with error handling and retry logic."""
        
        for attempt in range(self.max_retries + 1):
            try:
                return self._attempt_incremental_sync(resource_type)
                
            except RateLimitError as e:
                if e.retry_after:
                    wait_time = e.retry_after
                else:
                    wait_time = self.base_delay * (2 ** attempt)
                
                print(f"Rate limited, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                
            except (ServerError, NetworkError) as e:
                if attempt == self.max_retries:
                    raise e
                
                wait_time = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Server/network error, retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"Unexpected error during sync: {e}")
                raise e
        
        raise Exception(f"Sync failed after {self.max_retries} retries")
    
    def _attempt_incremental_sync(self, resource_type):
        """Single attempt at incremental sync."""
        
        last_sync = self.storage.get_last_sync_timestamp(resource_type)
        
        if resource_type == "properties":
            modified_records = self.client.property.get_properties(
                filter_query=f"ModificationTimestamp gt {last_sync.isoformat()}Z",
                select=["ListingId", "ListPrice", "StandardStatus", "ModificationTimestamp"]
            )
        elif resource_type == "members":
            modified_records = self.client.member.get_members(
                filter_query=f"ModificationTimestamp gt {last_sync.isoformat()}Z",
                select=["MemberKey", "MemberFirstName", "MemberLastName", "ModificationTimestamp"]
            )
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        # Get deleted records
        deleted_records = self.client.deleted.get_deleted_records(
            resource_type.title().rstrip('s'),  # Convert to singular
            date_from=last_sync
        )
        
        # Apply changes atomically
        with self.storage.transaction():
            if modified_records:
                getattr(self.storage, f"upsert_{resource_type}")(modified_records)
            
            if deleted_records:
                deleted_ids = [record['ResourceRecordKey'] for record in deleted_records]
                getattr(self.storage, f"delete_{resource_type}")(deleted_ids)
            
            # Update sync timestamp
            self.storage.update_last_sync_timestamp(resource_type, datetime.now())
        
        return {
            "updated": len(modified_records) if modified_records else 0,
            "deleted": len(deleted_records) if deleted_records else 0
        }

# Usage
robust_sync = RobustSyncManager(client, storage)

try:
    result = robust_sync.robust_incremental_sync("properties")
    print(f"Sync successful: {result}")
except Exception as e:
    print(f"Sync failed: {e}")
    # Implement fallback or alerting logic
```

## Monitoring and Metrics

### Sync Performance Monitor

```python
import time
from datetime import datetime, timedelta

class SyncMonitor:
    def __init__(self):
        self.metrics = {}
    
    def track_sync_performance(self, sync_function, *args, **kwargs):
        """Track performance metrics for sync operations."""
        
        start_time = time.time()
        start_datetime = datetime.now()
        
        try:
            result = sync_function(*args, **kwargs)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Record metrics
            metric_key = f"{sync_function.__name__}_{start_datetime.strftime('%Y%m%d_%H')}"
            
            if metric_key not in self.metrics:
                self.metrics[metric_key] = {
                    "function": sync_function.__name__,
                    "executions": 0,
                    "total_duration": 0,
                    "total_records": 0,
                    "errors": 0,
                    "last_execution": None
                }
            
            metrics = self.metrics[metric_key]
            metrics["executions"] += 1
            metrics["total_duration"] += duration
            metrics["last_execution"] = start_datetime.isoformat()
            
            if isinstance(result, dict):
                if "updated" in result:
                    metrics["total_records"] += result["updated"]
                if "total" in result:
                    metrics["total_records"] += result["total"]
            
            print(f"Sync completed in {duration:.2f} seconds")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            # Record error metrics
            metric_key = f"{sync_function.__name__}_{start_datetime.strftime('%Y%m%d_%H')}"
            
            if metric_key not in self.metrics:
                self.metrics[metric_key] = {
                    "function": sync_function.__name__,
                    "executions": 0,
                    "total_duration": 0,
                    "total_records": 0,
                    "errors": 0,
                    "last_execution": None
                }
            
            self.metrics[metric_key]["errors"] += 1
            self.metrics[metric_key]["total_duration"] += duration
            
            print(f"Sync failed after {duration:.2f} seconds: {e}")
            raise e
    
    def get_performance_report(self, hours_back=24):
        """Generate performance report for recent sync operations."""
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        report = {
            "report_period": f"Last {hours_back} hours",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_executions": 0,
                "total_errors": 0,
                "total_duration": 0,
                "total_records": 0
            },
            "by_function": {}
        }
        
        for metric_key, metrics in self.metrics.items():
            if metrics["last_execution"]:
                last_exec = datetime.fromisoformat(metrics["last_execution"])
                if last_exec >= cutoff_time:
                    function_name = metrics["function"]
                    
                    if function_name not in report["by_function"]:
                        report["by_function"][function_name] = {
                            "executions": 0,
                            "errors": 0,
                            "total_duration": 0,
                            "total_records": 0,
                            "avg_duration": 0,
                            "success_rate": 0
                        }
                    
                    func_metrics = report["by_function"][function_name]
                    func_metrics["executions"] += metrics["executions"]
                    func_metrics["errors"] += metrics["errors"]
                    func_metrics["total_duration"] += metrics["total_duration"]
                    func_metrics["total_records"] += metrics["total_records"]
                    
                    # Update summary
                    report["summary"]["total_executions"] += metrics["executions"]
                    report["summary"]["total_errors"] += metrics["errors"]
                    report["summary"]["total_duration"] += metrics["total_duration"]
                    report["summary"]["total_records"] += metrics["total_records"]
        
        # Calculate derived metrics
        for function_name, func_metrics in report["by_function"].items():
            if func_metrics["executions"] > 0:
                func_metrics["avg_duration"] = func_metrics["total_duration"] / func_metrics["executions"]
                func_metrics["success_rate"] = (func_metrics["executions"] - func_metrics["errors"]) / func_metrics["executions"]
        
        return report

# Usage
monitor = SyncMonitor()

# Track sync operations
def monitored_sync():
    return monitor.track_sync_performance(
        incremental_sync.incremental_sync_properties
    )

# Run monitored sync
result = monitored_sync()

# Generate report
report = monitor.get_performance_report(hours_back=24)
print(f"Performance Report:")
print(f"Total executions: {report['summary']['total_executions']}")
print(f"Total errors: {report['summary']['total_errors']}")
print(f"Total duration: {report['summary']['total_duration']:.2f} seconds")
```

## Best Practices

### Synchronization Strategy

1. **Use incremental sync** for regular updates
2. **Implement full sync** as a fallback option
3. **Track modification timestamps** for change detection
4. **Handle deleted records** explicitly
5. **Process in batches** for large datasets

### Performance Optimization

1. **Limit field selection** to reduce data transfer
2. **Use appropriate batch sizes** (100-1000 records)
3. **Implement caching** for frequently accessed data
4. **Consider parallel processing** for independent operations
5. **Monitor and tune** sync frequency

### Error Handling

1. **Implement retry logic** with exponential backoff
2. **Handle rate limits** gracefully
3. **Use transactions** for atomic operations
4. **Log sync operations** for debugging
5. **Implement alerting** for sync failures

### Data Integrity

1. **Validate data** before storage
2. **Maintain referential integrity** across resources
3. **Handle conflicts** with clear resolution strategies
4. **Backup data** before major sync operations
5. **Test sync logic** thoroughly

## Related Resources

- [Deleted Records API](../api/deleted.md) - Tracking deleted records
- [Error Handling Guide](error-handling.md) - Handling API errors
- [Rate Limits Guide](rate-limits.md) - Managing API rate limits