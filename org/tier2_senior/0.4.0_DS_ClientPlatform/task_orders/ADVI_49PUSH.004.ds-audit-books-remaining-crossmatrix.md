<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-004-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>1</wave>
    <phase>P2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~D" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Two deliverables in one TO:
    1. Design audit of Books tab remaining panels (P2 workstream 2.4): FeeEfficiencyPanel,
       FeeRoleBreakdownPanel, FeeSummaryPanel, Revenue/Cost Basis panel design, and
       advisor-level positions drilldown.
    2. Cross-surface consistency matrix (P2 TO-5): for EVERY metric that appears on more
       than one ADVI surface, document the gold source and flag divergences.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P2_PRD.md (read section 2.4 and "Audit Methodology"
    Step 6 in full).

    Phase 1 already designed platinum schemas for the Books tab core drill hierarchy.
    This TO audits the REMAINING panels that Phase 1 did not fully address:

    - N1: FeeEfficiencyPanel (scatter plot, C_08 data, included in P1 dashboard.json)
    - L2: FeeRoleBreakdownPanel (donut, included in P1 advisors/{id}/summary.json)
    - L3: FeeSummaryPanel (fee table, included in P1 clients/{rel_id}/summary.json)
    - L3 right-half: Revenue/Cost Basis Panel (DOES NOT EXIST YET -- design spec needed)
    - L2: Advisor positions pie + client drilldown (needs data model design)

    The cross-surface matrix is the capstone: it unifies findings from .002 (PartnerAnalytics
    + Distribution), .003 (Advisors tab), and this TO (Books remaining) into one consistency
    check. You will need to read the deliverables from .002 and .003 when they are available,
    but you can start the Books 2.4 audit and the matrix framework immediately.
  </context>

  <compiler_tools_mandate>
    BEFORE reading any .tsx file or tracing any import manually, run these comp-* commands.
    Do NOT skip this. Do NOT use Explore agents.

    1. comp-trace FeeEfficiencyPanel --direction both
       -- shows what FeeEfficiencyPanel.tsx fetches and what produces it

    2. comp-trace FeeRoleBreakdownPanel --direction both
       -- fee role breakdown data chain

    3. comp-trace FeeSummaryPanel --direction both
       -- fee summary data chain

    4. comp-trace advisor_fee_efficiency --direction up
       -- traces C_08 fee efficiency data origin

    5. comp-trace C_08 --all
       -- lists all C_08 function nodes + S3 write targets

    6. comp-blast advisor_fee_efficiency
       -- blast radius from the fee efficiency artifact -- shows all consumers

    7. comp-trace fee_rate_history --direction both
       -- traces fee rate data through A_02

    8. comp-trace client_tax_liability --direction both
       -- traces tax data (for Revenue/Cost Basis panel design)

    9. comp-trace B_01 --all
       -- lists all B_01 function nodes + outputs (holdings_lots consumers)

    THEN use comp-pipescript for authoritative script-level I/O:

    10. comp-pipescript io C_08
        -- every S3 key C_08 reads and writes (source of fee efficiency data)

    11. comp-pipescript io A_02
        -- A_02 I/O manifest (source of fee_rate_history)

    12. comp-pipescript feeds C_08
        -- what scripts feed C_08 (full upstream provenance for fee data)

    13. comp-pipescript consumers C_08
        -- what consumes C_08 output (verify if fee data is portal-only or used by other scripts)

    comp-pipescript is AUTHORITATIVE for script I/O (AST-parsed from s3_layout.py).

    THEN use comp-routes for serving layer traces:

    14. comp-routes trace FeeEfficiencyPanel
        -- every fetch FeeEfficiencyPanel makes, traced end-to-end

    15. comp-routes trace getAdvisorFeeEfficiency
        -- full serving chain for fee efficiency data

    16. comp-routes auth-map
        -- which paths have no auth / edge-only / double auth

    Use ALL THREE tool families for your fetch trace tables AND the cross-surface matrix:
    - comp-routes: how data gets from S3 to browser
    - comp-pipescript: how data gets produced
    - comp-trace: cross-layer connections
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="read">portal/src/pages/AdvisorIntelligence/tabs/FeeEfficiencyPanel.tsx</file>
      <file action="read">portal/src/pages/AdvisorIntelligence/tabs/FeeRoleBreakdownPanel.tsx</file>
      <file action="read">portal/src/pages/AdvisorIntelligence/tabs/FeeSummaryPanel.tsx</file>
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">data/black_diamond/scripts/gold/C_08.fee_efficiency.py</file>
      <file action="read">data/black_diamond/scripts/gold/A_02.fee_rate_history.py</file>
      <file action="create">docs/briefs/ADVI_49PUSH_P2_2.4_books_remaining.md</file>
      <file action="create">docs/briefs/ADVI_49PUSH_P2_cross_surface_matrix.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      BOOKS REMAINING AUDIT (2.4):
      For each of the 5 panels listed in the PRD section 2.4:
      Step 1: Read the .tsx component, inventory every rendered field
      Step 2: Trace each fetch to its API endpoint and gold source
      Step 3: Verify Phase 1 platinum schemas cover all rendered fields
      Step 4: For any gap, design the platinum schema extension
    </requirement>

    <requirement id="2">
      FeeEfficiencyPanel: Verify that Phase 1's platinum/firm/dashboard.json fee_efficiency
      section contains ALL fields the scatter needs: per-advisor nna, revenue, aua, growth_pct,
      percentile -- for EACH window (QTD/YTD/1Y/3Y/Max). If missing fields, document them.
    </requirement>

    <requirement id="3">
      Revenue/Cost Basis Panel (L3 right-half): This panel does not exist yet.
      Design spec per PRD:
      a) What data would it show? (annual revenue, cost basis summary, unrealized gain/loss)
      b) What gold sources feed it? Use comp-trace to find C_05, B_02, B_01 outputs.
      c) What platinum schema serves it? (extension of clients/{rel_id}/summary.json)
      d) Layout spec (left = fee summary, right = revenue/tax)
    </requirement>

    <requirement id="4">
      Advisor positions pie + client drilldown: Does this require new gold computation
      (new C_08 or D_02 section) or can it be assembled from existing outputs? Use comp-trace
      to determine. Document the data model.
    </requirement>

    <requirement id="5">
      CROSS-SURFACE CONSISTENCY MATRIX:
      For EVERY metric that appears on more than one ADVI surface, produce this table:

      | Metric | PartnerAnalytics | Distribution | Advisors Tab | Books N1 | Books L2 | Books L3 | Gold Source (current) | Divergent? | Platinum Source (proposed) |
      |--------|-----------------|-------------|-------------|---------|---------|---------|---------------------|-----------|--------------------------|

      Minimum metrics to cover:
      - Firm Total AUA
      - Firm NNA YTD
      - Advisor {id} AUA
      - Advisor {id} NNA YTD
      - Advisor {id} Growth %
      - Client {rel_id} AUA
      - Firm client count
      - Advisor client count

      For each divergent metric, specify which single gold source D_04 (expanded) should use.
    </requirement>

    <requirement id="6">
      Read the deliverables from .002 and .003 (when available in docs/briefs/) to complete
      the cross-surface matrix. If they are not yet available, build the matrix framework
      with Books data and note which cells need .002/.003 input.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_2.4_books_remaining.md -- fee panel audit + revenue/tax design + drilldown data model</deliverable>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_cross_surface_matrix.md -- complete metric x surface divergence matrix</deliverable>
    <deliverable>Session log documenting: comp-* traces run, audit findings, divergence analysis</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT write any code -- this is design only</rule>
    <rule>Do NOT use Explore agents -- use comp-trace and comp-blast for all tracing</rule>
    <rule>Do NOT declare "no divergence" without tracing each metric to its exact gold source row in each script</rule>
    <rule>Do NOT ignore the Revenue/Cost Basis panel design -- it is new work, not just an audit</rule>
  </do_not>
</task_order>
