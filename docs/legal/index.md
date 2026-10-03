---
title: "Software licensing and MLS data use"
description: "Distinguish the WFRMLS client MIT license from UtahRealEstate data agreements, IDX display rules, media permissions, and credential handling."
---

# Software licensing and MLS data use

The WFRMLS Python package and its documentation use the
[MIT License](license.md). That software license does not grant access to MLS
data, photographs, or vendor services. Your UtahRealEstate agreement and
applicable provider rules govern those uses.

## Review your data agreement

Confirm that your agreement permits the intended application, resource scope,
storage, retention, redistribution, and display. Use the
[UtahRealEstate vendor portal](https://vendor.utahrealestate.com) for your
account's access and service documentation.

For IDX uses, the provider's
[Rules and Regulations, effective February 27, 2026](https://help.utahrealestate.com/wp-content/uploads/2026/03/URE-Rules-and-Regulations-Effective-02-27-26.pdf)
include requirements for permitted fields and statuses, seller restrictions,
brokerage/source identification, consumer-use notices, and refresh frequency.
Apply the rules for your feed and intended use; an example query does not
establish display eligibility or compliance.

## Check media permissions

An accessible `MediaURL` does not establish rights to permanently retain,
redistribute, or modify an image. Check your agreement and any media permission
fields. RESO discusses media permissions in its
[data FAQ](https://www.reso.org/knowledge-base/data-topics-faq/).

The client's media expansion example is a retrieval pattern. It does not
authorize image downloading, public display, or reuse in marketing.

## Protect credentials and restricted data

Keep bearer tokens outside committed source and rotate them using the provider's
process. Avoid putting tokens, full response bodies, restricted remarks, or
personal data into logs and test fixtures. Access restrictions apply to local
caches and diagnostic exports as well as public pages.

Use the [authentication guide](../getting-started/authentication.md) for token
configuration and the [synchronization guide](../guides/data-sync.md) for
checkpoint and reconciliation boundaries. Follow your agreement when a record
is withdrawn or your access changes.

## Read the software license

The full [MIT license text](license.md) is copied from the repository's `LICENSE`
file. Preserve its notice when redistributing the software or substantial
portions of it. Data-use rights must be obtained separately from the provider.
