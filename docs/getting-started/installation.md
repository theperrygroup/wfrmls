# Installation

Install the WFRMLS Python client and set up your development environment for real estate data integration.

---

## 📦 Package Installation

### Using pip (Recommended)

```bash
# Install from PyPI
pip install wfrmls

# Verify installation
pip show wfrmls
```

### Using pip with version constraints

```bash
# Install specific version
pip install wfrmls==1.3.0

# Install with version range
pip install "wfrmls>=1.2.0,<2.0.0"
```

### Development Installation

For contributing to the project or using the latest features:

```bash
# Clone the repository
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

---

## 🐍 Python Version Requirements

!!! info "Python Compatibility"
    - **Minimum**: Python 3.8
    - **Recommended**: Python 3.10 or higher
    - **Tested**: Python 3.8, 3.9, 3.10, 3.11, 3.12

### Checking Your Python Version

```bash
# Check Python version
python --version
# or
python3 --version

# Check pip version
pip --version
```

---

## 🔧 Dependencies

The client has minimal dependencies for easy integration:

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **requests** | ≥2.25.0 | HTTP client for API requests |
| **python-dotenv** | ≥0.19.0 | Environment variable management |

### Development Dependencies

??? info "Development Tools (Optional)"
    These are only needed if you're contributing to the project:

    | Package | Purpose |
    |---------|---------|
    | **pytest** | Testing framework |
    | **pytest-cov** | Coverage reporting |
    | **black** | Code formatting |
    | **mypy** | Type checking |
    | **flake8** | Linting |

---

## 🚀 Environment Setup

### Virtual Environment (Recommended)

=== ":material-linux: Linux/macOS"

    ```bash
    # Create virtual environment
    python -m venv wfrmls-env
    
    # Activate virtual environment
    source wfrmls-env/bin/activate
    
    # Install the client
    pip install wfrmls
    
    # Deactivate when done
    deactivate
    ```

=== ":material-microsoft-windows: Windows"

    ```cmd
    # Create virtual environment
    python -m venv wfrmls-env
    
    # Activate virtual environment
    wfrmls-env\Scripts\activate
    
    # Install the client
    pip install wfrmls
    
    # Deactivate when done
    deactivate
    ```

=== ":material-language-python: conda"

    ```bash
    # Create conda environment
    conda create -n wfrmls-env python=3.10
    
    # Activate environment
    conda activate wfrmls-env
    
    # Install the client
    pip install wfrmls
    
    # Deactivate when done
    conda deactivate
    ```

### IDE Configuration

??? tip "VS Code Setup"
    Recommended VS Code extensions for working with the WFRMLS client:

    - **Python** - Python language support
    - **Pylance** - Advanced Python language server
    - **Python Docstring Generator** - Auto-generate docstrings
    - **autoDocstring** - Smart docstring generation

    Create `.vscode/settings.json`:
    ```json
    {
        "python.defaultInterpreterPath": "./wfrmls-env/bin/python",
        "python.formatting.provider": "black",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true
    }
    ```

---

## ✅ Verifying Installation

### Quick Test

```python
# Test import
try:
    from wfrmls import WFRMLSClient
    print("✅ WFRMLS client imported successfully!")
except ImportError as e:
    print(f"❌ Import failed: {e}")

# Check version
import wfrmls
print(f"📦 Version: {wfrmls.__version__}")
```

### Comprehensive Test

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError

def test_installation():
    """Test WFRMLS client installation and basic functionality."""
    try:
        # Test client creation (without token - should work)
        client = WFRMLSClient()
        print("✅ Client creation: Success")
        
        # Test available modules
        modules = [
            'property', 'member', 'office', 'openhouse',
            'lookup', 'adu', 'analytics', 'deleted'
        ]
        
        for module in modules:
            if hasattr(client, module):
                print(f"✅ Module {module}: Available")
            else:
                print(f"❌ Module {module}: Missing")
        
        print("\n🎉 Installation verification complete!")
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")

if __name__ == "__main__":
    test_installation()
```

---

## 🔍 Troubleshooting

### Common Installation Issues

??? question "Permission denied error"
    **Problem**: `ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied`
    
    **Solutions**:
    ```bash
    # Option 1: Use user installation
    pip install --user wfrmls
    
    # Option 2: Use virtual environment (recommended)
    python -m venv venv && source venv/bin/activate
    pip install wfrmls
    
    # Option 3: Use sudo (not recommended)
    sudo pip install wfrmls
    ```

??? question "SSL certificate error"
    **Problem**: `SSL: CERTIFICATE_VERIFY_FAILED`
    
    **Solutions**:
    ```bash
    # Option 1: Upgrade certificates
    pip install --upgrade certifi
    
    # Option 2: Trust PyPI (temporary fix)
    pip install --trusted-host pypi.org --trusted-host pypi.python.org wfrmls
    
    # Option 3: Update pip
    pip install --upgrade pip
    ```

??? question "Python version too old"
    **Problem**: `ERROR: Package 'wfrmls' requires a different Python: 3.7.0 not in '>=3.8'`
    
    **Solutions**:
    ```bash
    # Check available Python versions
    python3.8 --version
    python3.9 --version
    
    # Use specific Python version
    python3.8 -m pip install wfrmls
    
    # Or create environment with specific version
    conda create -n wfrmls python=3.10
    conda activate wfrmls
    pip install wfrmls
    ```

??? question "Module not found after installation"
    **Problem**: `ModuleNotFoundError: No module named 'wfrmls'`
    
    **Solutions**:
    ```bash
    # Check if installed in correct environment
    pip list | grep wfrmls
    
    # Verify Python path
    python -c "import sys; print('\n'.join(sys.path))"
    
    # Reinstall
    pip uninstall wfrmls
    pip install wfrmls
    
    # Check virtual environment activation
    which python
    which pip
    ```

### Network Issues

??? question "Connection timeout during installation"
    **Solutions**:
    ```bash
    # Increase timeout
    pip install --timeout 1000 wfrmls
    
    # Use different index
    pip install -i https://pypi.python.org/simple/ wfrmls
    
    # Download and install offline
    pip download wfrmls
    pip install wfrmls-*.whl
    ```

---

## 🔄 Updating

### Checking for Updates

```bash
# Check current version
pip show wfrmls

# Check for newer versions
pip list --outdated | grep wfrmls
```

### Upgrading

```bash
# Upgrade to latest version
pip install --upgrade wfrmls

# Upgrade with specific constraints
pip install --upgrade "wfrmls>=1.3.0"
```

---

## 🧹 Uninstalling

### Complete Removal

```bash
# Uninstall the package
pip uninstall wfrmls

# Remove virtual environment (if used)
rm -rf wfrmls-env

# Remove cached files (optional)
pip cache purge
```

---

## 📚 Next Steps

!!! success "Installation Complete"
    Great! You've successfully installed the WFRMLS client. Here's what to do next:

**Immediate Next Steps**:
1. **[Set up authentication](authentication.md)** - Configure your API credentials
2. **[Try the quick start](quickstart.md)** - Make your first API call
3. **[Explore examples](../examples/index.md)** - See real-world usage patterns

**For Developers**:
- **[Contributing Guide](../development/contributing.md)** - Set up development environment
- **[Testing Guide](../development/testing.md)** - Run tests and quality checks
- **[API Reference](../api/index.md)** - Detailed method documentation

---

*Having issues? Check our [troubleshooting guide](../guides/error-handling.md) or [open an issue](https://github.com/theperrygroup/wfrmls/issues) on GitHub.* 