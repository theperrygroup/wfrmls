# Authentication

Learn how to authenticate with the WFRMLS API using bearer tokens and configure secure access for your applications.

## 🔑 Authentication Overview

The WFRMLS API uses **Bearer Token Authentication** for secure access. You'll need a valid bearer token to make any API requests.

!!! info "Getting API Access"
    To obtain WFRMLS API credentials, contact the Wasatch Front Regional Multiple Listing Service directly. This wrapper is designed for developers who already have authorized access to the WFRMLS API.

## Bearer Token Setup

### Method 1: Environment Variable (Recommended)

The most secure way to handle your API token is using environment variables:

=== "Linux/macOS"
    ```bash
    # Set in your shell profile (~/.bashrc, ~/.zshrc, etc.)
    export WFRMLS_BEARER_TOKEN="9d0243d7632d115b002acf3547d2d7ee"
    
    # Or set for current session
    export WFRMLS_BEARER_TOKEN="your_actual_token_here"
    ```

=== "Windows"
    ```cmd
    # Command Prompt
    set WFRMLS_BEARER_TOKEN=your_actual_token_here
    
    # PowerShell
    $env:WFRMLS_BEARER_TOKEN="your_actual_token_here"
    ```

=== "Python (.env file)"
    ```python
    # Create a .env file in your project root
    # .env
    WFRMLS_BEARER_TOKEN=your_actual_token_here
    
    # Load in your Python code
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    ```

Then initialize the client without explicitly passing the token:

```python
from wfrmls import WFRMLSClient

# Automatically loads from WFRMLS_BEARER_TOKEN environment variable
client = WFRMLSClient()
```

### Method 2: Direct Token (Development Only)

For development and testing, you can pass the token directly:

```python
from wfrmls import WFRMLSClient

# Pass token directly (not recommended for production)
client = WFRMLSClient(bearer_token="your_actual_token_here")
```

!!! warning "Security Warning"
    Never hardcode API tokens in your source code, especially in production environments or public repositories.

## Token Management Best Practices

### 🔒 Security Guidelines

1. **Never Commit Tokens**: Add `.env` files to your `.gitignore`
2. **Use Environment Variables**: Keep tokens out of source code
3. **Rotate Regularly**: Update tokens periodically if possible
4. **Limit Scope**: Use tokens with minimal required permissions
5. **Monitor Usage**: Track API usage for unusual activity

### 📁 Project Structure for Token Security

```
your-project/
├── .env                    # Environment variables (add to .gitignore)
├── .gitignore             # Exclude .env from version control
├── config.py              # Configuration management
├── main.py                # Your application
└── requirements.txt       # Dependencies
```

**`.gitignore` example:**
```gitignore
# Environment variables
.env
.env.local
.env.production

# API keys and secrets
*.key
config/secrets.json
```

### 🛠️ Configuration Management

Create a configuration module for better token management:

```python
# config.py
import os
from typing import Optional

class Config:
    """Application configuration."""
    
    def __init__(self):
        self.wfrmls_token = self._get_wfrmls_token()
        self.base_url = os.getenv('WFRMLS_BASE_URL', 'https://api.wfrmls.com/RETS/api')
    
    def _get_wfrmls_token(self) -> str:
        """Get WFRMLS bearer token from environment."""
        token = os.getenv('WFRMLS_BEARER_TOKEN')
        if not token:
            raise ValueError(
                "WFRMLS bearer token not found. "
                "Set the WFRMLS_BEARER_TOKEN environment variable."
            )
        return token
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return os.getenv('ENVIRONMENT', 'development').lower() == 'production'

# Usage in your application
config = Config()
client = WFRMLSClient(bearer_token=config.wfrmls_token)
```

## Testing Authentication

### Verify Your Setup

Test your authentication setup with a simple connection test:

```python
from wfrmls import WFRMLSClient
from wfrmls.exceptions import AuthenticationError, WFRMLSError

def test_authentication():
    """Test WFRMLS API authentication."""
    try:
        # Initialize client
        client = WFRMLSClient()
        
        # Test with a simple API call
        service_doc = client.get_service_document()
        
        print("✅ Authentication successful!")
        print(f"📋 Found {len(service_doc.get('value', []))} available resources")
        
        # List available resources
        for resource in service_doc.get('value', [])[:5]:
            print(f"   • {resource.get('name', 'Unknown')}")
        
        return True
        
    except AuthenticationError:
        print("❌ Authentication failed!")
        print("🔧 Check your bearer token and try again")
        return False
        
    except WFRMLSError as e:
        print(f"🚨 API error: {e}")
        return False
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

# Run the test
if __name__ == "__main__":
    test_authentication()
```

### Common Authentication Issues

=== "Token Not Found"
    ```
    ValueError: WFRMLS bearer token not found
    ```
    
    **Solutions:**
    - Set the `WFRMLS_BEARER_TOKEN` environment variable
    - Check spelling of environment variable name
    - Ensure your shell has loaded the variable (`echo $WFRMLS_BEARER_TOKEN`)

=== "Invalid Token"
    ```
    AuthenticationError: Invalid credentials
    ```
    
    **Solutions:**
    - Verify your token is correct and not expired
    - Contact WFRMLS to confirm your API access
    - Check for extra spaces or characters in the token

=== "Access Denied"
    ```
    AuthenticationError: Access denied
    ```
    
    **Solutions:**
    - Ensure your account has API access permissions
    - Check if your IP address is allowlisted
    - Verify your MLS membership status

## Advanced Authentication

### Multiple Environments

Manage different tokens for different environments:

```python
import os

class EnvironmentConfig:
    """Multi-environment configuration."""
    
    def __init__(self):
        self.env = os.getenv('ENVIRONMENT', 'development')
        self.token = self._get_token_for_environment()
    
    def _get_token_for_environment(self) -> str:
        """Get appropriate token based on environment."""
        if self.env == 'production':
            return os.getenv('WFRMLS_PRODUCTION_TOKEN')
        elif self.env == 'staging':
            return os.getenv('WFRMLS_STAGING_TOKEN')
        else:
            return os.getenv('WFRMLS_DEVELOPMENT_TOKEN')

# Usage
config = EnvironmentConfig()
client = WFRMLSClient(bearer_token=config.token)
```

### Token Validation

Add token validation to catch issues early:

```python
def validate_token_format(token: str) -> bool:
    """Validate bearer token format."""
    if not token:
        return False
    
    # Basic validation (adjust based on actual WFRMLS token format)
    if len(token) < 32:  # Minimum expected length
        return False
    
    # Check for common issues
    if token.startswith(' ') or token.endswith(' '):
        print("⚠️ Token has leading/trailing spaces")
        return False
    
    return True

# Usage
token = os.getenv('WFRMLS_BEARER_TOKEN')
if not validate_token_format(token):
    raise ValueError("Invalid token format")
    
client = WFRMLSClient(bearer_token=token)
```

## Next Steps

Once authentication is working:

1. **[Quick Start](quickstart.md)** - Make your first API calls
2. **[First Steps](first-steps.md)** - Learn core concepts
3. **[API Reference](../api/)** - Explore available endpoints
4. **[Examples](../examples/)** - See practical usage patterns

---

*Having authentication issues? Check our [Troubleshooting Guide](../guides/troubleshooting.md) or [open an issue](https://github.com/theperrygroup/wfrmls/issues) for help.* 