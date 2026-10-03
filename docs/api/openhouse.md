---
description: Query MLS open houses by listing, agent, date range, status, and modification time, with documented date-helper limitations.
---

# Open house API reference

`OpenHouseClient` requests the `OpenHouse` resource. It supports collection and
key queries, property expansion, and helpers for listing, showing-agent, date,
and status filters.

## Configure access

Use `WFRMLSClient().openhouse` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`openhouse`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.


`client.open_house` is an alias for `client.openhouse`; both return the same cached
resource client.

## Query open house records

```text
get_open_houses(top=None, skip=None, filter_query=None, select=None,
             orderby=None, expand=None, count=None) -> Dict[str, Any]
```

| Parameter | Accepted value | Default | Request behavior |
| --- | --- | --- | --- |
| `top` | `int` | `None` | Sends `$top`, capped at 200 |
| `skip` | `int` | `None` | Sends `$skip` |
| `filter_query` | `str` | `None` | Sends the OData expression as `$filter` |
| `select` | `list[str]` or `str` | `None` | Sends `$select`; lists become comma-separated strings |
| `orderby` | `str` | `None` | Sends `$orderby` |
| `expand` | `list[str]` or `str` | `None` | Sends `$expand`; lists become comma-separated strings |
| `count` | `bool` | `None` | Sends `$count=true` or `$count=false` when provided |

`None` omits a parameter. The client forwards filters and field names without
checking them against the service schema. Check your service metadata for supported
fields, relationships, and value types. The 200-record cap is applied locally;
negative pagination values are not validated locally.

The method requests `OpenHouse` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve one open house

`get_open_house(open_house_key: str) -> Dict[str, Any]` requests
`OpenHouse('<key>')` and returns the record dictionary. HTTP 404 raises
`NotFoundError`.

## Use open house helpers

Every helper returns a collection response dictionary and forwards `**kwargs` to
`get_open_houses()`.

| Method | Actual request behavior |
| --- | --- |
| `get_open_houses_for_property(listing_key: str, **kwargs)` | Filters `ListingKey eq '<key>'` |
| `get_open_houses_by_agent(agent_key: str, **kwargs)` | Filters `ShowingAgentKey eq '<key>'` |
| `get_active_open_houses(**kwargs)` | Sets `OpenHouseStatus eq 'Active'` |
| `get_open_houses_with_property(**kwargs)` | Sets `expand="Property"` |
| `get_open_houses_by_date_range(start_date, end_date, **kwargs)` | Uses inclusive `OpenHouseDate ge <start> and OpenHouseDate le <end>` |
| `get_upcoming_open_houses(days_ahead: Optional[int] = 7, **kwargs)` | Adds `OpenHouseDate ge <local today>` when `days_ahead` is not `None` |
| `get_weekend_open_houses(weeks_ahead: Optional[int] = 2, **kwargs)` | Adds `OpenHouseDate ge <local today>`; does not restrict weekdays or weeks |
| `get_modified_open_houses(since: Union[str, date, datetime], **kwargs)` | Filters `ModificationTimestamp`; timestamp handling is described below |

Listing, agent, date-range, upcoming, and weekend helpers combine an additional
`filter_query` with `and`. Use parentheses around additional expressions containing
`or`. String keys are interpolated directly; escape apostrophes as doubled quotes.

Do not pass `filter_query` to `get_active_open_houses()` or `expand` to
`get_open_houses_with_property()`: duplicates raise `TypeError`.

### Date helper limitations

`get_upcoming_open_houses(days_ahead=7)` does **not** add a seven-day upper bound.
Any non-`None` value adds the same lower bound; `None` suppresses that added filter.
`get_weekend_open_houses(weeks_ahead=2)` ignores `weeks_ahead` and does **not**
filter for Saturday or Sunday. Neither helper automatically filters active events.
Their local date comes from the machine running the client.

Use `get_open_houses_by_date_range()` for a bounded schedule. Both dates accept
ISO date strings, `date`, or `datetime`; datetimes are reduced to their date.
The helper does not validate date ordering or normalize string input.

## Query a bounded active schedule

Set `WFRMLS_BEARER_TOKEN` before running this example. The range includes both
endpoints. Change these dates to the schedule you need.

```python
import os
from datetime import date

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.openhouse.get_open_houses_by_date_range(
    date(2026, 10, 3),
    date(2026, 10, 4),
    filter_query="OpenHouseStatus eq 'Active'",
    orderby="OpenHouseDate asc,OpenHouseKey asc",
    top=50,
)
for event in response.get("value", []):
    print(event.get("OpenHouseKey"), event.get("OpenHouseDate"))
```

## Find events for one listing

Replace `listing-key` with a listing key. This example filters one collection page
and requests its `Property` relationship without assuming the relationship exists.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.openhouse.get_open_houses_for_property(
    "listing-key",
    expand="Property",
    top=50,
)
for event in response.get("value", []):
    property_record = event.get("Property") or {}
    print(event.get("OpenHouseKey"), property_record.get("ListingKey"))
```

## Query modified records

`get_modified_open_houses(since, **kwargs)` builds `ModificationTimestamp gt '<timestamp>'`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDT00:00:00Z`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


## Interpret fields and enums

Query helpers use `OpenHouseDate`, `OpenHouseStatus`, `ListingKey`,
`ShowingAgentKey`, and `ModificationTimestamp`. Key lookups use `OpenHouseKey`.
The client returns JSON values unchanged; consult metadata for event times,
addresses, time zones, field types, and related records.

The `wfrmls.openhouse` module defines these constants:

| Enum | Members and values |
| --- | --- |
| `OpenHouseStatus` | `ACTIVE="Active"`, `ENDED="Ended"`, `CANCELLED="Cancelled"`, `COMPLETED="Completed"` |
| `OpenHouseType` | `PUBLIC="Public"`, `PRIVATE="Private"`, `BROKER="Broker"` |
| `OpenHouseAttendedBy` | `AGENT="Agent"`, `OWNER="Owner"`, `NONE="None"`, `LISTING_AGENT="ListingAgent"`, `BUYER_AGENT="BuyerAgent"` |

Enums do not validate provider values. Use `.value` to build a string filter.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Property records](properties.md) for listing keys.
- [Member records](members.md) for showing-agent keys.
- [OData queries](../guides/odata-queries.md) for explicit date and status filters.
