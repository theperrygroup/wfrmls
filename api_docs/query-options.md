# Query Options

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

These examples describe the provider wire protocol. In the wrapper, use `select`,
`filter_query`, `top`, `skip`, `count`, `orderby`, and `expand` with
`client.property.get_properties()`. See the [property API reference](../docs/api/properties.md)
for exact signatures and the [OData guide](../docs/guides/odata-queries.md) for Python examples.

## $select

The **$select** query option can be used to request limited fields in the results set.

`https://resoapi.utahrealestate.com/reso/odata/Property?$select=ListingKey,ListPrice,YearBuilt`

```http
GET /reso/odata/Property?$select=ListingKey,ListPrice,YearBuilt HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
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

## $filter

Each resource can be filtered on various fields and data types using the $filter query option.

Properties with more than 3 bedrooms (Number):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=BedroomsTotal gt 3`

```http
GET /reso/odata/Property?$filter=BedroomsTotal%20gt%203 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Properties in the price range 300,000 - 500,000 (Decimal):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ListPrice ge 300000 and ListPrice le 500000`

```http
GET /reso/odata/Property?$filter=ListPrice%20ge%20300000%20and%20ListPrice%20le%20500000 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Properties that have air conditioning (Boolean):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=CoolingYN eq true`

```http
GET /reso/odata/Property?$filter=CoolingYN%20eq%20true HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Properties listed since a given date (Date):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ListingContractDate gt 2018-01-01`

```http
GET /reso/odata/Property?$filter=ListingContractDate%20gt%202018-01-01 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Properties updated since a given date (Timestamp):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ModificationTimestamp gt 2019-09-01T01:00:00Z`

```http
GET /reso/odata/Property?$filter=ModificationTimestamp%20gt%202019-09-01T01:00:00Z HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Properties with Active status (single enum in the [schema snapshot](metadata.xml)):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=StandardStatus eq Odata.Models.StandardStatus'Active'`

```http
GET /reso/odata/Property?$filter=StandardStatus%20eq%20Odata.Models.StandardStatus'Active' HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

The snapshot marks `StandardStatus` as a non-flag enum and `ExteriorFeatures` as
a flag enum, so the examples use `eq` for the former and `has` for the latter.
The wrapper's convenience filters use string comparisons such as
`StandardStatus eq 'Active'`; confirm the accepted literal syntax for your
current account rather than assuming every historical enum form is supported.

Properties with a Balcony exterior feature (flag enum):

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=ExteriorFeatures%20has%20Odata.Models.ExteriorFeatures'Balcony'`

```http
GET /reso/odata/Property?$filter=ExteriorFeatures%20has%20Odata.Models.ExteriorFeatures'Balcony' HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

## $top and $skip

The retained provider material uses 200 records per page. Treat that as a
historical example: current page limits can depend on vendor configuration. The
Python property collection method caps a supplied `top` at 200, independently of
the provider configuration. A page size is not a request-rate quota.

The **$top** option requests a page size; **$skip** offsets the result set.

For a static result set with 200-record pages, these three requests cover 600
records using **$top** and **$skip**. A changing result set can shift between
requests; this is a pagination example, not a consistent snapshot guarantee:

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200&$skip=200`

`https://resoapi.utahrealestate.com/reso/odata/Property?$orderby=ModificationTimestamp desc&$top=200&$skip=400`

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200&$skip=200 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

```http
GET /reso/odata/Property?$orderby=ModificationTimestamp%20desc&$top=200&$skip=400 HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Using the **$skip** option to paginate over large data sets can be time consuming. Especially when ordering by a non numeric, or non indexed field. As the **$skip** value gets larger, query response time may slow down. If paginating through a large data set, it is advised to order by the primary key, or an indexed field. For example, if replicating the entire Property resource, the historical guide recommends ordering by `ListingKeyNumeric`. Actual performance
depends on the provider and query. See [replication](replication.md) for the
numeric-key alternative and completeness considerations.

## $count

The **$count** option asks the provider to include the matching record count.
The historical number below is illustrative; it is not a current inventory
count and does not prove that all pages of a scan were fetched.

`https://resoapi.utahrealestate.com/reso/odata/Property?$count=true`

```http
GET /reso/odata/Property?$count=true HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Property",
    "@odata.count": 1731072,
    "value": [
        {
            "ListingKeyNumeric": 1611952
        }
    ]
}
```

## $expand

The historical API material describes related resources returned through the
**$expand** option. Available relationships and media access must be confirmed
against current account metadata; see [getting photos](getting-photos.md).

For example, to request related Media with property data:

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
