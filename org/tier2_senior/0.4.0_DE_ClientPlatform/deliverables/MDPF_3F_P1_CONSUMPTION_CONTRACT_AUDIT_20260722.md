# 3F-P1 — MDPF Consumption Contract Audit (COMPLETE locus table)

- **TO:** MDPF_3FIRMS.3F-P1 (COO GO 20260722T203302Z) — READ-ONLY audit, zero FE modifications.
- **Auditor:** 0.4.0_DE_ClientPlatform
- **Vintage (all citations resolve here):** portal DEV @ `08c6d8b2` · workspace @ `1c42b3fd9` · audited 2026-07-22T20:45Z
- **Page:** `portal/src/pages/ModelPortfolios.tsx` (2,276 lines, read in full) + `ModelPortfolios/tabs/PeersTab.tsx` (props-only, fetches nothing) + `components/AccountDistribution{Chart,Metrics}.tsx` + `components/BenchmarkHeatmap.tsx`.

## DENOMINATOR

- **Data sources: 9 of 9 query hooks mapped** (the page's complete fetch surface — verified by grep `useQuery|fetch(|apiRequest` over the full file: 9 hooks, zero direct fetches; PeersTab receives props).
- **Rendered aggregates: 22 of 22 enumerated aggregates mapped** (A1–A14 Portfolio Analytics panel, T1–T4 trend charts, B1–B3 Benchmark tab, P-1 Peers tab). Every rendered number on the page traces to a row below. Presentation-only formatting (currency/date format, colors, ordering) is excluded by the §3.4 definition.

## VERDICT ON ANDREW'S QUESTION ("I suspect it is all client-side")

**MIXED — per aggregate, not in aggregate.** The suspicion is REFUTED for the artifact layer (every input is a served artifact; nothing is fetched row-level and aggregated from raw data) but CONFIRMED for specific load-bearing Global numbers: the Global headline Total, the Global trend aggregate as rendered, the Global deep-tail Non-Model band, Q-end prior levels, sleeve-level holdings, and unfunded counts are all FE-computed on top of served series. Each is itemized with a P5 flag below.

## PART 1 — Served-artifact inventory (the 9 hooks → 14 concrete endpoints)

| # | queryKey | Endpoint (live URL family) | Served key (current serving: opal-data-portal-v2 via CF behavior `/api/general/*`) | Producer (source-confirmed) |
|---|---|---|---|---|
| S1 | `['mdpf-per-firm-timeseries', firmId]` | `/api/general/mdpf/{firmId}/aggregate-aua-timeseries.json` (49financial · inflection · cottonwood) | `json/mdpf/{firmId}/aggregate-aua-timeseries.json` | `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` on mdpf-daily-runner EC2 (`mdpf-daily-dispatch.sh`; trigger = `mdpf-daily-trigger` lambda on INF spine sentinel) — pipescript `mdpf-global-view` |
| S2 | `['mdpf-aggregate-timeseries','global']` | `/api/general/mdpf/global/aggregate-aua-timeseries.json` | `json/mdpf/global/aggregate-aua-timeseries.json` | same as S1 |
| S3 | `['mdpf-per-firm-distribution', firmId]` | `/api/general/mdpf/{firmId}/account-distribution.json` | `json/mdpf/{firmId}/account-distribution.json` | `data/smartx/scripts/compute_per_firm_account_distribution.py` |
| S4 | `['aum-metrics']` | `/api/general/portfolios/aum-metrics.json` | `json/portfolios/aum-metrics.json` | SmartX exporter EC2 pipeline (`data/smartx/`, `SMARTX_BIBLE.md:291`; `infra/aws/ec2/smartx-exporter/ai-supervisor.py:132` reads it as its own freshness check) |
| S5 | `['aum-timeseries']` | `/api/general/portfolios/aum-timeseries.json` | `json/portfolios/aum-timeseries.json` | `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` (`LEGACY_AUM_KEY :54`); revamp sibling `dim_mdpf_aum_timeseries.py` stages `gold/mdpf_revamp/portfolios/aum-timeseries.json` (NOT served — publisher HELD, S5 flip rolled back per LD-0330) |
| S6 | `['account-distribution']` | `/api/general/portfolios/account-distribution.json` | `json/portfolios/account-distribution.json` | `data/smartx/scripts/compute_account_distribution.py` (`PORTAL_OUTPUT_KEY :81`) |
| S7 | `['non-model-assets']` | `/api/general/portfolios/non_model_assets.json` | `json/portfolios/non_model_assets.json` | `build_legacy_compat_emit.py` (`LEGACY_NM_KEY :55`; self-declares "sole SoT for non_model_assets.json" `:135`) |
| S8 | `['model-portfolio-benchmarks']` | `/api/general/benchmarks/model_portfolio_benchmarks.json` | `json/benchmarks/model_portfolio_benchmarks.json` | `yang-model-portfolio-benchmarks` lambda (Yang pipeline, ProcessBothPKLs branch) |
| S9 | `['etf-benchmark-returns']` | `/api/general/benchmarks/etf_returns.json` | `json/benchmarks/etf_returns.json` | `yang-generate-etf-returns` lambda |
| S10 | `['peer-performance']` | `/api/general/peers/peer_performance.json` | `json/peers/peer_performance.json` | `yang-generate-peer-performance` lambda (peer_excel-gated) |

No UNKNOWN PRODUCER rows — all 10 resolved with source citations.

## PART 2 — THE LOCUS TABLE (every rendered aggregate)

Legend: **SERVED** = number read from artifact and rendered; **FE-SELECT** = FE picks which served value (last-non-null, at-date lookup) but creates no number; **FE-COMPUTED** = FE arithmetic creates the number. `⚑P5` = FE-computed GLOBAL number flagged for 3F-P5 disposition.

### Portfolio Analytics panel

| ID | Rendered aggregate | Global locus | Per-firm locus |
|---|---|---|---|
| A1 | Donut per-model values | SERVED `metricsData.by_model[].aum` (+ FE blend-rollup `rollBlendsIntoArchetypeModels` `:673` — redistributes blend value 50/50 into archetypes, so displayed INT/LT values are **FE-COMPUTED when blends exist** ⚑P5-adjacent, see F-3) | FE-SELECT `lastNonNull(m.model_value)` `:617` over served series |
| A2 | Donut Non-Model slice | SERVED `nonModelData.latest.non_model_aum` `:978` | FE-SELECT `lastNonNull(non_model_aua)` `:968` |
| A3 | Donut center Total AUA | **FE-COMPUTED** `:886-890`: `trendLastPoint.aum + getNonModelAumForDate(...)` — and `trendLastPoint` itself reads the FE-summed T4 aggregate. Fallback: `modelAUM + nonModelData.latest`, where `modelAUM` = FE reduce `:856`. **⚑P5** | FE-SELECT `lastNonNullOrNull(partner_custody_total)` `:883-884`; all-null → `NOT_TRACKED` `:1206-1208` |
| A4 | AUMGrowthMetrics headline AUM | same as A3 (`aum: totalAUM` `:1399`) **⚑P5** | same as A3 per-firm (`aumNow` `:1364-1365`) |
| A5 | Account count tile | SERVED `metricsData.total.account_count` | SERVED `perFirmDistribution.total.account_count` `:1380` |
| A6 | Q0–Q2 quarterly growth tiles | change/growth SERVED (`metricsData.total.qN`); **priorLevel FE-OVERRIDDEN** `:1391-1393,:1401-1412` via `trendEnterpriseAt` `:1352-1356` = `getTrendAumForDate(agg,Q)` + `getNonModelAumForDate(...,Q)` — an FE-composed Global enterprise level per quarter **⚑P5** | **FE-COMPUTED** whole metric `qMetric` `:1366-1370`: priorLevel = `valueAtOrBeforeDate`, change/growth = FE arithmetic over served `partner_custody_total` |
| A7 | Total Holdings (sleeve-level headline) | **FE-COMPUTED** `totalHoldingsSleeveLevel` `:997-1004` = served distinct count + FE re-add of blend account counts **⚑P5** | same formula on per-firm distribution (blend keys absent for 49F → no-op) |
| A8 | Bell-curve histogram + p10/p25/median/p75/p90 | SERVED — `AccountDistributionMetrics.tsx:38-82` renders `data.percentiles.*`/`data.median` directly; zero FE math | SERVED (per-firm artifact) |
| A9 | Per-model distribution (donut-selected) | SERVED `activeDistribution.by_model[k]` (canonical-name join `:1452-1453`) | SERVED |
| A10 | Unfunded footer (per-model) | **FE-COMPUTED** `:1479`: `metricsData.by_model[].account_count − modelDistribution.account_count`; rendered Global-only by guard `:1486` **⚑P5** | suppressed by design (`:1486` guard — cross-scope subtraction was WRONG per-firm; TO-C) |
| A11 | Unfunded footer (total) | **FE-COMPUTED** `:1520`; Global-only guard `:1523` **⚑P5** | suppressed |
| A12 | Count-mode footer unfunded | **FE-COMPUTED** `:1916` (same subtraction, `distributionData` global) **⚑P5** | n/a (global data) |
| A13 | `dataAsOf` spine stamp | FE-SELECT `:587-590`: `globalMdpfData.as_of_last` → fallback last legacy period | FE-SELECT `perFirmMdpfData.as_of_last` |
| A14 | `spineIsStale` divergence notice | FE-COMPUTED boolean `:1013-1018` (two served timestamps, >3-day lag) — presentation guard, creates no financial number | same |

### Trend charts (Growth tab)

| ID | Rendered aggregate | Global locus | Per-firm locus |
|---|---|---|---|
| T1 | Trend aggregate line/total (incl. tooltip "Total AUA" and `trendLastPoint` feeding A3) | **FE-COMPUTED** `:724-731`: per-date SUM of served per-model `model_value` — the served artifact carries `model_aua` and `opal_aggregate_aua` fields but the rendered aggregate is re-summed client-side (code comment `:717` asserts `== model_aua`). Tooltip total = FE reduce over payload `:910`. **⚑P5 — a served equivalent EXISTS; re-point or document-deliberate.** | SERVED `partner_custody_total[i]` `:687` (tooltip total still FE reduce `:910`) |
| T2 | Per-model trend series | SERVED `model_value` per date, + FE blend-rollup `rollBlendsIntoArchetypeSeries` `:794-797` (blend value 50/50-split into archetypes → displayed INT/LT series FE-adjusted where blends exist) | same mechanism `:696-703` |
| T3 | Non-Model band | Three branches `:1800-1816` / `:1953-1968`: deep tail (<2026-01-16) **FE-COMPUTED** `opal_aggregate_aua − model_aua` `:1063-1073` **⚑P5**; calibrated region = FE roll-forward of SERVED `non_model_assets.time_series` (`getNonModelAumForDate` `:344-362`); honest-none dates suppressed via served `meta.honest_none` marker `:1058-1061` | SERVED `non_model_aua[i]` direct `:1025-1034` |
| T4 | Count trend | SERVED `account_count` per model (global = cross-partner-union counts from `globalMdpfData` `:756-770`) | SERVED `account_count[i]` `:702` |

### Benchmark tab

| ID | Rendered aggregate | Locus |
|---|---|---|
| B1 | Model/benchmark returns + spreads (gross) | SERVED `model.returns[period]` (FE selects index-vs-ETF variant `:837-843` — selection, not creation) |
| B2 | **Net** returns + net spreads | **FE-COMPUTED** — `BenchmarkHeatmap.tsx:85-104,:312-315,:396,:460`: `net = gross − 36bps × trading_days/252` (documented Yang formula). Not a Global-AUA composition; flag as documented-deliberate candidate, not a P5 violation |
| B3 | Return-vs-volatility scatter | SERVED (model/benchmark returns + volatility fields; FE variant selection only) |

### Peers tab

| ID | Rendered aggregate | Locus |
|---|---|---|
| P-1 | Peer percentile comparisons | SERVED `peer_performance.json` via `PeersTab` props (component fetches nothing, computes no aggregates) |

## PART 3 — 3F-P5 FLAG LIST (FE-computed GLOBAL numbers, per §3.4)

1. **Global headline Total AUA** (A3/A4, `:886-890`) — FE sum of FE-summed trend last bar + roll-forward non-model. Served candidate: `opal_aggregate_aua` last value (already in S2 artifact).
2. **Global trend aggregate as rendered** (T1, `:724-731`) — FE re-sum of per-model series despite served `model_aua` in the same artifact. **This refines PRD §2.4: "the Global TREND is server-composed" is true of the ARTIFACT but not of the RENDERED number.**
3. **Global deep-tail Non-Model band** (T3, `:1063-1073`) — FE `opal_aggregate_aua − model_aua` per date (<2026-01-16).
4. **Q-end enterprise priorLevels** (A6, `:1352-1356`) — FE composition of two served series at quarter-ends.
5. **Sleeve-level Total Holdings** (A7, `:997-1004`) — FE blend re-add on served distinct count.
6. **Unfunded counts** (A10/A11/A12, `:1479,:1520,:1916`) — FE cross-artifact subtraction (metrics − distribution).
7. **Blend rollups** (A1/T2, `rollBlendsIntoArchetypeModels/Series`) — FE 50/50 redistribution changes per-model displayed values (aggregate invariant).

Non-Global FE computations (documented, not P5 class): per-firm growth `qMetric` `:1366-1370`; per-firm last-non-null selections; net-of-fee benchmark returns (B2).

## PART 4 — Instrument findings (two enumerations disagreeing = the finding)

- `comp-transform fields ModelPortfolios` returned **7 field paths of the ≥40 actually bound** (missed all mdpf/per-firm/benchmark/peer hooks). `schema-check` found no co-located types.ts (types live in `portal-proxy.ts`/`endpoints/aum.ts`). Recorded as tool coverage gaps; audit denominator taken from the full-file walk instead.
- `comp-platinum page ModelPortfolios` traced **2 of 9 fetches** and resolved `getAccountDistribution` to `/api/private/portfolios/account-distribution.json` — that is the **commented-out TODO** in `aum.ts:517/549-551`; the live call is `/api/general/...` at `aum.ts:552`. The tool read the docstring, not the call. Same mis-read in `comp-routes trace ModelPortfolios`. **Do not trust comp-platinum/comp-routes URL columns for this endpoint until fixed.**
- `pipescript model-portfolios` covers the Yang/benchmark legs only; the AUA legs live in `pipescript mdpf` — the page spans two named threads.

## Cross-checks

- Reconciled with 3F-P2 route table (sibling deliverable, committed together): all 14 endpoints resolve to CF behavior `/api/general/*` (behavior 18) → S3 `opal-data-portal-v2` via `public-data-router` rewrite; zero orphan endpoints.
- Circulating to 0.4.0_DS per TO cross-domain note: this table defines what gold must produce (3F-G3/G4/G8 input).
