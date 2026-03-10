<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-F2-elapsed</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
  </metadata>

  <objective>
    The F2 projection ghost bars work on Annually and Quarterly but NOT on Monthly.
    The projection works on Year view. It must also work on Quarter and Month views.
    This is the same projection functionality — ghost bar showing the extrapolated
    full-period value — applied consistently across all three granularities.

    Root cause: computePeriodDays (line 411-441) uses `new Date()` (today's wall clock)
    to compute elapsedDays. The latest data is from 2026-01-13. When granularity is
    Monthly, the last bar is period `2026-01` (January). elapsedDays = (Mar 9 - Jan 1)
    = 68 days. totalDays = 31. Since 68 >= 31, the guard at line 457
    `if (elapsedDays >= totalDays) return aug` concludes January is complete and skips
    the projection. But January is NOT complete — we only have 13 days of data.

    Quarterly works because Q1 (90 days) hasn't fully elapsed by March 9 (68 days).
    Annually works because 2026 (365 days) hasn't fully elapsed. Monthly is the only
    granularity where the wall clock has moved past the data's actual period.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Change computePeriodDays to accept the data's actual end date
      for the period instead of using `new Date()`. The aggregated data already stores
      `endDate` on each entry (set at line 231: `existing.endDate = point.date`). Pass
      this value into computePeriodDays and use it to compute elapsedDays:
      ```
      elapsedDays = (dataEndDate - periodStart) / 86400000
      ```
      NOT:
      ```
      elapsedDays = (new Date() - periodStart) / 86400000
      ```
    </requirement>
    <requirement id="2">This change affects all three projection blocks — AUA
      (augmentedAuaData), NNA (augmentedNnaData), and GRO (augmentedGroData). Each
      must pass the entry's endDate to computePeriodDays. For GRO, the data structure
      may not have endDate — if so, derive it from the period key (last day of the
      source month, since GRO data is monthly pre-aggregation).</requirement>
    <requirement id="3">Verify with the actual data: last data date is 2026-01-13.
      At Monthly granularity, the last bar (2026-01) should now show a ghost projection
      because elapsedDays = 13, totalDays = 31, and 13 < 31.</requirement>
    <requirement id="4">The ratio should also use the data end date:
      `ratio = totalDays / elapsedDays` where elapsedDays is based on data, not wall
      clock. This means the projection extrapolates from 13 days to 31 days (ratio ~2.4)
      which is correct — "if this pace continues for the full month."</requirement>
    <requirement id="5">Do NOT change the projection formula itself (delta-based for AUA,
      flow-based for NNA/GRO). Only change how elapsedDays is computed.</requirement>
    <requirement id="6">After fixing, confirm all three granularity views show projections
      on the last bar: Monthly (2026-01), Quarterly (2026-Q1), Annually (2026).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Monthly view shows ghost bar projection on the last bar.</criterion>
    <criterion id="2">Quarterly view still shows ghost bar projection (no regression).</criterion>
    <criterion id="3">Annually view still shows ghost bar projection (no regression).</criterion>
    <criterion id="4">All three views (AUA, NNA, GRO) project correctly at all three
      granularities.</criterion>
    <criterion id="5">TypeScript clean. Portal DEV commit with --author flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT use new Date() or any wall-clock reference in elapsedDays
      computation. The elapsed time must come from the data itself.</constraint>
    <constraint>Do NOT change the projection formula, cap logic, or ghost rendering.
      Only change the elapsed days input.</constraint>
    <constraint>The GRO projection (augmentedGroData) may need special handling since
      GRO data is monthly and aggregated differently. Make sure the endDate or equivalent
      is available for GRO entries too.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_49FNV3.F2-fix" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit fixing elapsedDays to use data date.</deliverable>
  </deliverables>

  <references>
    <ref type="source">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</ref>
    <ref type="prior">Portal DEV 8e9facd (project last bar, not calendar-current)</ref>
    <ref type="prior">Portal DEV 9ce8d3b (AUA delta-based projection)</ref>
  </references>
</task_order>
