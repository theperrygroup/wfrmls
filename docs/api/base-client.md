---
description: Understand BaseClient authentication, independent Requests sessions, raw GET queries, JSON response handling, and timeout or retry limitations.
---

# BaseClient HTTP behavior

Every resource client inherits from `wfrmls.base_client.BaseClient`. This shared class configures authentication, issues HTTP requests, and converts JSON-response failures into custom exceptions.

## Authentication and sessions

`BaseClient(bearer_token=None, base_url=None)` requires an explicit token or `WFRMLS_BEARER_TOKEN` immediately. Importing the base-client module calls `load_dotenv()`; production applications should configure their environment deliberately.

The default root is `https://resoapi.utahrealestate.com/reso/odata`. A new `requests.Session` sets Bearer authorization, `Accept: application/json`, and `Content-Type: application/json`. Different resource clients create separate sessions. Credentials do not refresh automatically after construction.

## Raw GET requests

`get(endpoint, params=None)` appends the relative endpoint to the configured root and returns the handled response. Unlike resource methods, its `params` dictionary uses raw OData keys with `$` prefixes.

| Parameter | Type | Required | Description | Default |
| --- | --- | --- | --- | --- |
| **`endpoint`** | `str` | Yes | Relative path; leading slashes are stripped | — |
| `params` | `dict \| None` | No | Query parameters passed to Requests | `None` |

With `WFRMLS_BEARER_TOKEN` configured:

```python
from wfrmls.base_client import BaseClient

client = BaseClient()
response = client.get("Property", params={"$top": 5, "$count": "true"})
print(len(response.get("value", [])))
```

Raw `get()` does not clamp pagination values, escape filters, or validate endpoint names. Prefer a resource method when its supported parameters cover your request.

## Response and timeout limits

200/201 responses are parsed as JSON, 204 returns `{}`, and error statuses use the [exception mapping](exceptions.md). Invalid JSON is represented as `{"message": response.text}`. Parsed JSON is not checked against a response schema.

Shared resource requests do **not** pass a timeout to Requests. The facade's separate metadata request has a 30-second timeout. The wrapper provides no automatic retries, backoff, rate-limit scheduling, context-manager interface, or facade-wide session-close method. A resource's `session` is accessible when application-specific configuration or cleanup is needed.

See [WFRMLSClient](client.md) for lazy service construction and [response conventions](../reference/index.md) for result shapes.
