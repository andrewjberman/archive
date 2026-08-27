# Task Order: NFRA_SYSTEM P3 -- RUNTIME-COMPILED CURRENT-STATE (the comp-system compiler; current-by-construction)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-system-p3-compiler</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D or 0.4.0_DS_ClientPlatform~B (graph/comp-tool lane -- the compiler lives with the other comp-tools) + 1.0.0_SA_CTO (arch-gate the compiler design) + 3.0.0_SA_CVO (cert reads-live-truth-not-aspirational)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_SYSTEM is complete; this TO was last touched 2026-07-08, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: staged -- GO after P1 + P2. The load-bearing DIFFERENTIATOR (static architecture + runtime-compiled current-state).</status>
    <prd_ref>docs/architecture/NFRA_SYSTEM_PRD.md (SS4 Part-3, SS6 current-by-construction, SS9 Q1/Q2/Q4)</prd_ref>
    <dispatch_state>STAGED. Gated on P1 (what to compile) + P2 (where the output lives). Q1 lean: the compiler lives in org/modules/graph (with the tools), its OUTPUT lives in infra/system/06_current_state/ -- CTO rules Q1 as P1 grounds.</dispatch_state>
    <gate_note>CURRENT-BY-CONSTRUCTION: a stale current-state is a DESIGN failure, not a maintenance lapse. Mirrors the comp-tool philosophy -- the substrate is the source of truth; the doc reads FROM it.</gate_note>
  </metadata>

  <objective>Build the comp-system current-state compiler -- it reads the LIVE substrate (manifest for the tool catalog, marker-oracle for graph state, the graph for node/layer/cluster counts, cert-ledgers for maturity, tool_activity for usage) and emits the current-state (provenance-headed like comp-kuzu), regenerable on demand -- so the current-state is CURRENT BY CONSTRUCTION.</objective>

  <requirements>
    <requirement id="1">comp-system compiler: reads the live surfaces (manifest / marker-oracle / graph / cert-ledgers / tool_activity), emits the current-state with a provenance header (source + vintage per section, like comp-kuzu). Per Q2: compile every COUNT/STATE/FRESHNESS/CERT (volatile); the how-it-works stays hand-written (P2, stable).</requirement>
    <requirement id="2">The current-state doc it produces lives in infra/system/06_current_state/ (regenerable), each dynamic section CITING its live source.</requirement>
    <requirement id="3">Per Q4 (CTO rules): refresh cadence -- on-demand + optionally a scheduled regenerate + a drift-alarm if the P2 static docs contradict the compiled current-state.</requirement>
  </requirements>

  <acceptance_criteria>
    1. Each dynamic section cites its live source; re-running the compiler reflects a REAL change (a new tool, a new graph layer, a cert flip). A stale section is impossible-by-construction (generated, not written).
    2. CVO certs the compiler reads LIVE TRUTH, not an aspirational snapshot (exercise: change a live surface -> re-run -> the current-state moves). CTO arch-gate (compiler design). RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
