# Development

Resources for contributing to the WFRMLS Python client and following development best practices.

---

## 🛠️ Development Resources

<div class="grid cards" markdown>

-   :material-source-pull:{ .lg .middle } **Contributing**

    ---

    Guidelines for contributing code, reporting bugs, and requesting features

    [:octicons-arrow-right-24: Contribution Guide](contributing.md)

-   :material-test-tube:{ .lg .middle } **Testing**

    ---

    Running tests, writing test cases, and ensuring code quality

    [:octicons-arrow-right-24: Testing Guide](testing.md)

-   :material-rocket-launch:{ .lg .middle } **Release Process**

    ---

    How releases are managed and versioned

    [:octicons-arrow-right-24: Release Process](releases.md)

-   :material-code-tags:{ .lg .middle } **Style Guide**

    ---

    Code formatting, naming conventions, and best practices

    [:octicons-arrow-right-24: Style Guide](style-guide.md)

</div>

---

## 🚀 Quick Start for Contributors

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wfrmls --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code
black wfrmls/ tests/

# Check linting
flake8 wfrmls/ tests/

# Type checking
mypy wfrmls/

# Run all quality checks
make quality
```

---

## 📋 Development Workflow

### 1. **Issue Creation**

Before starting work:

- Check existing issues and discussions
- Create detailed issue with use case
- Wait for feedback from maintainers
- Get issue assigned before starting work

### 2. **Branch Strategy**

```bash
# Create feature branch
git checkout -b feature/add-new-endpoint

# Create bugfix branch
git checkout -b bugfix/fix-authentication-error

# Create documentation branch
git checkout -b docs/update-api-reference
```

### 3. **Development Process**

1. **Write Tests First** - Follow TDD when possible
2. **Implement Feature** - Keep changes focused and small
3. **Update Documentation** - Include docstrings and guides
4. **Run Quality Checks** - Ensure all checks pass
5. **Manual Testing** - Test with real API calls

### 4. **Pull Request Process**

1. **Commit Changes** - Use conventional commit messages
2. **Push Branch** - Push to your fork
3. **Create PR** - Use provided template
4. **Address Feedback** - Respond to review comments
5. **Merge** - Maintainer will merge when ready

---

## 🧪 Testing Strategy

### Test Categories

| Type | Location | Purpose | Coverage |
|------|----------|---------|----------|
| **Unit Tests** | `tests/unit/` | Test individual functions | >95% |
| **Integration Tests** | `tests/integration/` | Test API interactions | Key workflows |
| **End-to-End Tests** | `tests/e2e/` | Test complete scenarios | Critical paths |

### Writing Tests

```python
import pytest
from wfrmls import WFRMLSClient
from wfrmls.exceptions import ValidationError

class TestPropertyAPI:
    """Test property API functionality."""
    
    def test_get_properties_success(self, mock_client):
        """Test successful property retrieval."""
        # Arrange
        expected_properties = [{"ListingId": "12345678"}]
        mock_client.property.get_properties.return_value = expected_properties
        
        # Act
        result = mock_client.property.get_properties(top=1)
        
        # Assert
        assert result == expected_properties
        mock_client.property.get_properties.assert_called_once_with(top=1)
    
    def test_get_properties_validation_error(self, mock_client):
        """Test validation error handling."""
        # Act & Assert
        with pytest.raises(ValidationError):
            mock_client.property.get_properties(top=-1)
```

### Test Configuration

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_client():
    """Create mock WFRMLS client for testing."""
    client = Mock(spec=WFRMLSClient)
    client.property = Mock()
    client.member = Mock()
    client.office = Mock()
    return client

@pytest.fixture
def sample_property():
    """Sample property data for testing."""
    return {
        "ListingId": "12345678",
        "ListPrice": 450000,
        "StandardStatus": "Active",
        "City": "Salt Lake City"
    }
```

---

## 📖 Documentation Standards

### Code Documentation

```python
def get_properties(
    self,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    filter_query: Optional[str] = None,
    select: Optional[List[str]] = None,
    orderby: Optional[str] = None,
    count: bool = False
) -> List[Dict[str, Any]]:
    """Retrieve property listings from WFRMLS.
    
    This method fetches property data with optional filtering, sorting,
    and pagination. All parameters follow OData v4 conventions.
    
    Args:
        top: Maximum number of results to return. Defaults to API limit.
        skip: Number of results to skip for pagination. Defaults to 0.
        filter_query: OData filter expression for filtering results.
            Example: "StandardStatus eq 'Active' and ListPrice gt 500000"
        select: List of specific fields to include in response.
            Example: ["ListingId", "ListPrice", "City"]
        orderby: Field(s) to sort by with optional direction.
            Example: "ListPrice desc" or "City asc, ListPrice desc"
        count: Whether to include total count in response metadata.
    
    Returns:
        List of property dictionaries matching the query criteria.
        Each dictionary contains the requested fields or all available
        fields if select parameter is not specified.
    
    Raises:
        ValidationError: If query parameters are invalid.
        AuthenticationError: If API credentials are invalid.
        RateLimitError: If API rate limits are exceeded.
        NotFoundError: If no results match the query (rare).
        WFRMLSError: For other API-related errors.
    
    Examples:
        Basic usage:
        
        >>> client = WFRMLSClient()
        >>> properties = client.property.get_properties(top=10)
        >>> len(properties)
        10
        
        With filtering:
        
        >>> active_properties = client.property.get_properties(
        ...     filter_query="StandardStatus eq 'Active'",
        ...     select=["ListingId", "ListPrice"],
        ...     orderby="ListPrice desc"
        ... )
        
        With pagination:
        
        >>> page_1 = client.property.get_properties(top=50, skip=0)
        >>> page_2 = client.property.get_properties(top=50, skip=50)
    
    Note:
        Large result sets are automatically paginated by the API.
        Consider using the skip parameter for manual pagination
        when processing large datasets.
    """
```

### README Updates

When adding new features, update:

- **Installation instructions** - If new dependencies
- **Usage examples** - Show new functionality
- **API documentation** - Link to detailed docs
- **Contributing guide** - If new development requirements

---

## 🔧 Build & Release

### Local Development Build

```bash
# Install in development mode
pip install -e .

# Build source distribution
python -m build --sdist

# Build wheel
python -m build --wheel

# Check package
twine check dist/*
```

### Version Management

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0) - Breaking changes
- **MINOR** (1.1.0) - New features, backward compatible
- **PATCH** (1.1.1) - Bug fixes, backward compatible

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Tagged in git
- [ ] Published to PyPI

---

## 🎨 Code Style

### Python Code Standards

```python
# Good: Clear, descriptive names
def get_active_properties_by_city(city_name: str) -> List[Dict[str, Any]]:
    """Get active properties in a specific city."""
    pass

# Bad: Unclear abbreviations
def get_act_props_by_c(c: str) -> List[Dict]:
    pass

# Good: Type hints and docstrings
from typing import Optional, List, Dict, Any

def search_properties(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Search properties within a price range.
    
    Args:
        min_price: Minimum listing price filter.
        max_price: Maximum listing price filter.
        
    Returns:
        List of property dictionaries matching criteria.
    """
    pass

# Good: Error handling
try:
    properties = client.property.get_properties()
except WFRMLSError as e:
    logger.error(f"Failed to fetch properties: {e}")
    raise
```

### Import Organization

```python
# Standard library imports
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

# Third-party imports
import requests
from requests.adapters import HTTPAdapter

# Local imports
from wfrmls.exceptions import WFRMLSError, ValidationError
from wfrmls.utils import validate_parameters
```

---

## 📚 Additional Resources

### **Contributing**
- **[Contributing Guide](contributing.md)** - Detailed contribution process
- **[Code of Conduct](https://github.com/theperrygroup/wfrmls/blob/main/CODE_OF_CONDUCT.md)** - Community standards
- **[Issue Templates](https://github.com/theperrygroup/wfrmls/tree/main/.github/ISSUE_TEMPLATE)** - Bug reports and feature requests

### **Quality Assurance**
- **[Testing Guide](testing.md)** - Comprehensive testing documentation
- **[Style Guide](style-guide.md)** - Code formatting and conventions
- **[Security Policy](https://github.com/theperrygroup/wfrmls/blob/main/SECURITY.md)** - Vulnerability reporting

### **Project Management**
- **[Release Process](releases.md)** - How releases are managed
- **[Roadmap](https://github.com/theperrygroup/wfrmls/projects)** - Future development plans
- **[Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Community conversations

---

## 🤝 Getting Help

### **For Contributors**
- **[GitHub Discussions](https://github.com/theperrygroup/wfrmls/discussions)** - Ask development questions
- **[Discord Community](https://discord.gg/wfrmls)** - Real-time chat (if available)
- **[Office Hours](contributing.md#office-hours)** - Weekly maintainer availability

### **For Maintainers**
- **Release Automation** - CI/CD processes and scripts
- **Review Guidelines** - Code review best practices
- **Triage Process** - Issue classification and prioritization

---

*Ready to contribute? Start with our [Contributing Guide](contributing.md) or explore the [Testing Documentation](testing.md).* 