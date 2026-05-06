<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.006</id>
    <project>ADVI_INFLFE</project>
    <title>Inflection frontend: Distribution + Books hard errors + AUA alignment verification (gates on DS 006-data fix landing)</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>staged</status><!-- Gates on ADVI_INFLFE.006-data (DS~A) completing and RAVC landing to COO. Partner_analytics files must show $199.6M before DT debugging begins — otherwise error investigation may chase stale-data red herrings. -->
    <priority>high</priority>
    <estimated_effort>~2-3h DT (investigation + fix + portal commit + RD sweep)</estimated_effort>
  </metadata>

  <references>
    <ref type="data_fix_gate">ADVI_INFLFE.006-data (DS~A): INF_D_04 _build_aua_view rep-coverage fix. Gates Phase 1 of this TO. DS~A RAVC to COO → COO issues Phase 1 GO to DT.</ref>
    <ref type="user_requirement">Andrew 2026-05-06: "All AUA numbers have to agree, no matter how we get there (through assets, through advisors, etc)." Canonical: May 5 = $199,649,186.31; May 6 = $200.83M.</ref>
    <ref type="reported_issues">
      1. AUA toggle "Assets Overview" — no NMNC/NMEC breakdown (data fix resolves; DT verifies render)
      2. Mix view sums to $187.3M instead of $199.6M (data fix likely resolves; DT confirms)
      3. Distribution tab "Segment Analytics" — shows $183M + bell curve missing + hard error "Unable to Load Distribution"
      4. Books/ tab — hard error "Unable to Load Books, We encountered an error while loading this tab"
    </ref>
    <ref type="s3_data_confirmed_present">
      platinum/firm/activity_scan.json (May 5 16:23:58)
      platinum/firm/cash_drag.json (May 5 16:24:08)
      platinum/firm/concentration_risk.json (May 5 16:24:09)
      platinum/firm/partner_analytics_quarterly.json (May 6 10:42:28 — will be updated by DS~A fix)
      platinum/firm/mix_summary.json (May 5 17:45:32 — has $199.6M in mix_periods)
    </ref>
    <ref type="prior_inflfe_tos">INFLFE.001-005 COMPLETE. Error boundaries wired (inflection/index.tsx:28-60 TabErrorFallback). INFLFE.003 defensive guards on ActivityScanSection/CashDragSection (allAuaZero). INFLFE.005 CloudWatch sentinels live (Opal/InflectionSentinels).</ref>
    <ref type="portal_submodule">portal/ — DEV branch. bun install &amp;&amp; bun run dev --port 5175. Portal auth: login as Andrew + Select Partner dropdown → Inflection → firmId=inflection → opal-data-inf (devBypass broken for data-presence gates; use full login flow).</ref>
  </references>

  <context>
    Two categories of issues:

    CATEGORY A — Wrong AUA totals (resolved by DS~A INFLFE.006-data data fix):
    The partner_analytics_quarterly/monthly.json files had $182.5M (partial aum_snapshot,
    rep 6 missing). After DS~A fix, these files will show $199.6M. Mix view and Distribution
    total should auto-correct once the data is right. DT must VERIFY, not re-implement.

    CATEGORY B — Hard errors (DT investigation required):
    Distribution tab and Books/ tab both show "Unable to Load [tab], We encountered an error
    while loading this tab." This is the TabErrorFallback at inflection/index.tsx:37-40.
    The platinum data EXISTS in S3 — activity_scan.json, cash_drag.json,
    concentration_risk.json are all present. The error is in the fetch chain or render path.

    Likely causes to investigate (in priority order):
    1. opal-partners-data Lambda: is it returning an error for inflection firm?
       Check CloudWatch logs for the Lambda when Distribution/Books tab loads.
    2. CloudFront routing: comp-routes behaviors — does the Distribution endpoint
       route to the right origin for inflection? comp-routes trace [endpoint function].
    3. Response shape mismatch: InflectionInsightsPanel or DistributionTab receiving
       a shape that crashes on mount. Check warnOnInflection* sentinel logs in CW.
    4. Timeout: API_TIMEOUT_MS may be too short for cold Lambda starts.

    All AUA numbers must agree across all views:
    - Assets Overview main number
    - Assets Overview AUA toggle (sum of NMNC + NMEC + Existing = total)
    - Assets Overview Mix view (sum of equity + fi + alternatives + cash = total)
    - Distribution tab / Segment Analytics total
    - Books/ tab advisor totals (sum across advisors = firm total)
    Numbers should agree at $199.6M (May 5) or $200.83M (May 6) depending on data_as_of.
  </context>

  <phase id="0" when="BEFORE starting any code — verify DS~A data fix landed">
    <step>
      <run>
        Confirm DS~A INFLFE.006-data RAVC received by COO. Then verify S3:
          aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json - \
            | python3 -c "import sys,json; d=json.load(sys.stdin);
              aua=d['views']['aua']['donut'];
              print('total:', aua['total'], 'segments:', [s['key']+':'+str(round(s['aua']/1e6,1))+'M' for s in aua['segments']])"

        Expected: total ~$199.6M, NMNC segment present ~$174M.
        If still $182.5M: DO NOT proceed. Notify COO — DS~A fix has not landed yet.
      </run>
    </step>
  </phase>

  <phase id="1" when="after Phase 0 confirms data fix landed — frontend verification">
    <step id="1">
      <objective>Run portal dev server, load Inflection page, capture all AUA numbers.</objective>
      <run>
        Start portal: bun run dev --port 5175
        Navigate to Inflection Wealth Management as Andrew (full login + partner select).
        Record observed values for:
        a. Assets Overview main AUA total
        b. Assets Overview AUA toggle — NMNC / NMEC / Existing values (do they render?)
        c. Assets Overview Mix view total (sum of asset classes shown)
        d. Distribution tab total (Segment Analytics panel)
        e. Distribution tab bell curve — renders or blank?
        f. Books/ tab — renders or hard error?

        Check browser console for errors. Check network tab for failed API calls.
      </run>
    </step>

    <step id="2">
      <objective>Diagnose Distribution + Books hard errors.</objective>
      <run>
        For the "Unable to Load" error boundary trigger:
        1. Check CloudWatch logs for opal-partners-data Lambda:
           aws logs filter-log-events --log-group-name /aws/lambda/opal-partners-data \
             --start-time $(date -d '2 hours ago' +%s000) \
             --filter-pattern "inflection" 2>&gt;&amp;1 | head -50
        2. Check Opal/InflectionSentinels CloudWatch metrics (INFLFE.005 live):
           Look for ERROR-level events in the last 2 hours.
        3. comp-routes trace [distribution endpoint function] — confirm CF behavior.
        4. In InflectionInsightsPanel.tsx (lines 60-85): what queryFn are the 3 useQuery
           hooks calling? What URL/S3 key do they resolve to for firmId=inflection?
           If they call getInflectionActivityScan → confirm S3 key and Lambda routing.
        Document: exact fetch URL, HTTP status, response body (or error), Lambda log line.
      </run>
      <expect>Clear root cause identified: wrong URL, wrong routing, Lambda error, or shape mismatch.</expect>
    </step>

    <step id="3">
      <objective>Fix the identified root cause(s).</objective>
      <run>
        Apply targeted fix based on step 2 findings. Common patterns:
        - Wrong S3 key: fix endpoint resolver for inflection firm
        - Lambda error: fix opal-partners-data inflection routing
        - Shape mismatch: add guard/fallback (follow INFLFE.003 pattern)
        - Timeout: increase API_TIMEOUT_MS at advisor-intelligence.ts:~118

        comp-transform schema-check before any portal component edit:
          .tools/comp-transform schema-check Distribution
          .tools/comp-transform schema-check InflectionInsightsPanel

        Fix must address: Distribution tab renders correctly with bell curve,
        Books/ tab renders correctly, no error boundary triggered.
      </run>
    </step>

    <step id="4">
      <objective>Verify all AUA numbers agree.</objective>
      <run>
        With portal running after fixes:
        a. Assets Overview total = ~$199.6M (or May 6 canonical $200.83M)
        b. AUA toggle: NMNC + NMEC + Existing ≈ total_aua (within $1K rounding)
        c. Mix view: equity + fi + alternatives + cash ≈ total_aua
        d. Distribution tab total ≈ total_aua
        e. Books/: sum of per-advisor AUA ≈ total_aua

        Any vector that doesn't agree = additional data bug. Document and flag to COO.
        Do NOT patch the frontend to force agreement — fix the data path.
      </run>
      <expect>All 5 vectors agree at canonical AUA (±1K rounding). No error boundaries triggered.</expect>
    </step>

    <step id="5">
      <objective>Portal commit + push DEV.</objective>
      <run>
        .tools/safe-commit.sh --author "0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "fix(ADVI_INFLFE.006): Distribution + Books error fix + AUA alignment [inflection]" \
          -- [changed portal files]
        Push portal DEV. No PROD bump until RD Playwright sweep passes (INFLFE.006-rd).
      </run>
    </step>

    <step id="6">
      <objective>RAVC to COO.</objective>
      <run>
        Send RAVC to 2.0.0_SA_COO:
        - Root cause of Distribution + Books errors (confirmed)
        - Fix applied (commit hash)
        - All 5 AUA vectors (values observed post-fix)
        - Any remaining mismatches flagged as data gaps (not frontend bugs)
        - comp-transform schema-check results
        - Portal DEV commit hash
        COO will coordinate RD Playwright sweep (INFLFE.006-rd TO).
      </run>
    </step>
  </phase>

  <acceptance_criteria>
    <criterion id="AC1">Distribution tab renders without error boundary. Bell curve visible. Segment Analytics total ≈ $199.6M.</criterion>
    <criterion id="AC2">Books/ tab renders without error boundary. Per-advisor AUA visible.</criterion>
    <criterion id="AC3">AUA toggle in Assets Overview shows NMNC + NMEC + Existing segments. Sum ≈ total_aua.</criterion>
    <criterion id="AC4">Mix view total ≈ $199.6M (asset class sum = total AUA).</criterion>
    <criterion id="AC5">All 5 AUA vectors agree at canonical total (≤$1K rounding delta).</criterion>
    <criterion id="AC6">No browser console errors or network 4xx/5xx when loading Distribution or Books tabs.</criterion>
    <criterion id="AC7">comp-transform schema-check on modified components: no MISSING fields (NOTE is acceptable).</criterion>
    <criterion id="AC8">RAVC to COO includes all 5 AUA vector values + root cause documentation.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="before_edit">comp-routes behaviors + comp-routes trace [endpoint] for any route being modified. comp-transform schema-check [Component] before any portal component edit.</phase>
    <phase id="before_commit">comp-transform schema-check on ALL modified components. If Lambda modified: comp-iam service opal-partners-data.</phase>
    <phase id="after_fix">5-vector AUA agreement check (browser observation documented in RAVC).</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>GATES ON DS~A INFLFE.006-data. COO will issue Phase 1 GO after DS~A RAVC confirms partner_analytics files updated to $199.6M.</item>
    <item>RD Playwright sweep (INFLFE.006-rd) follows DT RAVC. COO coordinates after DT Phase 1 closes.</item>
    <item>If any AUA vector remains wrong after DS~A fix + DT frontend fix: DT surfaces as new data bug (separate TO/RAVC). Do NOT paperpatch the frontend to force numbers.</item>
  </cross_domain_coordination>

  <go_signal>
    <issued_at>STAGED — awaiting DS~A INFLFE.006-data RAVC to COO + COO GO to DT</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status staged. COO will issue Phase 1 GO after DS~A confirms $199.6M in partner_analytics files. DT: Phase 0 (data verification) can run any time. Phase 1 gates on DS~A RAVC.</message>
  </go_signal>
</task_order>
