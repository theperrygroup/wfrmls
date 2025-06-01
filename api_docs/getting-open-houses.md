# Getting Open Houses

## Open Houses

### Getting recent open houses

The OpenHouse resource can be queried directly. Each OpenHouse resource record is related to a Property resource through the ListingKey or ListingKeyNumeric field

For example, to get the most recent open houses and their ListingKeys:

`https://resoapi.utahrealestate.com/reso/odata/OpenHouse?$orderby=ModificationTimestamp desc`

```http
GET https://resoapi.utahrealestate.com/reso/odata/OpenHouse?$orderby=ModificationTimestamp desc HTTP/1.1
Host: https://resoapi.utahrealestate.com
Authorization: YourBearerToken
```

Response:

```json
{
    "@odata.context": "$metadata#OpenHouse",
    "value": [
        {
            "OpenHouseKeyNumeric": 306227,
            "ListingKeyNumeric": 1625740,
            "ShowingAgentKeyNumeric": 96422,
            "ListingId": "1625740",
            "ListingKey": "1625740",
            "OpenHouseId": "306227",
            "OpenHouseKey": "306227",
            "OriginatingSystemID": "M00000628",
            "OriginatingSystemKey": "M00000628",
            "OriginatingSystemName": "UtahRealEstate.com",
            "ShowingAgentFirstName": "Elizabeth",
            "ShowingAgentKey": "96422",
            "ShowingAgentLastName": "Covington",
            "ShowingAgentMlsID": "96422",
            "SourceSystemID": "M00000628",
            "SourceSystemKey": "M00000628",
            "SourceSystemName": "UtahRealEstate.com",
            "OpenHouseDate": "2019-10-05",
            "ModificationTimestamp": "2019-10-02T22:02:01Z",
            "OpenHouseEndTime": "2019-10-05T14:00:00Z",
            "OpenHouseStartTime": "2019-10-05T12:00:00Z",
            "OriginalEntryTimestamp": "2019-10-02T22:02:01Z",
            "OpenHouseAttendedBy": "Agent",
            "OpenHouseStatus": "Ended",
            "OpenHouseType": ""
        }
    ]
}
```

### Open House Start Time

OpenHouseDate, OpenHouseStartTime and OpenHouseEndTime are in UTC. The UTC offset for Utah is -7. If an open house is scheduled in the evening, the OpenHouseDate may show the next day. The most reliable way to get the day of an open house is to get it from OpenHouseStartTime. 