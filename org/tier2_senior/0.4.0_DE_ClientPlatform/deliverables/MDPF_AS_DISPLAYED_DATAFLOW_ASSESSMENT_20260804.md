# MDPF AS-DISPLAYED portal dataflow assessment — rendered view -> fetch URL -> resolved S3 object -> writer

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-08-04 ~03:0xZ · **Trigger:** Andrew-direct
(relayed by 3.0.0_SA_CVO, verbatim record @
`org/tier1_exec/3.0.0_SA_CVO/deliverables/ANDREW_DIRECT_de_portal_dataflow_assessment_20260804.md`).
**Read-only assessment; feeds MDPF_GLOBAL T3.B router-pin + T5 kill-order + CTO C.3.**
Briefing base: `MDPF_LEGACY_ROUTE_BLAST_CENSUS_20260804.md` (corrected state).

## GROUNDING PLANE (what "deployed" means in every row below)

- **Portal code:** `origin/PROD` @ `c6f561b6` (v2.1.155, merged 2026-08-03 13:29 ET) — the CI-deployed branch.
- **Router:** LIVE CloudFront distribution `EVTSA9VEHNZVH` (opalinvest.dev), behavior `/api/general/*`
  -> origin `S3-opal-data-portal-v2-json` = bucket `opal-data-portal-v2`, **OriginPath EMPTY**;
  viewer-request `auth-validator-edge:18`, **origin-request `public-data-router:6`**, origin-response
  `cache-control-injector:2` (live `get-distribution-config`, 2026-08-04 ~02:4xZ).
- **Deployed router code:** `public-data-router` **version 6** artifact downloaded from the live
  qualifier (zip sha256 `bc2eb90449e0d3eaa8c987db738d95c27d096745614c6b40c17d9f181fb7cd26`). Four
  branches, in order: `/api/general/json-tiered/` -> `/json-tiered/` · `/api/general/json/` -> `/json/`
  · **`/api/general/mdpf/` -> `/platinum/mdpf/`** · `/api/general/` -> `/json/`.
- **EXERCISED (live traffic, not config):** the router's own CW log emissions
  (`/aws/lambda/us-east-1.public-data-router`), 08-01 + 08-03 real viewer sessions:
  every `/api/general/mdpf/*` request rewritten `-> /platinum/mdpf/*` (all 4 scopes, all families,
  incl. `cottonwood/aum-metrics.json` 2026-08-03T12:56:25.422Z); negative control:
  `/api/general/portfolios/aum-metrics.json -> /json/portfolios/aum-metrics.json` fired 6+ times
  2026-08-03 12:09–13:24Z. Live unauthenticated curl of the mdpf URL: HTTP 401 `application/json`
  (auth edge live, no HTML error-masking on this path).
- **S3 state:** live listings + `get-object` provenance reads 2026-08-04 ~02:5xZ (times below in ET
  as listed, Z where stated).

## VERDICT ON ANDREW'S ACCEPTANCE EXAMPLE

**`opal-data-portal-v2/json/mdpf/*` is NOT displayed anywhere — PASS.**
- The deployed router's mdpf branch precedes the general branch, so every `/api/general/mdpf/*`
  fetch resolves to `platinum/mdpf/*` (config + code + live-traffic exercised, above).
- Zero deployed fetch sites use the `/api/general/json/mdpf/...` escape (PROD-wide grep: the string
  `json/mdpf` appears in COMMENTS only — `aum.ts:522`, `aum.ts:560`, `portal-proxy.ts:499`, `:517`).
- **Those comments are FALSIFIED by the deployed router** (they claim `/api/general/*` -> `/json/*`
  for the mdpf routes). Stale-comment cleanup belongs to T3.B; do not cite them as routing truth.

**BUT the json/ channel IS displaying model-portfolio assets for the third named family via a
DIFFERENT key — see FINDING F1.**

## THE AS-DISPLAYED MAP (deployed ModelPortfolios page — denominator: all 9 live fetches)

Deployed `src/pages/ModelPortfolios.tsx` carries exactly **9 live useQuery fetches** (call-site
census below; the page tree per comp-cluster = ModelPortfolios.tsx + tabs/PeersTab.tsx, 118/119
page-tree coverage). `{firmId}` ∈ {global, 49financial, cottonwood, inflection}.

| # | queryKey (view) | fetch site | URL | resolved object (FULL bucket+key) | obj last-modified | writer |
|---|---|---|---|---|---|---|
| 1 | `mdpf-per-firm-timeseries` (firm AUA trend) | MP.tsx:417-419 -> aum.ts:493 -> proxy | `/api/general/mdpf/{firmId}/aggregate-aua-timeseries.json` | `s3://opal-data-portal-v2/platinum/mdpf/{firmId}/aggregate-aua-timeseries.json` | 2026-08-03 16:15Z | `opal-assets-mdpf-portal-publisher` (in-artifact `_provenance.written_by`) |
| 2 | `mdpf-aggregate-timeseries` global (Global VALUE trend + donut count path) | MP.tsx:430-432 | `/api/general/mdpf/global/aggregate-aua-timeseries.json` | `s3://opal-data-portal-v2/platinum/mdpf/global/aggregate-aua-timeseries.json` | 2026-08-03 16:15Z | publisher (same) — **content `as_of_last: 2026-07-30`** |
| 3 | `mdpf-per-firm-distribution` (firm bell) | MP.tsx:466-473 -> aum.ts:544 | `/api/general/mdpf/{firmId}/account-distribution.json` | `s3://opal-data-portal-v2/platinum/mdpf/{firmId}/account-distribution.json` | 2026-08-03 16:15Z | publisher; source vintage 2026-07-31 (gold `2026-07-31.json`) |
| 4 | `mdpf-per-firm-aum-metrics` (**cottonwood ONLY** — `enabled: effectiveFirmId === 'cottonwood'`) | MP.tsx:485-490 -> aum.ts:622 | `/api/general/mdpf/cottonwood/aum-metrics.json` | `s3://opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json` | 2026-08-03 16:15Z | publisher; source vintage 2026-07-24 |
| 5 | `aum-metrics` (**base data, loads on mount, GATES the page**; model cards `:664-748`, quarterly totals `:1606-1695`, `:1762`) | MP.tsx:514-520 -> portal-proxy.ts:358 | `/api/general/portfolios/aum-metrics.json` | **`s3://opal-data-portal-v2/json/portfolios/aum-metrics.json`** | **2026-07-23 20:57Z (FROZEN)** | no in-artifact provenance; INFERRED = smartx global-metrics write (`:850`), now `DISABLE_PORTAL_AUM_METRICS_WRITE=1`-disabled (census @ae2d684f3b; freeze date matches flag landing) |
| 6 | `mdpf-account-distribution` global (Global bell; `enabled: global`) | MP.tsx:543-548 -> aum.ts:544 | `/api/general/mdpf/global/account-distribution.json` | `s3://opal-data-portal-v2/platinum/mdpf/global/account-distribution.json` | 2026-08-03 16:15Z | publisher; source vintage 2026-07-31 |
| 7 | `model-portfolio-benchmarks` (Performance tab, lazy) | MP.tsx:555-558 -> proxy | `/api/general/benchmarks/model_portfolio_benchmarks.json` | `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json` | 2026-08-03 16:23Z | not traced (outside the three families) |
| 8 | `etf-benchmark-returns` (Performance tab, lazy) | MP.tsx:563-566 -> proxy | `/api/general/benchmarks/etf_returns.json` | `s3://opal-data-portal-v2/json/benchmarks/etf_returns.json` | 2026-08-03 16:23Z | not traced |
| 9 | `peer-performance` (Peers tab, lazy) | MP.tsx:570-573 -> proxy | `/api/general/peers/peer_performance.json` | `s3://opal-data-portal-v2/json/peers/peer_performance.json` | 2026-08-03 13:54Z | not traced |

**Dead endpoint declarations (ZERO deployed callers — PROD-wide caller sweep):**
`getAccountDistribution()` (global json/portfolios bell — confirms T5.A), `getNonModelAssets()`,
`getAUMTimeSeries()` + `getModelTimeSeries()` (so `json/portfolios/aum-timeseries.json` is fetched
by NOTHING deployed), and the global `getMdpfAggregateAUATimeSeries()` wrapper (the page uses the
ByFirm('global') form). comp-cluster lists their URLs as page sources because the declarations live
in imported modules — declaration-level edges, not live calls.

**Same-artifact consumers OUTSIDE this page** (row-5's json object, call-sites cited; render-level
tracing was in-scope only for ModelPortfolios): `FactorTilts.tsx:83` (`getAUMMetrics`),
`Attribution/tabs/SelectionTab.tsx:89` + `Positioning/tabs/HoldingsTab.tsx:564` (`getAUMSummary`
-> portal-proxy.ts:277, same URL).

## FINDINGS

**F1 — The json/ channel IS displaying model-portfolio assets for the `aum-metrics.json` family —
via `json/portfolios/`, not `json/mdpf/`.** Row 5: the deployed Model Portfolios page loads
`s3://opal-data-portal-v2/json/portfolios/aum-metrics.json` on mount, GATES page render on it
(`:585`), and builds the model cards + quarterly totals from it. Live-traffic exercised (6+ rewrites
08-03). The artifact is **FROZEN at 2026-07-23** (period `2026-07-22`) because its writer was
flag-disabled — so the page's core metrics are 12 days stale while sitting one prefix away from a
canonical fresh(er) plane. Andrew's verbatim named the json/ bucket + three families; the CVO
acceptance example rendered it as `json/mdpf/*` (PASS above). **Surfacing, not adjudicating: if the
criterion is the json/ CHANNEL, F1 is a violation of it; if it is `json/mdpf/*`, the estate passes.**
NOTE: no platinum twin exists for the GLOBAL metrics (`platinum/mdpf/global/aum-metrics.json` absent)
— a repoint is not a pure retarget; the canonical global-metrics artifact does not exist yet.

**F2 — Platinum per-firm `aum-metrics` exists ONLY for cottonwood.** 49financial/inflection/global
have no `platinum/mdpf/{scope}/aum-metrics.json`. Deployed code is CONSISTENT (row 4's
cottonwood-only `enabled` gate; zero 404s in live logs — no 49f/inflection metrics requests exist),
but 3F-P3 firm-expansion is structurally blocked until the publisher writes those artifacts.

**F3 — Fresh stamps, stale content, corroborated at the display layer.** Every platinum hyphen
object displayed is stamped 2026-08-03 16:15Z by the publisher, but in-artifact content is
`as_of_last 2026-07-30` (timeseries) / source vintage 07-31 (bells) / 07-24 (cottonwood metrics) —
the T2.A source-truncation, now confirmed in what users actually see. The page's as-of stamp reads
the artifact's own `as_of_last`, so it honestly shows 07-30.

**F4 — Deployed source comments claim the OPPOSITE routing for mdpf paths** (aum.ts:520-523, :560;
portal-proxy.ts:498-501, :516-517 say `/api/general/*` -> `/json/*` serves them from json/mdpf).
Falsified by deployed router v6 + live logs. T3.B should sweep these in its router-pin doc pass.

**F5 — The json/mdpf channel is written daily and displayed never.** smartx writes
`json/mdpf/{firm}/account-distribution.json` daily 11:30Z unconditionally (census; 49financial +
inflection fresh 08-03 07:30 ET) into a channel with zero deployed readers — pure kill-list fodder
(T5 row 7 class), now with the display-side zero-reader half proven.

**F6 — Underscore twins on the serve prefix are displayed never.** No deployed fetch resolves any
`platinum/mdpf/**/aggregate_aua_timeseries.json` (underscore) — the page's underscore-named
TypeScript types are naming residue over hyphen URLs. The stopped runner plane serves nothing
user-visible on this page.

## COMPILER TOOLS

| Tool | Result |
|---|---|
| comp-cluster ModelPortfolios (+ --json) | page-rooted map, 25 sources, 118/119 coverage; declaration-vs-live-call caveat noted above |
| comp-routes behaviors / rewrites / trace / edge-versions | DESIRED-plane behavior table + rewrite table (mdpf -> platinum) + qualified_arn pinning; correctly self-labeled DESIRED, drove the live grounding |
| comp-kuzu (writer queries) | READS_URL edges found for row-5 URL; no WRITES edge for the json metrics key (gap noted; writer INFERRED via census) |
| comp-blast | not fired — the census (@01:1xZ) had just exercised it on this exact estate; re-running would duplicate its evidence, and the display-side question needed caller/router grounding instead |
| Raw aws (rail-checked inline each call) | live distribution config, deployed edge v6 artifact, S3 listings/objects, live CW rewrite logs — the APPLIED/EXERCISED legs comp tools declare themselves blind to |

— 0.4.0_DE_ClientPlatform
