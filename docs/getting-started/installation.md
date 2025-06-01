# Installation Guide

This guide will help you install and set up the WFRMLS Python API wrapper.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- WFRMLS API access token

## Installation Methods

### 1. Install from PyPI (Recommended)

```bash
pip install wfrmls
```

### 2. Install from Source

For the latest development version:

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
pip install -e .
```

### 3. Development Installation

For contributing to the project:

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
pip install -e ".[dev]"
```

This includes all development dependencies for testing, linting, and formatting.

## API Key Setup

### Option 1: Environment Variable (Recommended)

Set your API key as an environment variable:

**Linux/macOS:**
```bash
export WFRMLS_BEARER_TOKEN="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set WFRMLS_BEARER_TOKEN=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:WFRMLS_BEARER_TOKEN="your_api_key_here"
```

### Option 2: .env File

Create a `.env` file in your project root:

```bash
WFRMLS_BEARER_TOKEN=your_api_key_here
```

The client will automatically load this using python-dotenv.

### Option 3: Direct Parameter

Pass the API key directly when initializing the client:

```python
from wfrmls import WFRMLSClient

client = WFRMLSClient(api_key="your_api_key_here")
```

## Verification

Verify your installation by running:

```python
from wfrmls import WFRMLSClient

# Test basic initialization
client = WFRMLSClient()
print(f"WFRMLS Client initialized successfully")

# Test API access
try:
    resources = client.resource.get_resources()
    print("✅ API connection successful")
except Exception as e:
    print(f"❌ API connection failed: {e}")
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv wfrmls-env

# Activate it
# Linux/macOS:
source wfrmls-env/bin/activate
# Windows:
wfrmls-env\Scripts\activate

# Install WFRMLS
pip install wfrmls
```

## Requirements

### Runtime Dependencies
- `requests>=2.25.0` - HTTP client library
- `python-dotenv>=0.19.0` - Environment variable loading

### Development Dependencies (optional)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-mock>=3.10.0` - Mocking utilities
- `responses>=0.23.0` - HTTP response mocking
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking
- `isort>=5.12.0` - Import sorting
- `pylint>=2.17.0` - Additional linting
- `types-requests>=2.25.0` - Type stubs for requests

## Troubleshooting Installation

### Common Issues

**1. Permission Errors**
```bash
# Use --user flag
pip install --user wfrmls

# Or use virtual environment (recommended)
```

**2. SSL Certificate Issues**
```bash
# Upgrade pip and certificates
pip install --upgrade pip certifi
```

**3. Python Version Compatibility**
```bash
# Check Python version
python --version

# Ensure you're using Python 3.8+
```

**4. Network/Proxy Issues**
```bash
# Use proxy if needed
pip install --proxy http://proxy.company.com:port wfrmls
```

### API Key Issues

**Invalid API Key:**
- Verify your API key is correct
- Check that your account has API access enabled
- Ensure the environment variable name is exactly `WFRMLS_BEARER_TOKEN`

**Permission Denied:**
- Contact WFRMLS support to verify your API access level
- Check if your IP address is whitelisted (if required)

## Next Steps

Once installed, proceed to the [Quick Start Guide](quickstart.md) to begin using the WFRMLS API wrapper.

## Getting Help

If you encounter installation issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search existing [GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)
3. Create a new issue with:
   - Your Python version
   - Operating system
   - Complete error message
   - Installation method used 