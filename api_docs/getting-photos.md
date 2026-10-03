# Getting Photos

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

## Wrapper access and provider availability

`client.property.get_properties_with_media()` implements a request with
`$expand=Media`, but expanded media depends on provider access and behavior.
The current `WFRMLSClient` has no `client.media` accessor. A standalone
`MediaClient` remains exported; its existence does not establish current direct
Media endpoint availability. See the [property API reference](../docs/api/properties.md)
and [wrapper boundaries](index.md#protocol-and-wrapper-boundaries).

## Historical provider patterns

### Getting photos with $expand

The retained provider material uses **$expand=Media** to include related media
with each property. Inspect the actual response for available media and any
provider-imposed omissions; expansion is not a guarantee that all photos are
returned or permitted for redistribution.

For example, to request related Media for each returned property:

`https://resoapi.utahrealestate.com/reso/odata/Property?$expand=Media`

```http
GET /reso/odata/Property?$expand=Media HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Property",
    "value": [
        {
            "ListingKeyNumeric": 1723791,
            "AssociationFee": 0,
            "RoomsTotal": 18,
            "Media": [
                {
                    "Order": 1,
                    "ResourceRecordKeyNumeric": 1723791,
                    "ResourceRecordID": "1723791",
                    "ResourceRecordKey": "1723791",
                    "LongDescription": "",
                    "MediaURL": "https://example.com/property-photo.jpg"
                }
            ]
        }
    ]
}
```

### Getting photos directly

The retained material also queries Media directly and joins it to Property
through `ResourceRecordKeyNumeric`. The retained DD 1.7-era material and schema snapshot describe `ResourceRecordID`
and `ResourceRecordKey` as strings, which are quoted in filter literals. The
`ResourceRecordKeyNumeric` example below uses an unquoted numeric value. Confirm
these field types against current metadata before using a direct provider query.

For example, the historical query for `ListingKeyNumeric` 1611952 selects photo
URLs with their order and sorts by that order:

`https://resoapi.utahrealestate.com/reso/odata/Media?$filter=ResourceRecordKeyNumeric eq 1611952&$select=Order,MediaURL&$orderby=Order`

```http
GET /reso/odata/Media?$filter=ResourceRecordKeyNumeric%20eq%201611952&$select=Order,MediaURL&$orderby=Order HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Media(Order,MediaURL)",
    "value": [
        {
            "@odata.id": "Media(1611952_050774e9ef920b479d8e37ff459daf14_2880536.jpg)",
            "Order": 1,
            "MediaURL": "https://assets.utahrealestate.com/photos/640x480/1611952_050774e9ef920b479d8e37ff459daf14_2880536.jpg"
        },
        {
            "@odata.id": "Media(1611952_07fcb738e3bc6496ebeef1e03bce600c_2749934.jpg)",
            "Order": 2,
            "MediaURL": "https://assets.utahrealestate.com/photos/640x480/1611952_07fcb738e3bc6496ebeef1e03bce600c_2749934.jpg"
        },
        {
            "@odata.id": "Media(1611952_0d95fd7d205ec4674bc42b70d96011d9_2414957.jpg)",
            "Order": 3,
            "MediaURL": "https://assets.utahrealestate.com/photos/640x480/1611952_0d95fd7d205ec4674bc42b70d96011d9_2414957.jpg"
        }
    ]
}
```

The retained material also shows navigation from a numeric Property entity key
to Media. This is a raw provider path; there is no main-client Media navigation
method implied by the example. Confirm the entity key and relationship in
current metadata:

`https://resoapi.utahrealestate.com/reso/odata/Property(1655273)/Media`

```http
GET /reso/odata/Property(1655273)/Media HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

See [query options](query-options.md) for field selection and relationship expansion.
Photo URLs and records above are historical examples, not current media evidence.
