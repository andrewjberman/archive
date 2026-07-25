<task_order>
<id>NFRA_SYSPARITY.WS-3.complete-the-drift-gate-denominator</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<!-- CLOSED 2026-07-25 by 0.8.0_AE_CloudComp~A (status was STALE at `pending`; the work landed 07-19).
     Evidence: (a) @a8917afdfd -- surface_map NFRA_ONTOLOGY row now carries NFRA_ONTOLOGY_RULE_BANK.yaml +
     variance_dimensions.yaml, EXERCISED against real canonization commit 0f5ba0d92 (CLEAN before the add / DRIFT
     after); (b) whole-surface audit landed at _schema_version 3 with IN/OUT classification + reasons for
     org/modules/graph, the 39-file globgrph set and the 17 ontology deliverables, plus @322fde6327 (+6 ontology
     definition-deliverables, CTO-concurred @222113Z) and @7184e93a6d (grain_sentinel.py ambiguity->INCLUDE);
     (c) live-derived `# genesis-surface:` denominator DESIGNED + routed to CTO (design, not build, per scope).
     AC-5 CVO GATE SATISFIED: 3.0.0_SA_CVO @565729348c (20260719T1806Z) "WS-3 CLEAR -- my fire-1(c)/drift-gate-C1
     closed by seeded-FIRE (RULE_BANK+variance_dimensions now in surface, both fire rc1)". -->

<priority>P1 -- LOAD-BEARING control fix (PRD S3/S4). [CTO ARCH-GATE at build.] Closes the LD-0314 hole at its LIVE instance. Unblocked now (WS-1 landed @62b28c5fb = honest denominator). ~A owns the drift-gate; COO is drift-gate cadence-owner.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-3 = S3 third bullet)</ref>
  <ref type="ledger">org/tier0/ledger/LD-0314.md (Amendment @07c10e8d8: "a control's own denominator is live state")</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Complete the NESTEDABSTRACT drift-gate's surface_map DENOMINATOR at its live instance -- the exact LD-0314-amendment gap CVO's fire-1 caught:
(a) ADD the ratified ontology vocab to the NFRA_ONTOLOGY surface: NFRA_ONTOLOGY_RULE_BANK.yaml + variance_dimensions.yaml (canonized this session, LD-0311/0315). Today the ONTOLOGY row watches canon-patterns.yaml + AB_MATERIALIZE_SPEC only -- so a change to the RATIFIED ontology vocab passes the drift-gate UNDISPOSITIONED (the same under-inclusion class as the GLOBGRPH cse_emit_graphhead.py miss the 6-code widen already closed). CVO fire-1 confirmed this at source.
(b) AUDIT the WHOLE surface-map for other under-coverage (the recurring re-audit COO logged as a standing cadence-owner item -- the map itself needs the live-cadence discipline it enforces).
(c) DESIGN the P2.5+ path toward a LIVE-DERIVED denominator: prefer an author-declared IN-FILE marker (`# genesis-surface: <CODE>`) so the surface SELF-updates rather than being a frozen hand-list -- the denominator practicing the discipline the gate enforces (surface to CTO; do NOT build the full live-derived engine in this WS, design + route it).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read infra/system/sdk/abstraction_loop/surface_map.json (the NFRA_ONTOLOGY row + all 6 codes) + confirm RULE_BANK.yaml/variance_dimensions.yaml are org/modules/graph mechanism files absent from it</run>
      <expect>NFRA_ONTOLOGY currently maps canon-patterns.yaml + AB_MATERIALIZE_SPEC, NOT the ratified vocab. The audit (b) enumerates every code's real mechanism surface vs mapped -- print IN/OUT classifications with reasons (mechanism-DEFINITION IN / operational-USE OUT, per the ruled principle).</expect>
      <if_mismatch>N/A -- grounding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>python infra/system/sdk/abstraction_loop/drift_gate.py --self-test + seed a change to RULE_BANK.yaml and run the sweep</run>
      <expect>A SEEDED change to RULE_BANK.yaml now FIRES the drift-gate (undispositioned trigger) -- EXERCISED (the acceptance: the gate catches a ratified-vocab change it previously missed). self-test still PASS.</expect>
      <if_mismatch>STOP -- if the seeded RULE_BANK.yaml change does NOT fire, the surface add is incomplete; fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>COO runs the drift-gate cadence-sweep under the widened surface (COO cadence-owner authoritative run)</run>
      <expect>Sweep CLEAN under the widened surface (or any newly-caught undispositioned trigger surfaced); the ontology-vocab is now in the denominator. COO advances the checkpoint.</expect>
      <if_mismatch>COO dispositions any newly-caught trigger; surface to CTO if a real drift.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. surface_map NFRA_ONTOLOGY row includes NFRA_ONTOLOGY_RULE_BANK.yaml + variance_dimensions.yaml; a seeded change to RULE_BANK.yaml FIRES the drift-gate (EXERCISED).
2. The whole surface-map audited for under-coverage (print the IN/OUT classification + exclusions); any other under-inclusion added or documented.
3. The live-derived-denominator (`# genesis-surface:` marker) DESIGNED + surfaced to CTO as the P2.5+ path (design, not build).
4. CTO ARCH-GATE on the surface/denominator change (mirrors the drift-gate ruling) -- ping COO->CTO at the build gate.
5. LD-0318 CVO-VERIFIED GATE: CVO verifies the denominator-completeness (its fire-1 was the finding) per PRD S7 (cron 02d90dce). Ping CVO on land.
6. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- COO is drift-gate CADENCE-OWNER: COO runs the post-widen authoritative sweep + advances the checkpoint (do NOT self-advance; ~A builds the surface add, COO runs the cadence sweep + owns the checkpoint value). Ping COO on the surface add landed.
- ~C's WS-4 Part-A adds ontology citations to 0*_*.md (in the NFRA_SYSTEM surface) with an `abstraction-ledger: n-a` trailer -- WS-3 does NOT touch that; WS-3 is the ONTOLOGY-vocab surface (org/modules/graph files). Disjoint from ~C's citation-add.
- CTO-arch-gate flagged -- COO relays to CTO at the WS-3 build gate.
</cross_domain_coordination>

<notes>
Context-reallocation of ~A per Andrew-direct (2026-07-19): ~A owns the NESTEDABSTRACT drift-gate + just landed WS-1; WS-3 completes the
drift-gate denominator it built -- its exact continuation. This is the FIRST recurring-re-audit finding (CVO fire-1) landing in a governed
home, and it lands the COO's P2 standing-items (recurring surface re-audit + live-derived-denominator design) into WS-3. The LD-0314
amendment ("a control's own denominator is live state") is the doctrinal basis -- cite it.
</notes>
</task_order>
