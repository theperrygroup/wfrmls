# Development

Welcome to the WFRMLS development documentation! This section contains everything you need to contribute to the project, set up development environments, and understand the codebase.

## 🛠️ Developer Resources

<div class="grid cards" markdown>

-   :material-hand-heart:{ .lg .middle } **Contributing**

    ---

    Guidelines for contributing code, documentation, and reporting issues

    [:octicons-arrow-right-24: Contributing Guide](contributing.md)

-   :material-cog:{ .lg .middle } **Development Setup**

    ---

    Set up your local development environment

    [:octicons-arrow-right-24: Development Setup](development-setup.md)

-   :material-test-tube:{ .lg .middle } **Testing**

    ---

    Running tests, writing test cases, and ensuring code quality

    [:octicons-arrow-right-24: Testing Guide](testing.md)

-   :material-rocket:{ .lg .middle } **Deployment**

    ---

    Deployment processes, CI/CD, and release management

    [:octicons-arrow-right-24: Deployment](deployment.md)

-   :material-code-tags:{ .lg .middle } **Style Guide**

    ---

    Code style conventions and formatting standards

    [:octicons-arrow-right-24: Style Guide](style-guide.md)

</div>

## Quick Start for Contributors

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/wfrmls.git
cd wfrmls
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wfrmls --cov-report=html
```

### 4. Make Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes...
# Run tests and linting
pytest
black wfrmls/ tests/
flake8 wfrmls/ tests/

# Commit and push
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### 5. Submit Pull Request
Open a pull request on GitHub with a clear description of your changes.

## Development Workflow

### 🔄 Standard Process
1. **Issue First**: Create or find an issue to work on
2. **Branch**: Create a feature branch from `main`
3. **Develop**: Write code following our style guide
4. **Test**: Ensure all tests pass and add new tests
5. **Document**: Update documentation as needed
6. **Review**: Submit PR for code review
7. **Merge**: Maintainer merges after approval

### 📝 Commit Conventions
We follow conventional commits:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example: `feat: add property search by radius functionality`

## Project Structure

```
wfrmls/
├── wfrmls/              # Main package
│   ├── __init__.py
│   ├── client.py        # Main client class
│   ├── properties.py    # Property API client
│   ├── members.py       # Member API client
│   ├── exceptions.py    # Custom exceptions
│   └── ...
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test data
├── docs/               # Documentation
├── examples/           # Example scripts
├── pyproject.toml      # Project configuration
└── README.md
```

## Code Quality Standards

### ✅ Requirements
- **Test Coverage**: Maintain 100% test coverage
- **Type Hints**: Use comprehensive type annotations
- **Docstrings**: Google-style docstrings for all public APIs
- **Linting**: Pass flake8, black, and mypy checks
- **Performance**: No performance regressions

### 🔧 Tools We Use
- **Testing**: pytest, pytest-cov
- **Formatting**: black, isort
- **Linting**: flake8, mypy
- **Documentation**: mkdocs, mkdocstrings
- **CI/CD**: GitHub Actions

## Getting Help

### 💬 Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community chat
- **Pull Requests**: Code review and collaboration

### 📚 Additional Resources
- [Python Best Practices](https://docs.python.org/3/tutorial/)
- [RESO Standards](https://www.reso.org/reso-data-dictionary/)
- [OData v4 Specification](https://docs.oasis-open.org/odata/odata/v4.01/)

## Recognition

### 🏆 Contributors
We appreciate all contributors! Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributor graphs

### 🎯 Areas Needing Help
We especially welcome contributions in:
- Documentation improvements
- Example applications
- Performance optimizations
- API endpoint coverage
- Error handling enhancements

## Release Process

### 📋 Release Checklist
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch
4. Run full test suite
5. Build and test package
6. Create GitHub release
7. Publish to PyPI

### 🏷️ Versioning
We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

---

*Ready to contribute? Start with our [Contributing Guide](contributing.md) or check out [good first issues](https://github.com/theperrygroup/wfrmls/labels/good%20first%20issue) on GitHub!* 