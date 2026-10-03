---
description: Use the standalone GreenVerificationClient signatures for PropertyGreenVerification collections, quoted key lookups, and property filters.
---

# Standalone green-verification queries

`GreenVerificationClient` remains exported from `wfrmls`, but `WFRMLSClient` has no `green` attribute. Instantiate this compatibility class directly. Source and mocked tests establish its interface; current provider availability, schema, and account permissions have not been verified.

## Construct the client and query a page

`GreenVerificationClient(bearer_token=None, base_url=None)` resolves an explicit token or `WFRMLS_BEARER_TOKEN` immediately. Missing credentials raise `AuthenticationError`. See [BaseClient](base-client.md) for the default service root, sessions, and error handling.

`get_green_verifications(top=None, skip=None, filter_query=None, select=None, orderby=None, expand=None, count=None)` requests one `PropertyGreenVerification` collection page.

| Parameter | Type | Default | Request behavior |
| --- | --- | --- | --- |
| `top` | `int \| None` | `None` | `$top`; values above 200 are clamped |
| `skip` | `int \| None` | `None` | `$skip`, unchanged |
| `filter_query` | `str \| None` | `None` | Raw `$filter` |
| `select` | `list[str] \| str \| None` | `None` | `$select`; lists are joined with commas |
| `orderby` | `str \| None` | `None` | Raw `$orderby` |
| `expand` | `list[str] \| str \| None` | `None` | `$expand`; lists are joined with commas |
| `count` | `bool \| None` | `None` | Lowercase `$count` value |

`None` omits a parameter. The result is handled provider JSON, commonly a dictionary with `value`. The method does not paginate or validate field names, filter syntax, or positive pagination values.

This complete example validates the property filter with a fake token and a mock:

```python
from unittest.mock import patch
from wfrmls import GreenVerificationClient

with patch.object(GreenVerificationClient, "get", return_value={"value": []}) as request:
    green = GreenVerificationClient(bearer_token="example-token")
    response = green.get_verifications_for_property("12345", top=5)
    assert response == {"value": []}
    request.assert_called_once_with(
        "PropertyGreenVerification",
        params={"$top": 5, "$filter": "ListingKey eq '12345'"},
    )
```

## Key and property lookup behavior

`get_green_verification(verification_key: str)` requests `PropertyGreenVerification('<key>')`. It returns handled provider JSON without unwrapping a `value` array or applying the property client's single-record normalization.

`get_verifications_for_property(listing_key: str, **kwargs)` adds `ListingKey eq '<key>'`. An existing `filter_query` is joined using `and`, without extra parentheses. Other keyword arguments must match `get_green_verifications()`; arbitrary OData keywords are not accepted.

Keys and filter strings are inserted without escaping. Escape apostrophes in OData literals yourself and verify actual fields through your account's metadata.

## Verification-type constants

`GreenVerificationType` contains `ENERGY_STAR` (`Energy Star`), `LEED`, `GREEN_BUILDING` (`Green Building`), `HERS`, and `OTHER` (`Other`). These are package constants, not a freshly verified provider enumeration. Use `.value` when constructing a text filter.

The client does not validate a certification, interpret a rating, or verify that a listing holds a current credential. It only constructs the requests above and handles the response.

See [compatibility clients](unavailable-clients.md), [provider verification](live-api-updates.md), and [response conventions](../reference/index.md).

## Generated signatures and constants

::: wfrmls.green_verification
    options:
      show_root_heading: false
      show_source: false
