# Task Order: ADVI_INFGRD.004 — RD Option C Re-Validation (Post-INFGRD + F1-F3)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-infgrd-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — final gate before Inflection production sign-off (Andrew browser smoke)</priority>
  </metadata>

  <objective>
    Full Option C smoke of the Inflection portal against the final integrated state:
      - ADVI_INFGRD.003 COMPLETE: platinum artifacts reflect ~$191M / ~4 advisors (correct scope)
      - DS~A F1-F3 schema fixes COMPLETE: timeseries D_04 patch live (correct AUA scale + field naming)
      - Portal portal-v2.1.62 deployed: ADVI_INFPRTY UI suppressions live

    This is the definitive pre-production smoke. RAVC4 from this task is the final gate
    before COO dispatches Andrew sign-off request for Inflection production.
  </objective>

  <scope>
    <task id="1" label="Gate check">
      Confirm both prerequisites are live before starting smoke:
        1. AE RAVC from ADVI_INFGRD.003 (platinum $~191M, ~4 advisors, CF invalidated)
        2. DS~A RAVC4 from D_04 timeseries patch (timeseries_overview.json correct scale + shape)

      Do NOT start smoke until BOTH RACVs received. If gate is unclear, check with COO.
    </task>

    <task id="2" label="Option C smoke — full panel pass">
      Login as Andrew at opalinvest.dev, select Inflection in partner dropdown
      (AdvisorIntelligence/index.tsx firmId=inflection path).

      Panel-by-panel verification against expected state:

      OVERVIEW:
        - Stat tiles: total AUA ~$191M (NOT $429M), NNA YTD renders, new clients renders
        - AUA chart: quarterly bars render with non-zero values (~$191M scale)
        - GRO panel: market growth shows non-zero decomposition
        - NNA chart: renders correctly (confirmed PASS in prior smoke)

      ADVISORS TAB:
        - Leaderboard renders ~4 entries (NOT 9)
        - No ErrorBoundary crash (role_breakdown present — confirmed PASS in prior smoke)
        - No Keil Financial Partners row, no Jeremy Keil row (if non-Inflection)
        - Each advisor entry shows AUA, NNA, role

      BOOKS TAB:
        - Composition panel renders for at least one advisor
        - Fee Efficiency panel: HIDDEN for firmId=inflection (ADVI_INFPRTY suppression)

      DISTRIBUTION TAB:
        - AUA donut chart renders with non-empty slices
        - NNA distribution renders
        - OFC (Office) option: NOT present for firmId=inflection (ADVI_INFPRTY suppression)

      UNREACHABLE (pre-marked, do NOT open defects):
        - BooksTab advisor drill-through (Lambda path, confirmed gap in parity matrix)
        - ClientDetail panel (Lambda path, confirmed gap)
        - Any panel marked UNREACHABLE in INFLEC_BD_PARITY_MATRIX.md §4
    </task>

    <task id="3" label="Console + network check">
      Browser devtools check during smoke:
        - Zero JavaScript errors in console
        - No 404s or 5xx on platinum S3 key fetches
        - No HTML responses where JSON expected (CloudFront routing check)
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Overview total AUA stat tile shows ~$191M (within $140M–$250M range). Definitely
      NOT $429M — if $429M still shows, stop and report CF cache miss to COO.
    </criterion>
    <criterion id="2">
      AUA chart renders non-empty quarterly bars. GRO shows non-zero market growth.
    </criterion>
    <criterion id="3">
      Advisors tab shows ~4 entries. No Keil entries. No ErrorBoundary crash.
    </criterion>
    <criterion id="4">
      Fee Efficiency panel ABSENT on Books tab. OFC option ABSENT in Distribution tab.
      (ADVI_INFPRTY suppressions confirmed live.)
    </criterion>
    <criterion id="5">
      Zero JavaScript console errors. No unexpected 4xx/5xx on data fetches.
    </criterion>
    <criterion id="6">
      RAVC4 sent to 2.0.0_SA_COO with:
        - PASS/FAIL verdict per panel (table format)
        - Actual AUA value observed in UI
        - Actual advisor count observed in leaderboard
        - Screenshot hashes or panel state descriptions for audit trail
        - Any FAIL items with panel name + observed vs expected
      Subject: RAVC4 — ADVI_INFGRD.004 [PASS|FAIL] | $[X]M AUA | [N] advisors
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start until BOTH gate RACVs confirmed (INFGRD.003 + DS~A D_04 timeseries).
    Smoking pre-INFGRD data would validate wrong-scope artifacts.</constraint>
    <constraint>UNREACHABLE panels are pre-marked — do NOT open defects against them.
    Reference INFLEC_BD_PARITY_MATRIX.md §4 for the UNREACHABLE list.</constraint>
    <constraint>If AUA reads $429M instead of ~$191M, it is a CF cache miss — trigger
    CF invalidation (same pattern as prior invalidations) and re-check before declaring FAIL.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL"
                task="ADVI_INFGRD.003"
                status="open"
                note="Silver rebuild + full chain re-run must be COMPLETE with platinum
                at ~$191M, ~4 advisors, CF invalidated. AE RAVC is the go-signal."/>
    <dependency agent="0.4.0_DS_ClientPlatform~A"
                task="D_04 timeseries patch"
                status="in_progress"
                note="timeseries_overview.json must be live with correct AUA scale (~$191M
                quarterly bars) and correct field naming. DS~A RAVC4 is the go-signal.
                Both dependencies required before starting smoke."/>
  </dependencies>

  <deliverables>
    <deliverable type="mcp">RAVC4 to 2.0.0_SA_COO with full panel-by-panel verdict table,
    AUA + advisor count observed, console error status. This is the Inflection production
    sign-off gate — COO will relay to Andrew for final browser confirmation.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md §6 — Validation</ref>
    <ref type="parity_matrix">docs/architecture/INFLEC_BD_PARITY_MATRIX.md §4 — UNREACHABLE panels</ref>
    <ref type="portal">portal-v2.1.62 on opalinvest.dev (ADVI_INFPRTY suppressions)</ref>
    <ref type="option_c">AdvisorIntelligence/index.tsx — login as Andrew, Select Partner dropdown, firmId=inflection</ref>
  </references>
</task_order>
```
