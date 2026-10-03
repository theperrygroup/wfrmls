---
description: Query accessory dwelling unit records with AduClient, including exact OData parameters, type and status filters, and timestamp helper limitations.
---

# Accessory dwelling unit API

`AduClient` queries the `Adu` resource and returns the server's JSON response. Access it through `WFRMLSClient.adu` or construct it directly.

## Configure the client

```text
AduClient(bearer_token=None, base_url=None)
```

The constructor accepts a bearer token or reads `WFRMLS_BEARER_TOKEN`. Its default base URL is `https://resoapi.utahrealestate.com/reso/odata`.
Direct construction requires a token immediately. `WFRMLSClient` creates the ADU client lazily, so missing credentials raise `AuthenticationError` on first `.adu` access.

The examples require a configured `WFRMLS_BEARER_TOKEN`. Replace illustrative keys with keys from your data.
Use [service discovery](client.md) to inspect the provider's schema and available resources before choosing fields or relationships.

## Query one page of ADUs

```text
get_adus(top=None, skip=None, filter_query=None, select=None,
         orderby=None, expand=None, count=None) -> Dict[str, Any]
```

| Parameter | Accepted type | Request behavior |
| --- | --- | --- |
| `top` | `int` or `None` | Sends `$top=min(top, 200)` when provided. |
| `skip` | `int` or `None` | Sends `$skip` unchanged. |
| `filter_query` | `str` or `None` | Sends the expression as `$filter`. |
| `select` | `list[str]`, `str`, or `None` | Joins lists with commas for `$select`. |
| `orderby` | `str` or `None` | Sends `$orderby` unchanged. |
| `expand` | `list[str]`, `str`, or `None` | Joins lists with commas for `$expand`. |
| `count` | `bool` or `None` | Sends `$count=true` or `$count=false`; `None` omits it. |

The client does not validate field names, filter syntax, or negative pagination values. Supported fields and relationships depend on the provider.

```python
from wfrmls import AduStatus, WFRMLSClient

client = WFRMLSClient()
response = client.adu.get_adus(
    top=25,
    filter_query=f"AduStatus eq '{AduStatus.EXISTING.value}'",
    select=["AduKey", "ListingKey", "AduType", "AduStatus"],
    orderby="AduKey asc",
    count=True,
)

for adu in response.get("value", []):
    print(adu.get("AduKey"), adu.get("ListingKey"), adu.get("AduType"))
print("Count supplied by the server:", response.get("@odata.count"))
print("Next page supplied by the server:", response.get("@odata.nextLink"))
```

The method returns one response page, usually with a `value` list.
`@odata.context`, `@odata.count`, and `@odata.nextLink` are present only when the server supplies them.
The client preserves fields and values; it does not convert records into model objects or follow pagination links automatically.

`AduKey`, `ListingKey`, `AduType`, and `AduStatus` appear in client examples and mocked tests.
Those fixtures do not establish an exhaustive provider schema, rental data availability, or field types.

## Retrieve an ADU by key

```text
get_adu(adu_key: str) -> Dict[str, Any]
```

This method requests `Adu('<adu_key>')` and returns the single-record JSON dictionary directly, without a `value` wrapper added by the client.
A 404 response raises `NotFoundError`. The key is interpolated without escaping; use a trusted key.

## Use filters and relationship helpers

All helpers below return the same response shape as `get_adus()` and accept its query keywords through `**kwargs`.

| Method signature | Generated query |
| --- | --- |
| `get_adus_for_property(listing_key: str, **kwargs)` | `ListingKey eq '<listing_key>'` |
| `get_adus_by_type(adu_type: str, **kwargs)` | `AduType eq '<adu_type>'` |
| `get_adus_by_status(adu_status: str, **kwargs)` | `AduStatus eq '<adu_status>'` |
| `get_existing_adus(**kwargs)` | `AduStatus eq 'Existing'` |
| `get_permitted_adus(**kwargs)` | `AduStatus eq 'Permitted'` |
| `get_adus_with_property(**kwargs)` | Sets `expand="Property"`. |

The filter helpers append a supplied `filter_query` with `and` without adding parentheses.
Parenthesize your expression if it contains `or` and should apply as a group.
Keys, type names, and status names are interpolated without escaping; use trusted values or construct an escaped expression for `get_adus()`.

Pass `.value` when using an enum with the type or status helpers. These helpers expect strings and do not unwrap enum members.

| Enum | Members and string values |
| --- | --- |
| `AduType` | `DETACHED`: `Detached`; `ATTACHED`: `Attached`; `GARAGE_CONVERSION`: `Garage Conversion`; `BASEMENT`: `Basement`; `INTERIOR`: `Interior` |
| `AduStatus` | `EXISTING`: `Existing`; `PERMITTED`: `Permitted`; `PLANNED`: `Planned`; `UNDER_CONSTRUCTION`: `Under Construction` |

These constants describe the library's filters; they do not restrict values returned by the provider.
`get_adus_with_property()` fixes `expand`, so passing another `expand` raises `TypeError`. Use `get_adus()` to choose relationships yourself.

## Query modified ADUs

```text
get_modified_adus(since: Union[str, date, datetime], **kwargs) -> Dict[str, Any]
```

This method sets `filter_query="ModificationTimestamp gt '<timestamp>'"` and forwards other query keywords to `get_adus()`.
Passing `filter_query` also raises `TypeError`; use `get_adus()` when combining a timestamp with another filter.

| `since` input | Conversion performed by the helper |
| --- | --- |
| `str` | Used unchanged inside the quoted filter literal. |
| `date` | Converted to `YYYY-MM-DDT00:00:00Z`. |
| `datetime` | Converted with `isoformat()`, then appended with `Z`. |

The helper does not convert time zones. An aware datetime produces an offset followed by `Z`, such as `+00:00Z`.
Pass a normalized UTC string to avoid that malformed combination.

```python
from datetime import datetime, timedelta, timezone

from wfrmls import AduType, WFRMLSClient

client = WFRMLSClient()
property_adus = client.adu.get_adus_for_property(
    listing_key="1611952",
    filter_query="(AduStatus eq 'Existing' or AduStatus eq 'Permitted')",
    top=25,
)
detached_adus = client.adu.get_adus_by_type(AduType.DETACHED.value, top=25)
cutoff = datetime.now(timezone.utc) - timedelta(days=1)
cutoff_utc = cutoff.isoformat().replace("+00:00", "Z")
updates = client.adu.get_modified_adus(
    since=cutoff_utc,
    orderby="ModificationTimestamp asc",
    top=200,
)

print("Property page:", len(property_adus.get("value", [])))
print("Detached page:", len(detached_adus.get("value", [])))
print("Modified page:", len(updates.get("value", [])))
```

## Handle request failures

These methods use the shared HTTP client. It maps HTTP 400, 401, 404, 429, and 5xx responses to `ValidationError`, `AuthenticationError`, `NotFoundError`, `RateLimitError`, and `ServerError`.
Request exceptions raise `NetworkError`; other unsuccessful statuses raise `WFRMLSError`.
There is no automatic retry or pagination in these helpers.

See [error handling](../guides/error-handling.md) and the [main client reference](client.md) for shared behavior.
