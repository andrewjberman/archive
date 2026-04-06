# Task Order: ADVI_GLDRST.012 — Portal End-to-End Validation

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-26-gldrst-012</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Validate that the Advisor Intelligence portal renders correctly using
    data served from the new S3 key layout. This is a READ-ONLY validation
    task. Do NOT modify any portal code, API endpoints, or infrastructure.
    Produce a structured pass/fail report.
  </objective>

  <context>
    After .009 (migration gold rerun) + .007 (Lambda path migration) + .008
    (CloudFront behavior update), all portal data flows through the new S3
    key layout. This task validates that every user-facing feature renders
    correctly and that fallback paths work when pre-computed views are missing.
  </context>

  <depends_on>.009 (migration gold rerun must complete successfully)</depends_on>

  <scope>
    Validate every Advisor Intelligence portal feature. For each check,
    record PASS/FAIL with a screenshot or API response excerpt as evidence.

    ## Check 1: Header Metrics

    Navigate to the Advisor Intelligence page.
    Verify the header displays:
    - Total AUA (non-zero, formatted as currency)
    - Total NNA (can be negative, formatted as currency)
    - Client count (non-zero integer)
    - Period selector works (QTD, YTD, 1Y)

    ## Check 2: Distribution Tab

    Navigate to the Distribution tab.
    Verify:
    - NNA/AUA timeseries chart renders with data points
    - Geographic breakdown table populates
    - Architect breakdown table populates
    - Clicking a region/architect filters the timeseries

    ## Check 3: Leaderboard Tab

    Navigate to the Leaderboard tab.
    Verify:
    - Architect attribution table populates with rows
    - Columns: architect name, AUA, NNA, client count
    - Sorting works (click column headers)
    - MTD/QTD/YTD period toggle updates values

    ## Check 4: Books Tab — L1 (Firm Level)

    Navigate to the Books tab.
    Verify:
    - Composition donut chart renders with asset class segments
    - Total AUA displayed in donut center
    - Top holdings horizontal bars render
    - Clickable legend filters by asset class
    - Quarterly AUA metrics bar shows current + last 3 quarter-ends

    ## Check 5: Books Tab — L2 (Advisor Drill-Down)

    Click an advisor in the leaderboard or books view.
    Verify:
    - Advisor-level composition renders (donut + holdings)
    - Mix timeseries chart renders with historical data
    - Quarterly bars render (from pre-computed views via .001/.003)
    - Mix toggle switches between rich and simple views

    ## Check 6: Books Tab — L3 (Client Drill-Down)

    Click a client/relationship in the advisor view.
    Verify:
    - Client timeseries renders
    - Quarterly bars render (from pre-computed _views.json)
    - Composition breakdown renders (from _composition.json)
    - Open lots table renders (if available)

    ## Check 7: Clients Tab

    Navigate to the Clients tab.
    Verify:
    - Client list populates
    - Clicking a client shows detail panel
    - Client-level AUA and timeseries render

    ## Check 8: Pre-Computed View Fallback

    This is the critical graceful degradation test.

    Method: In the browser developer tools, intercept the API call for a
    _views.json file and force it to return 404. Verify:
    - The quarterly bars STILL render (via client-side deriveQuarterlyFromTimeseries)
    - No crash or blank panel
    - Console shows a warning (not an error) about fallback

    If the portal does not have a fallback path (.003 did not implement one),
    mark as FAIL and report to COO.

    ## Check 9: API Response Validation

    Using browser developer tools Network tab, capture 5 API responses:
    - /api/scoped/partners/books/firm/all/composition
    - /api/scoped/partners/books/firm/all/mix-views
    - /api/scoped/partners/books/advisor/{id}/timeseries (pick any advisor)
    - /api/scoped/partners/books/relationship/{id}/mix-timeseries (pick any client)
    - /api/partners (header metrics)

    For each, verify:
    - HTTP 200 response
    - Response body is valid JSON
    - Response contains expected data fields (non-empty arrays, non-null values)
    - No CORS errors in console
  </scope>

  <deliverable>
    A structured validation report in your session log with:
    - Each check (1-9): PASS/FAIL with evidence (screenshot description or API response excerpt)
    - Summary: X/9 checks passed
    - If any FAIL: which component is broken and which TO (.001-.009) likely caused it
    - Final verdict: CLEAR or BLOCKED (with blocking reason)

    Report to COO via send_message when complete.
  </deliverable>

  <constraints>
    - READ-ONLY. Do not modify any portal code, Lambda code, or S3 keys.
    - Do not push any commits. Do not deploy anything.
    - Run the portal locally (bun run dev --port 5175) pointed at production APIs.
    - Use browser developer tools for API inspection, not direct curl.
  </constraints>
  <tooling>
    <tool module="interpret.crossref_graph" when="during_validation">
      Run against portal/src/ to verify no orphaned imports or broken references
      after the S3 key migration. The graph should show zero new orphans compared
      to the pre-migration baseline.
    </tool>

    <tool module="adapt.coverage_auditor" when="during_validation">
      Compare: set of S3 API endpoints the portal calls vs set of S3 keys that
      exist at the new paths. Any endpoint returning 404 is a coverage gap.
    </tool>
  </tooling>
</task_order>
```
