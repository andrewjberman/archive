# TASK ORDER — NFRA_GRAPHUNI.P2 + P3 (re-point + retire = the unification payoff)

<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>
<!-- COMPLETE 2026-07-01 (0.8.0_AE_CloudComp~D) -- (b)-interim per JOINT VERDICT (CTO ruling + CVO~B fixture-bar). P2 read-handle comp_marker_read.py (dfad285bf/42b7f3c48, GRAPHDEPTH P3 composes). Re-point = (b) HEAD-PINNED build_graph (NOT literal Kuzu -- (a) deferred, coverage-equivalence-gated): 4 structure tools head-pinned (cli.py e0d839996 + graph_cache 70ff64a56) + the producer (extract_gold_compute 57518fc3a) -- the actual phantom source. CVO~B (b) re-point cert GREEN (150e0b8b4, 0 regression). D3 = no cache-DELETE under (b) (head-pinned cache IS the source). D4 one-head asserted -- test PASSING (org/modules/graph/tests/test_graphuni_headpin_d4.py, exec-land routed to CVO~B, AE-lane-blocked). Residual: D4-test SoD-land + COO~B 2-step close + (a) coverage-equivalence follow-on (CVO~B-gated). -->

<priority>HIGH — Andrew-direct close-out drive (2026-07-01). P1 (D1-fill) is COMPLETE + CVO-ACCEPTED (Phase-B derive landed, CVO~B L3 GREEN 5fc0bce73, marker 5434137157015633165). This is the UNIFICATION PAYOFF -- and it structurally kills the stale-cache-phantom class we just caught on the Phase-B derive. You're the registered GRAPHUNI build lane.</priority>
<date>2026-07-01</date>

## Context
NFRA_GRAPHUNI: ONE graph / ONE marker-published HEAD / every structure-tool reads the Kuzu projection AT that head. PRD: `docs/architecture/NFRA_GRAPHUNI_PRD.md` (5 rulings). Map: `org/projects/NFRA_GRAPHUNI/SUBSTRATE-CLOSEOUT-MAP.md`. P0 (D1-audit + CVO frozen fixture) + P1 (D1-fill, the Phase-A+B population) DONE. P2 (D2 re-point) + P3 (D3 retire + D4 assert) are the remaining close-path.

## WHY THIS IS LOAD-BEARING
The Phase-B derive nearly folded a PHANTOM (deleted script INF_D_00e) because ~D's tooling read a STALE `.comp-graph/graph.json` LOCAL cache at a pre-reboot vintage. D2/D3 is the structural fix: re-point every tool onto the ONE marker head + retire the local caches -> no tool can ever again read a stale divergent vintage.

## Objective
P2 (D2): stand up ONE shared marker-headed read-API + re-point the structure tools onto it. P3 (D3+D4): retire the local caches + comp-build's separate build, and ASSERT one-head. CVO-gated no-regression throughout.

## Scope
1. **P2 / D2 -- ONE shared read-API (ruling 2: extend the `comp-kuzu` path, NOT per-tool):** a marker-headed read surface all structure-tools call. Re-point comp-blast / comp-trace / comp-xref / comp-platinum off their `.comp-graph/graph.json` LOCAL-cache reads onto the marker-head projection. re-point-THEN-retire (ruling 3, CVO-gated).
2. **P3 / D3 -- retire:** remove the local `.comp-graph/graph.json` caches + comp-build's separate build once every tool reads the marker head. No tool left reading a private vintage.
3. **P3 / D4 -- assert one-head:** the generalized seam-4 in the read-API (ruling 4) asserts every read is AT the marker head (provenance-checked). D4 also threads as a COMPDRIFT seam AC (rides).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>locate every tool's `.comp-graph/graph.json` local-cache read (comp-blast/trace/xref/platinum + comp-build) + confirm CVO~B's pre-delta FROZEN FIXTURE (the no-regression control captured P0)</run>
      <expect>The local-cache read sites enumerated; the frozen fixture exists + is the set-equality baseline. The marker-head read path (comp-kuzu) is the extension point.</expect>
      <if_mismatch>STOP. If the frozen fixture is missing, coordinate with CVO~B BEFORE re-pointing (the no-regression control is load-bearing per the CVO-owned risk).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>the re-pointed tools vs the frozen fixture (set-equality) + ds-commit-gate + non-ASCII</run>
      <expect>Re-pointed comp-blast/trace/xref/platinum return the SAME answers as the pre-delta frozen fixture (NO-REGRESSION, the load-bearing risk); ds-gate clean; ASCII-only.</expect>
      <if_mismatch>STOP. A re-point that changes a tool's answer is a regression -> do NOT retire the cache; reconcile the delta with CVO~B first.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>D4 one-head assertion: every structure-tool read is AT the marker head (provenance-checked) + retire the local caches</run>
      <expect>0 tools reading a non-marker vintage; local `.comp-graph/graph.json` caches retired; D4 assertion passes. The stale-cache-phantom class is now structurally impossible.</expect>
      <if_mismatch>Fix before RAVC. A tool still reading a local cache = the exact gap this closes.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 3.0.0_SA_CVO~B: OWNS the no-regression frozen fixture + set-equality gate (re-point-THEN-retire is CVO-gated, ruling 3). Her set-equality GREEN authorizes the retire. This is the GRAPHUNI close-verify.
- 1.0.0_SA_CTO: PRD rulings (esp. 2 = one-shared-read-API-not-per-tool; 4 = D4 generalized-seam-4). RAVC.
- NFRA_COMPDRIFT (CLOSED): D4 threads as a COMPDRIFT seam AC -- the one-head assertion is a drift check.
- NFRA_GRAPHDEPTH: its P3 (depth-scoped tooling) reads THIS unified substrate -- coordinate the read-API so depth-scoping composes.
</cross_domain_coordination>

<acceptance_criteria>
1. ONE marker-headed shared read-API (comp-kuzu-path extension, not per-tool); comp-blast/trace/xref/platinum re-pointed onto it, off their local caches.
2. NO-REGRESSION verified: re-pointed tools return the SAME answers as CVO~B's pre-delta frozen fixture (set-equality GREEN).
3. Local caches + comp-build's separate build RETIRED; D4 one-head asserted (0 tools reading a non-marker vintage). The stale-cache-phantom class structurally eliminated.
4. Session log Compiler Tools section reproduces every run. RAVC COO~B + CC CTO + CVO~B -- CVO~B's set-equality + D4 GREEN closes GRAPHUNI (with GRAPHDEPTH P3).
</acceptance_criteria>

## Note
The unification payoff + the structural fix for the stale-cache class. re-point THEN retire (never retire a cache a tool still reads). CVO-gated no-regression is the whole risk control. On this + GRAPHDEPTH P3 + CVO~B GREEN, GRAPHUNI + GRAPHDEPTH close.
