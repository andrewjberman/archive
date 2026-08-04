# MDPF_CANRTE Phase A — Canonical Per-Firm Route: DESIGN

**Status:** PHASE-A DELIVERABLE v1.0 — submitted for CTO fork rulings (F-1/F-2/F-3).
**Author:** 0.4.0_DS_ClientPlatform (sole Phase-A seat, Andrew-named).
**Authority:** Andrew-direct mandate @f9952d616f (~06:00Z, verbatim below) · program GO
@ff160d0b5 (~13:07Z) · TIGHT SCOPE v0.1 @86f52bdfb (`docs/architecture/MDPF_CANONICAL_ROUTE_SCOPE.md`,
GOVERNING — on any conflict the scope doc wins and I surface) · COO GO 20260804T132111Z ·
TO `MDPF_CANRTE.A.canonical-route-design` (pending @11a770a93).
**Citation vintage:** every `file:line` in this document resolves at **@e0d657799** (CLOUD HEAD at
design time) unless a different commit-ish is stated inline. A citation without a vintage is not a
citation (CLAUDE.md Rule 22).
**Walls honored:** design-only (zero code changes, zero `data/` commits, zero serve-path contact);
downstream tail untouched; ETFS-CANON not adjudicated (§6.1 boundary statement); today's
MDPF_GLOBAL execution untouched and uncited as evidence.

> Andrew, verbatim (@f9952d616f): *"this process should be exactly the same for every single firm,
> going through exactly the same steps in exactly the same way. all the grief we have is from
> overly complex, not in-pattern, random ass fucking routes for each with no rhyme or reason.
> Your next task for tomorrow is going to be simplifying these to a canonical route for all firms."*

---

## 1. The measured current state (what exists, grounded)

Two chains exist side by side. Naming them precisely is half the design, because several census
"divergences" turn out to be **the seam between the two chains**, not four random routes.

### 1.1 The REVAMP chain (staged, gold/mdpf_revamp/*) — the survivor

```
opal-data-assets MONOLITH silver (per-vendor fact_* partitions)
        |
        |  49financial legs ---- smartx/platform/silver (model)          [dim:68]
        |                        DDB opal-assets-daily-aua               [dim:330-331]
        |                          cohort 49f_schwab_custody (custody)
        |                        schwab/08242234/silver fact_rps_s2      [dim:69, :376-389]
        |  inflection legs ----- eclipse/inflection/silver (model)       [dim:70]
        |                        orion/inflection/silver (custody)       [dim:71]
        |  cottonwood legs ----- blackdiamond/cottonwood/gold/dim_model_portfolio
        |                        + .../silver/fact_holdings (W-2b)       [slice:14-15, :96]
        v
   PER-FIRM SPINE ARTIFACT  gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json
        |     49f + inflection: built in dim_mdpf_aggregate_aua_timeseries.py
        |       (build_49f_artifact / build_inflection_artifact), WRITTEN by
        |       stage_mdpf_revamp_trio.py [trio:45-49, :77]
        |     cottonwood: built + WRITTEN by build_cottonwood_mdpf_slice.py
        |       [slice:98, :934-941] (assets tree, composed at producer)
        v
   GLOBAL FOLD  gold/mdpf_revamp/global/aggregate_aua_timeseries.json
        |     build_global_artifact folds 49f + inf + the cottonwood slice
        |       (load_cottonwood_slice [dim:1653-1715], called ONLY on the
        |       global path [dim:2537-2539])
        v
   DERIVED  gold/mdpf_revamp/{firm}/aum_metrics.json        [metrics:74]
            gold/mdpf_revamp/portfolios/aum-metrics.json    [metrics:55]  <- hyphen, see 4.4
            gold/mdpf_revamp/{firm}/account_distribution.json [dist:63-75]
            gold/mdpf_revamp/cottonwood/{aum_metrics,account_units}.json [pair:4-5, :480, :504]
        v
   TAIL (uniform, OUT OF SCOPE): accrual bridge -> portal/gold/mdpf/{scope}/aum-metrics/{date}.json
        -> platinum publish [metrics:59-77]
```

### 1.2 The LEGACY chain (currently feeding the served platinum rollup) — being retired

```
per-vendor feeders (data/mdpf/scripts/{feeders,gold}): wsb_49f_smartx_model_aua,
  build_mdpf_wsc_inflection_feeder, build_mdpf_wsd2_etf_netassets_feeder,
  build_mdpf_wse_49f_non_model_aua
        |   e.g. WS-C reads opal-data-inf gold/timeseries/client_performance.parquet
        |        [feeder:341-352] and writes opal-data-mdpf feeds parquet [feeder:451-465]
        v
mdpf_aggregate_aua.py reads opal-data-mdpf feeds [agg:228-241]
        v
platinum/mdpf/aggregate_aua/{date}.json via put_with_version_guard [agg:1353-1360]
platinum/mdpf/aggregate_aua_timeseries.json (the 445KB served rollup) written by the
  BACKFILL-tree script build_aggregate_aua_timeseries.py [backfill:78]
```

Retirement intent is already on the record: *"that nested shape belongs to the LEGACY platinum
artifact, which is being retired and must not be edited"* (CTO ruling 2026-07-22, quoted at
[slice:3-6]). Cutover has NOT happened: the spine's account_count carry reads the served
`json/mdpf/{firm}/aggregate-aua-timeseries.json` and its own comment distinguishes
"pre-cutover = legacy; post-cutover json/mdpf IS the revamp" [dim:563-564]. Serve-state claims
here are source+record-grounded (comp-estate names the legacy chain as the served producer at
census vintage; freshness adjectives in that output are snapshot claims, not live reads —
provenance note observed in this session's run).

### 1.3 Builder homes today (the grammar grief, measured)

| home | scripts |
|---|---|
| `data/mdpf/scripts/gold/` | dim_mdpf_aggregate_aua_timeseries, stage_mdpf_revamp_trio, dim_mdpf_aum_metrics, dim_mdpf_account_distribution, mdpf_aggregate_aua (legacy), wsb/wsd2/wse feeders, build_mdpf_wsc_inflection_feeder |
| `data/mdpf/scripts/backfill/` | build_aggregate_aua_timeseries — **writes the LIVE served rollup** [backfill:78] |
| `data/assets/scripts/gold/` | build_cottonwood_mdpf_slice, build_cottonwood_mdpf_pair |
| `data/smartx/scripts/` | compute_per_firm_account_distribution — **writes the LIVE served bell** `json/mdpf/{firmId}/account-distribution.json` [smartx-dist:275-277] |

Four trees produce one product. Two of the four LIVE served artifacts are written from homes
(`backfill/`, `smartx/`) that the route's own tree does not contain.

---

## 2. The canonical route (the design)

ONE route, four layers, identical for every firm. A firm differs ONLY in its **binding row**
(§3) — never in steps, shapes, or grammar.

```
L0  VENDOR SILVER      {source}/{firm-slot}/silver/fact_*        (opal-data-assets monolith)
L1  FEEDER PREP        firm-local, ONLY where vendor grain demands materialization;
                       declared in the binding table or absent          (see F-2, §5.2)
L2  PER-FIRM SPINE     gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json
                       ONE builder, firm-parameterized (F-3), ONE artifact contract (§2.1)
L3  GLOBAL FOLD        gold/mdpf_revamp/global/aggregate_aua_timeseries.json
                       = the same fold mechanism over every per-firm artifact (already the
                       ruled pattern: "one mechanism, not a special case" [slice:10-12])
L4  DERIVED            gold/mdpf_revamp/{firm}/{aum_metrics,account_distribution}.json
                       built off the SPINE artifacts only, never off L0/L1 directly
                       (account_distribution's silver reads migrate under this rule in Phase C,
                       or its exception is declared in the binding table)
TAIL (out of scope)    accrual bridge -> portal gold -> platinum/serve
```

### 2.1 The spine artifact contract (every firm, byte-identical rules)

Already implemented across both existing producers; the design canonizes it:
- `dates` = NYSE trading-day axis from `SERVED_AS_OF_FIRST` (2024-11-01 [dim:114, slice:99-100])
  to the firm's OWN measured frontier — never a sibling artifact's axis ([slice:20-27], the
  circular-frontier removal).
- ABSENT IS NOT ZERO: honest-`None` on any date the firm's sources lack; no LOCF, no
  interpolation, no numeric default ([slice:45-49] — the $107.2M false-dip incident;
  [dim:342-346] YANG_SITTW).
- `cohort_provenance` derived from the READ PATH, never hand-labeled ([dim:73-87]).
- Composed-at-producer: any sanctioned backfill is composed in the firm's OWN producer and
  declared in `meta.composed_backfill`; the fold VERIFIES, it never composes
  (one-live-composition, [dim:1660-1665]).
- Fail-closed leg reads: an absent contracted leg refuses the build ([dim:1686-1690]).

### 2.2 One path grammar

- **Staging** (`gold/mdpf_revamp/`): `gold/mdpf_revamp/{firm}/{artifact}.json`, filenames
  **snake_case**. `{firm}` resolves from `partner_roster.json` (+ literal `global`) — never a
  hardcoded firm string inside a builder body.
- **Serve** (`json/*`, `platinum/*`): filenames **kebab-case** (the live convention:
  `aum-metrics.json`, `account-distribution.json`, `aggregate-aua-timeseries.json`).
- **The rename boundary is the bridge/publisher, exactly once.** Today's hyphen/underscore
  mixture is accidental (§4.4); the rule converts it into one declared boundary: everything
  DS-staged is snake, everything served is kebab, and no other layer renames.
- **One builder home:** `data/mdpf/scripts/gold/` for every route builder. The cot slice/pair
  (assets tree) and the per-firm distribution script (smartx tree) migrate there in Phase C.
  A LIVE served artifact written from a `backfill/` home (§1.3) is a grammar violation on its
  face — the rollup writer moves into the scheduled route or the rollup is re-derived at the
  bridge.
- Phase-C option (flagged, not recommended now): once legacy `platinum/mdpf/*` retires, the
  staging prefix could rename `gold/mdpf_revamp/` -> `gold/mdpf/`; deferred — churn with no
  behavior content until the legacy name is free.

---

## 3. The per-firm binding table (the ONLY place firms differ)

| binding | 49financial | inflection | cottonwood |
|---|---|---|---|
| model leg source | `smartx/platform/silver` fact_model_aum_daily [dim:68, :8-11] | `eclipse/inflection/silver` [dim:70] | `blackdiamond/cottonwood/gold/dim_model_portfolio` [slice:14, :96] |
| custody leg source | **DDB `opal-assets-daily-aua` cohort `49f_schwab_custody`** — Andrew-canonical [dim:330-347] | `orion/inflection/silver` fact_assets.currentValue [dim:71] | `blackdiamond/cottonwood/silver/fact_holdings` W-2b totals [slice:15] |
| feeder prep (L1) | none (facts at grain) | none (facts at grain) | `dim_model_portfolio` (value_date re-key, is_opal filter, blend explosion [slice:29-69]) |
| non-model leg | schwab fact_rps_s2 envelope [dim:376-383] | 2b audit series [dim:2507] | — |
| model-key set | SERVED_MODEL_KEYS (7) [dim:110] | INFLECTION_MODEL_KEYS (7) [dim:106-109] | slice CANONICAL_KEY vocabulary [pair:12] |
| launch seam / depth | SMA_DEPTH_START 2026-05-18 [dim:119-121] | INFLECTION_MODEL_LAUNCH 2026-05-15 [dim:115-118] | first-assignment-date (absent before, honest-None [slice:45-49]) |
| carry window | — | — | roster-derived, `gate_policy.per_partner_max_lag_trading_days` [dim:1749-1761] |

Every row is already config-shaped in source (module constants + `partner_roster.json`
[dim:1718-1746]). F-3 (§5.3) makes the table literal: bindings move to declared config; the
builder body carries zero firm conditionals beyond binding lookups.

---

## 4. The five divergence dispositions (each at source)

### 4.1 The 49f DDB custody detour — CONFIRMED; dispositioned via F-1 (§5.1)
`load_ddb_0824_custody_history` [dim:334-373] scans DDB table `opal-assets-daily-aua`,
FilterExpression `cohort_id = 49f_schwab_custody` [dim:350-352]. It is the only DDB read in any
firm leg. It is NOT an accident: the docstring cites Andrew's 141545Z ruling that this series
SUPERSEDES the fact_rps_s2 envelope [dim:335-341] (trichotomy record
MODELPORTFOLIOS_GLOBAL_VIEW_BASIS_DEFINITIONS_20260723.md). Disposition: the route step becomes
uniform ("read the firm's DECLARED custody source"); the 49f binding stays the Andrew-canonical
DDB series; the storage question is ETFS-CANON's, boundary stated in §6.1. **C-1 disposition:
PRESERVED-BY-BINDING, explicitly — not dropped, not silently generalized away.**

### 4.2 The cottonwood-only tabular gold dim — CONFIRMED; dispositioned via F-2 (§5.2)
`build_cottonwood_mdpf_slice.py` reads `blackdiamond/cottonwood/gold/dim_model_portfolio/`
[slice:14, :96, :226]; no other firm has a parquet gold dim in this chain (49f/inf read silver
facts directly [dim:66-71]). The dim carries REAL vendor-grain work: value_date re-key (a
two-date fact on a one-date key, [slice:29-35]), strict-Opal blend/sleeve filter
([slice:58-64]), the 1.51x non-summable count axis ([slice:66-69]), relationship-grain collapse
(cot BD fact_holdings row = Relationship x Account x Asset; Andrew 08-04 record). Disposition:
firm-local FEEDER PREP (L1), permitted only where vendor grain demands it — see F-2 for the
recommendation and the honestly-named judgment call.

### 4.3 Inflection direct-silver spine leg — CONFIRMED; it IS the canonical base case
`ECLIPSE_SILVER`/`ORION_SILVER` constants [dim:70-71]; the inflection artifact builds from
monolith silver with no DDB and no gold dim. Under §2 this is not a divergence to repair — it is
the L1-absent reference shape for any firm whose silver facts are already at spine grain.
(The LEGACY inf leg — `build_mdpf_wsc_inflection_feeder.py` reading `opal-data-inf`
gold/timeseries/client_performance.parquet [feeder:341-352] — retires with the legacy chain;
it is not part of the canonical route.)

### 4.4 Naming/grammar residue — CONFIRMED, and WORSE than the census recorded
- Census knew: `aum_metrics.json` (staging) vs `aum-metrics.json` (served); homes split across
  `data/mdpf/` and `data/assets/`.
- Measured worse: the hyphen/underscore split lives INSIDE ONE SCRIPT
  (`dim_mdpf_aum_metrics.py` STAGING_KEY `portfolios/aum-metrics.json` [metrics:55] vs
  SCOPE_STAGING_KEY_TMPL `{firm}/aum_metrics.json` [metrics:74]); homes span FOUR trees not two
  (§1.3), including the two LIVE served artifacts written from `backfill/` and `smartx/` homes;
  serve-side grammar itself is split (`json/portfolios/*` legacy-49f vs `json/mdpf/{firm}/*`
  live vs `platinum/mdpf/*` legacy rollup).
- Disposition: the §2.2 grammar ruling (snake staging / kebab serve / bridge as the one rename
  boundary / one builder home / roster-resolved firm slot).

### 4.5 Candidate #5, the cross-firm hardcoded read — ADJUDICATED AT SOURCE: mechanism corrected
The scope's io run attributed `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` as a
read "inside the nominally-49f builder" [INFERRED, scope §6]. Source verdict:
- The read EXISTS [dim:1684-1686] — CONFIRMED as a read in that file.
- It is NOT 49f-leg contamination — REFUTED as stated: `load_cottonwood_slice` is called ONLY
  on the global path (`if "global" in want:` [dim:2537-2539]; also [trio:66]), and it is the
  global fold's CONTRACTED leg read under the one-live-composition ruling [dim:1660-1665],
  fail-closed on absence/un-composed/scope-drift [dim:1686-1713].
- The REAL defect it evidences is 4.4's, one level up: ONE script named like a 49f dim builder
  actually builds THREE firms' artifacts ([dim:2530-2539]), so any file-grain attribution
  (a tool manifest, a reviewer, a successor) mis-assigns its reads. Model-B (F-3) dissolves
  this class: a firm-parameterized builder + explicit binding table makes every read's firm
  scope declarative.

---

## 5. Fork recommendations (CTO rules; these are recommendations with evidence)

### 5.1 F-1 — 49f DDB custody: recommend SHAPE-UNIFORM, SOURCE-PARAMETERIZED (neither pole)
- **Not (a) retire-the-detour:** retiring the DDB read re-points 49f custody off the series
  Andrew explicitly ruled canonical ([dim:335-341]) — that is adjudicating a sovereign ruling
  away inside a route cleanup, the exact move C-1 exists to prevent.
- **Not (b) DDB-for-all:** generalizing the registry hop manufactures new infrastructure for
  firms whose canonical series already land in silver (inf [dim:71], cot [slice:15]) and would
  itself pre-empt the ETFS-CANON storage question from the wrong seat.
- **Recommend (c):** the canonical custody step is uniform — *read the firm's DECLARED custody
  source, per-date, honest-absent, provenance-from-path* — and the source is a binding-table
  row. 49f's row cites the Andrew-canonical DDB cohort as-is. If ETFS CANON later rules that
  series canonically lives elsewhere, ONE binding row flips; the route does not change.
- **C-1:** PRESERVED-BY-BINDING (explicit disposition, §4.1). **ETFS-CANON boundary:** §6.1.

### 5.2 F-2 — dim-for-all vs spine-direct: recommend NEITHER POLE — bind uniformity AT THE SPINE
- Recommend: the route-identity bar sits at L2 (one spine artifact, one contract, §2.1). BELOW
  the spine, L1 feeder prep is firm-local and exists ONLY where vendor grain demands
  materialization — declared in the binding table, absent otherwise.
- Against dim-for-all: 49f/inf facts are already at spine grain [dim:66-71]; adding dims there
  manufactures two hops whose only content is looking uniform. Against kill-the-cot-dim: the
  dim does necessary, tested work (§4.2) and feeds the pair producer [pair:63-65] — inlining it
  into a builder re-creates the 946-line special case Model-B is retiring.
- **The judgment call, named honestly:** if CTO reads Andrew's "exactly the same steps" as
  binding BELOW the spine as well, then dim-for-all is the only compliant answer and
  cottonwood's dim is the template for all firms. My recommendation reads the mandate's grief —
  storage-system forks, shape forks, grammar forks [@f9952d616f] — as a ROUTE-level complaint,
  and vendor-grain normalization as vendor-owned necessity (the same reason silver converters
  are per-vendor). Surfaced, not adjudicated.

### 5.3 F-3 — recommend MODEL-B: ONE firm-parameterized spine builder + binding config
- Evidence it is nearly true already: 49f + inflection + global share one module today
  ([dim:2530-2539]); cottonwood is parallel BY RULING ("built exactly parallel ... one
  mechanism, not a special case" [slice:3-12]); every firm difference found in this design fits
  a binding row (§3); the divergent builders' shared invariants (§2.1) are already
  copy-synchronized across the two producers — a drift class Model-B deletes.
- Shape: one builder, `--firm` driven by the roster; per-firm bindings as declared config
  (partner_roster.json extension or a sibling `route_bindings.yaml` — Phase-B detail); global =
  the existing fold mechanism over N per-firm artifacts; derived producers (metrics, dist,
  pair) collapse into the same parameterization (the cot pair already imports the dim script's
  machinery [pair:63-65] — the consolidation is half-done in the dependency direction).
- **C-2 rider (MANDATORY on this rec):** a Model-B GO carries the comp-pipescript cross-tree
  blindness fix in scope. Measured THIS SESSION (invocations + outputs in §7): the tool cannot
  address `build_cottonwood_mdpf_slice.py` in ANY tree (`--pipeline` enum has no assets tree;
  true rc=1 unpiped), is fully blind on `stage_mdpf_revamp_trio.py` and on the legacy SERVED
  producer `mdpf_aggregate_aua.py` ("no s3_layout constants ... manual review required"), and
  attributes the spine's S3 writes to nobody (the writes live in the stage trio [trio:77], not
  the builder [dim:2575-2580]). No canon route the drift instrument cannot see. Routed THROUGH
  CTO to the graph stream per anti-chatter — no direct contact from this seat.

---

## 6. Boundary statements

### 6.1 ETFS-CANON (the F-1 wall, stated explicitly per the TO)
The F-1 recommendation decides ONLY route shape: that every firm's custody leg is the same
step reading a per-firm declared source. It does NOT decide — and this document nowhere
implies — which DynamoDB table or S3 location is canonical for any series. The 49f custody
binding cites Andrew's existing 141545Z ruling verbatim as a STANDING FACT; it creates no new
canonicity. If ETFS CANON (the separate Andrew P0 at 0.7.0) rules on canonical storage for
these series, its ruling re-binds the affected row(s) with zero route change. If CTO judges any
part of the storage question inseparable from the route recommendation, F-1 ESCALATES rather
than adjudicates — per the scope's own seam clause.

### 6.2 Other walls
- Downstream tail (spine -> aum_metrics -> accrual bridge -> platinum): untouched; this design
  binds nothing past L4 except the §2.2 statement that the bridge is the rename boundary —
  which is a description of its EXISTING role [metrics:59-77], not a change to it.
- `json/mdpf/*` teardown: PARKED under its own gates; the hyphenated
  `json/mdpf/{firmId}/account-distribution.json` is the LIVE SERVED portal bell
  [smartx-dist:275-277] and is treated as live throughout.
- Today's MDPF_GLOBAL execution: not used as evidence anywhere here; all citations are source
  @e0d657799 or committed records.
- One declared route wrinkle carried forward honestly: the spine READS SERVED state for the
  account_count PRESERVE carry [dim:557-604] (deliberate, CTO+Andrew 225137Z, W-7
  self-reference guard [dim:589-603]). The canonical contract names this a CARRY-IMPORT leg
  class rather than pretending the route is serve-blind. Phase B decides whether it survives
  cutover unchanged (its own comment already handles the post-cutover identity [dim:563-564]).

---

## 7. Writes-by-source-read table (every builder in the route; extractor-blind writes named)

The extractor reports "WRITES: none detected" on dynamic keys — treated as UNKNOWN throughout;
every row below is from source read, cited @e0d657799.

| builder (home) | READS (source-cited) | WRITES (source-cited) | extractor saw |
|---|---|---|---|
| `dim_mdpf_aggregate_aua_timeseries.py` (mdpf/gold) | monolith silver smartx/schwab/eclipse/orion [dim:66-71]; DDB opal-assets-daily-aua cohort 49f_schwab_custody [dim:348-358]; fact_rps_s2 partitions [dim:376-389]; SERVED json/mdpf/{firm}/aggregate-aua-timeseries.json (count carry) [dim:566-569]; staged {firm}/account_distribution.json (frontier counts) [dim:631-638]; cottonwood slice json (GLOBAL path only) [dim:1684-1686, :2537-2539]; local partner_roster.json [dim:1728-1738] | LOCAL `--out-dir` files only [dim:2575-2580]. **NO S3 writes in this script** — its artifacts reach S3 via the stage trio | reads partial (2 hardcoded + 5 monolith names); writes "none" = TRUE here but attribution-misleading |
| `stage_mdpf_revamp_trio.py` (mdpf/gold) | via the spine's builders + loaders (imports dim as `spine` [trio:42], cottonwood slice [trio:66]) | `gold/mdpf_revamp/{49financial,inflection,global}/aggregate_aua_timeseries.json`, put + fresh-GET byte-verify [trio:45-49, :72-84]; then invokes metrics + dist mains [trio:50-53, :87-98] | **fully blind** ("no s3_layout constants") |
| `build_cottonwood_mdpf_slice.py` (assets/gold) | cot gold dim partitions [slice:96, :226-240]; cot silver fact_holdings [slice:15]; interpolated-backfill json [slice:16, :758] | `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` (composed), put + head-verify [slice:98, :934-941] | **unaddressable in any tree** (no assets tree in `--pipeline` enum; rc=1) |
| `build_cottonwood_mdpf_pair.py` (assets/gold) | slice vocabulary + dim machinery imports [pair:12, :63-65] | `gold/mdpf_revamp/cottonwood/aum_metrics.json` [pair:5, :480]; `.../account_units.json` [pair:504] via `_stage_upload` [pair:387] | not run through the tool (same tree gap) |
| `dim_mdpf_aum_metrics.py` (mdpf/gold) | staged global + per-firm aggregates [metrics:54, :73, :114, :159-161]; fact_rps_s2 | `gold/mdpf_revamp/portfolios/aum-metrics.json` [metrics:55]; `gold/mdpf_revamp/{firm}/aum_metrics.json` [metrics:74] | reads OK; writes "none" = FALSE (dynamic keys) |
| `dim_mdpf_account_distribution.py` (mdpf/gold) | monolith silver fact_allocation_valuation / fact_model_allocation_roster / fact_portfolios_full (io manifest); cottonwood account_units sidecar [dist:304-322] | `gold/mdpf_revamp/{firm}/account_distribution.json` [dist:63-75] | reads OK; writes "none" = FALSE |
| `compute_per_firm_account_distribution.py` (smartx/scripts) | smartx views (per its own header [smartx-dist:3-9]) | **LIVE SERVED** `json/mdpf/{firmId}/account-distribution.json` [smartx-dist:275-277] | outside every modeled tree |
| `mdpf_aggregate_aua.py` (mdpf/gold, LEGACY) | opal-data-mdpf feeds parquet [agg:228-241]; prior platinum dates [agg:510-527] | `platinum/mdpf/aggregate_aua/{date}.json` via version guard [agg:1353-1360] | **fully blind** — the SERVED producer |
| `build_mdpf_wsc_inflection_feeder.py` (mdpf/gold, LEGACY) | opal-data-inf gold/timeseries/client_performance.parquet [feeder:341-352]; eclipse silver + accounts/portfolios_full [feeder:529-533] | opal-data-mdpf feeds parquet [feeder:451-465] | reads 1 of several; writes "none" = FALSE |
| `build_aggregate_aua_timeseries.py` (mdpf/backfill) | (backfill inputs per its header) | **LIVE SERVED rollup** `platinum/mdpf/aggregate_aua_timeseries.json` [backfill:78] | not a scheduled-route script; home itself is the finding |

File tags: dim = `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` · trio =
`.../stage_mdpf_revamp_trio.py` · metrics = `.../dim_mdpf_aum_metrics.py` · dist =
`.../dim_mdpf_account_distribution.py` · agg = `.../mdpf_aggregate_aua.py` · feeder =
`.../build_mdpf_wsc_inflection_feeder.py` · backfill =
`data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` · slice =
`data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` · pair =
`.../build_cottonwood_mdpf_pair.py` · smartx-dist =
`data/smartx/scripts/compute_per_firm_account_distribution.py`.

---

## 8. Phase-B seed (NOT the plan — Phase B starts only on CTO's fork rulings)

What the migration plan will need, so the rulings can be made with the cost shape visible:
binding config lands first (pure-add); builder consolidation behind DELTA=0 per-firm artifact
parity (staging keys unchanged, so parity is byte-class comparison of staged artifacts);
home migrations (assets-tree + smartx-tree scripts into mdpf/gold) are `git mv` + dispatch
re-point, parity-gated; legacy-chain retirement rides its already-recorded intent [slice:3-6]
and the serve-repoint tail belongs to DE/DT lanes under Phase-C seating; the C-2 tool fix lands
before Phase-C cutover so the route is instrument-visible on day one. Rollback = staged keys
are additive throughout; nothing serve-facing moves until Phase C under its own gates.

---

## 9. Self-audit (TO phase-2 mandate)

- Every divergence disposition (§4) carries `file:line` @e0d657799: 4.1 ✔ · 4.2 ✔ · 4.3 ✔ ·
  4.4 ✔ · 4.5 ✔ (CONFIRMED-read / REFUTED-as-contamination, both cited).
- Candidate #5 explicitly adjudicated at source: §4.5.
- INFERRED remainders, labeled: serve-state chain attribution (which chain feeds served
  platinum TODAY) rests on comp-estate census-vintage + source comments [dim:563-564], not a
  live serve read (deliberate — Phase A is serve-blind by wall); the smartx per-firm dist
  script's READ set is header-cited, not line-walked (its WRITE — the live bell — is
  line-cited, which is the load-bearing half here).
- Reserved words check: "proof/provably/root cause/definitively" — absent. "Confirmed" appears
  only on source-cited claims.
