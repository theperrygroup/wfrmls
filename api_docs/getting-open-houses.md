# Getting Open Houses

This page preserves historical provider reference material. See the
[source and snapshot limitations](index.md#sources-and-snapshot-limits)
and [official provider documentation](https://docs.utahrealestate.com/).
Current account access and provider behavior have not been revalidated.

The Python wrapper exposes `client.openhouse` and the alias `client.open_house`.
See the [OpenHouse API reference](../docs/api/openhouse.md) for implemented
methods. This page explains historical provider request and response shapes.

## Getting recent open houses

The OpenHouse resource can be queried directly. Each OpenHouse resource record is related to a Property resource through the ListingKey or ListingKeyNumeric field.

For example, to get the most recent open houses and their ListingKeys:

`https://resoapi.utahrealestate.com/reso/odata/OpenHouse?$orderby=ModificationTimestamp desc`

```http
GET /reso/odata/OpenHouse?$orderby=ModificationTimestamp%20desc HTTP/1.1
Host: resoapi.utahrealestate.com
Authorization: Bearer YourBearerToken
```

Historical response example:

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

## Open House Start Time

The [schema snapshot](metadata.xml) declares `OpenHouseDate` as `Edm.Date`,
which contains no timezone, and the start/end fields as `Edm.DateTimeOffset`.
The sample start and end timestamps above use `Z`, meaning UTC. Preserve the
actual offset in a current response; do not attach a timezone to a date-only
value by assumption.

For local display, convert an offset-aware start timestamp to `America/Denver`
and derive the displayed day from that converted value. Utah observes daylight
saving time, so a fixed UTC−7 conversion is unsuitable year-round. See
[NIST's daylight saving guidance](https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst)
and [Python's IANA timezone support](https://docs.python.org/3/library/zoneinfo.html).

For Python 3.9 or newer, with IANA timezone data installed:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

start = datetime.fromisoformat("2019-10-05T12:00:00Z".replace("Z", "+00:00"))
local_start = start.astimezone(ZoneInfo("America/Denver"))
local_date = local_start.date()
```

`zoneinfo` is not in the Python 3.8 standard library. Applications supporting
Python 3.8 need their own compatible timezone library; the wrapper does not
supply one. Confirm the provider's current `OpenHouseDate` convention before
using that field for date-based filtering.
