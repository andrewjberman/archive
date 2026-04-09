<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>1</wave>
    <phase>P2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~B" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Design audit of PartnerAnalytics header (P2 workstream 2.1) AND Distribution tab
    (P2 workstream 2.2). These two surfaces share the same gold data sources -- auditing
    them together ensures the platinum design enforces number consistency between header
    and tab.
  </objective>

  <context>
    Phase 2 is design-only: no code ships. You produce a complete platinum file specification
    for the PartnerAnalytics header and Distribution tab, ready for Phase 3 execution.

    PRD: docs/architecture/ADVI_49PUSH_P2_PRD.md (read sections 2.1 and 2.2 in full).

    Key constraint: PartnerAnalytics header and Distribution tab fetch the SAME two files
    (partner_analytics/header_metrics_{gran}.json from D_01, timeseries_chart.json from D_00).
    The platinum design must serve BOTH surfaces from shared files -- no duplication.

    The "numbers tie" principle: if the donut total on the header doesn't match the area
    chart total on Distribution, the design has failed.
  </context>

  <compiler_tools_mandate>
    BEFORE reading any .tsx file or tracing any import manually, run these comp-* commands.
    Do NOT skip this. Do NOT use Explore agents.

    1. comp-trace PartnerAnalytics --direction both
       -- shows what PartnerAnalytics.tsx fetches and what produces those files

    2. comp-trace DistributionTab --direction both
       -- shows what DistributionTab.tsx fetches and what produces those files

    3. comp-trace header_metrics --direction up
       -- traces partner analytics data origin through D_01

    4. comp-trace timeseries_chart --direction up
       -- traces cumulative chart data origin through D_00

    5. comp-trace firm_mix_views --direction up
       -- traces mix data (shared with Books N1 from Phase 1)

    6. comp-trace D_01 --all
       -- lists all D_01 function nodes + S3 write targets (shows everything D_01 produces)

    7. comp-blast timeseries_chart
       -- blast radius from the S3 artifact -- shows all consumers of cumulative chart data

    8. comp-blast header_metrics
       -- blast radius from the partner analytics artifact -- shows all consumers

    THEN use comp-pipescript for authoritative script-level I/O:

    9. comp-pipescript io D_01
       -- every S3 key D_01 reads and writes (source of partner analytics data)

    10. comp-pipescript io D_00
        -- D_00 I/O manifest (source of cumulative chart data)

    11. comp-pipescript feeds D_01
        -- what scripts feed D_01 (full upstream provenance chain)

    comp-pipescript is AUTHORITATIVE for script I/O (AST-parsed from s3_layout.py).

    THEN use comp-routes for serving layer traces (URL -> CloudFront -> auth -> S3):

    12. comp-routes trace PartnerAnalytics
        -- every fetch PartnerAnalytics makes, traced end-to-end through serving layer

    13. comp-routes trace DistributionTab
        -- every fetch DistributionTab makes, traced end-to-end

    14. comp-routes trace getPartnerAnalytics
        -- full chain: URL -> CF behavior -> origin -> auth -> router -> S3 key

    15. comp-routes trace getCumulativeChart
        -- serving chain for cumulative chart data

    16. comp-routes auth-map
        -- which paths have no auth / edge-only / double auth (needed for P4 awareness)

    Use ALL THREE tool families to build your fetch trace table:
    - comp-routes: how data gets from S3 to browser (serving layer)
    - comp-pipescript: how data gets produced (gold script I/O)
    - comp-trace: cross-layer connections
    Then READ the .tsx files to confirm which fields are actually rendered.
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="read">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="read">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">data/black_diamond/scripts/gold/D_01.partner_analytics.py</file>
      <file action="read">data/black_diamond/scripts/gold/D_00.portal_aggregates.py</file>
      <file action="create">docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md</file>
      <file action="create">docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Follow the Phase 2 audit methodology (PRD section "Audit Methodology") for BOTH surfaces:
      Step 1: Trace the frontend (every useEffect, useQuery, data fetch in the .tsx)
      Step 2: Trace the API layer (CloudFront direct S3 vs Lambda proxy)
      Step 3: Trace to gold source (which script produces each file)
      Step 4: Identify waste + divergence (unused fields, over-fetched data, metric divergence)
      Step 5: Design platinum output (JSON schema serving exactly what is rendered)
      Step 6: Cross-surface consistency matrix (for metrics on both surfaces)
    </requirement>

    <requirement id="2">
      For PartnerAnalytics, answer these specific questions from the PRD:
      a) How much of header_metrics_{gran}.json does the component actually use?
      b) Can timeseries_chart.json be downsampled from daily to weekly?
      c) Can PartnerAnalytics reuse platinum/firm/mix_summary.json from Phase 1?
      d) Can the 3 granularity files (monthly/quarterly/annual) be merged into one?
    </requirement>

    <requirement id="3">
      For Distribution, answer:
      a) Should Distribution and PartnerAnalytics share the same platinum files? (expected: yes)
      b) Can the continuous stacked area chart downsample to weekly for the ~731-day series?
      c) Design a single platinum file that serves BOTH header and Distribution.
    </requirement>

    <requirement id="4">
      Produce the following deliverables for each surface:
      1. Fetch trace table (every fetch -> gold file -> script)
      2. Render field inventory (every field the JSX actually renders)
      3. Waste analysis (fields fetched but not rendered, data over-fetched)
      4. Platinum file schema (complete JSON schema for each platinum file)
      5. Provenance map (for each platinum field, the gold file + field it derives from)
      6. Cross-surface consistency matrix (metrics appearing on both 2.1 and 2.2)
    </requirement>

    <requirement id="5">
      Design deliverable: Platinum file specs for:
      - platinum/firm/partner_analytics.json (or split by granularity if size >200KB)
      - platinum/firm/cumulative_chart.json
      Document: approximate file size, which gold script feeds each field, shared vs exclusive fields.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md -- full audit + platinum spec</deliverable>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md -- full audit + shared file spec</deliverable>
    <deliverable>Session log documenting: comp-* traces run, audit findings, design decisions</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT write any code -- this is design only</rule>
    <rule>Do NOT use Explore agents -- use comp-trace and comp-blast for all tracing</rule>
    <rule>Do NOT design separate platinum files for header and Distribution if they share data -- enforce the "numbers tie" principle with shared files</rule>
  </do_not>
</task_order>
