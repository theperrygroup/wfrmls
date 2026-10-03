---
title: "Phase 1: Verify the package foundation"
description: "Audit WFRMLS package versions, metadata, dependency manifests, type-marker inclusion, and local wheel and source-distribution validation."
---

# Phase 1: Verify the package foundation

Use a contributor environment from the [development guide](../index.md), and
run these commands from the repository root. This phase checks packaging and
metadata before changing documentation or delivery workflows.

## Inspect versions and dependency ownership

```bash
rg '^version = ' pyproject.toml
rg '^__version__ = ' wfrmls/__init__.py
rg 'requires-python|license|authors|maintainers|Homepage|Documentation|Repository' pyproject.toml
rg --files -g '*requirements*.txt' -g 'pyproject.toml'
rg '\[tool\.|black|isort|flake8|mypy|pytest|coverage|pylint' pyproject.toml
```

Check that declared authors, ownership, project URLs, and supported versions
are factual. The existence of a metadata field alone does not establish its
accuracy or a provider affiliation.

Runtime dependencies and the development extra are declared in `pyproject.toml`.
Inspect the companion root requirements files for drift. Docs dependencies
are maintained in `docs/requirements.txt` and are not a package extra.

## Verify packaged files

```bash
python -m build
python -m twine check dist/*
python -m zipfile -l dist/wfrmls-1.3.10-py3-none-any.whl
```

Replace the wheel filename with the version just built. Confirm that the wheel
contains the runtime package and `wfrmls/py.typed`, and that the source
distribution contains the intended license and project documentation. A
successful `twine check` validates distribution metadata, not API behavior.

## Check the configured tools

Run the [development quality checks](../index.md#run-offline-tests-and-quality-checks).
Use their scoped `wfrmls/` and `tests/` arguments rather than recursively scanning
an entire checkout that may contain virtual environments or generated files.
Document optional or nonblocking tools honestly.

## Completion evidence

Record version parity, dependency-file responsibilities, artifact validation,
and the included typing marker. Report remaining metadata or packaging gaps
through the [gap map](repo-gap-map.md), then continue to
[documentation verification](phase-2-docs.md).
