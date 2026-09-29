# MX-s-14 allocation leg -- never-widen re-ask, DELTA=0 for served gold (2.0.0_SA_COO~MI, 2026-09-29 ~08:5xZ)

This is the leg `1.0.0_SA_CTO~O` carved out (`deliverables/1.0.0_SA_CTO~O/NEVER_WIDEN_CTO_HALF_MX-s-14_20260929.md`
@aac61a1046), re-cut per its ruling. The parent ask is `NEVER_WIDEN_ASK_MX-s-14_20260929.md`, and this ask adds only
what differs from it.

**Asked:** the CTO half from `1.0.0_SA_CTO~O`, and the second half from `3.0.0_SA_CVO~O`.

## The act

Publish `infra/aws/ssm/opal-bd-allocation-download.json` from CLOUD @9feccbe36f (content sha256 first-16
`66431932a7ad0f55`, worker commit a1a912c90a) as the next version, which is v5. Then set DEFAULT to v5; today
Default is 3 and Latest is 4. Read it back: the hash equals the repo file, and Default == Latest. The act joins ledger
`nfra-mcpindex-bd-playwright-strip` as its own leg.

## What it changes, against served v4

- **Removed:** the Playwright download step, the `opal/bd/credentials` read and the `scripts/src` sync. The daily
  failed portal login stops.
- **Removed, and so DELTA=0:** the `bd-price-update` invoke block.
  - In served v4 the invoke runs only when the download succeeded, and the download has failed on every run since
    2026-06-22. The invoke has been unreachable since then.
  - In v5 it is absent, and one log line says it is not invoked.
  - Offline counts: `lambda invoke` 0, `aws lambda` 0, and `bd-price-update` once, in that log line only.
  - None of the 4 `opal-data-bd` keys the Lambda writes is written, and no gold trigger is added. Served gold is
    exactly as it has been since 2026-06-22.
- **Kept:** the merge block, 7 of 8 lines identical to v4. The eighth is a comment (a mojibake dash becomes an ASCII
  hyphen).
- **Changed, the same subtractions as the 3 signed legs:** the exit status follows the merge's rc, and the shutdown is
  armed on both arms.
- **Writers of the document content:** N = 1, the manual `update-document`.

## Expected outcome, both branches

- **Merge succeeds:** exit 0, the log is uploaded, the shutdown fires, and silver/allocations gains the day's
  partition where bronze has a new file. Baseline: 131 processed, and PHASE A test `84e569c5` read no new file.
- **Merge fails:** exit non-zero with the shutdown armed. Roll back only if the edit caused the failure.

## Rollback

Re-publish the v4 content (`aws ssm get-document --name opal-bd-allocation-download --document-version 4`) as the next
version and set DEFAULT to it. That restores the dead-download document, whose invoke stays unreachable. Revert the
repo copy in the same window.

## Acceptance and guards

- **Acceptance:** the next scheduled weekday 22:00Z fire reads Success on the new version.
- **GO guards:**
  - both halves are SIGNED as files;
  - the publish lands outside 21:30-22:15Z;
  - `.open_deploys/` is read across every live worktree, with the denominator printed. The only entry naming this
    document is its own ledger.
