---
description: Use the standalone MediaClient interface to construct media queries, numeric property filters, primary-photo lookups, and URL extraction requests.
---

# Standalone MediaClient queries

`MediaClient` remains exported from `wfrmls`, but `WFRMLSClient` has no `media` attribute. Instantiate the class directly to use this compatibility interface. Its methods and mocked tests establish request construction; current provider availability and account permissions have not been verified.

## Construct the client and query a page

`MediaClient(bearer_token=None, base_url=None)` resolves an explicit token or `WFRMLS_BEARER_TOKEN` immediately. Missing credentials raise `AuthenticationError`. See [BaseClient](base-client.md) for HTTP handling and the default service root.

`get_media(top=None, skip=None, filter_query=None, select=None, orderby=None, expand=None, count=None)` requests one `Media` page:

| Parameter | Type | Default | Request behavior |
| --- | --- | --- | --- |
| `top` | `int \| None` | `None` | `$top`; values above 200 are clamped |
| `skip` | `int \| None` | `None` | `$skip`, unchanged |
| `filter_query` | `str \| None` | `None` | Raw `$filter` expression |
| `select` | `list[str] \| str \| None` | `None` | `$select`; lists are joined with commas |
| `orderby` | `str \| None` | `None` | Raw `$orderby` expression |
| `expand` | `list[str] \| str \| None` | `None` | `$expand`; lists are joined with commas |
| `count` | `bool \| None` | `None` | `$count` as lowercase `true` or `false` |

`None` omits a parameter. The response is handled provider JSON, commonly a dictionary with `value`. This method does not paginate, validate field names, or download files.

This complete example uses a fake token and a mock, so it makes no provider request:

```python
from unittest.mock import patch
from wfrmls import MediaClient

with patch.object(MediaClient, "get", return_value={"value": []}) as request:
    media = MediaClient(bearer_token="example-token")
    response = media.get_photos_for_property("12345", top=5)
    assert response == {"value": []}
    request.assert_called_once_with(
        "Media",
        params={
            "$top": 5,
            "$filter": "ResourceRecordKeyNumeric eq 12345 and MediaType eq 'Photo'",
        },
    )
```

## Property filters and extraction helpers

| Method | Parameters | Result or request behavior |
| --- | --- | --- |
| `get_media_item` | `media_key: str` | Requests `Media('<key>')`; returns provider JSON without single-record normalization |
| `get_media_for_property` | `listing_key: str \| int`, `**kwargs` | Filters unquoted `ResourceRecordKeyNumeric` |
| `get_photos_for_property` | `listing_key: str \| int`, `**kwargs` | Adds `MediaType eq 'Photo'` |
| `get_media_by_category` | `listing_key: str \| int`, `category: str`, `**kwargs` | Adds a quoted `MediaCategory` condition |
| `get_primary_photo` | `listing_key: str \| int` | Queries photos with `Order eq 1`, `top=1`; returns the first object or `None` |
| `get_media_urls_for_property` | `listing_key: str \| int`, `media_type=None` | Returns `MediaURL` values from one page of at most 200 records, requested in `Order asc` order |
| `get_media_with_property` | `**kwargs` | Sets `$expand=Property` |
| `get_modified_media` | `since: str \| date \| datetime`, `**kwargs` | Sets a quoted `ModificationTimestamp gt '<cutoff>'` filter |

Use numeric strings or integers for property keys: the helpers interpolate them without quotes or numeric validation. Text keys, categories, and media types are inserted without escaping. The property/category helpers combine an existing `filter_query` using `and` without extra parentheses.

URL extraction skips records lacking a `MediaURL` key; it does not validate the values or fetch additional pages. `MediaType` and `MediaCategory` are package constants, not a current provider lookup list. Pass their `.value` strings where a helper expects text.

## Timestamp and keyword limitations

For `get_modified_media()`, strings are sent unchanged; dates become midnight with `Z`; datetimes use `isoformat()` plus `Z` without timezone conversion. An aware datetime can therefore produce `...+00:00Z`. Prefer an already-normalized UTC string and verify that the provider accepts the quoted filter.

Do not pass `filter_query` to `get_modified_media()` or `expand` to `get_media_with_property()`: those helpers supply the keyword themselves and duplicate keywords raise `TypeError`. Other `**kwargs` must match `get_media()`.

For media through the facade, [property media expansion](properties.md#use-the-supported-search-helpers) requests `$expand=Media`; server acceptance still requires verification. See [compatibility clients](unavailable-clients.md) and [provider verification](live-api-updates.md).

## Generated signatures and constants

::: wfrmls.media
    options:
      show_root_heading: false
      show_source: false
