<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-snapshot-lookback-frontend-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_SNPLBK-001</thread_serial>
    <thread_ref>org/threads/ADVI_SNPLBK-001-snapshot-lookback-regression-diagnosis/</thread_ref>
  </metadata>

  <objective>
    Fix the Snapshot Lookback regression on the Distribution tab. The quarterly "time machine"
    strip (current + q1/q2/q3 period buttons) is no longer rendering in the Segment Analytics
    panel, despite the backend S3 JSON being fully intact. COO verified the published quarterly
    JSON at s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json contains
    all required keys (views.geo/adv/nna each with current, q1, q2, q3; periods with all 4 keys).
    The regression is confirmed frontend-only.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Diagnose the exact frontend root cause. The thread narrowed it to two candidates:
      (A) Granularity mismatch: if the page fetch uses monthly/annual instead of quarterly,
      the JSON would have m1/m2/m3 or y1/y2/y3 keys, but DistributionTab is hardcoded to
      q1/q2/q3. The default state is quarterly (AdvisorIntelligence.tsx:79), so this would
      only regress if user toggles granularity while on the Distribution tab.
      (B) Some other runtime issue: stale React Query cache, prop threading, or a race
      condition in how analyticsData is populated. The code path appears correct from static
      analysis (hasTimeMachine checks current.donut, strip renders per-period buttons).
      Use browser DevTools (network tab, React DevTools) to inspect the actual runtime data.
    </requirement>
    <requirement id="2">
      Fix the root cause. If it is a granularity mismatch, ensure DistributionTab either
      (a) always uses the quarterly file for the Snapshot view strip, OR (b) adapts its
      period keys to match the active granularity (q1/q2/q3 for quarterly, m1/m2/m3 for
      monthly, y1/y2/y3 for annual). Option (b) is the more robust fix.
    </requirement>
    <requirement id="3">
      After fix: confirm the time machine strip renders with 4 periods (current + 3 historical)
      in both GEO and ADV cohorts, for both AUA and NNA metrics.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Distribution tab, Snapshot mode shows quarter strip with 4 periods when
    granularity is set to quarterly (default)</criterion>
    <criterion id="2">If granularity toggle exists on Distribution tab, switching between
    monthly/quarterly/annual correctly updates the period strip labels and data</criterion>
    <criterion id="3">No TypeScript errors (bunx tsc -b passes)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Backend (script 09, bd-portal-publisher) must NOT be modified. S3 data is correct.</constraint>
    <constraint>Do not remove the granularity toggle from the page if it exists -- fix the frontend to handle all granularities.</constraint>
    <constraint>Coordinate with 0.4.2_RD_AdvisorIntelligence if the fix involves visual changes to the strip component.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_SNPLBK.001.snapshot-strip-visual-fix" status="pending"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Fix commit on portal DEV branch restoring time machine strip functionality</deliverable>
    <deliverable type="document">Session log documenting root cause and fix</deliverable>
  </deliverables>
</task_order>
