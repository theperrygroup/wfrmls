---
title: "Configure bearer-token authentication"
description: "Configure WFRMLS bearer-token authentication with environment variables or an explicit argument, and diagnose missing or rejected credentials."
---

# Configure bearer-token authentication

The client sends `Authorization: Bearer <token>` to the configured service.
It accepts an existing token; it does not implement an OAuth login flow,
discover scopes, or renew expired credentials.

## Obtain authorized access

Arrange access through the [UtahRealEstate vendor portal](https://vendor.utahrealestate.com)
and use credentials issued for your application and licensed use. Resource
availability depends on the provider's configuration and your agreement.
Confirm current token issuance and renewal instructions with the provider;
this guide does not assume a particular portal screen or token format.

## Use an environment variable

Set `WFRMLS_BEARER_TOKEN` through your process environment, deployment secret
store, or a local `.env` file. A local file has this form:

```dotenv
WFRMLS_BEARER_TOKEN=replace-with-your-issued-token
```

Exclude credential files from source control and restrict their local access.
`python-dotenv` is invoked when the base-client module is imported; by default,
an existing environment value takes precedence over a `.env` value.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(top=1, select=["ListingId"])
print("Records returned:", len(response["value"]))
```

This request tests the `Property` resource under your current access. An empty
collection can be a successful response. It does not prove access to every
resource or field.

## Pass a token explicitly

An explicit nonempty token takes precedence over `WFRMLS_BEARER_TOKEN`.
Use this option when your application's secret loader supplies the token:

```python
import os

from wfrmls import WFRMLSClient

token = os.environ["WFRMLS_BEARER_TOKEN"]
client = WFRMLSClient(bearer_token=token)
response = client.property.get_properties(top=1, select=["ListingId"])
print("Records returned:", len(response["value"]))
```

The constructor accepts only `bearer_token` and `base_url`. It has no `timeout`,
`max_retries`, or `retry_delay` arguments. Changing `base_url` sends your
credentials to that destination, so use an approved HTTPS service URL.

## Understand lazy initialization and credential changes

`WFRMLSClient()` stores its configuration and creates each service on first
access. A missing token normally raises `AuthenticationError` when you access
`client.property` or another service, rather than at construction.

Once a service has been created, its session retains the configured header.
After rotating a token, create a new client with the new value. Do not expect
existing services to reread a changed environment variable automatically.

## Diagnose authentication errors

| Result | Meaning and next action |
| --- | --- |
| `AuthenticationError` without an HTTP status | No explicit token or environment token was available when the service initialized. |
| `AuthenticationError` with status 401 | The service rejected the credential. Confirm the token and renewal requirements. |
| `WFRMLSError` with status 403 | The request was forbidden; the library does not map 403 to `AuthenticationError`. Check authorization and the requested resource. |

Do not print tokens, authorization headers, or entire error response bodies.
Use a status code and operation name when recording a diagnostic. See
[error handling](../guides/error-handling.md) for the exception mapping and
[data licensing](../legal/index.md) for permitted use.
