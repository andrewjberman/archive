# Task Order: ADVI_PSCFIX B1 — Portal Schema Update

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-b1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>complete</status>
  </metadata>

  <objective>
    Update PartnerAnalytics.tsx and the CumulativeChartDataPoint type to consume
    the new aua.{granularity}.data shape from timeseries_chart.json. The publisher
    (DS Track A2) is replacing the old daily aua.data flat array with three
    pre-aggregated period series. DE can build and type against mock data immediately;
    full integration test once the publisher Lambda is deployed.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts (or wherever CumulativeChartDataPoint is defined)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      NEW DATA SHAPE — timeseries_chart.json aua key:
      {
        "aua": {
          "quarterly": {
            "categories": ["NMNC", "NMEC"],
            "data": [
              {"period": "2023-Q3", "label": "Q3 '23", "end_date": "2023-09-30",
               "NMNC": 14200000, "NMEC": 989000000},
              ...
            ]
          },
          "monthly": { ... same shape ... },
          "annually": { ... same shape ... }
        }
      }

      The old aua.data daily array and aua.categories top-level key are gone.
      Each data entry has: period (string), label (string), end_date (YYYY-MM-DD),
      NMNC (number), NMEC (number).
    </requirement>

    <requirement id="2">
      TYPE UPDATE — CumulativeChartDataPoint:
      Add fields: period: string, label: string, end_date: string.
      Keep [category: string]: number | string for NMNC/NMEC values.
      Remove any field that assumed a daily "date" key for the AUA series
      (NNA type remains unchanged — NNA is still daily cumulative).
    </requirement>

    <requirement id="3">
      PartnerAnalytics.tsx — replace allSortedAuaPeriods aggregation logic:

      OLD: built a fullPeriodMap from daily data, grouped by period, kept last value.
      NEW: select directly from the correct granularity sub-key:

        const auaGranularity = granularity === 'annually' ? 'annually'
          : granularity === 'monthly' ? 'monthly' : 'quarterly'

        const auaSeriesData = timeseriesData?.aua?.[auaGranularity]?.data ?? []

        // Apply time-window filter using end_date, then pass to chart — no aggregation
        const aggregatedAuaData = auaSeriesData.filter(point =>
          !timeWindowCutoff || new Date(point.end_date + 'T12:00:00') >= timeWindowCutoff
        )

      Eliminate the old fullPeriodMap construction and all groupBy/reduce logic for
      the AUA series. The backend now delivers pre-aggregated data.
    </requirement>

    <requirement id="4">
      WHAT DOES NOT CHANGE:
        - NNA view aggregation (aggregatedNnaData) — NNA remains daily cumulative.
          Do not touch the NNA data path.
        - GEO/ADV views — untouched.
        - Time window filter logic — unchanged in structure; apply to end_date
          instead of date for the AUA series.
        - Granularity toggle UX — unchanged. Toggle still controls which sub-key
          (quarterly/monthly/annually) is selected.
    </requirement>

    <requirement id="5">
      MOCK DATA — start immediately using a local mock that matches the new shape.
      Do not wait for the publisher Lambda to be deployed. The TypeScript interface
      must be complete and bunx tsc -b must pass before the publisher is live.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      bunx tsc -b passes with zero errors after the type update.
    </criterion>
    <criterion id="2">
      AUA chart renders correctly with mock data: granularity toggle switches between
      quarterly/monthly/annually sub-keys. Time window filter applies to end_date.
    </criterion>
    <criterion id="3">
      NNA view is untouched — no regression in NNA chart rendering.
    </criterion>
    <criterion id="4">
      The old fullPeriodMap/groupBy aggregation logic for AUA is removed.
      No dead code left in the component.
    </criterion>
    <criterion id="5">
      After publisher Lambda is deployed (Track A2 + DT): swap mock for live data,
      confirm AUA bars render with correct NMNC/NMEC values at all granularities.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not touch NNA aggregation logic — NNA data path is unchanged.</constraint>
    <constraint>Do not touch GEO or ADV views.</constraint>
    <constraint>TypeScript strict — all new fields fully typed. No any casts for
    the AUA series data unless strictly necessary with a comment explaining why.</constraint>
    <constraint>bunx tsc -b must pass before handing off to DT.</constraint>
    <constraint>No emojis in code or comments.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_PSCFIX.A2.publisher-restructure.md"
                status="pending"
                note="DE can build against mock data immediately. Full integration
                test requires publisher Lambda deployed by DT. Type contract is
                defined in this task order and the PRD — no thread needed."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">PartnerAnalytics.tsx — new aua granularity selection logic, no aggregation</deliverable>
    <deliverable type="commit">types.ts — CumulativeChartDataPoint updated with period/label/end_date fields</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md — Deliverable 4: Frontend Wiring</ref>
  </references>
</task_order>
```
