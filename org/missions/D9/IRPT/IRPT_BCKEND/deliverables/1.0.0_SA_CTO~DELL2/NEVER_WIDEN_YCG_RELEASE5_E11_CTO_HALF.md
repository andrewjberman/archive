# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 5 (E11 with the E9 modules, plus the X-1 actor read-back)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~00:5xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 2015 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release4_ycg/NEVER_WIDEN_PAIR_RELEASE5_E11.md`,
**blob 553de57d42** (@7d5ff209ab). It supersedes release 4's half (@373a2086d3). Release 4 rolled back at 00:28:52Z (row D2-S16).

## Measured by this seat

| Read | Result |
|---|---|
| pin on origin | `2f3ee8c15b` is an ancestor of fetched origin box/dell2 |
| `release-census.py irpt-ycharts-generate --pin 2f3ee8c15b` | 100 built, 100 live, `changed_members=3`: `composition.py`, `custody_submission.py`, `repository.py`. The packet names exactly these 3 |
| live `get-function-configuration` | `Un0wVZqj...eNY=`, LastModified 2026-10-09T00:28:52Z. This is release 4's rollback, and the packet's rollback |

## Blast radius signed

- **ONE function, 3 members.**
  - E11: the statement revision, through the registry probe.
  - E9: per-family policy revisions, already live in export.
  - Two riders with named owners: `f60e6f1d2a` (~G2, INERT on the live path) and `b13bab7495` (~P2, one line).
  - No principal, route, grant or IAM change.
- **E11 has no live importer at HEAD**, as ~G2 measured. Its served proof stays with IRPT_CUSTDY E2a. This release's served claim is only
  "nothing breaks": after-reads 0 to 2 and 5.
- **Branch B:** roll back to `Un0wVZqj...` in the same session. **The import-census read (2) is the gate that release 4 failed.** Read it before
  anything else is graded.

## Conditions (carried from release 4's half)

1. **Read-back 4 before any delete**, with all three booleans. A missing boolean grades X-1 NOT MET. IB-yr-681 closes only on three trues.
2. **The S3 deletes are Andrew's act per object** (CLAUDE.md Agent Autonomy). The release is not held by them.
3. **The symbol-closure check** (`checks/r71/symbol_closure.py`, missing=0) is re-run against the zip actually uploaded, before the apply.

**Verdict: GIVEN**, for exactly these 3 members at `2f3ee8c15b`.

-- 1.0.0_SA_CTO~DELL2
