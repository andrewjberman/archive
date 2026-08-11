# OPAL_ANALYST TO-4b — Pod-2 Analytics artifact census, complete findings (/draw)

Census: `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/census/ARTIFACT_CENSUS_POD2.yaml` @49cb88ead
Grounded live 2026-08-10 (portal_lookup COMPLETE walks + portal DEV tree + comp-estate). Vertical 2 of 4,
ratified pilot grammar. Informational delivery — the structuring gate is discharged (@95b3e2852).

```
POD-2 PORTFOLIO ANALYTICS VERTICAL — nav "Analysis" minus Macro: 6 pages, 17 panels
DENOMINATOR: 11 vertical-owned S3 keys (COMPLETE walks) across 5 prefixes — ALL 11 rendered
+ 4 frozen top-level legacy keys (residue) + 2 borrowed cross-vertical artifacts (referenced)

1. The serving plane — one Yang pipeline, five prefixes, one vintage regime (with two exceptions)

   PRODUCER                      S3 STORE (opal-data-portal-v2)     CF ROUTE (/api/general/ -> /json/)   PAGE
   ────────                      ──────────────────────────────     ──────────────────────────────────   ────
  ┌─────────────────────────┐   ┌────────────────────────────────┐
  │ YangDataPipeline        │──►│ json/valuation/      (2 keys)  │──► getValuationData / getRisk-      /valuations
  │ (Step Functions, fires  │   │   valuation_data.json 2.2MB    │    PremiumData (proxy:1481/1534)
  │ on PKL upload manifest; │   │   risk_premium_data.json       │
  │ branches per artifact — │   ├────────────────────────────────┤
  │ comp-estate threads:    │──►│ json/positioning/    (3 keys)  │──► getPositioningData (GZIP) /       /positioning
  │ valuation, positioning, │   │   positioning_data.json GZIP   │    getAllocationSummary (GZIP) /     /attribution
  │ correlation,            │   │   allocation_summary.json GZIP │    getHoldingsAttribution
  │ factor-tilts)           │   │   holdings_attribution_data.   │    (proxy:1085/1595/1701)
  │                         │   │     json (attribution_excel,   │
  │ vintage: data_as_of     │   │     MONTH-END cadence 07-31)   │
  │ 2026-08-07 on all       │   ├────────────────────────────────┤
  │ EXCEPT the two flagged  │──►│ json/correlations/   (1 key)   │──► getCorrelationData (proxy:1633)   /correlations
  │ below                   │   │   correlation_data.json        │
  │                         │   ├────────────────────────────────┤
  │                         │──►│ json/factor-tilts/   (3 keys)  │──► tiered lazy loads:                /factor-tilts
  │                         │   │   tier1-snapshot.json 10KB     │    tier1 EAGER (proxy:1299)
  │                         │   │   tier2-spreads.json 126KB     │    tier2 LAZY on tab (proxy:1312)
  │                         │   │   tier3-timeseries.json 3.7MB  │    tier3 LAZY on toggle (proxy:1325)
  ├─────────────────────────┤   ├────────────────────────────────┤
  │ yang-generate-cma       │──►│ json/capital-markets/ (2 keys) │──► getCMAAssumptions/getOpalViews    /cma
  │ (cma_excel-gated branch │   │   assumptions.json 03-11       │    (proxy:1370/1412)
  │ — INTERMITTENT by       │   │   views.json      01-09        │    ** PREFIX ABSENT from the
  │ design, fires on CMA    │   │   vintage: data_as_of "2026"   │    portal_lookup channel map —
  │ Excel upload)           │   │   (YEAR-grain!) / 2026-01-09   │    channel-map gap **
  └─────────────────────────┘   └────────────────────────────────┘
  BORROWED (owned elsewhere, rendered here): json/portfolios/aum-metrics.json (AGG weighting on
  /positioning, /attribution, /factor-tilts) · json/latest/manifest.json (SmartPanelFooter
  freshness on ALL 6 pages)

2. The visual plane — 6 pages, nav order (page -> location -> panel -> artifact)

   /cma ─ header: PANEL "10-Year Assumptions"            <- assumptions.json [CANONICAL]
        ├ tab Expectations: PANEL "Capital Market
        │                    Expectations"               <- assumptions.json (pointer)
        └ tab Views: PANEL "Views"                       <- views.json [CANONICAL]

   /positioning (no tabs)
        ├ PANEL "Positioning Summary"                    <- positioning_data.json [CANONICAL]
        │   (4-view toggle; matrix: Asset Class /           + holdings_attribution_data.json
        │    Mgmt Style / Characteristics / Sub-Cats)       [CANONICAL] (sub-categories section)
        ├ PANEL "Portfolio Composition" (treemap)        <- positioning_data.json (pointer)
        └ PANEL "Holdings Breakdown" (dense table)       <- positioning_data.json (pointer)
                                                            + aum-metrics.json (borrowed, AGG)

   /attribution (no tabs)
        ├ PANEL "Style vs Benchmark Positioning"         <- allocation_summary.json [CANONICAL]
        │   (+ inline "Asset Allocation Attribution")       + holdings_attribution (pointer)
        └ PANEL "Attribution Breakdown"                  <- holdings_attribution (pointer)
             (holdings-grain; chips exclude AGG)            + aum-metrics.json (borrowed, AGG)
        [page also fetches positioning_data.json for its data_as_of ONLY — no panel]

   /factor-tilts ─ header: PANEL "Factor Exposure
        │            Profile" (radar + regression)       <- tier1-snapshot.json [CANONICAL]
        │                                                   + aum-metrics.json (borrowed, AGG)
        ├ tab Portfolio Factors: PANEL "Factor Tilts
        │            by Portfolio" (bars | timeseries)   <- tier1 (pointer) + tier3-timeseries
        │                                                   .json [CANONICAL] (lazy 3.7MB)
        └ tab Factor Spreads: PANEL "Market Factor
                     Spreads"                            <- tier2-spreads.json [CANONICAL] (lazy)

   /valuations ─ header (2 always-on):
        ├ PANEL "Equity Valuation Summary - Latest
        │    Percentile" (39-index heatmap)              <- valuation_data.json [CANONICAL]
        ├ PANEL "{index} Valuation Range" (40 indices)   <- valuation_data.json (pointer)
        ├ tab Valuation Time Series: PANEL "{index} -
        │    {metric} Time Series" (ratio mode)          <- valuation_data.json (pointer)
        └ tab Risk Premium:
             PANEL "Equity Risk Premium" (ERP 1990-)     <- risk_premium_data.json [CANONICAL]
             PANEL "Credit Risk Premium" (IG/HY OAS)     <- risk_premium_data.json (pointer)

   /correlations (no tabs)
        └ PANEL "Correlation Matrix" (59x59, 5 periods)  <- correlation_data.json [CANONICAL]

3. The residue plane — frozen legacy + zero owned-unrendered

   ┌────────────────────────────────────────────┬────────┬─────────────────────────────────────┐
   │ ARTIFACT                                   │ STATE  │ EVIDENCE                            │
   ├────────────────────────────────────────────┼────────┼─────────────────────────────────────┤
   │ valuation/valuation_data.json (top-level)  │ FROZEN │ 2026-01-04 legacy copy; PORTAL_     │
   │                                            │        │ RETRIEVAL rule 3 prefix             │
   │ positioning/** top-level (3 keys)          │ FROZEN │ all 2025-12-23; etf_categories.json │
   │                                            │        │ exists ONLY in the frozen tree      │
   │ (owned-unrendered)                         │  --    │ NONE — all 11 owned keys render     │
   └────────────────────────────────────────────┴────────┴─────────────────────────────────────┘

  The tiered-load ↔ library-stacks analogy is exact and deliberate:
  ┌───────────────────────────┬────────────────────────────────────────────────────┐
  │  factor-tilts tier        │  what the reader pays for                          │
  ├───────────────────────────┼────────────────────────────────────────────────────┤
  │ tier1 10KB, eager         │ the front desk — summary always in hand            │
  │ tier2 126KB, lazy on tab  │ the reading room — fetched when you walk in        │
  │ tier3 3.7MB, lazy on      │ the archive stacks — retrieved only on request     │
  │   toggle                  │ (2.3MB -> 46KB default page load, by design)       │
  └───────────────────────────┴────────────────────────────────────────────────────┘

ANSWER back in the concierge's vocabulary, post-census:
  "The S&P 500 forward P/E is 20.09 — its 79th percentile vs the trailing window — as of
   2026-08-07, from json/valuation/valuation_data.json (ranges."S&P 500"[fwd_pe]), shown on
   /valuations -> header -> Equity Valuation Summary - Latest Percentile."
```

The serving plane tells the freshness story: one `data_as_of` regime (2026-08-07) across nine of
eleven artifacts, with the two exceptions named — holdings-attribution is month-end by design
(2026-07-31 is healthy), and the CMA pair is Excel-upload-gated (03-11/01-09 is its cadence, not
staleness). The visual plane gives every number a full address to field grain. The residue plane
is short because this vertical is clean: every owned key renders; only the pre-`json/` frozen
twins remain, plus one artifact (`etf_categories.json`) that exists ONLY in the frozen tree.

## Findings for the record (census-surfaced, none blocking)

1. **Channel-map gap:** `json/capital-markets/` is served and rendered but ABSENT from
   `portal_lookup.py` CHANNELS and the PORTAL_RETRIEVAL table — a catalog-row-3 question about
   CMA cannot currently be answered by the sanctioned mechanism. (Registry/DATA_CATALOG v0.2
   should add the channel; widening is Andrew's word.)
2. **Vintage anomaly:** `assumptions.json` `data_as_of` is the YEAR-grain string `"2026"`, not a
   date — a `census_ref`/vintage consumer that parses dates will choke on this one artifact.
3. **Smells (not defects, banked):** /positioning HoldingsTab re-fetches positioning_data via a
   bare useEffect OUTSIDE the React Query cache (duplicate fetch); /attribution's Breakdown
   fetches swallow errors silently; /valuations' risk-premium tab error block renders light text
   on the silver canvas outside a Panel (the documented #1 portal color defect class); CMA Views
   fetch failure renders a permanent loading state. All portal-lane items, none touched under
   exclusivity.
4. **Dead-path inventory:** /positioning period selector hard-pinned 'Current' (attribution +
   AUM non-Current paths dead); Attribution treemap component unmounted; 1Y period retained in
   types but commented out of UIs.
