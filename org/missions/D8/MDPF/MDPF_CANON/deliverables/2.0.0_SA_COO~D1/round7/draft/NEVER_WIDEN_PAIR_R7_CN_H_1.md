# MDPF_CANON round 7 -- never-widen pair for CN-h-1: the frontier account counts read the newest A4 account-distribution at or before the axis date (S5 disarm)

**DRAFT -- COO half UNSIGNED.** Written by a fork of `2.0.0_SA_COO~D1` on 2026-10-13 ~11:4xZ for the issuer to read and sign after the cell is drained and
the fold's first scheduled fire is read. A signature is a line in a commit by the issuer; no fork carries it. Nothing here is deployed or committed.

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on a WORLD order cut after the drain by the CN-d-1 and CN-f-1 orders' shape.
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R7_CN_H_1_CTO_HALF.md`; COO half = this lane.
**Status:** COO half OWED (issuer); CTO half OWED.
**Rulings this pair carries:** the CTO's round-5 ADDENDA 3-5 (msgs 4773, 4776, 4780, 4782): S5 is "the Lambda's frontier counts read the frozen
08-18 distribution"; use the newest A4 at or before the axis date; no A4 -> refuse the counts, honest absent, never the staged runner object; name the
per-scope moves; both branches; prior VersionIds; cut after the fold's first fire is read; S5 disarms on its read-back.
**Code:** the cell is `TASK-ORDER MDPF_CANON.TO-CN-h-1` (draft at `round7/draft/TO-CN-h-1.DRAFT.md`); the pin is the drain merge, not yet cut.

## 1. Code

- **Pin:** the CN-h-1 drain merge (`<pin>`, to be named), which must be an ancestor of origin's `box/dell1` before D1 (`git ls-remote`, then
  `git merge-base --is-ancestor`), and must carry the fold (`51cfc93ea8`) in its history.
- **What changes:**
  - `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`: `load_account_dist_frontier_counts(firm_id, axis_date=None)` selects
    `portal/gold/mdpf/{firm_id}/account-distribution/<date>.json` with the greatest key date `<= axis_date`; none -> `{}`; a non-absence failure
    raises `C2-SIBLING FAIL-LOUD`; a `period` after the axis -> `{}`; the as-of sentinel is the A4's own `period`. Its two call sites (`build_firm_timeseries`
    for `49financial` and `inflection`, `build_global_artifact` for `global`) pass the last date of the series. Nothing else in the file moves.
  - `data/mdpf/scripts/gold/tests/test_canplat_p1_1.py` and `test_global_fold_flag2.py`: one stub lambda each takes the second argument.
  - `data/mdpf/tests/canon/test_frontier_counts_a4.py` (new, not shipped).
- **The rule as built:** the frontier cell (the last date) of each overridden model line is the A4 map's value; a series key not in the A4 map keeps its
  COMPOSED count (the two blends and the fold line `other_models` after CN-f-1); cottonwood never calls the loader; the staged
  `gold/mdpf_revamp/*/account_distribution.json` is no longer read by this module and is not touched.
- **Evidence (issuer's checks, `round7/checks/r6_cn_h_1.py`):** at base reader 1 of 8 (H0 control), seams 1 of 4 (S4 control), comparator 1 of 5 (K0
  control); on a scratch reference tree 8 of 8, 4 of 4, 5 of 5. The offline reader arms grade the function the build calls through a fake S3 client,
  as CN-d-1's A6 and CN-f-1's C11-C13 did, not `build_all`.

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | the one named file `dim_mdpf_aggregate_aua_timeseries.py` through `safe-deploy.sh`; read back with `python .tools/mdpf-code-equality.py --files <it>` (exit 0) | `s3://opal-data-mdpf/code/scripts/gold/` | re-copy the key's prior VersionId, recorded before the copy |
| D2 | `build_package.py --pin <pin>`, upload, ONE targeted `safe-apply` on `mdpf-gold-lambda` whose plan moves the function's code and the single environment value `MDPF_GOLD_COMMIT` (the full SHA of the pin built; row D1-S18 rule) and nothing else | the function | rebuild at the prior pin (the fold's merge pin or later), restore `MDPF_GOLD_COMMIT` to the printed prior value, apply the same target |
| D3 | NOT DEPLOYED: the emitter package; the staged runner objects; Stage 6; any dispatch file | -- | none owed |

**Sequencing.** Starts only on the issuer's written GO that the fold's first scheduled fire (2026-10-14 13:30Z at the earliest) is read and closed; one
change per scheduled fire, so this cell's first fire is 2026-10-15 13:30Z at the earliest and is attributable to this order alone; never within 45
minutes before the 13:30Z fire or while the runner dispatch or the gold lambda runs; in a gap between FIRMBKTS window acts; it touches none of the
router, guard, CloudFront behaviours, `bronze_homes.json`, `firm-config.mjs` or the WAF rider (PRD v2.11 R2).

## 3. Writers of the property (N = 6 distinct writer functions of a frontier `account_count`, counted at HEAD)

The property is the last-date `account_count` of a by_model line (and the totals composed from it) in a served object. ONE function chooses the
INPUT (`load_account_dist_frontier_counts`); six functions write the leaf:

| # | writer | leaf it writes |
|---|---|---|
| W1 | `build_firm_timeseries` (`dim_mdpf_aggregate_aua_timeseries.py`, override about :1233) | ts `by_model[k].account_count[-1]` for 49financial and inflection |
| W2 | `build_global_artifact` (same file, override about :2623) | ts `by_model[k].account_count[-1]` for global |
| W3 | `compose_count_total` (:625; global's own composition inside W2) | ts `account_count_total` from the by_model counts |
| W4 | `apply_global_min_firms_fold` (`mdpf_gold_consolidator.py`, CN-f-1) | the `other_models` count (sum of folded lines' counts); reads the composed counts |
| W5 | `build_aum_metrics` (`dim_mdpf_aum_metrics.py`, rows about :450 and :566; totals about :458-475 and :578-593) | aum-metrics rows `account_count` and `total.account_count` |
| W6 | `emit_gold_parquet` / `mdpf_gold_parquet.records_for` | the gold parquet count columns of the same cells |

Each rule was read: W1 and W2 are the only ones whose INPUT changes; W3-W6 follow from W1/W2 by the existing code and gain no new rule. Not a
writer of this property: `build_firm_distribution` (the A4 distribution itself, read here, not written), the staged object (frozen, unread).

## 4. Blast radius (what the act may touch)

- **Moves, from the first scheduled fire after D2 that mints a new date:** per scope, the last-date `account_count` of every overridden model line in
  the `aggregate-aua-timeseries` object, its `account_count_total[-1]`, `meta.frontier_count.staleness` (49financial; STALE -> FRESH or a few days),
  the aum-metrics rows' `account_count` and `total.account_count`, and the gold parquet cells of the same fields. Overridden keys: global the keys of
  `GLOBAL_MODEL_KEYS` that the A4 map carries (14 of 18 on the 2026-10-09 object, 6 of which move; the staged map carried 7); 49financial its 5 core
  keys; inflection its 7 keys.
- **Cannot move:** any dated object already served (write-once), any value (dollar) field, cottonwood, the staged `gold/mdpf_revamp/*` objects, the
  Model Portfolios page's Total Holdings headline (it reads the A4 distribution total, already fresh).
- **State writes of the gold run (C-S65 clause):** this cell adds none. The set named in the fold's pair (`round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md`
  section 4: `mdpf/global/state/taxsma_control/current.json` and the other routine state keys, each with its prior VersionId as rollback) applies to any
  on-demand gold run this order takes; the order prints each overwrite key's prior VersionId before D2.

## 5. Expected outcome, read from the rules (both branches)

- **An A4 exists at or before the axis date** (every trading day since 2026-07-28 on global and 49financial, 2026-07-27 on inflection): the frontier
  counts equal the selected A4 map's values for the overridden keys; `meta.frontier_count.staleness.as_of` is the A4's `period`, FRESH when it equals the
  frontier date; STALE (not refused) when the newest qualifying key is older (a day whose own run wrote no A4).
- **No A4 at or before the axis date** (not seen on any current axis; reachable only for an axis before 2026-07-28, i.e. a historical backfill): the
  loader returns `{}`; the override does not run; the frontier count stays at its composed value. For 49financial that is the honest-None it already
  carries (its count source is the served import, `same_source` False). For global and inflection the cross-axis gate's clause (v) (`account_count`
  is None iff `model_value` is None where count and value come from the same snapshot) reads a None frontier count beside a present value as a BUILD
  FAILURE: that scope is refused whole by the existing gate, its prior object keeps being served, no staged object is read. **The CTO's "refuse the
  counts, honest absent" is therefore, for global, the refusal of the Global scope that day, by an existing gate, not a quiet None** (the loader
  docstring already calls this "a coherence RESET the gate check catches"). Stated here so the pair is signed on the real branch.
- **A failed read (not absence):** `C2-SIBLING FAIL-LOUD`: the build raises for that scope and nothing is written for it.
- **The A4 map lacks a series key** (the two blends and `other_models` after the fold): that line keeps its composed count.
- **A fault inside the cell:** the existing isolation records it and refuses the scope; siblings unchanged.

## 6. Per-scope moves this pair accepts (priced; the first fire's own numbers are read from that fire)

| scope | overridden keys moved | frontier sum served -> fresh | `account_count_total[-1]` |
|---|---|---|---|
| global (A4 keyed 2026-10-09, the one the rule selects for the 2026-10-09 axis) | 6 of the 14 builder keys the A4 map carries (ultra_short, short, intermediate, long_conservative, long_aggressive, blend int_ltc; the 8 others read equal) | 8179 -> 8598 | 8264 -> 8683 (+419) |
| global (A4 keyed 2026-10-12, the issuer's first price) | the same 6 of the 7 staged-mapped keys | 8157 -> 8581 | 8264 -> 8688 (+424) |
| 49financial | 5 of 5 | 7144 -> 7474 (+330) | 7144 -> 7474 (equals the A4 distribution total) |
| inflection | 5 of 7 | 548 -> 560 (+12) | 548 -> 560 (equals the A4 distribution total) |

(The CTO named global +424; that is against the A4 keyed 2026-10-12. The rule selects the newest key at or before the axis, so on the first fire the
move is the difference between the staged 2026-08-17 roster and the selected key, one trading day earlier than the table's first row if the axis
trails by a day. Source: `round6/S5_FRONTIER_COUNTS_PRICE.md` @b246f4786f and this draft's comparator, K2.)
- Client-visible: the per-model account counts and the per-scope totals on the aggregate-aua-timeseries and aum-metrics objects (the Model Portfolios
  cards and any reader of `account_count`); `/portfolios` is partner-facing, so whether Andrew is told as information is the CTO's.

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

On the first SCHEDULED fire after D2 that mints a new date (2026-10-15 13:30Z at the earliest), per scope, with denominators printed:
1. each overridden key's served `account_count[-1]` equals the selected A4 map's value (the A4 read at its own key and `period`);
2. `meta.frontier_count.staleness.as_of` (49financial) is that A4's `period` and the verdict is FRESH when equal to the frontier date;
3. `account_count_total[-1]` moved by the sum of the overridden keys' deltas, and every other field equals the prior object on the shared dates;
4. the aum-metrics rows' `account_count` and `total.account_count` equal the ts's (the existing count-axis law);
5. no staged `gold/mdpf_revamp/*/account_distribution.json` was requested by the run (the lambda log carries no read of it);
6. the run manifest: `errors` empty, `run.code.commit` equals the pin (D1-S18).
The issuer's read-back script for items 1-6 (`round7/checks/r7_frontier_readback.py`) is OWED and is written, and dry-run against the served
objects, before the deploy order is issued. S5 disarms on this read-back (the CTO).

## 8. What the COO half asks the CTO half to read

1. Section 5, the no-A4 branch: for global and inflection the "honest absent" is the existing gate's scope refusal; is that the branch you ruled?
2. Section 6: the moves, with the A4 key date the rule selects, and whether Andrew is told as information.
3. Section 3: N = 6 and the statement that the staged object is unread; the stub-test grant (two one-line lambdas).
4. The sequencing in section 2 (the fold's first fire read first; one change per fire).

## COO half -- OWED (`2.0.0_SA_COO~D1`)

Sign on the bytes the CTO read, naming: the blast radius in section 4, both branches in section 5, the rollback per key in section 2, and the
conditions that the pin is on origin before D1 and that the fold's first scheduled fire reads closed in writing before D1.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
