---
description: Find exact WFRMLS Python client interfaces for listing queries, directory records, metadata, unit data, deletion tracking, analytics, and HTTP errors.
---

# WFRMLS Python API reference

Use these pages to choose a client method, understand its query parameters, and interpret its return value. Examples require `WFRMLS_BEARER_TOKEN` unless explicitly mocked.

## Client and HTTP behavior

- [WFRMLSClient](client.md): configuration, lazy service access, discovery JSON, and metadata XML.
- [BaseClient](base-client.md): authentication, sessions, raw OData requests, and HTTP limits.
- [Exceptions](exceptions.md): status mapping and failure paths that return partial data or error dictionaries.
- [Response conventions](../reference/index.md): collections, single objects, counts, and extracted lists.

## Listing and directory resources

- [Properties](properties.md): numeric lookup, filters, supported helpers, and pagination limitations.
- [Members](members.md): member records, office relationships, and search helpers.
- [Offices](offices.md): brokerage records and member expansion.
- [Open houses](openhouse.md): date/status queries and convenience-helper limits.

## Supporting resources

- [ADU](adu.md): accessory dwelling unit queries.
- [Property unit types](property-unit-types.md): unit records and field-specific helper filters.
- [Lookup values](lookup.md): lookup collections and name/value fields.
- [Resources](resource.md): resource metadata and resource-name queries.
- [Data systems](data-system.md): collection queries and system discovery.
- [Deleted records](deleted.md): deletion queries, date filters, and synchronization helpers.
- [Analytics](analytics.md): sampled summaries, price segments, agent reports, and data-quality checks.

## Availability and compatibility

- [Clients outside the facade](unavailable-clients.md): separately exported Media, History, and Green Verification classes.
- [Media](media.md), [history](history.md), and [green verification](green-verification.md): standalone class signatures and compatibility limits.
- [Implementation and provider verification](live-api-updates.md): what source/mocks establish and what needs account-specific verification.

The wrapper supports a subset of OData parameters through named Python arguments. It does not validate the server's complete schema, implement automatic retries, or make every helper a complete dataset query.

For task-oriented instructions, start with [authentication](../getting-started/authentication.md), [property search](../guides/property-search.md), and [OData queries](../guides/odata-queries.md).
