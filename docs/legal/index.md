# Legal Information

Legal documentation, licensing, and terms of service for the WFRMLS Python client.

---

## 📋 Legal Documents

<div class="grid cards" markdown>

-   :material-file-document:{ .lg .middle } **License**

    ---

    MIT License terms and conditions for using this software

    [:octicons-arrow-right-24: View License](license.md)

-   :material-gavel:{ .lg .middle } **Terms of Service**

    ---

    Terms and conditions for using the WFRMLS API and this client

    [:octicons-arrow-right-24: Terms of Service](terms.md)

</div>

---

## 📄 License Summary

### MIT License

The WFRMLS Python client is released under the **MIT License**, which means:

✅ **You Can:**
- Use the software for any purpose (commercial or personal)
- Modify and distribute the software
- Include the software in other projects
- Sell software that includes this library

⚠️ **You Must:**
- Include the original license and copyright notice
- Give credit to the original authors

❌ **We Are Not Liable:**
- For any damages caused by using this software
- For providing warranties or guarantees about the software

### Full License Text

```
MIT License

Copyright (c) 2024 WFRMLS API Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🔐 API Usage Terms

### WFRMLS API Terms

**Important**: This Python client is a wrapper for the WFRMLS API. Your use of this client is subject to:

1. **WFRMLS API Terms of Service** - Available at [vendor.utahrealestate.com](https://vendor.utahrealestate.com)
2. **Your API License Agreement** - Signed when you obtained API access
3. **RESO Data Standards** - Industry standards for real estate data usage

### Key API Restrictions

!!! warning "Important Limitations"
    - **Commercial Use**: Requires appropriate licensing from WFRMLS
    - **Data Redistribution**: Subject to strict licensing terms
    - **Rate Limits**: Must respect API quotas and limits
    - **Data Accuracy**: Use data "as-is" without warranties
    - **Attribution**: May require attribution to WFRMLS/Utah Real Estate

### Compliance Requirements

```python
# Example: Proper attribution in your application
attribution = (
    "Data provided by Wasatch Front Regional MLS (WFRMLS). "
    "Information deemed reliable but not guaranteed."
)

# Display attribution with property data
def display_property(property_data):
    print(f"Property: {property_data['Address']}")
    print(f"Price: ${property_data['ListPrice']:,}")
    print(f"\n{attribution}")
```

---

## ⚖️ Liability and Warranties

### No Warranties

This software is provided **"AS IS"** without any warranties:

- **No guarantee** of accuracy, completeness, or reliability
- **No warranty** that the software will meet your requirements
- **No warranty** that the software will be error-free or uninterrupted

### Limitation of Liability

The authors and contributors are not liable for:

- Direct, indirect, incidental, or consequential damages
- Loss of profits, data, or business opportunities
- Any claims arising from use of this software
- Issues with the underlying WFRMLS API service

### Your Responsibilities

When using this client, you are responsible for:

- **Compliance** with all applicable laws and regulations
- **Proper licensing** for your use case
- **Data security** and privacy protection
- **Error handling** and data validation
- **Respecting rate limits** and API terms

---

## 🛡️ Data Privacy and Security

### Data Handling

The WFRMLS Python client:

- **Does not store** your API credentials (except in memory during requests)
- **Does not log** sensitive information by default
- **Does not transmit** data to third parties
- **Uses HTTPS** for all API communications

### Your Privacy Obligations

When building applications with this client:

- **Protect user data** according to applicable privacy laws
- **Secure API credentials** - never expose them publicly
- **Handle personal information** (agent contacts, etc.) appropriately
- **Implement proper access controls** for sensitive data

### Security Best Practices

```python
import os
import logging

# ✅ Good: Secure credential management
def create_client():
    token = os.getenv('WFRMLS_BEARER_TOKEN')
    if not token:
        raise ValueError("API token required")
    return WFRMLSClient(bearer_token=token)

# ✅ Good: Avoid logging sensitive data
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_log_property(prop):
    logger.info(f"Processing property {prop.get('ListingId', 'unknown')}")
    # Don't log full property details that might contain sensitive info

# ❌ Bad: Never do this
# token = "9d0243d7632d115b002acf3547d2d7ee"  # Hardcoded token
# logger.info(f"Using token: {token}")        # Logging credentials
```

---

## 📞 Legal Contacts

### For Client Library Issues

- **GitHub Issues**: [Report bugs or legal concerns](https://github.com/theperrygroup/wfrmls/issues)
- **Email**: Contact maintainers through GitHub

### For API Licensing and Terms

- **WFRMLS Support**: [vendor.utahrealestate.com](https://vendor.utahrealestate.com)
- **Legal Department**: Contact through vendor dashboard
- **Licensing Questions**: Use vendor support channels

### For DMCA or Copyright Issues

If you believe this software infringes on your copyright:

1. **Contact us** through GitHub issues first
2. **Provide details** about the alleged infringement
3. **Include contact information** for follow-up
4. **Follow DMCA procedures** if necessary

---

## 📚 Related Legal Resources

### Industry Standards

- **[RESO Standards](../reference/reso-standards.md)** - Real Estate Standards Organization guidelines
- **[MLS Rules](https://vendor.utahrealestate.com)** - Local MLS regulations and requirements

### Developer Resources

- **[Contributing Guidelines](../development/contributing.md)** - How to contribute legally
- **[Code of Conduct](https://github.com/theperrygroup/wfrmls/blob/main/CODE_OF_CONDUCT.md)** - Community standards

### External Links

- **[MIT License](https://opensource.org/licenses/MIT)** - Full license text and explanation
- **[Python Software Foundation](https://www.python.org/psf/)** - Python language licensing
- **[GitHub Terms of Service](https://docs.github.com/en/github/site-policy/github-terms-of-service)** - Repository hosting terms

---

## ⚠️ Important Disclaimers

### Real Estate Data

- **Accuracy**: Real estate data changes frequently and may contain errors
- **Timeliness**: Information may not reflect the most current status
- **Completeness**: Some properties or fields may be incomplete
- **Legal Effect**: This data should not be relied upon for legal or financial decisions

### Software Limitations

- **Beta Software**: Some features may be experimental or subject to change
- **Third-Party Dependencies**: Relies on external services and libraries
- **Maintenance**: No guarantee of ongoing maintenance or support
- **Compatibility**: May not work with all Python versions or environments

### Professional Advice

For legal questions about:

- **Real estate licensing** - Consult a real estate attorney
- **Data usage rights** - Contact WFRMLS legal department
- **Software licensing** - Consult an intellectual property attorney
- **Privacy compliance** - Consult a privacy law specialist

---

## 📋 Legal Checklist

Before using this software in production:

- [ ] **Read and understand** the MIT License terms
- [ ] **Review WFRMLS API terms** and your license agreement
- [ ] **Ensure compliance** with applicable laws and regulations
- [ ] **Implement proper security** measures for credentials and data
- [ ] **Add appropriate attribution** to your application
- [ ] **Set up error handling** and monitoring
- [ ] **Consider legal review** for commercial applications

---

*This legal information is provided for convenience and is not legal advice. Consult with qualified legal counsel for specific legal questions.* 