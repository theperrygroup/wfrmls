# Provider OData Endpoints

This page explains the service-discovery and resource patterns in the retained
provider documentation. See the [source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Resource access depends on the authenticated vendor account; a historical example
is not a current inventory of available endpoints.

## Service document

The OData service root returns a JSON document describing entity sets available
to an account. The wrapper's default root is:

`https://resoapi.utahrealestate.com/reso/odata`

```http
GET /reso/odata HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
Accept: application/json
```

An abbreviated historical example:

```json
{
    "@odata.context": "https://resoapi.utahrealestate.com/reso/odata/$metadata",
    "value": [
        {"name": "Property", "url": "https://resoapi.utahrealestate.com/reso/odata/Property"},
        {"name": "Member", "url": "https://resoapi.utahrealestate.com/reso/odata/Member"},
        {"name": "Office", "url": "https://resoapi.utahrealestate.com/reso/odata/Office"},
        {"name": "OpenHouse", "url": "https://resoapi.utahrealestate.com/reso/odata/OpenHouse"}
    ]
}
```

`WFRMLSClient.get_service_document()` makes this discovery request and returns
its parsed JSON. No request was made during this documentation review.

## Metadata

The `$metadata` endpoint describes fields, entity keys, enum types, and navigation
relationships in XML:

```http
GET /reso/odata/$metadata HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
Accept: application/xml
```

`WFRMLSClient.get_metadata()` returns XML text. The checked-in
[metadata.xml](metadata.xml) can be used to inspect the historical schema, but
has no verified capture date and may differ from an account's current schema.
In that snapshot:

- Property uses the numeric `ListingKeyNumeric` entity key and also has a string
  `ListingKey` field.
- OpenHouse uses `OpenHouseKeyNumeric` as its entity key.
- Media uses a string `MediaKey` and has numeric `ResourceRecordKeyNumeric` and
  string `ResourceRecordKey` join fields.
- Navigation bindings include Property-to-Media and Property-to-OpenHouse.

Check field types before quoting keys or writing filters. Do not assume a
listing display ID, a string join key, and a numeric entity key are interchangeable.

## Resource endpoints

The retained provider material mentions these resources:

| Resource | Historical endpoint path |
| --- | --- |
| Property | `/reso/odata/Property` |
| Member | `/reso/odata/Member` |
| Office | `/reso/odata/Office` |
| OpenHouse | `/reso/odata/OpenHouse` |
| Media | `/reso/odata/Media` |
| DataSystem | `/reso/odata/DataSystem` |
| Resource | `/reso/odata/Resource` |
| PropertyGreenVerification | `/reso/odata/PropertyGreenVerification` |
| PropertyUnitTypes | `/reso/odata/PropertyUnitTypes` |
| HistoryTransactional | `/reso/odata/HistoryTransactional` |
| Adu | `/reso/odata/Adu` |
| Lookup | `/reso/odata/Lookup` |
| Deleted | `/reso/odata/Deleted` |

See the [wrapper boundaries](index.md#protocol-and-wrapper-boundaries) before
assuming each resource has a main-client accessor. In particular, the current
main client has no Media, History, or Green Verification accessors.

## Ordering by modification time

A historical Property query sorts by `ModificationTimestamp` descending:

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=10 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
Accept: application/json
```

Illustrative response shape, with one historical record:

```json
{
    "@odata.context": "$metadata#Property",
    "value": [
        {
            "ListingKeyNumeric": 1611952,
            "ListPrice": 2950000.0,
            "ModificationTimestamp": "2019-10-03T10:04:24Z"
        }
    ]
}
```

This retrieves a page of recent records, not every change since a checkpoint.
For complete synchronization, use a timestamp filter and process all pages; see
[replication](replication.md). Encode spaces as `%20` in raw request targets.
The Python wrapper passes query parameters through `requests`, which handles
URL encoding. See [query options](query-options.md) for selection and filtering,
and the [Python client reference](../docs/api/client.md) for discovery methods.
