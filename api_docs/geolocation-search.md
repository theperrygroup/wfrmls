# Geolocation Search

## Geolocation Search

### Radius Search

The web API can search for Properties within a given radius.

For example, the following query returns all Properties within 1 mile of the given latitude and longitude:

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=geo.distance(GeoLocation,geography'SRID=3956;POINT(-111.898248 40.576672)') lt 1`

```http
GET /reso/odata/Property?$filter=geo.distance(GeoLocation,geography%27SRID=3956;POINT(-111.898248%2040.576672)%27)%20lt%201 HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

### Polygon

The web API also supports searching polygons using latitude and longitude coordinates.

For example, a polygon selection in Sandy city:

`https://resoapi.utahrealestate.com/reso/odata/Property?$filter=geo.intersects(GeoLocation,geography%27SRID=3956;POLYGON((-111.85518354177475%2040.60508413156539,-111.85518354177475%2040.55798337746534,-111.89896021038294%2040.55798337746534,-111.89896021038294%2040.60508413156539,-111.85518354177475%2040.60508413156539))%27)&$top=100&$select=StreetNumber,StreetName,PostalCode`

```http
GET /Property?$filter=geo.intersects(GeoLocation,geography'SRID=3956;POLYGON((-111.85518354177475%2040.60508413156539,-111.85518354177475%2040.55798337746534,-111.89896021038294%2040.55798337746534,-111.89896021038294%2040.60508413156539,-111.85518354177475%2040.60508413156539))')&$top=100&$select=StreetNumber,StreetName,PostalCode HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#Property(PostalCode,StreetName,StreetNumber)",
    "value": [
        {
            "@odata.id": "Property(1001613)",
            "PostalCode": "84093",
            "StreetName": "1480",
            "StreetNumber": "9261"
        }
    ]
}
``` 