# WFRMLS Python Client Code Style Guide

Use this guide when changing the Python client and its tests. For Markdown and
MkDocs content, use the [documentation style guide](docs/STYLE_GUIDE.md). The
configuration in [pyproject.toml](pyproject.toml), [setup.cfg](setup.cfg), and
[the workflows](.github/workflows/) defines the commands and enforced checks.

## Supported Python and tools

The package declares Python 3.8 or newer. The checked-in CI and release workflows
test Python 3.8 through 3.12. Keep library syntax compatible with Python 3.8 until
the declared minimum and the workflows change together.

| Tool | Repository configuration | Contributor guidance |
| --- | --- | --- |
| Black | Line length 88; target `py38` | Format Python code with Black. |
| isort | Black profile; line length 88; multiline mode 3 | Sort imports with isort. |
| flake8 | Settings in `setup.cfg` | Preserve the configured ignores; avoid new lint findings. |
| mypy | Typed definitions, return warnings, strict equality | Add precise annotations; this is a selected set of checks, not `strict = true`. |
| pytest | Test discovery under `tests/`; coverage enabled | Use mocked tests for normal development. |

Install development and documentation dependencies in an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pip install -r docs/requirements.txt
```

On Windows, activate the environment using the appropriate `.venv\Scripts`
activation command. CI uses Python 3.11 for its code quality and documentation
jobs; the library still needs to support its declared minimum.

## Formatting and imports

Use four spaces for indentation, parentheses for multiline expressions, and
Black's formatting. Keep prose and signatures readable even where a tool permits
a longer line. Group imports as standard library, third party, then package
imports, with a blank line between groups:

```python
from typing import Any, Dict, Optional

import requests

from .base_client import BaseClient
from .exceptions import WFRMLSError
```

Prefer relative imports within `wfrmls`. Use `TYPE_CHECKING` for imports needed
only by annotations when that avoids a circular dependency. In `WFRMLSClient`,
`property_decorator` aliases `builtins.property` so the service named `property`
does not shadow the decorator.

## Names and types

Use `snake_case` for modules, functions, methods, parameters, and local variables;
`PascalCase` for classes and enums; and `UPPER_SNAKE_CASE` for constants and enum
members. Name resource clients after their actual resource, such as
`PropertyClient`, `MemberClient`, and `OpenHouseClient`.

Annotate public parameters and return values. Follow the existing Python 3.8
compatible `typing` forms such as `Dict[str, Any]`, `List[str]`, `Optional[int]`,
and `Union[List[str], str]`. Use `Any` for genuinely unstructured provider data,
rather than discarding types for the whole interface.

Python arguments use names such as `filter_query`, `select`, and `orderby`.
Translate them to the provider's exact wire names (`$filter`, `$select`,
`$orderby`) when building a request. Preserve the case of resource names, fields,
and provider enum values. Do not invent camelCase query parameters or new enum
values from another API's conventions.

## Client structure and authentication

Resource clients inherit `BaseClient`; `WFRMLSClient` exposes them lazily. Keep
shared HTTP behavior in `BaseClient` and resource-specific filters and response
handling in the appropriate resource module. Follow an existing resource's
pattern before introducing a new abstraction.

The constructor parameter is `bearer_token`. `BaseClient` uses an explicit,
nonempty token first, then `WFRMLS_BEARER_TOKEN` from the environment, and raises
`AuthenticationError` if neither provides a token. Its request header is
`Authorization: Bearer <token>`.

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(bearer_token="example-token")
```

The default base URL is `https://resoapi.utahrealestate.com/reso/odata`.
`WFRMLSClient` stores the constructor values and initializes a `BaseClient` or
resource client on first access, so missing-token validation happens at that
access. Document this timing accurately. The package calls `load_dotenv()` on
import; tests and examples must not depend on a contributor's real credentials.

Use placeholder tokens in documentation and fake tokens in mocked tests. Do not
commit credentials or log bearer tokens, authorization headers, or private
provider payloads.

## Query and response handling

Include optional parameters only when supplied. Check `is not None` rather than
truthiness when `0` or `False` is a meaningful value. Join field lists with commas,
serialize booleans according to the endpoint's OData handling, and preserve the
public method's documented input types.

Do not assume every response is a collection. Collection methods generally
return an OData envelope with `value`; `get_property()` returns one normalized
entity dictionary; `get_metadata()` returns XML text; analytics helpers have
their own derived result shapes. Document and test the actual shape.

The property collection method caps a supplied `top` at 200. That is a client
behavior, separate from the provider's current per-vendor page size or rate
limits. The current property pagination helper uses `$top`/`$skip`, accumulates
records in memory, and can return partial results after an exception. Do not
describe it as automatic `@odata.nextLink` handling or a complete replication
engine.

Use ISO 8601 strings with an explicit timezone for timestamp examples. Preserve
the distinction between date-only fields and timestamp fields. Avoid documenting
a fixed UTC offset for local times that observe daylight saving time.

## Public API documentation

Write Google-style docstrings for public classes and methods. Include a concise
summary, parameter names and defaults, the return shape, and exceptions that the
implementation can actually raise. Explain limitations that affect use. Examples
must use existing methods and arguments and handle empty collection results.

```python
from typing import Any, Dict

from wfrmls import WFRMLSClient


def property_page(client: WFRMLSClient) -> Dict[str, Any]:
    """Request a small page of property identifiers.

    Args:
        client: Configured WFRMLS client.

    Returns:
        OData envelope containing a `value` list of property records.

    Raises:
        WFRMLSError: If the underlying property request fails.
    """
    return client.property.get_properties(top=10, select=["ListingKey", "ListPrice"])
```

Use parameter tables in Markdown when they help explain a public signature:

| Parameter | Type | Required | Description | Default |
| --- | --- | --- | --- | --- |
| `top` | `int` | No | Requested number of records; the client caps it at 200. | `None` |
| `select` | `List[str]` \| `str` | No | Fields to include in the provider response. | `None` |
| `filter_query` | `str` | No | OData filter expression passed to the provider. | `None` |

Escape literal pipes in Markdown tables. Document `**kwargs` only for methods
that accept it, and list the supported forwarded arguments. Keep provider
protocol descriptions in [the provider reference](api_docs/index.md) distinct
from the Python API reference. A historical schema or resource listing does not
prove that a resource is currently available or exposed by `WFRMLSClient`.

## Exceptions

Use the existing hierarchy in [wfrmls/exceptions.py](wfrmls/exceptions.py):
`AuthenticationError`, `ValidationError`, `NotFoundError`, `RateLimitError`,
`ServerError`, and `NetworkError` all inherit `WFRMLSError`. `WFRMLSError` supports
`status_code` and `response_data` when those are available.

The shared JSON response handler maps HTTP 400, 401, 404, 429, and 5xx to the
corresponding exceptions. Other HTTP errors use `WFRMLSError`, and request
failures use `NetworkError`. `get_metadata()` has separate error handling; avoid
claiming that every method uses the same mapping. Do not promise retries,
backoff, token refresh, or automatic recovery unless the relevant code implements
them.

## Tests and validation

Name tests `tests/test_<module>.py` and describe the observed behavior in each
test name. Use `responses` or mocks for HTTP calls, with a fake bearer token.
Cover request serialization, successful response shapes, empty results, and the
error behavior affected by a change. Add regression tests for meaningful fixes.

Normal test runs must exclude the live integration file:

```bash
python -m pytest tests/ --ignore=tests/test_integration.py
black --check --diff wfrmls/ tests/
isort --check-only --diff wfrmls/ tests/
flake8 wfrmls/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
mypy wfrmls/ --ignore-missing-imports --show-error-codes
```

Do not rely only on `-m "not integration"`: the integration file contains live
tests without consistent markers. Running it requires separate authorization
for live provider calls and the correct account permissions.

Coverage is enabled by `pyproject.toml`. The checked-in CI test command enforces a
15% floor; it does not enforce 100% coverage. Aim for strong coverage of changed
behavior, and do not weaken a configured gate to make a change pass. Report the
measured result rather than claiming a project-wide coverage target was met.

For documentation, install `docs/requirements.txt` and build from the repository
root:

```bash
mkdocs build --clean
```

Use `mkdocs build --strict --clean` to surface warnings when appropriate, while
distinguishing a stricter local check from the checked-in workflow command. The
documentation workflow installs the package for its main build so mkdocstrings
can inspect source. Changes to provider snapshots are reviewed as documentation;
they must not trigger live API calls merely to validate examples.

## Repository layout

| Location | Purpose |
| --- | --- |
| `wfrmls/base_client.py` | Shared bearer authentication, GET requests, and JSON error handling. |
| `wfrmls/client.py` | Lazy resource access, service discovery, and XML metadata retrieval. |
| `wfrmls/properties.py`, `member.py`, `office.py`, `openhouse.py` | Main resource clients. |
| `wfrmls/adu.py`, `lookup.py`, `deleted.py` | Additional resource clients. |
| `wfrmls/data_system.py`, `resource.py`, `property_unit_types.py` | Supporting resource clients. |
| `wfrmls/media.py`, `history.py`, `green_verification.py` | Standalone resource modules; do not imply matching main-client accessors exist. |
| `wfrmls/analytics.py` | Derived analytics helpers. |
| `wfrmls/exceptions.py`, `__init__.py`, `py.typed` | Errors, package exports/version, and typing marker. |
| `tests/` | Mocked unit tests and a separate live integration file. |
| `docs/`, `mkdocs.yml` | Published client documentation and its site configuration. |
| `api_docs/` | Historical provider reference and schema snapshot. |
| `.github/workflows/` | CI, documentation, and release automation. |

Keep resource-related enums with their client module. Export intended public
types through `wfrmls/__init__.py` and `__all__`. Add a main-client accessor only
when that interface is intentional and supported; an exported standalone class
does not imply a main-client property.

## Versions and delivery

Keep `pyproject.toml`'s version and `wfrmls/__init__.py`'s `__version__` consistent.
The release workflow is triggered by a `v*` tag and verifies that both match the
tag's version before packaging. It runs its test matrix, builds with
`python -m build`, checks distributions with `twine check`, publishes to PyPI,
and creates a GitHub release. Do not describe tag creation as a harmless local
version update: pushing a matching tag can initiate publication.

Record relevant behavior changes in the authorized issue, release notes, or
review record. The repository has no `tasks/` directory to update. Follow the
current task's delivery authorization and branch policy; documentation or code
review alone does not authorize a commit, push, release, or live provider call.

When adding or changing a resource, update its source, public docstrings, tests,
API page, and guide examples together. Validate the changed behavior and the
documentation build, and report authored, tested, and published results
separately.
