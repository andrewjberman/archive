# 3F-P2 — MDPF Endpoint/Route Audit

- **TO:** MDPF_3FIRMS.3F-P2 (COO GO 20260722T203302Z) — READ-ONLY; joint 0.7.0_AE for behavior-side follow-ups.
- **Auditor:** 0.4.0_DE_ClientPlatform
- **Vintage:** portal DEV @ `08c6d8b2` · workspace @ `1c42b3fd9` · live CF config read 2026-07-22 ~20:38Z
- **Ground truth instruments:** `comp-routes behaviors` + `comp-routes trace` (DESIRED/graph view) **and** live `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH` (APPLIED truth, rail-checked per TO Phase-2) — Rule 22a both-layers grounding.

## HEADLINE VERDICTS

1. **The §2.1 premise HOLDS at live state: 24 non-default behaviors / 7 origins / ZERO mdpf- or portfolios-pattern behaviors live.** Origins: S3-opal-data-portal-v2-json, S3-opal-data-inf, S3-opal-data-cot, S3-opal-data-bd, S3-opalinvest-portal, APIGateway-portfolio, APIGateway-portal. No `S3-opal-data-assets` origin exists on the live distribution. **Nothing from the revamp has ever been served — confirmed, no escalation triggered.** (comp-routes shows 25 = 24 ordered + the `/*` default; counts reconciled, same set.)
2. **Every MDPF-page endpoint (14 of 14) resolves to ONE live behavior:** `/api/general/*` (position 18 in comp-routes' listing) → origin `S3-opal-data-portal-v2-json` → edge chain `auth-validator-edge` (viewer-request JWT) → `public-data-router` (origin-request; rewrites `/api/general/X` → `/json/X`) → `cache-control-injector` (origin-response). **Zero orphan endpoints.**
3. **CustomErrorResponses on the live distribution: quantity 0.** The banked "CF error rules mask JSON errors" hazard does NOT operate via custom-error-responses on EVTSA9VEHNZVH at current state. The masking mechanism that DOES exist: a URL matching no ordered behavior falls to the default `/*` → SPA (`S3-opalinvest-portal`) → HTML 200 (index.html via the SPA deep-link fallback CloudFront Function, `cloudfront-distribution.tf:91`). So "endpoint returns HTML" here = the path missed every ordered behavior, not an intercepted 404. Within behavior 18, a missing S3 key returns the raw S3 error (no interception declared).

## PART 1 — The two URL families

| Family | Endpoints (FE call sites at 08c6d8b2) | Live serving today | Declared future (flip) |
|---|---|---|---|
| **Legacy** `/api/general/portfolios/*` | `aum-metrics.json` (`portal-proxy.ts:345`) · `aum-timeseries.json` (`:321`) · `non_model_assets.json` (`:393`) · `account-distribution.json` (`aum.ts:552`) | behavior `/api/general/*` → portal-v2 `json/portfolios/*` (legacy nightly keeps writing = the shadow) | 4 of the 9 declared exact-path behaviors re-home these SAME URLs to `opal-data-assets` |
| **Revamp** `/api/general/mdpf/{firmId}/*` | `aggregate-aua-timeseries.json` for global/49financial/inflection/cottonwood (`portal-proxy.ts:494,:513`) · `account-distribution.json` per firm (`aum.ts:597`) | SAME behavior `/api/general/*` → portal-v2 `json/mdpf/{firmId}/*` (yes — the "revamp" URL family is ALREADY LIVE as URLS, served from the LEGACY bucket; what has never been served is the opal-data-assets ORIGIN) | 5 of the 9 declared behaviors re-home global/49f/inf; **Cottonwood: see FINDING F-1** |
| Adjacent (same page, out of both families) | `benchmarks/model_portfolio_benchmarks.json` · `benchmarks/etf_returns.json` · `peers/peer_performance.json` | same behavior 18 → portal-v2 | NOT in the declared flip set (stay on portal-v2) |

**Nuance worth stating precisely:** the PRD's "nothing from the revamp has ever been served" is true of the **origin/behavior layer** (no assets-origin behavior live). The revamp **URL family** `/api/general/mdpf/{firmId}/*` IS live today through the catch-all, serving portal-v2 keys produced by the legacy/current nightly (mdpf_aggregate_aua.py family). The flip changes WHERE those URLs resolve, not the URLs.

## PART 2 — comp-routes trace, all 14 endpoints

All 14 (4 legacy + 7 mdpf incl. cottonwood pair + 3 adjacent) traced individually: identical resolution — behavior `/api/general/*`, origin `S3-opal-data-portal-v2-json`, auth `auth-validator-edge` JWT, router `public-data-router`, response `cache-control-injector`. (Raw outputs in session log; MSYS note: URL args need `MSYS2_ARG_CONV_EXCL="/api"` — bare `MSYS_NO_PATHCONV=1` breaks the launcher's internal python path.)

## PART 3 — The 9 declared-not-live behaviors → artifacts (EXPECTED drift, NOT an action item)

Declared at `infra/aws/terraform/portal-auth/cloudfront-distribution.tf:77-87` (`local.mdpf_assets_behavior_paths`, dynamic block `:654-684`): exact-path clones of behavior 18, target `S3-opal-data-assets`, placed BEFORE the catch-all so exact paths win; rollback = remove the block. Publisher `opal-assets-mdpf-portal-publisher` `PUBLISH_MAP` (`lambda_function.py:37-47`) maps staged → served keys **1:1 with these 9 paths**:

| # | Declared path_pattern | Would serve (opal-data-assets key) | Staged source (`gold/mdpf_revamp/...`) | Producer | Live? |
|---|---|---|---|---|---|
| 1 | `/api/general/mdpf/global/aggregate-aua-timeseries.json` | `json/mdpf/global/aggregate-aua-timeseries.json` | `global/aggregate_aua_timeseries.json` | revamp_stage (mdpf-daily-dispatch.sh Stage 6) | **no** |
| 2 | `/api/general/mdpf/49financial/aggregate-aua-timeseries.json` | `json/mdpf/49financial/...` | `49financial/aggregate_aua_timeseries.json` | same | **no** |
| 3 | `/api/general/mdpf/inflection/aggregate-aua-timeseries.json` | `json/mdpf/inflection/...` | `inflection/aggregate_aua_timeseries.json` | same | **no** |
| 4 | `/api/general/mdpf/49financial/account-distribution.json` | `json/mdpf/49financial/account-distribution.json` | `49financial/account_distribution.json` | same | **no** |
| 5 | `/api/general/mdpf/inflection/account-distribution.json` | `json/mdpf/inflection/account-distribution.json` | `inflection/account_distribution.json` | same | **no** |
| 6 | `/api/general/portfolios/account-distribution.json` | `json/portfolios/account-distribution.json` | `global/account_distribution.json` | same | **no** |
| 7 | `/api/general/portfolios/non_model_assets.json` | `json/portfolios/non_model_assets.json` | `global/non_model_assets.json` (`dim_mdpf_non_model_assets.py`) | same | **no** |
| 8 | `/api/general/portfolios/aum-metrics.json` | `json/portfolios/aum-metrics.json` | `portfolios/aum-metrics.json` (`dim_mdpf_aum_metrics.py`) | same | **no** |
| 9 | `/api/general/portfolios/aum-timeseries.json` | `json/portfolios/aum-timeseries.json` | `portfolios/aum-timeseries.json` (`dim_mdpf_aum_timeseries.py`) | same | **no** |

All 9 confirmed NOT live against the applied distribution config (zero mdpf/portfolios path patterns, no assets origin, no OAC in the live Origins list). **Drift recorded as EXPECTED per TO — nothing actioned, zero TF touched.**

## PART 4 — FINDINGS

- **F-1 (WS-F/3F-G2, route to CTO+COO): THE DECLARED FLIP SET HAS NO COTTONWOOD PATHS.** `local.mdpf_assets_behavior_paths` carries global/49f/inflection only — no `/api/general/mdpf/cottonwood/aggregate-aua-timeseries.json`, no `/api/general/mdpf/cottonwood/account-distribution.json`. Under Andrew's ruling (LD-0330: ONE FLIP, **Cottonwood INSIDE the gate**), flipping the block as declared would serve Cottonwood from the legacy portal-v2 shadow while the other firms move to assets — a silent per-firm origin split. This is the RF-1 defect class (`PUBLISH_MAP` 9-entry hardcode) at the CF layer: **`mdpf_assets_behavior_paths` is an EIGHTH hardcoded firm-enumeration consumer that PRD §3.3's registry-retrofit list does not name.** Recommend: add it to the 3F-G2 consumer list; the flip TF and PUBLISH_MAP must both grow their Cottonwood entries (and the FE already calls the cottonwood URLs today — `ALL_MDPF_PARTNER_FIRMS`, `ModelPortfolios.tsx:244-249`).
- **F-2: The null-on-404 wrapper (TO item d), documented at source.** `portal/src/api/endpoints/aum.ts:586-608 @ 08c6d8b2` — `getAccountDistributionByFirm` wraps `apiRequest` in try/catch `:595-607`; ANY failure (404 on a missing per-firm key, 403, network, malformed JSON) → `console.error` + `return null`. The consuming query (`ModelPortfolios.tsx:487-497`) treats null as data. **Rendered consequence:** the bell-curve panel renders empty ("Distribution Data Unavailable" path) with no error surface — a missing Cottonwood artifact is byte-indistinguishable at the component from "this firm has no data yet." Same pattern on the per-firm AUA fetch (`getMdpfAggregateAUATimeSeriesByFirm`, comment at `ModelPortfolios.tsx:238-241`: a firmId/key mismatch "404s into the queryFn's catch and renders an EMPTY partner rather than an error — silent"). The error branch also caches nothing, so every render retries. **This is the day-one-Cottonwood rendering question in disguise (TO's words), now with file:line.** Disposition belongs to 3F-P3 (FE build): distinguish absent-artifact (render "not yet tracked" honestly) from fetch-error (render an error).
- **F-3: No distribution-level 404 interception exists** (CustomErrorResponses=0) — 4xx diagnosis on this distribution should look for SPA fallthrough (HTML 200 from `/*`), not error-response masking. The TO's masked-404 warning is satisfied by this enumeration: the intercept rule set is EMPTY; the mask is the default-behavior fallthrough.
- **F-4 (instrument): comp-routes/comp-platinum resolve `getAccountDistribution` to the commented-out `/api/private/...` TODO** (`aum.ts:517`), not the live `/api/general/...` call at `:552` — behavior + auth columns for that endpoint are wrong in the tools (they route it to APIGateway-portfolio; live truth is behavior 18 → S3). Flagged to the comp-tools owner lane; do not cite the tool's URL column for this endpoint.

## Acceptance mapping

1. Route table committed (Parts 1–3); every flip-served artifact has behavior + origin + auth path; zero orphans. ✔
2. 9 declared behaviors mapped to artifacts + producers, each confirmed NOT live against applied config. ✔
3. Null-on-404 documented at `aum.ts:586-608 @ 08c6d8b2` with rendered consequence (F-2). ✔
4. `comp-routes behaviors` run first; intercept rules enumerated (= empty set + SPA fallthrough, F-3). ✔
5. Zero TF applied, zero behavior changes; portal-auth drift recorded EXPECTED, not actioned. ✔
