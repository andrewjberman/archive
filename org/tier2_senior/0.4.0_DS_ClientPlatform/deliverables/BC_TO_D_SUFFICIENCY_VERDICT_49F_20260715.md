# B/C -> D SUFFICIENCY VERDICT — 49F (bd) Group-D Consumed-Input Census

**TO:** OPAL_GLDRNS.A2 | **Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-07-15 (~20:5x-21:2xZ)
**Status:** COMPLETE — 8/8 publishers censused; every consumed field carries a verdict.
**Consumes:** A1 contract @ 9be9c2402 (the D-to-D edge map + per-script input lists are this census's
spine). **Judged against:** build plan @ baba79230 (`OPAL_RUNNERS_49F_BUILD_PLAN.md`), dictionary v0.5
(`OPAL_RUNNERS_49F_SILVER_DATA_DICTIONARY.md`, current), Wave-2 cores @ 80240881d, D1 dim v1.1 (built
+ live, NO-FEE binary law), B_00 lots-union spec. W1 census cited not redone
(`OPAL_RUNNERS_W1_SCRIPT_CENSUS_20260714.md`). **Gate this verdict serves:** OPAL_CONSOLIDATION C5b —
no Wave-3 C-port spec freezes until this lands. Basis: BLACK DIAMOND 0833 throughout, never summed.

## 1. Method + denominators

Column census = static source extraction over the 8 D scripts @ repo 0f248d7f9 (regex pass over
`columns=` projections, `_load_parquet`/`_read_s3_parquet` bindings, df-subscript string refs — raw
output preserved in session scratchpad `a2_column_census_raw.txt`) + hand attribution of variables to
input tables from the A1 source reads. Extraction caveat stated honestly: regex subscript capture
under-counts fields referenced via `.col` attribute access or computed names; per-table rows below are
therefore a LOWER BOUND labeled per-table, and two fields are carried as UNKNOWN rather than guessed.

| denominator | count |
|---|---|
| Publishers censused | 8/8 |
| Consumed input surfaces | 16 (13 gold tables/prefixes + 1 legacy-cert JSON + 2 lib/off-S3 classes) |
| Distinct consumed fields carrying verdicts | 88 |
| Verdict distribution | CARRIED 61 · RENAMED 3 · DERIVED-IN-D 7 · MISSING 5 (-> CTO) · UNKNOWN 2 · DELETED-LAYER-DISPOSITIONED 10 |
| Pre-declared divergences (S4 harness section) | 10 |
| CTO-ruled surface classes applied | ORPHAN-NO-FEED-REQUIRED (employee_leaderboard platinum) · OUT-OF-D-SCOPE-PRODUCER-NAMED(ES-1) (exec_summary) |

## 2. Census + verdicts, by consumed input table

### T1. `gold/timeseries/account_performance.parquet` -> **C_01.account_performance** (G4 port)
Consumers: D_00, D_00b, D_00c, D_02, D_04. Fields (17):
`date, account_id, relationship_id, total_aua, cum_inflows, cum_outflows, nna, daily_inflow,
daily_outflow, num_positions, aua_taxable, aua_tax_deferred, aua_tax_exempt, tax_status` -> **CARRIED**
(G4 port; flows via C_00's dim_transaction sb-code decomposition; tax splits via A_00.tax_status join —
derivation named). `growth, market_growth` -> **CARRIED** (C_00's decomposition names growth:
`d_aua = nna_cash + nna_in_kind + income - fees_tax + growth`). `pct_priced` -> **MISSING (M4)**.
`synthetic_correction, aua_residual, churn` -> **DELETED-LAYER** (sec-4, injection artifacts).

### T2. `gold/timeseries/client_performance.parquet` -> **C_02.client_performance** (G5)
Consumers: D_00, D_00b, D_01. Fields (12): `date, relationship_id, total_aua, aua_taxable,
aua_tax_deferred, aua_tax_exempt, cum_inflows, cum_outflows, nna, daily_inflow, daily_outflow,
num_accounts` -> **CARRIED**. D_01's `period_nna/period_inflows/period_outflows/lifecycle/nmnc/nmec`
are **DERIVED-IN-D** (lawful window differencing + cohort split inside the publisher; derivation =
period boundaries x first_seen — stays D-side). Cross-contract `SUM(account)==relationship`
row-for-row preserved per plan verification 3.

### T3. `gold/dimensions/accounts_dimension_latest.parquet` -> **A_00.dim_account**
Consumers: D_00, D_00b, D_00f, D_01, D_04. Fields (13): `account_id, account_name` -> **CARRIED**
(acc identity; FAM/SLM naming = dictionary open cell 1). `relationship_id` -> **CARRIED** (A_01
household reconstruction). `relationship_display_name` -> **RENAMED** (A_00/A_01 `relationship_name`).
`relationship_first_seen_date` -> **CARRIED** (per-type first-seen, LABELED fallback semantics —
divergence D8). `tax_status` -> **CARRIED** (tax-from-title derivation — divergence D3).
`architect, implementor, local_ops` (+ consultant/additional_advisor/manager read via T5) ->
**CARRIED** (JOIN DIM 2 facts, never txn-derived — the named 49F variance). `client_state,
client_city, client_country` -> **CARRIED** (acc address passthrough — the lossy-ACC scar row).
`account_type` -> **CARRIED** (acc registration; the legacy left-join-to-allocations disappears, named).

### T4. `gold/dimensions/client_dimension.parquet` -> **A_01.dim_relationship**
Consumers: D_00, D_01, D_02, D_03, D_04. Fields (6): `relationship_id, relationship_name,
first_seen_date` -> **CARRIED**. `has_taxable, has_tax_deferred, has_tax_exempt` -> **CARRIED**
(derivation named: any-account-of-tax-status rollup in A_01).

### T5. `gold/views/account_team.parquet` (legacy C_07) -> **C_08.advisor_attribution** on dim_advisor_fee_role
Consumers: D_00, D_00b, D_00c, D_00f, D_01, D_02. Fields (9): `account_id, architect, implementor,
consultant, local_ops, additional_advisor` -> **CARRIED** (D1 dim's 6 role columns are facts).
`architect_no_infer` -> **CARRIED** (anti-pathology (c): house/placeholder inference stays gold-side +
labeled — the precedent is cited by the dictionary itself). `_role_split_pct / split weights` ->
**CARRIED** (6 split pcts in D1 dim; "No Normalizing" verbatim law). `weight` (assignment tenure) ->
**CARRIED** (SCD2 effective periods replace first/last-date tenure windows — divergence D6 names the
value-shift risk).

### T6. `gold/views/rel_architect_lookup.parquet` -> **C_08 relationship-grain rollup**
Consumers: D_00, D_01, D_02, D_03. Fields (4): `relationship_id, architect, primary_architect,
primary_state/primary_city` -> **CARRIED** (rollup of T5 by relationship; geo via A_00 address). 

### T7. `gold/views/client_tax_liability.parquet` -> **C_05.tax_liability** (G7)
Consumers: D_00, D_02. Fields (6): `account_id, long_term_gain, short_term_gain, total_accrued_gain,
total_cost_basis, total_market_value` -> **CARRIED** (G7 on real 1099-DIV + ULT actuals; the legacy
holdings_lots fallback patch is DELETED — divergence D7 pre-declares gain-value shifts).

### T8. `gold/dimensions/fee_rate_history.parquet` -> **JOIN DIM 2 fee-schedule columns** (+ C_09/C_10)
Consumers: D_00, D_02. Fields (6): `account_id, effective_date, end_date, end_date_raw, fee_bps,
is_current_rec` -> **CARRIED** (dim_advisor_fee_role v1.1: 8 fee-schedule columns, SCD2 in-table,
dual-fee alternates carried never-slimmed). Downstream `fee_earning/no_fee` splits (consumed at every
headline) re-ground on the BINARY fee-presence law (dim-row-exists / no-row, mechanically derived,
observed-state-not-business-assertion) — divergence D4. G13 billable-gate drift fixed at C_10 port
(plan, verbatim).

### T9. `gold/canonical/advisor_fee_detail/{date}.parquet` -> **C_09.advisor_fee_efficiency** (G12)
Consumers: D_00c, D_02. Fields (8): `advisor, date, fee_yield_bps, ann_fee, implied_revenue, role,
split_pct, share_daily/prorated_daily_fee` -> **CARRIED** (C_09 on D1-dim rates x C_01 AUA).

### T10. `gold/canonical/nna/{date}.parquet` -> **C_03.nna** (G6)
Consumers: D_00b, D_00c, D_00f, D_01, D_02, D_04. Fields (8): `account_id, date, daily_inflow,
daily_outflow, nna_txn, net_nna, relationship_id` -> **CARRIED** (G6 port; flows from dim_transaction
sb-codes via C_00). `nna_clean` -> **CARRIED** as a QUALITY FLAG — the A1 sec-7 pin binds: it is
never an aggregation filter (summing over ALL rows is the served semantic). `hh_seen` -> **UNKNOWN**
(household-first-seen marker; carrier not named in plan — verify at G6 port whether C_03 carries or
A_01 derives; one-line check, does not gate Wave-3).

### T11. `gold/canonical/role_aua/{date}.parquet` (written by D_02 pre-pass) -> **MISSING (M2)**
Consumers: D_00b, D_00c, D_01, D_02. Fields (10): `date, advisor, role, aua, aua_current,
aua_fee_paying, aua_no_fee, avg_split_pct` + `ghost_flag, source_filter_stack` (exclusion-stack
fields -> sec-4). **No planned C table owns (date, advisor, role) AUA.** This is also the INVERTED
D-to-D edge from A1 (a D script feeding earlier-phase scripts). PROPOSED RESOLUTION: C_08 EMITS
role_aua as a first-class output table (it is literally "advisor attribution x AUA"); this
simultaneously kills the inverted edge and the D_02 pre-pass. ROUTES TO CTO.

### T12. `gold/timeseries/holdings_lots/{date}.parquet` (B_01 FIFO) -> **B_00.lots** (fact_uln + fact_rld union)
Consumers: D_00b, D_02, D_03, D_04. Fields (9): `account_id, ticker, asset_name, market_value,
cost_basis, acquisition_date` -> **CARRIED** (vendor lot fields; no FIFO anywhere). `is_open` ->
**RENAMED** (B_00 `lot_status`). `accrued_gain` -> **DERIVED-IN-D legal today, carried as B_00
`market_value - cost_basis`** (derivation named). `asset_class` -> **RENAMED-RESOURCED** (C_07 on
dim_asset from fact_sec — no regex banks; divergence D2). B_01's FIFO/phantom-lot taxonomies are
DELETED-LAYER (sec-4); lot counts/cost-basis value shifts pre-declared (D7).

### T13. `gold/validation/aua_certification/{date}.json` (legacy recon cert) -> **DELETED-LAYER + MISSING (M1)**
Consumers: D_00 (headline AUA authority + degenerate-cert floor), D_00b, D_01. Fields (3):
`certified_aua, gold_aua, gap_pct`. The producing reconciliation layer is deleted per casebook; its
replacement C_04.recon_guard FLAGS and never patches — **so the plan currently names NO authority for
the SERVED firm-AUA number once the cert dies, and no home for the never-serve-a-degenerate-AUA floor**
(D_00:246-280, A1 sec-7 invariant). PROPOSED RESOLUTION: headline AUA = C_02/C_01 computed total,
gated by C_04's flag state, with the <=0 floor preserved as an emit-time assert in the D_00 port
(hold-last-good semantics retired WITH the cert, divergence D5). **THE BIGGEST CELL — it decides what
number the portal headline shows. ROUTES TO CTO.**

### T14. `gold/dimensions/dim_advisor_office.csv` -> **MISSING (M3)**
Consumers: D_00b, D_01 (the `ofc`/office views + `ofc_per_period` — live served surfaces in
timeseries_chart + header_metrics granularities). Fields (2): `advisor -> office` mapping. Absent from
dictionary + plan. PROPOSED RESOLUTION: fold `office` into JOIN DIM 2 if the BD allocation report
carries it (it carries roles/splits/fees today — one bytes-check answers), else a small maintained
dim under the same SCD2 pattern. ROUTES TO CTO.

### T15. bd silver `allocations` read DIRECTLY by D_04 (cohort_a, cash_coverage, out_of_scope, c1_recovered)
Fields (8): `account_id, allocation_aua, account_market_value, cash_market_value, rep_code, custodian,
classification_bucket, in_dimension/exclusion_reason`. **RE-SOURCED (named):** these transparency/audit
artifacts re-ground on JOIN DIM 1 (`fact_allocation_account_map`) + `fact_rps_s2` balances + A_00
membership in the monolith build — a D script reading raw-side silver directly disappears with the
legacy feed (which died after 07-10; D1's daily REST bronze is the replacement source of record).

### T16. D-to-D JSON inputs (A1 sec-5 map) + lib/off-S3 dependencies
- D-to-D re-wiring is mechanical once C tables exist (new-D re-reads new-C; the plan's INCREMENTAL
  PUBLISH model consumes A_00/C change manifests). No field verdicts beyond T1-T15 (the JSON fields
  are those tables' fields, already versed above).
- `lib.exclusions` (ghost ids, insurance config, AP gate; consumed D_02/D_03/D_04) -> **DELETED-LAYER**:
  per-exclusion NAMED DISPOSITION at port (obsolete-by-construction vs still-a-real-business-rule) —
  already mandated by the plan; census note: `ghost_flag` + `source_filter_stack` reach the SERVED
  role_aua table today, so dispositions must land BEFORE M2's table freezes.
- `lib.etf_classifier` (DynamoDB; D_03/D_04) -> **RESOURCED** to dim_asset classes (divergence D2).
- `lib.advisor_nna_attribution` (D_00c + D_00f shared) -> **CARRIED** (the cross-route per-advisor NNA
  identity is a pinned invariant; C_08 owns the one source).

## 3. MISSING register (5) — each at CTO's gate BEFORE Wave-3 C-port spec freeze

| id | missing thing | consumed by | proposed resolution |
|---|---|---|---|
| M1 | Served firm-AUA authority + degenerate floor home, post-cert | D_00 headline (every firm surface) | C_02-computed total gated by C_04 flags + emit-time <=0 assert; retire hold-last-good WITH the cert (divergence D5) |
| M2 | (date, advisor, role) AUA table — legacy role_aua | D_00b, D_00c, D_01, D_02 | C_08 emits role_aua as a first-class output; kills the D_02 pre-pass + inverted edge |
| M3 | advisor->office mapping (ofc views) | D_00b, D_01 | fold office into JOIN DIM 2 if the BD report carries it (bytes-check), else small maintained dim |
| M4 | pct_priced / pricing-coverage source | D_00, D_00b (priced-AUA weighting) | C_01 carries pct_priced from the canonical-prices coverage; NOTE the prices builder (`build_canonical_prices_v2`) is itself an UNMAPPED W1 variance — resolve its group home in the same ruling |
| M5 | `hh_seen` carrier | D_00f | verify at G6 port: C_03 carries or A_01 derives (one line; non-gating) |

## 4. Deleted-layer dispositions (10 fields/mechanisms, each named)

| deleted mechanism | D-consumed artifact of it | disposition |
|---|---|---|
| Injection/synthetic layer | `synthetic_correction` (D_00b growth_decomposition, D_04 decomposition_90d + rfs decompositions) | ceases by construction (PIT RPS spine); field emits absent/0 + schema note — divergence D1 |
| Injection/synthetic layer | `aua_residual`, `aua_residual_delta/sum`, `churn` | unexplained delta becomes C_04 FLAG territory, never a shipped column patch |
| Reconciliation layer | `certified_aua/gold_aua/gap_pct` + degenerate-cert floor | M1 (above) |
| Ghost/AP-gate exclusion stack | `ghost_flag`, `source_filter_stack`, lib.exclusions call sites | per-exclusion named disposition AT PORT (obsolete vs real rule); must precede M2 freeze |
| B_01 FIFO/phantom-lot taxonomies | holdings_lots FIFO fields | vendor ULN/RLD truth (B_00); D7 |
| C_05 holdings_lots fallback patch | tax gain fields | G7 vendor actuals; D7 |
| Legacy B_00 BD<->Schwab reconcile/NAME_ALIASES/self-heal | (no direct D consumption found — census note) | gone with dual-source |
| Txn-engine valuation (ruled unacceptable) | (indirect: all AUA fields) | PIT snapshots are the valuation spine — dictionary law |
| Legacy A_01/A_02/A_03 | advisor roles from txn archaeology | JOIN DIM 2 facts (T3/T5) |
| Legacy allocation left-join enrichment | `account_type` enrichment | acc registration fields (T3) |

## 5. PRE-DECLARED DIVERGENCES (the S4 harness consumes THIS section; undeclared = FAIL, declared = DESIGN)

| id | surface(s) | expected divergence | why lawful |
|---|---|---|---|
| D1 | growth_decomposition, decomposition_90d, rfs decompositions | `synthetic_correction` term disappears | injection layer deleted by construction |
| D2 | every mix/composition/concentration surface | some asset-class assignments shift | classifier swap: regex banks + DynamoDB -> dim_asset (fact_sec) |
| D3 | tax splits everywhere (aua_taxable/deferred/exempt, tax_exposure) | some accounts reclassify | tax-from-title replaces legacy inferred patch (W-2 bar already names it) |
| D4 | fee_earning/non_fee splits on every headline | counts/AUA shift | binary fee-presence law (dim-row-exists), Andrew-direct ~17:1xZ |
| D5 | firm headline AUA | value re-grounds; hold-last-good behavior retired | cert layer deleted (M1 resolution) |
| D6 | advisor books, leaderboards, role_aua | per-advisor AUA/NNA shift where SCD2 periods differ from legacy tenure windows | roles become JOIN DIM 2 facts; no txn archaeology |
| D7 | lots, tax gains, account summaries | lot counts + cost basis shift on some accounts | FIFO deleted; vendor lot truth (B_00/G7/G8) |
| D8 | active_since, first_seen, NMNC/NMEC cohorts | some dates shift | custodian start_date where carried; first-seen fallback LABELED; per-type floors |
| D9 | MAX/inception windows (timeseries, leaderboard MAX, cumulative_chart) | history shortens to per-type monolith floors (acc/rps/trn 2024-07-08; rld 2023-07-12) unless the pre-floor thaw lands | Andrew open cell: pre-floor history default — carried, NOT resolved here |
| D10 | ofc views | shape preserved or retired per M3 ruling | office source is a MISSING cell |

## 6. cohort_a discrimination cell (CTO ruling 3, executed)

The 49F tenant page CALLS `getCohortASummary` on every load (`_partners/49financial/index.tsx:191-196`,
react-query) and renders the transparency note ONLY on success (`{cohortSummary && ...}` :309). On the
404 (consumed key `platinum/firm/cohort_a_summary.json` ABSENT — A1-verified; written key is
`gold/platinum/firm/cohort_a_summary.json`) the query errors, `data` stays undefined, and the note
SILENTLY never renders. **VERDICT: live consumer, FAIL-SILENT — the renders-and-fails class, masked by
the conditional render.** Escalating to CTO + DT as a portal defect per the ruling (the demo tenant
:156-158 has the same call). The one-line fix is EITHER side (D_04 write key or FE path) — held for
the CTO+DT verdict per instruction; noted that the D_04-side fix would also need the platinum listing's
retirement pass to not orphan the old key.

## 7. IMPROVEMENT-CANDIDATES (Andrew DIRECTIVE 8 via CTO 210455Z — shape improvements, each naming the D-emitter it builds into)

| id | candidate | builds into | evidence |
|---|---|---|---|
| I1 | Per-entity ARTIFACT MANIFEST + type-aware cleanup: each entity dir carries an expected-artifact list; cleanup diffs against it (kills the exec_summary orphan CLASS, not just the instance) | D_04 (all entity fan-outs) | A1 finding 2 mechanism: id-scoped cleanup is artifact-type-blind |
| I2 | `schema_version` on EVERY platinum artifact (ownership_map already has it; ~30 surfaces do not) — makes S4 parity + future migrations mechanical | all 8 D emitters | ownership_map precedent (schema frozen v1) |
| I3 | In-band basis label (`nna_basis`-style) extended to every NNA-bearing surface (advisor summaries, nna_clients, advisor_nna_canonical, cumulative_chart) | D_04, D_00f | never-summed law; dashboard.headline already carries it |
| I4 | Retire the 36MB platinum `timeseries_chart.json` in favor of the purpose-built 7x-smaller `cumulative_chart.json` (one consumer each today; the big copy is a pass-through burning 36MB/night) OR gzip-at-rest it (D_00f's gzip pattern is proven in the same bucket) | D_04 pass-through + FE re-point | A1 shapes; D_00f gzip precedent |
| I5 | Unify the analytical-artifact grammar: `gold/platinum/firm/*` (cohort_a, cash_coverage) is a path family NOTHING routes to — move to `platinum/firm/*` at the D_04 port (with the cohort_a defect verdict from sec-6 deciding the FE side) | D_04 | sec-6; A1 finding 3 |
| I6 | role_aua becomes a C_08 first-class emitted table (M2) — removes the D_02 pre-pass, the inverted edge, and the exclusion-stack fields riding a served table | C_08 (feeding D_00b/D_00c/D_01/D_02 ports) | T11 |
| I7 | Retire legacy dual-writes at cutover rather than porting them (D_01 legacy gran files, D_03 `gold/advisors/`, frozen fargate relics) | D_01, D_03 ports | A1 finding 5 |
| I8 | INCREMENTAL PUBLISH manifests (plan sec: change-manifest-driven entity re-publish) — named here because the census confirms the fan-out (23,593 objects) is the cost center | all D ports | plan incrementality contract; A1 fan-out denominators |

## 8. Sufficiency verdict (the C5b answer)

**The planned B/C shapes are SUFFICIENT for the D-group's consumed inputs EXCEPT the five MISSING
cells in sec-3** — of which M1 (served-AUA authority) and M2 (role_aua owner) are structural and must
resolve before Wave-3 C-port specs freeze; M3/M4 are single-ruling cells; M5 is a port-time
verification line. Every other consumed field is CARRIED/RENAMED/DERIVED-IN-D with its source named,
every deleted-layer input has a disposition, and the 10 expected divergences are pre-declared for the
S4 harness. 

-- END --
