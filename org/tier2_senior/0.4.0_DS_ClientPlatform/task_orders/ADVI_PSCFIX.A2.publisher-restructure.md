# Task Order: ADVI_PSCFIX A2 — Publisher Restructure

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-a2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
  </metadata>

  <objective>
    Restructure the bd-portal-publisher Lambda to (1) replace the rolling-12M
    NMNC/NMEC classification with a static period-bound definition, (2) output
    pre-aggregated period-level AUA data at three granularities (quarterly,
    monthly, annually) instead of a daily time series, and (3) apply certified_aua
    overrides to all total_aua fields across publisher outputs when
    gold/aua_certification/{today}.json is present.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/bd_pipeline/bd-portal-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      NMNC/NMEC STATIC DEFINITION — replace rolling-12M classification entirely.

      For each granularity (quarterly, monthly, annually), compute completed
      periods plus the current in-progress period:

        period_df = client_performance[date == period_end]  # snapshot at period end
        joined_this_period = client_dim[
            (first_seen_date >= period_start) AND (first_seen_date <= period_end)
        ]
        NMNC = sum(total_aua) for relationship_ids in joined_this_period
        NMEC = sum(total_aua) for all other relationship_ids
        assert abs((NMNC + NMEC) - period_df.total_aua.sum()) < 1.0  # float precision

      Period_end for the current in-progress period = client_performance.date.max().

      Period boundaries:
        Quarterly: Q1 = Jan 1 - Mar 31, Q2 = Apr 1 - Jun 30, Q3 = Jul 1 - Sep 30,
                   Q4 = Oct 1 - Dec 31
        Monthly: calendar month start/end
        Annually: Jan 1 - Dec 31

      Window: emit all periods from the earliest available first_seen_date through
      current. Frontend applies its own time-window filter (1Y/3Y/Max) on top.
    </requirement>

    <requirement id="2">
      OUTPUT SHAPE — new timeseries_chart.json aua key:

      "aua": {
        "quarterly": {
          "categories": ["NMNC", "NMEC"],
          "data": [
            {"period": "2023-Q3", "label": "Q3 '23", "end_date": "2023-09-30",
             "NMNC": 14200000, "NMEC": 989000000},
            ...
            {"period": "2026-Q1", "label": "Q1 '26", "end_date": "2026-03-11",
             "NMNC": 12000000, "NMEC": 1587225407}
          ]
        },
        "monthly": {
          "categories": ["NMNC", "NMEC"],
          "data": [
            {"period": "2024-01", "label": "Jan '24", "end_date": "2024-01-31",
             "NMNC": ..., "NMEC": ...},
            ...
          ]
        },
        "annually": {
          "categories": ["NMNC", "NMEC"],
          "data": [
            {"period": "2022", "label": "2022", "end_date": "2022-12-31",
             "NMNC": ..., "NMEC": ...},
            ...
          ]
        }
      }

      The old "aua.data" daily array is REMOVED. The old "aua.categories" top-level
      key is REMOVED. DE is updating the portal to consume this new shape.
    </requirement>

    <requirement id="3">
      CERTIFIED AUA OVERRIDE — load certification JSON once at Lambda start:

        cert = _load_aua_certification(today)  # returns None if absent

      _load_aua_certification(today):
        key = f"gold/aua_certification/{today}.json"
        try: load from S3, return parsed dict
        except: return None  # non-blocking

      When cert is present, apply to timeseries_chart.json aua series:
        For each granularity, for the LAST entry in data (current period):
          gold_total = last['NMNC'] + last['NMEC']
          scale = cert['certified_aua'] / gold_total
          last['NMNC'] = round(last['NMNC'] * scale, 2)
          last['NMEC'] = round(last['NMEC'] * scale, 2)
        (Same scale applied to all three granularities independently)

      Apply certified_aua override (simple field replacement, no scaling) to:
        - summary/header_metrics.json -> total_aua = cert['certified_aua']
        - snapshots/aua_by_architect.json -> total_aua = cert['certified_aua']
        - snapshots/aua_by_state.json -> total_aua = cert['certified_aua']
        - snapshots/aua_by_tax_status.json -> total_aua = cert['certified_aua']
        - snapshots/aua_by_region.json -> total_aua = cert['certified_aua']
        For each snapshot, optionally recompute aua_pct per row:
          row['aua_pct'] = round(row['aua'] / cert['certified_aua'] * 100, 1)

      Also apply to script 09 (partner_analytics/header_metrics_{gran}.json):
        views.aua.current.donut.total = cert['certified_aua']
        views.geo.current.donut.total = cert['certified_aua']
        views.adv.current.donut.total = cert['certified_aua']
        Only the current period is overridden. Historical periods untouched.
    </requirement>

    <requirement id="4">
      WHAT DOES NOT CHANGE:
        - NNA view aggregation (aggregatedNnaData) — daily cumulative, untouched
        - GEO and ADV views — untouched
        - All historical period values — certification override applies to current
          period only
        - NNA values (nna_ytd, nmnc_ytd, nmec_ytd) in summary/header_metrics.json
          — these are flow metrics, not AUA balances; untouched
        - Segment-level AUA values in snapshot rows — untouched (only total_aua)
        - 02_build_positions_cube.py — untouched
        - gold/client_performance.parquet — untouched

      Preserve the rolling/gradient NMNC concept as a code comment in the publisher.
      It must NOT be rendered in any v1 portal view. Keep the comment so future
      developers understand the two-definition system.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      timeseries_chart.json aua key contains quarterly/monthly/annually sub-keys,
      each with categories array and data array of period-level entries.
      The old flat aua.data daily array is absent.
    </criterion>
    <criterion id="2">
      Static classification verified: a client with first_seen_date = 2025-11-15
      appears as NMNC in the Q4'25 quarterly bar and NMEC in Q1'26.
      Under the old rolling implementation, they would appear NMNC in both.
    </criterion>
    <criterion id="3">
      NMNC + NMEC == total_aua on every bar across all granularities
      (within float rounding). No stacking gaps.
    </criterion>
    <criterion id="4">
      When gold/aua_certification/{today}.json is present:
        - summary/header_metrics.json total_aua == certified_aua
        - Each aua_by_{dim}.json total_aua == certified_aua
        - current-period NMNC + NMEC in timeseries_chart.json aua ==
          certified_aua (after scale application)
    </criterion>
    <criterion id="5">
      When gold/aua_certification/{today}.json is absent:
        - Publisher completes normally, outputs gold-derived totals
        - No error thrown, no disruption
    </criterion>
    <criterion id="6">
      DT can deploy this Lambda. Deliver the commit and notify
      [0.4.0_DT_ClientPlatform] that publisher is ready for deployment.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Rolling NMNC definition must NOT be rendered in any v1 portal view.
    Preserve it as a code comment only.</constraint>
    <constraint>Certification override is non-blocking. All error paths return None;
    publisher falls back to gold totals.</constraint>
    <constraint>No emojis in code, logs, or print statements.</constraint>
    <constraint>Standard Lambda deployment via Terraform — do not deploy yourself.
    Deliver the commit and notify DT.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_PSCFIX.A1.aua-certification-script.md"
                status="pending"
                note="05d must be deployed and producing gold/aua_certification/ JSONs
                before the override logic can be end-to-end tested. DS can implement
                and unit-test the override logic before A1 is deployed by loading
                a manually placed certification JSON from S3 for testing."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-portal-publisher lambda_function.py — static NMNC/NMEC + restructured aua output + certified_aua overrides</deliverable>
    <deliverable type="handoff">Notify 0.4.0_DT_ClientPlatform that publisher is ready for deployment</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md — Deliverables 1, 2, 3</ref>
  </references>
</task_order>
```
