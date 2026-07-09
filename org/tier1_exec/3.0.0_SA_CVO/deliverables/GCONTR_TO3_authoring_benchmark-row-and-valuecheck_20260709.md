# NFRA_GCONTR.TO-3 -- authoring pass: benchmark row (SEV1) + the period_defs value-check

**Author:** 3.0.0_SA_CVO. **Date:** 2026-07-09. **Status:** authoring in progress -- benchmark row +
value-check designed; SEV2 census + row-write (AE-converged) + BMKAUD replay = remaining.
**Unblock:** TO-2 COMPLETE (0.7.0_AE, 2026-06-16) -- `globgrph.graph_contracts` EXISTS on Nessie main
(13-field §3 schema, 0 rows). TO-3 (this) is the active long pole; the COO closeout
(`ratify-rows-flip-enforcement`) depends on it.

## Phase 1 -- scope ceiling verified (comp-surface-check list, 0 drift)

SEV1 = {model_portfolios.headline, model_portfolios.benchmark, advisor_intelligence};
SEV2 = {model_portfolios.peers, model_portfolios.aum}. Exactly the §9 v1 ceiling. (The 6th surface
`compilerkit.promote_seam` is out of GCONTR scope.) Author exactly these 5, stop there.

## Row 1 -- `benchmark-model-portfolios` (SEV1) -- authored, ratified_by HELD for Andrew

From the fully-worked seed (`period-contracts-seed-benchmark-20260615.md`), §9-updated: the seed's
`ratified_by:[CTO,COO]` is SUPERSEDED by §9 (Andrew-direct 2026-06-16: SEV1 = Andrew-only). Schema-conformant
to the RATIFIED §3 (13 fields, `active` BOOLEAN, `contract_id` required, `period_defs` MAP / `enforcement`
STRUCT / ARRAY types):

```yaml
contract_id: benchmark-model-portfolios
surface: "critical-surfaces:model_portfolios.benchmark (SEV1) | pipescript:model-portfolios/yang-benchmarks-etf-returns"
artifact_keys:
  - s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json
  - s3://opal-data-portal-v2/json/benchmarks/benchmark_returns.json
  - s3://opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json
  - s3://opal-data-portal-v2/json/benchmarks/etf_returns.json
canonical_writer: yang-pipeline-lambda-role
canonical_producer: "yang-model-portfolio-benchmarks (ProcessBothPKLs branch)"
source_of_truth: "s3://opal-data-portal-v2/benchmarks/data_YYYYMMDD_v1.pkl  # Yang PKL (BMKAUD WS-1)"
period_defs:
  "1D": "prior-trading-day -> as-of"
  "WTD": "week-start(Mon) -> as-of"
  "MTD": "month-start -> as-of (PARTIAL current month)"
  "1M": "trailing-1-calendar-month -> as-of"    # NOT last-complete-calendar-month = the SmartX violation
  "1Q": "trailing-3-calendar-months -> as-of"
  "YTD": "year-start -> as-of"
  "1Y": "trailing-365-CALENDAR-days, TOTAL return (incl dividends)"
  "3Y": "trailing-3Y, annualized"
  "SI": "since-inception, annualized"
  "_rfr_tenor": "duration-matched: UST/ST=1Y, INT=5Y, LTC/LTA=10Y"
  "_return_basis": "TOTAL return (dividends incl) + calendar-day arithmetic"
models: [UST, ST, INT, LTC, LTA]
forbidden_writers:
  - smartx-model-monthly-pull        # ROOT CAUSE: 1M=last-complete-calendar-month != contract
  - opal-generate-benchmark-returns  # EC2 smartx-exporter dual-writer (dormant)
  - smartx-ingestion-role            # latent (BMKAUD writer census)
  - news-pipeline-role               # latent (BMKAUD writer census)
enforcement:
  iam_backstop: "DenyNonYangWriteBenchmarks on opal-data-portal-v2/json/benchmarks/* (b1a3543c9)"
  surface_gate: "comp-surface-check SEV1 (model_portfolios.benchmark)"
  value_check:  "period_defs value-check (below) -- codifies BMKAUD WS-2"
ratified_by: [ PENDING-ANDREW ]     # SEV1 tier §9 -- HELD; the authorizing Nessie commit -> ratified_at
ratified_at: "<PENDING: the Andrew-authorized Nessie commit that lands this row>"
status: active
```
**§9 gate:** this row is NOT written-as-ratified until Andrew's sign-off is recorded in `ratified_by` +
the authorizing commit in `ratified_at` (Phase-2 hard constraint). Content is CVO-attested + schema-conformant;
only the ratification is held.

## The period_defs value-check (CVO-owned, §9 value limb) -- DESIGN

The assertion that runs a SERVED column against its `period_defs` -- independent of who wrote it (PRD §3.3);
the codified WS-2 benchmark-truth-audit. For the benchmark row:
1. Read the served `model_portfolio_benchmarks.json` (+ `benchmark_returns.json`) -> the `1M` column per model.
2. Recompute `1M` from the source-of-truth basis: **trailing-1-calendar-month, TOTAL return** (as-of -> as-of
   minus 1 calendar month), from the underlying returns (the Yang PKL / etf_returns).
3. VIOLATION iff `served_1M` != `recomputed_trailing_1M` within tolerance AND matches the
   `last-complete-calendar-month` signature (the SmartX override's window) -- the exact BMKAUD break.
4. Fires LOUD; an uncontracted SEV1 surface reads `unreviewed` (never silently "fine").
Generalizes to every `period_defs` entry (each column's window is the assertion). Implementation homes on
`comp-validate` / the benchmark period-def test. **Falsifiability bar (Phase-3 BMKAUD replay):** inject a
`last-complete-calendar-month` 1M into the served column -> the value-check MUST flag it; inject a correct
trailing-1M -> MUST pass.

## Remaining (the focused pass)

- **SEV2 census (peers, aum) + SEV1 census (headline, advisor_intelligence):** canonical_writer / producer /
  artifact_keys / period_defs per surface (peers/aum are the AUM + peer panels; headline the top-line;
  advisor_intelligence the NNA canonical). comp-pipescript io + comp-surface-check watch-files per surface.
- **Row-write path:** converge with 0.7.0_AE on the pyiceberg-on-Nessie-main write (the `_ensure` never
  overwrites CVO rows; need the append path + the Nessie catalog). Rows + AE's Q2 JOIN must agree on field usage.
- **Ratification:** SEV1 (benchmark/headline/advisor_intelligence) -> Andrew via COO; SEV2 (peers/aum) -> CTO+COO.
- **Phase-3 BMKAUD replay** with TO-2's Q2 (joint acceptance): synthetic SmartX write -> UNSANCTIONED;
  non-trailing 1M -> value-check flags. End-to-end BMKAUD-catch.
