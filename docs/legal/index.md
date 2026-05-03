# Legal

Legal information for this project, including the repository license and pointers to the external terms that govern WFRMLS API access.

---

## Quick Navigation

<div class="grid cards" markdown>

-   :material-file-document:{ .lg .middle } **Project License**

    ---

    Review the MIT license used by this repository.

    [:octicons-arrow-right-24: Project License](license.md)

-   :material-gavel:{ .lg .middle } **WFRMLS API Terms**

    ---

    Review vendor-managed terms and licensing requirements.

    [:octicons-arrow-right-24: WFRMLS Vendor Portal](https://vendor.utahrealestate.com)

</div>

---

## What This Section Covers

This documentation separates two things that are easy to conflate:

- The **project license** for the Python package in this repository.
- The **API access terms** and licensing obligations that come from WFRMLS and the UtahRealEstate vendor platform.

---

## Project License

This repository is distributed under the **MIT License**. The full text is available on the **[License](license.md)** page and in the repository root `LICENSE` file.

---

## WFRMLS API Terms

Use of the underlying MLS data and API is governed by WFRMLS and vendor-issued agreements, not by this repository alone.

Before using the client in production, review:

- Your WFRMLS or UtahRealEstate vendor agreement.
- Any data-display, attribution, and redistribution requirements tied to your account.
- Operational limits such as authentication, rate limits, and permitted downstream use.

See the **[WFRMLS vendor portal](https://vendor.utahrealestate.com)** for the current source of truth.

---

## Practical Reminders

- Do not hardcode bearer tokens in source control.
- Validate your application's data-display requirements with your vendor agreement.
- Treat this page as documentation guidance, not legal advice.

---

## Related Documentation

- **[Reference Guide](../reference/index.md)** - Shared data and response conventions.
- **[Development Guide](../development/index.md)** - Local workflow and documentation expectations.
- **[Authentication Guide](../getting-started/authentication.md)** - Credential setup for local use.
