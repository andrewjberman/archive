# BRIEF: NFRA_EDGES -- the parallel EDGE ladder for the SEMCTL substrate

**Author:** 0.4.0_DS_ClientPlatform~B | **Date:** 2026-07-08
**Status:** CVO-REVIEWED (grounding-review 2a6a8a3a0 -- SOUND + CTO-ready; deltas folded) -> issuing to CTO for project creation (proposed code: NFRA_EDGES)
**Proposed home on creation:** `docs/briefs/nfra-edges-*.md` or `docs/architecture/NFRA_EDGES_PRD.md` (CTO's call)
**Origin:** Andrew-flagged 2026-07-08 -- the C0->C3 ladder tracks NODES; the EDGE axis is missing a parallel ladder. Grounded in the /verify + NFRA_SYSTEM class-1 substrate audit.

---

## 1. The problem (grounded)

The SEMCTL compression ladder (C0 fact -> C1 estate -> C2 motif -> C3 system) is **node-biased in the frontend MOTIF pipeline**. Ground truth:

- **The algebra ALREADY treats edges as first-class.** `cse_schema` gates THREE co-equal primitive families -- `Entity`, `Relationship` (`CLOUDEDGE_TO_RELATIONSHIP`), and `EdgeKind` (`{passthrough, rename, recompute_guarded}`). An edge is a typed, provenance-carrying, governed primitive with a `kind` + optional `condition` (the guard), swept co-equally with entities (`NFRA_CSE_P2_coverage_sweep.py`).
- **The REFERENCE ladder reifies edges correctly.** `comp_ladder.py` has ONE `Node` type across all layers (`:42-50`); a relationship is reified as a Node whose `children` = its endpoints + evidence. `build_firm_sep_ladder` builds `DeniedEdge`/`AllowedEdge` as C1 edge-nodes (`:119-139`), and the C2 motif `FirmSeparation = allowed(own) AND denied(all others)` is **defined entirely over edges** (`:142-147`). Edges climb the ladder identically to nodes and pass the same `fidelity_check`.
- **The frontend MOTIF pipeline FLATTENS the defining edges.** The D1-D7 motifs are edge-patterns (D1 = ">=2 guarded FLOWS_TO into one sink"), but in `motif_c2c3_materialize.json` the C1 constituents are the **sink NODES** (`out:...ClientsTab:291#name`), not reified `FlowsToEdge` nodes. The `FLOWS_TO` edges -- and their `EdgeKind` + guard `condition` (i.e. *how the data flows*) -- survive only as text in the motif `rule` string + the C0 `evidence`. The only edges materialized up the ladder are the **structural `CONTAINS`** rungs, never the **semantic** estate edges.

**Consequence:** a C3 system is really a **subgraph** (member nodes + the FLOWS_TO/RENDERS edges among them), but we materialize only its **node-skeleton**. "firm-conditional-display" records *that* 3 motifs belong together (node overlap on `ClientsTab:291#name`), but NOT *why in flow terms* (firm-literal -> guarded-fork -> display-sink). This is a completeness/expressiveness gap, not a correctness bug.

## 2. The proposal: reify the edge ladder into the existing Node model (NOT a new structure)

The edge ladder is the SAME ladder -- edges ride it via reification. No new fidelity gate, no new store type; extend the MOTIF/materialize pipeline to lift the defining edges into first-class rungs.

| Tier | Node axis (WHAT participates) | **Edge axis (HOW it's wired) -- to build** |
|---|---|---|
| **C0** | node lexical fact (`ClientsTab.tsx:291 #name`) | the **flow fact** -- the exact source line of the relationship + its `condition` ("`= firm ? recompute(x) : y`") |
| **C1** | estate node (`out:...#name`) | reified **`FlowsToEdge`/`RendersEdge`** node: children = `{src, sink, C0-flow-fact}`, carries `EdgeKind` + `condition` |
| **C2** | node-motif (recurring sink pattern) | **edge-motif** -- the recurring edge CONFIGURATION (the "guarded-fork": >=2 guarded FLOWS_TO converging), a subgraph pattern |
| **C3** | system (bag of member motifs) | the system's **data-flow SIGNATURE** + the intra-system estate edges -> the C3 becomes a real **subgraph** |

## 3. Proposed phasing (for CTO decomposition)

- **P1 -- edge reification in the MOTIF ladder.** Lift the motif-defining `FLOWS_TO`/`RENDERS` edges into C1 `*Edge` Nodes (reusing `comp_ladder.Node`, `ntype=*Edge`, children = endpoints + a C0 flow-fact carrying `EdgeKind`+`condition`). Prove on `firm-conditional-display`: it decompresses to BOTH node AND edge constituents, all grounded to C0, `fidelity_check` green.
- **P2 -- C2 edge-motifs.** The D1-D7 detectors emit the edge-configuration as a first-class edge-motif (the guarded-fork subgraph), not just its sink node. Recurrence + fidelity apply unchanged.
- **P3 -- C3 as subgraph.** Materialize the intra-system estate edges (not just `CONTAINS`) so a C3 carries its data-flow signature; extend the emergence connectivity to use edge-overlap as a signal alongside node-overlap. **The collision-safe C3 node_id is (re)computed AFTER final membership (node + edge overlap) settles** -- edge-overlap changes membership -> changes the member-set hash (correct), but the id must be computed once membership is final so it stays stable per the final member set.
- **P4 (optional, FOLDS into NFRA_PROMOTE -- Q3) -- edge promotion.** A validated edge-motif promotes via the EXISTING NFRA_PROMOTE 5-invariant gate as a new `ProducerKind` (not a new mechanism). Scoped OUT of NFRA_EDGES core (P1-P3 = reification); tracked as a NFRA_PROMOTE extension.

## 4. Acceptance (machine-checkable)

1. A C3 system's `decompress()` yields its edge constituents (reified `*Edge` C1 nodes) AND node constituents, each bottoming out in C0 evidence; `fidelity_check` passes on edge-nodes (a LATENT edge-node fails, same as a latent node).
2. The materialized graph for a C3 carries the intra-system `FLOWS_TO`/`RENDERS` edges (the subgraph), not only `CONTAINS`.
3. The coverage-sweep's `Relationship`+`EdgeKind` families are exercised by the reified edge-motifs (no new gap; the sweep already gates them).
4. **(collision-safe ids -- MANDATORY, CVO Ask#2)** Every NFRA_EDGES-materialized node_id (`*Edge` C1 nodes, edge-motif nodes, any new C3-subgraph node) is **unique-by-construction from its defining tuple** (a stable hash: `FlowsToEdge <- hash(src, sink, edge_type, condition)`; edge-motif <- its canonical edge-set), NEVER a reused label -- inheriting the collision-safe discipline of the C3 node_id fix (f875bc854). A self-test proves two DISTINCT edges/edge-motifs sharing a label yield DISTINCT node_ids (else the store-side MERGE silently collapses them -- the exact corruption f875bc854 fixed).
5. **(freshness contract -- cross-project AC, CVO)** All NFRA_EDGES-materialized entities conform to the `CloudNode`/`CloudEdge` schema + carry the `snapshot_ts` producer-stamp (the batch_ts guarantee), so the incremental-kuzu-refresh + reconcile-oracle drift-safety (`kuzu_incremental_refresh.py`, CVO-certed this session) COVERS them -- else NFRA_EDGES is born drift-blind. Bind to the freshness contract from day one.

## 5. Non-goals / relationship to existing

- Does NOT replace the node ladder -- complements it (the two are duals; nodes = WHAT, edges = HOW).
- Does NOT change the algebra (`Relationship`+`EdgeKind` already exist) or the fidelity gate.
- Does NOT re-open the C3 collision fix (f875bc854) -- it EXTENDS the same unique-by-construction id discipline to edge entities (AC4).
- Retro-consistency: the reference firm-sep ladder is already edge-reified -- this brings the frontend MOTIF pipeline to the same bar.

## 6. Design decisions (RESOLVED -- CVO grounding-review 2026-07-08, record 2a6a8a3a0)

- **Q1 reification eager-vs-lazy -> HYBRID.** Reify EAGERLY only the intra-system edges of a MATERIALIZED C3 (P3's bounded scope -- where the subgraph earns its store cost); LAZY (reify-on-decompress) everywhere else. Bound the eager set to materialized-C3 membership (eager-everything bloats the store with every estate `FLOWS_TO`; lazy-everywhere loses the queryable subgraph).
- **Q2 data-flow signature -> a PROPERTY of the C3 node** (not a new node_type -- fewer collision surfaces; the C3 node already carries a collision-safe id). Distinction: edge-MOTIFS (P2) materialized as nodes DO need collision-safe node_ids (AC4); intra-system EDGES (P3) are `CloudEdge`s keyed on edge-identity, not node_ids.
- **Q3 edge-promotion (P4) -> FOLDS into NFRA_PROMOTE as a new `ProducerKind`** (not a new promotion mechanism). NFRA_EDGES stays scoped to reification (P1-P3); P4 becomes a NFRA_PROMOTE extension -- avoids duplicating the 5-invariant gate.
- **Q4 edge-motif recurrence bar -> START at AC3 (>=2), tunable in P2.** Same >=2 as node-motifs for launch; re-tune edge-specific in P2 IF the edge-configuration recurrence distribution proves sparser/noisier (an edge-config is a higher-order pattern -- may recur less). Measure in P2, don't pre-optimize.

## 7. Provenance
DS~B draft (b878feb1d) -> CVO~B grounding-review (2a6a8a3a0: flatten-claim confirmed grounded-exact, phasing sound, AC4 + freshness-AC5 mandated, Q1-Q4 dispositioned) -> this revision folds all deltas -> **CTO-ready for NFRA_EDGES project creation** (Andrew-directed path 2026-07-08).
