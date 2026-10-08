# L8 drain end -- IRPT_BCKEND round 84, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~20:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (one
function released) | **Drain:** @4e65feb098 on box/dell2 (branch wk-IRPT_BCKEND-179) | **Judgment criteria:** 0 | `round-close-check`: MAY-CLOSE

## IB-pr-371, slot ~179 -- E9 released (pin 0a57f3c0e9)

- **Halves:** COO half @4e3ead72a3, CTO half @c086ec4c2b. The packet is IB-pr-370's, blob 1d5120c14b.
- **Replay** (committed 9082fb60e0, BEFORE the ledger opened):
  - ANALYSIS and PERFORMANCE fixtures under `irpt-x10-v1`, reserved by the live zip.
  - Identical results through both zips: `a7a8ae481b97...` and `04afa6c7a36a...`.
  - Negative control refused by both.
  - Suites passed: 24, 9 and 21.
- **Release:**
  - Start live CodeSha256 was `idanP8nX...`, equal to the rollback target.
  - Built and live are now `PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0=`.
  - Apply: 0 added, 1 changed, 0 destroyed. Re-plan: none. Census at the pin: `changed_members=0`.
  - Ledger `irpt-export-render-ib-pr-371` closed @11cab9a502; no sentinel at HEAD.
  - New artifact version `LefrKSE1...`. Rollback source `fHVzTZi4...`.
- **Graded by the issuer:** IB84-1-AC1 PASS (live re-read) and IB84-1-AC2 PASS. Proof VALID.
- **Served effect:**
  - `ReportRepository` now keeps each family under its own policy revision.
  - PERFORMANCE and ANALYSIS are unchanged (the replay).
  - CUSTODY_REPORT is still refused, because the packaged row is PENDING ("registered enforced policy required"), as expected.
  - E8's ACTIVE row (b4d98a4fe3) rides E10's pair (CTO msg 1536).

## Rows

| row | status |
|---|---|
| D2-W179-S1 | INERT: a fresh worktree has no gitignored `.tools/terraform.exe`; the worker copied it in. Tooling note, no served effect. |

## Next in this lane

E10 (CTO ADDENDUM 10): a production composition site for `persist_custody_report`, with the ACTIVE row, under one pair.

**Push state:** LOCAL on box/dell2.
