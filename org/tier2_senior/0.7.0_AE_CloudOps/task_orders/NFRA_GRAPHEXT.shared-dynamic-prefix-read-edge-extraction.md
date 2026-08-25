# TASK ORDER — NFRA_GRAPHEXT (shared dynamic-prefix-read edge extraction)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "NFRA_GRAPHEXT" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>MEDIUM (prevention-tier, shared dep) — CTO-ruled single-owner. Central graph-extractor capability serving BOTH comp-diff (edge-axis) AND comp-drift (consumer_evidence completeness). Sequence behind your live work (provisioning/cot); it's a shared P1 dep, not a fire.</priority>
<date>2026-06-29</date>

## Context

CTO ruled (212133Z) you own this single shared enhancement (COO lean confirmed). The graph extractor today MISSES dynamic-prefix reads: INF_D_00's holdings read (`load_latest_X` / `list_objects(Prefix=CONST)`) was INVISIBLE to the extractor -> the graph couldn't point at the inf freeze (no edge from INF_D_00 to the frozen input). That blind spot is why the freeze hid from every graph-based tool.

This is a CENTRAL graph-extractor capability, NOT a comp-diff-private fix. It serves BOTH:
- **comp-diff** (NFRA_COMPDIFF.P1, 0.8.0): the edge-axis consumes the new edges (which producer feeds which consumer's frozen input).
- **comp-drift** (NFRA_COMPDRIFT): the disposition safety rule — `no modeled consumer -> UNVERIFIABLE-CONSUMER, never auto-ABANDONED` (the abandoned-vs-genuine discipline, Andrew-direct) DEPENDS on the edge set being COMPLETE. A missed dynamic-prefix edge would mis-classify a genuinely-consumed resource as abandoned (a false-gap, the exact class we're disciplining).

Centralizing here = ONE enhancement both tools consume; folding it into comp-diff would duplicate + drift it.

## Objective

Enhance the graph extractor to capture dynamic-prefix / latest-pointer reads (`load_latest_X`, `list_objects(Prefix=CONST)`, `glob`/manifest-driven reads) as producer->consumer EDGES, so the graph's edge set is complete enough that (a) comp-diff can trace a frozen input to its consumer, and (b) comp-drift can safely apply the no-modeled-consumer disposition.

## Scope

- Extend the extractor's read-detection to recognize the dynamic-prefix / latest-pointer patterns (not just literal-key reads): `load_latest_*(prefix)`, `list_objects(Prefix=<const>)`, manifest/glob-driven reads. Emit each as an edge (consumer-node -> the prefix/producer-node it reads).
- Ground the patterns against the REAL blind-spot source: INF_D_00.portal_aggregates.py's reads (base-DS knows them) — confirm the enhanced extractor now emits the INF_D_00 -> {its inputs} edges that were missing. Use that as the acceptance fixture.
- Conform to the graph node/edge schema + the drift-record contract (CTO's). Don't break the existing literal-key extraction (regression-check the current edge set).

<compiler_tools_mandate>
- Verify against the REAL graph (NEVER#7): after the enhancement, re-extract + confirm the INF_D_00 dynamic-prefix edges now EXIST in the graph (the blind spot is closed) — not just "the code parses the pattern".
- from __future__ import annotations; ds-commit-gate; no emojis/non-ASCII.
- comp-which / the graph-extractor lane tooling; ground the patterns in actual source, not invented.
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: ruled the single-owner + owns the graph schema/drift-record contract. RAVC.
- 0.8.0_AE_CloudComp: CONSUMES this for the COMPDIFF P1 edge-axis — coordinate the edge-record shape so its edge-axis reads cleanly. (0.8.0's other P1 axes + the freeze-monitor proceed in PARALLEL — only its edge-axis waits on you.)
- 0.4.0_DS_ClientPlatform (base-DS): knows INF_D_00's reads (the acceptance fixture) — confirm the missing edges with them.
</cross_domain_coordination>

<acceptance_criteria>
1. The extractor captures dynamic-prefix / latest-pointer / manifest-glob reads as producer->consumer edges (pattern set grounded in real source).
2. VERIFIED on the INF_D_00 fixture: the previously-missing INF_D_00 -> {frozen-input} edges now EXIST in the re-extracted graph (the blind spot that hid the inf freeze is closed). NEVER#7 — check the real graph, not the parse.
3. No regression to the existing literal-key edge set.
4. Edge-record shape coordinated with 0.8.0 (COMPDIFF edge-axis consumer) + conforms to the graph schema / drift-record contract. RAVC me + CC CTO + 0.8.0 + MSTR.
</acceptance_criteria>

## Note
Prevention-tier shared dep — sequence behind your live work (provisioning/user-data + cot/COTETL). It UNBLOCKS only 0.8.0's COMPDIFF edge-axis (the freeze-monitor + the other cheap axes don't wait on it). One enhancement, both tools consume centrally — the anti-duplication win CTO centralized for.
