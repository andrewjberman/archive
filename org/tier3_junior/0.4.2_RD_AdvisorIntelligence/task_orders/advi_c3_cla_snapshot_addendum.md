# Task Order Addendum: C3 CLA Snapshot — Data Source + Design Correction

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-04-c3-cla-snapshot-addendum</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <also_applies_to>0.4.0_DE_ClientPlatform, 0.4.0_DS_ClientPlatform</also_applies_to>
    <date>2026-03-04</date>
    <status>active</status>
    <supersedes>advi_c3_cla_snapshot.md (requirements C3.2, C3.3, C3.4 and the data source)</supersedes>
  </metadata>

  <summary>
    The original C3 task order had two errors:

    ERROR 1 — Wrong data source.
      Said: "Data is in header_metrics.json" then C3.1 said check ClaView from PartnerAnalytics.
      Both were wrong as written. ClaSnapshotView must NOT depend on PartnerAnalyticsResponse
      for the redesigned view. Use header_metrics.json directly via getHeaderMetrics() useQuery
      inside ClaSnapshotView. No prop threading. No interpage dependencies.

    ERROR 2 — Wrong content.
      Said: "AUA dollar amounts and percentages" as the proportional basis.
      Correct: the snapshot is a COMPOSITION VIEW — percentage of relationship count (NMNC vs NMEC),
      not AUA. Show what share of the book (by client count) is new clients vs existing clients.
      No NNA vocabulary. No flows data.

    C4 continuous (ADVI-004 task order) is unchanged — stacked area from timeseries_chart.json
    cla.total is correct. This addendum is C3 only.
  </summary>

  <context>
    CLA = Client Lifecycle Analysis. Two views:

    C3 SNAPSHOT (this addendum):
      "What portion of our client book is new clients (NMNC) vs existing (NMEC),
      and how has that mix shifted over the past few quarters?"
      Format: radial donut (proportion) + quarter strip (trend) + distribution histogram
      Data: header_metrics.json — already loaded in this tab via useQuery pattern

    C4 CONTINUOUS (ADVI-004 task order, unchanged):
      "How has the NMNC/NMEC AUA split evolved over time (cumulative timeseries)?"
      Format: stacked area chart — same visual pattern as Assets Overview continuous view
      Data: timeseries_chart.json cla.total (CumulativeChartView — two series: NMNC, NMEC)
  </context>

  <requirements>

    <!-- ================================================================ -->
    <!-- DATA SOURCE — fetch header_metrics.json inside ClaSnapshotView   -->
    <!-- ================================================================ -->
    <requirement id="C3-A.1">
      Remove ClaSnapshotView's dependency on PartnerAnalyticsResponse.views.cla entirely.
      Delete the claViews / periodData / claView reads from analyticsData.

      Add a useQuery inside ClaSnapshotView (same pattern as DistributionTab's getCumulativeChart query):

        import { getHeaderMetrics } from '@/api/endpoints/advisor-intelligence'

        const { data: headerData, isLoading: headerLoading } = useQuery({
          queryKey: ['headerMetrics'],
          queryFn: getHeaderMetrics,
          staleTime: 5 * 60 * 1000,
        })

      All CLA snapshot rendering reads from headerData (HeaderMetricsResponse).
      If headerData is undefined: show the same "CLA data not available" fallback.
    </requirement>

    <!-- ================================================================ -->
    <!-- C3 SNAPSHOT — RADIAL DONUT                                        -->
    <!-- ================================================================ -->
    <requirement id="C3-A.2">
      Replace the existing ClaSnapshotView bar chart (inflows/outflows/NNA bars) with a
      two-segment radial donut — same visual format as the AUA snapshot donut elsewhere
      in DistributionTab.

      Data source: headerData.total
        nmnc_segment: {
          label: "New Clients (NMNC)",
          value: headerData.total.new_client_aua,
          count: headerData.total.new_client_count,
          pct:   headerData.total.new_client_pct,        // already a percentage
          color: "#16A34A"                               // green (consistent with NMNC branding)
        }
        nmec_segment: {
          label: "Existing Clients (NMEC)",
          value: headerData.total.existing_client_aua,
          count: headerData.total.existing_client_count,
          pct:   100 - headerData.total.new_client_pct,  // remainder
          color: "#2563EB"                               // blue (consistent with NMEC branding)
        }

      Donut labels: show percentage + client count (e.g. "32% / 47 clients")
      No NNA. No inflow/outflow. This is a book composition view.

      Note: new_client_aua and existing_client_aua reflect the trailing-12-month
      NMNC/NMEC classification in the current period. That is the correct basis for
      the snapshot view.
    </requirement>

    <!-- ================================================================ -->
    <!-- C3 SNAPSHOT — QUARTER STRIP (trend over time)                    -->
    <!-- ================================================================ -->
    <requirement id="C3-A.3">
      Add a quarter strip below the donut showing how the NMNC/NMEC mix has shifted
      across the last four quarters.

      Data source: headerData.timeseries.data (RollingTimeseriesDataPoint[])
      Quarter end dates: headerData.dates.q0 / q1 / q2 / q3

      For each quarter (q0 = most recent, q3 = oldest):
        1. Find the last data point in timeseries.data where date <= headerData.dates.qN
        2. Read nmnc_pct and nmec_pct from that data point
        3. Render as a mini two-segment bar (green/blue stacked to 100%)
           with the quarter label below (e.g., "Q4 2025")

      If headerData.timeseries is absent (older cached JSON): render the strip
      with only q0 using headerData.total.new_client_pct. Do not error.

      This strip replaces the current period selector on ClaSnapshotView (the
      current/q1/q2/q3 toggle). The strip is read-only; it is not clickable.
    </requirement>

    <!-- ================================================================ -->
    <!-- C3 SNAPSHOT — DISTRIBUTION HISTOGRAM                             -->
    <!-- ================================================================ -->
    <requirement id="C3-A.4">
      Replace the distribution panel (right side of the snapshot layout) with
      a two-series account-size distribution:

      Data source:
        headerData.account_distribution.by_segment.NMNC   (SegmentDistribution)
        headerData.account_distribution.by_segment.NMEC   (SegmentDistribution)

      Each SegmentDistribution has:
        histogram.bins[]       — bin edges (dollar values)
        histogram.counts[]     — count per bin
        histogram.bin_labels[] — formatted labels
        mean, median, percentiles.p10/p25/p50/p75/p90

      Render as two overlapping/adjacent histogram bars — NMNC in green, NMEC in blue.
      Same SnapshotDistributionChart component pattern already in DistributionTab.
      Show median and mean lines for each segment.

      Label panels: "New Client Account Sizes (NMNC)" and "Existing Client Account Sizes (NMEC)"
      No NNA. No flows. These are account size (AUA per relationship) distributions.
    </requirement>

    <!-- ================================================================ -->
    <!-- PROPS CHANGE — update ClaSnapshotViewProps                       -->
    <!-- ================================================================ -->
    <requirement id="C3-A.5">
      Update ClaSnapshotViewProps interface:

        REMOVE:
          analyticsData: PartnerAnalyticsResponse
          selectedPeriod: TimePeriodKey
          onPeriodChange: (period: TimePeriodKey) => void

        KEEP:
          cohort: CohortOption   // still used if geo/adv breakdown is added later;
                                 // for now renders the same data regardless of cohort
                                 // (header_metrics.json has no geo/adv split for NMNC/NMEC)

      Update all ClaSnapshotView call sites (search DistributionTab.tsx for
      <ClaSnapshotView) to remove the removed props.

      If removing selectedPeriod breaks any parent state management: simplify —
      the quarter strip is self-contained inside ClaSnapshotView.
    </requirement>

    <!-- ================================================================ -->
    <!-- TYPE CHECK                                                        -->
    <!-- ================================================================ -->
    <requirement id="C3-A.6">
      Run bunx tsc -b --noEmit after all changes. Must pass clean.
      HeaderMetricsResponse, SegmentDistribution, RollingTimeseriesDataPoint,
      AccountDistributionData are all typed in types.ts. Use them directly.
      Do not invent new types.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">ClaSnapshotView fetches via useQuery(getHeaderMetrics) — no PartnerAnalyticsResponse dependency.</criterion>
    <criterion id="2">Donut shows two segments: NMNC (green) and NMEC (blue) with % and client count labels.</criterion>
    <criterion id="3">Quarter strip shows NMNC/NMEC mix trend across q0-q3 using timeseries data.</criterion>
    <criterion id="4">Distribution shows NMNC vs NMEC account-size histograms from account_distribution.by_segment.</criterion>
    <criterion id="5">No inflow/outflow/NNA values anywhere in the view. Composition vocabulary only.</criterion>
    <criterion id="6">bunx tsc -b --noEmit passes clean.</criterion>
    <criterion id="7">Fallback renders cleanly when headerData is loading or absent.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT use PartnerAnalyticsResponse.views.cla in this view. That data stays for C4 continuous only.</constraint>
    <constraint>Do NOT add headerData as a prop to DistributionTab. Fetch inside ClaSnapshotView via useQuery.</constraint>
    <constraint>cohort toggle (geo/adv) does not change the data in this view — header_metrics.json has no per-cohort NMNC/NMEC split. Keep the prop for future use but do not show different data based on it.</constraint>
    <constraint>No emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- C3 CLA snapshot redesign (header_metrics source)"</constraint>
  </constraints>

  <note_for_ds>
    DS: Verify that header_metrics.json (S3: opal-data-bd/gold/summary/header_metrics.json)
    contains the following fields in the live file:
      - total.new_client_aua
      - total.existing_client_aua
      - total.new_client_count
      - total.existing_client_count
      - total.new_client_pct
      - account_distribution.by_segment.NMNC (histogram present)
      - account_distribution.by_segment.NMEC (histogram present)
      - timeseries.data[].nmnc_pct
      - timeseries.data[].nmec_pct
    If any are missing from the live file, flag to DE and CTO before RD implements.
    Types are already defined in types.ts — this is a data presence check only.
  </note_for_ds>

  <note_for_de>
    DE: After RD commits C3 redesign, review for:
      1. useQuery key consistency — 'headerMetrics' should match any existing key used elsewhere
         for the same endpoint. Check other components that call getHeaderMetrics() to confirm
         the queryKey matches so React Query deduplicates the fetch.
      2. Type correctness: SegmentDistribution extends DistributionStats — confirm histogram
         fields are accessed correctly (histogram.bins, not histogram.data or similar).
      3. timeseries sampling logic — confirm the date comparison is correct for finding
         the last data point before each quarter-end date.
    Signal DT when review is complete.
  </note_for_de>

</task_order>
```
