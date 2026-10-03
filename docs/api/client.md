---
description: Configure WFRMLSClient, understand lazy authentication, access resource clients, and retrieve service discovery JSON or metadata XML.
---

# WFRMLSClient: configuration and service access

`WFRMLSClient` creates resource-specific clients when you first access them. Use it for listing queries, directory data, resource discovery, and metadata.

## Configure the client

`WFRMLSClient(bearer_token=None, base_url=None)` stores configuration without making a request or checking credentials.

| Parameter | Type | Required | Description | Default |
| --- | --- | --- | --- | --- |
| `bearer_token` | `str \| None` | No | Token passed to each service client | `None` |
| `base_url` | `str \| None` | No | Override the OData service root | `None` |

When a service client is first constructed, it uses the explicit token or `WFRMLS_BEARER_TOKEN`. Missing credentials raise `AuthenticationError` at that point. Token validity is checked by the server when a request is made.

The default service root is `https://resoapi.utahrealestate.com/reso/odata`. The facade's `bearer_token` and `base_url` properties return the values passed to its constructor, including `None`; they do not expose resolved environment values or defaults.

With `WFRMLS_BEARER_TOKEN` configured:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(top=10)
for listing in response.get("value", []):
    print(listing.get("ListingId"), listing.get("ListPrice"))
```

## Access the resource clients

Each property caches its client instance. Repeated access returns the same instance; different services have separate HTTP sessions.

| Attribute | Client class | Reference |
| --- | --- | --- |
| `property` | `PropertyClient` | [Properties](properties.md) |
| `member` | `MemberClient` | [Members](members.md) |
| `office` | `OfficeClient` | [Offices](offices.md) |
| `openhouse` | `OpenHouseClient` | [Open houses](openhouse.md) |
| `open_house` | `OpenHouseClient` | Alias of `openhouse` |
| `data_system` | `DataSystemClient` | [Data systems](data-system.md) |
| `resource` | `ResourceClient` | [Resources](resource.md) |
| `property_unit_types` | `PropertyUnitTypesClient` | [Unit types](property-unit-types.md) |
| `lookup` | `LookupClient` | [Lookup values](lookup.md) |
| `adu` | `AduClient` | [Accessory dwelling units](adu.md) |
| `deleted` | `DeletedClient` | [Deleted records](deleted.md) |

There are no `media`, `history`, or `green` attributes on this facade. The separately exported compatibility classes are described in [clients outside the facade](unavailable-clients.md).

## Discover entity sets and field definitions

`get_service_document()` returns the parsed JSON response from the service root. `get_metadata()` returns the raw XML string from `/$metadata`.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
document = client.get_service_document()
for entity_set in document.get("value", []):
    print(entity_set.get("name"), entity_set.get("url"))

metadata_xml = client.get_metadata()
print(metadata_xml[:100])
```

Discovery describes the server response for your credentials; it does not verify that every query, field, or relationship will succeed. The package does not parse the XML schema for you.

Service-document failures use the [shared HTTP exception mapping](exceptions.md). Metadata retrieval uses a separate request with a 30-second timeout: any non-200 response raises generic `WFRMLSError`, and Requests transport exceptions propagate directly.

## Related references

- [HTTP behavior](base-client.md): sessions, response handling, and timeout limits.
- [Response conventions](../reference/index.md): collections and single records.
- [Authentication](../getting-started/authentication.md): configure credentials before making requests.
