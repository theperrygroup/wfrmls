# WFRMLS API Endpoints Implementation Tasks

## Overview
This document outlines all the endpoints and features that need to be implemented for the WFRMLS (UtahRealEstate.com) Web API client library. The API is RESO certified and built on OData v4.0.

## Core Infrastructure Tasks

### 1. Authentication & Base Configuration
- [ ] Implement Bearer token authentication system
- [ ] Create base API client with configurable base URL (`https://resoapi.utahrealestate.com/reso/odata`)
- [ ] Implement request headers management (Authorization: Bearer token)
- [ ] Add rate limiting support (200 records per request default)
- [ ] Implement error handling and response validation

### 2. Service Discovery Endpoints

#### Service Document Endpoint
- [ ] **GET** `/reso/odata` - Service document endpoint
  - Returns all available resources for the authenticated vendor
  - Lists resource names and URLs
  - Provides discovery of available endpoints

#### Metadata Endpoint  
- [ ] **GET** `/reso/odata/$metadata` - OData metadata endpoint
  - Returns XML schema with all resources, fields, enumerations
  - Provides entity relationships and data types
  - Essential for understanding API structure

## Resource Endpoints

### 3. Property Resource (Primary)
- [ ] **GET** `/reso/odata/Property` - Property listings endpoint
  - Core property data retrieval
  - Support for all OData query options
  - Primary resource for real estate listings
- [ ] **GET** `/reso/odata/Property({key})` - Single property by key
- [ ] **GET** `/reso/odata/Property({key})/Media` - Property photos via navigation

### 4. Member Resource
- [ ] **GET** `/reso/odata/Member` - Real estate agent information
  - Agent profile data
  - Contact information
  - License details
- [ ] **GET** `/reso/odata/Member({key})` - Single member by key

### 5. Office Resource
- [ ] **GET** `/reso/odata/Office` - Real estate office details
  - Office information and contact details
  - Brokerage data
- [ ] **GET** `/reso/odata/Office({key})` - Single office by key

### 6. OpenHouse Resource
- [ ] **GET** `/reso/odata/OpenHouse` - Open house schedules
  - Open house events and timing
  - UTC timestamp handling
  - Relationship to properties
- [ ] **GET** `/reso/odata/OpenHouse({key})` - Single open house by key

### 7. Media Resource
- [ ] **GET** `/reso/odata/Media` - Property photos and media
  - Property image URLs
  - Media metadata (order, descriptions)
  - Support for filtering by ResourceRecordKeyNumeric
- [ ] **GET** `/reso/odata/Media({key})` - Single media item by key

### 8. HistoryTransactional Resource
- [ ] **GET** `/reso/odata/HistoryTransactional` - Historical transaction data
  - Property history and changes
  - Transaction records
- [ ] **GET** `/reso/odata/HistoryTransactional({key})` - Single history record

### 9. Lookup and Reference Resources
- [ ] **GET** `/reso/odata/DataSystem` - Data system information
- [ ] **GET** `/reso/odata/Resource` - Resource metadata
- [ ] **GET** `/reso/odata/Lookup` - Lookup table data
- [ ] **GET** `/reso/odata/PropertyGreenVerification` - Green verification data
- [ ] **GET** `/reso/odata/PropertyUnitTypes` - Unit type information
- [ ] **GET** `/reso/odata/Adu` - ADU (Accessory Dwelling Unit) data

### 10. Deletion Tracking
- [ ] **GET** `/reso/odata/Deleted` - Deleted records tracking
  - Track removed records for data synchronization
  - Filter by resource type and timestamp
  - Essential for maintaining data integrity

## OData Query Options Support

### 11. Basic Query Options
- [ ] **$select** - Field selection
  - Limit returned fields to reduce payload size
  - Support comma-separated field lists
- [ ] **$filter** - Data filtering
  - Support for all data types (string, number, boolean, date, timestamp)
  - Comparison operators (eq, ne, gt, ge, lt, le)
  - Logical operators (and, or, not)
  - String functions (contains, startswith, endswith)
- [ ] **$orderby** - Result sorting
  - Single and multiple field sorting
  - Ascending/descending order support
- [ ] **$top** - Limit number of results
  - Pagination support (max 200 records)
- [ ] **$skip** - Offset results for pagination
  - Warning: Can be slow for large datasets
- [ ] **$count** - Include total count in results

### 12. Advanced Query Options
- [ ] **$expand** - Include related resources
  - Property with Media (photos)
  - Property with Member (agent info)
  - Property with Office (brokerage info)
  - Property with OpenHouse (scheduled showings)
- [ ] **NextLink** pagination support
  - Follow @odata.nextLink for efficient pagination
  - Automatic continuation handling

## Geolocation Features

### 13. Geographic Search Capabilities
- [ ] **Radius Search** - `geo.distance()` function
  - Search properties within specified radius
  - Support for latitude/longitude coordinates
  - Distance calculations with SRID=3956
- [ ] **Polygon Search** - `geo.intersects()` function
  - Search properties within defined polygon areas
  - Support for complex geographic boundaries
  - Multi-point polygon definitions

## Specialized Features

### 14. Lookup Value Handling
- [ ] **Single Lookup Values** - using `has` operator
  - StandardStatus, PropertyType, etc.
  - Proper enum handling with Odata.Models namespace
- [ ] **Multi Lookup Values** - using `has` operator
  - ExteriorFeatures, InteriorFeatures, etc.
  - Multiple value selection support

### 15. Media and Photo Management
- [ ] **Photo Retrieval via $expand**
  - Include photos in property queries
  - Efficient single-request photo loading
- [ ] **Direct Media Queries**
  - Query Media resource directly
  - Filter by property key
  - Support for Media URL access

### 16. Data Replication Support
- [ ] **Full Replication**
  - Initial data download capabilities
  - Efficient pagination strategies
  - Primary key-based pagination (faster than $skip)
- [ ] **Incremental Updates**
  - ModificationTimestamp-based filtering
  - 15-minute update recommendations
  - Delta synchronization support
- [ ] **Deletion Handling**
  - Deleted resource queries
  - Cleanup of removed records
  - Data integrity maintenance

## Address Handling

### 17. Utah Address System Support
- [ ] **Standard Address Formatting**
  - StreetNumber, StreetName, StreetSuffix, UnitNumber
  - City, StateOrProvince, CountyOrParish, PostalCode
- [ ] **Grid Address Formatting**
  - Utah's grid system support (e.g., "1300 E 9400 S")
  - StreetNumber, StreetDirPrefix, CrossStreet, StreetDirSuffix
  - Logic to detect grid vs standard addresses

## Error Handling & Utilities

### 18. Robust Error Management
- [ ] **HTTP Error Handling**
  - Authentication failures (401)
  - Rate limiting (429)
  - Server errors (500)
  - Network timeouts
- [ ] **Data Validation**
  - Response format validation
  - Required field checking
  - Type conversion safety
- [ ] **Retry Logic**
  - Automatic retry for transient failures
  - Exponential backoff strategies

### 19. Developer Experience Features
- [ ] **Response Models**
  - Typed response objects for all resources
  - Proper datetime handling (UTC conversion)
  - Enum value mapping
- [ ] **Query Builders**
  - Fluent API for building complex queries
  - Type-safe filter construction
  - Query validation
- [ ] **Documentation & Examples**
  - Comprehensive API documentation
  - Code examples for common use cases
  - Best practices guide

## Testing & Quality Assurance

### 20. Test Coverage
- [ ] **Unit Tests**
  - All endpoint implementations
  - Query option combinations
  - Error scenarios
- [ ] **Integration Tests**
  - Live API testing with test credentials
  - End-to-end workflow validation
- [ ] **Performance Tests**
  - Large dataset handling
  - Pagination efficiency
  - Memory usage optimization

## Notes
- All timestamps are in UTC format
- Bearer token must be included in Authorization header
- Rate limit is 200 records per request by default
- Recommended update frequency: every 15 minutes
- URL encoding required for special characters in query parameters
- ResourceRecordKey and ResourceRecordID are strings (as of 2020-11-09 update) 