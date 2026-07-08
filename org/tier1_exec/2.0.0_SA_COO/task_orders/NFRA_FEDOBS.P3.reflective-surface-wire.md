# Task Order: NFRA_FEDOBS P3 -- the reflective surface + wire the measured signals as standing inputs to PROMOTE + MOTIF

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-fedobs-p3</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL (surface) + 0.4.0_DS~A (query library, gated)</issued_to>
    <date>2026-07-07</date>
    <status>dispatched -- GO'd 2026-07-08 by COO~B to 0.5.0_AE. FEDOBS-P2 measure arm CLOSED+certed (7735815e3) = the signals P3 surfaces are live+certed. Build the reflective surface + wire the standing inputs NOW; it does NOT gate on the fedobs-role apply (that's the AC2 crown-jewel, parallel).</status>
    <prd_ref>docs/architecture/NFRA_FEDOBS_PRD.md (P3)</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 to 0.5.0_AE (surface) + DS~A (query library, gated). Builds on the live+certed P2 measure library. This is the standing-input wiring PROMOTE (measure arm) + MOTIF (co-occurrence) consume.</dispatch_state>
    <gate_note>Gated on FEDOBS-P2. Makes the measured signals STANDING inputs so PROMOTE/MOTIF consume them continuously (not a one-off query).</gate_note>
  </metadata>

  <objective>Package the observation library (P2) as queryable reflective observations -- a comp-tool / dashboard so agents + humans can ask the reflective questions -- and WIRE the directive-effectiveness + compiler-coverage signals as the STANDING inputs to NFRA_PROMOTE, and co-occurrence as the standing input to NFRA_MOTIF.</objective>

  <requirements>
    <requirement id="1">A queryable surface (a comp-tool, e.g. `comp-fedobs` / reflective-observations, following the comp-tool convention) exposing the S4.2 reflective questions over the CSE log + runtime graph.</requirement>
    <requirement id="2">Directive-effectiveness + compiler-coverage wired as STANDING inputs to NFRA_PROMOTE (the measure-arm + post-promotion monitor); co-occurrence wired as the standing input to NFRA_MOTIF.</requirement>
    <requirement id="3">Every observation is inspectable + provenance-linked back to its CSEs (the decompression chain holds through the surface).</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_FEDOBS.P2: the measured signals this TO surfaces. HARD PREREQUISITE.
    - NFRA_PROMOTE.P1/P3: consumes directive-effectiveness as its measure/monitor arm.
    - NFRA_MOTIF.P1/P3: consumes co-occurrence.
    - comp-tools rail (NFRA_COMPROUTE/COMPRAIL): register the new comp-tool in the graph-call-manifest so it's on-rails.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. PROMOTE can query a measured directive-effect via the standing surface (live rows).
    2. MOTIF can query co-occurrence via the standing surface (live rows).
    3. The comp-tool is registered on the rail + returns provenance-linked observations.
    4. RAVC COO~B + CC CTO; CVO verifies the standing wiring actually feeds PROMOTE/MOTIF (exercise, not config-read).
  </acceptance_criteria>
</task_order>
```
