<task_order>
  <metadata>
    <id>YALP_MDSRC.005</id>
    <slug>cto-ws5-synthesis-migration-matrix-prd-v0-3</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GATE CLEARED 2026-05-20 — all four Phase-0 audits RAVC4-accepted by COO (WS-1 1baf13dfa / WS-2 7de5d3b69+368510231 / WS-3 b7153c70c / WS-4 b88787708, all on origin/CLOUD; the four briefs + WS-1/WS-2/WS-3 matrix slices verified committed). COO flipped status->pending + fired the GO to 1.0.0_SA_CTO. Original gate: STAGED — Phase 1 synthesis, GATED on TO-1..4 ALL RAVC-complete (PRD v0.2 §9: Phase 1 gates on all four Phase-0 audits). On the fourth RAVC2 COMPLETE: COO verifies all four audit deliverables are committed, flips this TO status->pending + dispatch_held=false, and fires the GO to 1.0.0_SA_CTO. No Andrew GO needed for TO-5 — the TO-1..4 completion gate IS the unblock.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct (CEO interview 2026-05-20). WS-5 is the synthesis that turns four domain audits into the implementation charter (PRD v0.3).</priority>
    <sla>~1-2 CTO days (PRD §9).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2 (1.0.0_SA_CTO, self-authored). This TO = WS-5 / §8 TO-5. WS-5 produces PRD v0.3 in-place on this same file.</prd>
    <audit_inputs>The four Phase-0 audit deliverables (gated dependency):
      - WS-1 `docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md` + WS-1 matrix slice (YALP_MDSRC.001, 0.1.0_DS_MarketIntelligence)
      - WS-2 `docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md` + WS-2 matrix slice (YALP_MDSRC.002, 0.2.0_DS_PortfolioAnalytics)
      - WS-3 `docs/briefs/mdsrc-ws3-client-facing-data-audit-20260520.md` + WS-3 matrix slice + model-portfolio sourcing recommendation (YALP_MDSRC.003, 0.4.0_DS_ClientPlatform)
      - WS-4 YCharts operational-pattern design doc (YALP_MDSRC.004, 0.7.0_AE_CloudOps)</audit_inputs>
  </references>

  <context>
    YALP_MDSRC v0.2 charters four parallel Phase-0 audits + this synthesis. WS-5 consumes the three DS domain-audit matrix slices + the AE operational-pattern design doc and produces the IMPLEMENTATION CHARTER — PRD v0.3. v0.3 is what authorizes (gated additionally on the Andrew Q1/Q7 business calls) any actual YCharts-integration code/Terraform/Lambda work.
  </context>

  <scope>
    <in_scope>
      Consume the four audit deliverables and produce, as PRD `YALP_MDSRC.md` v0.3:
      - (a) The MIGRATION DECISION MATRIX — every portal surface across the three domain matrix slices x {YCharts-replaceable | Bloomberg-pkl-only | SmartX-sourced | proprietary | hybrid}, with evidence. Assemble the three domain slices into one matrix; explicitly reconcile the WS-2/WS-3 Model Portfolios seam so no surface is dropped or double-verdicted.
      - (b) The recommended YCharts integration ARCHITECTURE — folding WS-4's operational pattern + the Q1 official-API-vs-scrape decision (once Andrew rules; flag as still-pending-Andrew if not yet ruled).
      - (c) A PHASED IMPLEMENTATION PLAN with effort estimates and per-TO compiler mandates (comp-iam / comp-routes / comp-blast as applicable to each implementation TO).
    </in_scope>
    <out_of_scope>
      - Implementation itself — v0.3 charters it; the implementation TOs are decomposed by COO from v0.3.
      - The Andrew Q1/Q7 business calls — v0.3 surfaces them; it does not make them.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before authoring v0.3">
      <step>
        <run>(none) — WS-5 is a CTO synthesis authored from the four audit inputs; no graph query.</run>
        <expect>Documented-none: synthesis authoring. The §5 Compiler Evidence already in PRD v0.2 carries forward.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="v0.3 implementation-TO mandates">
      <step>
        <run>(in v0.3) — v0.3 carries the full per-TO compiler mandates for each implementation TO it defines: `comp-iam service` + `comp-iam gaps` for any new Lambda/Secrets-Manager boto3 calls, `comp-routes` for any serving-path change, `comp-blast` for any shared-artifact change.</run>
        <expect>Every v0.3 implementation TO ships with a structured `<phase><step><run>/<expect>/<if_mismatch>` mandate per the COO TO-mandate format.</expect>
        <if_mismatch>A v0.3 implementation TO lacking a structured compiler mandate is structurally invalid — fix before decomposition.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    v0.3 enumerates the implementation-phase cross-domain coordination — portal-component changes (Pods 1+2 DE/RD), MDPF_ASSETS reconciliation, CloudFront/Lambda. v0.2 itself writes no shared artifact.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The migration decision matrix covers every surface across the three domain matrix slices with a verdict + evidence — no gap at the WS-2/WS-3 Model Portfolios seam.</ac>
    <ac id="AC2">Q1 + Q7 (the Andrew business calls) are explicitly resolved, or explicitly flagged as still-pending-Andrew, before any v0.3 implementation TO dispatches.</ac>
    <ac id="AC3">v0.3 ships as a committed PRD (`docs/architecture/YALP_MDSRC.md` v0.3) with a phased implementation plan and per-TO compiler mandates.</ac>
    <ac id="AC4">v0.3 folds in WS-4's operational pattern as the integration-architecture basis. Session log / RAVC: CTO notifies 2.0.0_SA_COO on v0.3 ship for the implementation-TO decomposition handoff.</ac>
  </acceptance_criteria>

  <deliverables>
    - PRD `docs/architecture/YALP_MDSRC.md` v0.3 — the implementation charter (migration decision matrix + integration architecture + phased plan).
    - Handoff notification to 2.0.0_SA_COO for v0.3 implementation-TO decomposition.
  </deliverables>

  <do_not>
    <rule>Do NOT start WS-5 before all four of TO-1..4 are RAVC-complete — the synthesis needs all four domain inputs (PRD §9 gate).</rule>
    <rule>Do NOT make the Q1/Q7 Andrew business calls inside v0.3 — surface them; Andrew decides.</rule>
    <rule>No emojis in PRD v0.3 or any CLI transcript (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
