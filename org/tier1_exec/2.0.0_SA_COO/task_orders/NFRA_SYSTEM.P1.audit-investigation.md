# Task Order: NFRA_SYSTEM P1 -- AUDIT & INVESTIGATION (the load-bearing unblocker; a grounded per-scope-class fan-out)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-system-p1-audit</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>FAN-OUT (a reader per scope class -- executors audit what they built, PRD SS7): 0.4.0_DS_ClientPlatform~B (substrate + learning-loops) + 0.7.0_AE_CloudOps (graph infra) + 0.8.0_AE_CloudComp~D (comp-tools/comp-which/COMPRAIL) + 0.5.0_AE_OpalETL (federated) + 2.0.0_SA_COO~B (synthesis/interaction-map) | CTO arch-gate + CVO grounding-cert</issued_to>
    <date>2026-07-08</date>
    <status>complete -- CLOSED 2026-08-05 ~2350Z (2.0.0_SA_COO). The PROJECT completed 2026-07-08, all 4 phases CTO-arch-gate-PASSED + CVO-CERTIFIED per org/projects/NFRA_SYSTEM.json. This TO was paper the project closure never swept. Surfaced as a stale-open row by 0.4.0_DS_ClientPlatform's backlog triage (addressed to the then-non-live ~B lane); dispositioned by 0.0.0_AB_MSTR grounded on the project record before closing.</status>
    <prd_ref>docs/architecture/NFRA_SYSTEM_PRD.md (SS3 scope classes, SS4 Part-1, SS6 principles, SS9 open decisions)</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 by COO~B on Andrew's decomp directive. Fan-out per scope class so the audit is COMPREHENSIVE not thin.</dispatch_state>
    <gate_note>The knowledge is scattered (~313 docs + ~105 org/modules/graph files + agent memory). P1 grounds every component against LIVE source/state (Rule 22) -> the inventory feeds P2 (structure) / P3 (compiler) / P4 (maturity). CTO arch-gates audit-completeness; CVO certs grounded-not-recalled.</gate_note>
  </metadata>

  <objective>A comprehensive, GROUNDED (Rule 22) audit of the system AS BUILT across the 6 scope classes. Per component: real source location + current-state (built-proven / built-unproven / forming / designed-only) + dependencies/interactions + existing docs. Deliver the inventory + the cross-layer interaction map + a doc-consolidation index + an honest GAP LIST.</objective>

  <requirements>
    <requirement id="1" owner="0.4.0_DS~B">SCOPE CLASS 1 -- SUBSTRATE (C0-C3): the CSE algebra + tiers (C0 facts/C1 estate/C2 motifs/C3 systems), the compression/decompression ladder + fidelity gate (cse_schema.py @0.4, comp_ladder.py), LAW 1 (lexical-before-statistical) + LAW 2 (explicit-promotion). Ground each against live source + current-state.</requirement>
    <requirement id="2" owner="0.7.0_AE_CloudOps">SCOPE CLASS 2 -- GRAPH INFRA: Nessie/Iceberg/Kuzu (comp-kuzu), derive_runner + marker-oracle (freshness/provenance header), the node/edge/layer taxonomy (7 node-types, 6 edge-types + the semctl analysis layer), FRESHGUARD (non-delivery watchdog, per-table vintage, FinalizeS3). Ground against live.</requirement>
    <requirement id="3" owner="0.8.0_AE_CloudComp~D">SCOPE CLASS 3 -- COMP-TOOLS + COMP-WHICH: the ~30-tool catalog (graph-call-manifest.yaml + comp-coverage-map.yaml + comp-tools.yaml), comp-which selection logic, the rail (COMPRAIL) + enforcement, the tool families (trace/blast, kuzu, iam, routes, freshness/heat/drift/xray, pipescript, validate, honesty). Ground against live.</requirement>
    <requirement id="4" owner="0.5.0_AE_OpalETL">SCOPE CLASS 4 -- FEDERATED LAYER: FEDOBS (cross-producer correlation over the CSE log via in-VPC Trino), the heat map (comp-heat + object-freshness), analytics, the observe->measure axis (co-evolution, effectiveness). Ground against live.</requirement>
    <requirement id="5" owner="0.4.0_DS~B (+ 0.8.0~D GOV-B)">SCOPE CLASS 5 -- LEARNING LOOPS: COMPLEARN, MOTIF (C2/C3 discovery), PROMOTE (ratify+materialize+reverse), the closed federated-learning loop (proven 2026-07-08), GOV-A (I1/I2/I3) + GOV-B (hot-registration), the 5 PROMOTE invariants. Ground against live + the cert-ledgers.</requirement>
    <requirement id="6" owner="2.0.0_SA_COO~B">SCOPE CLASS 6 -- SYNTHESIS + the CROSS-LAYER INTERACTION MAP: assemble from classes 1-5 -- the flow C0->C1->C2->C3, how a comp-tool query routes, how an observation becomes a measure becomes a ratified promotion, how the freshness + honesty gates thread every hop. + the DOC-CONSOLIDATION INDEX (which existing doc is the deep source for what) + the honest GAP LIST (undocumented / stale / contradictory surfaces).</requirement>
    <requirement id="7">EACH class-audit: per component -> {source_location, current_state[built-proven|built-unproven|forming|designed-only], dependencies, existing_docs, grounding_citation}. NO scope class left TODO; NO current-state claim without a Rule-22 grounding cite. RAVC COO~B (I assemble the synthesis + route to CTO/CVO).</requirement>
  </requirements>

  <cross_domain_coordination>
    - Surface the 4 OPEN DECISIONS (PRD SS9) to CTO as P1 grounds them: Q1 comp-system home / Q2 static-vs-dynamic boundary / Q3 maturity taxonomy / Q4 refresh cadence.
    - CONSOLIDATE don't duplicate (PRD SS6): index the ~313 docs as the deep source; the audit is the synthesis + gap-list, not a re-copy.
    - Grounds P2 (structure) + P3 (compiler) + P4 (maturity). It is the unblocker.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Every component in all 6 scope classes inventoried with source + current-state + grounding citation (Rule 22). No class TODO.
    2. The cross-layer interaction map is complete + source-grounded; the doc-consolidation index maps deep-source docs; the gap list is honest (built-but-unproven labeled as such -- GOV-A).
    3. CTO arch-gate (audit-completeness) + CVO cert (grounded-not-recalled -- no aspirational current-state). RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
