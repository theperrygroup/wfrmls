---
title: "Handle WFRMLS request failures"
description: "Match WFRMLS HTTP and network exceptions accurately, add bounded retries for transient GET failures, and avoid logging credentials or records."
---

# Handle WFRMLS request failures

Most service helpers use `BaseClient`, which translates HTTP status codes and
Requests transport errors into the exceptions below. All inherit from
`WFRMLSError` and expose `status_code` and `response_data`. A local validation
or network failure can have no HTTP status.

## Match the actual exception mapping

| Exception | Trigger in the base client | Suggested action |
| --- | --- | --- |
| `AuthenticationError` | Missing token or HTTP 401 | Check configuration or obtain a valid token. |
| `ValidationError` | HTTP 400, or validation in a helper | Correct the query or argument before retrying. |
| `NotFoundError` | HTTP 404, or an empty single-property wrapper | Handle absence according to your application. |
| `RateLimitError` | HTTP 429 | Reduce traffic and apply a bounded retry policy. |
| `ServerError` | HTTP 500–599 | Consider retrying a read after a delay. |
| `NetworkError` | A Requests exception during a base-client request | Consider retrying a read; inspect connectivity. |
| `WFRMLSError` | Other unsuccessful statuses, including 403 | Inspect the status and the permitted operation. |

There is no package-defined `TimeoutError`, and 403 is not mapped to
`AuthenticationError`. The base client does not retain response headers in its
exceptions, so `error.retry_after` and `error.response.headers` are unavailable.

## Handle a specific failure

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import NotFoundError, WFRMLSError

client = WFRMLSClient()
try:
    record = client.property.get_property("1234567")
except NotFoundError:
    print("The requested property was not returned.")
except WFRMLSError as error:
    print("Property lookup failed; HTTP status:", error.status_code)
    raise
else:
    print(record.get("ListingId"))
```

Error response bodies and exception messages can include provider data. Log
operation names, exception classes, attempt counts, and status codes rather
than tokens, headers, URLs containing query details, or entire response bodies.

## Add bounded retries for reads

This helper is application code, not a library feature. It retries only the
library's transient error classes, with a capped exponential delay and jitter.
Authentication, query validation, and not-found failures propagate immediately.

```python
import random
import time

from wfrmls import WFRMLSClient
from wfrmls.exceptions import NetworkError, RateLimitError, ServerError


def read_with_retry(operation, attempts=4, base_delay=1.0, max_delay=30.0):
    if attempts < 1 or base_delay < 0 or max_delay < 0:
        raise ValueError("Use positive attempts and nonnegative delays.")
    for attempt in range(attempts):
        try:
            return operation()
        except (NetworkError, RateLimitError, ServerError):
            if attempt == attempts - 1:
                raise
            ceiling = min(max_delay, base_delay * (2**attempt))
            time.sleep(random.uniform(ceiling / 2, ceiling))


client = WFRMLSClient()
response = read_with_retry(
    lambda: client.property.get_properties(top=5, select=["ListingId"])
)
print("Records returned:", len(response["value"]))
```

Choose attempts and delays for your provider contract and workload. This policy
has an attempt limit, but cannot impose a total deadline on the library's
base requests because they have no explicit timeout. HTTP `Retry-After` is
optional and has defined seconds/date forms; this helper cannot honor it because
the library exceptions do not expose headers. See
[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3) and
[rate limits](rate-limits.md).

## Distinguish the metadata and paging paths

`WFRMLSClient.get_metadata()` uses a separate Requests call with a 30-second
timeout. Transport failures can escape as `requests.exceptions.RequestException`,
and a non-200 response raises a plain `WFRMLSError` without the base client's
status mapping.

The [next-link example](odata-queries.md#follow-collection-next-links) also
uses Requests directly, sets timeouts, and raises `HTTPError` on bad statuses.
Handle those exceptions explicitly if you adopt that application helper; the
retry example above is for normal library service calls.

## Preserve synchronization failures

Do not convert a failed page into an empty collection or advance a checkpoint
after a partial run. The library's `get_all_properties_paginated()` catches page
failures and returns partial records, so a successful return from it is
insufficient evidence of a complete sync. Follow the
[synchronization guide](data-sync.md) for a failure-preserving pattern.
