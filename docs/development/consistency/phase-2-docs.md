---
title: "Phase 2: Verify documentation and examples"
description: "Audit WFRMLS documentation against source and primary provider guidance, verify mocked examples, and validate navigation with a strict MkDocs build."
---

# Phase 2: Verify documentation and examples

Start from an identified repository commit and use the
[Python 3.11 docs environment](../index.md). The objective is useful, accurate
documentation with verifiable examples and working navigation.

## Inventory pages and advertised behavior

```bash
rg --files docs
rg '^nav:' -A 100 mkdocs.yml
rg 'pre-commit|make |Python 3\.[0-9]|pytest|mypy|black|isort|flake8' README.md docs
```

Review every page in scope, including indexes and contributor runbooks. Verify
method names, parameters, imports, response shapes, exception mapping, paging,
timeouts, retries, and credential handling against source and tests.

Provider quotas, access, schema, deletion retention, and display rights require
current provider evidence. Link primary sources near supported claims and
identify unavailable evidence. Copied historical provider pages are not a
verified current contract.

## Improve navigation and page metadata

Keep each `mkdocs.yml` entry connected to a real file. Add unique, accurate
frontmatter descriptions and descriptive headings. Check relative links,
code examples, and rendered tables rather than adding text to meet a word count.

Use [docs/STYLE_GUIDE.md](../../STYLE_GUIDE.md) for writing guidance and the
[code style page](../style-guide.md) for the separate Python conventions.

## Verify examples and the rendered site

Compile Python snippets, then execute network examples with mocked responses.
Include empty collections, single-entity normalization, page failure, invalid
continuation URLs, and checkpoint preservation where those behaviors matter.
Never use real tokens or provider calls as a substitute for isolated example tests.

```bash
python -m pip install -e .
python -m pip install -r docs/requirements.txt
mkdocs build --strict --clean
```

Inspect representative rendered pages for readable code, headings, tables,
descriptions, and links. A clean build is necessary but does not prove that
an example performs the documented task.

## Completion evidence

Record pages reviewed, example checks, and the strict-build result. Verify any
deployed documentation separately through the
[workflow phase](phase-3-github-actions.md).
