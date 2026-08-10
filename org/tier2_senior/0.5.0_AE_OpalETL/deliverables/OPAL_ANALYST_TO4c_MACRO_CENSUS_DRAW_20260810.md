# OPAL_ANALYST TO-4c — Macroeconomics artifact census, complete findings (/draw)

Census: `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/census/ARTIFACT_CENSUS_MACRO.yaml` @5efce36b7
Grounded live 2026-08-10. Vertical 3 of 4, ratified pilot grammar. ALL panel evidence first-hand
(COO discipline flag honored — no subagent evidence). Informational delivery, gate discharged.

```
MACROECONOMICS VERTICAL — one page, two tabs, one 84-key channel
DENOMINATOR: json/macro/ 84 keys (COMPLETE walk) = 5 top-level + 79 timeseries/{slug}
= 4 RENDERED artifact types + 2 unrendered keys + 1 frozen adjacent + 1 borrowed ref

1. The serving plane — TWO producer families feed one channel, three vintage clocks

   PRODUCERS                       S3 (opal-data-portal-v2/json/macro/)   PAGE FETCH
   ─────────                       ────────────────────────────────────   ──────────
  ┌──────────────────────────┐    ┌─────────────────────────────────┐
  │ yang-generate-macro      │───►│ macro_data.json 197KB           │──► getMacroData (proxy:1750)
  │ (yang pipeline, PKL-     │    │   data_as_of 2026-08-07         │    FETCHED TWICE (heatmap
  │ driven; comp-estate      │    │                                 │    useEffect + YieldCurve tab,
  │ FRED-04)                 │    │                                 │    no shared cache -- smell)
  │ yang-generate-macro-     │───►│ timeseries/{slug}.json x79 GZIP │──► getMacroTimeSeries
  │ timeseries (FRED-05)     │    │   as_of 2026-08-07 (** field    │    (endpoints/macro.ts:26-28;
  │                          │    │   is as_of, NOT data_as_of --   │    LAZY, per indicator click
  │                          │    │   3rd vintage-name variant **)  │    in the heatmap modal)
  ├──────────────────────────┤    ├─────────────────────────────────┤
  │ fred-data-ingestion      │───►│ yield_curve_fred.json 675KB     │──► getYieldCurveData
  │ (daily cron 23:00Z;      │    │   data_as_of 2026-08-05         │    (endpoints/yield-curve.ts:48;
  │ FRED-01)                 │    │   (FRED clock, not yang's)      │    1Y-ago leg, soft-fails null)
  │ opal-portal-volatility-  │───►│ volatility_data.json 1.4MB      │──► getVolatilityData (proxy:
  │ fetcher family (own      │    │   data_as_of 2026-08-06         │    1836; EAGER at page mount,
  │ cadence, gen 08-10       │    │   (VIX=FRED VIXCLS,             │    even on the other tab --
  │ 12:30Z)                  │    │    MOVE=Yahoo ^MOVE)            │    smell)
  ├──────────────────────────┤    ├─────────────────────────────────┤
  │ fred-macro-ingestion     │───►│ macro_data_fred.json 76KB       │    (NO portal consumer --
  │ (daily 23:30Z; FRED-02)  │    │   data_as_of 2026-07-01         │     STAGING twin, orphan)
  │ (yang pipeline)          │───►│ vix_data.json 787KB 08-06       │    (getVIXData: ZERO callers
  └──────────────────────────┘    └─────────────────────────────────┘     -- superseded, still published)

2. The visual plane — /macro (page -> location -> panel -> artifact)

   /macro ─ header (always-on, above tabs):
        ├ PANEL "Macroeconomic Indicators"               <- macro_data.json [CANONICAL]
        │    (hand-rolled container MacroHeatmap.tsx:136-143; Value/Position toggle;
        │     12 collapsible groups, ~73 indicators, cell = {value, percentile} per month)
        └ PANEL MacroTimeSeriesModal (drill-down         <- timeseries/{slug}.json [CANONICAL,
             overlay, untitled -- component name)            79-slug FAMILY] (lazy per click;
                                                             monthly history since 1990 + stats)
        ├ tab Yield Curve (default):
        │    PANEL "USD Treasury Yield Curve"            <- macro_data.json (pointer, Treasury
        │    (YieldCurveTab.tsx:289; Current/1M/1Y-ago      Yields group) + yield_curve_fred
        │     checkboxes; 2Y/10Y/30Y/2s10s StatCards)       .json [CANONICAL] (1Y-ago FRED leg)
        │    PANEL "Yield Changes (1M)" (:479)           <- macro_data.json (pointer)
        └ tab Volatility (id vix):
             PANEL "AI Analysis" (VolatilityTab.tsx:715, <- volatility_data.json [CANONICAL]
                VIX|MOVE toggle)                            (page-level eager fetch, props down)
             PANEL "{VIX|MOVE} Current Level" (:728)     <- volatility_data.json (pointer)
             PANEL "{VIX|MOVE} Historical Time           <- volatility_data.json (pointer)
                Series" (:746)

3. The residue plane

   ┌────────────────────────────────┬────────┬────────────────────────────────────────────┐
   │ ARTIFACT                       │ STATE  │ EVIDENCE                                   │
   ├────────────────────────────────┼────────┼────────────────────────────────────────────┤
   │ json/macro/macro_data_fred.json│ live   │ FRED-02 staging twin of macro_data.json —  │
   │                                │        │ frontend-orphan [CVO]; merge decision open │
   │ json/macro/vix_data.json       │ live   │ getVIXData has ZERO callers (first-hand    │
   │                                │        │ grep); superseded by volatility_data.json  │
   │                                │        │ yet STILL PUBLISHED daily — decommission   │
   │                                │        │ candidate for the record                   │
   │ market-metrics.json.gz         │ FROZEN │ 04-15 vintage; NEVER-serve-as-current row; │
   │  (bucket top level, adjacent)  │        │ allowlist routes row-4 queries at it       │
   └────────────────────────────────┴────────┴────────────────────────────────────────────┘

  The three-clocks analogy is exact and deliberate:
  ┌──────────────────────────────┬────────────────────────────────────────────────────┐
  │  producer clock              │  what "fresh" means on this page                   │
  ├──────────────────────────────┼────────────────────────────────────────────────────┤
  │ yang PKL pipeline (08-07)    │ heatmap + curves: T-1 vs the Bloomberg pull        │
  │ FRED daily crons (08-05/06)  │ 1Y-ago curve + volatility: FRED's own publish lag  │
  │ volatility fetcher (gen      │ gauge freshness: its fetch time, data still T-x    │
  │  08-10 12:30Z, data 08-06)   │ (generated_at is a RUN time, never the vintage)    │
  └──────────────────────────────┴────────────────────────────────────────────────────┘

ANSWER back in the concierge's vocabulary, post-census:
  "VIX is 15.15 — Normal regime, 34th percentile — as of 2026-08-06, from
   json/macro/volatility_data.json (vix.current, source FRED VIXCLS), shown on
   /macro -> Volatility -> VIX Current Level."
```

## Findings for the record (census-surfaced, none blocking)

1. **Third vintage-field variant:** the timeseries family stamps `as_of`, not `data_as_of`
   (adds to TO-4a's provenance-block variant and TO-4b's year-grain "2026" — the §8.2
   `census_ref` design now has THREE measured vintage-name regimes to absorb).
2. **Decommission candidate:** `vix_data.json` is superseded by `volatility_data.json`,
   has zero frontend callers (first-hand grep), and is still published daily — a standing
   twin of exactly the never-decommissioned class. Recorded, not touched (not my call).
3. **Smells banked:** `macro_data.json` fetched twice with no cache sharing (heatmap
   useEffect + YieldCurveTab useEffect); `volatility_data.json` fetched eagerly on page
   mount even when the Volatility tab is never opened.
```
