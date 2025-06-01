# Changelog

All notable changes to the WFRMLS Python API wrapper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Repository URL updates and documentation improvements

### Removed
- **TEMPORARY**: Disabled Media, History, and Green Verification endpoints due to server-side issues
  - Media endpoints: 504 Gateway Timeout errors
  - History endpoints: Missing entity type `HistoryTransactional` 
  - Green Verification endpoints: Missing entity type `PropertyGreenVerification`
  - These endpoints will be restored once server issues are resolved

### Fixed
- All unit tests now pass after removing problematic server-side endpoints
- Updated documentation to reflect current endpoint availability

## [1.2.1] - 2024-12-21

### Fixed
- GitHub Pages deployment workflow issues
- Documentation build warnings and navigation errors
- Missing requirements-docs.txt file for documentation dependencies

### Changed
- Simplified documentation deployment workflow to focus on documentation building
- Removed test execution from docs workflow to prevent deployment failures
- Improved documentation file organization and structure

### Added
- Complete documentation requirements file (requirements-docs.txt)
- STYLE_GUIDE.md to docs directory for proper navigation

## [1.2.0] - 2024-12-20

### Added
- Enhanced GitHub Actions CI/CD workflows with multi-version testing
- Automated release management and documentation deployment
- Comprehensive test coverage reporting

### Fixed
- CI workflow robustness improvements
- Test discovery and execution reliability

## [1.1.0] - 2024-12-19

### Added
- Comprehensive documentation structure following industry best practices
- Auto-documentation maintenance rules with WFRMLS_DOCUMENTATION_RULES.md
- Version consistency validation across all files
- Professional MkDocs documentation site with Material theme
- Complete API reference structure (ready for code implementation)
- Detailed installation, quickstart, and troubleshooting guides
- Contributing guidelines with development workflow
- Deployment guide for production usage

### Changed
- Enhanced documentation with more detailed examples and troubleshooting
- Updated repository references to correct GitHub organization (theperrygroup/wfrmls)
- Improved MkDocs configuration with proper theming and navigation
- Documentation URLs updated to use GitHub Pages

### Fixed
- Repository URL corrections throughout all documentation files
- MkDocs build issues with FontAwesome icons (switched to Material Design icons)
- Documentation link consistency across all files

## [1.0.0] - 2024-01-15

### Added
- Complete WFRMLS API wrapper implementation
- Support for all major endpoints:
  - Properties (search, get, analytics)
  - Members (agents and member data)  
  - Offices (brokerage information)
  - Media (property photos and documents)
  - Analytics (market statistics and reporting)
  - Lookup (reference data and valid values)
  - History (property and listing history)
  - Open Houses (event information)
  - ADU (Accessory Dwelling Unit data)
  - Green Verification (building certifications)
  - Resource (API metadata)
  - Data System (system information)
  - Property Unit Types (classification data)
- Comprehensive type hints throughout codebase
- Google-style docstrings for all public methods
- Custom exception hierarchy with meaningful error messages
- 100% test coverage with pytest
- Environment variable support for API key management
- Rate limiting and error handling best practices
- Support for Python 3.8+

### Infrastructure
- Black code formatting with 88-character line length
- isort import organization
- mypy strict type checking
- flake8 linting
- pytest with coverage reporting
- GitHub Actions CI/CD pipeline
- Comprehensive development dependencies

### Documentation
- Complete API reference documentation
- Installation and setup guides
- Usage examples for all endpoints
- Error handling patterns
- Best practices documentation
- Contributing guidelines

### Security
- Secure API key handling with environment variables
- Input validation and sanitization
- HTTPS-only API communication

## Version History

### Breaking Changes

#### v1.0.0
- Initial stable release
- Established public API interface
- All future changes will follow semantic versioning

### Migration Guides

#### From Pre-1.0 Versions
This is the first stable release. If you were using development versions:

1. Update your installation: `pip install --upgrade wfrmls`
2. Review the [API Reference](api-reference.md) for any method signature changes
3. Update import statements if needed:
   ```python
   # New stable imports
   from wfrmls import WFRMLSClient
   from wfrmls.exceptions import WFRMLSError, AuthenticationError
   ```

### Deprecation Notices

No current deprecations. Future deprecations will be announced here with migration timelines.

### Known Issues

- None currently identified

### Planned Features

#### v1.1.0 (Next Minor Release)
- Async/await support for improved performance
- Bulk operation helpers
- Caching mechanisms for frequently accessed data
- Enhanced filtering capabilities

#### v1.2.0 (Future Release)
- Webhook support for real-time updates
- Advanced analytics and reporting features
- Integration with common real estate platforms

### Support Matrix

| Version | Python Support | Status | Security Fixes | Bug Fixes |
|---------|----------------|--------|----------------|-----------|
| 1.0.x   | 3.8+          | Active | ✅ Yes         | ✅ Yes    |

### Release Process

1. **Pre-release Testing**
   - All tests must pass
   - Code coverage must remain at 100%
   - Documentation must be updated
   - Version numbers must be consistent

2. **Version Bumping**
   - Update `pyproject.toml` version
   - Update `wfrmls/__init__.py` `__version__`
   - Update this changelog

3. **Release Validation**
   - Tag release in Git
   - Build and test package
   - Publish to PyPI
   - Update documentation sites

### Contributing to Changelog

When making changes:

1. **Add entries to [Unreleased]** section
2. **Use categories**: Added, Changed, Deprecated, Removed, Fixed, Security
3. **Be specific**: Include method names, parameter changes, etc.
4. **Include migration notes** for breaking changes
5. **Reference issues/PRs** where applicable

Example entry format:
```markdown
### Added
- `PropertiesClient.search_properties()` now supports `sort_order` parameter (#123)
- New `ValidationError` exception for parameter validation failures
- Support for batch property updates via `PropertiesClient.update_properties_batch()`

### Changed
- **BREAKING**: `MemberClient.search_members()` parameter `name` renamed to `full_name` (#456)
- Improved error messages for authentication failures
- Updated minimum Python version to 3.9 (security reasons)

### Fixed
- Fixed pagination bug in `OfficeClient.search_offices()` when `page_size > 100` (#789)
- Corrected type hints for optional parameters in analytics methods
```

### Release Notes Template

For maintainers creating release notes:

```markdown
## [X.Y.Z] - YYYY-MM-DD

Brief description of the release focus.

### 🚀 New Features
- Major new functionality

### 🔧 Improvements  
- Enhancements and optimizations

### 🐛 Bug Fixes
- Important fixes

### ⚠️ Breaking Changes
- Changes requiring user action

### 🔒 Security
- Security-related updates

### 📚 Documentation
- Documentation improvements

**Full Changelog**: https://github.com/theperrygroup/wfrmls/compare/vX.Y.Z-1...vX.Y.Z
``` 