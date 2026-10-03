---
description: Handle WFRMLS HTTP exceptions, local validation failures, metadata request differences, and helpers that return error dictionaries or partial results.
---

# WFRMLS exceptions and failure behavior

All custom exceptions inherit from `WFRMLSError`. Their optional `status_code` and `response_data` attributes describe HTTP failures; local failures may leave both as `None`.

## HTTP response mapping

The shared `BaseClient` maps response codes as follows:

| Condition | Exception or return value |
| --- | --- |
| 200 or 201 | Parsed JSON; invalid JSON becomes `{"message": response.text}` |
| 204 | Empty dictionary |
| 400 | `ValidationError` |
| 401 | `AuthenticationError` |
| 404 | `NotFoundError` |
| 429 | `RateLimitError` |
| 500–599 | `ServerError` |
| Other statuses, including 403 | `WFRMLSError` |
| Requests transport exception in shared requests | `NetworkError` |

Missing credentials raise `AuthenticationError` when a `BaseClient` or service client is constructed. `WFRMLSClient()` defers that construction until service access. Nonnumeric property lookup strings and unsupported radius/polygon calls raise `ValidationError` locally. An empty wrapped single-property result raises `NotFoundError` locally.

## Catch expected failures

With `WFRMLS_BEARER_TOKEN` configured:

```python
from wfrmls import NotFoundError, WFRMLSClient, WFRMLSError

client = WFRMLSClient()
try:
    listing = client.property.get_property("12345")
    print(listing.get("ListingId"))
except NotFoundError:
    print("No property record was returned.")
except WFRMLSError as error:
    print(type(error).__name__, error.status_code)
```

Do not log tokens or complete response payloads containing personal data. The exception's message is inherited from `Exception`; there is no custom `message` attribute.

## Failure paths that need separate handling

- `get_metadata()` uses a direct Requests call. Non-200 responses raise generic `WFRMLSError` without shared HTTP attributes; transport exceptions propagate as Requests exceptions.
- Analytics helpers catch exceptions and return `{"error": ...}` instead of raising them.
- `get_all_properties_paginated()` catches request failures and returns partial data without an error marker.
- `DeletedClient.get_all_deleted_for_sync()` suppresses per-resource failures, retaining empty lists for those resources without an error marker.
- Incorrect or duplicate Python keyword arguments can raise `TypeError`; that is not a `WFRMLSError` subclass.

The client does not implement automatic retries, backoff, token refresh, or rate-limit scheduling. Design those policies around your application requirements.

## Generated exception definitions

::: wfrmls.exceptions
    options:
      show_root_heading: false
      show_source: false

See [HTTP client behavior](base-client.md) and [response conventions](../reference/index.md) for request and result details.
