---
title: "WFRMLS code style and documentation rules"
description: "Find the canonical WFRMLS Python style rules for type hints, docstrings, formatting, testing, and the separate documentation writing guide."
---

# WFRMLS code style and documentation rules

The repository root
[STYLE_GUIDE.md](https://github.com/theperrygroup/wfrmls/blob/master/STYLE_GUIDE.md)
is the canonical code-style document. This page points to it rather than
maintaining a second copy.

## Apply the code standards

Use typed public interfaces, Google-style docstrings, clear exception handling,
and focused tests. Check formatting with Black, import order with isort, and
typing with mypy using the commands in the [development guide](index.md).

Treat aspirational coverage goals as goals. The actual enforced coverage floor
and blocking lint categories are described in that guide and the CI workflow;
do not infer them from a broader style recommendation.

## Follow the writing standards

[docs/STYLE_GUIDE.md](../STYLE_GUIDE.md) owns the documentation writing and
formatting guidance. When an API changes, update its reference and task examples
together. Keep setup commands, supported methods, response shapes, and provider
claims verifiable against source, tests, or linked primary documentation.

For a coordinated repository audit, use the
[consistency runbooks](consistency/index.md).
