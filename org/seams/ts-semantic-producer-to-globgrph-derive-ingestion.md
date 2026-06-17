# SEAM: ts-semantic producer JSON  ->  globgrph derive ingestion -> Iceberg/Kuzu   (scale: MESO)
**archetype:** VALIDATE
**seam-run:** 2026-06-17 by 0.7.0_AE_CloudOps (/seams on own Leg B work) · marker HEAD 243790a7

## Seam definition
- **Side A (producer):** the DE's ts-morph full-portal extractor -> `s3://opal-313476888478-globgrph/producers/ts-semantic/portal_full.json` (corrected/seams-repaired vintage, 11130 nodes / 12911 edges / 639 unresolved; gen 2026-06-17T20:00Z).
- **Side B (consumer):** globgrph derive ingestion -- `derive_runner.ingest_ts_semantic_producer` -> `graph["classes_data"]["ts_semantic"]` (+ `graph["edges"]`) -> `commit_to_iceberg` -> Iceberg `graph_nodes`/`graph_edges` -> comp-kuzu canonical `CloudNode`/`CloudEdge`.
- **Boundary / contract (as recorded):** node `{id, type, ...props}` / edge `{source, target, edge_type, ...props}` + `coverage.unresolved`; "string node_type/edge_type discriminators on the existing CloudNode/CloudEdge -- NO schema change" (my RAVC2s 192324Z/210745Z + COO Leg B GO 200139Z hard-constraint).
- **Scale:** MESO (one producer->consumer handoff; boundary = the S3 producer JSON + the Iceberg/Kuzu schema).

## Axis verdicts
| Axis | Verdict | Evidence | Delta (if FAIL) |
|---|---|---|---|
| MECHANICAL  | **PASS** (post-fix) | Live: Iceberg `ICEBERG_NODES_WRITTEN=12397` + `ICEBERG_EDGES_WRITTEN=15938` (3027 AWS + 12911 ts_semantic); comp-kuzu current @ 243790a7, 12397n/15618e; counts match the corrected producer exactly (DE co-verify: FLOWS_TO 714 / RENDERS 2447 / PROP_PASSES 1382 / FETCHES 109); intra-portal stitch traverses `hook -FETCHES-> Endpoint -READS_URL-> ServedURL`. | run-1 had a MECHANICAL break -- ALL ts_semantic edges dropped (edges placed in `classes_data["ts_semantic"]["edges"]` but `commit_to_iceberg` reads `graph["edges"]` top-level). Caught + fixed (0d8ef8920); run-2 landed 15938. Now PASS. |
| DECLARATIVE | **FAIL** | Live Kuzu `CALL TABLE_INFO('CloudEdge')` = {edge_type, layer, snapshot_ts}; `CloudNode` = {node_id, arn, node_type, name, layer, drift_class, source, snapshot_ts}. The recorded contract ("node {id,type,...props} / edge {source,target,edge_type,...props}, no schema change") has NO landing place for the `...props` half. | **believed** the full producer shape (incl props) ingests with "no schema change / matches the reads exactly"; **actually** only the fixed columns land -- the existing schema has no generic props column, so every non-fixed key silently drops. Map != territory. |
| SEMANTIC    | **FAIL** | Live CloudEdge carries NO `kind`/`condition` (the FLOWS_TO payload: passthrough\|rename\|recompute/guarded + the ternary gate); CloudNode carries no `tsType`/`ownerType`/etc. Structure + counts + types present + valid -- but the meaning that distinguishes the semantic graph from regex is absent. | right shape, **missing semantic payload**: the FLOWS_TO kind/condition (CTO P1 note #2 display-logic-bug lever + the AC5 forked-FLOWS_TO mechanism) dropped -> kind-aware comp-transform re-back (Leg C) + goal-3 analyses BLOCKED. Highest-value catch class (counts-match MASKED the drop). |

## Knowledge-parity delta
- **BELIEVED:** the ts-semantic producer ingests fully into CloudNode/CloudEdge with no schema change -- the producer shape "matches the reads exactly" (my repeated RAVC2 claim).
- **TRUE (live):** only the fixed columns land; ALL non-fixed props (edge kind/condition/srcField/dstField/via/resolution, node tsType/ownerType/optional/path/line) are SILENTLY dropped by `commit_to_iceberg` -- masked by counts-match (the no-silent-Unknown invariant violated one layer down, at the SCHEMA seam).
- **RECORD CORRECTED:** CTO revised the Leg B constraint (214828Z): "no BREAKING/restructuring schema change; ADDITIVE non-breaking columns ARE permitted to carry required payload (additive-safe migration)." The deeper banked lesson: NO SILENT DROP AT THE SCHEMA SEAM -- the fix is not just "add props" but `commit_to_iceberg` must assert any key that can't land is a LOUD coverage-error, never silent.
- **ROUTED/GO'd (owning lane = mine, derive):** additive `props STRING` JSON column on CloudNode+CloudEdge + the no-silent-drop assert + comp-kuzu loader (json_extract) + the binding live test (etf_spread recompute/guarded FLOWS_TO carries kind+condition from live Kuzu). In-progress (task #12).

## Verdict
**BROKEN@SEMANTIC** (with DECLARATIVE drift, both now corrected-on-record + GO'd-for-repair). The mechanical connection physically carries the structure (post the run-1 edges fix); the payload it carries is incomplete -- the semantic content that justifies the project drops at the schema seam.

## Residual / unknowns
- Props fix (props column + assert + loader + etf_spread test) GO'd, NOT yet implemented -- the SEMANTIC axis flips to PASS only when a live FLOWS_TO row carries kind+condition via comp-kuzu json_extract.
- Cross-domain `ServedURL -> S3 -> Lambda-ARN` join = a SEPARATE follow-on leg (CTO 210944Z; the DE's recorded coverage.unresolved) -- the intra-portal half of the stitch traverses; the full fine-lineage does not yet. Not this seam's defect; a documented boundary.
- D8-FP surface-scan (re-exercised by the same derive run) = SOUND (3-case live re-test ALL PASS, by-construction baseline) -- a sibling seam, separately closed.

## Compiler Tools
| tool | axis | result |
|---|---|---|
| `comp-kuzu CALL TABLE_INFO('CloudEdge'/'CloudNode')` | DECL/SEM | live schema = fixed columns only, no props -> confirmed the silent drop against ground truth (not self-report) |
| `comp-kuzu MATCH ...-[:FETCHES]->... / Endpoint out-edges` | MECH | intra-portal stitch traverses to ServedURL; stops there (cross-domain join = follow-on) |
| derive CloudWatch log (ICEBERG_NODES/EDGES_WRITTEN, SURFACE_SCAN findings=0) | MECH | structure + counts landed; edges-fix verified vs run-1's 0 |
