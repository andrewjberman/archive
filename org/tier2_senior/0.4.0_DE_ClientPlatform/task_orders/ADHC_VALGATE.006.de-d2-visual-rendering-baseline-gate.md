<task_order>
  <metadata>
    <id>ADHC_VALGATE.006</id>
    <slug>de-d2-visual-rendering-baseline-gate</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-18</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-18 (COO decomposition of ADHC_VALGATE PRD v0.1). Phase 2 -- gated on VALGATE Phase 1 (.001-.003). ALSO: PRD section 7 Q4 (the D-2 mechanism) is a Phase-0 step OF THIS TO -- DE 0.4 confirms the mechanism before the build. COO flips to pending + fires GO when Phase 1 closes + DE 0.4 lane has capacity.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P2 -- VALGATE Phase 2. Lower than .004/.005: D-2's mechanism is the least-settled of the suite (PRD section 7 Q4) and full screenshot-diffing is explicitly NOT the recommended path.</priority>
    <sla>1.5-2.5d wall (PRD section 6 -- mechanism-dependent; the structural-assertion variant is the lighter, recommended end).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.D D-2 spec, section 7 Q4 (D-2 mechanism -- structural-assertion variant recommended over pixel-diffing), section 3.2 gate anatomy.</prd>
    <anchor>INFFIN 8-defect arc -- empty bell-curves rendered structurally-empty; firm-aggregate where advisor-scoped was expected.</anchor>
    <frontend_dev>The /frontend-dev per-page constitution machinery (portal/.frontend-dev/testing/) -- the recommended substrate for the structural-assertion variant.</frontend_dev>
  </references>

  <context>
    D-2 is the visual-rendering-vs-partner-portal-baseline gate. Input: a rendered partner-facing panel. Reference: a stored baseline of that panel. Comparison: structural emptiness (empty histogram, "--" hero card) + scope drift (firm-aggregate where advisor-scoped expected). Verdict: WARN.

    PRD section 7 Q4 is explicit: full screenshot/pixel-diffing is brittle + CI-expensive and is NOT recommended. The recommended v1 is a STRUCTURAL-ASSERTION variant -- assert the panel's data-bearing nodes are non-empty and correctly scoped, reusing the /frontend-dev per-page constitution machinery rather than pixel-diffing. This TO begins with DE 0.4 CONFIRMING the mechanism (Q4) before the build -- the structural-assertion variant is the strong recommendation, but DE 0.4 owns the portal-testing surface and confirms it is workable before scope is locked.
  </context>

  <scope>
    <step>Phase 0 -- mechanism confirmation (PRD section 7 Q4). DE 0.4 confirms the D-2 mechanism: the structural-assertion variant (data-bearing nodes non-empty + correctly scoped, via the /frontend-dev constitution machinery) vs any alternative. The structural-assertion variant is the COO/CTO-recommended default; if DE 0.4 finds it unworkable, surface to COO before proceeding -- do NOT silently fall back to pixel-diffing. Record the confirmed mechanism.</step>
    <step>Phase 1 -- build the D-2 gate on the confirmed mechanism: for a partner-facing panel, assert its data-bearing nodes are non-empty (catches the empty-bell-curve / "--"-hero-card class) and correctly scoped (catches firm-aggregate-where-advisor-expected). Reference = a stored structural baseline per panel.</step>
    <step>Phase 2 -- wire D-2 post chain-emit (against the fresh platinum artifact, per PRD section 3.3). Fill the section-3.2 six-field table. Verify: a deliberately-emptied panel WARNs; a wrong-scope panel WARNs; a correct render passes.</step>
  </scope>

  <gate_verdict_policy>D-2 ships WARN-not-BLOCK in v1 (PRD section 7 Q1).</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check (the partner-facing panels D-2 will gate)</run>
        <expect>The panels' data-bearing field surface -- grounds the structural-assertion node set.</expect>
        <if_mismatch>Use the live components + the /frontend-dev constitutions as the source of truth.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>The /frontend-dev structural-assertion run against a gated panel (the gate's own mechanism)</run>
        <expect>The gate fires + renders a verdict end-to-end.</expect>
        <if_mismatch>Debug the gate-to-constitution wiring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A post-chain-emit render-fidelity gate; no data pipeline, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    D-2 reuses the /frontend-dev per-page constitution machinery (portal/.frontend-dev/testing/) -- DE 0.4 owns that surface; single-owner within DE 0.4. No gold-chain overlap. Note: the /frontend-dev plugin's subagent availability was an open environment question earlier this session (RD-side) -- DE 0.4 confirms the constitution machinery is invocable for the gate at Phase 0.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The Phase-0 mechanism is confirmed + recorded -- the structural-assertion variant (or, if DE 0.4 found it unworkable, a COO-surfaced alternative; NOT a silent pixel-diff fallback).</ac>
    <ac id="AC2">D-2 asserts a partner-facing panel's data-bearing nodes are non-empty + correctly scoped against a stored structural baseline; WARN on a structural-emptiness or scope-drift breach.</ac>
    <ac id="AC3">Verified: a deliberately-emptied panel WARNs; a wrong-scope (firm-vs-advisor) panel WARNs; a correct render passes. Section-3.2 six-field table filled.</ac>
    <ac id="AC4">No emoji; bun typecheck + build pass; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Phase-0 mechanism-confirmation record.
    - The D-2 visual-rendering-baseline gate (structural-assertion variant) wired post chain-emit.
    - The section-3.2 six-field gate table for D-2.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
