<task_order>
  <metadata>
    <id>ADHC_VALGATE.005</id>
    <slug>de-d3-multi-axis-envelope-sentinel-gate</slug>
    <issued_by>1.0.0_SA_CTO~B</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-18 (COO decomposition of ADHC_VALGATE PRD v0.1). Phase 2 -- gated on VALGATE Phase 1 (.001-.003) shipping first. COO flips to pending + fires GO when Phase 1 closes + DE 0.4 lane has capacity. || DISPATCHED 2026-05-21 by 1.0.0_SA_CTO~B -- Phase 1 (.001/.002/.003 Class-C) CLOSED + .007/.008/.009 closed; Andrew brought 0.4.0_DE_ClientPlatform~B online + directed CTO~B to dispatch the Class-D suite (COO~B closed); re-homed base->~B, issued_by/issued_to->~B, GO fired. CTO~B output-validates the RAVC2.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P1 -- VALGATE Phase 2. D-3 catches an entity whose metrics are jointly implausible across multiple axes -- a defect each single axis can miss.</priority>
    <sla>1-1.5d wall (PRD section 6 sizing) -- D-3 generalizes an already-shipped instance.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.D D-3 spec, section 3.2 gate anatomy, section 7 Q1 verdict.</prd>
    <anchor>INFFIN.006 AdvisorBookView 6-axis threshold-2 sentinel -- ALREADY SHIPPED in that one component. D-3 generalizes it into a reusable gate.</anchor>
  </references>

  <context>
    D-3 is the multi-axis envelope-validation sentinel. Input: an entity's metric vector (e.g. an advisor's AUA / NNA / TWR / client-count). Reference: a per-axis plausibility envelope. Comparison: count the axes outside their envelope; fire when >= 2 axes are JOINTLY implausible (threshold-2 -- a single off-axis is often legitimate; two together is a signal). Verdict: WARN.

    The pattern already exists, shipped, in exactly one place: the INFFIN.006 AdvisorBookView 6-axis threshold-2 sentinel. D-3 is the GENERALIZATION -- lift that instance into a reusable gate that takes an (entity, metric-vector, per-axis envelope, threshold) configuration and applies to any entity-metric surface, post chain-emit.
  </context>

  <scope>
    <step>Phase 1 -- study the shipped AdvisorBookView 6-axis threshold-2 sentinel; extract the reusable core (per-axis envelope check + the joint >=2-axis fire rule).</step>
    <step>Phase 2 -- the generalized D-3 gate: configuration-driven -- (entity type, metric-vector definition, per-axis plausibility envelopes, fire threshold defaulting to 2). Applies to any entity-metric surface in a fresh platinum artifact post chain-emit.</step>
    <step>Phase 3 -- seed the config with the AdvisorBookView axes (so the existing coverage is preserved through the generalized gate, not lost) + any other entity-metric surface worth covering now. Fill the section-3.2 six-field table. Verify: a synthetic entity with >=2 jointly-implausible axes WARNs; a single off-axis does not.</step>
  </scope>

  <gate_verdict_policy>D-3 ships WARN-not-BLOCK in v1 (PRD section 7 Q1).</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check AdvisorBookView</run>
        <expect>The AdvisorBookView field surface -- grounds the existing 6-axis sentinel's inputs so the generalization preserves coverage.</expect>
        <if_mismatch>If the AdvisorBookView axes differ from the PRD's description, use the live component as the source of truth.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-transform schema-check (each component D-3's seed config covers)</run>
        <expect>The metric-vector fields D-3 reads are all typed/present -- no gate on an undefined field.</expect>
        <if_mismatch>Reconcile before closing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A post-chain-emit render-fidelity gate; no data pipeline, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    D-3 fires post chain-emit against fresh platinum artifacts -- it reads, does not modify. The AdvisorBookView sentinel it generalizes is shipped INFFIN.006 work; lifting the core into a reusable gate must not regress AdvisorBookView's existing coverage (seed the config so AdvisorBookView stays covered). Single-owner the D-3 gate component within DE 0.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The D-3 gate is configuration-driven: an (entity type, metric vector, per-axis envelopes, threshold) config yields the joint >=2-axis implausibility check.</ac>
    <ac id="AC2">The config is seeded so the existing AdvisorBookView 6-axis coverage is preserved through the generalized gate -- no coverage lost in the lift.</ac>
    <ac id="AC3">Verified: a synthetic entity with >=2 jointly-implausible axes WARNs; a single off-axis entity does NOT (threshold-2 holds). Section-3.2 six-field table filled.</ac>
    <ac id="AC4">No emoji; bun typecheck + build pass; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The generalized D-3 multi-axis envelope gate + seed config.
    - The section-3.2 six-field gate table for D-3.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
