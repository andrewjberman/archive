# OPAL_ANALYST TO-4a — Model Portfolios artifact census, complete findings (/draw)

Census: `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/census/ARTIFACT_CENSUS_MP.yaml` @0c1dae3da
Grounded live 2026-08-10 (portal_lookup COMPLETE walks + portal DEV tree + comp-routes + comp-estate).
For Andrew's structuring review — verticals 2-4 (Pod-2, Macro, News) gate on this structuring.

```
MODEL PORTFOLIOS VERTICAL — every served artifact, its visual coordinates, and its fields
DENOMINATOR: 482 S3 keys swept COMPLETE = platinum/mdpf(464) + json/mdpf(10)
+ json/benchmarks(6) + json/peers(1) + json/yang(1)
= 7 RENDERED artifact types + 9 unrendered/frozen row-groups (nothing elided)

1. The serving plane — how each artifact is produced, stored, and routed to the page

   PRODUCERS                 S3 STORE (opal-data-portal-v2)      CF ROUTE                 PAGE FETCH
   ─────────                 ──────────────────────────────      ────────                 ──────────
  ┌──────────────────────┐   ┌───────────────────────────────┐
  │ opal-assets-mdpf-    │   │ platinum/mdpf/{scope}/        │  /api/general/mdpf/      getAUMMetricsByFirm
  │ portal-publisher     │──►│   aum-metrics.json            │──── rewrite ────────────► getAccountDistributionByFirm
  │ (daily; scopes:      │   │   account-distribution.json   │  -> platinum/mdpf/       getMdpfAggregateAUATimeSeriesByFirm
  │  global, 49financial,│   │   aggregate-aua-timeseries.   │  (comp-routes rewrites,  (endpoints/aum.ts:520-612,
  │  inflection,         │   │       json                    │   live 2026-08-10)        portal-proxy.ts:523)
  │  cottonwood)         │   │ vintage: _provenance.source_  │
  │ upstream: mdpf-daily │   │  vintages / as_of_last        │
  │ convergence chain    │   │  (2026-08-05/06 live)         │
  │ (comp-estate mdpf)   │   ├───────────────────────────────┤
  │                      │   │ platinum/mdpf/ ALSO holds:    │   (no route — see plane 3)
  │                      │──►│  archive/** x444 FROZEN       │
  │                      │   │  _manifests/** x6 ops         │
  │                      │   │  global/non-model-assets.json │
  │                      │   │  cottonwood/account-units.json│
  └──────────────────────┘   ├───────────────────────────────┤
  ┌──────────────────────┐   │ json/benchmarks/              │  /api/general/ -> /json/  getModelPortfolioBenchmarks
  │ YangDataPipeline     │   │   model_portfolio_benchmarks. │──── rewrite ────────────► getETFBenchmarkReturns
  │ (Step Functions;     │──►│       json                    │                           getModelPortfolioTimeseries
  │  fires on PKL upload │   │   model_portfolio_timeseries. │                           (portal-proxy.ts:826/858/889)
  │  manifest; branches  │   │       json                    │
  │  yang-model-portfolio│   │   etf_returns.json            │
  │  -benchmarks +       │   │   benchmark_returns.json      │   (NO frontend caller)
  │  yang-generate-etf-  │   │   _smartx_model_{daily,       │   (internal views)
  │  returns)            │   │       monthly}.json           │
  │                      │   │ vintage: data_as_of           │
  │                      │   │  (2026-08-07 live)            │
  └──────────────────────┘   ├───────────────────────────────┤
  ┌──────────────────────┐   │ json/peers/                   │  /api/general/ -> /json/  getPeerPerformance
  │ yang-generate-peer-  │──►│   peer_performance.json       │──── rewrite ────────────► (portal-proxy.ts:934;
  │ performance (gated   │   │ vintage: data_as_of           │                           month-end cadence is
  │ on peer Excel upload)│   │  (2026-07-31 live = NORMAL)   │                           NORMAL, not stale)
  └──────────────────────┘   └───────────────────────────────┘

2. The visual plane — where every artifact appears on /model-portfolios (page -> location -> panel -> artifact -> fields)

   PAGE /model-portfolios (portal/src/pages/ModelPortfolios.tsx)
   │
   ├─ HEADER: "Page header + Portfolio Analytics summary"
   │   └─ PANEL "Portfolio Analytics" (:1226-1646)
   │       │  left partition "{AUA} by Model" donut (:1241) · right partition "Client
   │       │  Holdings" histogram (:1500) · footer source-attribution + dataAsOf (:1634)
   │       ├─ ARTIFACT platinum/mdpf/{scope}/aum-metrics.json          [live]
   │       │    fields: by_model[7]{model_name, aum USD (e.g. 51,737,347.29),
   │       │            account_count (e.g. 186), q0..q3{change,growth,priorLevel}},
   │       │            _provenance.source_vintages (role: vintage, 2026-08-05)
   │       ├─ ARTIFACT platinum/mdpf/{scope}/account-distribution.json [live]
   │       │    fields: by_model{7}{account_count 2028, active_accounts_count 2040,
   │       │            excluded_unfunded_count 12, histogram{bin_labels[20] "$1K-$2K",
   │       │            bins[21], counts[20]}, min/max/mean/median USD,
   │       │            percentiles p10-p95}, vintage 2026-08-06
   │       └─ ARTIFACT platinum/mdpf/{scope}/aggregate-aua-timeseries.json [live]  <== CANONICAL
   │            fields: dates[448] 2024-11-01..2026-08-05, as_of_last (role: vintage),
   │                    model_aua / non_model_aua / opal_aggregate_aua USD series
   │                    (e.g. 795,389,602.69), account_count_total[448] (e.g. 2826),
   │                    by_model{9 cohorts}{display_name, cohort_class model|sma,
   │                    account_count[], model_value[]}, cohort_provenance[448]
   │                    (measured|absent per partner), count_as_of/count_basis/
   │                    point_class lineage arrays, meta{22}, source_vintage_last{8}
   │
   ├─ TAB "Growth" (label dynamic: assetLbl.short, e.g. "AUA")
   │   └─ PANEL "{AUA} Trend Analysis" (:1713; sub-charts "Period End Summary" :1752
   │       │    stacked bars + "Daily {AUA} Analysis" :2000; Global=since-inception,
   │       │    per-firm=rolling-1Y; value-basis ONLY — count toggle REMOVED
   │       │    Andrew-direct 2026-07-29 @72f132c5)
   │       └─ pointer -> aggregate-aua-timeseries.json (canonical above; same family)
   │
   ├─ TAB "Benchmark" (id: performance)
   │   ├─ PANEL "Return vs Volatility" multi-view: Rolling Sharpe / Upside-Downside
   │   │   │    Capture / Maximum Drawdown (ReturnVolatilityScatter.tsx:80-95,
   │   │   │    mounted :2263)
   │   │   ├─ ARTIFACT json/benchmarks/model_portfolio_timeseries.json [live]
   │   │   │    fields: timeseries[2970]{date, model_code, model_return,
   │   │   │            benchmark_return, index_benchmark_return, etf_benchmark_return
   │   │   │            (decimal, e.g. -0.009261)}, rfr_tenors{5} (UST:1Y..ULT:10Y),
   │   │   │            series_note "Yang model-DESIGN series", data_as_of 2026-08-07
   │   │   └─ pointer -> model_portfolio_benchmarks.json (props; canonical below)
   │   ├─ PANEL "Benchmark Comparison" (:2273; net-of-36bps spreads; internal-only
   │   │   │    benchmark-type toggle SHOW_BENCHMARK_TOGGLE)
   │   │   ├─ ARTIFACT json/benchmarks/model_portfolio_benchmarks.json [live]  <== CANONICAL
   │   │   │    fields: models[5]{code UST.., name, returns{10 periods}{model 0.1,
   │   │   │            model_source yang_design, index_benchmark, etf_benchmark,
   │   │   │            index_spread, etf_spread, model/index/etf volatility}},
   │   │   │            periods[10] 1D.., inception 2024-04-30, data_as_of 2026-08-07
   │   │   └─ ARTIFACT json/benchmarks/etf_returns.json [live]
   │   │        fields: etfs{5: BIL/AGG/IVV/..}{name, asset_class,
   │   │                returns{9 periods} pct (e.g. BIL 1D 0.03)}, data_as_of 2026-08-07
   │   └─ PANEL "Data Source" (:2381) — static SmartX note, renders NO served artifact
   │
   └─ TAB "Peers"
       └─ PANEL "Peer Performance Comparison" (PeersTab.tsx:404)
           └─ ARTIFACT json/peers/peer_performance.json [live]
                fields: models{5}{code, name, periods{6: 1M/QTD/1Q/YTD/1Y/SI}
                        {model 0.1654, benchmark 0.1448, peer_percentiles
                        p5/p25/p50/p75/p95}}, data_as_of 2026-07-31 (month-end basis)

3. The residue plane — served-but-unrendered (MECE completion; every row has evidence)

   ┌────────────────────────────────────────────┬────────┬──────────────────────────────────────────┐
   │ ARTIFACT                                   │ STATE  │ WHY IT HAS NO PANEL (evidence)           │
   ├────────────────────────────────────────────┼────────┼──────────────────────────────────────────┤
   │ json/benchmarks/benchmark_returns.json     │ live   │ zero frontend callers (grep: only its    │
   │                                            │        │ portal-proxy.ts:757 definition)          │
   │ json/benchmarks/_smartx_model_daily.json   │ live   │ underscore internal view, no caller      │
   │ json/benchmarks/_smartx_model_monthly.json │ live   │ same class                               │
   │ platinum/mdpf/global/non-model-assets.json │ live   │ page reads non_model_aua from canonical  │
   │                                            │        │ timeseries; legacy fetch RETIRED         │
   │                                            │        │ (ModelPortfolios.tsx:530; proxy:414 off) │
   │ platinum/mdpf/cottonwood/account-units.json│ live   │ zero portal callers (grep: none)         │
   │ platinum/mdpf/_manifests/** (6)            │ live   │ publisher run-manifests (ops metadata)   │
   │ platinum/mdpf/archive/** (444)             │ FROZEN │ archived Andrew 2026-08-06; allowlist    │
   │  incl. underscore twin + etf_ownership x4  │        │ NOT-servable rows                        │
   │ json/mdpf/** (10)                          │ FROZEN │ legacy pre-platinum-flip tree; CF        │
   │                                            │        │ rewrite bypasses it (live 2026-08-10)    │
   │ json/yang/volatility_data.json             │ FROZEN │ frontend-orphan, superseded by           │
   │                                            │        │ json/macro/ twin (comp-estate MA-08)     │
   └────────────────────────────────────────────┴────────┴──────────────────────────────────────────┘

  The census ↔ street-address analogy is exact and deliberate:
  ┌───────────────────────────┬────────────────────────────────────────────────────┐
  │  census level             │  what the concierge can now cite                   │
  ├───────────────────────────┼────────────────────────────────────────────────────┤
  │ page (/model-portfolios)  │ the city — which surface the number lives on       │
  │ location (header/tab)     │ the street — where in the nav the user looks       │
  │ panel (visual container)  │ the building — the chart/table they are seeing     │
  │ artifact (S3 key)         │ the deed — the exact served object to quote        │
  │ field (+unit +example)    │ the room — the datum, citable with its vintage     │
  └───────────────────────────┴────────────────────────────────────────────────────┘

ANSWER back in the concierge's vocabulary, post-census:
  "Global aggregate AUA is $795,389,602.69 as of 2026-08-05 — from
   platinum/mdpf/global/aggregate-aua-timeseries.json (opal_aggregate_aua, latest
   point), shown on /model-portfolios -> header -> Portfolio Analytics."
```

The serving plane tells the freshness story (every artifact's producer, vintage field, and live value — the two vintage regimes are explicit: `data_as_of` on the Yang set, `_provenance.source_vintages`/`as_of_last` on the MDPF platinum set, which carries **no** top-level `as_of_date`). The visual plane tells the citation story: every number the concierge serves now has a full visual+data address down to field, unit, and a live example. The residue plane tells the honesty story — the 9 served-but-unrendered row-groups (2 of them frozen trees totaling 454 keys) are enumerated with the evidence for why they render nowhere, so this census's MECE claim is checkable, not asserted.

## Structuring-review notes for Andrew (grammar feedback from the pilot)

1. **The 8.1 skeleton has no home for a served-but-unrendered artifact.** The labeled
   `unrendered_artifacts` section (residue plane above) is this pilot's honest completion —
   your call whether it becomes part of the grammar for verticals 2-4.
2. **Scope-family dedup:** the 3 platinum types are published x4 scopes with identical
   schemas; the census carries ONE field list per type (grounded on global) + a
   `scope_family` list, rather than 12 near-identical entries.
3. **Vintage is not uniform:** Yang artifacts carry `data_as_of`; MDPF platinum artifacts
   carry provenance-block vintages only. If the registry (§8.2 `census_ref`) assumes one
   vintage field name, it will mis-cite half the vertical.
4. **One sub-panel ambiguity:** panels with internal partitions/sub-charts ("Portfolio
   Analytics" left/right; "Trend Analysis" two charts) are censused as ONE panel with the
   partitions named in render_evidence — adding a 6th level would violate rule 1 as ruled.
