---
title: "WFRMLS implementation differences and review gaps"
description: "Compare WFRMLS implementation facts with consistency goals, including dependency files, CI gates, publishing, documentation, and API limitations."
---

# WFRMLS implementation differences and review gaps

This map separates implementation facts from review goals. Recheck the source
at the commit being reviewed before treating a historical observation as current.
Use [development commands](../index.md) for local validation.

## Inspect the relevant files

```bash
rg --files -g 'pyproject.toml' -g '*requirements*.txt' -g 'STYLE_GUIDE.md' -g 'mkdocs.yml'
rg 'cov-fail-under|exit-zero|Type checking failed|needs:|mkdocs build|PYPI_API_TOKEN' .github/workflows
rg --files wfrmls tests docs .github
```

## Review repository-specific differences

| Area | Implemented behavior to verify | Review question |
| --- | --- | --- |
| Versions | `pyproject.toml` and `wfrmls/__init__.py` carry the package version. | Do both match the intended `v*` release tag? |
| Dependencies | Root requirements files coexist with `pyproject.toml`; docs have a separate dependency file. | Are companion manifests synchronized and their roles explicit? |
| Python support | Library CI tests 3.8–3.12; docs tooling uses 3.11. | Are runtime and tooling requirements described separately? |
| Coverage | The CI floor is 15 percent, below the broader style-guide goal. | Is the enforced floor documented accurately, with useful tests for changed behavior? |
| Lint and typing | Critical flake8 categories and the dedicated mypy job block; broader lint and matrix mypy include nonblocking paths. | Do docs identify the blocking checks rather than promise all warnings are enforced? |
| Artifacts | The CI build job depends on security; the release build depends on tests. | Does each dependency graph meet the project's intended readiness policy? |
| Docs | Navigation includes these runbooks; strict local builds validate links and generated API docs. | Do deployment builds enforce the desired strict mode and install the package? |
| Publishing | Release configuration uses a PyPI API token and a protected environment. | Does the documented mechanism match the actual workflow? |
| Optional tools | Pylint is installed as a development tool but has no required invocation in CI. | Is it described as optional rather than a passing required gate? |

## Retain API-contract gaps explicitly

- Radius and polygon helpers reject calls locally. Do not advertise spatial
  search implementation based on the existence of a method name.
- The property pagination convenience method returns partial results after
  failures. A complete replication requires failure-preserving pagination.
- The copied deletion examples and `DeletedClient` helpers use different field
  names. Current provider schema and retention need independent verification.
- Provider access, numeric quotas, and image/display rights are separate from
  package installation and the MIT license.

The [task guides](../../guides/index.md) document these boundaries. If resolving
one requires source or provider changes, assign that concrete work separately
and preserve its acceptance evidence.

## Record a resolved or intentional gap

For each actual gap found, record the affected file, observed behavior,
desired result, owner, next action, and proof of closure. Do not retain obsolete
missing-navigation or tooling claims after the source has been corrected.
