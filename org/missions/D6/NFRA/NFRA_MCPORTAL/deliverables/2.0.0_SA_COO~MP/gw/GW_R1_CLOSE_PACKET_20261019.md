# NFRA_MCPORTAL -- L8 packet for the CVO: two ungraded judgment criteria (FWD-20) and the evidence file for FWD-1, 2, 14-17

**From:** `2.0.0_SA_COO~MP`. **To:** `3.0.0_SA_CVO~Z`. **Date:** 2026-10-19 ~19:3xZ. **Push state:** LOCAL on `box/sitez` (not read against `origin`).
**Why now:** `python .tools/round-close-check.py --project NFRA_MCPORTAL --round 1` reads `verdict=REFUSED` with exactly two judgment criteria ungraded: `TO-MP-z-2 AC3` and `TO-MP-z-6 AC2`. Nothing below grades either one.

Absolute roots used below: `file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/` (repo-relative paths follow in backticks).

## 1. MP-z-6 AC2 (new today)

**Criterion (verbatim from the order):** Andrew's own reading of the page shows he got the full breakdown he asked for -- every vendor or channel, the tools and indexes on each, and the current state of entitlements -- which is also his stated condition for closing NFRA_OPLGTW.

| what | where |
|---|---|
| his words, verbatim, with the window | `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~16/z6_andrew_read.md` |
| the run file (channel, both tool lists, principal, both tool lists) | `.../0.9.0_WK_NFRA_MCPORTAL~16/z6_run.json` |
| the proof instance (AC2 recorded `UNVERIFIABLE-BY-INSTRUMENT`, no verdict) | `.../0.9.0_WK_NFRA_MCPORTAL~16/NFRA_MCPORTAL.TO-MP-z-6.fwd20-close-run.proof_of_spec.json` |
| the order, with AMENDMENT 1 | `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-z-6.fwd20-close-run.md` |

His words (2026-10-16 ~18:5xZ, at the issuer's terminal): "we can close the name one box projects i see those displaying cleanly. gateway reads well. and, open calls lets close the sitez-20261009T173038Z-21c5 id, as well as sitez-20261013T213807Z-21d9. and also close laptop-20261013T153821Z-44eb"

**What AC1 measured (mechanical, PASS 4 of 4, drained `0aba910bd0e`).** Gateway access log for 2026-10-16T18:30Z-19:05Z: `GET /api/admin/gateway/breakdown` 200 x24; the Control Plane's four data routes each 200 (boxes 2, overlap 2, gitstate 2, calls 3); channel `portal_index` 6 tools, page equals deployed code; principal `opalbloomberg@opalinvest.com` 5 data-grant tools, page equals the store read under the operator role. Control arms of the check: base FAIL (no run file); an empty window (12:00-12:30Z) FAIL.

**Said plainly so the grade rests on the right object:**
- His words are short. They say the page "reads well"; they do not list vendors, tools, indexes or entitlement state. Whether that meets the bar is yours.
- The window is a superset (his look was ~18:40-18:55Z; the minute was not recorded). The log shows page activity starting 18:40Z.
- The first run of this order failed on the issuer's own mistakes (a sparse worktree missing the read paths; a pick rule that chose a bucket channel; a store reader that had only writers). AMENDMENT 1 changed the method, not the bar: row `NFRA_MCPORTAL-Z-S75`.
- Channel choice tied at 6 tools (`portal_index`, `ycharts`); the worker took `portal_index`, first in page order (row Z-W16-S6). Principal choice: the first non-owner principal with a data grant in page order (Z-W16-S5).

## 2. MP-z-2 AC3 (older, still ungraded)

**Criterion (verbatim):** Control Plane and Open Calls read easily at a glance, and no identifier breaks mid-token. Graded on the issuer's rendered screenshots of both pages with live data (after AMENDMENT 1, 2026-10-13).

| what | where |
|---|---|
| Control Plane, after the readability amendment | `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/fwd20/render_20261013/mp_cp_after.png` |
| Open Calls, after | `.../fwd20/render_20261013/mp_oc_after.png` |
| Control Plane full page; Gateway page | `.../fwd20/render_20261013/mp_cp_full.png`, `.../mp_gw.png` |
| the order | `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-z-2.gateway-page-and-route-list.md` |

Not a grade, only a fact: on 2026-10-16 Andrew said of the live Control Plane "i see those displaying cleanly".

## 3. Evidence file for FWD-1, 2, 14, 15, 16, 17 (not a criterion; CTO `1.0.0_SA_CTO~Z` msg 36018: "put it in the record for the CVO's L9 grade")

`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/EVIDENCE_FOR_CVO_FWD_1_2_15_16_17_20261019.md`. It lists what the project holds with a claim level on each line (RECORDED, MEASURED-NOW, ABSENT). The human halves of FWD-1, 2, 14, 15, 16 and 17 are ABSENT; the orders that would have produced them (`MP-c-2`, `MP-v-2`, `MP-x-5`, `MP-q-1`) are `cancelled` citing Andrew's `ANDREW_DIRECT_20261019_163xZ_SIX_HANGING_OPEN_CALLS_RESOLVED.md` or his 2026-10-16 closing of call 21c5. That record grades nothing; the grading is yours.

## 4. Rows this packet leaves for you

`NFRA_MCPORTAL-Z-W16-S1` (BLOCKING, the issuer's provisioning), `-S3`, `-S4` (BLOCKING, the order text): all three answered by AMENDMENT 1 and `Z-S75`. `-S2` (ARMED): disarmed by `Z-S75`; its residue (the commit-time naming gate prints NAMING ERROR and does not refuse in a sparse worktree) is carried to `0.0.0_AB_MSTR` as the gate's owner. `-S5`, `-S6`, `-S7`, `-S8`: OBSERVATION, INERT.

## 5. Open after this

The People page controls (`MP-pd-4`) call a per-person access route that PD has not released; `MP-pd-7` and `MP-pd-8` stay staged and PD stays held by the CTO. The P1 display cell (CTO msg 36021) waits on `2.0.0_SA_COO~O` adding the per-index vendor and firm pair to the breakdown.
