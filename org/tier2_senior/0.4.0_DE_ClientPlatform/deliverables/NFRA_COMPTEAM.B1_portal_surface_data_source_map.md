# NFRA_COMPTEAM B1 -- Portal-surface -> data-source map (grounded vs live served)

**Owner:** 0.4.0_DE_ClientPlatform | **Status:** v0.1 (this session) | **Date:** 2026-07-01
**Machine-checkable map:** `NFRA_COMPTEAM.B1_portal_surface_data_source_map.json` (this dir)
**PRD:** `docs/architecture/NFRA_COMPTEAM_PRD.md` SS3 / SS8-B1 / AC-3 / arch-gate-4
**For:** CTO arch-gate (map fidelity + the grounding method spec) -> feeds B2 (AE-graph + SCTY) read-partition.

## What this is
The "give me the data behind panel X" map: every portal **PanelCluster** (TSGRAPH `CLUSTERS`) ->
its served **data source** -> the **gold/platinum artifact**, **grounded vs the live served object**
(arch-gate-4: "a hypothesis until source-confirmed"). Built by REUSING P2-3 `comp-cluster` for the
PanelCluster enumeration + the SERVED_FROM lineage, then live-confirming each artifact.

## Grounding provenance
- **Enumeration:** `comp-cluster <page> --json` over all 15 portal pages -> 91 PanelClusters / 125 source-bindings.
  Source = live canonical Kuzu (nessie **HEAD current**, built 2026-07-01T04:45Z).
- **Lineage:** TSGRAPH edges -- `Hook -FETCHES-> Endpoint`, `Endpoint -READS_URL-> ServedURL`,
  `ServedURL -SERVED_FROM-> {bucket, s3_key}` (29 edges, `verified: object+node`).
- **Live-confirm:** `comp-freshness artifact <s3>` per static artifact (2026-07-01).

## The map has TWO grounding tiers (a load-bearing finding)
| Tier | Count | Chain | Grounded to live artifact? |
|---|---|---|---|
| **STATIC** | 42 bindings / 12 artifacts | `Endpoint -READS_URL-> ServedURL -SERVED_FROM-> s3_key` (bucket `opal-data-portal-v2`, `json/...`) | YES -- 9 PASS, 3 FAIL (see findings) |
| **DYNAMIC** | 83 bindings / 55 endpoints | portal `Endpoint` terminal (no SERVED_FROM); Lambda-mediated: `advisor-intelligence` / `portal-proxy` / `mdpf` -> FIRM_CONFIG -> `opal-data-{bd,cot,inf}/platinum` | NOT via graph (see GAP) |

The DYNAMIC tier is the whole ADVI / PortfolioManagement-partner / MDPF surface (e.g.
`getFirmLeaderboard`, `partner-analytics`, `getClientDirectory`, `getPlatinumAdvisorSummary`,
`mdpf-aggregate-timeseries`). These resolve to a live platinum artifact through the backend Lambda's
firm-scoped FIRM_CONFIG, NOT a single static ServedURL -- so SERVED_FROM does not (and structurally
cannot, as modeled today) ground them. Ground-truth spot-checks already confirm the resolution is real:
`getFirmLeaderboard` (49F) -> `s3://opal-data-bd/gold/artifacts/employee_leaderboard.json` (LIVE, 2026-07-01T04:43Z);
`getClientDirectory` (cottonwood) -> `s3://opal-data-cot/platinum/firm/client_directory.json` (first-serves tonight's nightly).

## Findings
1. **STALE-SERVED x3** (STATIC clusters served from artifacts past the 48h fail threshold):
   - `s3://opal-data-portal-v2/json/capital-markets/views.json` -- last modified **2026-01-09** (~173d). Page: CapitalMarketAssumptions.
   - `s3://opal-data-portal-v2/json/capital-markets/assumptions.json` -- last modified **2026-03-11** (~113d). Page: CapitalMarketAssumptions.
   - `s3://opal-data-portal-v2/json/portfolios/non_model_assets.json` -- last modified **2026-06-25** (~6d, just over 48h). Page: ModelPortfolios.
   -> The CapitalMarketAssumptions page is served from artifacts frozen since Jan/Mar 2026. Routes to the CMA/ModelPortfolios producer owner (not a B1 fix; a B1-surfaced fidelity break).
2. **GRAPH-COVERAGE-GAP** (feeds NFRA_TSGRAPH / GLOBGRPH): SERVED_FROM grounds source->artifact for only the 29 static
   ServedURL endpoints. 83/125 bindings (the DYNAMIC tier) terminate at a portal Endpoint with no modeled artifact edge.
   **Recommend:** enrich TSGRAPH with `Endpoint -> artifact` (or `Endpoint -> Lambda -READS_S3-> S3Key`) edges for dynamic
   endpoints, so B1 grounding is fully graph-native AND B2's read-partition can be machine-checked over BOTH serving tiers.

## Machine-checkable acceptance (PRD AC-3)
- Every PanelCluster's sources are enumerated + tier-classified in the JSON (`pages[].clusters[].sources[]` with
  `tier`, and for STATIC: `bucket`/`s3_key`/`graph_verified`/`live.status`).
- STATIC tier: 12/12 artifacts resolved + live-checked (9 PASS / 3 FAIL recorded).
- DYNAMIC tier: 100% enumerated + flagged with the FIRM_CONFIG resolution path (grounding = v0.2 follow, below).

## v0.2 follow (next)
Resolve the 55 DYNAMIC endpoints to their platinum artifacts via the `advisor-intelligence` / `portal-proxy` / `mdpf`
FIRM_CONFIG map (per-firm: bd/cot/inf), then live-confirm each -- closing full per-cluster artifact grounding.
Gated only by reading the backend Lambda's endpoint->artifact routing; no external dependency.

## CTO arch-gate asks (spec)
1. Confirm the two-tier grounding method (STATIC graph-native + live-confirm; DYNAMIC via FIRM_CONFIG) is the accepted B1 spec.
2. Rule on the GRAPH-COVERAGE-GAP recommendation (enrich TSGRAPH dynamic Endpoint->artifact edges) -- own-lane NFRA_TSGRAPH, or defer.
3. Confirm the machine-checkable JSON schema is the B1 hand-off contract to B2 (read-partition keys off `pages[].clusters[].sources[].{bucket,s3_key}` + the DYNAMIC firm-scope).
