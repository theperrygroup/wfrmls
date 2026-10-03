---
title: "Manage WFRMLS request traffic"
description: "Handle WFRMLS 429 responses, distinguish provider quotas from the client page-size cap, and control request volume in application code."
---

# Manage WFRMLS request traffic

The client maps HTTP 429 to `RateLimitError`. It does not throttle requests,
track quota usage, read rate-limit headers, or automatically wait and retry.
Configure traffic controls in your application using your provider's current
agreement and service instructions.

## Confirm your limits with the provider

This documentation has no verified universal requests-per-minute, hourly,
daily, or concurrency quota for UtahRealEstate. Do not assume a published
number applies to every token, IP address, or feed. Ask the provider which
limits apply to your account and how it communicates them.

HTTP 429 indicates rate limiting and **may** include `Retry-After`; it does not
require a particular `X-RateLimit-*` header family. See
[RFC 6585 section 4](https://www.rfc-editor.org/rfc/rfc6585.html#section-4).
When present, `Retry-After` can be a delay in seconds or an HTTP date, as
defined by [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3).
Library exceptions do not expose those headers.

## Recognize a rate-limit failure

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import RateLimitError

client = WFRMLSClient()
try:
    response = client.property.get_properties(top=5, select=["ListingId"])
except RateLimitError as error:
    print("Property request was rate limited; HTTP status:", error.status_code)
    raise
else:
    print("Records returned:", len(response["value"]))
```

Use [bounded GET retries](error-handling.md#add-bounded-retries-for-reads) to
recover transient failures. Retrying immediately, or allowing many workers
to retry together, can increase the load that caused the 429 response.

## Reduce unnecessary requests

- Request only the required fields with `select` and apply filters on the server.
- Follow server continuation links instead of repeatedly fetching the first page.
- Persist a checkpoint after a complete synchronization run so later runs can
  query a bounded modification window.
- Share pacing across workers that use the same account or token. A separate
  limiter in each process does not enforce an aggregate limit.
- Reuse a service client for a workload so its Requests session can reuse
  connections. Separate services have separate sessions.

The library's `top` cap of 200 is a page-size implementation limit. It is
different from a traffic quota and does not guarantee that a server returns
200 records or that a requested result set is complete.

## Choose application controls explicitly

Start with serial requests while establishing your permitted operating rate.
Use a configurable minimum interval or a shared queue if the workload needs
pacing; select the interval from the provider contract, rather than a guessed
safe value. Add jitter to retry delays and put a finite limit on attempts.

Track request counts, durations, HTTP status, and retry counts without recording
credentials or full MLS payloads. Stop and diagnose repeated 401/403/400 failures
rather than treating them as ordinary rate limiting.

## Cache only within your licensed use

The library does not provide caching. Any cache needs an application-defined
scope, expiry, invalidation policy, and data-access controls. Follow the feed's
refresh and retention requirements; a cache hit is not evidence that a listing
is still available for display. See [data licensing](../legal/index.md) and
[synchronization](data-sync.md).
