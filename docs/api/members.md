---
description: Query MLS members by key, MLS ID, name, office, status, or modification timestamp with the WFRMLS MemberClient.
---

# Member API reference

`MemberClient` requests the `Member` resource for MLS participant records. It
provides list, key, MLS ID, name, office, and modification-time queries; it does
not verify professional licenses or normalize provider fields.

## Configure access

Use `WFRMLSClient().member` after setting `WFRMLS_BEARER_TOKEN`, or pass a token
to `WFRMLSClient(bearer_token=...)`. The main client creates resource clients
lazily; missing credentials raise `AuthenticationError` when you first access
`member`. Direct resource client construction validates credentials immediately.

Both constructors accept `bearer_token: Optional[str] = None` and
`base_url: Optional[str] = None`. The default resource URL is
`https://resoapi.utahrealestate.com/reso/odata`.

## Query member records

```text
get_members(top=None, skip=None, filter_query=None, select=None,
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

The method requests `Member` and returns the response dictionary unchanged.
Collection responses normally contain a `value` list. `@odata.count`,
`@odata.context`, and `@odata.nextLink` may be present. Empty collections return an
empty `value` list rather than `None`.

Each call retrieves one page. It does not follow `@odata.nextLink`, accumulate all
records, or retry failed requests. See [pagination](../guides/odata-queries.md).


## Retrieve one member

| Method | Request and return value |
| --- | --- |
| `get_member(member_key: str) -> Dict[str, Any]` | Requests `Member('<key>')`; returns the record dictionary; HTTP 404 raises `NotFoundError` |
| `get_member_by_mls_id(mls_id: str) -> Dict[str, Any]` | Requests a collection with `MemberMlsId eq '<id>'`, `expand="Office"`, and `top=1`; returns its first record |

The MLS ID method raises `NotFoundError` when the response has no records. It does
not test whether an MLS ID is unique. Expanded office fields depend on the service;
the client does not flatten the `Office` relationship.

## Use member helpers

Each helper returns a collection response dictionary and forwards its `**kwargs`
to `get_members()`.

| Method | Filter or expansion |
| --- | --- |
| `get_active_members(**kwargs)` | Sets `MemberStatus eq 'Active'` |
| `get_members_by_office(office_key: str, **kwargs)` | Sets `OfficeKey eq '<key>'`; appends an additional filter with `and` |
| `search_members_by_name(first_name=None, last_name=None, **kwargs)` | Uses `contains(MemberFirstName, '<name>')` and/or `contains(MemberLastName, '<name>')`; combines both with `and` |
| `get_members_with_office(**kwargs)` | Sets `expand="Office"` |
| `get_modified_members(since: Union[str, date], **kwargs)` | Filters `ModificationTimestamp`; timestamp handling is described below |

`first_name` and `last_name` accept strings or `None`. With neither name supplied,
the search helper calls `get_members(**kwargs)` without adding a name filter.
With a name supplied, do not pass a separate `filter_query`. Likewise, do not pass
`filter_query` to the active helper or `expand` to the office-expansion helper.
Those keywords would conflict with the helper's arguments and raise `TypeError`.

Name, office, and MLS ID helpers interpolate strings directly. Escape apostrophes
as doubled quotes when constructing an OData string literal. Parenthesize an
additional filter containing `or` before combining it with an office condition.

## Read an office's active members

Set `WFRMLS_BEARER_TOKEN` before running this example. Replace `office-key` with
an office key returned by your service. This retrieves one page.

```python
import os

from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
response = client.member.get_members_by_office(
    "office-key",
    filter_query="MemberStatus eq 'Active'",
    select=["MemberKey", "MemberFirstName", "MemberLastName"],
    orderby="MemberLastName asc,MemberKey asc",
    top=50,
    count=True,
)
for member in response.get("value", []):
    print(member.get("MemberKey"), member.get("MemberLastName"))
print("Matching records:", response.get("@odata.count"))
```

## Look up a member by MLS ID

Replace `member-mls-id` with an MLS ID. This example handles an empty lookup without
assuming a collection response from the MLS ID helper.

```python
import os

from wfrmls import WFRMLSClient
from wfrmls.exceptions import NotFoundError

client = WFRMLSClient(bearer_token=os.environ["WFRMLS_BEARER_TOKEN"])
try:
    member = client.member.get_member_by_mls_id("member-mls-id")
except NotFoundError:
    print("No matching member")
else:
    print(member.get("MemberKey"), member.get("MemberFirstName"))
```

## Query modified records

`get_modified_members(since, **kwargs)` builds `ModificationTimestamp gt <timestamp>`. Pass an ISO 8601 UTC string such as
`2026-01-01T00:00:00Z` to control the timestamp representation. Strings are not
normalized or validated. Do not also supply `filter_query`: the helper supplies
that keyword itself.

A `date` becomes `YYYY-MM-DDZ`. Datetime objects are serialized with `isoformat()` followed by `Z`;
timezone-aware datetimes can therefore produce an offset followed by `Z`.
Prefer an explicit UTC string. If the service requires different temporal literal
syntax, construct the expression with the collection method's `filter_query`.


## Interpret fields and enums

The client returns JSON fields without converting values. Common fields used by
the implementation and tests include `MemberKey`, `MemberMlsId`,
`MemberFirstName`, `MemberLastName`, `MemberFullName`, `MemberEmail`,
`MemberPreferredPhone`, `MemberStatus`, `OfficeKey`, and `OfficeName`.
An expanded `Office` may contain the related record. Fields may be absent or null;
use metadata to establish the schema required by your application.

`wfrmls.member.MemberStatus` defines `ACTIVE="Active"`, `INACTIVE="Inactive"`,
and `SUSPENDED="Suspended"`. `MemberType` defines `AGENT="Agent"`,
`BROKER="Broker"`, and `ASSISTANT="Assistant"`. These enums do not enforce
service lookup values. Use `.value` when building a filter; passing an enum itself
does not automatically serialize its string value.

## Handle errors

HTTP 400 raises `ValidationError`; HTTP 401 raises `AuthenticationError`; HTTP 404
raises `NotFoundError`; HTTP 429 raises `RateLimitError`; HTTP 5xx raises
`ServerError`. Request failures raise `NetworkError`. Other unsuccessful responses
raise `WFRMLSError`. See the [exception reference](exceptions.md) for details.


## Related references

- [Office records](offices.md) for office keys and brokerage queries.
- [Lookup values](lookup.md) for service-defined categories.
- [Authentication](../getting-started/authentication.md) for credential setup.
