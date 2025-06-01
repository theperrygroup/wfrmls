# WFRMLS Python Client - Documentation Maintenance Rules

## 🔄 Auto-Documentation Updates
When making ANY changes to the WFRMLS library code, you MUST automatically update the corresponding documentation:

### Code Changes → Documentation Updates

#### 1. Function/Method Changes
When modifying any function or method in `wfrmls/`:
- **Update Google-format docstring** with new parameters, return types, or behavior changes
- **Update examples in docstring** to reflect new usage patterns
- **Check and update** corresponding examples in `docs/examples.md`
- **Update API reference** in `docs/api-reference.md` if method signatures change
- **Update type hints** throughout affected files

#### 2. New Endpoints/Methods
When adding new functionality to any client in `wfrmls/`:
- **Add comprehensive Google-format docstrings** with examples showing real-world usage
- **Add usage examples** to `docs/examples.md` with practical scenarios
- **Update `docs/api-reference.md`** with new endpoint documentation
- **Update main `README.md`** if it's a major feature addition
- **Add corresponding test documentation** in test files with clear descriptions
- **Update `wfrmls/__init__.py`** exports if adding new public classes/functions

#### 3. Parameter Changes
When changing function signatures in any `wfrmls/` file:
- **Update all docstrings** with new parameter descriptions and types
- **Update type hints** throughout the codebase for consistency
- **Update all examples** in documentation that use the changed functions
- **Update troubleshooting docs** if error conditions or parameter validation changes
- **Add migration notes** to `docs/changelog.md` for breaking changes

#### 4. Breaking Changes
When making breaking changes to any client or method:
- **Update `docs/changelog.md`** with detailed migration notes and version information
- **Update all affected examples** across all documentation files
- **Update version number** in `wfrmls/__init__.py` and `pyproject.toml`
- **Add deprecation warnings** to old methods with clear migration paths
- **Create migration guides** with before/after code examples

### 📝 Specific Documentation Files to Maintain

#### Core Documentation Files
- **`docs/api-reference.md`** - Keep endpoint documentation synchronized with actual code
- **`docs/examples.md`** - Ensure all examples work with current API and show best practices
- **`docs/quickstart.md`** - Update getting started examples to reflect current API
- **`docs/troubleshooting.md`** - Add new error conditions, solutions, and common issues
- **`README.md`** - Keep main examples, feature lists, and installation instructions current
- **`docs/changelog.md`** - Document all changes with version numbers and migration notes

#### Supporting Documentation
- **`docs/installation.md`** - Update dependencies, Python version requirements
- **`docs/contributing.md`** - Keep development setup and contribution guidelines current
- **`docs/deployment.md`** - Update production deployment recommendations

### 🧪 Documentation Quality Standards
Always ensure documentation includes:

#### Docstring Requirements
- **Google-format docstrings** for ALL public methods and classes
- **Complete type hints** for all parameters, return values, and class attributes
- **Usage examples** showing real-world scenarios with actual WFRMLS data patterns
- **Error handling examples** for common failure cases and API errors
- **Parameter validation** documentation explaining valid values and constraints
- **Cross-references** to related methods, classes, and concepts

#### Code Example Standards
- **Runnable examples** that work with actual WFRMLS API endpoints
- **Error handling** demonstrations in examples
- **Real-world scenarios** not just basic "hello world" examples
- **Consistent naming** and code style across all examples
- **Current API patterns** reflecting the latest best practices

### 🧪 Test Documentation Updates
When updating tests in `tests/`:
- **Update test docstrings** to reflect new test scenarios and edge cases
- **Ensure test method names** clearly describe what functionality they test
- **Update test documentation** in `docs/contributing.md` with new testing patterns
- **Maintain 100% test coverage** documentation and reports
- **Document integration test** requirements and setup

### 🔢 Version Management
When updating version numbers:
- **Update `wfrmls/__init__.py`** `__version__` attribute
- **Update `pyproject.toml`** version field
- **Add comprehensive entry** to `docs/changelog.md` with all changes
- **Update version references** in documentation examples if needed
- **Tag release** with consistent version numbering

### 📋 Checklist for Every Code Change

Before completing any change to the WFRMLS library:
- [ ] **Updated relevant docstrings** with new parameters, behavior, examples
- [ ] **Updated examples** in affected documentation files to work with changes
- [ ] **Updated API reference** if method signatures, parameters, or return types changed
- [ ] **Updated changelog** if user-facing change (any public API modification)
- [ ] **Verified all examples** still work by running them against actual API
- [ ] **Updated type hints** if signatures, parameters, or return types changed
- [ ] **Added test documentation** for new features with clear descriptions
- [ ] **Updated version numbers** consistently if making a release
- [ ] **Validated imports and exports** in `__init__.py` files

### 🚨 Documentation Validation Rules

#### Quality Gates
- **All public methods** MUST have comprehensive docstrings with examples
- **All examples** in documentation MUST be runnable and current
- **Version numbers** MUST be consistent across `pyproject.toml`, `__init__.py`, and docs
- **Breaking changes** MUST be documented in changelog with migration examples
- **New features** MUST include usage examples showing real WFRMLS scenarios
- **Type hints** MUST be complete and accurate for all public APIs

#### Testing Documentation
- **API examples** must be tested against actual WFRMLS endpoints (when possible)
- **Code snippets** in documentation should be syntax-highlighted and properly formatted
- **Error handling examples** should show actual exception types and messages
- **Integration examples** should demonstrate real-world usage patterns

### 📂 Documentation Structure to Maintain

```
docs/
├── index.md                 # Main landing page with overview and quick links
├── installation.md          # Detailed setup instructions and troubleshooting
├── quickstart.md           # 5-minute getting started guide
├── api-reference.md        # Complete API documentation with all endpoints
├── examples.md             # Comprehensive examples for all major use cases
├── troubleshooting.md      # Common issues, solutions, and debugging
├── contributing.md         # Development guide and contribution workflow
├── changelog.md            # Complete version history with migration notes
└── deployment.md           # Production deployment and best practices
```

## 🎯 Code Quality Rules for WFRMLS

### Style & Standards
- **Use Black code formatter**: `black .` with 88-character line length
- **Follow Google docstring format** consistently across all modules
- **Include comprehensive type hints** for all public APIs
- **Maintain 100% test coverage** with meaningful tests
- **Follow existing naming conventions** as defined in `STYLE_GUIDE.md`
- **Use isort for import organization** with Black-compatible settings

### Security & Best Practices
- **Never commit API keys** or sensitive tokens to repository
- **Use environment variables** for all configuration (`WFRMLS_BEARER_TOKEN`)
- **Validate all input parameters** with appropriate error messages
- **Handle all possible error conditions** with custom exception types
- **Follow principle of least surprise** in API design and method naming

### Testing Requirements
- **Write tests for all new functionality** including edge cases
- **Maintain 100% code coverage** without sacrificing test quality
- **Include both unit and integration tests** where appropriate
- **Test error conditions and edge cases** thoroughly
- **Use descriptive test method names** that explain what is being tested
- **Mock external API calls** in unit tests using `responses` library

### Release Process
When preparing for any release:
1. **Update version** in `pyproject.toml` and `wfrmls/__init__.py`
2. **Update changelog** with all changes, breaking changes, and migration notes
3. **Verify all documentation** is current and examples work
4. **Run full test suite** with 100% coverage
5. **Build and test package** locally before publishing
6. **Update deployment documentation** if deployment process changes

## 🤖 Automation Rules for WFRMLS

### Auto-Generated Content
These should be automatically maintained when code changes:
- **API reference documentation** generated from docstrings
- **Test coverage reports** with HTML output
- **Package dependency lists** in requirements files
- **Version consistency checks** across all files
- **Import/export validation** in `__init__.py` files

### Continuous Integration Requirements
Ensure CI processes validate:
- **Documentation builds successfully** without warnings
- **All examples are runnable** and produce expected output
- **Internal and external links** in documentation work correctly
- **Code formatting is consistent** with Black and isort
- **Type checking passes** with mypy strict mode
- **Test coverage remains** at 100% for all new code

### WFRMLS-Specific Automation
- **Endpoint completion tracking** in task files when new endpoints are added
- **API documentation synchronization** with actual endpoint implementations
- **Error message consistency** across all client modules
- **Example data validation** using real WFRMLS data patterns

## 🔧 WFRMLS-Specific Documentation Rules

### API Wrapper Documentation
- **Each client class** (`properties.py`, `member.py`, etc.) must have complete documentation
- **All search methods** must document available filters and parameter formats
- **All get methods** must document expected return data structures
- **Pagination examples** must be included for all search endpoints
- **Error handling** must show WFRMLS-specific error codes and messages

### Endpoint Documentation Pattern
For each endpoint implemented:
```python
def search_properties(
    self,
    city: Optional[str] = None,
    max_list_price: Optional[int] = None,
    # ... other parameters
) -> List[Dict[str, Any]]:
    """Search properties with specified criteria.

    Args:
        city: Filter by city name (exact match)
        max_list_price: Maximum listing price in dollars
        # ... document all parameters

    Returns:
        List of property dictionaries with keys including:
        - ListingKey: Unique property identifier
        - UnparsedAddress: Full property address
        - ListPrice: Current listing price
        # ... document key return fields

    Raises:
        WFRMLSError: If API request fails
        AuthenticationError: If API key is invalid
        ValidationError: If parameters are invalid

    Example:
        ```python
        # Search for homes under $500k in Salt Lake City
        properties = client.properties.search_properties(
            city="Salt Lake City",
            max_list_price=500000,
            property_type="Residential"
        )
        
        for prop in properties:
            print(f"{prop['UnparsedAddress']}: ${prop['ListPrice']}")
        ```

    Note:
        - Results are paginated with default page_size of 20
        - Use page_number parameter for additional pages
        - See get_property() for detailed property information
    """
```

### Task Completion Documentation
When implementing endpoints from `tasks/`:
- **Mark endpoint as completed** in the task file
- **Add implementation notes** about any deviations from API docs
- **Document any limitations** or special requirements
- **Update progress tracking** in project status files

Remember: **Documentation is code!** Treat it with the same rigor and attention to detail as the WFRMLS library implementation itself. The documentation is often the first (and sometimes only) interaction users have with your code. 