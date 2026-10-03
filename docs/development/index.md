---
title: "Develop and verify the WFRMLS client"
description: "Set up a WFRMLS contributor environment, run offline tests and CI quality checks, build strict documentation, and verify package artifacts."
---

# Develop and verify the WFRMLS client

Run contributor commands from the repository root. Use Python 3.11 for the
current development and documentation toolchain; the library's compatibility
matrix also tests Python 3.8–3.12.

## Set up a local checkout

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install -r docs/requirements.txt
python -m pip install build twine
```

On Windows, create the environment with `py -3.11 -m venv .venv` and activate
`.venv\Scripts\Activate.ps1`. The `dev` extra and docs dependency file have
different purposes. There is no `docs` extra, `Makefile`, or pre-commit
configuration in this repository.

## Run offline tests and quality checks

The normal CI test path excludes `tests/test_integration.py`. Follow the same
path locally; do not use live provider credentials for the ordinary unit suite.
The CI coverage floor is currently 15 percent. A broader coverage goal in
the style guide is a development target, not a claim about the enforced floor.

```bash
python -m pytest tests/ --ignore=tests/test_integration.py --cov=wfrmls --cov-report=term-missing --cov-fail-under=15
black --check --diff wfrmls/ tests/
isort --check-only --diff wfrmls/ tests/
flake8 wfrmls/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
mypy wfrmls/ --ignore-missing-imports --show-error-codes
```

The flake8 command checks the CI-blocking syntax/undefined-name categories.
CI also prints a broader lint report with `--exit-zero`; that report does not
enforce every style warning. The dedicated code-quality job enforces mypy,
even though the test-matrix copy currently permits it to continue after failure.
Consult the [workflow review runbook](consistency/phase-3-github-actions.md)
when changing those gates.

Tests that deliberately exercise the live API require separate, explicit
authorization, licensed access, and isolated credentials. Keep token values
and real MLS payloads out of test fixtures and published logs.

## Check for embedded credentials

Install the pinned [Gitleaks 8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1)
for your platform, then check staged changes before committing:

```bash
gitleaks version
python scripts/check_secret_rules.py
gitleaks git . --pre-commit --staged --config .gitleaks.toml --redact=100 --ignore-gitleaks-allow
```

The dedicated Secrets Check workflow verifies the downloaded executable's
checksum, tests detection with generated synthetic input, and scans all fetched
Git history, including root scripts such as `get_property.py`, the package,
tests, and documentation. It preserves Gitleaks' default rules and adds detection for
32-character hexadecimal WFRMLS bearer-token literals, including environment
assignments, constructor keywords, and authorization headers. It does not use
live credentials or contact the MLS API.

Use environment lookups or short mock sentinels such as `test_token` in examples
and tests. Never copy real credentials into fixtures. CI ignores inline
`gitleaks:allow` comments and repository fingerprint-ignore files. A confirmed
false positive needs a reviewed rule-specific exception constrained to its
exact harmless value and file path; never exempt entire test or docs directories.

If a credential is detected, remove it before publishing and arrange its
revocation or rotation with the credential owner. A clean scanner result does
not prove that an exposed credential is inactive.

## Build and preview documentation

```bash
mkdocs build --strict --clean
mkdocs serve
```

The first command is the validation gate. The second starts a local preview;
stop it when finished. Check examples against source signatures and verify
network examples with mocked responses before documenting them as runnable.

Keep [documentation style](../STYLE_GUIDE.md), [code style](style-guide.md),
and the [consistency runbooks](consistency/index.md) aligned with actual behavior.

## Verify package artifacts

```bash
python -m build
python -m twine check dist/*
```

These commands create and validate artifacts; they do not publish them.
Check that the wheel includes the typing marker and that package metadata
matches the intended release.

## Understand release and deployment boundaries

The [release workflow](https://github.com/theperrygroup/wfrmls/blob/master/.github/workflows/release.yml)
runs on `v*` tags. It checks tag/version parity against `pyproject.toml` and
`wfrmls/__init__.py`, runs tests, builds distributions, publishes through the
protected release environment, and creates a GitHub release. A successful local
build or a master commit alone does not prove a PyPI release.

The separate [documentation workflow](https://github.com/theperrygroup/wfrmls/blob/master/.github/workflows/docs.yml)
builds changed docs and deploys on qualifying master pushes. Verify its actual
deployment result before reporting the published site as updated.

Report defects through [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)
with a minimal synthetic reproduction, the installed version, and a sanitized
status or traceback.
