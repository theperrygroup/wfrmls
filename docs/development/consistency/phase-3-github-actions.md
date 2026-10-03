---
title: "Phase 3: Verify GitHub Actions behavior"
description: "Review actual WFRMLS CI gates, coverage behavior, docs deployment, version-tagged releases, security audits, and dependency automation."
---

# Phase 3: Verify GitHub Actions behavior

Workflow files determine what CI enforces and what can publish. Start with the
[local development checks](../index.md), then compare the workflow behavior
with the claims in README and contributor docs.

## Inventory responsibilities and failure handling

```bash
rg --files .github/workflows
rg 'black|isort|flake8|mypy|pytest|mkdocs|build|twine|bandit|pip.audit|codecov' .github/workflows
rg 'exit-zero|continue-on-error|\|\| true|Type checking failed|needs:|permissions:|environment:' .github/workflows
rg --files .github -g '*dependabot*' -g '*renovate*'
```

Identify each blocking check, informational report, prerequisite, and publishing
permission. A green artifact build does not imply that all independent jobs
passed. Preserve environment protections and review any proposed gate change.

## Review coverage across Python versions

The test matrix excludes the live integration module and enforces a 15-percent
coverage floor. `pyproject.toml` adds a narrowly anchored `if TYPE_CHECKING:`
exclusion so coverage.py versions available across Python 3.8–3.12 count the
type-only branches consistently. The additive rule preserves other defaults;
see [coverage.py exclusions](https://coverage.readthedocs.io/en/latest/excluding.html).

Confirm a proposed upgrade's exact-head test and upload results. Do not confuse
the enforced floor with a style-guide target or an upload success with a test pass.

## Review docs and release delivery

Build docs with `mkdocs build --strict --clean` before deployment. Check whether
the workflow uses that validation mode, installs the package for generated API
docs, and deploys only from its intended event and branch. A local build cannot
prove the published Pages site changed.

The release workflow runs on `v*` tags, tests before building, and checks the
tag against both version declarations. It publishes with `PYPI_API_TOKEN`
through the release environment. Review the configured mechanism rather than
calling it trusted publishing merely because `id-token: write` is present.
Do not create a release tag or activate publishing as part of a documentation audit.

## Review security and updates

The CI workflow includes CodeQL, Bandit, and pip-audit. Inspect which invocations
fail the job, what environment is audited, and how reports are retained.
Dependency automation must cover the actual manifests and Actions dependencies;
the presence of a configuration file does not prove an update was merged.

## Completion evidence

Record the inspected workflow commit, blocking/nonblocking gates, relevant
check results, and verified deployment or release outputs when those are in
scope. Use the [gap map](repo-gap-map.md) to retain intentional differences and
concrete follow-up actions.
