# wfrmls Gap Map

Use this file with the phase docs. The commands below assume the variables
from `index.md` are already exported.

## Snapshot

| Area | Current state |
| --- | --- |
| Package target | `wfrmls` |
| Python floor | `>=3.8` in `pyproject.toml` |
| Release flow | `.github/workflows/release.yml` |
| Docs flow | `.github/workflows/docs.yml` |
| Security flow | Mostly inside `.github/workflows/ci.yml`, plus Dependabot |
| Dependency automation | Dependabot via `.github/dependabot.yml` |
| Style guides | Root `STYLE_GUIDE.md` and `docs/STYLE_GUIDE.md` both exist |

## Phase 1 Priorities

- `pyproject.toml` and `LICENSE`: verify the maintainer and legal story are
  consistent, because authorship and copyright wording point at different
  names.
- `pyproject.toml`: verify the built wheel includes `py.typed`, since package
  data is not declared as explicitly as it is in the other repos.
- `pyproject.toml`: `pylint` is part of the dev toolchain, but the workflows do
  not enforce it.
- `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, and
  `docs/requirements.txt`: document the dependency source of truth.

## Phase 1 Commands

```bash
rg 'authors|license|requires-python|Homepage|Documentation|Repository' pyproject.toml
rg --files -g 'LICENSE' .
rg --files -g 'requirements*.txt' -g 'docs/requirements.txt' .
rg 'pylint|py.typed|Typing :: Typed' pyproject.toml .github/workflows/ci.yml README.md
python -m build
python -m twine check dist/*
```

## Phase 2 Priorities

- `mkdocs.yml`: the nav references missing files under `docs/development/`,
  `docs/examples/`, `docs/reference/`, and `docs/legal/`.
- `docs/development/index.md`: contributor instructions mention
  `pre-commit install` and `make quality`, but neither a
  `.pre-commit-config.yaml` file nor a `Makefile` exists.
- `docs/api/openhouse.md` and `docs/api/openhouses.md`: decide which page name
  is canonical and remove the duplicate drift.
- `STYLE_GUIDE.md` and `docs/STYLE_GUIDE.md`: define which copy owns updates.
- `mkdocs.yml`: replace the analytics placeholder or remove it.

## Phase 2 Commands

```bash
rg --files docs
rg '^nav:' -A 220 mkdocs.yml
rg 'pre-commit|make quality|Style Guide|Contributing|Testing|Release Process' docs/development/index.md docs
python -m pip install -e .
python -m pip install -r docs/requirements.txt
mkdocs build --strict
```

## Phase 3 Priorities

- `.github/workflows/ci.yml`: raise the coverage gate so CI matches the 100
  percent standard advertised in docs.
- `.github/workflows/ci.yml`: remove the soft-fail `mypy` step from the test
  job or make it match the hard gate in the code-quality job.
- `.github/workflows/ci.yml`: stop letting the build job depend only on the
  security job if release artifacts are meant to imply a green test suite.
- `.github/workflows/ci.yml`: either run `pylint` or remove it from the
  documented toolchain.
- `.github/workflows/release.yml` and `.github/workflows/docs.yml`: keep the
  split flow only if it remains clearer than a unified deployment path.

## Phase 3 Commands

```bash
rg 'cov-fail-under|Type checking failed but continuing|needs: \[security\]|pylint|safety' .github/workflows/ci.yml .github/workflows/release.yml .github/workflows/docs.yml
rg --files .github | rg 'dependabot|renovate'
black --check .
isort --check-only .
flake8 .
mypy "$PACKAGE_TARGET"
pytest --cov="$PACKAGE_TARGET"
mkdocs build --strict
python -m build
python -m twine check dist/*
```

## Recommended Order

1. Clarify metadata ownership, package data, and dependency source of truth.
2. Fix the docs nav and contributor command drift so `mkdocs build --strict`
   becomes meaningful.
3. Tighten the CI coverage and typing gates to match the written standard.
4. Decide whether the current split docs and release workflows still earn their
   complexity.
