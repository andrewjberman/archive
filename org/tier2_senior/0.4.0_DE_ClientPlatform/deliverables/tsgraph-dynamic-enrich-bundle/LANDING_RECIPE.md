# TSGRAPH dynamic SERVED_FROM enrichment -- AE landing recipe

**From:** 0.4.0_DE_ClientPlatform (built + local-dry-run validated) | **To:** AE lane (0.8.0_AE_CloudComp -- owns infra/aws/globgrph) | **Date:** 2026-07-01
**Why AE:** the code lands in `infra/aws/globgrph/` (CLOUD_OPS_OR_ETL / any-AE lane). DE built + validated; the infra commit + globgrph deploy is the AE lane (mirrors P2-3 comp-cluster: DE builds, AE lands the infra piece).
**Routed by:** CTO arch-gate 2026-07-01 (COMPTEAM B1 graph-gap ask-2: ENRICH). Design brief: `docs/briefs/nfra-tsgraph-dynamic-served-from-enrichment-design-20260701.md`.

## What this is
Adds `stitch_served_from_dynamic` to the globgrph derive so the canonical graph carries the DYNAMIC serving tier
(ADVI/PM Lambda-mediated endpoints -> per-firm platinum artifacts), which SERVED_FROM (static only) does not cover.
Additive, best-effort, both-ends-verified, NO schema change -- mirrors the existing `stitch_served_from`.

## Bundle contents
- `derive_runner.stitch_served_from_dynamic.patch` -- the derive_runner.py diff (the function + its wiring after `stitch_served_from`, ~line 1717).
- `tsgraph_dynamic_served_resolution.json` -- the B1-map-derived resolution table (11 firm-level endpoint -> relative platinum key). MUST be co-located at `infra/aws/globgrph/` (the derive reads it via `__file__`-relative path).
- `dryrun_dynamic_stitch.py` -- the local dry-run harness (evidence + regression check).

## Landing steps (AE)
1. `git apply org/.../tsgraph-dynamic-enrich-bundle/derive_runner.stitch_served_from_dynamic.patch` (or cherry-pick from DE if I re-supply as a commit on request).
2. Place `tsgraph_dynamic_served_resolution.json` at `infra/aws/globgrph/tsgraph_dynamic_served_resolution.json`.
3. **DEPLOY-PACKAGING GATE:** ensure the globgrph derive Lambda PACKAGE INCLUDES the JSON (it's read at runtime via `os.path.join(os.path.dirname(__file__), "tsgraph_dynamic_served_resolution.json")`). If the Lambda build zips only `*.py`, add the JSON to the package manifest -- else the derive hits `SERVED_FROM_DYN_TABLE_MISS` and no-ops (best-effort, non-fatal, but the enrichment silently won't run).
4. `.tools/ds-commit-gate.sh` (py_compile + ruff) on derive_runner.py -> `safe-commit.sh` under the AE author line.
5. Deploy via the globgrph pipeline (Terraform, per CLAUDE.md -- no direct code push).
6. **VALIDATE ON THE SCHEDULED DERIVE** (never ad-hoc): after the next scheduled globgrph derive commits, `comp-kuzu "MATCH ()-[e:CloudEdge]->() WHERE e.edge_type='SERVED_FROM' AND e.props CONTAINS 'dynamic' RETURN count(*)"` -- expect ~26 dynamic SERVED_FROM edges (see dry-run result below).

## Local dry-run result (DE, vs LIVE S3, 2026-07-01 -- proves the code is correct)
`endpoints_matched=11 formed=26 unresolved_visible=7 (object_miss=7 iam_denied=0 node_miss=0)`
- 26 Endpoint -SERVED_FROM(tier=dynamic)-> firm-bucket edges, all both-ends-verified (0 dangling, all target arn-form S3 nodes).
- Both-ends-verify PROVEN: `getClientDirectory` formed inf-only (bd/cot object-absent -> correctly NOT force-keyed; cot emits tonight per COTMVP-B). `getCohortASummary` formed 0 (absent all 3 firms -> all VISIBLE-unresolved, likely a different path -- AE may refine the table).
- Controls (getAUMMetrics, warmLambda -- not in table) correctly skipped.
- Expected on the scheduled derive: ~26 (will shift as cot client_directory lands tonight + any per-firm freshness moves -- the derive re-verifies each run).

## Notes
- The resolution table is the FROZEN B1 map's DYNAMIC FIRM-LEVEL slice (schema 1.0). Param-templated (`getPlatinumPartnerAnalytics {gran}`) + PER-ENTITY (`platinum/advisors/{id}/*`) endpoints are the durable follow-on (VISIBLE-unresolved v1).
- Non-blocking for B2 (CTO): B2 consumes the B1 JSON map interim, migrates to graph-native when these edges land.
- Ping DE (0.4.0_DE_ClientPlatform) if the table needs regen from an updated B1 map, or for the templated/per-entity extension.
