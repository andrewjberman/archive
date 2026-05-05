<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.003</id>
    <project>ADVI_INFLFE</project>
    <title>Defensive rendering pre-wire — 8 RED cells (zero-guard + 404-tolerant)</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- Cells 4-8: d52d04a0 (Cell 7 fix) + VERIFIED-DEFENSIVE (4,5,6,8). Cells 1-3: 6fd66973. All ACs PASS. -->
    <priority>medium</priority>
    <estimated_effort>1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INFLEC_FE_BACKEND_WIRING.md §4 TO-3 + §3 RED cells table</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v4 — 8 RED cells: activity_scan AUA=0, cash_drag AUA=0, concentration_risk [], period_start_aua MAX=null, lifecycle_aua all-zero, joe top_holdings absent, per-advisor timeseries.json absent ×4, per-advisor nna_clients.json absent ×4</ref>
    <ref type="data_fix_timetable">AUDIT-002 (DS~D pricing, ~1-2d), AUDIT-003 (DS~B+AE, ~1d), AUDIT-005 (DS~A timeseries, staged), RPBKTPI (DS+AE, ~2d)</ref>
  </references>

  <context>
    The 8 RED cells will flip to populated over the next 3-4 days via sibling data TOs. This TO
    pre-wires the FE so that when data lands, it renders correctly WITHOUT follow-on FE work.
    Equally important: while data is still absent/zero, the FE must NOT render misleading values
    (e.g., top-8 ranked by AUA when all AUA=0 is junk ranking). Use "data unavailable" or
    empty-state placeholders for the current broken state.

    This TO does NOT require INFLFE.001 AC3 or INFLFE.002 to be complete. It is data-layer
    independent. Start immediately on all components EXCEPT InflectionInsightsPanel — wait for
    INFLFE.002 to commit that file first.
  </context>

  <red_cells>
    <cell id="1" artifact="platinum/firm/activity_scan.json" component="InflectionInsightsPanel.ActivityScanPanel">
      <current_state>307 rows ALL AUA=0 — top-8 ranking by AUA produces junk ordering</current_state>
      <defensive_render>If max(rows.aua) === 0 across all rows, render "Awaiting data" placeholder. NOT misleading top-8. Flip to live when AUDIT-002 lands non-zero AUA.</defensive_render>
      <gate>Wait for INFLFE.002 to commit InflectionInsightsPanel before editing this component</gate>
    </cell>
    <cell id="2" artifact="platinum/firm/cash_drag.json" component="InflectionInsightsPanel.CashDragPanel">
      <current_state>295 rows ALL AUA=0 AND cash_pct=0</current_state>
      <defensive_render>Same — if max(rows.cash_aua) === 0, render "Awaiting data". Same gate as cell 1.</defensive_render>
      <gate>Same gate as cell 1</gate>
    </cell>
    <cell id="3" artifact="platinum/firm/concentration_risk.json" component="InflectionInsightsPanel.ConcentrationRiskPanel">
      <current_state>2 bytes = [] empty array</current_state>
      <defensive_render>Verify FE already renders empty-state correctly (array.length === 0 check). If it crashes or renders misleadingly: add empty-state placeholder. Same gate as cell 1.</defensive_render>
      <gate>Same gate as cell 1</gate>
    </cell>
    <cell id="4" artifact="platinum/firm/leaderboard.json field: period_start_aua" component="BooksTab leaderboard">
      <current_state>period_start_aua MAX=null for all Inflection advisors (per matrix v4)</current_state>
      <defensive_render>Verify optional-chain is in place. Confirm null renders as empty string or "—", NOT "0%" or misleading zero. Playwright screenshot from DT (AC3 in INFLFE.004) will verify render.</defensive_render>
    </cell>
    <cell id="5" artifact="platinum/firm/leaderboard.json field: lifecycle_aua" component="BooksTab leaderboard">
      <current_state>lifecycle_aua all-zero for all Inflection advisors</current_state>
      <defensive_render>Zero is a valid numeric value — FE should not suppress. Verify the lifecycle AUA stack renders 0-valued bars as empty (not missing) and does not crash on zero-sum stack.</defensive_render>
    </cell>
    <cell id="6" artifact="platinum/advisors/joe_brandenburg/top_holdings.json" component="BooksTab ADV drill joe_brandenburg">
      <current_state>File absent (rep_id=6 not in silver assets; AUDIT-003 fix in flight)</current_state>
      <defensive_render>ADV drill for joe_brandenberg should render empty-cohort placeholder for top_holdings, NOT crash. Other 3 advisors (IWM, peter_lee, patrick_scanlan) render normally. 404-tolerant useQuery with isError state showing placeholder.</defensive_render>
    </cell>
    <cell id="7" artifact="platinum/advisors/{id}/timeseries.json (all 4 absent)" component="BooksTab ADV drill per-advisor timeseries chart">
      <current_state>Missing for all 4 Inflection advisors (AUDIT-005 in flight)</current_state>
      <defensive_render>Pre-wire getPlatinumAdvisorTimeseries hook with 404-tolerant error boundary. Render "timeseries coming soon" placeholder or empty chart. Must NOT crash the ADV drill.</defensive_render>
    </cell>
    <cell id="8" artifact="platinum/advisors/{id}/nna_clients.json (all 4 absent)" component="BooksTab L2 NNA cohort drill">
      <current_state>Missing for all 4; ADV-cohort GRAY at layout level (may not be fetched)</current_state>
      <defensive_render>Verify whether BooksTab L2 independently fetches nna_clients.json for Inflection (layout.ts GRAY may suppress). If fetch IS attempted: add 404-tolerant fallback. If fetch NOT attempted (confirmed GRAY): document as GRAY-confirmed, no code change.</defensive_render>
    </cell>
  </red_cells>

  <phase id="0" when="before any code write — scope confirmation">
    <step>
      <run>grep -n "nna_clients\|getPlatinumAdvisorNNAClients" portal/src/pages/AdvisorIntelligence/endpoints/advisor-intelligence.ts | head -10</run>
      <expect>Either: (a) fetch present → wire 404 fallback; (b) fetch absent → cell 8 is GRAY-confirmed, document and skip</expect>
    </step>
    <step>
      <run>comp-transform schema-check BooksTab (to confirm which sub-components consume each RED artifact)</run>
      <expect>Shows which props map to each RED artifact — narrows which components need defensive-render changes</expect>
    </step>
  </phase>

  <phase id="1" when="implementation — start with non-InflectionInsightsPanel cells first">
    <step>
      <action>Implement defensive renders for cells 4-8 (leaderboard, joe top_holdings, timeseries, nna_clients) first — these do NOT require INFLFE.002 gate</action>
    </step>
    <step>
      <action>After INFLFE.002 commits InflectionInsightsPanel: implement defensive renders for cells 1-3 (activity_scan AUA=0, cash_drag AUA=0, concentration_risk [])</action>
    </step>
  </phase>

  <phase id="2" when="before committing">
    <step>
      <run>comp-transform schema-check BooksTab (post-change)</run>
      <expect>No new MISSING fields introduced</expect>
      <if_mismatch>Fix before committing</if_mismatch>
    </step>
    <step>
      <run>bun run typecheck</run>
      <expect>exit 0</expect>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>INFLFE.002: gate on InflectionInsightsPanel. Execute cells 4-8 first; cells 1-3 after INFLFE.002 commits.</coord>
    <coord>INFLFE.004 (RD Playwright): TO-3 ships before RD sweep — defensive renders must be in PROD or at least on DEV portal branch that RD uses.</coord>
    <coord>Data lanes (AUDIT-002/003/005/RPBKTPI): when these flip data live, the defensive renders should automatically lift without FE code change. Verify this assumption for each cell during implementation.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Cells 1-3 (activity_scan/cash_drag/concentration_risk): renders "Awaiting data" placeholder when AUA=0/[] instead of junk rankings or crash</criterion>
    <criterion id="AC2">Cells 4-5 (leaderboard): period_start_aua null renders as "—" not "0%"; lifecycle_aua zero-sum stack does not crash</criterion>
    <criterion id="AC3">Cell 6 (joe top_holdings): ADV drill renders empty-cohort placeholder, other 3 advisors unaffected</criterion>
    <criterion id="AC4">Cell 7 (timeseries): ADV drill renders "coming soon" placeholder or empty chart, does not crash</criterion>
    <criterion id="AC5">Cell 8 (nna_clients): either 404-tolerant fallback wired OR GRAY-confirmed with documentation</criterion>
    <criterion id="AC6">bun run typecheck exit 0; comp-transform schema-check BooksTab no new MISSING</criterion>
    <criterion id="AC7">RAVC3 to COO: portal commit hash + per-cell AC1-5 evidence (grep or screenshot) + AC6 status</criterion>
  </acceptance_criteria>
</task_order>
