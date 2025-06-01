# WFRMLS Documentation Rules

This document outlines the documentation standards and rules for the WFRMLS Python API wrapper project.

## Overview

The WFRMLS project follows strict documentation standards to ensure consistency, clarity, and maintainability of all documentation.

## Documentation Standards

### 1. Documentation Structure

- **Repository Name**: Always use "wfrmls", never "wfrmls-python"
- **Repository URL**: `https://github.com/theperrygroup/wfrmls`
- **Documentation Site**: `https://theperrygroup.github.io/wfrmls/`

### 2. MkDocs Configuration

- Use MkDocs Material theme without custom CSS/JavaScript by default
- Google-style docstrings with mkdocstrings plugin
- No ReZEN references in WFRMLS project documentation

### 3. Deployment Rules

- Documentation deployed via GitHub Pages only
- No Netlify deployment workflows
- Active workflows: CI, Docs (GitHub Pages), and Release management

### 4. Content Guidelines

- All code examples must be runnable
- Include comprehensive type hints
- Use Google-style docstrings for all functions and classes
- Maintain 100% test coverage documentation

### 5. File Organization

```
docs/
├── index.md                    # Homepage
├── installation.md             # Installation guide
├── quickstart.md              # Quick start guide
├── examples.md                # Usage examples
├── api-reference.md           # API documentation
├── troubleshooting.md         # Common issues
├── contributing.md            # Contribution guidelines
├── changelog.md               # Release notes
├── deployment.md              # Deployment guide
├── STYLE_GUIDE.md            # Code style guide
└── LICENSE                    # License file
```

### 6. Version Management

- Use semantic versioning
- Update version in both `wfrmls/__init__.py` and `pyproject.toml`
- Maintain changelog for all releases

### 7. Link Standards

- All internal links use relative paths
- External links include full URLs
- Repository links always point to `https://github.com/theperrygroup/wfrmls`

## Enforcement

These rules are enforced through:

- CI/CD pipeline checks
- Documentation build validation
- Code review process
- Automated testing of documentation examples

## Compliance

All documentation changes must comply with these rules. Non-compliant documentation will not be merged until brought into compliance. 