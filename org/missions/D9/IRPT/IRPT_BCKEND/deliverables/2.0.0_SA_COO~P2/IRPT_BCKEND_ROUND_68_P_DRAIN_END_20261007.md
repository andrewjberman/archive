# L8 drain end -- IRPT_BCKEND round 68, workstream ~P (the EMERGENCY export fail-closed release)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~16:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD

**Cut from:** CTO msg 525 (a non-zero reach is a security exception), after IB-pr-347 measured non_opal_reach = 7. The release was
re-pinned after the issuer's census refused the first pin. Decomposition section 61.

## The order

**IB-pr-349, applier laptop `0.7.0_AE_CloudOps~I`.**
- **Branch drained** @3501b78d4a; the amended after-reads and proof reached dell2 through origin (@0fe967b745).
- **Flipped complete** @8cfdf2a38c.
- **Judgment criteria:** 0.

## The real run of the outcome

The real run is production itself. `irpt-export-render` serves CodeSha256 `aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`
(LastModified 2026-10-07T14:38:36Z). The issuer's `release-census.py irpt-export-render --pin b921635dad` reads `changed_members=0`:
live equals the signed pin, which carries the fail-closed `entry.py` fc241d806ecc.

**Graded on the deployed bytes by the applier:**
- An existing receipt that names no account is REFUSED for an admin and for a non-Opal principal.
- An Opal read is ADMITTED.
- There is no blanket deny.

**Re-run by the issuer at HEAD 581ccf5454:**
- IB68-1-AC1 PASS under AMENDMENT 1. The live CodeSha256 is re-read by the check.
- proof VALID.
- The ledger `org/critical_paths/change_management/20261007T1356Z_irpt-export-render-ib-pr-349-failclosed-20261007_deploy_completion.md`
  is CLOSED.

## What the issuer caught and ruled

1. **Pin 34f71024a1 omitted the fix.** The source map staged `entry.py` at 0642c9d004.
   - The COO half was refused (@477f0faa28).
   - The re-pin @b921635dad has a census of exactly the nine members CTO amendment 1 names, including six IB-pr-336 custody members
     that the CTO's widened half covers.
2. **Row S382.** After-reads 4-5 (a NEW export READY, plus its admitted-read log line) need an authenticated Opal principal; creating
   one is an auth-plane write the order forbids.
   - AMENDMENT 1 @b883510cd9 (agreeing with CTO REC msg 757) marks them OPEN-BY-DESIGN.
   - They are discharged by the first real Opal export read with its `irpt_export_read_admitted` line.

## Rows

| row | what it records |
|---|---|
| S385 | disarms W148-S1 (BLOCKING: 7 non-Opal principals reached a fail-open read) and W146-S1 |
| S381, S382, S383, S384 | minted on the laptop by the applier |
| S371 | disposed W148-S2 as wrong face wording, per ruling 106244 |

## Still open

- **The back-fill.** Every existing export stays refused until IB-pr-350 runs. IB-pr-344 counted 1 receipt. IB-pr-350 is cut
  (@3e85fbf2b0) to the same applier: pass 1 census and packet, then halves, then apply.
- **The open leg.** New-export READY stays OPEN-BY-DESIGN until the first real Opal export.
- **Push state:** LOCAL at the time of writing.
