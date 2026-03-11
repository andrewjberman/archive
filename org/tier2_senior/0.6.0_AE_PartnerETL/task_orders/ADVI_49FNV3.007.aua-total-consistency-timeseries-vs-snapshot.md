<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-11-aua-total-consistency</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
    <project>ADVI_49FNV3</project>
  </metadata>

  <objective>
    Investigate and resolve a ~$10M AUA total discrepancy between two gold files
    published by bd-portal-publisher. The portal displays two different total AUA
    figures for the same period depending on which panel is rendering, because each
    panel reads from a different source file. These must agree.
  </objective>

  <context>
    The Advisor Intelligence portal has two panels that both display "Total AUA":

    1. Assets Overview bar chart (AUA mode — NMNC + NMEC):
       Source: opal-data-bd/gold/timeseries_chart.json
       Field:  aua.data[period].NMNC + aua.data[period].NMEC (summed per period)
       Frontend: PartnerAnalytics.tsx line ~1864, barCategories.reduce(...)

    2. Snapshot / GEO / segment panels:
       Source: opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json
       Field:  views.aua.current.metrics.aua  OR  views.geo.current.metrics.aua
       Frontend: PartnerAnalytics.tsx line ~2426, snapshot.metrics.aua

    For the current quarter, one panel shows $1.60B and the other shows $1.59B.
    The discrepancy is approximately $10M on a ~$1.6B book.

    These two files are published independently by bd-portal-publisher. The gap
    suggests that either:
    a) The two files are computed from different date cutoffs or account sets
    b) One file includes/excludes certain account types the other does not
    c) Rounding or aggregation differences in the publisher scripts
  </context>

  <scope>
    <files>
      <file action="investigate">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="investigate">opal-data-bd/gold/timeseries_chart.json (S3)</file>
      <file action="investigate">opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json (S3)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Pull both S3 files and compare total AUA for the current quarter period.
      Quantify the exact gap: timeseries_chart total AUA vs header_metrics total AUA.
      Confirm which is correct against the source data (Black Diamond / cube).
    </requirement>
    <requirement id="2">
      Trace the computation path in bd-portal-publisher for each figure:
      - Which script/function writes timeseries_chart.json aua.data?
      - Which script/function writes header_metrics_quarterly.json views.aua.current.metrics.aua?
      Identify where they diverge (different filters, different aggregation windows,
      different account exclusions, different rounding).
    </requirement>
    <requirement id="3">
      Fix the root cause so both files produce the same total AUA for the same period.
      If one is definitively correct and one is wrong, fix the wrong one.
      If both have legitimate differences (e.g., one is end-of-period, one is as-of-date),
      document the semantic difference and escalate to DE to surface it correctly in the UI.
    </requirement>
    <requirement id="4">
      After fix, confirm the two totals agree within rounding tolerance ($0 or $1 due to
      integer storage). Deploy updated publisher and re-run gold layer.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      timeseries_chart.json aua.data[current_period] NMNC+NMEC sum equals
      header_metrics_quarterly.json views.aua.current.metrics.aua within $1
    </criterion>
    <criterion id="2">Root cause documented in session log</criterion>
    <criterion id="3">Fix deployed, gold layer re-run, both files refreshed in S3</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change the JSON schema of either file — DE depends on the existing field structure</constraint>
    <constraint>If the fix requires a full pipeline rebuild, coordinate with DE on expected downtime</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">Session log with root cause, gap magnitude, and fix applied</deliverable>
    <deliverable type="deploy">Updated bd-portal-publisher deployed, gold files refreshed</deliverable>
  </deliverables>
</task_order>
