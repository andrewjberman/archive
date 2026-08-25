# Task Order: NFRA_SYSTEM P3 -- the comp-system COMPILER (org/modules/graph -> infra/system/06_current_state, the runtime index)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-system-p3-compiler</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D (comp-tool lead, org/modules/graph -- built the class-3 inventory the compiler aggregates) | CTO arch-gate (grounded-against-live) + CVO cert (no-fabricated-current-state)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_SYSTEM is complete; this TO was last touched 2026-07-08, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: staged -- GO'd (base COO LOCALROOT-P2 CTO-GO 225633Z closes SYSTEM-P2 + unblocks P3). Sequence AFTER ~D wraps TOOLCHECK P3 (imminent -- the HUD). Coordinate with base COO's LOCALROOT-P3 (the index reuses this compiler's 06 output).</status>
    <prd_ref>docs/architecture/NFRA_SYSTEM_PRD.md (Part 3 runtime-compiled current-state) + the class-6 synthesis + CTO Q1/Q2 rulings + NFRA_LOCALROOT-P2 (c345f4038, the index reuses 06)</prd_ref>
    <gate_note>THE HARD LINE (CTO, arch-gate-verified on P2): 06_current_state is the DYNAMIC half -- it MUST ground against LIVE state (comp-kuzu / comp-freshness / marker-oracle), auto-refresh on HEAD-advance, NEVER self-report or hand-fabricate numbers. The P2 stub already documents this contract; P3 fills it from grounded live state.</gate_note>
  </metadata>

  <objective>Build the comp-system COMPILER (a comp-tool in org/modules/graph) that reads the LIVE compiled-system state across the 5 scope classes + emits infra/system/06_current_state -- the runtime current-state (the dynamic half of the SYSTEM home) that ALSO serves as the LOCALROOT runtime index (one source, two consumers). Grounded against live; auto-refreshing on HEAD-advance.</objective>

  <requirements>
    <requirement id="1">READ LIVE STATE per scope class (via the existing comp-tools -- do NOT build new readers): the graph (comp-kuzu: node/edge counts, C1/C2/C3 tier populations, the materialized C2/C3 nodes); freshness (comp-freshness + the marker-oracle: per-table vintage, the FRESHGUARD leg-3/4/5 alarm state); comp-tool health (the NFRA_TOOLCHECK verification matrix / comp-tool-health: works/broken/retired per tool); cert status (the CVO cert ledger); the materialized-recognizer inventory (the PROMOTE-materialized recognizers live in the graph).</requirement>
    <requirement id="2" priority="THE HARD LINE -- grounded-against-live, no fabrication">every number in 06_current_state is GROUNDED against live (the comp-tool output / the served artifact / the marker-oracle), NEVER self-reported or hand-fabricated (CTO's arch-gate line, the 06 grounding-rule the P2 stub documents). If a source is unavailable, 06 marks it UNKNOWN-VINTAGE, never invents. AUTO-REFRESH on HEAD-advance (the marker-oracle pattern, like comp-kuzu's re-finalize-on-advance).</requirement>
    <requirement id="3">WRITE to infra/system/06_current_state (CTO Q1: compiler in org/modules/graph, output to 06). Output is exec-committable per base COO's infra/system/** carve (LOCALROOT §4 governance rule) -- COO~B commits the compiler's output. The compiler CODE lives in org/modules/graph (comp-tool lane).</requirement>
    <requirement id="4" priority="LOCALROOT coordination">the 06_current_state output IS the LOCALROOT runtime index (base COO LOCALROOT §5 REUSES it -- no second index mechanism). Coordinate with base COO's LOCALROOT-P3 so the 06 output-shape serves BOTH consumers (SYSTEM P4-maturity grading + the LOCALROOT runtime index). One source of runtime current-state, two consumers.</requirement>
    <requirement id="5">register the compiler in the comp-tool catalog (graph-call-manifest / comp-coverage-map) as a comp-tool (e.g. comp-system) -- it's a first-class comp-tool; the TOOLCHECK health axis then covers it too.</requirement>
  </requirements>

  <acceptance_criteria>
    1. The compiler emits 06_current_state GROUNDED against live (spot-verify: the counts/freshness/certs/recognizers MATCH live state via comp-kuzu/comp-freshness, NOT fabricated -- a fabricated number is a hard-fail, CVO's cert target); auto-refreshes on HEAD-advance; marks UNKNOWN-VINTAGE where a source is unavailable.
    2. The 06 output serves both SYSTEM P4-maturity + the LOCALROOT runtime index (coordinated with LOCALROOT-P3). Registered as a comp-tool. CTO arch-gate (grounded-against-live, the same discipline as the C3-materialize) + CVO cert (no-fabricated-current-state). RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
