---
name: github-pr-merge-worthiness
description: Audit open GitHub pull requests for theperrygroup/wfrmls, decide whether they are worth merging, start fixing clear blockers for worthwhile PRs, safely merge PRs that pass repo gates, and close PRs that are unsafe or not recommended. Use when the user asks to review open PRs, decide whether PRs should be merged, merge worthwhile PRs, close bad PRs, clean up the PR queue, or inspect https://github.com/theperrygroup/wfrmls/pulls.
---

# GitHub PR Merge Worthiness

## Use This Skill

Use this as the default repo-local workflow when the user wants open pull
requests reviewed for merge-worthiness. The default outcome is active queue
management: merge PRs that are clearly worth merging, close PRs that are
clearly unsafe or not recommended, and automatically start fixing clear blockers
for worthwhile PRs instead of returning only a status report.

This skill is write-capable when the user asked for PR queue cleanup or
merge-worthiness action. Merging and closing still require concrete evidence
from GitHub metadata, CI, code diff, and this repository's rules.

Repository:

- owner/repo: `theperrygroup/wfrmls`
- PR list: `https://github.com/theperrygroup/wfrmls/pulls`
- primary merge base: `main`
- package: `wfrmls`
- Python support: 3.8 through 3.12

## Read First

Before acting, read these repo-local rules and project files:

- `STYLE_GUIDE.md`
- `.cursor/rules/styleguide.mdc`
- `.cursor/rules/release-process.mdc`
- `.cursor/rules/endpointtasks.mdc`
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/release.yml`

When a PR changes library behavior, endpoints, or public docs, also inspect the
affected files in `wfrmls/`, `tests/`, `docs/`, `api_docs/`, and `mkdocs.yml`.
Do not hard-code API tokens or other secrets. Use `WFRMLS_BEARER_TOKEN` from the
environment for live API verification when integration testing is necessary.

## Start With A Queue Snapshot

Fetch open PRs and enough metadata to classify them:

```bash
gh pr list --repo theperrygroup/wfrmls --state open --limit 100 --json number,title,author,isDraft,baseRefName,headRefName,headRepositoryOwner,headRepository,mergeStateStatus,reviewDecision,updatedAt,url
```

For each candidate PR, inspect details before deciding:

```bash
gh pr view <number> --repo theperrygroup/wfrmls --json number,title,body,author,isDraft,baseRefName,headRefName,headRepositoryOwner,headRepository,headRefOid,mergeStateStatus,mergeable,reviewDecision,commits,files,additions,deletions,changedFiles,labels,assignees,reviewRequests,statusCheckRollup,latestReviews,closingIssuesReferences,url
gh pr diff <number> --repo theperrygroup/wfrmls
gh pr checks <number> --repo theperrygroup/wfrmls --watch=false
```

For multiple PRs, rank first by likely package value and merge readiness:

- small, focused, repo-owned fixes with green CI
- bug fixes, security fixes, endpoint fixes, docs fixes, release blockers, or CI fixes
- endpoint implementations that include docs, tests, exports, and task updates
- public API changes with clear tests, docs, and version handling
- stale, broad, duplicative, failing, or unclear PRs later

## Auto-Work Before Reporting

Do not stop after classifying a valuable PR as blocked when the next safe
engineering action is clear. Start working on the highest-confidence blocker,
then continue the merge-worthiness workflow after verification.

Automatically proceed when the blocker is one of these repo-local issues:

- CI fails on a small stale assertion, fixture drift, import error, lint failure,
  formatting issue, type hint issue, docstring issue, or missing docs artifact.
- The PR branch is only behind `main` and GitHub can update it safely.
- A library change forgot to update matching docs, examples, or `mkdocs.yml` nav.
- A version bump is required and only `pyproject.toml` or `wfrmls/__init__.py`
  needs to be synchronized.
- Several open PRs share the same inherited failure; fix the shared blocker once
  on `main` or the most appropriate repo-owned branch, then re-check the queue.

Pick the work target conservatively:

- Prefer fixing inherited/shared failures on `main` when multiple PRs are blocked
  by the same `main` failure.
- Prefer checking out and fixing the PR branch when the failure is introduced by
  that PR's diff and the head branch is in `theperrygroup/wfrmls`.
- Do not push to fork branches unless the user explicitly asked for a fork branch
  update and permissions allow it.
- Treat PR branch checkouts as temporary. Before checking out a PR branch, note
  the current branch, and before handoff switch back to local `main`.
- Do not commit unless the user explicitly asked for a commit.

Only return a blocker-only report when the next action is unsafe, destructive,
requires missing permissions, depends on a product/API decision, or needs author
context that is not present in the PR.

## Merge-Worthiness Criteria

A PR is worth merging only when all required gates pass:

- It targets `main` unless the user explicitly asked for a different base.
- It is not a draft.
- It is mergeable or can be made mergeable by safely updating from base.
- Required checks are passing after any base refresh.
- Review state is acceptable: approved or no required review outstanding, no
  unresolved requested changes, and no unresolved review threads that block
  correctness.
- The diff is understandable and has a clear purpose.
- Public code has thorough type hints and Google-style docstrings.
- Tests match the changed behavior and avoid live API calls unless marked or
  clearly intended as integration coverage.
- Endpoint changes update `wfrmls/`, `tests/`, `docs/`, exports, and task status
  when applicable.
- User-facing docs and examples match the changed behavior.
- Library changes keep `pyproject.toml` and `wfrmls/__init__.py` versions in sync.
- It does not include secrets, credential material, `.env`, cache files, build
  artifacts, coverage output, or local-only files.
- It does not weaken CI, coverage, formatting, type checking, docs build,
  packaging, release, or PyPI publication guardrails.
- It does not remove or mask WFRMLS API failures without clear docs and tests.

## Local Verification

Run focused commands first, then broaden to repo gates before merging. Use the
commands that match the changed surface:

```bash
python -m pytest tests/<focused_test_file>.py -x -v
python -m pytest tests/ --ignore=tests/test_integration.py --cov=wfrmls --cov-report=term-missing --tb=short -x -v
black --check --diff wfrmls/ tests/
isort --check-only --diff wfrmls/ tests/
flake8 wfrmls/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 wfrmls/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
mypy wfrmls/ --ignore-missing-imports --show-error-codes
mkdocs build --clean
python -m build
twine check dist/*
```

Run `tests/test_integration.py` only when the PR needs live API verification and
`WFRMLS_BEARER_TOKEN` is available. Do not paste token values into comments,
logs, code, or skill output.

## Safe Merge Path

For PRs that pass the criteria:

1. Confirm merge state and check status immediately before merging:

```bash
gh pr view <number> --repo theperrygroup/wfrmls --json headRefOid,mergeStateStatus,mergeable,reviewDecision,statusCheckRollup
gh pr checks <number> --repo theperrygroup/wfrmls --watch=false
```

2. If the PR is only blocked because the branch is behind `main`, update it:

```bash
gh pr update-branch <number> --repo theperrygroup/wfrmls
```

After updating, poll CI in short intervals until checks pass or a real blocker
appears.

3. Determine the merge method from repo settings and recent merged PRs. Prefer
the repository's established method. If only one method is enabled, use that.
Do not use force pushes or bypass required checks.

```bash
gh repo view theperrygroup/wfrmls --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed,deleteBranchOnMerge
gh pr list --repo theperrygroup/wfrmls --state merged --limit 10 --json number,title,mergedAt,mergeCommit
```

4. Merge non-interactively with the chosen method, deleting the branch when the
repo allows it:

```bash
gh pr merge <number> --repo theperrygroup/wfrmls --merge --delete-branch
```

Use `--squash` or `--rebase` instead of `--merge` only when that is the
established or only enabled repo method.

5. For library changes that require release follow-through, confirm the release
process is complete before saying the release is complete: docs updated, tests
run, version bumped, commit created, matching `v*` tag pushed, release workflow
passed, and PyPI publication verified.

## Close Path

Close PRs that are unsafe or not recommended when there is concrete evidence,
not just uncertainty. Add a concise comment explaining the reason.

Close a PR when one or more of these are true:

- It is spam, malicious, includes secrets, or introduces obvious security risk.
- It targets the wrong base or stale architecture and is not salvageable.
- It duplicates already-landed work.
- It is abandoned and failing, with no clear small repair path.
- It removes required guardrails such as CI checks, docs builds, release
  workflow, version consistency, type checking, or coverage.
- It introduces broad API semantics or endpoint behavior the user has not
  approved.
- It has unresolved requested changes or failing checks that indicate the design
  should not land, not merely that a small fix is needed.
- The diff is dominated by generated, cache, local, vendored, or unrelated churn.

Close with:

```bash
gh pr close <number> --repo theperrygroup/wfrmls --comment "$(cat <<'EOF'
Closing this because it is not recommended to merge in its current form.

Reason:
- <specific evidence from CI/reviews/diff/repo rules>

This can be reopened or replaced if the underlying issue is addressed in a focused PR.
EOF
)"
```

Do not close when the evidence only says "needs a small fix." In that case,
either fix the PR locally if it is repo-owned and safe, or classify it as blocked
with the exact fix needed.

## Fix-Locally Path

If a PR is valuable but blocked by a clear repo-local issue:

- Fetch the PR branch only after confirming the branch source and that the work
  is safe to inspect.
- If the same failure is already present on `main`, fix the inherited failure on
  `main` first rather than patching every PR branch.
- Work without overwriting unrelated local changes.
- Run focused tests and formatting/lint/type checks for any code edit.
- Push only when the PR branch is in this repository or the user explicitly asked
  for a fork branch update and permissions allow it.
- Do not leave the local checkout on the PR branch. Return to `main` before final
  handoff unless a concrete blocker prevents it.

Useful commands:

```bash
git branch --show-current
gh pr checkout <number> --repo theperrygroup/wfrmls
PR_BRANCH="$(git branch --show-current)"
git status -sb
git switch main
git merge --ff-only "$PR_BRANCH"
```

If fast-forward is impossible, run a normal merge on `main` only when the
conflict surface is small and safe to resolve. Otherwise stop with the exact
merge blocker and leave the checkout on `main`.

## Escalate Instead Of Acting

Stop before merge or close only for concrete blockers:

- missing GitHub permissions
- merge method cannot be determined and multiple methods are enabled
- required product, endpoint, data semantics, or release decision
- destructive or irreversible data action
- evidence conflict between CI, reviews, and local diff
- the PR appears valuable but needs author context not present in the PR

When stopping, provide the exact PR number, blocker, evidence gathered, and the
specific action that would make the next step safe.

## Final Report

Return a compact queue summary:

- merged PRs with numbers, titles, URLs, merge methods, and merge SHAs
- closed PRs with numbers, titles, URLs, and specific close reasons
- PRs left open with exact blockers or next actions
- CI or review evidence used for each decision
- commands run and any commands that were blocked by permissions
