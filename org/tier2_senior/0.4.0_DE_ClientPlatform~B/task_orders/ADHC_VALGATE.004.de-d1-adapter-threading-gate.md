<task_order>
  <metadata>
    <id>ADHC_VALGATE.004</id>
    <slug>de-d1-adapter-threading-gate</slug>
    <issued_by>1.0.0_SA_CTO~B</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-18 (COO decomposition of ADHC_VALGATE PRD v0.1). Phase 2 -- gated on VALGATE Phase 1 (.001-.003) shipping first per the PRD phasing. Hard dependency ADHC_COMPIL_V4.031 (comp-adapter-audit) is CONFIRMED SHIPPED (702fe31c5). COO flips to pending + fires GO when Phase 1 closes + DE 0.4 lane has capacity. || DISPATCHED 2026-05-21 by 1.0.0_SA_CTO~B -- Phase 1 (.001/.002/.003 Class-C) CLOSED + .007/.008/.009 closed; Andrew brought 0.4.0_DE_ClientPlatform~B online + directed CTO~B to dispatch the Class-D suite (COO~B closed); re-homed base->~B, issued_by/issued_to->~B, GO fired. CTO~B output-validates the RAVC2.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P1 -- VALGATE Phase 2. D-1 catches the INFFIN-arc class: a typed nested path a portal component reads that was never threaded from the raw S3 envelope -- tsc passes, the logic-walk reads correct, runtime does not crash, and partner data is silently absent.</priority>
    <sla>1-1.5d wall (PRD section 6 sizing) -- D-1 wraps an existing tool; the work is the structural fire + verdict + pre-push wiring.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.D D-1 spec, section 3.2 gate anatomy, section 3.3 (Class-D lives at portal pre-push), section 7 Q1 (verdict -- D-1 partner-facing is the BLOCK exception).</prd>
    <tool_dependency>ADHC_COMPIL_V4.031 -- comp-adapter-audit, the diagnostic tool D-1 wraps. CONFIRMED SHIPPED (702fe31c5). D-1 is the structural fire + verdict AROUND the tool; it does not re-author the audit.</tool_dependency>
    <anchor>INFFIN 8-defect arc (2026-05-13): adapter-threading bugs 32df3b85 / d622a249 / 22b7b7b4 -- each a one-line adapter delta, each shipped past tsc + logic-walk + runtime smoke, each caught only empirically.</anchor>
  </references>

  <context>
    D-1 is the adapter-vs-shipped-emit field-threading gate. Input: a portal static adapter (e.g. getPlatinumAdvisorSummaryStaticInflection). Reference: the most-recent S3 platinum envelope for that adapter's data source. Comparison: field-by-field -- every consumer-readable typed OUTPUT path of the adapter must thread from a raw field in the envelope; flag any output path that defaults with no raw source. The defect class: a typed path the component reads with no raw-envelope source -> production data silently absent.

    D-1 = the structural fire + verdict around comp-adapter-audit (the tool produces the field-by-field audit; D-1 makes it fire structurally at portal pre-push and renders a verdict). It is NOT a new diagnostic tool.
  </context>

  <scope>
    <step>Phase 1 -- the D-1 gate: a portal pre-push hook step (alongside comp-cache collisions) that, for each partner-facing static adapter changed in the push, invokes comp-adapter-audit and renders a verdict from its output.</step>
    <step>Phase 2 -- verdict policy: for a PARTNER-FACING adapter, an output path with no raw-envelope source = BLOCK at pre-push (PRD section 7 Q1 exception -- a missing field on a partner surface is high-cost; D-1 justifies BLOCK from v1). For a non-partner-facing adapter, WARN. Distinguish the two via the adapter's data source / partner-facing classification.</step>
    <step>Phase 3 -- fill the section-3.2 six-field gate table. Verify: a synthetic adapter with a deliberately un-threaded output path is BLOCKed; a correct adapter passes; the INFFIN-arc anchor case (32df3b85-class inverted/missing thread) is caught.</step>
  </scope>

  <gate_verdict_policy>D-1 is the PRD section 7 Q1 EXCEPTION (COO decomposition ruling): partner-facing adapter with an un-threaded output path = BLOCK from v1 (not WARN) -- a silently-absent field on a partner surface is high-cost and the comp-adapter-audit signal is precise (low false-positive risk for a structural threading check). Non-partner-facing adapters = WARN.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check (the partner-facing adapters / components D-1 will gate)</run>
        <expect>The adapter/component typed-field surface -- MISSING / NOTE / UNUSED. Grounds which output paths D-1 audits.</expect>
        <if_mismatch>If schema-check surfaces a current MISSING on a live partner adapter, that is a present D-1-class defect -- flag it to COO, it may want immediate fixing independent of the gate ship.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>The current portal pre-push hook surface D-1 wires alongside -- confirms the hook insertion point.</expect>
        <if_mismatch>Reconcile the hook surface before wiring D-1.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-adapter-audit (a sample partner-facing adapter, via the D-1 gate path)</run>
        <expect>The gate invokes the tool and renders a verdict end-to-end.</expect>
        <if_mismatch>Debug the gate-to-tool wiring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A portal pre-push validation gate; no data pipeline, no S3 producer, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    D-1 attaches to the portal pre-push hook surface (alongside comp-cache collisions). No gold-chain / orion-gold-dispatch.sh overlap. The hook surface is portal-side; single-owner the hook edit within DE 0.4. comp-adapter-audit (COMPIL_V4.031) is a shipped tool -- consumed, not modified.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">D-1 fires structurally at portal pre-push for each partner-facing static adapter changed in the push -- it invokes comp-adapter-audit and renders a verdict; it is not a discretionary manual run.</ac>
    <ac id="AC2">Verdict policy correct: a partner-facing adapter with an un-threaded output path BLOCKs the push; a non-partner-facing adapter WARNs. The partner-facing classification is deterministic.</ac>
    <ac id="AC3">Verified: a synthetic adapter with a deliberately un-threaded output path is BLOCKed; a correct adapter passes; the INFFIN-arc anchor pattern (an output path with no raw-envelope source) is caught. Section-3.2 six-field table filled.</ac>
    <ac id="AC4">No emoji; bun typecheck + build pass; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The D-1 adapter-threading gate wired at portal pre-push.
    - The section-3.2 six-field gate table for D-1.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
