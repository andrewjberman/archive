<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.004</id>
    <project>ADVI_INFLFE</project>
    <title>INFLEC AdvisorIntelligence Playwright render sweep + constitution doc</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- Deliverables shipped 2026-05-05: matrix v6 Render column updated; constitution doc at portal/.frontend-dev/testing/inflection_advisor_intelligence.md; 5 follow-on TOs identified. Andrew manual sweep + S7 smoke evidence. RAVC5 sent to COO. Commit blocked by Andrew "no more commits this session — COO handles" directive — handed to COO for coordination. -->
    <priority>medium</priority>
    <estimated_effort>1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INFLEC_FE_BACKEND_WIRING.md §4 TO-4</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v4 (f6ea12221) — Render column currently "(Phase 2)" for all GREEN cells; this TO populates it</ref>
    <ref type="constitution_convention">portal/.frontend-dev/testing/advi_inflec_advisor_intelligence.json — output path for constitution doc</ref>
    <ref type="auth_path">memory/project_inflec_frontend_dev_auth_path.md — login as Andrew + Select Partner dropdown; devBypass is broken for data-presence gates</ref>
  </references>

  <context>
    Matrix v4 has 25 GREEN cells and 2 YELLOW cells. The Render column for all GREEN cells is
    "(Phase 2)" — no panel has been empirically confirmed to render correctly on a live Inflection
    JWT. S7SUMFIX shipped 2026-05-04 (first day with all 4 advisor summary.json populated).
    portal-v2.1.70 is in PROD with INFLFE.001 Bug A + Bug B fixes.

    This TO runs the Phase 2 render sweep: screenshot every panel under real Inflection JWT,
    compare against matrix v4 verdicts, and produce the constitution document. Any GREEN cell
    that fails to render becomes a YELLOW cell and spawns a same-day FE follow-on TO.

    DO NOT start until INFLFE.001 AC3 PASS + INFLFE.002 COMPLETE + INFLFE.003 COMPLETE.
  </context>

  <phase id="0" when="setup">
    <step>
      <run>bun run dev --port 5175 (from portal/ directory)</run>
      <expect>Dev server running; accessible at localhost:5175</expect>
    </step>
    <step>
      <run>Auth path: login as Andrew (andrew@opalinvest.com), Select Partner dropdown → Inflection Wealth Management → firmId=inflection JWT</run>
      <expect>Portal loads under firmId=inflection; AUA strip shows ~$429M; 4 advisor list visible in BooksTab</expect>
      <if_mismatch>If devBypass path fails: use Option C (Select Partner dropdown per auth_path memory). DO NOT use devBypass — it is broken for data-presence gates.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="screenshot sweep — per surface">
    <surface name="Page header">
      <screenshot>FirmDisplayName + AUA strip + last-update timestamp</screenshot>
      <screenshot>FidelityCustodianBar (footer)</screenshot>
      <screenshot>Data Source panel (Orion Connected status)</screenshot>
    </surface>
    <surface name="PartnerAnalytics">
      <screenshot>Quarterly rollup (clients, accounts, AUA, NNA)</screenshot>
      <screenshot>Geo donut</screenshot>
      <screenshot>Time-series chart (1Y / 3Y / 5Y / SI)</screenshot>
      <screenshot>NNA cohort breakdown</screenshot>
    </surface>
    <surface name="DistributionTab geo cohort">
      <screenshot>Geo donut + table</screenshot>
      <screenshot>Continuous AUA chart per geo</screenshot>
      <screenshot>NNA bell curve per geo</screenshot>
      <screenshot>Advisor list per geo</screenshot>
    </surface>
    <surface name="BooksTab">
      <screenshot>Firm-level books table</screenshot>
      <screenshot>L2 drill: Inflection Wealth Management</screenshot>
      <screenshot>L2 drill: Peter Lee</screenshot>
      <screenshot>L2 drill: Patrick Scanlan</screenshot>
      <screenshot>L2 drill: Joe Brandenburg</screenshot>
      <screenshot>InflectionInsightsPanel (all 3 sub-panels)</screenshot>
      <screenshot>L3 client detail drill (click a client from L2)</screenshot>
    </surface>
    <surface name="ADV per-advisor drill">
      <screenshot>IWM: book.json, summary.json, composition.json, fee_efficiency.json, top_holdings, radial_12m</screenshot>
      <screenshot>Peter Lee: same panels</screenshot>
      <screenshot>Patrick Scanlan: same panels</screenshot>
      <screenshot>Joe Brandenburg: same panels (expect empty top_holdings placeholder per INFLFE.003)</screenshot>
    </surface>
  </phase>

  <phase id="2" when="matrix render column update">
    <step>
      <action>For each screenshot: compare rendered output against matrix v4 cell status. GREEN = renders correctly. YELLOW = data present but visual defect (FE bug). File discrepancy cells as follow-on TO to DE.</action>
    </step>
    <step>
      <action>Update matrix v4 Render column in docs/architecture/ADVI_INFLEC_AUDIT.md: replace "(Phase 2)" with "CONFIRMED-GREEN [screenshot path]" or "YELLOW [defect description]"</action>
    </step>
  </phase>

  <phase id="3" when="constitution doc authoring">
    <step>
      <action>Write portal/.frontend-dev/testing/inflection_advisor_intelligence.md:
      - Header: surface, panel, expected, observed, screenshot path, verdict
      - One row per screenshot
      - Defect rows include: defect description + suggested fix
      - Format matches existing 49F constitution if available</action>
    </step>
  </phase>

  <acceptance_criteria>
    <criterion id="AC1">Screenshot taken for every panel in Phase 1 — no surface skipped; paths documented in constitution</criterion>
    <criterion id="AC2">Matrix v4 Render column populated for all GREEN/YELLOW cells — no "(Phase 2)" remaining</criterion>
    <criterion id="AC3">Constitution doc at portal/.frontend-dev/testing/inflection_advisor_intelligence.md — one row per panel with verdict</criterion>
    <criterion id="AC4">Any failing GREEN cell (renders incorrectly) flagged as YELLOW in matrix + follow-on TO authored and MCP'd to COO same session</criterion>
    <criterion id="AC5">RAVC3 to COO: commit hash (matrix v4 Render update + constitution doc) + YELLOW count (delta from TO execution) + screenshot directory path</criterion>
  </acceptance_criteria>
</task_order>
