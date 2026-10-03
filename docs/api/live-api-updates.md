---
description: Distinguish verified WFRMLS package behavior from provider schema, endpoint availability, authorization, historical observations, and mocked test evidence.
---

# Implementation behavior and provider verification

This reference describes what the package implements and what requires verification against your provider account. It replaces historical testing claims with explicit evidence boundaries.

## What source and mocked tests establish

- `WFRMLSClient` exposes ten service clients plus the `open_house` alias.
- Collection methods translate named arguments into OData parameters and return parsed JSON.
- `PropertyClient.get_property()` converts a numeric string to a numeric key URL and normalizes a wrapped result to one object.
- Radius and polygon helpers raise `ValidationError`; address search is a city fallback.
- The facade does not expose Media, History, or Green Verification clients. Their classes remain importable separately.

Mocked tests validate request construction and response handling. They do not establish live authorization, current entity counts, server uptime, complete field schemas, or endpoint availability.

## Verify the schema for your account

After configuring `WFRMLS_BEARER_TOKEN`, discover entity sets and inspect metadata:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
document = client.get_service_document()
entity_names = [item.get("name") for item in document.get("value", [])]
print(entity_names)
metadata_xml = client.get_metadata()
print(metadata_xml[:100])
```

Use that schema to choose fields, key types, lookup values, and expansion relationships. Availability in a service document does not guarantee that every requested filter or expansion is accepted.

## Read method-specific return shapes

Collection responses commonly contain `value`; single-key methods and extraction helpers return different shapes. Metadata is XML. Do not assume every result contains `value` or that every response includes a count or next link. The [response reference](../reference/index.md) lists the concrete differences.

## Treat historical observations as historical

Previous documentation reported provider errors, special IDs, a member count, and a testing date. Those statements did not include reproducible current evidence and have been removed. The package's stale endpoint comments do not establish a current provider outage or a restoration date.

For a production investigation, record the package version, entity set, sanitized query, response status, and observation time. Keep credentials and private record content out of published documentation.

See [clients outside the facade](unavailable-clients.md), [property limitations](properties.md#location-helper-limitations), and [exception behavior](exceptions.md).
