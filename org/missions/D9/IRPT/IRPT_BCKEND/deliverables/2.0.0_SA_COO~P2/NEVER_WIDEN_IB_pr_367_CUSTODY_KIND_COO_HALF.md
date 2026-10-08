# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-367: irpt-export-render packages repository.py (CUSTODY_REPORT kind) + retention.py

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~18:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~175/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-367.md`, **blob
aa9115a66f459f89ec970a60998cd26be23cc310** (read at HEAD 9a594e96a8). **Release pin P: a0d8d4943f** (in HEAD).

## The blast radius this half signs

One function, `irpt-export-render`, code built at P. Exactly two packaged members change: `repository.py` (b13bab7495) and
`retention.py` (f60e6f1d2a). No route, IAM, bucket, key prefix, other function or portal file.

## Measured by this seat (not taken from the packet)

| claim | instrument | read |
|---|---|---|
| census at P = the two repinned members, each owned | `p80_cells.py . IB80-1-AC1` (re-runs `release-census.py irpt-export-render --pin a0d8d4943f`) | `2 changed members re-read, each owned: ['repository.py', 'retention.py']` |
| the packaged kind and route at P; clean BUILD_ONLY | `p80_cells.py . IB80-1-AC2` | KINDS ("PERFORMANCE", "ANALYSIS", "CUSTODY_REPORT"); entry.py routes custody-report-read; BUILD_ONLY rc 0 from a clean tree, built idanP8nX... |
| the diff is the two rows only | `git diff 08fe7d444d a0d8d4943f` | 4 lines in, 4 out: two `pin` + two `sha256` fields |
| retention.py is required, not a rider | `git show <pin>:reports/retention.py`, `b13bab7495:reports/repository.py` | packaged `reference(owner, family, logical_id)` at 83e8b9577a; repository at b13bab7495 calls `retention.reference(owner, family, logical_id, revision)` when the revision is a string; f60e6f1d2a takes `policy_revision` |
| rollback target live | `aws lambda get-function-configuration irpt-export-render` (this session, 18:3xZ) | CodeSha256 `03p2eIEKU9iSIOe5GYDbkbisapqAjULUyAPA/Wcxrfc=` |

Writers of the changed property: N = 1 (the function CodeSha256, written by the source-map build plus Terraform). Its rule was read.

## Both branches

- **A, released:** an Opal principal can read a retained CUSTODY_REPORT by reference, once one is retained. A firm principal reads only
  its own firm's covered accounts; otherwise `OBJECT_NOT_COVERED`, with no body. PERFORMANCE and ANALYSIS reads keep the same outcome.
  **But no CUSTODY_REPORT can be retained or read until `reporting_policies.json` carries the family (row D2-W175-S1).** Until then the
  read still fails CLOSED. Releasing first is therefore harmless and moves toward refusal, never toward exposure.
- **B, rolled back:** redeploy artifact version `FHKz88vjxHfi5uqADSw5GlQq8IULm615` (CodeSha256 `03p2eIEK...`) through the Terraform path.
  The owner read returns to DEPENDENCY_UNAVAILABLE.

## STOP conditions for the release order

The applier writes nothing if any of these holds:
1. Both halves are not at HEAD naming blob aa9115a66f.
2. The build is not at P, or its census shows a member other than these two.
3. The live CodeSha256 at the start is not `03p2eIEK...`.
4. No change-management ledger entry is open at the start.
5. The build runs in the dell2 shared tree, not a clean worktree (row D2-S3).

## After-reads owed by the release order

- Live CodeSha256 equals the built `idanP8nX...`, and the census at P reads `changed_members=0`.
- The other-firm `custody-report-read` returns `OBJECT_NOT_COVERED` with no body.
- The Opal read of a REAL CUSTODY_REPORT by reference returns it. This leg is discharged after the registry family row lands and
  IRPT_CUSTDY E2 (`2.0.0_SA_COO~K2`) retains one.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 2.0.0_SA_COO~P2
