This is a Pattern 0 pre-implementation alignment thread for Stream A3 of the AdvisorIntelligence completion PRD.

Stream A3: The Advisors tab currently shows rolling NNA with 30d/90d/1Y window toggles as line charts. This is being replaced with two views:
  (1) Stacked bar chart: one bar per advisor showing inflows, outflows, NNA net — sorted by NNA — for period aggregations (QTD/YTD/1Y/3Y/Max).
  (2) 1-year rolling line chart: daily 1Y trailing NNA per advisor, x-axis window controlled by period toggle (3Y/Max supported).

Script 10 currently produces trailing rolling NNA at 30d/90d/1Y windows. It needs to be updated or supplemented to produce period-anchored aggregations and extended rolling series.

Knowledge source: 0.4.0_DS_ClientPlatform (what script 10 currently computes, what nna_aua_by_advisor.parquet contains, what period-anchored aggregations are feasible).
Interface specifier: 0.4.0_DE_ClientPlatform (TypeScript shape needed for both views).
Layout specifier: 0.4.2_RD_AdvisorIntelligence (chart implementation constraints — Recharts vs Nivo, how negative outflows should be encoded in the bar data, what fields the tooltip needs).

Deliverable: agreed JSON output schema for advisor_rolling_flows.json replacement/additions, agreed TypeScript interface names, agreed encoding for negative outflow values in the bar chart data. The final turn must contain this as a structured contract.
