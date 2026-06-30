# ADVI_INFREF P1 — unified single-pull-stage DIM LIST (for 0.6.1_AE EC2/IAM sizing + CTO surface sanity-check)

**Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-06-30 | **TO:** ADVI_INFREF.P1 LEG-2
**Source of record:** INFLEC_API_ENDPOINTS_CATALOG.md (mine, CTO-ratified 20260428T0455Z) + D3 §S1/S2/S3 + SPEC-1 §4/§59.
**Convention:** bronze RAW-NATIVE (CSV stays CSV, JSON stays JSON; NO parquet at bronze). Two domains separate: `bronze/orion-api/{date}/` + `bronze/eclipse-api/{date}/`. JSON/CSV->parquet is a SILVER function.

## ORION domain (`bronze/orion-api/{date}/`) — Session-JWT auth (orion/jwt/current, runner role covered)

| # | dim (bronze file) | endpoint family / path | method | native fmt | est size | cohort filter | status |
|---|---|---|---|---|---|---|---|
| 1 | representatives.json + household_rep_mapping.json | (reps) Portfolio/Accounts-derived | GET | JSON | small (~100s KB) | rep allowlist | LIVE (inline+cron) |
| 2 | new_portfolio_accounts.json / accounts_v2 | `GET /api/v1/Portfolio/Accounts/NewPortfolio?$top=50000&createdDateStart=01/01/1970&isActive=true` | GET sync | JSON | ~5.1 MB | custodian=Fidelity_Inflection | LIVE |
| 3 | unified_account_dim.csv | Envision ExcelReports (account grain, 24 col) | async POST->poll->CSV | CSV | ~884 KB | requiredOptions entityIds [3,11,12] | LIVE (cron-only) |
| 4 | performance_dim.csv | Envision ExcelReports (account grain, 27 col) | async POST->poll->CSV | CSV | ~878 KB | [3,11,12] | LIVE (inline+cron) |
| 5 | activity (from unified_account_dim, 3y window) | Envision (Activity Options 7/8/9/11/12/13/20) | async->CSV | CSV | (shares #3) | [3,11,12] | LIVE |
| 6 | billing.csv | Envision ExcelReports (billing fields) | async->CSV | CSV | ~884 KB | @RepIDs=[3,11,12] | LIVE (cron-only) |
| 7 | tax_unrealized.csv + tax_realized.csv | Envision Tax 3-level paths (Tax.{Term}.{Field}) | async->CSV (2 POSTs in series) | CSV | mod | [3,11,12] | LIVE (cron-only) |
| 8 | transactions.csv | Custom Reports `POST /api/v1/Reporting/Custom/28198/Generate/csv` (Homepage Daily Transactions - Rep) | async POST->poll->CSV | CSV | <50 MB cohort (503 MB full-firm) | @RepIDs="3,11,12" | LIVE (inline+cron) |
| 9 | positions.json / assets.json (positions_mv + assets_v2 source) | `GET /api/v1/Portfolio/Clients/{cid}/Assets/{MM-DD-YYYY}?$top=50000&includeCostBasis=false` × 313 HHs | GET sync ×313 | JSON (RAW -- de-convert target, currently parquet) | ~2-4 min/date wall; per-call ~300-600ms; 58 fields/row | iterate 313 household_ids | LIVE (the AUA backbone) |

### NEW cataloged surface to ADD (SPEC-1 §59 "pull the full cataloged surface", currently UNPULLED)
| # | dim | endpoint | method | fmt | size | status |
|---|---|---|---|---|---|---|
| 10 | trading_models + model_composition | `GET /api/v1/Trading/Models` + `/Trading/Models/{id}` (139 models, ticker-level) | GET sync | JSON | mod | NOT pulled (catalog-documented) |
| 11 | per-account assets (Track-2, optional) | `GET /api/v1/Portfolio/Accounts/{aid}/Assets/{date}` × ~2,755 | GET sync | JSON | ~3.7min 4-way | DISCOVERED-not-wired (per-client #9 covers v1) |
| 12 | aux (optional) | Authorization/User+Privileges; Homepage/Action/DataSources; SignalR completion | GET | JSON | tiny | aux/observe |

## ECLIPSE domain (`bronze/eclipse-api/{date}/`) — SEPARATE product; Session-JWT via orion->eclipse EXCHANGE (see IAM note)

| # | dim | endpoint | method | fmt | size | status |
|---|---|---|---|---|---|---|
| E1 | portfolios_simple.json | `/v1/portfolio/portfolios/simple` | GET | JSON | ~835 rows | LIVE (pull_eclipse_portfolios.py) |
| E2 | portfolios_full.json | `/v1/portfolio/portfolios` | GET | JSON | ~842 rows | LIVE |
| E3 | models.json | `/v1/modeling/models` | GET | JSON | ~18 | LIVE |
| E4 | model_composition_{id}.json ×9 | `/v1/modeling/models/{id}` (9 Opal model IDs {3,5,6,7,8,9,10,28,29}) | GET ×9 | JSON | small | LIVE |

## SIZING + IAM NOTES for 0.6.1_AE
- TOTAL daily raw footprint: dominated by transactions cohort (<50 MB) + the 313-HH per-client assets JSON (a few hundred MB raw across 313 calls before silver compaction). Well within 200 GB gp3. Inflection is a small book -- NO EC2 resize expected (your read agrees).
- S3: all under `opal-data-inf/*` (runner role wildcard-covered) -- ZERO S3 IAM add for the new orion-api + eclipse-api prefixes.
- SM: Orion JWT (orion/jwt/current) -- runner role HAS it. ECLIPSE: pull_eclipse_portfolios.py reads the ORION jwt from SM then EXCHANGES orion->eclipse via the API (_exchange_orion_for_eclipse_jwt) -- so the pull does NOT directly read orion/eclipse_jwt/current. => the GetSecretValue-on-eclipse_jwt add is LIKELY UNNEEDED (I'll give the definitive verdict at the eclipse-onto-runner step, sequenced last). Net Leg-2 IAM footprint: plausibly ZERO adds.

## DE-CONVERT / CUTOVER ORDER (the 4 own-prefix-parquet dims -> raw, atomic per dim)
1. performance + transactions FIRST (CSV dims; de-convert = drop the redundant inline-parquet double-write `bronze/{performance,transactions}/{date}.parquet`; the orion-api CSV already exists -- simplest pattern-setter, lowest stakes).
2. assets (raw JSON bronze + silver repoint).
3. positions LAST (AUA backbone; proven pattern + tightest parity: served AUA == Orion to the cent).
Eclipse onto-runner: LAST (after the 4 de-converts), with the (likely-zero) IAM verdict.

## OPEN for CTO
- Confirm the NEW surface (#10 trading_models, #11 per-account, #12 aux) is in P1 scope vs a follow (SPEC-1 says pull the full cataloged surface; #11/#12 are optional/observe).
