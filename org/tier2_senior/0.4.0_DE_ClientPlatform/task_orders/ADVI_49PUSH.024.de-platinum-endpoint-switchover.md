<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-024-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~C</issued_to>
    <date>2026-04-09</date>
    <status>pending -- Phase 1 DONE (DEV 33fef24); Phase 2 blocked on DS .023 + AE deploy</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>6</wave>
    <phase>P3 compliance</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Switch all 8 non-platinum endpoints in advisor-intelligence.ts to their platinum/ paths,
    and delete the one legacy endpoint that has already been superseded. After this TO,
    advisor-intelligence.ts must contain zero references to gold/ or silver/ S3 paths.
    This is the companion frontend switchover for DS .023 (D_04 platinum compliance gaps).
  </objective>

  <context>
    DS TO .023 extends D_04 to publish 6 new platinum/ files. Once AE deploys and re-runs
    D_04, those files will exist in S3. Two of the 8 violations require no D_04 work at all
    (platinum files already exist) and can be switched immediately. The remaining 6 must wait
    for .023 + AE re-run before being switched, so you can validate the files exist before
    pointing the frontend at them.

    All violations are in portal/src/api/endpoints/advisor-intelligence.ts.
    All switches follow the same pattern: change the S3 key string in the existing function,
    do not change function signatures or TypeScript types.

    The TypeScript types were written against the gold/ schemas. DS .023 passes all objects
    through verbatim -- so no type changes are required for any of these switches.
  </context>

  <phase_1 label="Do immediately -- no D_04 dependency">

    <switch id="1">
      <function>getAdvisorFeeEfficiency (line ~596)</function>
      <current_path>artifacts/advisor_fee_efficiency.json</current_path>
      <platinum_path>platinum/firm/fee_efficiency.json</platinum_path>
      <notes>
        D_04 already writes platinum/firm/fee_efficiency.json. This is a pure path swap.
        The function may have a "legacy" comment; remove it after switching.
        Verify the platinum file is live in S3 before committing.
      </notes>
    </switch>

    <deletion id="2">
      <function>getPartnerAnalyticsHeader (line ~254)</function>
      <current_path>artifacts/partner_analytics/header_metrics_{suffix}.json</current_path>
      <action>DELETE the function entirely.</action>
      <notes>
        getPlatinumPartnerAnalytics already serves platinum/firm/partner_analytics_{suffix}.json.
        getPartnerAnalyticsHeader is a legacy stub -- no component should be calling it.
        Before deleting: grep all .tsx files to confirm zero call sites. If any call site
        exists, replace with getPlatinumPartnerAnalytics, then delete the old function.
      </notes>
    </deletion>

  </phase_1>

  <phase_2 label="After DS .023 complete + AE re-runs D_04">

    <switch id="3">
      <function>getHeaderSummary (lines ~217, 232)</function>
      <current_path>artifacts/summary/header_metrics.json</current_path>
      <platinum_path>platinum/firm/header_metrics.json</platinum_path>
      <notes>
        Two lines reference this path (possibly a variant for firmId param). Switch both.
        Before switching, curl platinum/firm/header_metrics.json from S3 (with a valid JWT
        via CloudFront) and confirm the file exists and is valid JSON.
      </notes>
    </switch>

    <switch id="4">
      <function>getTimeseriesChart (line ~270)</function>
      <current_path>artifacts/timeseries_chart.json</current_path>
      <platinum_path>platinum/firm/timeseries_chart.json</platinum_path>
      <notes>Straight path swap. Confirm file exists in S3 first.</notes>
    </switch>

    <switch id="5">
      <function>getEmployeeLeaderboard (line ~613)</function>
      <current_path>artifacts/employee_leaderboard.json</current_path>
      <platinum_path>platinum/firm/employee_leaderboard.json</platinum_path>
      <notes>Straight path swap. Confirm file exists in S3 first.</notes>
    </switch>

    <switch id="6">
      <function>advisor mix Lambda (line ~534)</function>
      <current_path>gold/entities/advisors/{id}/mix.json</current_path>
      <platinum_path>platinum/advisors/{id}/mix.json</platinum_path>
      <notes>
        This path is served via Lambda (not direct S3). The Lambda handler constructs
        the S3 key from the advisor id parameter. Find the key construction in the Lambda
        handler (partners-api) and update the prefix from gold/entities/advisors/ to
        platinum/advisors/. Also update the corresponding path string in advisor-intelligence.ts
        if it constructs the route URL using a gold/ path fragment.
        Coordinate with DT if the Lambda key construction is in a separate file.
      </notes>
    </switch>

    <switch id="7">
      <function>getClientViews (line ~555)</function>
      <current_path>entities/clients/{relId}_views.json</current_path>
      <platinum_path>platinum/clients/{relId}/views.json</platinum_path>
      <notes>
        Note the path shape change: gold uses underscore suffix ({relId}_views.json),
        platinum uses directory format ({relId}/views.json) -- DS .023 normalizes this.
        Update accordingly. Confirm file exists for a sample relId in S3 before switching.
      </notes>
    </switch>

    <switch id="8">
      <function>getClientComposition (line ~569)</function>
      <current_path>entities/clients/{relId}_composition.json</current_path>
      <platinum_path>platinum/clients/{relId}/composition.json</platinum_path>
      <notes>
        Same directory normalization as client views (underscore suffix -> /composition.json).
        Confirm file exists for a sample relId in S3 before switching.
      </notes>
    </switch>

  </phase_2>

  <validation>
    After all 8 switches + 1 deletion:

    1. Run: grep -r "gold/" portal/src/api/endpoints/advisor-intelligence.ts
       Expected output: zero matches.

    2. Run: grep -r "silver/" portal/src/api/endpoints/advisor-intelligence.ts
       Expected output: zero matches.

    3. Run: grep -r "artifacts/" portal/src/api/endpoints/advisor-intelligence.ts
       Expected output: zero matches.

    4. Run: comp-routes auth-map (confirm all ADVI CloudFront behaviors still route correctly)

    5. Build portal (bun run build) -- confirm zero TypeScript errors introduced by the switches.

    6. Smoke test: open opalinvest.dev, navigate to each ADVI tab, confirm panels load data.
       Pay specific attention to: header metrics bar, timeseries chart, employee leaderboard,
       advisor mix panel, client views, client composition.

    7. Report: list all 8 switched paths + the 1 deleted function in your session log.
  </validation>

  <acceptance_criteria>
    1. advisor-intelligence.ts contains zero gold/ or silver/ S3 path references
    2. getPartnerAnalyticsHeader function deleted, no call sites remain
    3. Portal build clean (zero TS errors)
    4. All switched panels render data correctly in opalinvest.dev
    5. Phase 1 switches committed and deployed before Phase 2 begins
    6. Phase 2 switches committed and deployed only after confirming platinum files exist in S3
  </acceptance_criteria>


  <compiler_tools>
    comp-routes auth-map
      -- Run after EACH phase switch (not just at the end). Verifies all ADVI CloudFront
         behaviors still route correctly after each path change. Catches misconfigured
         origins before they hit production.

    comp-routes trace getAdvisorFeeEfficiency
      -- Before Phase 1 switch: confirms the current gold/ path being served and the
         CF behavior that will be affected. Run for each endpoint being switched.

    comp-blast advisor-intelligence.ts
      -- Shows all portal components that import from advisor-intelligence.ts.
         Run before deleting getPartnerAnalyticsHeader to confirm zero call sites
         remain after the switch.

    comp-transform schema-check PartnerAnalytics
    comp-transform schema-check DistributionTab
    comp-transform schema-check ClientsTab
    comp-transform schema-check AdvisorsTab
      -- Run after all Phase 2 switches are committed. Confirms no rendered field
         became unmapped after the path changes.
  </compiler_tools>

</task_order>
