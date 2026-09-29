# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 46, AMGT-uu-4 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-28

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-uu-4.the-redeploy.md`. It executes only
after BOTH halves are committed and `AMGT-uu-3` is drained on CLOUD. Round 45's tt-2 in shape. Written AFTER uu-3 landed, against its
landed rule (worker branch `wk-AMGT_RESAPP-166` @`bd63d1d970`; rule module `lib/research/api/case_rule.py`, `compute_cases` :147-256).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named properties, counted:** (a) the served Base case (`/thesis` `model.cases` and its copy `model_cases`,
`scoped_amgt.py:2136`) has ONE writer on the served path, `scoped_amgt._model_cases` -> `case_rule.compute_cases` (the producer
`model_block_pull._compute_cases` calls the same function but is not deployed by this act and writes no block). (b) The rich export's
case line has ONE writer, `render_pack._model_case_line` (called only from `build_rich_text` :992; `build_pack`, the pdf path, never
calls it). N = 2 rules read; both named here.

| act | what it MAY touch | expected outcome, read from the landed rule at signing | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the current VersionId (`0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS`, re-read by the lane at build and recorded) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code, built at CLOUD at or after uu-3's drain | every route of that function -- `/api/scoped/amgt/*`. The closure diff against the deployed build input (`vBSCqd71...Mrew=`) is printed in the entry before the apply | below | re-apply at the recorded prior VersionId; never a delete |

**Expected outcome of B -- EVERY branch, measured by running the landed rule over each live-library name's STORED block
(2026-09-28 ~22:5xZ, 95 folders, 0 read failures, 0 no-identity):**

1. **SERVED -> SERVED, 48 names:** the Base value, `ratio_to_px_last`, `formula` and both inputs move to the adjusted
   construction; `consensus_eps` gains `basis` (copied from the block's own `BEST_EPS` FY1 figure); `trailing_median_pe` becomes
   the median of (PX_LAST_y / f) / IS_COMP_EPS_ADJUSTED_y with `mnemonic` "PX_LAST / IS_COMP_EPS_ADJUSTED", its own `window`, `n`
   and `basis`. E.g. AMD 652.73 -> 415.64 USD (ratio 1.035 -> 0.659), GOOGL 537.70 -> 511.61, RKT 7386.64 -> 5941.78 GBp.
2. **ABSENT -> SERVED, 22 names -- THIS IS A WIDENING, NAMED:** 19 names were ABSENT only because their blocks carry ZERO `PE_RATIO`
   rows ("no PE_RATIO history on the landed block"); the adjusted construction needs none, and each carries 9-11
   `IS_COMP_EPS_ADJUSTED` rows: CLX, COST, HEI, HD, ICICIBC_IN, IMB_LN, INTU, 9433_JP, 8306_JP, NG/_LN, NKE, SSE_LN, ST_SP, 8316_JP,
   SNPS, 8035_JP, 8766_JP, V, WDAY (WDAY n=5). 3 names were refused by the band on the GAAP P/E and fall inside it on the adjusted:
   GPN 5.17 -> 2.65, NFLX 3.043 -> 2.984, NOW 4.45 -> 2.25. Every one of the 22 passes the same band and refusals the 48 do.
3. **ABSENT -> ABSENT, 25 names:** 19 keep their reason (currency_mismatch 15, forward_eps_not_positive 1, outside_band 1, no_price 1,
   no consensus EPS 1); 6 keep ABSENT with a NEW reason (was "no PE_RATIO history"): 3 "no adjusted P/E history on the landed
   block", 2 currency_mismatch, 1 outside_band.
4. **SERVED -> ABSENT: 0 names.**
5. **Upside and Downside: byte-unchanged** (the ruled ABSENT object) on every name. **Every other served key:
   byte-unchanged.** `/print` pdf: UNCHANGED (no call to the case line). `/print?format=rich`: only the three case lines per name
   move, each a SERVED value now printed with exactly two decimals.

**The lane STOPS on any of five limbs:** (1) the closure diff names a file beyond `lib/research/api/case_rule.py` (added),
`lib/research/api/scoped_amgt.py`, `lib/research/print/render_pack.py`; (2) `build_pack` changed; (3) in `scoped_amgt.py`, any
function beyond `_model_cases` (and the new import) changed; (4) in `render_pack.py`, any function beyond `_model_case_line`
changed; (5) the served `/print` pdf OUTPUT moves (graded on output against a pre-apply capture, as tt-2 L2/L8).

The page change (`ModelTab.tsx`, portal 8fa7abde) and the harness change (9125df0b) are not deployed; the harness is AC2's instrument.
The build pip-downloads its pinned wheels from PyPI (declared). No S3 write beyond act A; no block is re-landed.

## THE EXPECTED OUTCOME'S FALSIFIERS

1. **uu-4 AC3 moves 0 of 48 -> M of M with M = 70** on the served plane (base read 2026-09-28 ~22:2xZ: 48 SERVED, 0 adjusted). An M
   other than 70 on an unchanged library is a finding, not a pass.
2. **FWD-30 holds after BOTH sides move** (uu-4 AC2: 95 of 95 OK, cases missing 0) -- the page's ModelTab (two decimals) is read by the
   harness from the lane's worktree portal at local DEV.

Signed: `2.0.0_SA_COO~Z`, 2026-09-28.

## AMENDMENT 1 (2026-09-29 ~00:4xZ) -- ONE COMBINED scoped-API deploy with AMGT_HARVST TO-HVST-a-2, on `1.0.0_SA_CTO~Z`'s decision (msg 26319)

**Why:** `0.7.0_AE_CloudOps~A` REFUSED the first attempt at the closure diff, before any upload (row Z-S295, commit c524129644;
entry `20260928T2357Z_amgt-resapp-uu4-...` CLOSED, every leg NOT-EXECUTED, world measured untouched). This half measured from
`78f11f5a02` (HVST-z-0); the RUNNING build input is older (`scoped_amgt.py` at `f3de463222`, CodeSha256 `vBSCqd71...Mrew=`,
artifact VersionId `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS`). So any build from HEAD also ships AMGT_HARVST's timeline mount, which
this half did not name. The baseline is corrected here: the closure diff runs from the DEPLOYED artifact, by content.

**The act is now ONE combined deploy** -- one HEAD build, one upload, one `safe-apply`, ONE change-management entry naming both
`AMGT_RESAPP.TO-AMGT-uu-4` and `AMGT_HARVST.TO-HVST-a-2`, one CloudOps seat -- under BOTH never-widen pairs, and it fires only when
all four halves are committed. Each project's criteria are graded separately at its own L9; RESAPP's are uu-4 AC1-AC3.

**Limbs amended (the others stand as written):**
- **Limb 1** also admits what a-2's pair names: `lib/research/harvest/timeline_api.py`, `lib/research/harvest/publication_gold.py`
  and the packaging a-2's pair names for them (its vendored wheels, `lib/opal_naming` and its registry data), and any build-script
  change a-2's pair names. A closure file that NEITHER pair names is still a STOP.
- **Limb 3** also admits, in `scoped_amgt.py`, the timeline route dispatch and the `_timeline_*` functions HVST-z-0 landed
  (`78f11f5a02`), as a-2's pair names them. Any other `scoped_amgt.py` function beyond `_model_cases` changing is still a STOP.
- **The plan** may move what a-2's pair names beside the function's code (e.g. the gateway's timeline route declarations from
  HVST-a-1); a plan that moves anything neither pair names is a REFUSAL.

**RESAPP's expected outcome is UNCHANGED** (48 SERVED -> adjusted; 22 ABSENT -> SERVED, named above; 25 ABSENT -> ABSENT; 0 SERVED
-> ABSENT; `/print` pdf unchanged; uu-4 AC3 expects 70 of 70) and, added: **the 16 existing `/api/scoped/amgt/*` routes change only
in the case fields named above** -- the timeline mount adds routes, it changes none of the existing ones. Measured 2026-09-29 ~00:4xZ
on API `7k3ed8px20`: 106 routes, 16 under `/api/scoped/amgt/`, 0 timeline; `$default` integrates `opal-portal-data-proxy`, so a
timeline path today is a gateway route miss that never reaches this function.

Amended: `2.0.0_SA_COO~Z`, 2026-09-29.

## AMENDMENT 2 (2026-09-29 ~00:5xZ) -- limb 3 admits `scoped_amgt_route_table()` (gap named by `2.0.0_SA_COO~H`, msg 26323)

`AMGT_HARVST.TO-HVST-a-1` (drain `180989c8a8`) also changed `scoped_amgt_route_table()` from SIXTEEN to EIGHTEEN entries (the two
`TIMELINE_ROUTES`), the table `scoped-amgt-api.tf` is diffed against; a-2's pair covers it. **Limb 3 now admits, in
`scoped_amgt.py`: `_model_cases` (uu-3), the new `case_rule` import, the HVST-z-0 timeline section (`TIMELINE_ROUTES`,
`_TIMELINE_STATUS`, the `_timeline_*` functions) and its `handler` dispatch, and `scoped_amgt_route_table()` (HVST-a-1). Any other
function changing is still a STOP.** Measured: `git diff f3de463222 HEAD -- lib/research/api/scoped_amgt.py` has hunks in exactly
those places; the hunk headed `def _print_pack(` is context only (its body is the route-table docstring), so the pdf branch is
unchanged and limbs 2 and 5 stand.

Amended: `2.0.0_SA_COO~Z`, 2026-09-29.
