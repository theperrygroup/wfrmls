---
description: Identify Media, HistoryTransactional, and PropertyGreenVerification compatibility classes that remain exported but are absent from the WFRMLSClient facade.
---

# Media, history, and green compatibility clients

`WFRMLSClient` has no `media`, `history`, or `green` property. Calling those attributes raises `AttributeError`. The package still exports three standalone classes with request-building helpers.

## Exported classes and entity paths

| Exported class | Collection path | Key method |
| --- | --- | --- |
| `MediaClient` | `Media` | `get_media_item(media_key)` |
| `HistoryTransactionalClient` | `HistoryTransactional` | `get_history_transaction(transaction_key)` |
| `GreenVerificationClient` | `PropertyGreenVerification` | `get_green_verification(verification_key)` |

Their constructors require a token, as other service clients do. Methods exist and are covered by mocked tests; that does not establish current provider availability or access permissions. Earlier comments about outages and missing entity types are historical claims without fresh verification.

Use service discovery and metadata to inspect your account before relying on these compatibility interfaces. The ordinary facade supports [property media expansion](properties.md#use-the-supported-search-helpers), which requests `$expand=Media`; the server still decides whether that relationship is accepted.

## Verify the interface without a provider call

This complete example uses a mock and a fake token. It validates the request-building interface only:

```python
from unittest.mock import patch
from wfrmls import MediaClient, WFRMLSClient

assert not hasattr(WFRMLSClient(), "media")
with patch.object(MediaClient, "get", return_value={"value": []}) as request:
    media = MediaClient(bearer_token="example-token")
    result = media.get_photos_for_property("12345", top=5)
    assert result == {"value": []}
    request.assert_called_once_with(
        "Media",
        params={"$top": 5, "$filter": "ResourceRecordKeyNumeric eq 12345 and MediaType eq 'Photo'"},
    )
```

## Compatibility-helper limitations

- Media key lookup quotes the key. Property-media filters interpolate `ResourceRecordKeyNumeric` without quotes; pass a numeric string or integer.
- `get_primary_photo()` returns the first matching object or `None`; URL extraction returns a list from one page of at most 200 records.
- History key lookup quotes the transaction key. Property-history and green helpers quote `ListingKey` strings.
- Media/history modification helpers append `Z` to datetime input without converting its timezone. Prefer an already-normalized UTC string; their filters quote the timestamp.
- `get_recent_sales()` uses a local naive datetime cutoff. It does not fetch every sale or calculate analytics.
- Fixed-filter or fixed-expansion helpers cannot accept a duplicate `filter_query` or `expand` through `**kwargs`.

None of these clients adds automatic retries, endpoint restoration, or pagination. See [provider verification](live-api-updates.md) and [shared HTTP handling](base-client.md).
