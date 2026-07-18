# TASK ORDER: NFRA_ONTOLOGY.AB-MAT-S1 -- DS~B: extend NFRA_MOTIF_P1 catalog to emit the 13 canonical A+B motif detectors + materialize C2/C3

<task_order id="NFRA_ONTOLOGY.AB-MAT-S1">
<issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<closure date="2026-07-18">APPLIED-CLOSED by CTO 210214Z, grounded at CTO's own comp-kuzu (nodes_snap 1276252256517924052, a 4th independent grounding). C2 accepted @fbfa06590; C3 re-emit @c7048f484 (overlapping-domain-cover, 3 systems object-data/compute-orchestration/pipeline); ADDITIVE ingest (debt layer preserved, C3System=4). Producer arn-index fix (78a5fddbe) recovered C2->C1 edges 79%->99.96% (5077/5079; 2 misses = confirmed estate drift, not id-space bug). Verified live FOUR ways: CVO round-trip cert PASS (@205653Z) + ~C re-census CONFORM (@203144Z) + DS~B resolve PASS (@202957Z) + CTO independent grounding. All 3 CTO semctl materialize-producer invariants confirmed (filed NFRA_SEMCTL @8e96ebf5f; +auto-classifier #2-hardening ruled in 210214Z). LANDMARK: the estate's FIRST canonical motif+system layer (13 motifs + 3 operational overlapping systems; previously 0 canonical / 1 degenerate debt-system), under ratified ontology LD-0311. Chain: DS~B emit + 0.7.0 ingest/root-cause/fix + ~C cover-model + CVO decisive drift-discrimination + COO run-ownership. The desired-vs-applied gate caught a silent 21% edge loss the emit alone would have shipped as 100%.</closure>
<date>2026-07-18</date>
<priority>HIGH -- Andrew-direct NFRA headline (A+B materialization); CTO SoD gate OPEN (msg 140326Z); chain step 1 of 4; DS~B live+idle, start now.</priority>

<references>
  <ref type="spec">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_AB_MATERIALIZE_SPEC.md @7892f3fbc (BINDING -- the 13-detector vocabulary/detector spec, ~C-authored, CTO arch-gated SOUND: 13 recurrence-backed typed-path detectors, scan-grounded 2026-07-18T02:18Z)</ref>
  <ref type="cto-gate">CTO routing+acceptance msg 20260718T140326Z (SoD gate OPEN + 2 exercised acceptance conditions + hard guardrail)</ref>
  <ref type="precedent">the 07-08 debt materialize path (semctl-c2c3-materialize) + org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_MOTIF.P1.absorb-detectors-c2-catalog.md</ref>
  <ref type="catalog">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_MOTIF_P1_c2_catalog.py (your P1 catalog, currently DEBT-only A1-A9)</ref>
</references>

<objective>
Extend NFRA_MOTIF_P1_c2_catalog (or a canonical sibling) to emit the 13 canonical A+B motif detectors per spec @7892f3fbc -- Plane A Cloud/IAM/Serve x9 (a-store / a-access / a-table / a-grant / a-event / a-api / a-serve / a-watch / a-orch) + Plane B Pipeline/Data x4 (b-struct / b-run / b-io / b-dataflow). Then run it + P2 emergence over the FRESH graph to emit the motif_c2c3_materialize.json-analog (C2Motif/C3System nodes + CONTAINS edges; candidate C3 systems ~3-5 operational vs the 1 degenerate debt-system today). A+B planes FIRST (Andrew-direct). This is graph-COMPLETENESS (make discovered structure queryable), NOT a PROMOTE (motif->first-class recognizer stays separately human-ratified + measure-gated -- keep them distinct).
</objective>

<hard_guardrail>
Canonical motifs materialize into the graph ONLY through the governed semctl promotion (the motif_c2c3_materialize path). NEVER hand-write a C2Motif/C3System node -- MSTR doctrine, CTO enforces as semctl owner (a hand-written node is a forged compression layer). If NFRA_MOTIF_P1_c2_catalog is exec-locked: STAGE the extension, an EXEC lands it (the atomic-bundle/single-editor precedent). SURFACE any block to COO -- do NOT split around the gate.
</hard_guardrail>

<compiler_tools_mandate>
  <phase id="1" when="before write/emergence run">
    <step>
      <run>comp-kuzu-inc  # ensure the local graph projection is fresh before the P2 emergence run</run>
      <expect>Fresh/current-vintage projection; provenance header is NOT "UNKNOWN VINTAGE" and NOT a frozen scratch DB. Emergence runs over the current estate.</expect>
      <if_mismatch>STOP. Refresh first (comp-kuzu-full if the incremental is insufficient). A stale graph emits a stale materialization.</if_mismatch>
    </step>
    <step>
      <run>Confirm C2Motif + C3System are already in NODE_TYPE_LAYER (from the 07-08 debt materialize) -- NO new node_type introduced by this extension</run>
      <expect>Both node types present. No new node_type => derive_runner.py relabel_layers_by_node_type fail-closed gate (~:1497) will NOT trip on 0.7.0 ingest (CTO acceptance condition 2).</expect>
      <if_mismatch>STOP. A new node_type = re-freeze risk. Surface to CTO before emitting.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before handoff to 0.7.0 ingest">
    <step>
      <run>NODE-ID RESOLVE self-check (CTO acceptance condition 1 -- the 07-08 comp-kuzu correctness trap): verify emitted C2->C1 CONTAINS edges use the discriminator-STRIPPED node_id form and resolve to NON-ZERO rows against the estate store</run>
      <expect>The discriminator-stripped form resolves to the EXISTING estate store node; COUNT the resolving edges and state the denominator. The `c1:D{n}:` form resolves to 0 rows (latent nodes) -- that form is WRONG.</expect>
      <if_mismatch>STOP. Do NOT hand off. CONTAINS edges resolving to 0 rows IS the 07-08 comp-kuzu correctness trap ~C flagged. Fix the node_id form first.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after emit">
    <step>
      <run>Report emitted-layer evidence: motif_c2c3_materialize.json-analog path + C2Motif node count + C3System candidate count + CONTAINS edge count + the Phase-2 resolve-count/denominator</run>
      <expect>13 A+B detectors emitted; C3 systems > the 1 degenerate debt-system; resolve-count NON-ZERO with denominator stated.</expect>
      <if_mismatch>Surface the gap to COO before signaling done.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
- The extended catalog emits ALL 13 canonical A+B detectors per spec @7892f3fbc (not the DEBT A1-A9 only).
- motif_c2c3_materialize.json-analog emitted through the governed promotion path (C2Motif/C3System nodes + CONTAINS edges); ZERO hand-written nodes.
- CTO acceptance condition 1 EXERCISED (not asserted): C2->C1 CONTAINS edges use the discriminator-stripped node_id form + resolve to NON-ZERO rows; resolve-count + denominator stated. (0.7.0/CVO re-exercise this on ingest -- your self-check is the FIRST gate.)
- CTO acceptance condition 2 confirmable: no new node_type (no re-freeze).
- Session-log Compiler Tools section reproduces EVERY <run> above with observed result + explicit pass/fail vs <expect>. Missing rows = REWORK.
- Emitted-layer evidence reported to COO for the 0.7.0-ingest handoff.
</acceptance_criteria>

<chain>
Step 1 (THIS TO): DS~B build/emit -> Step 2: 0.7.0 ingest (dual-sign, same path as the debt materialize; COO spawns 0.7.0 via MSTR on your emit) -> Step 3: CVO round-trip cert incl. re-exercise of the resolve-count (COO spawns CVO via MSTR) -> Step 4: 0.8.0_AE_CloudComp~C verifies the materialized A+B layer against spec @7892f3fbc. COO owns the run + the 0.7.0/CVO wake coordination + signals CTO the emitted-layer evidence (resolve-count + CVO cert) to close the materialization gate.
</chain>
</task_order>
