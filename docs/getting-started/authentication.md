# Authentication

Configure your WFRMLS API credentials and authentication settings for secure access to real estate data.

---

## 🔑 Getting Your API Token

### Step 1: Register for API Access

1. **Visit the Vendor Dashboard**: Go to [vendor.utahrealestate.com](https://vendor.utahrealestate.com)
2. **Create an Account**: Register with your company information
3. **Request API Access**: Submit your application for API access
4. **Wait for Approval**: API access requires approval from the WFRMLS team

### Step 2: Generate Bearer Token

Once approved:

1. **Login to Dashboard**: Access your vendor dashboard
2. **Navigate to Service Details**: Find the API section
3. **Generate Token**: Create a new bearer token
4. **Copy and Secure**: Save your token securely (you won't see it again)

!!! warning "Token Security"
    Your bearer token provides full access to the WFRMLS API. Keep it secure and never commit it to version control.

---

## 🔧 Configuration Methods

### Method 1: Environment Variable (Recommended)

The most secure way to configure authentication:

=== ":material-linux: Linux/macOS"

    ```bash
    # Add to your shell profile (.bashrc, .zshrc, etc.)
    export WFRMLS_BEARER_TOKEN="9d0243d7632d115b002acf3547d2d7ee"
    
    # Or set for current session
    export WFRMLS_BEARER_TOKEN="9d0243d7632d115b002acf3547d2d7ee"
    
    # Verify it's set
    echo $WFRMLS_BEARER_TOKEN
    ```

=== ":material-microsoft-windows: Windows"

    ```cmd
    # Command Prompt
    set WFRMLS_BEARER_TOKEN=9d0243d7632d115b002acf3547d2d7ee
    
    # PowerShell
    $env:WFRMLS_BEARER_TOKEN="9d0243d7632d115b002acf3547d2d7ee"
    
    # Permanently (System Properties > Environment Variables)
    # Add WFRMLS_BEARER_TOKEN with your token value
    ```



### Method 2: .env File

Create a `.env` file in your project root:

```bash
# .env file
WFRMLS_BEARER_TOKEN=9d0243d7632d115b002acf3547d2d7ee
```

Load it in your Python code:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from wfrmls import WFRMLSClient

# Client will automatically use the environment variable
client = WFRMLSClient()
```

### Method 3: Direct Configuration

Pass the token directly (not recommended for production):

```python
from wfrmls import WFRMLSClient

# Initialize with explicit token
client = WFRMLSClient(bearer_token="9d0243d7632d115b002acf3547d2d7ee")
```

---

## 🛡️ Security Best Practices

### Token Management

!!! danger "Never Do This"
    ```python
    # ❌ Don't hardcode tokens in source code
    client = WFRMLSClient(bearer_token="9d0243d7632d115b002acf3547d2d7ee")
    
    # ❌ Don't commit tokens to version control
    # ❌ Don't share tokens in chat or email
    # ❌ Don't log tokens in application logs
    ```

!!! success "Best Practices"
    ```python
    # ✅ Use environment variables
    client = WFRMLSClient()  # Reads from WFRMLS_BEARER_TOKEN
    
    # ✅ Use configuration management
    import os
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    if not token:
        raise ValueError("WFRMLS_BEARER_TOKEN environment variable required")
    
    client = WFRMLSClient(bearer_token=token)
    ```

### Production Security

```python
"""
Production-ready authentication setup
"""

import os
import logging
from wfrmls import WFRMLSClient
from wfrmls.exceptions import AuthenticationError

def create_authenticated_client():
    """Create a properly authenticated WFRMLS client."""
    
    # Get token from environment
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    
    if not token:
        raise ValueError(
            "WFRMLS_BEARER_TOKEN environment variable is required. "
            "Set it with: export WFRMLS_BEARER_TOKEN='your_token_here'"
        )
    
    # Validate token format (should be 32-character hex string)
    if len(token) != 32 or not all(c in '0123456789abcdef' for c in token):
        logging.warning("Bearer token format may be invalid")
    
    try:
        client = WFRMLSClient(bearer_token=token)
        
        # Test authentication with a minimal request
        client.property.get_properties(top=1)
        logging.info("WFRMLS client authenticated successfully")
        
        return client
        
    except AuthenticationError:
        logging.error("WFRMLS authentication failed - check your bearer token")
        raise
    except Exception as e:
        logging.error(f"Failed to create WFRMLS client: {e}")
        raise

# Usage
if __name__ == "__main__":
    client = create_authenticated_client()
```

---

## 🔍 Token Validation

### Test Your Authentication

```python
"""
Test script to validate your WFRMLS authentication
"""

import os
from wfrmls import WFRMLSClient
from wfrmls.exceptions import AuthenticationError, WFRMLSError

def test_authentication():
    """Test WFRMLS API authentication."""
    
    print("🔍 Testing WFRMLS Authentication...")
    
    # Check environment variable
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    if not token:
        print("❌ WFRMLS_BEARER_TOKEN environment variable not found")
        print("   Set it with: export WFRMLS_BEARER_TOKEN='your_token_here'")
        return False
    
    print(f"✅ Found token: {token[:8]}...{token[-8:]}")
    
    try:
        # Initialize client
        client = WFRMLSClient()
        print("✅ Client initialized")
        
        # Test API access with minimal request
        properties = client.property.get_properties(top=1)
        print(f"✅ API access confirmed - retrieved {len(properties)} property")
        
        # Test different endpoints
        try:
            members = client.member.get_members(top=1)
            print(f"✅ Members access - retrieved {len(members)} member")
        except Exception:
            print("⚠️  Members endpoint access limited")
        
        try:
            offices = client.office.get_offices(top=1)
            print(f"✅ Offices access - retrieved {len(offices)} office")
        except Exception:
            print("⚠️  Offices endpoint access limited")
        
        print("\n🎉 Authentication test successful!")
        return True
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Check your bearer token at: https://vendor.utahrealestate.com")
        return False
        
    except WFRMLSError as e:
        print(f"❌ API error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_authentication()
```

### Common Authentication Issues

??? question "Error: 'Invalid bearer token'"
    **Causes**:
    - Token is incorrect or expired
    - Token not properly set in environment
    - Token contains extra whitespace or characters
    
    **Solutions**:
    ```python
    # Verify token is set correctly
    import os
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    print(f"Token: '{token}'")  # Look for extra quotes or spaces
    
    # Clean the token
    token = token.strip() if token else None
    client = WFRMLSClient(bearer_token=token)
    ```

??? question "Error: 'WFRMLS_BEARER_TOKEN environment variable not found'"
    **Solutions**:
    ```bash
    # Check if variable is set
    echo $WFRMLS_BEARER_TOKEN
    
    # Set the variable
    export WFRMLS_BEARER_TOKEN="your_token_here"
    
    # Add to shell profile for persistence
    echo 'export WFRMLS_BEARER_TOKEN="your_token_here"' >> ~/.bashrc
    source ~/.bashrc
    ```

??? question "Error: 'Access denied' or '403 Forbidden'"
    **Causes**:
    - API access not approved yet
    - Token permissions insufficient
    - Account suspended or expired
    
    **Solutions**:
    - Contact [WFRMLS Support](https://vendor.utahrealestate.com)
    - Verify account status in vendor dashboard
    - Check if you need additional permissions

---

## 🔄 Token Rotation

### Best Practices for Token Management

```python
"""
Token rotation and management utilities
"""

import os
import json
from datetime import datetime, timedelta
from wfrmls import WFRMLSClient

class TokenManager:
    """Manage WFRMLS API token rotation and validation."""
    
    def __init__(self, token_file='.wfrmls_token'):
        self.token_file = token_file
    
    def save_token(self, token, expires_at=None):
        """Save token with optional expiration."""
        token_data = {
            'token': token,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat() if expires_at else None
        }
        
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
    
    def load_token(self):
        """Load saved token."""
        try:
            with open(self.token_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def is_token_valid(self, token_data):
        """Check if saved token is still valid."""
        if not token_data:
            return False
        
        # Check expiration
        if token_data.get('expires_at'):
            expires_at = datetime.fromisoformat(token_data['expires_at'])
            if datetime.now() >= expires_at:
                return False
        
        # Test token with API
        try:
            client = WFRMLSClient(bearer_token=token_data['token'])
            client.property.get_properties(top=1)
            return True
        except Exception:
            return False
    
    def get_valid_token(self):
        """Get a valid token, using cached if available."""
        # Try cached token first
        token_data = self.load_token()
        
        if self.is_token_valid(token_data):
            return token_data['token']
        
        # Fall back to environment variable
        env_token = os.getenv('WFRMLS_BEARER_TOKEN')
        if env_token:
            # Save environment token
            self.save_token(env_token)
            return env_token
        
        raise ValueError("No valid WFRMLS token available")

# Usage
token_manager = TokenManager()
token = token_manager.get_valid_token()
client = WFRMLSClient(bearer_token=token)
```

---

## 🚀 Advanced Configuration

### Custom Client Configuration

```python
from wfrmls import WFRMLSClient

# Custom timeout and retry settings
client = WFRMLSClient(
    bearer_token="your_token",
    timeout=30,  # Request timeout in seconds
    max_retries=3,  # Maximum retry attempts
    retry_delay=1.0  # Delay between retries
)
```

### Multiple Environment Configuration

```python
"""
Multi-environment token management
"""

import os
from wfrmls import WFRMLSClient

class MultiEnvClient:
    """WFRMLS client with multi-environment support."""
    
    def __init__(self, environment='production'):
        self.environment = environment
        self.client = self._create_client()
    
    def _create_client(self):
        """Create client for specific environment."""
        
        # Environment-specific token variables
        token_var = f'WFRMLS_BEARER_TOKEN_{self.environment.upper()}'
        token = os.getenv(token_var)
        
        if not token:
            # Fallback to default token
            token = os.getenv('WFRMLS_BEARER_TOKEN')
        
        if not token:
            raise ValueError(
                f"No token found for environment '{self.environment}'. "
                f"Set {token_var} or WFRMLS_BEARER_TOKEN environment variable."
            )
        
        return WFRMLSClient(bearer_token=token)
    
    def __getattr__(self, name):
        """Delegate all other attributes to the client."""
        return getattr(self.client, name)

# Usage
dev_client = MultiEnvClient('development')
prod_client = MultiEnvClient('production')

# Use like normal client
properties = prod_client.property.get_properties(top=10)
```

---

## 📚 Next Steps

!!! success "Authentication Configured"
    Great! Your authentication is set up. Here's what to do next:

### **Start Building**
- **[Quick Start Tutorial](quickstart.md)** - Make your first API calls
- **[Property Search Guide](../guides/property-search.md)** - Advanced property queries
- **[API Reference](../api/index.md)** - Complete method documentation

### **Security & Production**
- **[Error Handling Guide](../guides/error-handling.md)** - Robust error management
- **[Rate Limits Guide](../guides/rate-limits.md)** - Manage API quotas
- **[Development Best Practices](../development/index.md)** - Production guidelines

### **Get Help**
- **[Vendor Dashboard](https://vendor.utahrealestate.com)** - Manage your API access
- **[GitHub Issues](https://github.com/theperrygroup/wfrmls/issues)** - Technical support
- **[WFRMLS Support](https://vendor.utahrealestate.com/support)** - Account and access issues

---

*Ready to make your first API call? Head to the [Quick Start Guide](quickstart.md).* 