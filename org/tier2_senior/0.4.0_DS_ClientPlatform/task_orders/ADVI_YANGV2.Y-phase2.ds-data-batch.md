# Task Order: Yang V2 Phase 2 DS Data Batch — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI_YANGV2.Y-phase2.ds-data-batch</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <completed>2026-03-05 — deployed bd-v2.16.2 (Lambda) + bd-v2.16.3 (EC2)</completed>
    <priority>HIGH — run parallel with RD Phase 1</priority>
    <streams>Y2, Y3, Y5, Y6b, Y6c, Y6d, Y7, Y9, Y10, Y11, Y13</streams>
  </metadata>

  <objective>
    Execute the full DS data batch for Yang V2. This covers all DS-owned streams from
    the V2 PRD: bug fixes, definition audits, data extensions, and field investigations.
    These streams are organized in delivery priority order. Bugs and investigations
    are highest priority (they are blocking or may change scope). Data extensions
    are second priority (they gate Phase 3 FE task orders).

    DT deploys after DS commits each batch. DS does NOT handle deployment — write code,
    commit, flag to DT when a deploy batch is ready.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md</ref>
    <ref type="prd-v1">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="data_contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
    <ref type="script09">data/black_diamond/scripts/gold/09_build_partner_analytics.py</ref>
    <ref type="script10">data/black_diamond/scripts/gold/10_build_advisor_rolling_flows.py</ref>
    <ref type="publisher">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</ref>
    <ref type="holdings">data/black_diamond/scripts/gold/03_build_holdings_lots.py</ref>
    <ref type="client_dim">data/black_diamond/scripts/gold/04_build_client_dimension.py</ref>
  </references>

  <priority_order>
    Deliver in this order to maximize unblocking downstream agents:

    PRIORITY 1 — Bug Fixes (deliver first, independent, no downstream gate):
      Y7  — Snapshot ADV-AUA single-account binning bug (script 09)
      Y10 — QTD/YTD math bug (script 10)
      Y6c — Outflows quartile inversion fix (script 09, ALL 4 grain levels)

    PRIORITY 2 — Investigations (run parallel with Priority 1, deliver findings early):
      Y2  — AUA NMNC/NMEC period-bookended definition audit (script 09)
      Y11 — Advisor field investigation (gold layer + accounts_dimension_latest)

    PRIORITY 3 — Data Extensions (deliver after Priority 1+2, gate Phase 3 FE):
      Y3  — Asset class AUA breakdown (holdings_lots + security classification)
      Y5  — Growth decomposition time series (AUA start/end + NNA accounting identity)
      Y6b — City-level NNA distribution histograms (script 09, GEO-NNA drill-down)
      Y6d — Relationship-level NNA distribution histograms (script 09, ADV-NNA drill-down)
      Y9  — Continuous NNA inflow/outflow availability at drill levels (timeseries_chart.json)
      Y13 — Rolling Flows NNA bar format monthly data (script 10) [GATES ON Y11]
  </priority_order>

  <requirements>

    <!-- ============================================================== -->
    <!-- PRIORITY 1 — BUG FIXES                                         -->
    <!-- ============================================================== -->

    <requirement id="Y7">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      (or publisher Lambda if binning is done post-script)

      BUG: Single-account relationships (e.g., "McGauley Kevin and Kelly") show 0 accounts
      on hover across all ADV-AUA histogram buckets, and x-ticks display "5m-5m"
      (degenerate range). This is a binning edge case.

      Investigate:
        1. When a relationship has exactly one account/data point, the bin edges may collapse
           to a single value, producing a degenerate "5m-5m" range.
        2. The count for the relationship may be zero or may be placed outside all bins.
        3. The relationship's AUA may sit exactly on a bin edge with off-by-one behavior.

      Fix: Ensure single-account relationships are placed in exactly one bin with a
      non-degenerate range. Options:
        - If bin edges are computed from the data (np.histogram or pd.cut), add a guard
          for the edge case where all values are identical (add epsilon to the range).
        - If bin counts are off-by-one at edges, use `include_lowest=True` (pd.cut) or
          equivalent.
      Verify the fix by constructing a test case with a known single-value input.

      Document the root cause and fix in data_contract.xml.
    </requirement>

    <requirement id="Y10">
      Script: data/black_diamond/scripts/gold/10_build_advisor_rolling_flows.py
      (or publisher Lambda)

      BUG: As of 2026-03-04, QTD and YTD should show identical numbers (Q1 2026 started
      January 1 — QTD start = YTD start). They currently differ.

      Investigate the period boundary calculation:
        - QTD start for Q1 2026 = January 1, 2026
        - YTD start = January 1, 2026
        - These are the same date for Q1. If they differ in the script, there is a
          calendar quarter boundary bug.

      Common causes:
        - Quarter start date lookup uses wrong month boundaries (off by one quarter)
        - YTD uses a different period_start than QTD for the same observation date
        - Data filtering applies inconsistent date windows for QTD vs YTD

      Fix and document corrected period boundary logic in data_contract.xml.
    </requirement>

    <requirement id="Y6c">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py

      BUG: Outflows distribution ranking is backwards. Relationships with the largest
      outflows (most negative NNA) should rank as TOP quartile (P90+), not bottom quartile.
      The current logic likely sorts by signed NNA, placing the most negative values at P10.

      Fix: When computing percentile thresholds for the outflow side of NNA distributions,
      sort by absolute magnitude (abs(nna)) so that the largest outflows are P90+. This
      must be applied at ALL FOUR grain levels:
        1. GEO state-level NNA distribution (Snapshot GEO-NNA)
        2. GEO city-level NNA distribution (Snapshot GEO-NNA drill-down — new in Y6b)
        3. ADV architect-level NNA distribution (Snapshot ADV-NNA)
        4. ADV relationship-level NNA distribution (Snapshot ADV-NNA drill-down — new in Y6d)

      The fix at levels 2 and 4 must be built into the Y6b/Y6d data extensions when
      those run. Document the corrected quartile logic in data_contract.xml.

      Note: levels 1 and 3 exist now — fix these immediately. Levels 2 and 4 are part of
      the Y6b/Y6d extensions — apply the same fix there when writing those.
    </requirement>

    <!-- ============================================================== -->
    <!-- PRIORITY 2 — INVESTIGATIONS                                     -->
    <!-- ============================================================== -->

    <requirement id="Y2">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      (or publisher Lambda)

      Audit the NMNC/NMEC classification for AUA stacked bar. Yang requires "new client"
      to mean: a client whose relationship first_seen_date falls within the bounded display
      interval (month/quarter/year). No rolling window. No smoothed logic. Strictly
      period-bookended.

      Current state: script 09 uses cdim.first_seen_date with a trailing-12-month rule
      for NMNC/NMEC. This must be verified or corrected.

      Investigation steps:
        1. Read the NMNC/NMEC classification logic in script 09 (or publisher Lambda).
        2. Determine whether classification is computed once at data build time (static
           NMNC flag per relationship) or recomputed per display interval.
        3. If static: the classification cannot vary by period, which means it is correct
           only if the flag means "new as of the period where they first appear." Verify.
        4. If period-recomputed: confirm whether the window used is a trailing rolling
           window or a strict period boundary.

      If the current logic does NOT implement period-bookended NMNC:
        Patch to classify a relationship as NMNC for period P if and only if
        first_seen_date >= period_start(P) AND first_seen_date <= period_end(P).

      If it already implements period-bookended correctly:
        Document the verification result in data_contract.xml. No patch needed.

      Either way: document the authoritative NMNC/NMEC definition in data_contract.xml.
    </requirement>

    <requirement id="Y11">
      Investigation: Does an "Advisor" identity field exist in the gold layer, distinct
      from Architect and Implementor?

      Check the following sources:
        1. accounts_dimension_latest.parquet columns — is there an advisor_name,
           advisor_id, or similar field beyond arch_name/impl_name?
        2. rel_architect_lookup.parquet — does it contain advisor entries?
        3. Any BD raw data files that map advisor names or roles
           (data/black_diamond/ raw or staging parquets)
        4. infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py
           — what advisor-type fields are currently used?

      Document findings precisely in your session log:
        - If the field EXISTS: name the exact column name, source file, and confirm whether
          it can be used as a third category alongside Architect/Implementor.
        - If the field DOES NOT EXIST: document what is missing and whether it can be
          sourced from BD raw data.

      Y11 result directly gates Y13:
        - If Advisor field EXISTS: Y13 must extend rolling flows data to include advisors.
        - If Advisor field DOES NOT EXIST: Y13 proceeds with only Architects/Implementors
          (monthly granularity extension still needed). Notify COO.
    </requirement>

    <!-- ============================================================== -->
    <!-- PRIORITY 3 — DATA EXTENSIONS                                    -->
    <!-- ============================================================== -->

    <requirement id="Y3">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      or publisher Lambda: infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py

      Produce an asset-class breakdown of AUA per period interval (month/quarter/year).
      Source: holdings_lots.parquet joined to ETF/security classification
      (DynamoDB etf-classifications table or security_master, per existing script 03 or 09 patterns).

      Asset classes: Equities, Fixed Income, Real Estate, Alternatives, Cash, Other.

      Output shape (append to existing timeseries_chart.json AUA view OR add as aua_mix
      sub-view — determine the cleanest extension and document in data_contract.xml):

        views.aua_mix (or timeseries_chart.json aua.mix):
          data: [
            {
              period: "2024-01",
              segments: [
                { label: "Equities",      value: 12345678.90 },
                { label: "Fixed Income",  value:  5678901.23 },
                { label: "Real Estate",   value:  1234567.89 },
                { label: "Alternatives",  value:   987654.32 },
                { label: "Cash",          value:  2345678.90 },
                { label: "Other",         value:   123456.78 }
              ]
            },
            ...
          ]

      Three granularities: monthly, quarterly, yearly (same pattern as existing AUA data).
      Update data_contract.xml with the chosen output location and field spec.

      Note: AUA Mode A label ("Clients" / "Tenure" / "Client Type") decision is pending
      from Andrew/Yang. DS does not need to wait for this — label is a frontend concern.
      Mode B label is confirmed as "Mix".

      This output gates Y3-FE (RD asset mix toggle frontend).
    </requirement>

    <requirement id="Y5">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      or publisher Lambda

      Produce a growth decomposition time series using the accounting identity:
        market(period) = aua_end(period) - aua_start(period) - nna_net(period)
        total(period) = market(period) + nna_net(period)

      Where:
        - aua_end(period) and aua_start(period) are the period-boundary AUA values
          (already available if AUA timeseries is present)
        - nna_net(period) is already computed in the existing NNA timeseries

      Output shape (new field in timeseries_chart.json or header_metrics.json —
      DS determines cleanest placement):

        growth_decomposition.data: [
          { period: "2024-01", market: 1234567, nna: 567890, total: 1802457 },
          { period: "2024-02", market: -234567, nna: 345678, total:  111111 },
          ...
        ]

      Where total = market + nna and market = aua_end - aua_start - nna.
      Monthly granularity required (frontend aggregates to quarter/year from monthly points).
      Update data_contract.xml with output location and field spec.

      This output gates Y5-FE (RD GRO mode frontend — new toggle + 3-line chart).
    </requirement>

    <requirement id="Y6b">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      or publisher Lambda

      Extend the Snapshot GEO-NNA output to include per-state city-level NNA distribution
      histograms. Currently the snapshot distribution shows only state-level buckets.

      Investigation first: confirm whether city-level NNA data per state already exists
      in header_metrics.json (e.g., as a nested geo_drill structure). If it exists,
      confirm it contains distribution histograms (not just per-city NNA values).
      If not, produce them.

      Output shape (per-state city-level distribution):

        views.nna.geo.drill: {
          [stateKey]: {
            distribution: {
              segments: [ { label: "Austin, TX", range_start: ..., range_end: ..., count: ... }, ... ],
              percentiles: { p25: ..., p50: ..., p75: ..., p90: ... }
            }
          }
        }

      Apply the Y6c outflows quartile inversion fix to city-level distributions:
      outflows ranked by absolute magnitude (largest outflows = P90+).

      Update data_contract.xml.
      This output gates Y6b-FE (RD city drill-down UI for Snapshot GEO-NNA).
    </requirement>

    <requirement id="Y6d">
      Script: data/black_diamond/scripts/gold/09_build_partner_analytics.py
      or publisher Lambda

      Extend the Snapshot ADV-NNA output to include per-architect relationship-level NNA
      distribution histograms. Currently the snapshot shows only architect-level buckets.

      Output shape (per-architect relationship-level distribution):

        views.nna.adv.drill: {
          [architectKey]: {
            distribution: {
              segments: [ { label: "Smith Family Trust", range_start: ..., range_end: ..., count: ... }, ... ],
              percentiles: { p25: ..., p50: ..., p75: ..., p90: ... }
            }
          }
        }

      Apply the Y6c outflows quartile inversion fix here too: relationship-level outflow
      distributions must rank by absolute magnitude.

      Update data_contract.xml.
      This output gates Y6d-FE (RD relationship drill-down UI for Snapshot ADV-NNA).
    </requirement>

    <requirement id="Y9">
      File: infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py
      (timeseries_chart.json output)

      The Continuous NNA GEO and ADV views currently render series data. Yang requires
      a diverging bar format (inflow above / outflow below) at all drill-down levels,
      not just the top level.

      Audit step first:
        Inspect timeseries_chart.json (from S3 or a cached copy) to confirm whether the
        following views include separate inflow and outflow fields alongside nna_net:
          - views.geo (state-level): does each data point have inflow AND outflow?
          - views.geo_drill[stateKey] (city-level): same question
          - views.adv (architect-level): same question
          - views.adv_drill[architectKey] (client/relationship-level): same question

      If inflow + outflow are ALREADY present at all levels: no data change needed.
      Document findings and notify COO. RD can proceed with Y9-FE directly.

      If inflow + outflow are MISSING at any drill level: extend the publisher Lambda
      to produce inflow and outflow alongside nna_net for those views. The output shape
      per data point is:
        { period: "...", inflow: 1234567, outflow: 987654, nna_net: 246913 }

      Note: the relationship-level view is a special case per PRD Section 2.6 —
      at relationship grain, the chart simplifies to a single green/pink bar (positive/
      negative NNA), no inflow/outflow decomposition. So relationship-level (adv_drill)
      does NOT need the inflow/outflow split even if other levels do.

      Update data_contract.xml with findings and any changes.
      This output gates Y9-FE (RD diverging bar at drill levels for Continuous NNA).
    </requirement>

    <requirement id="Y13">
      Script: data/black_diamond/scripts/gold/10_build_advisor_rolling_flows.py

      DEPENDENCY: Complete Y11 first. Y13 behavior changes based on Y11 result:
        - If Advisor field EXISTS: extend stacked_bar to include advisors key alongside
          architects and implementors.
        - If Advisor field DOES NOT EXIST: proceed with architects and implementors only.

      Current state of advisor_rolling_flows.json stacked_bar:
        stacked_bar.architects[period]: AdvisorBarEntry[]
        stacked_bar.implementors[period]: AdvisorBarEntry[]
        Period keys: qtd / ytd / 1y / 3y / max

      Required change 1 — Monthly granularity:
        Add monthly period keys to stacked_bar. The interval keys for the new NNA bar
        format (Y13-FE) need monthly data points. Add:
          stacked_bar.architects.monthly: AdvisorBarEntry[] (all periods monthly)
          stacked_bar.implementors.monthly: AdvisorBarEntry[] (same)
        OR restructure the output so monthly data is a separate key that the frontend
        can use for Month/Quarter/Year interval toggle. DS determines cleanest approach.

      Required change 2 — Advisor type (if Y11 confirmed):
        If Advisor field exists: add stacked_bar.advisors[period] following the same
        AdvisorBarEntry shape as architects and implementors.

      Update data_contract.xml with the new key structure.
      This output gates Y13-FE (RD rolling flows NNA bar with interval/advisorType toggle).
    </requirement>

  </requirements>

  <delivery_batching>
    Batch commits and DT deploy notifications by priority group:

    BATCH 1 (Priority 1 bugs): Y7 + Y10 + Y6c (levels 1+3)
      Commit: script 09 binning fix + script 10 QTD/YTD fix + quartile inversion fix
      Notify DT: "Ready for bd-pipeline deploy batch 1 (Y7/Y10/Y6c)"

    BATCH 2 (Priority 2 investigations): Y2 + Y11
      If Y2 requires a patch: include in a commit. If audit-only: session log only, no commit.
      If Y11 finds advisor field: note it, no commit needed yet (Y13 will consume it).
      Notify COO of Y11 result immediately (gates Y13 scope).

    BATCH 3 (Priority 3 data extensions): Y3 + Y5 + Y6b + Y6d + Y9
      Commit: new data views in script 09 and/or publisher Lambda
      Notify DT: "Ready for bd-pipeline deploy batch 3 (Y3/Y5/Y6b/Y6d/Y9)"
      COO will schedule Pattern 0 alignment threads for each FE stream after DT deploys.

    BATCH 4 (Y13 — after Y11 complete): rolling flows monthly + advisor type
      Commit: script 10 changes
      Notify DT: "Ready for bd-pipeline deploy batch 4 (Y13)"
      COO will schedule Pattern 0 alignment thread for Y13-FE after DT deploys.
  </delivery_batching>

  <acceptance_criteria>
    <criterion id="Y7">Single-account relationships appear in exactly one non-degenerate ADV-AUA histogram bin.</criterion>
    <criterion id="Y10">QTD and YTD values are identical for Q1 (January 1 start date).</criterion>
    <criterion id="Y6c">Outflow distributions at GEO state and ADV architect levels rank by absolute magnitude (largest outflows = P90+).</criterion>
    <criterion id="Y2">NMNC/NMEC classification confirmed as period-bookended (or patched to be so). Authoritative definition in data_contract.xml.</criterion>
    <criterion id="Y11">Advisor field investigation result documented in session log. COO notified of Y11 outcome.</criterion>
    <criterion id="Y3">Asset-class AUA breakdown present in timeseries_chart.json or header_metrics.json at month/quarter/year granularity.</criterion>
    <criterion id="Y5">Growth decomposition time series (market/nna/total) present in output JSON at monthly granularity.</criterion>
    <criterion id="Y6b">Per-state city-level NNA distribution histograms present. Y6c quartile fix applied.</criterion>
    <criterion id="Y6d">Per-architect relationship-level NNA distribution histograms present. Y6c quartile fix applied.</criterion>
    <criterion id="Y9">inflow + outflow availability confirmed (or added) at all drill levels except adv_drill (relationship). Findings in data_contract.xml.</criterion>
    <criterion id="Y13">stacked_bar includes monthly granularity. advisors key added if Y11 confirmed field exists.</criterion>
    <criterion id="all">data_contract.xml updated for each stream. All changes committed before notifying DT.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start Y13 until Y11 investigation is complete.</constraint>
    <constraint>Apply Y6c outflow quartile fix to Y6b and Y6d new distributions as they are written.</constraint>
    <constraint>Do NOT populate opal-partner-49financial or modify opal-users-v2 — those are DT/AE territory (J2/J3 chain).</constraint>
    <constraint>Do NOT remove rolling_1y key from script 10 output until COO confirms no other consumer. Y12 removes the RD UI only — data removal is a separate decision. Flag to COO before removing.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>Follow CLAUDE.md deployment rules: commit code before DT deploys. DS does not terraform apply.</constraint>
  </constraints>

  <what_this_unlocks>
    Y3 deploy -> Pattern 0 thread -> Y3-FE task order (RD)
    Y5 deploy -> Pattern 0 thread -> Y5-FE task order (RD)
    Y6b deploy -> Pattern 0 thread -> Y6b-FE task order (RD)
    Y6d deploy -> Pattern 0 thread -> Y6d-FE task order (RD)
    Y9 deploy (if data gap) -> Pattern 0 thread -> Y9-FE task order (RD)
    Y13 deploy -> Pattern 0 thread -> Y13-FE task order (RD)

    COO will schedule the Pattern 0 threads after DT confirms each deploy batch.
    Phase 3 FE task orders are NOT issued until threads complete.
  </what_this_unlocks>

  <deliverables>
    <deliverable type="commit">script 09 patches: Y7 binning fix, Y6c quartile inversion fix, Y6b city drill-down data, Y6d relationship drill-down data</deliverable>
    <deliverable type="commit">script 10 patches: Y10 QTD/YTD fix, Y13 monthly granularity + advisor type</deliverable>
    <deliverable type="commit">publisher Lambda patches (if needed): Y9 inflow/outflow at drill levels, Y3 asset class AUA, Y5 growth decomposition</deliverable>
    <deliverable type="commit">data_contract.xml: all stream findings and output shapes documented</deliverable>
    <deliverable type="document">Session log per batch with Y11 field investigation result and DT notification notes</deliverable>
  </deliverables>

</task_order>
```
