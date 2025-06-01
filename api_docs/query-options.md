# Query Options

## Query Options

### $select

The **$select** query option can be used to request limited fields in the results set.

`https://resoapi.utahrealestate.com/reso/odata/Property?$select=ListingKey,ListPrice,YearBuilt`

```http
GET /reso/odata/Property?$select=ListingKey,ListPrice,YearBuilt HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Property(ListPrice,YearBuilt,ListingKey)",
    "value": [
        {
            "ListPrice": 222500.0,
            "YearBuilt": 1964,
            "ListingKey": "543141"
        },
        {
            "ListPrice": 265000.0,
            "YearBuilt": 1977,
            "ListingKey": "549289"
        },
        {
            "ListPrice": 450000.0,
            "YearBuilt": 1956,
            "ListingKey": "1622752"
        }
    ]
}
```

### $filter

Each resource can be filtered on various fields and data types using the $filter query option.

Properties with more than 3 bedrooms (Number):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=BedroomsTotal gt 3`

```http
GET /reso/odata/Property?$filter=BedroomsTotal%20gt%203 HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties in the price range 300,000 - 500,000 (Decimal):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ListPrice ge 300000 and ListPrice le 500000`

```http
GET /reso/odata/Property?$filter=ListPrice%20ge%20300000%20and%20ListPrice%20le%20500000 HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties that have air conditioning (Boolean):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=CoolingYN eq true`

```http
GET /reso/odata/Property?$filter=CoolingYN%20eq%20true HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties listed since a given date (Date):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ListingContractDate gt 2018-01-01`

```http
GET /reso/odata/Property?$filter=ListingContractDate%20gt%202018-01-01 HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties updated since a given date (Timestamp):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ModificationTimestamp gt 2019-09-01T01:00:00Z`

```http
GET /reso/odata/Property?$filter=ModificationTimestamp%20gt%202019-09-01T01:00:00Z HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties with Active status (Single Lookup):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=StandardStatus has Odata.Models.StandardStatus'Active'`

```http
GET /reso/odata/Property?$filter=StandardStatus%20has%20Odata.Models.StandardStatus'Active' HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Properties with certain exterior features ExteriorFeatures (Multi Lookup):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ExteriorFeatures%20has%20Odata.Models.ExteriorFeatures'Balcony'`

```http
GET /reso/odata/Property?$filter=ExteriorFeatures%20has%20Odata.Models.ExteriorFeatures'Balcony' HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

### $top and $skip

The web API has a limit on how many records can be pulled at once. Currently, the limit is set to 200 records per request.

The **$top** and **$skip** query options can be used to offset the result set.

For example, to get the 600 most recent listings, make 3 requests using **$top** and **$skip**:

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200&$skip=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200&$skip=400`

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200 HTTP/1.1
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200&$skip=200 HTTP/1.1
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200&$skip=400 HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Using the **$skip** option to paginate over large data sets can be time consuming. Especially when ordering by a non numeric, or non indexed field. As the **$skip** value gets larger, query response time may slow down. If paginating through a large data set, it is advised to order by the primary key, or an indexed field. For example, if replicating the entire Property resource, ordering by ListingKeyNumeric would be the fastest. See the Replication section for more information.

### $count

The total number of records for a given resource can be included in the result set by using the **$count** option.

`https://resoapi.utahrealestate.com/reso/odata/Property?$count=true`

```http
GET /reso/odata/Property?$count=true HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Property",
    "@odata.count": 1731072,
    "value": [
        {
            // Property data
        }
    ]
}
```

### $expand

The web API can return related resources with each record using the **$expand** query option.

For example, to get all images for each property in addition to the data:

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