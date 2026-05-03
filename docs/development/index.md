# Development

Resources for working on the WFRMLS Python client and keeping docs, tests, and packaging in sync with the repository's current state.

---

## Quick Navigation

<div class="grid cards" markdown>

-   :material-hammer-wrench:{ .lg .middle } **Local Setup**

    ---

    Create an environment and install development dependencies.

    [:octicons-arrow-right-24: Local Setup](#local-setup)

-   :material-check-decagram:{ .lg .middle } **Quality Checks**

    ---

    Run the same commands maintainers use for tests and docs.

    [:octicons-arrow-right-24: Quality Checks](#quality-checks)

-   :material-code-tags:{ .lg .middle } **Code Style Guide**

    ---

    Follow the canonical Python style guide for this repository.

    [:octicons-arrow-right-24: Code Style Guide](style-guide.md)

-   :material-book-edit:{ .lg .middle } **Documentation Style Guide**

    ---

    Use the docs-specific writing and formatting guidance.

    [:octicons-arrow-right-24: Documentation Style Guide](../STYLE_GUIDE.md)

-   :material-file-document-multiple:{ .lg .middle } **Consistency Runbooks**

    ---

    Review the documentation and repository consistency notes.

    [:octicons-arrow-right-24: Consistency Runbooks](consistency/index.md)

</div>

---

## Local Setup

Set up a local environment with the commands that are supported by the current repository:

```bash
# Clone the repository
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package and development tooling
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install -r docs/requirements.txt
```

!!! note "Current tooling"
    This repository does not currently provide a `Makefile` or a `.pre-commit-config.yaml` file. Run the individual commands below directly instead of relying on `make quality` or `pre-commit install`.

---

## Quality Checks

Use these commands before opening or updating a pull request:

```bash
# Run the test suite
pytest

# Run coverage locally
pytest --cov=wfrmls --cov-report=term-missing

# Format and static analysis
black wfrmls tests
flake8 wfrmls tests
mypy wfrmls

# Verify the documentation site
mkdocs build --strict
```

If you update library behavior, also update the relevant documentation pages and examples in `docs/`.

---

## Documentation Expectations

When you change the package, keep the surrounding docs truthful:

- Update examples and guides that mention the affected behavior.
- Keep navigation in `mkdocs.yml` aligned with files that actually exist.
- Prefer removing stale links over inventing placeholder pages.
- Keep package metadata in sync when a library release changes the public package version.

---

## Release And Packaging Notes

The repository includes release-process guidance in project rules and consistency runbooks. At a minimum, maintainers should confirm the following before calling a release complete:

- Tests pass.
- Documentation is updated.
- Version metadata is in sync.
- The package build and documentation build both succeed.

---

## Additional Resources

- **[Code Style Guide](style-guide.md)** - Canonical Python coding expectations for this project.
- **[Documentation Style Guide](../STYLE_GUIDE.md)** - Writing and formatting rules for docs pages.
- **[Consistency Runbooks](consistency/index.md)** - Repository cleanup notes and gap analysis.
- **[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)** - Report bugs or doc problems.
- **[GitHub Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Ask project questions.
