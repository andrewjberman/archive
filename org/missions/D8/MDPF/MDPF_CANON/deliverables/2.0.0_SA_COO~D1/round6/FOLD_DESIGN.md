# MDPF_CANON round 6 -- the fe9b Global fold: design read (2.0.0_SA_COO~D1, 2026-10-12 ~15:0xZ)

Read-only. No code, order or decomposition is changed by this file. It is the read the cut stands on, after `FE9B_FOLD_PREP.md` @71af9dbc31 and the CTO's
ADDENDUM 1 (`RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md`, msg 4398). Every number below was read from the served global and firm
`aggregate-aua-timeseries` objects at as-of 2026-10-09 (494 dates, 2024-11-01 .. 2026-10-09), the 2026-10-09 global `aum-metrics` and `category-views`, and the
2026-10-12 global `account-distribution`, plus the consolidator tree at HEAD of `box/dell1`.

## 0. Verdict

The fold is buildable. THREE measured facts stand between the ruling as worded and a cell that can publish. Each is one decision for the CTO; none is mine to make.

| # | Finding | Why it blocks | Section |
|---|---|---|---|
| D1 | The flip guard cannot pass on any honest definition of "held". The five core lines were 49financial's book ALONE on 383 dates (2024-11-01 .. 2026-05-14; inflection's first positive value is 2026-05-15, cottonwood's 2026-06-11). | As ruled, the build counts 383 flips per core line (1,915 in all) and refuses on every run. On a "non-null value" definition it counts 0, but only by treating inflection's measured $0.00 as holding. | 5 |
| D2 | The 3 SMA-class lines cannot fold into a line held by 2 or more firms without breaking the SMA source-basis axis. | `opal_div_sma` and `opal_growth_sma` are 49financial-only and carve-out; `pfde` is cottonwood-only and additive. Any one-firm group still discloses one firm; the only two-firm group is mixed-basis, which the registry and the category-views build refuse by design. | 4 |
| D3 | The two inflection blends are not "other models" to the page: it rolls them 50/50 into the Short, Intermediate and Long archetype cards and adds their counts to the Total Holdings headline. | "Page keeps working" holds (no crash); the numbers it shows move: Total Holdings -185, archetype cards -$43.16M in all. A client-facing number moves, so it is named in the pair and waits on a word. | 6 |

Everything else (the other-models line, the sum rule, the writers, the comparator) is settled in sections 1-3 and 7-9.

## 1. The fold set at as-of 2026-10-09, split by cohort class

"Held" here is the CN-c-1 / CN-d-2 basis the prep read used (a nonzero `account_count` at the as-of in the firm scope's own object). On the as-of both the count and
the value basis give the same 14 of 20 lines held by fewer than 2 firms (measured; they differ only in the history, section 5).

MODEL class (11 lines; inside `model_aua`; sum of the nine valued lines = $68,083,780.15 = the served `category-views` Models > Custom node, to the cent):

| line | held by | value at as-of | count at as-of |
|---|---|---|---|
| `opal_blend_5050_int_ltc` | inflection | 35,463,321.87 | 160 |
| `opal_moderate_income_portfolio` | cottonwood | 8,394,643.90 | 13 |
| `opal_fixed_income` | cottonwood | 8,284,035.47 | 2 |
| `opal_blend_5050_st_int` | inflection | 7,691,846.77 | 23 |
| `opal_income_portfolio_gillham` | cottonwood | 4,024,270.03 | 1 |
| `opal_moderate_income_tax_efficient` | cottonwood | 3,178,004.60 | 3 |
| `opal_muni_sleeve` | cottonwood | 553,337.61 | 1 |
| `opal_15_85_income_portfolio` | cottonwood | 301,744.13 | 1 |
| `opal_moderate_income` | cottonwood | 192,575.77 | 1 |
| `opal_income` (NULL line) | none | null at as-of; last value 2026-08-19 = 1,188,397.34 | null |
| `opal_moderate_income_portfolio_tax_efficient` (NULL line) | none | null at as-of; last value 2026-09-25 = 1,117,136.69 | null |

The two NULL lines are printed with their last dollars as the ruling asks. They fold with the rest: their history dollars enter the other-models line on the
dates they carry them, and the other-models line steps down by exactly those dollars on 2026-08-20 and 2026-09-26. That step is the data, not a defect, and the
fold print states it.

SMA class (3 lines; OUTSIDE `model_aua`; sum $21,532,921.91): `opal_div_sma` 17,103,256.79 (count 40, a `count_as_of` carry), `opal_growth_sma` 4,017,944.59
(count 45, carry), `pfde` 411,720.53 (count 4). Held by 49financial, 49financial, cottonwood.

Six lines stay: the five core models and `tax` (49financial + cottonwood). `tax` is held by two firms at the as-of and on every date it carries a value.

Identity checked (CORRECTED 2026-10-12 by the issuer's re-read of the served 2026-10-09 object; the first text here read "479 of 485 ... the other 6", which was
wrong): the sum of the global model-class lines equals `model_aua` to the cent on 277 of 485 valued dates, and differs by $0.01 or $0.02 (rounding) on the
other 208. So a model-class fold that keeps the sum keeps `model_aua`; an SMA-class dollar added to it breaks that by $21.5M. The two classes cannot share a line.

## 2. Writers of a global per-model leaf (N), counted at HEAD

| object | writer(s) | N |
|---|---|---|
| ts `by_model` | `build_global_artifact` (`dim_mdpf_aggregate_aua_timeseries.py:2247`, iterates `GLOBAL_MODEL_KEYS`, a static tuple); `apply_taxsma_overlay` (writes `tax`); `apply_sma_sleeve_overlay` (writes sleeve members such as `pfde`) | 3 |
| ts `meta.by_model_channels` | `build_global_artifact` | 1 |
| ts `sma_additive_withheld[]` | `apply_sma_sleeve_overlay` (rows carry `member_id`, `firm_id` and dollars) | 1 |
| `aum-metrics` `by_model[]` | `build_aum_metrics` (`dim_mdpf_aum_metrics.py:512`, iterates the literal `MODEL_ORDER`, names via `SERVED_MODEL_NAME`) | 1 |
| `account-distribution` `by_model{}`, `meta.account_count_by_model_key`, `meta.cottonwood_fold.by_model_folded` | `build_firm_distribution("global")` (`dim_mdpf_account_distribution.py:~440`), from account-level values | 1 |
| `category-views` Models > Custom and SMA members | `_shape_category_views` -> `registry.build_category_views`, reading shaped ts `by_model` | 1 |
| gold parquet (wide ts, long others) | `emit_gold_parquet` -> `mdpf_gold_parquet.records_for`, reading the shaped docs | 1 |

N is 8 writers across 7 leaf classes. Not a global-labelled leaf: `mdpf_aggregate_aua.py:430` (the `_aggregate_aua` dated contract) keys `by_model` under each
`partner` entry by `firm_id`; the ruling's property is the Global label, so it is out of the cell and stated so in the pair.

Coupling that the fold must not break: the ts builder reads the staged `gold/mdpf_revamp/global/account_distribution.json` `meta.account_count_by_model_key` to set
each line's FRONTIER count (`load_account_dist_frontier_counts`, `dim_mdpf_aggregate_aua_timeseries.py:769`). If the folded distribution is what lands there, the
folded keys are missing next run and their frontier counts silently revert from the distribution's funded count to the composed-from-legs count (a declared basis
seam: 160 vs 162 on the Int/Ltc blend today). The design keeps that staged object UNFOLDED and folds only the served A4 document (section 3).

## 3. The design

ONE new function, `apply_global_min_firms_fold(arts, firm_scopes)`, in `mdpf_gold_consolidator.py`, called in `build_all` immediately after
`guard_global_served_identity` and wrapped in the same `_isolated` pattern. A fault (a non-zero flip count included) refuses Global alone; the firm scopes and
their objects are unchanged. That is the shape the CTO required of CN-d-1's guard (msg 3573).

1. HELD SET. For each global `by_model` key, `held(key, date)` = the firm scopes (`49financial`, `inflection`, `cottonwood`) whose OWN `by_model[key]` carries the
   per-date predicate chosen under D1. The firm key is mapped to the global member id with `registry.resolve_any`, as the sleeve overlay does. Evaluated against
   `arts` in memory, never a static list.
2. FOLD SET at the as-of `dates[-1]`: model-class keys with `len(held) < 2`. The `tax` line and the five core lines are never in it.
3. FOLDED LINE `other_models` (display name "Other Models", `cohort_class` "model", no `source_basis`):
   - `model_value[i]` = the sum of the folded members' non-null values at `i`; `None` only where EVERY member is `None` (absent is not zero; a member that is `None`
     does not poison the sum, because an absent model is not a measurement gap).
   - `account_count[i]` = the sum of the members' non-null counts, `None` where all are. This keeps `account_count_total` (the W-7 sum over `by_model`)
     byte-equal, because it already sums every key.
   - `count_as_of` = the latest source date any carried member's count was held from; absent when no member carries.
   - It is held by two firms at the as-of (cottonwood for 8 members, inflection for 2) and the build ASSERTS `len(union of held firms of the members) >= 2`, or
     refuses: a folded line held by one firm would be the same disclosure under a new name.
4. REMOVAL: the folded members are deleted from `by_model` and from `meta.by_model_channels`; the line's own channel entry is the sorted union of its members' firms.
   `sma_additive_withheld[]` rows of a folded member are not touched (SMA class, D2).
5. UNTOUCHED, asserted equal before and after: `opal_aggregate_aua`, `model_aua`, `non_model_aua`, `tax_additive_aua`, `sma_additive_aua`,
   `account_count_total`, `account_count_total_raw`, `count_basis`, `count_as_of`, `point_class`, `cohort_provenance`, every top-level key set.
6. FLIP COUNT (D1) is computed and printed on every run, per line, in both directions; non-zero refuses Global.
7. A4 IMMUTABILITY. `conditional_put` records `conflict` and never overwrites an existing dated key. The fold therefore takes effect on the FIRST fire whose as-of
   is a new date. The 135 dated global objects already served (43 ts, 34 aum-metrics, 38 account-distribution, 20 category-views) keep their one-firm lines. A
   retro-fold is a separate served-output act with its own pair (bucket versioning is Enabled, so each key has a version to roll back to). It is not in this
   cell. The CTO is asked in section 9.

Account-distribution: `build_firm_distribution("global", ...)` takes `fold_keys` (default `None`, so every other caller and the staged object are unchanged). With
it, the members' per-account value vectors are CONCATENATED before `_distribution_stats`, because min, max, mean, median, percentiles and std_dev cannot be summed
from per-model stats. A single-account line shows its one balance as min = max = mean today; the pooled line does not. `account_count`,
`active_accounts_count` and `excluded_unfunded_count` equal the sums of the removed entries. `meta.account_count_by_model_key` and
`meta.cottonwood_fold.by_model_folded` drop the folded keys and gain `other_models` (pooled count). Bin edges are identical across models (measured: 1 distinct
`bin_labels` tuple), so histogram counts add.

`aum-metrics`: `MODEL_ORDER` is a literal, so a folded key is dropped silently. The cell adds `other_models` to `MODEL_ORDER` and `SERVED_MODEL_NAME`; its q0-q3
cells come from the folded series with the same `measured_series` and `calc_metric` as the other rows. The two blends leave the list (D3).

`category-views`: `resolve_any` refuses an unknown key (F5, "never fold an unknown into a bucket"). The cell registers `other_models` as a `CategoryMember` in
`mdpf_category_registry.py` (view_path "Models > Custom", qualifier "custom", `served` True), OUTSIDE `CANONICAL_MODELS`, so `GLOBAL_MODEL_KEYS` and the two
crosswalk copies (`data/mdpf/scripts/gold/` and `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/`) are untouched; there is one registry file, no lambda
copy. The Custom node total stays $68,083,780.15 (it sums `by_model`); the 11 members' own rows read `aum: None` (absent), and `other_models` carries the dollars.

Gold parquet follows the shaped documents with no code change. The wide ts partition's column set changes (folded `by_model.<key>.*` columns leave,
`by_model.other_models.*` arrives), so the first fold partition has a different column set from its predecessor.

> CORRECTION (2026-10-12, from `draft/DECOMP_V6_DRAFT.md`): section 3's "registers `other_models` as a `CategoryMember` ... OUTSIDE `CANONICAL_MODELS`"
> is wrong. `mdpf_category_registry.py:773-804` (`_check_crosswalk_keyspace`) raises at import on a model-class member the crosswalk does not hold. The
> fold line is a crosswalk row in both homes (`data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py` and the emitter lambda's copy), which makes the
> cell WORLD-class and adds a deployed package to the deploy order. The draft carries the corrected owned-file set.

## 4. D2 -- why the SMA-class lines are held out of the cell

- `registry.sma_basis_of` / `sma_global_basis_of`: `opal_div_sma`, `opal_growth_sma` read carve-out; `pfde` carries `source_basis: additive`, `firms: [cottonwood]`.
- A by_model entry carries ONE `source_basis`, validated against the registry per firm; a mixed entry is refused at `category-views` build (`SystemExit`, "two
  declarations of the same fact disagree").
- Grouped by basis, each group is one firm: {div, growth} = 49financial; {pfde} = cottonwood. A one-firm group does not satisfy min_firms.
- Withholding them instead moves $21.1M of carve-out SMA from the SMA node into Client and breaks the view-plane identity the build asserts.
- The Global SMA tree already serves `by_firm` per member (MDPF_STRATID R1, Andrew-direct rulings). That firm-level disclosure was granted on purpose, which is
  why the ruling's "per-model line" may not have meant strategy sleeves at all.

Recommendation: the cell folds the 11 model-class lines; the 3 SMA-class lines are not touched; the CTO or the cluster lead names the SMA outcome. The 14-line
count in the ruling then reads 11 folded now, 3 pending.

## 5. D1 -- the flip guard, measured over all 494 dates

A flip, as ruled: an earlier date where a line is held by fewer than 2 firms while the as-of holds 2 or more. Counted only where the global line carries a value on
that date (a date with no global value reveals nothing). Core lines are `ultra_short`, `short`, `intermediate`, `long_term_conservative`, `long_term_aggressive`.

| predicate for "a firm holds the line on a date" | flips, each core line | total | what it means |
|---|---|---|---|
| firm `model_value` non-null | 0 | 0 | passes, but counts inflection's measured `0.0` (383 pre-launch dates) as holding |
| firm `model_value` > 0 | 383 (`ultra_short`: 50 dates held by none, 333 by 49financial only) | 1,915 | the honest reading; the guard refuses every run |
| firm `account_count` > 0 (the prep's basis) | 399 | 1,995 | same; adds dates where a firm has a value and no published count |

Other directions measured: a folded line that held 2 or more firms on an earlier date: 0 (all 14). `tax`: 0 on the value basis (its 486 earlier dates carry no
global value).

What D1 decides, in the CTO's words ("the grant's basis is per DATE"): either (a) the guard's date set starts at the date Global became multi-firm for that line
(2026-05-15 for inflection), so the pre-launch history, which is by construction the single firm that was Global, is outside the guard, or (b) the core lines fold
for those 383 dates too, which leaves Global with no per-model lines for 78% of its history, or (c) the predicate is value non-null and the guard is vacuous for
this history. I recommend (a), stated in-band on the object as the epoch date. It is a rule change to the ruling, so it is asked, not assumed.

## 6. D3 -- what the Model Portfolios page does with the blends (read at `portal/src/pages/ModelPortfolios.tsx`)

| page behaviour | source | after the fold |
|---|---|---|
| donut: `rollBlendsIntoArchetypeModels` adds each blend's AUM/2 to each archetype card and its count to each | `:207`, `BLEND_ARCHETYPES :163` | blends not in `aum-metrics`; Short about -$3.85M, Intermediate about -$21.58M, Long about -$17.73M (exactly half of each blend per archetype; blends sum to $43,155,168.64) |
| Total Holdings headline = `total.account_count` + the blend counts in `account-distribution.by_model` (ANDREW-AUTHORIZED INTERIM, "DO NOT REMOVE") | `:1238-1245` | the reduce finds no blend key: -185 (162 + 23 at 2026-10-12) |
| trend: `rollBlendsIntoArchetypeSeries` for the series the same way | `:171` | blend series absent; archetype series fall by half each |
| unknown key `other_models` | `getCanonicalModelName` passes unknown names through; `trendStackSeries` appends unmapped labels; `sortByModelOrder` puts them last | renders as an extra slice and series; no crash |

So the page keeps working and shows different numbers. The durable fix the page's own comment names (a producer-stated `total.sleeve_level_count`) adds a key,
which the ruling forbids ("served JSON keys unchanged"). The Model Portfolios page is client-facing: a served-object change that moves a client-visible number is
named in the never-widen pair and needs the CTO's and the cluster lead's acceptance of those deltas; no portal push is needed for the fold itself.

## 7. The never-widen pair (to be drafted at the cut, contract fixed here)

- BLAST RADIUS: global `aggregate-aua-timeseries`, `aum-metrics`, `account-distribution`, `category-views` and the global gold parquet partitions, FROM THE FIRST
  NEW-DATE FIRE ONWARD. No firm scope object, no staged object, no dated key already served.
- WRITER COUNT: N = 8 (section 2), printed in the pair, each rule read.
- BRANCHES: (1) flips = 0 -> publishes; (2) flips non-zero -> Global refused alone, firm scopes publish, the prior Global object stays served (stale, never
  half-folded); (3) a fault in the fold -> same isolation.
- COMPARATOR (before = the last unfolded global object per type; after = the first folded one; both read, none rewritten). Per type, on every shared date:
  - ts: every top-level array outside `by_model` and `meta.by_model_channels` equal element by element; each kept `by_model` line equal; `other_models.model_value[i]`
    = the sum of the removed lines' values at `i` (None where all None); counts the same; `count_as_of` and `account_count_total` equal.
  - aum-metrics: `total` equal; kept rows equal; the two blend rows absent; `other_models` present with its aum equal to the sum of the removed rows plus the model-class
    lines the page never showed (printed).
  - account-distribution: `total` equal; kept entries equal; `other_models.account_count` = sum of removed counts; histogram counts = sum; min/max/mean are
    recomputed from the pooled accounts and printed beside the removed entries.
  - category-views: every node `aum` equal (Custom, Models, Client, SMA); `sums` equal.
  - key sets: each type's top-level key set equal across the four scopes and to before (`assert_keyset_identity`).
- LEAVES READ before and after: the census of section 2's seven classes; the pair lists the leaf path classes and the count per class, with the denominator.
- ROLLBACK per key: a folded Global object at a new dated key is restored by version id (versioning Enabled); the old code redeploys from the prior commit under the
  same ledger. A folded object a reader already served is not recalled.
- DISARM: row D1-W8-S5 on the cell's read-back.

## 8. Cell size verdict

One cell, worker class `worker` (not light): the fold function (~120 lines), the distribution `fold_keys` (~40), `MODEL_ORDER` / `SERVED_MODEL_NAME` (~10), the
registry member (~15), tests (~250) are about 200 product lines and one behaviour. Splitting it puts a cross-cell contract (`fold_keys`) between two workers who
share one file. Three mechanical criteria at the cut: (1) the fold unit contract (sum rule, absent is not zero, isolation, flips fail closed, `>= 2` union assertion);
(2) the comparator on a dry-run build, headline arrays byte-equal, every folded line the sum of its members; (3) key-set identity plus firm-scope objects byte-equal.
Write surface: `mdpf_gold_consolidator.py`, `dim_mdpf_account_distribution.py`, `dim_mdpf_aum_metrics.py`, `mdpf_category_registry.py`, one new test file under
`data/mdpf/tests/canon/`, the issuer's check. The registry and `dim_mdpf_aum_metrics.py` are NOT in CN-d-1's code deploy; the consolidator is, so the fold deploys after
that ledger closes. Nothing here touches `bronze_homes.json`, `firm-config.mjs` or another R2 surface.

## 9. What goes to the CTO (three asks, one per message)

1. D1 -- the flip guard's date set and predicate (section 5). Blocks the cut.
2. D2 -- the three SMA-class lines (section 4). Does not block the model-class cell.
3. D3 -- acceptance of the page deltas, and the retro-fold of the 135 dated keys (sections 3.7 and 6). Blocks the pair, not the cut.

Not read in this pass, and the cell's first act: the unfolded staging write path for `gold/mdpf_revamp/global/account_distribution.json` (who writes it on the
daily run, since `build_all` does not stage `dists`), and the MCP gateway tools `mdpf_get_aggregate_aua` / `mdpf_get_account_distribution` as readers of the global
leaves by name.
