# WFRMLS Python client for Utah real estate data

[![CI](https://github.com/theperrygroup/wfrmls/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/theperrygroup/wfrmls/actions/workflows/ci.yml)
[![Documentation](https://github.com/theperrygroup/wfrmls/actions/workflows/docs.yml/badge.svg?branch=master)](https://theperrygroup.github.io/wfrmls/)
[![PyPI](https://img.shields.io/pypi/v/wfrmls)](https://pypi.org/project/wfrmls/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/theperrygroup/wfrmls/blob/master/LICENSE)

`wfrmls` is a Python client for the **Wasatch Front Regional MLS (WFRMLS)**
RESO Web API from **UtahRealEstate.com**. Query property listings, agents,
brokerages, and open houses with OData filters, field selection, and sorting.
Use the resource clients to build listing search and data synchronization tools.

**[Documentation](https://theperrygroup.github.io/wfrmls/) ·
[Quick start](https://theperrygroup.github.io/wfrmls/getting-started/quickstart/) ·
[API reference](https://theperrygroup.github.io/wfrmls/api/) ·
[PyPI package](https://pypi.org/project/wfrmls/)**

This repository contains the Python library, not the MLS service. Access to
listing data requires a valid provider-issued bearer token and permission to
use the requested resources. See the
[UtahRealEstate.com vendor dashboard](https://vendor.utahrealestate.com/) for
API access. The software's MIT license does not grant rights to MLS data.

## Installation

The library supports Python 3.8 and later. Building the documentation uses
Python 3.11, as configured in the documentation workflow.

```bash
python -m pip install wfrmls
```

Set `WFRMLS_BEARER_TOKEN` in your application's environment, or pass
`bearer_token` when constructing the client. Keep credentials out of source
control, logs, and public examples. The client also loads a local `.env` file
through `python-dotenv`; exclude that file from Git.

## Query active property listings

After configuring your token, run:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()
response = client.property.get_properties(
    top=10,
    filter_query="StandardStatus eq 'Active'",
    select=["ListingId", "ListPrice", "City"],
    orderby="ListPrice desc",
)

for listing in response.get("value", []):
    print(listing.get("ListingId"), listing.get("ListPrice"), listing.get("City"))
```

Collection methods return a dictionary containing a `value` list, plus any
OData metadata returned by the server. Count records with
`len(response.get("value", []))`, rather than `len(response)`.

`client.property.get_property(listing_id)` returns one property dictionary.
An empty wrapped result raises `NotFoundError`. Other resources' detail methods
return the server's response; check their reference pages before assuming the
same normalization.

## Resource clients

| Client attribute | Use |
| --- | --- |
| `property` | Property listings, city and price filters, and paginated retrieval. |
| `member` | Real estate agents and office affiliations. |
| `office` | Brokerages and office information. |
| `openhouse` / `open_house` | Open house schedules and listing associations. |
| `lookup` | Enumeration names and values. |
| `adu` | Accessory dwelling unit records. |
| `property_unit_types` | Property unit type records. |
| `deleted` | Deletion records for data synchronization. |
| `resource` | Resource metadata. |
| `data_system` | Data system information. |

`WFRMLSClient.get_service_document()` lists the resources available to your
token. `get_metadata()` returns the provider's XML schema. Resource and field
availability depend on your access and the provider's current service.

`WFRMLSAnalytics` is a separate utility initialized with a client:
`WFRMLSAnalytics(client)`. Its reports operate on retrieved samples, so they
should not be treated as complete market statistics.

## Behavior to account for

- **Geolocation:** radius and polygon helpers raise `ValidationError`.
  The near-address helper falls back to a city query or returns an empty error
  payload; it does not geocode or apply the requested radius. Use
  [city and address filters](https://theperrygroup.github.io/wfrmls/guides/geolocation/).
- **Media and history:** `MediaClient`, `HistoryTransactionalClient`, and
  `GreenVerificationClient` are exported standalone classes. There are no
  `client.media`, `client.history`, or `client.green_verification` attributes.
  Confirm provider access before using those classes; historical outage notes
  do not establish current availability.
- **Pagination:** `get_all_properties_paginated()` combines pages using
  `$top` and `$skip`. It does not follow `@odata.nextLink` and silently returns
  collected records if a request fails. `pagination_info` has no completeness
  flag. Use explicit request/error handling for a reliable synchronization.
- **Retries and timeouts:** ordinary resource requests have no automatic
  retry, rate limiter, or request timeout. Configure the underlying service
  session or application policy as described in the
  [error handling](https://theperrygroup.github.io/wfrmls/guides/error-handling/)
  and [rate limits](https://theperrygroup.github.io/wfrmls/guides/rate-limits/)
  guides. HTTP 429 responses raise `RateLimitError`.

## Learn more

- [OData queries](https://theperrygroup.github.io/wfrmls/guides/odata-queries/):
  filters, sorting, selected fields, and response metadata.
- [Property search](https://theperrygroup.github.io/wfrmls/guides/property-search/):
  supported listing search patterns.
- [Data synchronization](https://theperrygroup.github.io/wfrmls/guides/data-sync/):
  pagination, update checkpoints, and deletion handling.
- [Examples](https://theperrygroup.github.io/wfrmls/examples/):
  complete application patterns using the public client.

The documentation site tracks `master`. For release-specific behavior, inspect
the matching [release](https://github.com/theperrygroup/wfrmls/releases) and
installed package version.

## Development and contributions

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

# Mocked tests; no provider credentials or live API calls are needed.
PYTHON_DOTENV_DISABLED=1 WFRMLS_BEARER_TOKEN='' \
    python -m pytest tests/ --ignore=tests/test_integration.py
```

See the [development guide](https://theperrygroup.github.io/wfrmls/development/)
for Windows setup, documentation builds, and the quality checks used in CI.
Follow the [code style guide](https://github.com/theperrygroup/wfrmls/blob/master/STYLE_GUIDE.md) and
[documentation style guide](https://theperrygroup.github.io/wfrmls/STYLE_GUIDE/). Changes should include
appropriate tests and accurate examples; use the current CI results for
coverage evidence.

Report library bugs and documentation errors in
[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues). Include the
package version, a minimal reproduction, and redacted error details. Direct
token, data-access, and provider service questions to UtahRealEstate.com.

## License

The Python client is maintained in The Perry Group's repository and distributed
under the [MIT License](https://github.com/theperrygroup/wfrmls/blob/master/LICENSE).
