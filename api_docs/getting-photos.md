# Getting Photos

## Photos

### Getting photos with $expand

The easiest way to get the photos for each listing is to use the **$expand** query option to append all Media resources that match with each property.

For example, to get all images for each returned property.

`https://resoapi.utahrealestate.com/reso/odata/Property?$expand=Media`

```http
GET /reso/odata/Property?$expand=Media HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
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
                    "MediaURL": "https://.....jpg"
                }
            ]
        }
    ]
}
```

### Getting photos directly

The Media resource can be queried directly. Each Media resource record is relataed to a Property resource through the ResourceRecordKeyNumeric field. Note that as of DD 1.7 ResourceRecordID and ResourceRecordKey are Strings and need to be surrounded with single quotes in the query string.

For example, to get all images for a listing with a ListingKey of 1611952:

`https://resoapi.utahrealestate.com/reso/odata/Media?$filter=ResourceRecordKeyNumeric eq 1611952&$select=MediaURL`

```http
GET /reso/odata/Media?$filter=ResourceRecordKeyNumeric%20eq%201611952&$select=MediaURL HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
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

You can also get the photos for a single listing by adding the Media resource to the end of a single lookup query.

`https://resoapi.utahrealestate.com/reso/odata/Property(1655273)/Media`

```http
GET /reso/odata/Property(1655273)/Media HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
``` 