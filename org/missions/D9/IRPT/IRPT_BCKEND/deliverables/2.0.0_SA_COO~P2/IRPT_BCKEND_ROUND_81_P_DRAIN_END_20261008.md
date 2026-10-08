# L8 drain end -- IRPT_BCKEND round 81, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~20:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (one
function released) | **Drain:** @4f101ea53d (branch wk-IRPT_BCKEND-176) | **Judgment criteria:** 0 | `round-close-check`: MAY-CLOSE

## IB-pr-368, slot ~176 -- the IB-pr-367 release (repository.py + retention.py at pin a0d8d4943f)

- **Halves:** COO half @764a0abf3c. CTO half @275e506034, with its AMENDMENT 1 @49efddd80c (condition 1 restated as an offline
  differential replay, msg 1423).
- **First seat:** STOPPED pre-apply on row D2-W176-S1, because `irpt-export-render` has no read route for a retained
  ANALYSIS/PERFORMANCE report. Nothing was applied. The issuer's AMENDMENT 1 @0004fcc566 replaced the live read-back with the replay.
- **Replay** (committed d8d2fb723c, BEFORE the ledger opened):
  - One ANALYSIS fixture under `irpt-x10-v1`, reserved by the LIVE zip's code path.
  - Live and built `repository.get` returned the same result_sha256, `a7a8ae481b97...`; neither raised or refused.
  - Negative control: an altered `policy_sha256` was refused by both zips (`RetentionRefused: retention binding changed`).
  - The three suites passed, each run alone (24, 9, 21).
- **Release:**
  - Start CodeSha256 was `03p2eIEK...`, equal to the rollback target.
  - Live CodeSha256 is now `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=`, equal to the packet's built sha.
  - Apply: 0 added, 1 changed, 0 destroyed. Re-plan: no changes. Census at the pin: `changed_members=0`.
  - Ledger `irpt-export-render-ib-pr-368-20261008`: 4 of 4 legs closed, no sentinel at HEAD. Branch B did not fire.
  - New artifact version `fHVzTZi4...`. The rollback source stays `FHKz88vj...`.
- **Graded by the issuer:** IB81-1-AC1 PASS (live re-read), IB81-1-AC2 PASS. Proof VALID.

## What this changes and what it does not

- The live function now packages a repository whose KINDS names CUSTODY_REPORT.
- **The custody read still fails CLOSED.** No retention policy family exists yet: E8 (`~M2`) adds it, and E9 (IB-pr-369) retains the
  kind under its own revision.
- PERFORMANCE and ANALYSIS behave the same. The replay proves it for the served combination.

## Rows

| row | status |
|---|---|
| D2-W176-S1 | Resolved by D2-W176-S2 (CTO msg 1423, replay commit d8d2fb723c). |
| D2-W176-S3 | Carried by D2-S6 to E9's release pair: the packaged composition.py lags HEAD and must be repinned with E9. |

## Next in this lane

IB-pr-369 (E9) code, worker ~177, is re-seated on AMENDMENT 1 to disarm D2-W177-S1. The custody revision will be requested only when
the registry carries the row. Its branch stays undrained until then.

**Push state:** LOCAL.
