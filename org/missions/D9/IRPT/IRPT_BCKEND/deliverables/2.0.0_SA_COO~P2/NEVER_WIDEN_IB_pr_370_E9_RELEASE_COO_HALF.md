# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-370: E9 (per-family policy revisions) in irpt-export-render

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~20:0xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~178/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-370.md`, **blob
1d5120c14b2231b33d8adf3dc5f7a5b186519f67** (read at HEAD a1f2d9f43c on box/dell2). **Release pin P: 0a57f3c0e9**.

## The blast radius this half signs

One function, `irpt-export-render`, built at P. Exactly five packaged members change:
- `repository.py` and `composition.py` (IB-pr-369, 2aa217ec58);
- `reporting_policies.json` (E8, 8530114ff9; `irpt-custody-x10-v1` PENDING);
- `lib/opal_naming.py` (b77e2af4d5, which the new registry needs);
- `submit_installed.py` (IB-pr-369, source dir).

No route, IAM, bucket, key prefix, other function or portal file.

## Measured by this seat (not taken from the packet)

| claim | instrument | read |
|---|---|---|
| census at P: five owned members | `p83_cells.py . IB83-1-AC1` | `IB83-1-AC1 PASS` |
| packaged revisions, registry row, route; clean BUILD_ONLY | `p83_cells.py . IB83-1-AC2` | `IB83-1-AC2 PASS` |
| the source-map diff is the four staged rows only | `git diff e1ed355884 0a57f3c0e9 --stat` | 1 file, 8 lines in, 8 out |
| opal_naming repin is the validator for the new family key | `git show c4fedd31c5:/b77e2af4d5:lib/opal_naming.py`; commit b77e2af4d5 (4.0.0_SA_CRO, X10 registry) | the newer validator carries the family `object` key |
| rollback target live | `get-function-configuration irpt-export-render` (20:0xZ) | `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=` |

## Both branches

- **A, released:** `ReportRepository` keeps PERFORMANCE and ANALYSIS under `irpt-x10-v1`; the replay shows identical bytes, live vs
  built. A CUSTODY_REPORT is composed under `irpt-custody-x10-v1`, but that row is PENDING, so retention REFUSES it ("registered
  enforced policy required"). **Custody stays fail closed until an ACTIVE row is repinned and released (row D2-S8).** Nothing widens.
- **B, rolled back:** redeploy S3 version `fHVzTZi4vdHmRqcy0KK1hmrQ_dcT1QkO` (CodeSha256 `idanP8nX...`) through the Terraform path.

## STOP conditions for the release order

The applier writes nothing if any of these holds:
1. Both halves are not at HEAD naming blob 1d5120c14b.
2. The census at P shows a member other than the five.
3. The start CodeSha256 is not `idanP8nX...`.
4. The built sha is not the packet's `PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0=`.
5. No ledger entry is open.
6. The build runs outside a clean worktree.
7. The offline differential replay (irpt-x10-v1 fixture, live vs built, plus the negative control) fails before the apply.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 2.0.0_SA_COO~P2
