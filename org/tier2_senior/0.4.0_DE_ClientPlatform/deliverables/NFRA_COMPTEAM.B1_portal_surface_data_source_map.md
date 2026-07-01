# NFRA_COMPTEAM B1 -- Portal-surface -> data-source map (grounded vs live served, cadence-aware)

**Owner:** 0.4.0_DE_ClientPlatform | **Version:** v0.3 | **Schema:** 1.0-FROZEN | **Date:** 2026-07-01
**Machine-checkable map:** `NFRA_COMPTEAM.B1_portal_surface_data_source_map.json` (this dir)
**PRD:** `docs/architecture/NFRA_COMPTEAM_PRD.md` SS3 / SS8-B1 / AC-3 / arch-gate-4
**Arch-gate:** CTO-ACCEPTED 2026-07-01 (all 4 asks ruled -- see below).

## What this is
The "give me the data behind panel X" map: every portal **PanelCluster** (TSGRAPH `CLUSTERS`) -> its served
**data source** -> the **gold/platinum artifact**, **grounded vs the live served object**, freshness judged
**cadence-aware** (stale = past ITS OWN cadence, not a blanket threshold). Reuses P2-3 `comp-cluster` (enumeration) +
SERVED_FROM (static) + `comp-platinum`/FIRM_CONFIG (dynamic).

## Grounding provenance
- **Enumeration:** `comp-cluster <page> --json` x15 pages -> 91 PanelClusters / 125 source-bindings. Live Kuzu (nessie **HEAD current**, 2026-07-01T04:45Z).
- **STATIC lineage:** `Endpoint -READS_URL-> ServedURL -SERVED_FROM-> {bucket,s3_key}` (29 edges, `verified: object+node`).
- **DYNAMIC lineage:** `comp-platinum tab-audit` + `portal/src/api/endpoints/advisor-intelligence.ts` -> endpoint -> relative platinum key; firm prefix -> `opal-data-{bd,cot,inf}`.
- **Live-confirm:** `comp-freshness artifact` (2026-07-01). **Cadence:** per-artifact; CMA **Andrew-confirmed yearly**; non_model_assets/mdpf cadence sibling-evidenced daily.

## Two grounding tiers + counts (v0.3)
| Tier | Bindings | Grounding | Live/verdict |
|---|---|---|---|
| **STATIC** | 47 | `ServedURL -SERVED_FROM-> s3_key` (+5 TAIL labels reclassified to static portal-v2) | 36 FRESH / 6 EXPECTED-CADENCE / 5 REAL-STALE-bindings -> **2 real-stale artifacts** |
| **DYNAMIC** | 78 | endpoint -> relative platinum key, firm-scoped | FIRM-LEVEL 38 (live bd/cot/inf) / PER-ENTITY 32 (pattern) / TAIL 8 (residual) |

**DYNAMIC FIRM-LEVEL** (38): live-confirmed across all 3 firms (getFirmLeaderboard->platinum/firm/leaderboard.json etc.).
Notable non-PASS: cot leaderboard/advisor_nna_canonical = WARN (cot platinum content-lag 2td); client_directory = inf PASS /
cot WARN (absent -> first-emits tonight, COTMVP-B) / bd WARN. **PER-ENTITY** (32): resolved to the {id} artifact pattern
(per-id live-check = follow). **TAIL** (8 residual, portal-manifest / mdpf-per-firm): enumerated w/ resolution route.

## Findings (cadence-aware, CTO-ruled)
1. **REAL-STALE x2 (one root):** `portfolios/non_model_assets.json` (frozen **2026-06-25T16:42:16**) + `mdpf/aggregate-aua-timeseries.json` (frozen **2026-06-25T16:42:42**) -- the EXACT same freeze timestamp = one **49F/Schwab non-model-asset feed freeze**. Cadence VERIFIED **daily** (siblings aum-metrics/account-distribution/aum-timeseries updated 2026-07-01T11:30Z; these two frozen). Both **fold into the MDPF basis-switch thread** (COO-routed); self-resolve on the roll-forward. (The mdpf one was surfaced by the v0.3 TAIL reclassification -- it was mis-tiered DYNAMIC.)
2. **EXPECTED-CADENCE (NOT stale) x2:** CMA `views.json` (2026-01-09) + `assumptions.json` (2026-03-11). **Andrew-confirmed yearly** -> intentional; DROPPED from the fidelity-break list per CTO ruling.
3. **GRAPH-COVERAGE-GAP (routed):** the 78 dynamic bindings are FIRM_CONFIG-grounded, not graph-grounded. CTO ruling = ENRICH in the **NFRA_TSGRAPH lane (my lane)**: model dynamic `Endpoint->Lambda->READS_S3` edges so the canonical graph carries BOTH tiers; this B1 JSON map IS the enrichment input; B2 consumes the JSON interim, migrates to the enriched graph when it lands.
4. **SCHEMA-RULE (adopted):** `expected_cadence` is a first-class map field; stale = past the artifact's OWN cadence. De-noises AC-3 (CTO: same class as ~7 gate-integrity catches this session -- a gate keying on a non-discriminating condition).

## CTO arch-gate -- ALL 4 ASKS RULED (2026-07-01)
1. **Two-tier grounding method: ACCEPTED** as the B1 spec (honest model -- grounds each binding the real way it resolves).
2. **Graph-gap: ENRICH** (scoped/sequenced, NFRA_TSGRAPH lane, B1-map-fed; does NOT block B2).
3. **JSON schema: CONFIRMED** as the B1->B2 hand-off contract -> **FROZEN at schema_version 1.0** (a change = re-RAVC).
4. **expected_cadence: ADOPTED** first-class + per-artifact cadence registry. CMA reclassified (yearly, not stale); non_model_assets cadence-verified (daily, real-stale).

## Follow (my queue, no external dep)
- **B1 tail:** ground the 32 PER-ENTITY endpoints per representative `{id}`/firm + the 8 residual TAIL (portal-manifest, mdpf-per-firm).
- **TSGRAPH enrichment (routed by CTO, my TSGRAPH lane):** add dynamic `Endpoint->Lambda->READS_S3` edges to the canonical graph, fed by this B1 map -> B2 migrates to graph-native when it lands.
