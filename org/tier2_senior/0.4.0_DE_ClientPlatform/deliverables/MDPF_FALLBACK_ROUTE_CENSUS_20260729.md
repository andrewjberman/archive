# MDPF PAGE FALLBACK-ROUTE CENSUS — 2026-07-29 ~0230Z
**Author:** `0.4.0_DE_ClientPlatform` · **Per:** Andrew-sovereign ~0200Z via CTO Amendment 3 (20260729T020253Z) + 0204Z cache clarification.
**Method (as ordered):** SOURCE-READ (denominator printed below) + FORCED-FAILURE exercise (canonical route blocked in the dev harness, render recorded). A runtime capture cannot find a fallback; none was used as evidence here.
**Page:** `portal/src/pages/ModelPortfolios.tsx` @ `d0fb493e` (post headline fix). Discriminator per 0204Z: *WHERE does the path get its bytes?* Cache-of-canonical = fine; wrong LOCATION = finding regardless of the value it serves.

## DENOMINATOR — every reachable route from the /portfolios page
The page imports fetchers from `src/api/endpoints/aum.ts` (wrappers) and `src/api/portal-proxy.ts` (direct). 10 fetch routes + 2 module caches + 5 in-page fallback/derivation branches + 1 zombie. Enumerated exhaustively from source; nothing sampled.

### A. CANONICAL routes (fine)
| # | Route | Bytes from | Note |
|---|---|---|---|
| A1 | `getMdpfAggregateAUATimeSeriesByFirm('global')` → `/api/general/mdpf/global/aggregate-aua-timeseries.json` | CF router v6 → `platinum/mdpf/global/` (tonight's WO-3 flip) | THE canonical read. Headline field-read consumes it. |
| A2 | same, per-firm (`49financial`/`inflection`/`cottonwood`) | `platinum/mdpf/{firm}/` | canonical family |
| A3 | `getAccountDistributionByFirm` → `/api/general/mdpf/{firm}/account-distribution.json` + 60-min module cache | mdpf namespace | cache-of-canonical = fine (0204Z) |
| A4 | `getAUMMetricsByFirm` → `/api/general/mdpf/{firm}/aum-metrics.json` + 60-min module cache (cottonwood-enabled only) | mdpf namespace | fine |
| A5 | react-query caches keyed `['mdpf-*']`, staleTime 5min | canonical responses | freshness knob, not a route (0204Z) |

**Census note (declarative drift, not a route defect):** `portal-proxy.ts:497-501` and `:515-519` still document the OLD serving chain ("publish copies platinum → json; serves from json/mdpf/*"). Post-flip the router serves platinum directly. Stale comments on the canonical route — doc fix rides the next change.

### B. NON-CANONICAL-LOCATION routes the page still consumes — FINDINGS
| # | Route | Bytes from | Global-view consumers |
|---|---|---|---|
| B1 | `getAUMMetrics` → `/api/general/portfolios/aum-metrics.json` | legacy `json/portfolios/*` | quarter dates; Q-cell change/growth; `account_count`; **donut model slices + per-model cards** (`metricsData.by_model`, `:688`) |
| B2 | `getAUMTimeSeries` → `/api/general/portfolios/aum-timeseries.json` | legacy | graceful-degrade Global trend branch (`:849-894`); Q-end priorLevels (`:1680-1685`); the page `isLoading` gate (`:612`) is keyed to THIS legacy route |
| B3 | `getNonModelAssets` → `/api/general/portfolios/non_model_assets.json` | legacy, **deprecated basis — the artifact behind the $1.91B** | Non-Model chart band (`:2168`, `:2403`); donut Non-Model slice (`:1303-1308`); footnote last-update (`:2777`); legend gating (`:1649`) |
| B4 | `getAccountDistribution` → `/api/general/portfolios/account-distribution.json` + 60-min module cache | legacy | Global bell curve + Total Holdings |
| B5 | `getModelPortfolioBenchmarks` → `/api/general/benchmarks/model_portfolio_benchmarks.json` · `getETFBenchmarkReturns` → `/api/general/benchmarks/etf_returns.json` · `getPeerPerformance` → `/api/general/peers/peer_performance.json` | non-mdpf namespaces | Benchmark + Peers tabs. **No canonical platinum location exists for these families** (design set = latest-per-(scope,type) of gold/mdpf). Server-side design question, CTO/COO to rule — reported, not fixed. |

### C. FALLBACK BRANCHES + CATCH-RENDERS — FINDINGS
| # | Shape | Location | Verdict |
|---|---|---|---|
| C1 | ~~`:1170-1171` composition + `:1172 .latest`~~ | headline | **DELETED tonight** (`d0fb493e`) — both branches, no graceful-degrade retained |
| C2 | `getAUMMetrics` **catch → fabricated zero structure** (`aum: 0, account_count: 0`) | `endpoints/aum.ts:388-413` | **a catch that renders a NUMBER instead of an error** — the named defect class verbatim. On metrics failure the donut/cards paint $0s |
| C3 | `getAUMTimeSeries` catch → empty-but-truthy structure | `endpoints/aum.ts:438-445` | silently defeats the `isLoading` error state — page renders "loaded" on a dead route |
| C4 | Global VALUE trend graceful-degrade onto legacy `rawTimeSeriesData` | `ModelPortfolios.tsx:849-894` | **THE route that painted legacy $1.78B during the 01:31–01:41Z 403 window** (DT's trace). Headline now immune; the CHARTS still take it — exercised live in the forced-failure control (screenshot: full trend renders from legacy while canonical is dead) |
| C5 | Zombie: `getMdpfAggregateAUATimeSeries()` (scope-less) | `portal-proxy.ts:505` + wrapper `endpoints/aum.ts:470` | **zero page callers, still callable** — dead code that can serve a number is a zombie route whether or not it fires. Duplicate-definition multiplicity too: `getAUMTimeSeries`/metrics families exist in BOTH portal-proxy and endpoints/aum (page uses the wrappers, which add C2/C3) |

### D. CLIENT DERIVATIONS remaining on the page (D1 forbidden class — census for the second change, per CTO sizing clause)
| # | Derivation | Location | Canonical field that should replace it |
|---|---|---|---|
| D1a | Q-end enterprise priorLevels: `trendAum + getNonModelAumForDate(...)` | `:1680-1685` | none exists per-quarter in platinum → **server-side gap, publisher/gold work** |
| D1b | trend aggregate line client-sums per-model `model_value` | `:828` | artifact's own `opal_aggregate_aua[]` / `model_aua[]` rows (EXIST — read them) |
| D1c | deep-tail Non-Model band: `oaa − model_aua` client subtraction | `:1392-1402` | server-emitted per-date non-model band field → gap |
| D1d | `getNonModelAumForDate` roll-forward carry logic | `:363` + call sites `:2168/:2403` | forbidden class ("roll-forward/carry"); non-model series should come from the canonical artifact's `non_model_aua[]` |
| D1e | tooltip total bucket-sum fallback | `:1212` | anchored `total_aua` row field exists; the fallback sums client-side on the legacy/global path |
| D1f | QoQ % in `AUMGrowthMetrics` computed from composed priorLevel | component `:92` region | percentage-of-server-total is presentation ONLY if both legs are server fields; today the prior leg is D1a |
| D1g | blend roll `rollBlendsIntoArchetypeSeries` redistribution | `:900` | value redistribution client-side; rule needed on whether presentation (regroup) or derivation (50/50 split arithmetic) |

## FORCED-FAILURE EXERCISE (dev harness, ui-smoke; screenshots in session scratchpad)
1. **All routes dead** (auth-stubbed harness, no fixtures): headline renders **"—"** (honest absence), quarters N/A, no fabricated dollars on the headline. PASS post-fix.
2. **Discriminating control — canonical dead, ALL FOUR legacy routes alive** (fixtures minus the platinum artifact): headline renders **"—"**; pre-fix code provably painted a composed legacy number in exactly this state. **PASS.** Same frame shows the charts/quarters/donut still rendering legacy numbers → C4/B1-B4 confirmed live by exercise, not inference.
3. **Happy path** (live platinum artifact as fixture): headline renders **$1.95B** — the field `opal_aggregate_aua[-1 real] = 1,950,519,805.86 @ 2026-07-27`, zero arithmetic to the pixel.

## SHIPS vs REPORTS tally
- **SHIPPED tonight (`d0fb493e`, DEV, pushed):** C1 deleted; headline = field read; honest-absence states.
- **REPORTED (this census):** B1–B5, C2–C5, D1a–D1g, the A-route stale comments. Boundary held per Amendment 3 — nothing outside the headline path was edited.
- **Second-change proposal (D1 remainder):** re-point charts/donut/quarters onto the canonical artifact's own arrays (D1b/D1d/D1e are field reads that EXIST today); D1a/D1c need server-side fields first (publisher/gold work — reported as gaps); then delete B1–B4 consumption and re-key `isLoading` (B2), C2/C3 catch-fabrications replaced with honest error states, C5 zombie deleted.
