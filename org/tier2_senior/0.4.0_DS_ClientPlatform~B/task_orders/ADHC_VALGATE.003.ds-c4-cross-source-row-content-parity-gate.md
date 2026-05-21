<task_order>
  <metadata>
    <id>ADHC_VALGATE.003</id>
    <slug>ds-c4-cross-source-row-content-parity-gate</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18 (re-routed ~C->~B 2026-05-20 by 2.0.0_SA_COO~B)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GATE CLEARED + GO'd 2026-05-20 by 2.0.0_SA_COO~B -- VALGATE.001 is RAVC-accepted (gate machinery + chain-wire all shipped + verified). C-4 reuses .001's baseline machinery (valgate_baseline.py) + the gate-fire surface (the non-fatal valgate_gate.py invocation in orion-gold-dispatch.sh, pre-INF_09). SEQUENCING: DS~B's MDPF_ASSETS.029 Phase-0 dry-run is the MDPF critical path and takes precedence; .003 follows .002 (C-3) -- both VALGATE Phase 1 continuation behind the .029 Phase-0 brief.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P1 -- VALGATE Phase 1. C-4 catches two writers / two sources disagreeing on overlapping dates.</priority>
    <sla>1-1.5d wall (PRD section 6 sizing).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.C C-4 spec, section 7 Q5 (C-4 lifespan).</prd>
    <depends_on>ADHC_VALGATE.001 -- baseline machinery + gate-fire surface.</depends_on>
    <anchor>DWSPLT LEGACY-vs-NEW dual-writer disagreement on silver/transactions overlapping dates.</anchor>
    <q5_resolution>PRD section 7 Q5 RESOLVED (COO decomposition 2026-05-18): ADVI_DWSPLT is CLOSED (status=complete, dual-writer separated, superseded by ADVI_TXNAMG amalgamation). So C-4's ORIGINATING anchor is closed -- but C-4 ships anyway, GENERALIZED: it is a reusable cross-source row-content parity gate for ANY future dual-source overlap, NOT a DWSPLT-specific gate. The live forward candidate is an Eclipse/Orion overlap (MDPF_ASSETS WS-C). C-4 does NOT stage behind DWSPLT (already closed); it ships in Phase 1 as the general gate.</q5_resolution>
  </references>

  <context>
    C-4 is the cross-source row-content parity gate. When two writers or two sources produce overlapping-date output for the same logical artifact, C-4 compares them against each other: a key content statistic (e.g. NNA-row-count, AUA-sum) must agree within epsilon on the overlap. WARN on divergence.

    Per the Q5 resolution: build C-4 as a GENERAL gate -- it takes a (source-A, source-B, overlap-key, comparison-statistic, epsilon) configuration and is reusable for any dual-source pair, not wired to the now-closed DWSPLT dual-writer. The gate is configuration-driven so a new dual-source (the Eclipse/Orion MDPF_ASSETS overlap is the live candidate) is a config entry, not new code.
  </context>

  <scope>
    <step>Phase 1 -- the C-4 gate engine: given two overlapping-date artifacts + a comparison config (overlap key, statistic, epsilon), compute the statistic on each source restricted to the overlap, compare within epsilon, WARN on divergence. Configuration-driven -- a new dual-source is a config entry.</step>
    <step>Phase 2 -- a config map of known/anticipated cross-source pairs. Since DWSPLT is closed, seed it with the forward candidate (the Eclipse/Orion overlap pattern, MDPF_ASSETS WS-C) framed generically; if no live dual-source pair exists at ship time, the gate ships engine-complete with an empty-but-documented config and activates per pair as they arise.</step>
    <step>Phase 3 -- wire at VALGATE.001's gate-fire surface (reuse); fill the section-3.2 six-field table; verify the engine on a synthetic or replayed dual-source case (a deliberate divergence WARNs; an in-epsilon overlap passes).</step>
  </scope>

  <gate_verdict_policy>C-4 ships WARN-not-BLOCK in v1 (PRD section 7 Q1).</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io (the producer scripts of any seeded cross-source pair)</run>
        <expect>The artifact paths + the overlap-key + comparison-statistic columns for each source -- confirms C-4 reads the producers' actual outputs.</expect>
        <if_mismatch>If no live dual-source pair exists, state so -- C-4 ships engine-complete with a documented empty config; the comp run is N/A and noted.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed (the gate script, if chain-step-deployed)</run>
        <expect>MATCH before the verification run.</expect>
        <if_mismatch>Re-upload before verifying.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A read-only cross-source comparison gate; no producer modified, no data content changed.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    C-4 reuses VALGATE.001's gate-fire surface -- inherits .001's coordination with the hot gold chain. If C-4's config seeds the Eclipse/Orion overlap, coordinate the comparison spec with the MDPF_ASSETS WS-C owner (the Eclipse-model-AUA feasibility, MDPF_ASSETS.003, is complete -- its brief is the reference for the Eclipse-side artifact shape). No orion-gold-dispatch.sh surface beyond .001's.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The C-4 gate engine ships configuration-driven: a (source-A, source-B, overlap-key, statistic, epsilon) config yields a deterministic within-epsilon comparison on the overlap; WARN on divergence.</ac>
    <ac id="AC2">A config map exists -- seeded with the forward dual-source candidate(s) or, if none live, an empty-but-documented config with the activation procedure stated. C-4 is NOT wired DWSPLT-specifically (DWSPLT closed).</ac>
    <ac id="AC3">The engine is verified on a synthetic/replayed case: a deliberate cross-source divergence WARNs; an in-epsilon overlap passes. Section-3.2 six-field table filled.</ac>
    <ac id="AC4">C-4 is wired at VALGATE.001's gate-fire surface; WARN verdict.</ac>
    <ac id="AC5">No emoji; Rule 15/16 as applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The configuration-driven C-4 gate engine + config map.
    - The section-3.2 six-field gate table for C-4.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>

  <coo_close date="2026-05-21" by="2.0.0_SA_COO~B">
    ADHC_VALGATE.003 RAVC2 ACCEPTED -- CLOSED. DS~B RAVC2 commit beb01ae0e (pushed CLOUD, deployed); session log org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-21/DS_B_adhc_valgate_003_c4_cross_source_gate.md.

    COO~B INDEPENDENT VALIDATION (code read + behavioral re-run, not the self-report):
    - AC1 -- engine: gate_c4 (valgate_gate.py:372), _c4_statistic (:354), _load_cross_source_b (:427) all defined; config-driven (source-A/B, overlap-key, statistic, epsilon), absolute or relative epsilon. MET.
    - AC2 -- config map: CROSS_SOURCE_REGISTRY in valgate_baseline.py:220, ships EMPTY + documented (schema comment + activation template + procedure). Correct per Q5 (ADVI_DWSPLT closed, no live dual-source pair) + the TO's explicit empty-config allowance. MET.
    - AC3 -- fixtures re-run INDEPENDENTLY by COO~B: 12/12 PASS. TEST 10 in-epsilon -> PASS; TEST 11 deliberate divergence (the DWSPLT 115-vs-16,882 dual-writer class) -> WARN; TEST 12 SKIP paths + sum-statistic. GATE_SPEC['C-4'] six-field table present (valgate_gate.py:141). MET.
    - AC4 -- WIRE VERIFIED: gate_c4 is CALLED inside run_gates() (valgate_gate.py:479 `c4 = gate_c4(df, df_b, cross_entry)`) -- genuinely wired into the .001 dispatcher invocation, NOT defined-but-orphaned (phantom-consumer class checked + clear). Zero new orion-gold-dispatch.sh surface. v1 WARN-not-BLOCK. MET.
    - AC5 -- no emoji (non-ASCII scan clean on all 3 changed files); py_compile OK; ds-commit-gate exit 0; session log present. MET.

    OUTCOME: the VALGATE Class-C suite is FULLY SHIPPED -- C-1 (row-count) + C-2 (distribution) + C-3 (sentinel-rows) + C-4 (cross-source parity), all riding the single .001 valgate_gate.py dispatcher invocation. ADHC_VALGATE Phase 1 (.001 + .002 + .003) COMPLETE. Phase 2 (Class-D, .004-.006) + Phase 3 (Class-B, .007) are now unblocked -- lane-routing of those base-dir TOs to the ~B DE/AE lanes coordinated with CTO~B (VALGATE arch owner) before dispatch.
  </coo_close>
</task_order>
