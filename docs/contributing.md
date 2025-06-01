# Contributing to WFRMLS Python API Wrapper

Thank you for your interest in contributing to the WFRMLS Python API wrapper! This guide will help you get started with development and ensure your contributions follow our standards.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Code Standards](#code-standards)
4. [Documentation Requirements](#documentation-requirements)
5. [Testing Guidelines](#testing-guidelines)
6. [Submitting Changes](#submitting-changes)
7. [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Access to WFRMLS API (for testing)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
git clone https://github.com/YOUR_USERNAME/wfrmls.git
cd wfrmls
   ```

3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/theperrygroup/wfrmls.git
   ```

## Development Environment

### 1. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
WFRMLS_BEARER_TOKEN=your_test_api_key_here
```

### 4. Verify Setup

```bash
# Run tests to verify everything works
pytest

# Check code formatting
black --check .
isort --check-only .

# Run type checking
mypy wfrmls/

# Run linting
flake8 wfrmls/
```

## Code Standards

We follow strict code quality standards to ensure consistency and maintainability.

### Code Formatting

We use Black with isort for code formatting:

```bash
# Format code
black .
isort .

# Check formatting
black --check .
isort --check-only .
```

### Type Hints

All code must include comprehensive type hints:

```python
from typing import Dict, List, Optional, Any
from datetime import date

def search_properties(
    self,
    city: Optional[str] = None,
    max_price: Optional[int] = None,
    date_from: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Search properties with type hints for all parameters."""
    # Implementation
```

### Docstring Standards

Use Google-style docstrings for all public methods:

```python
def get_property(self, property_id: str) -> Dict[str, Any]:
    """Get detailed information for a specific property.

    Args:
        property_id: The unique identifier for the property

    Returns:
        Dictionary containing detailed property information including:
        - ListingKey: Property identifier
        - UnparsedAddress: Full address
        - ListPrice: Current listing price
        - PropertyType: Type of property

    Raises:
        WFRMLSError: If the API request fails
        AuthenticationError: If authentication is invalid
        ValidationError: If property_id format is invalid

    Example:
        ```python
        client = WFRMLSClient()
        property_data = client.properties.get_property("123456")
        print(f"Address: {property_data['UnparsedAddress']}")
        ```
    """
```

### Error Handling

Use our custom exception hierarchy:

```python
from wfrmls.exceptions import WFRMLSError, AuthenticationError, ValidationError

def example_method(self, param: str) -> Dict[str, Any]:
    """Example method with proper error handling."""
    if not param:
        raise ValidationError("Parameter 'param' is required")
    
    try:
        response = self.get(f"/endpoint/{param}")
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif e.response.status_code == 404:
            raise WFRMLSError(f"Resource not found: {param}")
        else:
            raise WFRMLSError(f"API error: {e}")
```

## Documentation Requirements

### Automatic Documentation Updates

**CRITICAL**: When making any code changes, you MUST update documentation following our [Documentation Maintenance Rules](../WFRMLS_DOCUMENTATION_RULES.md).

### Documentation Checklist

For every change:
- [ ] Updated docstrings with new parameters/behavior
- [ ] Updated examples in `docs/examples.md` if applicable
- [ ] Updated `docs/api-reference.md` for new/changed endpoints
- [ ] Added entries to `docs/changelog.md` for user-facing changes
- [ ] Verified all examples still work
- [ ] Updated type hints throughout

### Documentation Testing

Test your documentation changes:

```bash
# Test code examples in documentation
python -m doctest docs/examples.md

# Verify all examples are runnable
python scripts/test_examples.py  # If such script exists
```

## Testing Guidelines

### Test Structure

We maintain 100% test coverage. Tests are organized by module:

```
tests/
├── test_properties.py      # Properties client tests
├── test_member.py          # Member client tests
├── test_office.py          # Office client tests
├── test_media.py           # Media client tests
├── test_analytics.py       # Analytics client tests
├── test_exceptions.py      # Exception handling tests
└── test_base_client.py     # Base client functionality
```

### Writing Tests

#### Test Class Structure

```python
"""Tests for the properties client."""

import pytest
import responses
from datetime import date

from wfrmls.properties import PropertiesClient
from wfrmls.exceptions import WFRMLSError, ValidationError


class TestPropertiesClientInit:
    """Test PropertiesClient initialization."""

    def test_init_with_api_key(self) -> None:
        """Test initialization with provided API key."""
        client = PropertiesClient(api_key="test_key")
        assert client.api_key == "test_key"

    def test_init_without_api_key_raises_error(self) -> None:
        """Test initialization without API key raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            PropertiesClient()


class TestPropertiesClientMethods:
    """Test PropertiesClient methods."""

    def setup_method(self) -> None:
        """Set up test client for each test method."""
        self.client = PropertiesClient(api_key="test_key")

    @responses.activate
    def test_search_properties_success(self) -> None:
        """Test successful property search."""
        # Mock API response
        responses.add(
            responses.GET,
            "https://api.wfrmls.com/reso/odata/Property",
            json=[
                {
                    "ListingKey": "123456",
                    "UnparsedAddress": "123 Main St, Salt Lake City, UT",
                    "ListPrice": 450000
                }
            ],
            status=200
        )

        # Test method
        properties = self.client.search_properties(city="Salt Lake City")
        
        # Assertions
        assert len(properties) == 1
        assert properties[0]["ListingKey"] == "123456"
        assert properties[0]["ListPrice"] == 450000

    @responses.activate
    def test_search_properties_with_filters(self) -> None:
        """Test property search with multiple filters."""
        responses.add(
            responses.GET,
            "https://api.wfrmls.com/reso/odata/Property",
            json=[],
            status=200
        )

        properties = self.client.search_properties(
            city="Salt Lake City",
            min_list_price=200000,
            max_list_price=500000,
            property_type="Residential"
        )

        assert isinstance(properties, list)

    def test_search_properties_invalid_parameters(self) -> None:
        """Test search with invalid parameters raises ValidationError."""
        with pytest.raises(ValidationError):
            self.client.search_properties(min_list_price=-1000)
```

#### Integration Tests

For testing against real API endpoints:

```python
import os
import pytest

@pytest.mark.integration
class TestPropertiesIntegration:
    """Integration tests for properties client."""

    @pytest.fixture(scope="class")
    def client(self):
        """Create client for integration tests."""
        api_key = os.getenv("WFRMLS_BEARER_TOKEN")
        if not api_key:
            pytest.skip("Integration tests require WFRMLS_BEARER_TOKEN")
        return PropertiesClient(api_key=api_key)

    def test_search_properties_real_api(self, client):
        """Test search against real API."""
        properties = client.search_properties(
            city="Salt Lake City",
            page_size=5  # Small number for testing
        )
        assert isinstance(properties, list)
        if properties:  # Only check if results exist
            assert "ListingKey" in properties[0]
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=wfrmls --cov-report=html

# Run specific test file
pytest tests/test_properties.py

# Run with specific markers
pytest -m "not integration"  # Skip integration tests
pytest -m "integration"      # Run only integration tests

# Run specific test method
pytest tests/test_properties.py::TestPropertiesClient::test_search_properties_success
```

### Test Coverage

Maintain 100% test coverage:

```bash
# Generate coverage report
pytest --cov=wfrmls --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=wfrmls --cov-report=html
open htmlcov/index.html
```

## Submitting Changes

### Branch Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/description-of-change
   ```

2. Make your changes following all guidelines above

3. Add tests for new functionality

4. Update documentation (following our documentation rules)

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add property search filtering

   - Add support for price range filtering
   - Add city and property type filters
   - Update documentation with examples
   - Add comprehensive tests
   
   Fixes #123"
   ```

### Commit Message Format

Use conventional commits:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### Pre-commit Checks

Before submitting, ensure all checks pass:

```bash
# Format code
black .
isort .

# Run all tests
pytest --cov=wfrmls

# Type checking
mypy wfrmls/

# Linting
flake8 wfrmls/

# Check documentation
# Verify examples work and are up to date
```

### Pull Request Process

1. Push your branch to your fork:
   ```bash
   git push origin feature/description-of-change
   ```

2. Create a pull request on GitHub

3. Fill out the pull request template completely

4. Ensure all CI checks pass

5. Address any review feedback

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation
- [ ] Verified examples work

## Documentation
- [ ] Updated docstrings
- [ ] Updated API reference if needed
- [ ] Updated examples if needed
- [ ] Updated changelog for user-facing changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Release Process

### Version Bumping

When preparing a release:

1. Update version in `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

2. Update version in `wfrmls/__init__.py`:
   ```python
   __version__ = "1.1.0"
   ```

3. Update `docs/changelog.md` with release notes

4. Create release commit:
   ```bash
   git commit -m "chore: bump version to 1.1.0"
   ```

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Changelog is updated
- [ ] Version numbers are consistent
- [ ] Examples work with new version
- [ ] Breaking changes are documented

### Publishing

1. Tag the release:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

2. Build and test package:
   ```bash
   python -m build
   python -m twine check dist/*
   ```

3. Publish to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Getting Help

### Development Questions

- Check existing GitHub Issues
- Review the [Style Guide](../STYLE_GUIDE.md)
- Look at existing code patterns in the codebase

### Setting Up Development Environment

- Ensure Python 3.8+ is installed
- Use virtual environments
- Install development dependencies
- Set up API key for testing

### Common Issues

**Import errors**: Ensure you installed in development mode with `pip install -e ".[dev]"`

**Test failures**: Check that your API key is set and valid

**Type errors**: Ensure all public methods have complete type hints

**Coverage issues**: Add tests for all new code paths

Remember: Quality contributions include code, tests, and documentation updates. Follow our documentation maintenance rules to ensure your changes are properly documented! 