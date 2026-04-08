# ADVI_REBORN.W5-001 -- DS: Fix NNA Cumulative vs Daily Mismatch

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-08-reborn-w5-001-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <objective>Fix NNA data in timeseries_chart.json to be cumulative, not daily. The frontend diffs adjacent period endpoints to compute period-level flows -- this only works with cumulative data.</objective>

  <root_cause>
  D_00.portal_aggregates.py outputs DAILY flow values:
    - Line 1123: NNA = daily_inflow - daily_outflow (one day's flow)
    - Line 1124: Inflows = daily_inflow (one day's inflow)

  Frontend (PartnerAnalytics.tsx lines 312-314 and DistributionTab.tsx lines 620-628)
  takes the LAST data point per period and diffs adjacent endpoints:
    periodNet = lastDayNNA_thisQuarter - lastDayNNA_prevQuarter

  This produces near-zero or nonsensical results because it's diffing two random
  daily values instead of computing total period flows.

  Same bug in nna_geo and nna_adv data built by _nna_drill_data() (D_00 lines 1442-1462):
  outputs daily nna_txn/daily_inflow/daily_outflow per category, frontend diffs endpoints.

  Why Snapshot works: header_metrics uses cumulative values correctly
  (D_00 line 1685: cum_inflows_end - cum_inflows_start).

  Affected views:
    - Assets Overview NNA panel (PartnerAnalytics.tsx)
    - ADV Continuous NNA (DistributionTab.tsx ContinuousNnaDivergingView)
    - GEO Continuous NNA (DistributionTab.tsx ContinuousNnaDivergingView)
  </root_cause>

  <deliverables>
  1. Fix D_00 NNA view (lines 1120-1128): output cumulative running sums instead of daily values
     - NNA = cumsum(daily_inflow - daily_outflow)
     - Inflows = cumsum(daily_inflow)
     - Outflows = cumsum(daily_outflow)

  2. Fix _nna_drill_data() (lines 1442-1462): output cumulative running sums per category
     - point[cat] = cumulative nna_txn for that category
     - point[f'{cat}_inflow'] = cumulative daily_inflow for that category
     - point[f'{cat}_outflow'] = cumulative daily_outflow for that category

  3. Verify Snapshot (header_metrics) is unaffected by this change

  4. After fix: coordinate with AE for gold re-run to regenerate timeseries_chart.json
  </deliverables>

  <dependencies>None -- root cause identified. AE gold re-run needed after fix.</dependencies>
</task_order>
