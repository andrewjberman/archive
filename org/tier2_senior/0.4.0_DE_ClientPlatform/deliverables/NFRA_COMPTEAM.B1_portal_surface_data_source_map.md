# NFRA_COMPTEAM B1 -- Portal-surface -> data-source map (grounded vs live served, cadence-aware)

**Owner:** 0.4.0_DE_ClientPlatform | **Version:** v0.2 | **Date:** 2026-07-01
**Machine-checkable map:** `NFRA_COMPTEAM.B1_portal_surface_data_source_map.json` (this dir)
**PRD:** `docs/architecture/NFRA_COMPTEAM_PRD.md` SS3 / SS8-B1 / AC-3 / arch-gate-4
**For:** CTO arch-gate (grounding method + schema + the cadence-per-artifact rule) -> feeds B2 (AE-graph + SCTY) read-partition.

## What this is
The "give me the data behind panel X" map: every portal **PanelCluster** (TSGRAPH `CLUSTERS`) -> its served
**data source** -> the **gold/platinum artifact**, **grounded vs the live served object** (arch-gate-4). Built by
REUSING P2-3 `comp-cluster` for enumeration + SERVED_FROM (static) + `comp-platinum`/FIRM_CONFIG (dynamic), then
live-confirming each artifact **cadence-aware** (stale = past ITS OWN cadence, not a blanket threshold).

## Grounding provenance
- **Enumeration:** `comp-cluster <page> --json` x15 pages -> 91 PanelClusters / 125 source-bindings. Live Kuzu (nessie **HEAD current**, 2026-07-01T04:45Z).
- **STATIC lineage:** `Endpoint -READS_URL-> ServedURL -SERVED_FROM-> {bucket,s3_key}` (29 edges, `verified: object+node`).
- **DYNAMIC lineage:** `comp-platinum tab-audit` + `portal/src/api/endpoints/advisor-intelligence.ts` -> endpoint -> relative platinum key; firm prefix selects `opal-data-{bd,cot,inf}`.
- **Live-confirm:** `comp-freshness artifact` (2026-07-01). **Cadence:** per-artifact; CMA **Andrew-confirmed yearly** (2026-07-01).

## Two grounding tiers + counts
| Tier | Bindings | Grounding | Live result |
|---|---|---|---|
| **STATIC** | 42 (12 artifacts) | `ServedURL -SERVED_FROM-> s3_key` (bucket `opal-data-portal-v2`) | 33 FRESH / 6 EXPECTED-CADENCE / 3 REAL-STALE-bindings |
| **DYNAMIC** | 83 | endpoint -> relative platinum key, firm-scoped | FIRM-LEVEL 38 (live bd/cot/inf) / PER-ENTITY 32 (pattern) / TAIL 13 (v0.3) |

**DYNAMIC FIRM-LEVEL** (38 bindings, e.g. `getFirmLeaderboard`->`platinum/firm/leaderboard.json`, `getHeaderMetrics`,
`getPlatinumFirmDashboard`, `getTimeseriesOverview`, `getPlatinumCumulativeChart`, `getClientDirectory`): live-confirmed
across all 3 firms. Most PASS; notable non-PASS -- cot `leaderboard.json`/`advisor_nna_canonical.json` = WARN (cot platinum
content-lag, 2td behind), `client_directory.json` = inf PASS / cot WARN (absent -> **first-emits tonight's nightly per COTMVP-B**) / bd WARN.
**DYNAMIC PER-ENTITY** (32, e.g. `getPlatinumAdvisorSummary`->`platinum/advisors/{id}/summary.json`): resolved to the
firm+entity artifact PATTERN; per-`{id}` live-check is on-demand (v0.3). **TAIL** (13, mdpf-* / aum-metrics / portal-manifest):
enumerated, NOT silently dropped -- several are actually STATIC portal-v2 (`/api/general/mdpf/*`, `/api/general/portfolios/aum-metrics.json`) that the graph-native pass missed; v0.3 reclassifies + grounds.

## Findings (cadence-aware)
1. **REAL-STALE x1:** `s3://opal-data-portal-v2/json/portfolios/non_model_assets.json` (last modified **2026-06-25**, past its daily cadence). Page: ModelPortfolios. = the 49F/Schwab freeze -> **folds into the MDPF basis-switch thread** (COO-routed), self-resolves with the roll-forward.
2. **EXPECTED-CADENCE (NOT stale) x2:** CMA `views.json` (2026-01-09) + `assumptions.json` (2026-03-11). **Andrew-confirmed yearly cadence** -> ~4-6mo age is INTENTIONAL. Cadence-aware verdict prevents the blanket-threshold false-FAIL (v0.1 wrongly flagged these).
3. **GRAPH-COVERAGE-GAP:** SERVED_FROM grounds only the 29 static ServedURLs; the DYNAMIC tier is grounded via FIRM_CONFIG, not the graph. **Rec:** enrich TSGRAPH with `Endpoint->artifact` edges (the FIRM_CONFIG map IS the enrichment input) -> fully graph-native B1 + machine-checkable B2 over both tiers.
4. **SCHEMA-RULE (cadence-per-artifact):** freshness verdict is now cadence-aware -- `expected_cadence` (daily/weekly/monthly/quarterly/yearly/event-driven) is a first-class map field; stale = past the artifact's OWN cadence. This is what makes AC-3's live-grounded flag actionable (slow-cadence artifacts must not false-FAIL).

## Machine-checkable acceptance (PRD AC-3)
- Every PanelCluster's sources enumerated + tier-classified + grounded in the JSON (`pages[].clusters[].sources[]`).
- STATIC: 12/12 artifacts resolved + live-checked + cadence-verdicted.
- DYNAMIC: FIRM-LEVEL live-confirmed across bd/cot/inf; PER-ENTITY pattern-resolved; TAIL enumerated (no silent drop).

## CTO arch-gate asks (spec)
1. Confirm the two-tier grounding method (STATIC graph-native + DYNAMIC via FIRM_CONFIG) as the accepted B1 spec.
2. Adopt the **cadence-per-artifact rule** (`expected_cadence` field + per-artifact cadence registry) as B1 map schema -- it de-noises AC-3.
3. Rule on the GRAPH-COVERAGE-GAP rec (enrich TSGRAPH dynamic `Endpoint->artifact` edges -- own-lane NFRA_TSGRAPH, or defer).
4. Confirm the JSON schema is the B1->B2 hand-off contract (read-partition keys off `sources[].{bucket,s3_key}` static + `{relative_key, firm}` dynamic).

## v0.3 follow (no external dep)
Ground the 32 PER-ENTITY endpoints per-`{id}` (pick representative ids per firm) + reclassify/ground the 13 TAIL endpoints (mdpf/aum-metrics are static portal-v2; portal-manifest via portal-proxy). Closes 100% per-binding live grounding.
