<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.006-rd</id>
    <project>ADVI_INFLFE</project>
    <title>INFLFE.006 DT fix verification — Playwright sweep: Distribution + Books error resolution + 5-vector AUA</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~1h RD (targeted sweep, not full matrix)</estimated_effort>
  </metadata>

  <references>
    <ref type="dt_fix">Portal DEV commit 43411a79: DistributionTab.tsx + ClientsTab.tsx guards for inflection city key fallback + tax null guard + total_aua fallback. Submodule bump CLOUD f4dfe7149.</ref>
    <ref type="root_causes">
      B1: Distribution city segments emit 'name' not 'key' → formatSegLabel crash on drilldown. Fix: city.key ?? city.name fallback in city mapping.
      B2: clients-tab-slim.json missing tax field → clientsTabData.tax.taxable TypeError. Fix: tax null guard + total_aua fallback.
    </ref>
    <ref type="data_fix">DS~A INFLFE.006-data (commit a9435bc90): partner_analytics_quarterly.json total_aua = $199,649,186.31 (was $182.5M). NMNC=$19.7M, NMEC=$7.5M, Existing=$172.5M. Live in platinum/ since 16:01Z.</ref>
    <ref type="constitution_doc">portal/.frontend-dev/testing/inflection_advisor_intelligence.md — sole constitution doc for Inflection AdvisorIntelligence surface. RD has uncommitted changes from Line 211 sweep (prior session) — bundle with this session's updates.</ref>
    <ref type="auth_path">Login as michael@opalinvest.com (or andrew@opalinvest.com) → Select Partner dropdown → Inflection Wealth Management → firmId=inflection. DO NOT use devBypass — broken for data-presence gates.</ref>
    <ref type="portal_server">bun run dev --port 5175 (from portal/ dir). Bun: /c/Users/AndrewBerman/.bun/bin/bun</ref>
  </references>

  <context>
    DT closed INFLFE.006 Phase 1 (portal commit 43411a79). Two hard errors fixed:
    1. Distribution tab "Unable to Load Distribution" — city drilldown crash (formatSegLabel seg.key undefined)
    2. Books tab "Unable to Load Books" — clients-tab-slim.json missing tax field TypeError

    RD sweep confirms: (a) both tabs now render without error boundary, (b) 5-vector AUA agreement
    holds at $199.6M canonical, (c) no regressions in other inflection tabs.

    Portal is on DEV branch. This sweep validates DEV. PROD bump is HELD until RD RAVC4 PASS.

    Note: Books firm overview AUA will show ~$182.5M (clients-tab-slim.json DG-1 — stale, DS~A fix
    pending separately). This is a data gap, NOT a frontend bug. Do not flag it as a test failure.
    The crash (TypeError on tax.taxable) is fixed — the headline AUA number is still stale data.
  </context>

  <phase id="0" when="setup">
    <step>
      <run>Start portal dev server: bun run dev --port 5175</run>
      <expect>Dev server running at localhost:5175</expect>
    </step>
    <step>
      <run>Auth: login as michael@opalinvest.com → Select Partner dropdown → Inflection Wealth Management</run>
      <expect>firmId=inflection JWT active. AUA strip visible (target: ~$199.6M post DS~A fix).</expect>
    </step>
  </phase>

  <phase id="1" when="targeted sweep — error fix verification">
    <step id="1">
      <objective>Distribution tab — no error boundary, drilldown functional</objective>
      <run>
        Navigate to Distribution tab.
        1. Confirm tab loads without "Unable to Load Distribution" error boundary.
        2. Screenshot Segment Analytics panel (donut + table).
        3. Click a state segment to drill down into cities. Confirm city list renders (no crash).
        4. Screenshot the city drilldown state.
        5. Note Segment Analytics total ($199.1M expected — $515K geographic exclusion is expected).
      </run>
      <accept>Tab renders. Drilldown does not crash. Total ~$199.1M (geographic exclusion expected).</accept>
      <reject>Error boundary "Unable to Load Distribution" still shows.</reject>
    </step>

    <step id="2">
      <objective>Books tab — no error boundary, advisor AUA visible</objective>
      <run>
        Navigate to Books/ tab.
        1. Confirm tab loads without "Unable to Load Books" error boundary.
        2. Screenshot firm overview panel (headline AUA will show ~$182.5M — this is a data gap, not a bug).
        3. Screenshot advisor list with per-advisor AUA (expect: sum ~$199.6M).
        4. Click one advisor to confirm drilldown loads (no crash).
      </run>
      <accept>Tab renders. No error boundary. Advisor list with AUA visible.</accept>
      <reject>Error boundary "Unable to Load Books" still shows.</reject>
    </step>

    <step id="3">
      <objective>5-vector AUA agreement check</objective>
      <run>
        Record observed values for all 5 vectors:
        1. Assets Overview main AUA total (dashboard.json headline)
        2. AUA toggle NMNC + NMEC + Existing (sum should = total_aua)
        3. Mix view total (equity + fi + alternatives + cash = total_aua)
        4. Distribution Segment Analytics total (~$199.1M expected — geographic exclusion)
        5. Books advisor sum (sum of per-advisor AUA QTD = total_aua)

        Note any vectors that do NOT agree at $199.6M (±$1K rounding for vectors 1/2/3/5;
        vector 4 allowed $515K geographic exclusion delta).
      </run>
      <accept>Vectors 1, 2, 3, 5 agree at ~$199.6M (±$1K). Vector 4 = ~$199.1M (delta expected).</accept>
    </step>

    <step id="4">
      <objective>Regression check — other inflection tabs</objective>
      <run>
        Quickly verify no regressions in:
        - PartnerAnalytics quarterly panel (AUA strip, donut, time-series)
        - Mix view (asset class breakdown)
        - Advisors tab (advisor list renders)
        Report any tab that shows an error boundary or blank render.
      </run>
      <accept>No new error boundaries or blank renders in other tabs.</accept>
    </step>
  </phase>

  <phase id="2" when="constitution doc update + commit">
    <step id="5">
      <objective>Update constitution doc with INFLFE.006 sweep results</objective>
      <run>
        File: portal/.frontend-dev/testing/inflection_advisor_intelligence.md

        Updates:
        - Distribution tab row: mark B1 fix PASS (drilldown no crash, ~$199.1M)
        - Books tab row: mark B2 fix PASS (no error boundary, advisor AUA visible)
        - AUA strip: confirm $199.6M (was $182.5M before DS~A fix)
        - INFLFE.006 sweep section: add evidence table for AC1-AC5 with observed values
        - Summary table: update GREEN/RED/YELLOW counts
        - Bundle Line 211 sweep uncommitted changes from prior session (already in working tree)

        Note data gaps (NOT failures):
        - Books firm overview AUA = ~$182.5M (DG-1: clients-tab-slim pending DS~A fix)
        - Bell curve not rendering (DG-4: no histogram in distribution.total — future enhancement)
        - City drilldown labels use name fallback not canonical key (DG-3: pending DS~A fix)
      </run>
    </step>

    <step id="6">
      <objective>Commit constitution doc (portal DEV)</objective>
      <run>
        Commit constitution doc changes in portal submodule (DEV branch):
        cd portal
        /c/Users/AndrewBerman/Desktop/ajb_workspace/.tools/safe-commit.sh \
          --author "0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "test(ADVI_INFLFE.006-rd): constitution doc — Distribution + Books fix sweep PASS" \
          -- .frontend-dev/testing/inflection_advisor_intelligence.md
        Push portal DEV.
        Then bump submodule pointer in CLOUD (workspace root).
      </run>
    </step>
  </phase>

  <phase id="3" when="RAVC to COO">
    <step id="7">
      <run>
        Send RAVC4 to 2.0.0_SA_COO:
        - AC1: Distribution tab renders (PASS/FAIL)
        - AC2: Distribution drilldown no crash (PASS/FAIL)
        - AC3: Books tab renders (PASS/FAIL)
        - AC4: 5-vector AUA table (observed values for all 5 vectors)
        - AC5: Regression check result (PASS/FAIL)
        - Constitution doc commit hash
        - Portal DEV commit hash (submodule bump)
        - Any data gaps observed (distinguish from test failures)
      </run>
    </step>
  </phase>

  <acceptance_criteria>
    <criterion id="AC1">Distribution tab renders without error boundary. Segment Analytics total ~$199.1M.</criterion>
    <criterion id="AC2">Distribution city drilldown functional — clicking a state shows city list without crash.</criterion>
    <criterion id="AC3">Books tab renders without error boundary. Per-advisor AUA visible.</criterion>
    <criterion id="AC4">AUA vectors 1, 2, 3, 5 agree at ~$199.6M (±$1K). Vector 4 ~$199.1M (geographic exclusion OK).</criterion>
    <criterion id="AC5">No regressions in PartnerAnalytics, Mix, Advisors tabs.</criterion>
    <criterion id="AC6">Constitution doc updated with sweep evidence. Committed + pushed (portal DEV). CLOUD submodule bumped.</criterion>
    <criterion id="AC7">RAVC4 to COO with all 5 vector values + pass/fail per AC.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>20260506T~1735Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Portal DEV commit 43411a79 is live. DS~A data fix (a9435bc90) is live in platinum/. Execute Phase 1 sweep now.</message>
  </go_signal>

  <final_verification>
    <date>2026-05-07</date>
    <portal_commit>52a6d84c (portal-v2.1.81)</portal_commit>
    <verified_by>0.4.2_RD_AdvisorIntelligence</verified_by>
    <summary>All checks PASS on PROD 52a6d84c. INFLFE.006 visual verification track closed.</summary>

    <check id="A" label="Stacked bars (nmnc+nmec)">
      <verdict>PASS</verdict>
      <evidence>
        bar_group_count=2; fills=[#2196f3 (blue/nmec), #4caf50 (green/nmnc)].
        timeseries_chart.json?firm=inf: 200 OK, 25 quarters, categories=['nmnc','nmec'].
        Q2 '26 raw: nmnc=$18,661,836.44 + nmec=$170,585,869.06 = $189.2M (FE patches last bar to canonical $199.6M).
        49F isInflectionFirm gate: timeseries_chart.json NOT fetched for 49F (PASS).
      </evidence>
    </check>

    <check id="B" label="QoQ growth tiles">
      <verdict>PASS</verdict>
      <evidence>
        NEW CLIENTS: $19.7M, +$4.18M (+27.0%) vs Q1 '26.
        EXISTING CLIENTS: $179M, +$15.5M (+9.5%) vs Q1 '26.
        TOTAL AUA: $199M, +$19.7M (+11.0%) vs Q1 '26.
        as of Apr 28, 2026.
      </evidence>
    </check>

    <check id="C" label="Regressions">
      <verdict>PASS</verdict>
      <evidence>
        No error boundaries on Inflection or 49F. Total AUA $199M. 49F bar chart unchanged (3 bar_groups, own fills).
      </evidence>
    </check>
  </final_verification>
</task_order>
