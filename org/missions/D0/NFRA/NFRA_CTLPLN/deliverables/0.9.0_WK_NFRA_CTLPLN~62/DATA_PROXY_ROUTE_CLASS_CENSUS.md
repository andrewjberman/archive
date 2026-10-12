RULED: PRD v0.25 / msg 108445 -- class (i) routes stay open; class (ii) routes fence on tier
# DATA_PROXY_ROUTE_CLASS_CENSUS -- NFRA_CTLPLN TO-CT-u-6, AMENDMENT 1 step 1

Worker: 0.9.0_WK_NFRA_CTLPLN~62 (branch wk-NFRA_CTLPLN-62, worktree ctlpln-62, base HEAD 49af906f74).
Scope: every route the data-proxy handler matches, traced by reading portal/src (no portal build, no run).
Authority: PRD v0.24 FWD-28; the order's AMENDMENT 1 step 1.

ROUTES total=41

## 1. Denominator and method

- Handler: infra/aws/lambda/portal_data_proxy/lambda_function.py, lambda_handler, the matches
  `if http_method == '<VERB>' and path == '<p>'` and `... path.startswith('<p>')`.
  Enumerated by a regex over the file: 41 matches (40 GET, 1 POST). The CTO's figure of 11 is
  not the handler's route count (difference: 30). OPTIONS and `?warm=1` are returns before the
  route block, not routes, and are not in the 41.
- Prefix routes are written with a trailing `*` in the table and in route_pages.json.
- Portal reads: portal/src/api/portal-proxy.ts, portal/src/api/endpoints/*.ts, and every
  `apiRequest`/`publicApiRequest`/`fetch` literal under portal/src (tests excluded).
- Portal source version: `portal` is a gitlink in this repo, pinned at c96efe1714. The checkout on
  disk is at 2ed4373d (ahead of the pin). The files this census traces are identical to the pin
  (portal-proxy.ts, endpoints/sentiment.ts, endpoints/market.ts, endpoints/aum.ts, contexts/DataSourceContext.tsx,
  main.tsx, components/market-performance/*, pages/MarketPerformance/*, lib/firmAccess.ts) except App.tsx
  (the /market, /portfolios, /philosophy, /positioning, /valuations and /macro routes are unchanged at the pin).
  firmAccess.ts is byte-identical to the pin after LF normalisation (sha256 895ee782...). Surprise row
  NFRA_CTLPLN-W62-S5 records that the generator's input is a submodule checkout.
- URL routing (infra/aws/terraform/portal-auth/cloudfront-distribution.tf): `/v1/*` ->
  APIGateway-portal (the data proxy, lines 776-777); `/api/general/*` -> S3 JSON origin (709-711);
  `/api/private/*` and `/api/scoped/*` -> APIGateway-portal or S3 (not data-proxy routes);
  default -> S3-opalinvest-portal (line 273). vite.config.ts:57-66 states the same for the dev proxy.
- Result of the portal search: a data-proxy path is called from portal/src at ONLY five sites.
  Two of them sit in a module a page's import closure reaches (row 1 via /market; row 2 via the
  app-root provider, see section 4). Three sit in portal-proxy.ts or endpoints functions that no
  module imports (rows 3-5). Every other portal read of this data uses a `/api/general/*` S3 path.
- Production note: `portal/.env.production` sets `VITE_PORTAL_API_URL=` (empty). The un-prefixed
  calls (rows 3-5 and the DataSourceContext call) are therefore NOT under `/v1/*` and fall to the
  default S3 origin. Recorded as surprise row NFRA_CTLPLN-W62-S3. The class below does not depend on it.

## 2. FIRM_ALLOWED_PATHS (portal/src/lib/firmAccess.ts, read at HEAD)

Firm keys: 49financial, inflection, cottonwood, demo. `opal-capital` is INTERNAL_FIRM_ID and is
not a key (admitted by tier, not by the set). Partner paths in the union of the four sets:
/market, /portfolios, /advisor-intelligence, /philosophy, /positioning, /attribution, /factor-tilts,
/valuations, /macro, /trade-submission (10 paths). /market is in all four sets.
FIRM_EXEMPT_PATHS (/change-password) is not a firm set and carries no data route.

## 3. Route table

Columns: route | portal caller (client function, file:line) | importers under portal/src | App.tsx Route path | path in a firm set | class | firm union.

| # | route | portal caller | importers (page or shared component) | App.tsx Route | in FIRM_ALLOWED_PATHS | class | firm union |
|---|---|---|---|---|---|---|---|
| 1 | POST /sentiment/keyword-intelligence | getKeywordIntelligence, endpoints/sentiment.ts:786, `apiRequest('/v1/sentiment/keyword-intelligence')` :791 | components/market-performance/KeywordSentimentModal.tsx:16 -> components/market-performance/SentimentGauge.tsx:17 -> pages/MarketPerformance/panels/SentimentPanel/SentimentPanel.tsx:7 -> pages/MarketPerformance/MarketPerformance.tsx:16,135 | `/market` (App.tsx:448) | yes, all four sets | i | 49financial, cottonwood, demo, inflection |
| 2 | GET /aum/metrics | DataSourceContext.tsx:104 `apiRequest('/aum/metrics')`, inside the smartx query, `enabled: false` (line 110) | contexts/DataSourceContext.tsx, imported only by main.tsx:11 (DataSourceProvider wraps the app root) | every route (root provider) | root-wide; the set is App-wide | i | 49financial, cottonwood, demo, inflection |
| 3 | GET /news/articles/* | queryArticlesByDate, portal-proxy.ts:565 `apiRequest('/news/articles/${date}')` | NONE (named only in the export block portal-proxy.ts:2579) | -- | no | ii | -- |
| 4 | GET /returns/etf-periods | getETFPeriodReturns, portal-proxy.ts:962 | NONE (named only in portal-proxy.ts:2555) | -- | no | ii | -- |
| 5 | GET /aum/summary | validateAPIConnection, portal-proxy.ts:2518 | NONE (named only in portal-proxy.ts:2597; default-export object not imported anywhere) | -- | no | ii | -- |
| 6 | GET /health/data-availability | none | none | -- | no | ii | -- |
| 7 | GET /market/metrics | none (portal reads `/api/general/market/all_returns.json` and VITE_METRICS_URL) | none | -- | no | ii | -- |
| 8 | GET /market/metrics/full | none | none | -- | no | ii | -- |
| 9 | GET /market/rsi | none | none | -- | no | ii | -- |
| 10 | GET /market/rsi/details | none | none | -- | no | ii | -- |
| 11 | GET /market/all | none (getAllMarketData reads `/api/general/market/all_returns.json`, portal-proxy.ts:160) | none | -- | no | ii | -- |
| 12 | GET /market/ticker/* | none (getMarketDataForTicker reads `/api/general/market/ticker/`, :177) | none | -- | no | ii | -- |
| 13 | GET /market/entity-type/* | none (`/api/general/market/entity-type/`, :195) | none | -- | no | ii | -- |
| 14 | GET /aum/flows | none (getAUMFlows reads `/api/private/portfolios/aum-flows.json`, :307) | none | -- | no | ii | -- |
| 15 | GET /aum/timeseries | none (`/api/general/portfolios/aum-timeseries.json`, :345) | none | -- | no | ii | -- |
| 16 | GET /aum/account-distribution | none (serve path only in the handler; portal reads S3 via aum.ts) | none | -- | no | ii | -- |
| 17 | GET /aum/non-model | none (`/api/general/portfolios/non_model_assets.json`, :417) | none | -- | no | ii | -- |
| 18 | GET /peers/performance | none (`/api/general/peers/peer_performance.json`, :942) | none | -- | no | ii | -- |
| 19 | GET /benchmarks/returns | none (`/api/general/benchmarks/benchmark_returns.json`, :764) | none | -- | no | ii | -- |
| 20 | GET /positioning/data | none (`/api/general/positioning/positioning_data.json`, :1178) | none | -- | no | ii | -- |
| 21 | GET /positioning/attribution | none (`/api/general/positioning/holdings_attribution_data.json`, :2046) | none | -- | no | ii | -- |
| 22 | GET /positioning/allocation-summary | none (`/api/general/positioning/allocation_summary.json`, :1940) | none | -- | no | ii | -- |
| 23 | GET /metadata/yang | none (YangDataContext.tsx:45 reads `/api/general/metadata/yang.json`) | none | -- | no | ii | -- |
| 24 | GET /positioning/model | none (`/api/general/positioning/model.json`, :1489) | none | -- | no | ii | -- |
| 25 | GET /valuation/data | none (`/api/general/valuation/valuation_data.json`, :1826) | none | -- | no | ii | -- |
| 26 | GET /valuation/risk-premium | none (`/api/general/valuation/risk_premium_data.json`, :1879) | none | -- | no | ii | -- |
| 27 | GET /correlations/data | none (`/api/general/correlations/correlation_data.json`, :1979) | none | -- | no | ii | -- |
| 28 | GET /macro/data | none (`/api/general/macro/macro_data.json`, :2096) | none | -- | no | ii | -- |
| 29 | GET /macro/volatility | none (`/api/general/macro/volatility_data.json`, :2182) | none | -- | no | ii | -- |
| 30 | GET /macro/vix | none (`/api/general/macro/vix_data.json`, :2206) | none | -- | no | ii | -- |
| 31 | GET /macro/timeseries/* | none (endpoints/macro.ts:28 reads `/api/general/macro/timeseries/`) | none | -- | no | ii | -- |
| 32 | GET /factor-tilts/data | none (`/api/general/factor-tilts/*.json`, :1630-1656) | none | -- | no | ii | -- |
| 33 | GET /cma/assumptions | none (`/api/general/capital-markets/assumptions.json`, :1715) | none | -- | no | ii | -- |
| 34 | GET /cma/views | none (`/api/general/capital-markets/views.json`, :1757) | none | -- | no | ii | -- |
| 35 | GET /benchmarks/etf-returns | none (`/api/general/benchmarks/etf_returns.json`, :897) | none | -- | no | ii | -- |
| 36 | GET /trending/latest | none (`/api/general/trending/latest.json`, :656) | none | -- | no | ii | -- |
| 37 | GET /trending/topics/* | none (`/api/general/trending/topics/`, :630) | none | -- | no | ii | -- |
| 38 | GET /sentiment/fear-greed | none (`/api/general/sentiment/fear-greed-index.json`, endpoints/sentiment.ts:123) | none | -- | no | ii | -- |
| 39 | GET /sentiment/fear-greed/details | none (same S3 file, sentiment.ts:135) | none | -- | no | ii | -- |
| 40 | GET /sentiment/keywords | none (`/api/general/sentiment/keyword-sentiments.json`, :2256) | none | -- | no | ii | -- |
| 41 | GET /sentiment/keyword-history/* | none (`/api/general/sentiment/keyword-history-summary/`, sentiment.ts:612) | none | -- | no | ii | -- |

Rows with "none" were searched in portal/src (tests excluded) for the route tail as a literal
(`/aum/`, `/market/`, `/macro/`, ... with a leading quote, backtick or slash). Every hit was an
`/api/general/`, `/api/private/` or `/api/scoped/` path, a comment, or a test. Row 1's `/v1/` literal
is the only `/v1/` call in portal/src.

## 4. Class and firm union

- CLASS (i) -- rows 1 and 2. Row 1 is reached by /market (MarketPerformance.tsx renders SentimentPanel,
  line 135). /market is in all four firm sets, so the union is 49financial, cottonwood, demo, inflection.
  Row 2 is reached through the app-root provider, which every page renders under; it is not in any
  page's import closure, so it is classed (i) by the conservative rule (App-wide page set, union of all
  four). Its query is `enabled: false`; the class stands regardless.
- CLASS (ii) -- rows 3-5 and 6-41. Rows 3-5 have a portal client function but no importer in portal/src,
  so no FIRM_ALLOWED_PATHS page's import closure reaches it. Rows 6-41 have no portal caller at all.
  Firm union: none (class ii admits internal tier only).
- Ambiguous routes: none. Every route was traced; no route was classed (i) for lack of a trace.

## 5. Consequences recorded for the issuer

- The conservative-class arm for row 1 is firm-scoped: a partner firm in the four-set union reaches
  keyword-intelligence; a firm outside it gets 403.
- Partner pages named in surprise row NFRA_CTLPLN-W62-S1 (YieldCurveTab, RiskPremiumTab, ModelPortfolios,
  Positioning) call functions whose URLs are `/api/general/*` (S3), not data-proxy routes. The fence never
  touched those reads. The content GET (`/api/scoped/portal-content`) is unfenced again (step 4).
  See surprise row NFRA_CTLPLN-W62-S4.
