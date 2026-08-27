<to_id>NFRA_TSGRAPH.P3-2</to_id>
<project>NFRA_TSGRAPH</project>
<title>P3-2 -- frontend bug/logic detectors on the NFRA_TSGRAPH graph, each EMPIRICALLY-VALIDATED against its log-anchored exemplar</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>3.0.0_SA_CVO (P3-1 catalog author -- the exemplar anchors); 1.0.0_SA_CTO (empirical-gate wording refinement, offered section-9)</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; 2b61ac87e)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_TSGRAPH is complete; this TO was last touched 2026-06-18, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>HIGH -- GATED on P3-1 (detectors anchor on the catalog's frontend partition + exemplars). The empirical-validation gate is the defining bar.</priority>

<gate>P3-1 <status>complete</status> (catalog frontend partition + per-class exemplar incidents delivered). COO GOes after P3-1 RAVC2.</gate>

<scope>
For each FRONTEND-detectable class in the P3-1 catalog, author the canonical comp-*/Cypher detector on the NFRA_TSGRAPH graph (Rule 20: QUERY, never rebuild): OFC cohort/ternary fork (guarded FLOWS_TO/RENDERS), cross-firm conditional asymmetry, silent-display-fork, `any`-erosion, dead-code, prop-drill-depth, hook-dep-mismatch, render-guard-vs-nullability. Kuzu build lacks SPLIT() -- author without it.
EMPIRICAL-VALIDATION GATE (the defining bar, CTO-flagged): EACH detector MUST catch its known log-anchored exemplar -- the catalog names a real instance, the query MUST find it. A detector that does not catch its exemplar is NOT accepted (theoretical detectors are rejected). CTO offered per-class anchor-wording refinement at GO -- take it.
</scope>

<compiler_tools_mandate>
  <phase id="2" when="before commit"><step><run>comp-kuzu -- run each detector query; comp-blast if a detector keys on a shared predicate</run><expect>Each detector returns its log-anchored exemplar instance (empirical catch, not 0 rows / not theoretical).</expect><if_mismatch>STOP. A detector that does not catch its exemplar fails the gate -- fix the query or re-scope the class with CVO/CTO.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>Consumes P3-1's frontend partition (CVO). FRONTEND ONLY -- the cross-domain classes are NOT built here; they route to NFRA_DEBTSCAN (Andrew-locked boundary). Detectors ride the live P1/P4/P2 graph.</cross_domain_coordination>

<acceptance_criteria>1. A detector for every frontend-detectable class in the catalog. 2. EMPIRICAL GATE: every detector catches its log-anchored exemplar (cited instance found by the query) -- not theoretical. 3. Frontend-only (no cross-domain scope-creep). 4. Session-log Compiler Tools reproduces each detector <run> + the exemplar-catch evidence. RAVC2 to COO (CC CTO).</acceptance_criteria>

<dependencies><dependency project="NFRA_TSGRAPH" task="P3-1" status="staged"/></dependencies>
<references><ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9</ref></references>
<lane_note>DE-primary (graph detectors). Full mandate-triad + per-class exemplar anchors finalize at GO (depend on P3-1 catalog). COO GOes post-P3-1; pull CTO's empirical-gate wording refinement.</lane_note>
