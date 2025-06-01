# UtahRealEstate.com Web API Documentation

## Overview

Welcome to the UtahRealEstate.com Web API documentation. This API is a RESO certified RESTful API built on OData v4.0. The API is both RESO web API Certified and RESO Data Dictionary Certified.

## Documentation Sections

### [Overview](overview.md)
Introduction to the API, REST concepts, getting started, and authentication details.

### [OData Endpoints](odata-endpoints.md)
Information about service documents, metadata, and available resource endpoints.

### [Query Options](query-options.md)
Detailed guide on using OData query options including $select, $filter, $top, $skip, $count, and $expand.

### [Geolocation Search](geolocation-search.md)
How to perform radius searches and polygon searches using geographic coordinates.

### [Replication](replication.md)
Comprehensive guide on pulling data, keeping data up-to-date, and managing deletions. Includes PHP code examples.

### [Getting Photos](getting-photos.md)
Methods for retrieving property photos using $expand or direct Media resource queries.

### [Getting Open Houses](getting-open-houses.md)
How to query OpenHouse resources and understand time zone considerations.

### [Addresses](addresses.md)
Understanding Utah's grid address system vs. standard addresses and the appropriate RESO fields.

### [Change Log](change-log.md)
Historical log of API updates, releases, and bug fixes.

## Quick Start

1. **Authentication**: Use Bearer token authentication
2. **Base URL**: `https://resoapi.utahrealestate.com/reso/odata`
3. **Rate Limits**: 200 records per request (default)
4. **Update Frequency**: Recommended every 15 minutes for incremental updates

## Key Resources

- **Property**: Main property listings data
- **Media**: Property photos and media files
- **Member**: Real estate agent information
- **Office**: Real estate office details
- **OpenHouse**: Open house schedules and information
- **HistoryTransactional**: Historical property transaction data

## Support

For additional support and vendor registration, visit:
- [Vendor Dashboard](https://vendor.utahrealestate.com)
- [Registration](https://vendor.utahrealestate.com) (for new vendors)

---

*Last updated: API documentation scraped from vendor.utahrealestate.com*
