---
title: "Shared Python-client consistency standard"
description: "Review shared Python-client goals for WFRMLS packaging, types, documentation, validation, release parity, and explicit repository exceptions."
---

# Shared Python-client consistency standard

This standard defines review goals. It does not imply that every goal is
already enforced in WFRMLS or in the other Perry Group clients. Verify current
behavior using the [repository gap map](repo-gap-map.md) and source workflows.

## Keep packaging and dependencies explicit

Use `pyproject.toml` for package metadata and tool configuration. Keep its
version synchronized with `wfrmls/__init__.py` and the intended release tag.
Check the actual license, ownership, supported Python versions, project URLs,
and the built wheel's `py.typed` marker.

Document the purpose of every dependency manifest. WFRMLS defines runtime
dependencies and the `dev` extra in `pyproject.toml`, has companion root
requirements files, and maintains docs tooling in `docs/requirements.txt`.
Inspect all of them when changing a shared dependency; do not imply that a
docs extra or generated lockfile exists.

## Make validation claims match enforcement

The shared baseline includes Black, isort, flake8, mypy, pytest with coverage,
strict MkDocs builds, `build`, and `twine`. See the
[development commands](../index.md) for the current WFRMLS forms.

Verify which lint categories and coverage threshold fail CI. An installed tool
or a nonblocking report is different from an enforced gate. Tools such as
Pylint or pre-commit must not be advertised as required checks unless the
repository actually provides and runs them.

## Keep documentation useful and verifiable

Maintain real navigation entries, distinct task guides, and accurate response
and exception descriptions. Exercise examples with synthetic mocked responses.
Separate implemented library behavior from provider permissions and protocol
guidance. Keep the root code-style guide and docs writing guide authoritative
for their respective subjects.

## Review delivery and security boundaries

Require tag/version parity and successful artifact checks before publishing.
Review whether the release workflow depends on all checks the project intends
to require. Strict docs validation and a successful deployment are separate
evidence. Document the publishing mechanism actually configured; WFRMLS's
release workflow currently uses a PyPI API token.

Check static analysis, dependency audits, and dependency-update configuration
for root Python, docs, and GitHub Actions dependencies. Preserve protected
environments and permissions when changing delivery workflows.

## Record intentional differences

Keep service-specific modules, examples, and workflow names when they make the
client clearer. A shared goal does not require identical file trees. Record
the reason and verification for an exception rather than silently asserting
that all four repositories are equivalent.
