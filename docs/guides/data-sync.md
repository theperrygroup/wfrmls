# Data Synchronization Guide

This guide covers how to efficiently synchronize data from the WFRMLS API, including incremental updates, change tracking, and maintaining local data consistency.

---

## Overview

Data synchronization is crucial for applications that need to maintain up-to-date real estate information. The WFRMLS API provides several mechanisms for efficient data synchronization:

- **Timestamp-based incremental updates** - Track changes since last sync
- **Change tracking** - Monitor specific field modifications
- **Deleted record tracking** - Handle removed listings
- **Batch processing** - Efficiently process large datasets

---

## Synchronization Strategies

### Full Synchronization

Complete data refresh - useful for initial setup or periodic validation:

```python
from wfrmls import WFRMLSClient
from datetime import datetime
import json

client = WFRMLSClient()

def full_sync_properties():
    """Perform a complete synchronization of all active properties."""
    
    print("Starting full property synchronization...")
    start_time = datetime.now()
    
    all_properties = []
    skip = 0
    batch_size = 100
    
    while True:
        # Get batch of properties
        batch = client.property.get_properties(
            filter_query="StandardStatus eq 'Active'",
            select=[
                "ListingId", "ListPrice", "StandardStatus", "ModificationTimestamp",
                "PropertyAddress", "PropertyCity", "BedroomsTotal", "BathroomsTotalInteger",
                "LivingArea", "ListAgentKey", "OfficeKey"
            ],
            orderby="ModificationTimestamp asc",
            top=batch_size,
            skip=skip
        )
        
        if not batch:
            break
        
        all_properties.extend(batch)
        skip += batch_size
        
        print(f"Processed {len(all_properties)} properties...")
        
        # Optional: Save progress periodically
        if len(all_properties) % 1000 == 0:
            save_sync_progress(all_properties, "full_sync_progress.json")
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"Full sync completed: {len(all_properties)} properties in {duration}")
    
    # Save final results
    save_sync_data(all_properties, "full_sync_properties.json")
    update_sync_metadata("properties", "full", end_time, len(all_properties))
    
    return all_properties

def save_sync_data(data, filename):
    """Save synchronization data to file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def save_sync_progress(data, filename):
    """Save synchronization progress."""
    progress = {
        "timestamp": datetime.now().isoformat(),
        "count": len(data),
        "data": data
    }
    with open(filename, 'w') as f:
        json.dump(progress, f, indent=2, default=str)

def update_sync_metadata(resource_type, sync_type, timestamp, count):
    """Update synchronization metadata."""
    metadata = {
        "resource_type": resource_type,
        "sync_type": sync_type,
        "last_sync": timestamp.isoformat(),
        "record_count": count
    }
    
    with open(f"sync_metadata_{resource_type}.json", 'w') as f:
        json.dump(metadata, f, indent=2)
```

### Incremental Synchronization

Update only changed records since last sync:

```python
def incremental_sync_properties(last_sync_time=None):
    """Perform incremental synchronization of properties."""
    
    if last_sync_time is None:
        last_sync_time = get_last_sync_time("properties")
    
    if last_sync_time is None:
        print("No previous sync found, performing full sync...")
        return full_sync_properties()
    
    print(f"Starting incremental sync since {last_sync_time}")
    start_time = datetime.now()
    
    # Get properties modified since last sync
    modified_properties = client.property.get_properties(
        filter_query=f"ModificationTimestamp gt {last_sync_time.isoformat()}Z",
        select=[
            "ListingId", "ListPrice", "StandardStatus", "ModificationTimestamp",
            "PropertyAddress", "PropertyCity", "BedroomsTotal", "BathroomsTotalInteger",
            "LivingArea", "ListAgentKey", "OfficeKey"
        ],
        orderby="ModificationTimestamp asc"
    )
    
    # Process changes
    changes = process_property_changes(modified_properties, last_sync_time)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"Incremental sync completed: {len(modified_properties)} changes in {duration}")
    
    # Save results
    save_sync_data(changes, f"incremental_sync_{start_time.strftime('%Y%m%d_%H%M%S')}.json")
    update_sync_metadata("properties", "incremental", end_time, len(modified_properties))
    
    return changes

def get_last_sync_time(resource_type):
    """Get the timestamp of the last synchronization."""
    try:
        with open(f"sync_metadata_{resource_type}.json", 'r') as f:
            metadata = json.load(f)
            return datetime.fromisoformat(metadata["last_sync"])
    except FileNotFoundError:
        return None

def process_property_changes(properties, last_sync_time):
    """Process and categorize property changes."""
    changes = {
        "new_listings": [],
        "updated_listings": [],
        "status_changes": [],
        "price_changes": []
    }
    
    # Load existing data for comparison
    existing_properties = load_existing_properties()
    
    for prop in properties:
        listing_id = prop["ListingId"]
        
        if listing_id not in existing_properties:
            # New listing
            changes["new_listings"].append(prop)
        else:
            # Updated listing
            existing_prop = existing_properties[listing_id]
            
            # Check for status changes
            if prop["StandardStatus"] != existing_prop.get("StandardStatus"):
                changes["status_changes"].append({
                    "listing_id": listing_id,
                    "old_status": existing_prop.get("StandardStatus"),
                    "new_status": prop["StandardStatus"],
                    "property": prop
                })
            
            # Check for price changes
            if prop["ListPrice"] != existing_prop.get("ListPrice"):
                changes["price_changes"].append({
                    "listing_id": listing_id,
                    "old_price": existing_prop.get("ListPrice"),
                    "new_price": prop["ListPrice"],
                    "property": prop
                })
            
            changes["updated_listings"].append(prop)
    
    return changes

def load_existing_properties():
    """Load existing property data for comparison."""
    try:
        with open("full_sync_properties.json", 'r') as f:
            properties = json.load(f)
            return {prop["ListingId"]: prop for prop in properties}
    except FileNotFoundError:
        return {}
```

---

## Change Tracking

### Field-Level Change Detection

Track specific field changes for detailed monitoring:

```python
class PropertyChangeTracker:
    def __init__(self, client):
        self.client = client
        self.tracked_fields = [
            "ListPrice", "StandardStatus", "DaysOnMarket", "ListAgentKey",
            "PropertyAddress", "BedroomsTotal", "BathroomsTotalInteger"
        ]
    
    def track_changes(self, listing_ids, since_timestamp):
        """Track changes for specific properties."""
        
        changes_by_property = {}
        
        for listing_id in listing_ids:
            try:
                # Get current property data
                current_property = self.client.property.get_property(
                    listing_id,
                    select=self.tracked_fields + ["ModificationTimestamp"]
                )
                
                # Load previous data
                previous_property = self.load_previous_property_data(listing_id)
                
                if previous_property:
                    changes = self.detect_field_changes(
                        previous_property, current_property
                    )
                    
                    if changes:
                        changes_by_property[listing_id] = {
                            "changes": changes,
                            "current_data": current_property,
                            "previous_data": previous_property
                        }
                
                # Save current data for future comparisons
                self.save_property_data(listing_id, current_property)
                
            except Exception as e:
                print(f"Error tracking changes for {listing_id}: {e}")
        
        return changes_by_property
    
    def detect_field_changes(self, previous, current):
        """Detect changes between previous and current property data."""
        changes = []
        
        for field in self.tracked_fields:
            prev_value = previous.get(field)
            curr_value = current.get(field)
            
            if prev_value != curr_value:
                changes.append({
                    "field": field,
                    "previous_value": prev_value,
                    "current_value": curr_value,
                    "change_timestamp": current.get("ModificationTimestamp")
                })
        
        return changes
    
    def load_previous_property_data(self, listing_id):
        """Load previous property data for comparison."""
        try:
            with open(f"property_data/{listing_id}.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def save_property_data(self, listing_id, property_data):
        """Save property data for future comparisons."""
        import os
        os.makedirs("property_data", exist_ok=True)
        
        with open(f"property_data/{listing_id}.json", 'w') as f:
            json.dump(property_data, f, indent=2, default=str)

# Usage
tracker = PropertyChangeTracker(client)

# Track changes for specific properties
listing_ids = ["12345678", "87654321", "11223344"]
since_time = datetime.now() - timedelta(hours=24)

changes = tracker.track_changes(listing_ids, since_time)

for listing_id, change_data in changes.items():
    print(f"\nChanges for {listing_id}:")
    for change in change_data["changes"]:
        print(f"  {change['field']}: {change['previous_value']} → {change['current_value']}")
```

### Status Change Monitoring

Monitor specific status transitions:

```python
def monitor_status_changes():
    """Monitor property status changes."""
    
    # Define status transitions to monitor
    monitored_transitions = [
        ("Active", "Pending"),
        ("Pending", "Closed"),
        ("Active", "Withdrawn"),
        ("Active", "Expired")
    ]
    
    last_check = get_last_sync_time("status_monitoring")
    if not last_check:
        last_check = datetime.now() - timedelta(hours=1)
    
    # Get recently modified properties
    recent_properties = client.property.get_properties(
        filter_query=f"ModificationTimestamp gt {last_check.isoformat()}Z",
        select=["ListingId", "StandardStatus", "ModificationTimestamp", "PropertyAddress"],
        orderby="ModificationTimestamp asc"
    )
    
    status_changes = []
    
    for prop in recent_properties:
        listing_id = prop["ListingId"]
        current_status = prop["StandardStatus"]
        
        # Get previous status
        previous_data = load_previous_property_data(listing_id)
        if previous_data:
            previous_status = previous_data.get("StandardStatus")
            
            # Check if this is a monitored transition
            transition = (previous_status, current_status)
            if transition in monitored_transitions:
                status_changes.append({
                    "listing_id": listing_id,
                    "address": prop["PropertyAddress"],
                    "previous_status": previous_status,
                    "current_status": current_status,
                    "change_timestamp": prop["ModificationTimestamp"],
                    "transition": f"{previous_status} → {current_status}"
                })
    
    # Save status changes
    if status_changes:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_sync_data(status_changes, f"status_changes_{timestamp}.json")
        
        print(f"Detected {len(status_changes)} status changes:")
        for change in status_changes:
            print(f"  {change['listing_id']}: {change['transition']}")
    
    update_sync_metadata("status_monitoring", "incremental", datetime.now(), len(status_changes))
    
    return status_changes
```

---

## Deleted Record Handling

### Tracking Deleted Listings

Handle properties that have been removed from the MLS:

```python
def sync_deleted_properties():
    """Synchronize deleted property records."""
    
    last_sync = get_last_sync_time("deleted_properties")
    if not last_sync:
        last_sync = datetime.now() - timedelta(days=7)
    
    # Get deleted properties since last sync
    deleted_properties = client.deleted.get_deleted_properties(
        filter_query=f"DeletedDate gt {last_sync.isoformat()}Z",
        select=["ListingId", "DeletedDate", "DeletedReason"],
        orderby="DeletedDate asc"
    )
    
    print(f"Found {len(deleted_properties)} deleted properties since {last_sync}")
    
    # Process deletions
    deletion_summary = process_deletions(deleted_properties)
    
    # Update sync metadata
    update_sync_metadata("deleted_properties", "incremental", datetime.now(), len(deleted_properties))
    
    return deletion_summary

def process_deletions(deleted_properties):
    """Process deleted property records."""
    
    deletion_summary = {
        "total_deleted": len(deleted_properties),
        "by_reason": {},
        "processed_deletions": []
    }
    
    for deleted_prop in deleted_properties:
        listing_id = deleted_prop["ListingId"]
        reason = deleted_prop.get("DeletedReason", "Unknown")
        
        # Count by reason
        deletion_summary["by_reason"][reason] = deletion_summary["by_reason"].get(reason, 0) + 1
        
        # Remove from local storage
        remove_local_property_data(listing_id)
        
        deletion_summary["processed_deletions"].append({
            "listing_id": listing_id,
            "deleted_date": deleted_prop["DeletedDate"],
            "reason": reason
        })
        
        print(f"Processed deletion: {listing_id} ({reason})")
    
    # Save deletion summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_sync_data(deletion_summary, f"deletions_{timestamp}.json")
    
    return deletion_summary

def remove_local_property_data(listing_id):
    """Remove local property data files."""
    import os
    
    files_to_remove = [
        f"property_data/{listing_id}.json",
        f"property_images/{listing_id}/",
        f"property_cache/{listing_id}.json"
    ]
    
    for file_path in files_to_remove:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
```

---

## Batch Processing

### Efficient Bulk Operations

Process large datasets efficiently:

```python
class BatchProcessor:
    def __init__(self, client, batch_size=100):
        self.client = client
        self.batch_size = batch_size
    
    def process_all_properties(self, processor_func, filter_query="StandardStatus eq 'Active'"):
        """Process all properties in batches."""
        
        total_processed = 0
        skip = 0
        
        while True:
            # Get batch
            batch = self.client.property.get_properties(
                filter_query=filter_query,
                top=self.batch_size,
                skip=skip,
                orderby="ModificationTimestamp asc"
            )
            
            if not batch:
                break
            
            # Process batch
            try:
                processor_func(batch)
                total_processed += len(batch)
                skip += self.batch_size
                
                print(f"Processed batch: {len(batch)} properties (total: {total_processed})")
                
            except Exception as e:
                print(f"Error processing batch at skip {skip}: {e}")
                # Continue with next batch
                skip += self.batch_size
        
        return total_processed
    
    def sync_property_images(self, properties):
        """Sync property images for a batch of properties."""
        
        for prop in properties:
            listing_id = prop["ListingId"]
            
            try:
                # Get property media
                media = self.client.media.get_media(
                    filter_query=f"ResourceRecordKey eq '{listing_id}'",
                    select=["MediaKey", "MediaURL", "MediaType", "MediaModificationTimestamp"]
                )
                
                # Process media files
                self.process_property_media(listing_id, media)
                
            except Exception as e:
                print(f"Error syncing images for {listing_id}: {e}")
    
    def process_property_media(self, listing_id, media):
        """Process media files for a property."""
        import os
        import requests
        
        media_dir = f"property_images/{listing_id}"
        os.makedirs(media_dir, exist_ok=True)
        
        for media_item in media:
            if media_item["MediaType"] == "Photo":
                media_url = media_item["MediaURL"]
                media_key = media_item["MediaKey"]
                
                # Download image if not already cached
                image_path = f"{media_dir}/{media_key}.jpg"
                if not os.path.exists(image_path):
                    try:
                        response = requests.get(media_url)
                        response.raise_for_status()
                        
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"Downloaded image: {media_key}")
                        
                    except Exception as e:
                        print(f"Error downloading image {media_key}: {e}")

# Usage
processor = BatchProcessor(client, batch_size=50)

# Process all active properties to sync images
def sync_images_batch(properties):
    processor.sync_property_images(properties)

total_processed = processor.process_all_properties(sync_images_batch)
print(f"Completed image sync for {total_processed} properties")
```

### Parallel Processing

Use threading for improved performance:

```python
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

class ParallelSyncProcessor:
    def __init__(self, client, max_workers=5):
        self.client = client
        self.max_workers = max_workers
        self.results_queue = Queue()
    
    def parallel_property_sync(self, listing_ids):
        """Sync properties in parallel."""
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_listing = {
                executor.submit(self.sync_single_property, listing_id): listing_id
                for listing_id in listing_ids
            }
            
            # Collect results
            for future in as_completed(future_to_listing):
                listing_id = future_to_listing[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"Completed sync for {listing_id}")
                except Exception as e:
                    print(f"Error syncing {listing_id}: {e}")
        
        return results
    
    def sync_single_property(self, listing_id):
        """Sync a single property with full details."""
        
        try:
            # Get property details
            property_data = self.client.property.get_property(listing_id)
            
            # Get property media
            media = self.client.media.get_media(
                filter_query=f"ResourceRecordKey eq '{listing_id}'"
            )
            
            # Get open houses
            open_houses = self.client.openhouse.get_openhouses(
                filter_query=f"PropertyKey eq '{listing_id}'"
            )
            
            # Combine all data
            complete_data = {
                "property": property_data,
                "media": media,
                "open_houses": open_houses,
                "sync_timestamp": datetime.now().isoformat()
            }
            
            # Save to file
            self.save_complete_property_data(listing_id, complete_data)
            
            return {
                "listing_id": listing_id,
                "status": "success",
                "media_count": len(media),
                "open_house_count": len(open_houses)
            }
            
        except Exception as e:
            return {
                "listing_id": listing_id,
                "status": "error",
                "error": str(e)
            }
    
    def save_complete_property_data(self, listing_id, data):
        """Save complete property data."""
        import os
        
        os.makedirs("complete_property_data", exist_ok=True)
        
        with open(f"complete_property_data/{listing_id}.json", 'w') as f:
            json.dump(data, f, indent=2, default=str)

# Usage
parallel_processor = ParallelSyncProcessor(client, max_workers=3)

# Get list of properties to sync
recent_properties = client.property.get_properties(
    filter_query="ModificationTimestamp gt 2024-01-01T00:00:00Z",
    select=["ListingId"],
    top=100
)

listing_ids = [prop["ListingId"] for prop in recent_properties]

# Sync in parallel
results = parallel_processor.parallel_property_sync(listing_ids)

# Analyze results
successful = [r for r in results if r["status"] == "success"]
failed = [r for r in results if r["status"] == "error"]

print(f"Parallel sync completed: {len(successful)} successful, {len(failed)} failed")
```

---

## Synchronization Scheduling

### Automated Sync Jobs

Set up automated synchronization schedules:

```python
import schedule
import time
from datetime import datetime, timedelta

class SyncScheduler:
    def __init__(self, client):
        self.client = client
        self.setup_schedules()
    
    def setup_schedules(self):
        """Set up synchronization schedules."""
        
        # Full sync weekly on Sunday at 2 AM
        schedule.every().sunday.at("02:00").do(self.run_full_sync)
        
        # Incremental sync every hour
        schedule.every().hour.do(self.run_incremental_sync)
        
        # Status monitoring every 15 minutes
        schedule.every(15).minutes.do(self.run_status_monitoring)
        
        # Deleted records sync daily at 3 AM
        schedule.every().day.at("03:00").do(self.run_deleted_sync)
    
    def run_full_sync(self):
        """Run full synchronization."""
        try:
            print(f"Starting full sync at {datetime.now()}")
            result = full_sync_properties()
            print(f"Full sync completed: {len(result)} properties")
        except Exception as e:
            print(f"Full sync failed: {e}")
    
    def run_incremental_sync(self):
        """Run incremental synchronization."""
        try:
            print(f"Starting incremental sync at {datetime.now()}")
            result = incremental_sync_properties()
            print(f"Incremental sync completed: {len(result.get('updated_listings', []))} updates")
        except Exception as e:
            print(f"Incremental sync failed: {e}")
    
    def run_status_monitoring(self):
        """Run status change monitoring."""
        try:
            result = monitor_status_changes()
            if result:
                print(f"Status monitoring: {len(result)} changes detected")
        except Exception as e:
            print(f"Status monitoring failed: {e}")
    
    def run_deleted_sync(self):
        """Run deleted records synchronization."""
        try:
            result = sync_deleted_properties()
            print(f"Deleted sync completed: {result['total_deleted']} deletions")
        except Exception as e:
            print(f"Deleted sync failed: {e}")
    
    def start_scheduler(self):
        """Start the synchronization scheduler."""
        print("Starting sync scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Usage
scheduler = SyncScheduler(client)

# Run scheduler (this will run indefinitely)
# scheduler.start_scheduler()

# Or run specific sync operations manually
scheduler.run_incremental_sync()
```

---

## Error Handling and Recovery

### Robust Sync Operations

Handle errors gracefully and provide recovery mechanisms:

```python
class RobustSyncManager:
    def __init__(self, client):
        self.client = client
        self.max_retries = 3
        self.retry_delay = 5  # seconds
    
    def robust_sync_with_retry(self, sync_function, *args, **kwargs):
        """Execute sync function with retry logic."""
        
        for attempt in range(self.max_retries):
            try:
                result = sync_function(*args, **kwargs)
                return result
                
            except Exception as e:
                print(f"Sync attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print("All retry attempts failed")
                    raise e
    
    def sync_with_checkpoint(self, sync_function, checkpoint_interval=100):
        """Sync with periodic checkpoints for recovery."""
        
        checkpoint_file = "sync_checkpoint.json"
        
        # Load previous checkpoint
        checkpoint = self.load_checkpoint(checkpoint_file)
        start_skip = checkpoint.get("last_processed", 0)
        
        skip = start_skip
        batch_size = 100
        
        try:
            while True:
                # Get batch
                batch = self.client.property.get_properties(
                    filter_query="StandardStatus eq 'Active'",
                    top=batch_size,
                    skip=skip,
                    orderby="ModificationTimestamp asc"
                )
                
                if not batch:
                    break
                
                # Process batch
                sync_function(batch)
                skip += len(batch)
                
                # Save checkpoint
                if skip % checkpoint_interval == 0:
                    self.save_checkpoint(checkpoint_file, {
                        "last_processed": skip,
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"Checkpoint saved at {skip} records")
        
        except Exception as e:
            print(f"Sync failed at record {skip}: {e}")
            self.save_checkpoint(checkpoint_file, {
                "last_processed": skip,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            })
            raise e
        
        finally:
            # Clean up checkpoint on successful completion
            if skip > start_skip:
                self.clear_checkpoint(checkpoint_file)
    
    def load_checkpoint(self, filename):
        """Load sync checkpoint."""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_checkpoint(self, filename, checkpoint_data):
        """Save sync checkpoint."""
        with open(filename, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
    
    def clear_checkpoint(self, filename):
        """Clear sync checkpoint."""
        import os
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

# Usage
robust_sync = RobustSyncManager(client)

# Sync with retry logic
def my_sync_function():
    return incremental_sync_properties()

result = robust_sync.robust_sync_with_retry(my_sync_function)

# Sync with checkpoints
def process_batch(properties):
    for prop in properties:
        # Process individual property
        print(f"Processing {prop['ListingId']}")

robust_sync.sync_with_checkpoint(process_batch)
```

---

## Performance Monitoring

### Sync Performance Metrics

Monitor synchronization performance:

```python
class SyncPerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def time_sync_operation(self, operation_name, sync_function, *args, **kwargs):
        """Time a sync operation and collect metrics."""
        
        start_time = datetime.now()
        start_memory = self.get_memory_usage()
        
        try:
            result = sync_function(*args, **kwargs)
            
            end_time = datetime.now()
            end_memory = self.get_memory_usage()
            
            duration = (end_time - start_time).total_seconds()
            memory_delta = end_memory - start_memory
            
            # Record metrics
            self.metrics[operation_name] = {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "memory_usage_mb": memory_delta,
                "records_processed": len(result) if isinstance(result, list) else 1,
                "records_per_second": len(result) / duration if isinstance(result, list) and duration > 0 else 0,
                "status": "success"
            }
            
            print(f"{operation_name} completed in {duration:.2f}s ({len(result) if isinstance(result, list) else 1} records)")
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.metrics[operation_name] = {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "status": "error",
                "error": str(e)
            }
            
            raise e
    
    def get_memory_usage(self):
        """Get current memory usage in MB."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def generate_performance_report(self):
        """Generate performance report."""
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "operations": self.metrics,
            "summary": {
                "total_operations": len(self.metrics),
                "successful_operations": len([m for m in self.metrics.values() if m["status"] == "success"]),
                "failed_operations": len([m for m in self.metrics.values() if m["status"] == "error"]),
                "total_duration": sum(m["duration_seconds"] for m in self.metrics.values()),
                "average_duration": sum(m["duration_seconds"] for m in self.metrics.values()) / len(self.metrics) if self.metrics else 0
            }
        }
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"sync_performance_report_{timestamp}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

# Usage
monitor = SyncPerformanceMonitor()

# Monitor sync operations
properties = monitor.time_sync_operation("incremental_sync", incremental_sync_properties)
deleted = monitor.time_sync_operation("deleted_sync", sync_deleted_properties)

# Generate performance report
report = monitor.generate_performance_report()
print(f"Performance report generated: {report['summary']}")
```

---

## Related Resources

- **[Property API](../api/properties.md)** - Property data access methods
- **[Analytics API](../api/analytics.md)** - Market data synchronization
- **[Error Handling Guide](error-handling.md)** - Robust error management
- **[Rate Limits Guide](rate-limits.md)** - API usage optimization