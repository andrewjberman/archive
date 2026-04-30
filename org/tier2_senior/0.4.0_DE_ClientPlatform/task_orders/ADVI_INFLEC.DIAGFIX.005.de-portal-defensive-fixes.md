<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.005</id>
    <project>ADVI_INFLEC</project>
    <title>Portal defensive fixes — Books null-check + date cap + Continuous view investigation</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- GT-recon 2026-04-30 Session 50: DE confirmed COMPLETE via session_wrap_diagfix005.md; portal commit d565f8b3 (Tasks A+B+C); pushed to origin/DEV + parent CLOUD 082a3a80a -->
    <priority>high</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §C4 §C2 §C9</ref>
    <ref type="target_component_1">portal/src/components/books/ClientsTab.tsx line 288-291</ref>
    <ref type="target_component_2">portal/src/components/partner-analytics/PartnerAnalytics.tsx line 1844-1848</ref>
    <ref type="target_investigation">portal/src/components/partner-analytics/PartnerAnalytics.tsx — Continuous view toggle; s3 timeseries_chart.json vs Lambda endpoint routing</ref>
    <ref type="crash_root">ClientsTab.tsx: dash.clients_tab.headline on undefined — TypeError caught by ErrorBoundary</ref>
    <ref type="date_bug">PartnerAnalytics.tsx: end_date read directly from timeseries period (shows '2026-06-30' for current quarter)</ref>
  </references>

  <context>
    Three portal-side tasks. DIAGFIX.002 (DS) and DIAGFIX.004 (DS) are the primary fixes
    — this TO adds defensive belt-and-suspenders for resilience regardless of DS progress.

    TASK A — Books tab crash (belt-and-suspenders):
    ClientsTab.tsx line 288-291 does:
      { ...dash.clients_tab, headline: { ...dash.clients_tab.headline, ... } }
    When clients_tab is undefined (current state — dashboard.json is a thin stub without
    split: true), this throws TypeError. DS DIAGFIX.002 fixes the root cause (adds split: true
    + correct clients_tab.json schema). This TO adds a null-guard so the portal
    fails gracefully instead of crashing to ErrorBoundary if the data is ever missing.

    TASK B — "Jun 30, 2026" date display (belt-and-suspenders):
    PartnerAnalytics.tsx line 1844 reads end_date from the selected timeseries period.
    For 2026Q2, end_date = '2026-06-30' (projected quarter end), rendering "Jun 30, 2026"
    as the "as of" date. DS DIAGFIX.004 fixes the upstream timeseries script to emit
    end_date = data_as_of for in-progress periods. This TO adds a portal-side cap:
      display_date = min(end_date, data_as_of)   // use actual snapshot if period is open
    One-line change, defensible regardless of DS fix.

    TASK C — Continuous view data path investigation:
    The Distribution tab has a Continuous view toggle (AreaChart with 2-year daily data).
    For 49F this is served by the opal-partners-data Lambda. For Inflection it is unclear
    whether: (a) timeseries_chart.json (436KB, s3://opal-data-inf/platinum/firm/) is the
    source and is already wired, or (b) the Continuous toggle expects the Lambda endpoint
    which may not route to Inflection. DE needs to trace the data path and report.
    This is an investigation: either confirm working or document what's needed to wire it.
  </context>

  <scope>
    TASK A — ClientsTab.tsx null-guard (line 288-291):

    Read ClientsTab.tsx. Locate the spread that throws:
      { ...dash.clients_tab, headline: { ...dash.clients_tab.headline, ... } }

    Add null-guard:
      if (!dash.clients_tab || !dash.clients_tab.headline) {
        return &lt;div className="empty-state"&gt;Client data unavailable&lt;/div&gt;;
      }
    (or equivalent early-return / conditional render pattern already used in this file)

    Ensure: ErrorBoundary is no longer triggered by absent clients_tab data.
    The Books tab should show a graceful "unavailable" state instead of crashing.

    Also check: does the Books tab show a loading state while clients_tab is null?
    If there's an existing loading/error UI pattern in the file, use that.

    TASK B — PartnerAnalytics.tsx date cap (line 1844-1848):

    Read PartnerAnalytics.tsx. Locate the "as of" date computation at line ~1844.
    It likely reads: displayDate = selectedPeriod.end_date (or similar).

    Add a cap against data_as_of from the timeseries root:
      const dataAsOf = timeseriesData?.data_as_of;
      const periodEndDate = selectedPeriod?.end_date;
      const displayDate = dataAsOf &amp;&amp; periodEndDate &amp;&amp; periodEndDate &gt; dataAsOf
        ? dataAsOf
        : periodEndDate;

    Use displayDate for the "as of" sub-caption render.
    This prevents "Jun 30, 2026" from showing for an in-progress quarter.

    TASK C — Continuous view investigation:

    In PartnerAnalytics.tsx (or the file handling the Continuous toggle):
    1. Trace the data fetch for the Continuous view (AreaChart 2-year daily).
    2. Is it fetching timeseries_chart.json from S3 directly (via getPlatinumFirmTimeseriesChart
       or similar)? If so, check if opal-data-inf is in the bucket routing.
    3. Or does it call the opal-partners-data Lambda? If so, does the Lambda routing
       support firmId=inflection?

    Document findings in session log:
    - If Continuous is already wired to timeseries_chart.json and it's routing to
      opal-data-inf: WORKING — just needs DS to refresh the stale April 27 file.
    - If Continuous goes through the Lambda endpoint with no Inflection routing: note
      the gap + what routing change is needed (AE scope, not DE).
    - If Continuous is blocked by the AUA scope bug: note it; it's a DS/AE problem.

    All portal changes — pre-commit gate:
    bun run typecheck (portal/) — must pass 0 errors.
    Component tests if any exist for ClientsTab/PartnerAnalytics.

    Commit to DEV branch as per portal commit protocol.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check ClientsTab</run>
        <expect>No MISSING fields introduced by the null-guard change.
        NOTE fields OK. UNUSED fields at clients_tab prop level — investigate.</expect>
        <if_mismatch>Document any schema gaps in RAVC.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check PartnerAnalytics</run>
        <expect>No MISSING fields introduced by the date cap change.
        Confirm data_as_of is accessible at the point of the displayDate computation.</expect>
        <if_mismatch>If data_as_of is not in scope at line 1844, trace where it is available
        and thread it down or pull it from a different prop.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>cd portal &amp;&amp; /c/Users/AndrewBerman/.bun/bin/bun run typecheck</run>
        <expect>0 TypeScript errors. 0 new regressions.</expect>
        <if_mismatch>STOP. Fix type errors before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      ClientsTab.tsx: when clients_tab is undefined, Books tab renders graceful empty/loading
      state instead of throwing TypeError to ErrorBoundary.
      Evidence: code snippet showing null-guard + bun typecheck 0 errors.
    </criterion>
    <criterion id="2">
      PartnerAnalytics.tsx: "as of" date for an in-progress quarter renders data_as_of
      (April 28) not projected end date (June 30) when end_date > data_as_of.
      Evidence: code snippet showing date cap logic.
    </criterion>
    <criterion id="3">
      Continuous view data path documented in session log:
      - Source (timeseries_chart.json or Lambda endpoint) identified.
      - Whether Inflection routing is in place or what's needed to wire it.
    </criterion>
    <criterion id="4">
      bun typecheck 0 errors. All changes committed to DEV branch.
      Evidence: typecheck output + commit hash in session log.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO: commit hash, typecheck pass, Continuous view finding,
      and confirmation that Books tab no longer crashes to ErrorBoundary.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="independent"/>
    Defensive belt-and-suspenders — does NOT wait for DS DIAGFIX.002/.004.
    Parallelizable with all other DIAGFIX TOs.
    TASK C (Continuous investigation) may surface an AE routing task — COO will route
    if needed after DE reports findings.
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      If TASK C finds Continuous view requires Lambda routing for Inflection:
      COO routes follow-up TO to 0.7.0_AE_CloudOps or 0.6.1_AE_PartnerETL.
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    Portal commits go to DEV branch. Standard portal commit identity for DE.
    Session log: org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-29/diagfix005_portal_defensive.md
  </commit_identity>
</task_order>
