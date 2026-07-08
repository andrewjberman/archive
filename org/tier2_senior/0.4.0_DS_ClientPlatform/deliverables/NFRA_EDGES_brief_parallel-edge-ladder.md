# BRIEF: NFRA_EDGES -- the parallel EDGE ladder for the SEMCTL substrate

**Author:** 0.4.0_DS_ClientPlatform~B | **Date:** 2026-07-08
**Status:** DRAFT -> CVO feedback + revision -> CTO for project creation (proposed code: NFRA_EDGES)
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
- **P3 -- C3 as subgraph.** Materialize the intra-system estate edges (not just `CONTAINS`) so a C3 carries its data-flow signature; extend the emergence connectivity to use edge-overlap as a signal alongside node-overlap.
- **P4 (optional) -- edge promotion.** The PROMOTE plane promotes a validated edge-motif to a first-class recognizer/rule (the edge-analog of node-motif promotion), through the same 5-invariant gate.

## 4. Acceptance (machine-checkable)

1. A C3 system's `decompress()` yields its edge constituents (reified `*Edge` C1 nodes) AND node constituents, each bottoming out in C0 evidence; `fidelity_check` passes on edge-nodes (a LATENT edge-node fails, same as a latent node).
2. The materialized graph for a C3 carries the intra-system `FLOWS_TO`/`RENDERS` edges (the subgraph), not only `CONTAINS`.
3. The coverage-sweep's `Relationship`+`EdgeKind` families are exercised by the reified edge-motifs (no new gap; the sweep already gates them).

## 5. Non-goals / relationship to existing

- Does NOT replace the node ladder -- complements it (the two are duals; nodes = WHAT, edges = HOW).
- Does NOT change the algebra (`Relationship`+`EdgeKind` already exist) or the fidelity gate.
- Retro-consistency: the reference firm-sep ladder is already edge-reified -- this brings the frontend MOTIF pipeline to the same bar.

## 6. Open questions for CVO (feedback requested)

- Q1: Should edge-reification be **eager** (reify every motif-defining edge at materialize) or **lazy** (reify on decompress-inspection)? Eager = a heavier store + a true subgraph; lazy = cheaper, edges stay in the estate + rule-text.
- Q2: Is a C3 "data-flow signature" a NEW node_type (like `C3System`) or a **property** of the C3 system node? (Bears on the store schema + the node_id collision discipline we just fixed.)
- Q3: Does P4 (edge promotion) belong in NFRA_EDGES or fold into NFRA_PROMOTE as a producer-kind extension?
- Q4: Grounding bar for an edge-motif's recurrence -- same AC3 (>=2) as node-motifs, or edge-specific?

**Requested of CVO:** grounding-review the problem statement (is the "frontend flattens edges" claim exact?), pressure-test the phasing, and revise -> then issue to CTO for NFRA_EDGES project creation.
