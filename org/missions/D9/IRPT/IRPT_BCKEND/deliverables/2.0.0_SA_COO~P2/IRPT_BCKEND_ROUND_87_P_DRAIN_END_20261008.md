# L8 drain end -- IRPT_BCKEND round 87, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~22:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (one
function released) | **Drains:** IB-pr-375 @ed1303986b, IB-pr-374 @f13741c8d4, both on box/dell2 | **Judgment criteria:** 0 |
`round-close-check`: MAY-CLOSE (2 orders)

## IB-pr-374, slot ~182 -- the Performance client statement writer released, function only

- **Halves:** COO half @cb29ea67bd, CTO half @ece42ad420 (conditions 2-4 bind).
- **Replay** (committed a5eeec04a4, BEFORE the ledger opened):
  - ANALYSIS `a7a8ae481b97...` and PERFORMANCE `04afa6c7a36a...` gave identical results through the live and built zips.
  - The negative control was refused by both.
  - Suites passed: 24, 9 and 21.
- **Release:**
  - Start live CodeSha256 was `PbyqmHBQ...`, equal to the rollback target.
  - Built and live are now `rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek=`. The issuer re-read live at ~22:3xZ.
  - Apply: 0 added, 1 changed, 0 destroyed. Re-plan: none. Census: `changed_members=0`.
  - Ledger `irpt-export-render-ib-pr-374` closed; no sentinel at HEAD.
  - **The route `POST .../custody-report` was NOT applied.** It waits for the laptop IAM leg (row D2-W181-S1, CTO condition 2).
- **Graded by the issuer:** IB87-1-AC1 PASS (live re-read), IB87-1-AC2 PASS. Proof VALID after AMENDMENT 1 (row D2-W182-S2: the issuer's
  cell_refs derivation defect).

## IB-pr-375, slot ~183 -- persisted_by + content binding (CTO condition 1, row D2-W181-S2)

- **persisted_by:** the stored record carries the verified caller's principal id. A body key `persisted_by` is refused by name.
- **Binding:** the document must declare `composition_sha256`, equal to the retained REQUEST_COMPOSITION artifact's content hash. An
  absent or different hash is refused (INVALID_INPUT) and writes 0 blobs.
- **Graded by the issuer:** IB87-2-AC1 PASS (5), IB87-2-AC2 PASS (5; whole file 54). Mutant controls bite.
- This is code only. It ships in the next release pair of irpt-export-render, cut to `0.7.0_AE_CloudOps~DELL2` (Andrew-direct, msg 1756).

## For the CTO (condition 1)

- **Row D2-W183-S1:** `custody-report-read` returns only the document, so an HTTP reader does not see `persisted_by`. It is in the
  stored record.
- **Row D2-W183-S2:** the binding proves which composition the statement claims. It does not recompute the sections, because the render
  is IRPT_CUSTDY's. Every producer must post the hash.

Both are ruled into this packet by row D2-S10.

**Push state:** LOCAL on box/dell2.
