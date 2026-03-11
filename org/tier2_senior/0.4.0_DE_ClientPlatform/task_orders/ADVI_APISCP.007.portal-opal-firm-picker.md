```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-apiscp-007-de-firm-picker</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_APISCP-007</thread_serial>
  </metadata>

  <objective>
    Advisor Intelligence currently hardcodes selectedFirmId='49financial' and never passes
    a firm selection signal to the static S3-backed API calls. Opal employees need a firm
    picker dropdown and all static advisor-intelligence fetch calls must append ?firm={selectedFirmId}
    so the router (v7) can route them to the correct partner bucket. Partner users (non-internal)
    do not see the dropdown — their routing is determined by their JWT firmId alone.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Fix selectedFirmId default. The current default is '49financial', which is a display
      name — the actual data firmId for 49 Financial is 'bd'. The router routes to
      opal-data-{firmId}, so the value must match the S3 bucket suffix.

      Change: useState&lt;string&gt;('49financial') -> useState&lt;string&gt;('bd')

      Confirm the firm picker dropdown options also use data firmIds (e.g., value='bd',
      label='49 Financial'), not display names as values. If getAllowedPartners() returns
      a firmId field per partner, use that as the option value.
    </requirement>
    <requirement id="2">
      All static advisor-intelligence API call functions in advisor-intelligence.ts must
      accept an optional firmId parameter and append ?firm={firmId} to the URL when provided.

      Static call functions (currently take no firmId param):
        - getPartnerAnalytics(granularity)
        - getCumulativeChart() [timeseries_chart.json]
        - getClientsTab() [clients_tab.json]
        - getLeaderboard() [architect_leaderboard.json]
        - getRollingFlows() [advisor_rolling_flows.json]
        - getHeaderMetrics() / getHeaderSummary() [header_metrics.json]
        - getAdvisorBook(advisorId) [advisors/{advisorId}/book.json]
        - getClientDetail(clientKey) [clients/{clientKey}.json]

      Each function signature gains an optional firmId?: string parameter.
      When firmId is provided, append ?firm={firmId} to the URL.
      When firmId is not provided, URL is unchanged (partner users — router uses X-Firm-Id).
    </requirement>
    <requirement id="3">
      In AdvisorIntelligence.tsx, determine whether the user is internal:
        const { claims } = useAuth()  // or however auth context is accessed
        const isInternal = claims?.tier === 'internal'

      Pass selectedFirmId to all static API call sites when isInternal is true.
      For partner users (isInternal false), do not pass firmId to static calls — leave
      the URL without ?firm= so routing uses X-Firm-Id from the JWT as before.

      The selectedFirmId state is already threaded into tabs as firmId={selectedFirmId}.
      The tabs pass this to their useQuery calls. Confirm the tab components forward this
      to the static call functions (or update them if they don't).
    </requirement>
    <requirement id="4">
      The firm picker dropdown is already partially wired (selectedFirmId state +
      handlePartnerChange + PartnerAnalytics component). Confirm the dropdown:
        - Is visible ONLY for internal users (isInternal check)
        - Partner users see no dropdown
        - The selected value drives both static and dynamic API calls

      Do not redesign the component — the existing structure is fine. Just ensure the
      visibility gate is wired to isInternal.
    </requirement>
    <requirement id="5">
      E2E verification (perform after AE DynamoDB patch + DT router v7 are both live):
        1. Log in as an Opal user.
        2. Navigate to Advisor Intelligence.
        3. Confirm the firm picker dropdown is visible.
        4. Confirm the page loads with 49 Financial data (selectedFirmId='bd' default).
        5. If multiple partners are available, switch the dropdown and confirm data changes.
        6. Log out. Log in as a 49 Financial partner user.
        7. Confirm no dropdown is visible.
        8. Confirm the page loads correctly (firmId from JWT, no ?firm= in requests).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Opal user logs in, navigates to Advisor Intelligence, page loads (no blank/error).
      Network tab: static calls include ?firm=bd. No request goes to opal-data-null or
      opal-data-opal-capital.
    </criterion>
    <criterion id="2">
      Partner user (49 Financial) logs in, navigates to Advisor Intelligence. Network tab:
      static calls have NO ?firm= query param. X-Firm-Id header present from JWT.
    </criterion>
    <criterion id="3">
      Firm picker dropdown visible for Opal user, hidden for partner user.
    </criterion>
    <criterion id="4">
      selectedFirmId default is 'bd' (not '49financial').
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do NOT add ?firm= to static calls for partner users. Partner routing uses X-Firm-Id
      exclusively. Adding ?firm= for partners would put an unexpected query string in
      the cache key (no-op for now, confusing forever).
    </constraint>
    <constraint>
      Dynamic calls (getTimeSeries, getSnapshot, getFilters, etc.) already pass ?firmId=.
      Do NOT rename those to ?firm=. The ?firm= param is ONLY for static file calls
      going through shared-advisor-router. Dynamic calls go to API Gateway and use ?firmId=.
    </constraint>
    <constraint>
      Commit to DEV. DT pushes. Do not push to PROD.
    </constraint>
    <constraint>
      Wait for AE CloudOps (DynamoDB patch) and DT (router v7) to be live before
      performing E2E verification (req 5). Portal changes can be committed to DEV
      independently — they are inert until the backend is ready.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_APISCP.007.opal-dynamo-patch-and-cf-cache"
      status="pending"/>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_APISCP.007.router-v7-opal-routing"
      status="pending"/>
    <!-- DE can implement and commit immediately. E2E verify (req 5) waits for AE + DT. -->
  </dependencies>

  <deliverables>
    <deliverable type="commit">
      Portal DEV commit: static API functions accept optional firmId, ?firm= appended for
      internal users, selectedFirmId default fixed to 'bd', firm picker gated to isInternal.
      Session log with portal DEV commit hash.
    </deliverable>
    <deliverable type="document">
      E2E verification results (req 5) documented in session log after AE + DT are live.
    </deliverable>
  </deliverables>
</task_order>
```
