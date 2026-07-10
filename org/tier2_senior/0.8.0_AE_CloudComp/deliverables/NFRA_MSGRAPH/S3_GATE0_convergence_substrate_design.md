# NFRA_MSGRAPH S3 GATE-0 — convergence-substrate binding design (heat as a DIMENSION, not a surface)

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26 | **TO:** NFRA_MSGRAPH S3/S5 re-scope (COO `e8485eabf`)
**Gate:** CTO **decision-#6 convergence arch-gate** (gates decision #2 — heat generalization). **No heat code until this is arch-gated.** RAVC → [1.0.0_SA_CTO]; CC [2.0.0_SA_COO] + [3.0.0_SA_CVO] (debtscan/comp-dups owner).
**Scope:** DESIGN ONLY (no-code GATE-0). Grounds the existing debtscan/comp-dups/graph_nodes model, then specifies the unified per-node health record MS-heat lands ON.

---

## 1. Why this gate exists (the CTO COND-B ruling, verbatim intent)

CTO arch-GO 194857Z, COND B (load-bearing): *"node-health is ONE surface; heat is a DIMENSION of it. Unify (i) SUBSTRATE — one materialization home; (ii) DATA MODEL — one per-node health record {reachable, duplicated, heat_band, cold_since, cost} with comp-dups/comp-heat/comp-debtscan as LENSES; (iii) TOOL FAMILY — comp-heat/comp-ms-find/comp-debtscan in the same comp-* family + manifest, as comp-dups already is."* This **replaces** PRD §4.2's standalone `ms_object_subtree_heat` table.

So the gate's question is NOT "how do we compute heat" — it is **"what is the one per-node health record, and how do the existing debt/dups/heat/cost producers converge onto it without standing up a parallel surface."**

## 2. Grounded current state (what exists today — cited, not assumed)

| Component | What it IS today | Citation |
|---|---|---|
| `graph_nodes` record | 6 FIXED keys `{id, arn, type, name, layer, drift_class}` + an additive `props` JSON column (no-silent-drop invariant). MS nodes carry `layer='ms'`, `source='ms'`. | `infra/aws/globgrph/derive_runner.py:202` (`_NODE_FIXED_KEYS`) + `_props_and_guard` |
| canon-motif scorecard | A pattern-**CLASS** census — `AUTH_CANON` / `DEPLOY_CANON` / `SERVED_LINEAGE_CANON` / `PIPELINE_CANON`, each scoring shape-deviation CANDIDATES. **Node-blind** (organized by deviation family, not by node id). | `infra/aws/globgrph/canon_motif_scorer.py` (comp-canon-motif live scorer) → dated ledger `infra/aws/globgrph/debtscan/canon_motif/<day>.json`. **RE-POINTED 2026-07-10:** the retired `debtscan_canon_scorer.py`/`debtscan_scorecard_latest.json` was superseded by the productized thin scorer; NFRA_MSGRAPH had no live consumer of the old `_latest.json` (0.7.0_AE_CloudOps CM1 delete, my clear). All 4 classes present, canonical-graph-grounded. |
| debtscan findings | D8-shape graded findings ledger (family, severity, firm-scope, triage-state, owner-routed), dated files. **Finding-centric.** | `org/modules/graph/debtscan/*.md`; PRD-request `docs/briefs/nfra-debtscan-prd-request-20260612.md` §4 |
| comp-dups | The dups DIMENSION engine (`dup_scan.py`), advisory/read-only; emits a finding-LIST by class (CROSS_FIRM / IAM_POLICY_SPLIT / SERVICE_SPLIT / ENV_TWIN) + nightly `dups_latest.json`. **Finding-list, not a per-node attribute.** | `.tools/comp-dups` → `org/modules/graph/debtscan/dup_scan.py` |
| heat (to build) | Reuse `org/modules/heatmap` S0+O1, domain-parameterized (COO directive — NO fork). | COO `e8485eabf` |

**THE CRUX (the real finding):** debtscan + comp-dups today are **finding-centric** (lists of deviations, by family). COND B wants a **node-centric** record (one row per node: is THIS node reachable / duplicated / hot-or-cold / costly). These are duals, but the substrate does not exist yet — there is **no per-node health table**. GATE-0's job is to specify it and make the finding-families its PRODUCERS.

## 3. The unified per-node health record (the one data model)

A NEW, **additive** Iceberg table `node_health` in the SAME Nessie warehouse as `graph_nodes` (one materialization home — COND B(i)). Keyed by `node_id` (joins 1:1 to `graph_nodes.id`). One row per node, layer-agnostic (AWS + MS + portal alike):

```
node_health (
  node_id        STRING   -- FK -> graph_nodes.id (the join key; never mutates graph_nodes)
  layer          STRING   -- aws | ms | portal  (denormalized for cheap lens filters)
  reachable      BOOLEAN  -- from the reachability sweep (dead-path forward/backward)
  reachable_why  STRING   -- trace/owner hint when reachable=false (never auto-delete; PRD 3a doctrine)
  duplicated     STRING   -- null | CROSS_FIRM | IAM_POLICY_SPLIT | SERVICE_SPLIT | ENV_TWIN  (comp-dups class)
  dup_set_id     STRING   -- the dup cluster this node belongs to (null if unique)
  heat_band      STRING   -- HOT | WARM | COLD | DORMANT  (write-activity banding; MS+AWS)
  cold_since     STRING   -- ISO date of last activity when COLD/DORMANT (null if HOT/WARM)
  cost           DOUBLE   -- monthly $ attributable to the node (null where not cost-bearing)
  debt_flags     STRING   -- JSON: the deviation families this node trips (auth/deploy/canon/layer) as a LIST
  scored_at      STRING   -- derive timestamp (Nessie snapshot gives the time axis)
)
```

- `reachable`, `duplicated`, `heat_band`, `cold_since`, `cost` are exactly the CTO's five named fields. `debt_flags` carries the EXISTING class-census deviations as a per-node projection (so the current scorecard is not lost — it becomes a lens, §4).
- **It is a SEPARATE table** — `graph_nodes` is never widened or mutated. That is what makes COND A mechanical (§5).

## 4. Producers → record → lenses (how convergence actually works)

**Producers (existing families write the node record — they do NOT each own a table):**
- reachability sweep (PRD 3a) → `reachable` + `reachable_why`
- `dup_scan.py` / comp-dups (PRD 3b) → `duplicated` + `dup_set_id`
- heat (new, `org/modules/heatmap` reused) → `heat_band` + `cold_since` (banding `graph_nodes`/MS `last_modified_dt` write-activity)
- cost-recon (debtscan D4 cost lane) → `cost`
- canon/auth/deploy/layer censuses (the current scorecard classes) → `debt_flags`

**Lenses (the comp-* family READS the one record — COND B(iii)):**
- `comp-debtscan` → `WHERE debt_flags != '[]' OR reachable=false` (the deviation view)
- `comp-dups` → `WHERE duplicated IS NOT NULL` (today's finding-list, now a projection of the record)
- `comp-heat` (new) → `WHERE heat_band IN ('COLD','DORMANT')` / heat distribution
- `comp-ms-find` (new, the S4 deliverable) → `WHERE layer='ms' …` over the SAME record + the MS graph

"One surface, not three" = one `node_health` table, many comp-* lenses. comp-dups stops being a silo and becomes a lens over the shared record — its current engine becomes a producer that writes the `duplicated` column instead of a standalone ledger.

## 5. COND A compliance (additive 0-diff on the certified graph) — mechanical

- `node_health` is a NEW table; the first heat/health materialization writes ONLY new tables. `graph_nodes` / `graph_edges` are **read-join only, never mutated**.
- **Gate:** reuse the AWS-superset invariant already instrumented for L6 (`e99a1a601`): on the first health-enabled derive, assert `graph_nodes` / `graph_edges` are **byte-identical** to the certified pre-health snapshot (same snapshot-id / row counts / a structural sample). MS/health is purely additive — same proof shape as the MS-extract additive-only cert (`test_superset_when_enabled`). If the certified graph diffs at all, fail closed, do not commit.

## 6. COND B compliance — explicit mapping

| COND B clause | This design |
|---|---|
| (i) one SUBSTRATE / materialization home | `node_health` Iceberg table in the SAME Nessie warehouse as `graph_nodes` (not a side-car store; CTO decision #4 = materialized Iceberg tables) |
| (ii) one per-node health RECORD | the §3 schema — the five named fields co-resident per `node_id`, debt as `debt_flags` |
| (iii) one comp-* TOOL FAMILY + manifest | comp-debtscan / comp-dups / comp-heat / comp-ms-find all lens the one record; register all in `graph-call-manifest.yaml` in the debtscan family, as comp-dups already is |

## 7. MS-heat is just a layer on the same record

MS file-object nodes (`layer='ms'`) get `heat_band` + `cold_since` from `last_modified_dt` (already emitted by `ms_cloud_extract._item_node`) — the identical banding the AWS nodes get. No MS-specific heat table (PRD §4.2 `ms_object_subtree_heat` is RETIRED per the ruling). The pseudo-RAG / index (decision #4) reads `node_health ⋈ graph_nodes` as materialized Iceberg, queried via the (feasibility-only, decision #3) Trino SQL path — no bolt-on store.

## 8. Open questions for the CTO arch-gate

1. **Migrate vs feed:** does the current finding-centric scorecard/ledger fully MIGRATE into `node_health.debt_flags`, or stay as a parallel finding-ledger that ALSO writes the node record? (I lean: the node record is canonical; the dated ledger becomes a rendered VIEW of it, preserving the burn-down/`graph_metrics` time-series.)
2. **heat_band thresholds:** HOT/WARM/COLD/DORMANT day boundaries — propose from the `org/modules/heatmap` S0 defaults, CTO ratifies.
3. **cost for MS nodes:** AWS nodes have a cost source; MS file-objects likely `cost=null` day-one (storage cost not per-object attributable) — confirm null-is-fine vs a site-level allocation.
4. **dup_scan refactor:** comp-dups currently emits its own `dups_latest.json`; converging it to WRITE `node_health.duplicated` is a real refactor of the CVO-owned engine — coordinate authoring lane (CVO owns `dup_scan.py`).

## 9. What this gate does NOT do

- No heat code, no `node_health` build, no `dup_scan` refactor until CTO arch-gates this binding. This is the design only.
- Does not touch the MS re-target (separately STAGED, `f861a238e`, deploy held til L6) or `graph_nodes` (COND A keeps it certified-untouched).

**Net:** the convergence is achievable as a single additive `node_health` table keyed by node id, with the existing debt/dups/heat/cost families as producers and the comp-* tools as lenses — satisfying COND A (additive 0-diff) and COND B (one substrate / one record / one family) without a parallel heat surface. RAVC → CTO for the decision-#6 arch-gate.
