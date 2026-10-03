---
title: Documentation writing and verification standards
description: Write accurate WFRMLS documentation with tested examples, clear response shapes, descriptive metadata, useful links, and strict build verification.
---

# Documentation style guide

Documentation should help a developer make a correct request and understand the
result. Accuracy, useful examples, and clear limits take priority over page
length or decorative formatting.

## Establish the source of truth

- Read the current implementation and relevant tests before describing a method.
- Use exact import paths, method names, argument names, defaults, and return types.
- Distinguish Python-client behavior from the provider's protocol and service.
- Cite primary provider documentation for provider-specific requirements.
- Label historical observations and checked-in schema snapshots. Do not describe
  an old outage, record count, or scraped page as current service evidence.
- Explain unsupported features and helpers that return partial results.
- Keep the API reference and public docstrings consistent. Generated reference
  pages expose those docstrings directly.

The documentation site tracks `master`; released packages can differ. Link to
release-specific source when documenting behavior introduced in a release.

## Write for the task

Begin with one descriptive H1 and a short explanation of what the reader will
learn. State prerequisites, give a working example, explain the result, and link
to the next relevant task. Use sentence case and a logical heading hierarchy.

Prefer active voice and concrete statements. Avoid claims such as "complete
market data," "automatic rate limiting," or "100% coverage" unless the
implementation and current verification establish them. Explain which behavior
belongs to the library and which policy the application must implement.

Keep a page focused on one topic. Use tables for parameters or comparisons and
lists for steps. Remove repetition and unsupported application scenarios rather
than adding words to meet a length target.

## Make examples usable

Python examples should include their imports and setup, or state the setup they
continue from. Use placeholders for credentials and synthetic records. Never
include tokens, customer information, or private MLS payloads.

A collection request returns a dictionary. Iterate its `value` list:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient()  # WFRMLS_BEARER_TOKEN is configured in the environment.
response = client.property.get_properties(top=10)
for listing in response.get("value", []):
    print(listing.get("ListingId"))
```

A property detail lookup returns a single dictionary; it does not use the same
access pattern as a collection. Other detail methods may return an unmodified
provider payload. Document each method's actual behavior.

Test Python examples with fake credentials and mocked transport. Verify method
signatures, query parameters, representative response shapes, and expected
exceptions. Check failure paths for retries, pagination, and synchronization.
Do not use a live provider call as the default documentation test.

When showing partial code or an intentionally unsupported call, label it
explicitly. Do not put a failing helper in a normal quick-start example.

For shell commands, use `python -m pip` and quote extras such as `'.[dev]'`.
Show platform-specific environment or activation commands where they differ.
Keep live integration tests separate from the standard mocked test command.

## Describe errors and operational limits

State when authentication is checked, what exceptions are raised, and whether a
request has a timeout or retry policy. An exception mapping is not an automatic
retry mechanism.

For pagination and synchronization, explain completion criteria, checkpoint
persistence, error handling, and the consequences of partial responses. Never
advance a checkpoint based on a helper that silently returns a partial batch.

Treat page-size limits, request quotas, and polling recommendations as distinct
concepts. Cite current provider guidance when available and qualify snapshots.

## Keep navigation and links useful

Use relative links between site pages. Link to the section that answers the
reader's next question, with descriptive text rather than "click here."
Preserve existing page URLs where possible so external links keep working.

Add new pages to `mkdocs.yml`. When a method's heading changes, check incoming
fragment links. Avoid linking to disabled GitHub features or inventing pages that
do not exist. Keep raw provider notes in `api_docs/` separate from client guides.

Material cards, admonitions, and tabs are available. Use cards on section landing
pages and admonitions for a prerequisite or meaningful limitation. Do not repeat
navigation panels or emojis on every reference page.

## Provide accurate search metadata

Every published page needs a distinct, concise title and a description of its
actual content. Set these in YAML front matter:

```yaml
---
title: WFRMLS property query examples
description: Query listings by city, price, and status with the Python client, then read collection records from the OData value list.
---
```

Use relevant terms naturally in the opening paragraph and headings. Do not add
keyword lists, fake certifications, unsupported ratings, or ranking promises.
Descriptions can influence snippets, but search engines choose what to display.
See [Google's title guidance](https://developers.google.com/search/docs/appearance/title-link)
and [description guidance](https://developers.google.com/search/docs/appearance/snippet).

The theme supplies canonical URLs from `site_url`. The local template adds
Open Graph, Twitter, and JSON-LD metadata using page front matter. Keep metadata
consistent with visible content. MkDocs generates `sitemap.xml`; its URLs must
match the deployed project path.

## Verify before publication

Use Python 3.11 for the documentation environment, matching CI:

```bash
python -m pip install -e .
python -m pip install -r docs/requirements.txt
python -m mkdocs build --clean --strict
python scripts/check_docs.py site
```

The HTML check verifies metadata, canonical URLs, sitemap coverage, internal
links, and link fragments. Run the mocked example checks appropriate to your
change, plus the code checks when editing public docstrings.

For docstring-only Python changes, compare parsed source with docstrings removed
to establish that imports, signatures, and runtime statements did not change.
Keep package and runtime versions unchanged for documentation-only work.

Check the final deployment, not only the local build. A page can build correctly
while deployment or its public links still fail.
