# WFRMLS Documentation

This directory contains the documentation for the WFRMLS Python API wrapper, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Quick Start

To build and serve the documentation locally:

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Serve the documentation locally
mkdocs serve
```

The documentation will be available at http://127.0.0.1:8000

## Building for Production

```bash
# Build static HTML files
mkdocs build

# The built documentation will be in the site/ directory
```

## Documentation Structure

- `index.md` - Main landing page
- `installation.md` - Installation instructions
- `quickstart.md` - Quick start guide
- `examples.md` - Comprehensive examples
- `api-reference.md` - Complete API reference
- `troubleshooting.md` - Common issues and solutions
- `contributing.md` - Development guidelines
- `changelog.md` - Version history
- `deployment.md` - Production deployment guide

## Documentation Rules

When making changes to the WFRMLS library code, follow the documentation maintenance rules in `../WFRMLS_DOCUMENTATION_RULES.md` to ensure documentation stays current.

## Configuration

The documentation is configured in `../mkdocs.yml`. Key features:

- **Material Theme**: Modern, responsive design
- **Code Highlighting**: Syntax highlighting for Python code
- **Search**: Full-text search functionality
- **Navigation**: Tabbed navigation with sections
- **Dark/Light Mode**: Theme switching
- **Auto-generated API Docs**: Using mkdocstrings
- **Copy Code**: One-click code copying
- **Mermaid Diagrams**: Support for flowcharts and diagrams

## Contributing to Documentation

1. Follow the [ReZEN documentation process](../WFRMLS_DOCUMENTATION_RULES.md)
2. Update documentation when code changes
3. Test locally with `mkdocs serve`
4. Ensure all examples work
5. Check links and formatting 