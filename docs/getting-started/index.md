---
title: "Getting started with the WFRMLS Python client"
description: "Start using the WFRMLS Python client: install the package, configure a bearer token, and query UtahRealEstate property data."
---

# Getting started with the WFRMLS Python client

`wfrmls` is a Python client for the UtahRealEstate RESO Web API. It sends
authenticated requests and exposes service helpers for properties, members,
offices, open houses, and other resources. Access to MLS data requires a
separate provider agreement and an authorized bearer token.

## Before you start

- Use Python 3.8 or later; the repository tests Python 3.8–3.12.
- Obtain API access and credentials from UtahRealEstate for your intended use.
- Know which resources and fields your account is permitted to read.

An installed package does not grant data access. See [data licensing](../legal/index.md)
before displaying or redistributing records or photos.

## Set up and make a request

<div class="grid cards" markdown>

-   :material-download: **Install the package**

    ---

    Create a virtual environment and install the runtime dependencies.

    [Installation instructions](installation.md)

-   :material-key: **Configure authentication**

    ---

    Supply a bearer token without embedding it in application source.

    [Authentication options](authentication.md)

-   :material-play: **Query a property collection**

    ---

    Read the `value` list and distinguish collection and single-property responses.

    [First request](quickstart.md)

-   :material-test-tube: **Try an offline example**

    ---

    Exercise a real client helper with a mocked response and no provider access.

    [Runnable examples](../examples/index.md)

</div>

## What to expect from the client

`WFRMLSClient()` creates service clients lazily. Constructing it alone does not
check a token or contact the API. Most service queries return the provider's
JSON dictionary; collections store their records under `value`.

The client does not automatically refresh credentials, retry failed requests,
throttle traffic, or follow collection next links. The guides explain how to
handle these concerns in your application.

## Continue with a task

Use [property search](../guides/property-search.md) for filters and media,
[OData queries](../guides/odata-queries.md) for paging, and
[data synchronization](../guides/data-sync.md) for checkpoints and deletion checks.
