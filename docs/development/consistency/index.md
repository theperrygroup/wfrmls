---
title: "Repository consistency runbooks"
description: "Use WFRMLS consistency runbooks to review package metadata, documentation, GitHub Actions, dependency ownership, and evidence of completion."
---

# Repository consistency runbooks

These runbooks describe the shared review approach for The Perry Group's Python
clients (`vestaboard`, `rezen`, `flex_mls`, and `wfrmls`). The commands and
repository observations here are specific to `wfrmls`; they do not certify the
state of the other projects.

## Choose a review phase

1. [Shared standard](shared-standard.md): goals and rules for documented exceptions.
2. [Foundation](phase-1-foundation.md): metadata, versions, dependencies, and artifacts.
3. [Documentation](phase-2-docs.md): truthful examples, navigation, and local builds.
4. [GitHub Actions](phase-3-github-actions.md): actual gates, releases, security, and deployment.
5. [Repository gap map](repo-gap-map.md): implementation differences and review questions.

Read phases in that order when auditing the whole repository. A focused change
only needs the relevant phase and its dependencies. Use the
[development guide](../index.md) for environment setup and the exact local
quality commands; run them from the repository root.

## Record a reviewable result

Capture the inspected commit, affected files, checks actually run, and their
results. Distinguish a recommendation from an enforced gate and a successful
build from a published release or docs deployment.

A review closes when metadata and runtime versions agree, examples match the
implemented API, navigation resolves, required checks pass, and any remaining
exceptions have a concrete owner and rationale. Do not replace failed checks
with unverified completion claims.
