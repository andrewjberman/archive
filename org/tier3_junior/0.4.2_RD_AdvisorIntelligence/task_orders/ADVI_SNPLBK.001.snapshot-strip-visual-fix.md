<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-snapshot-strip-visual-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_SNPLBK-001</thread_serial>
    <thread_ref>org/threads/ADVI_SNPLBK-001-snapshot-lookback-regression-diagnosis/</thread_ref>
  </metadata>

  <objective>
    Support the DE in fixing the Snapshot Lookback regression. The Distribution tab's
    "time machine" quarter strip (DistributionQuarterlyStrip / NnaQuarterlyStrip) is no
    longer rendering historical periods. Backend data is confirmed intact by COO (S3 JSON
    has current + q1/q2/q3 for all views). The regression is frontend-only.

    Your role: if the DE identifies a granularity mismatch as the root cause (strip
    hardcoded to q1/q2/q3 but fetching monthly/annual data), update the strip components
    to dynamically use the correct period keys based on the active granularity:
    - quarterly: q1, q2, q3
    - monthly: m1, m2, m3
    - annual: y1, y2, y3
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      If DE confirms granularity mismatch: update DistributionQuarterlyStrip and
      NnaQuarterlyStrip to accept a granularity prop and use the correct period keys
      (q1/q2/q3 for quarterly, m1/m2/m3 for monthly, y1/y2/y3 for annual).
      Update TimePeriodKey type to include all period key variants.
    </requirement>
    <requirement id="2">
      If DE identifies a different root cause: implement the visual fix as directed
      by the DE task order. Document what changed.
    </requirement>
    <requirement id="3">
      Period labels in the strip should match the backend periods metadata
      (analyticsData.periods[key].label) with fallback labels appropriate to the
      granularity (e.g., "Last Month" / "2M Ago" for monthly instead of "Last Qtr").
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Time machine strip renders 4 periods in Snapshot mode for all three
    granularities (quarterly, monthly, annual) when the respective backend file exists</criterion>
    <criterion id="2">Strip labels correctly reflect the period type (quarter labels for
    quarterly, month labels for monthly, year labels for annual)</criterion>
    <criterion id="3">No TypeScript errors</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Wait for DE to confirm the root cause before making changes. DE leads this investigation.</constraint>
    <constraint>Do not modify backend code or API endpoints.</constraint>
    <constraint>Maintain existing drill-down functionality (city/client drill) within the strip.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_SNPLBK.001.snapshot-lookback-frontend-fix" status="pending"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit fixing the strip rendering for all granularities</deliverable>
  </deliverables>
</task_order>
