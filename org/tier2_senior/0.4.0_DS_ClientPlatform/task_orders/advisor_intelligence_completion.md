# Task Order: AdvisorIntelligence Data Completion — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-ds-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all data-layer additions required to complete AdvisorIntelligence to v1.0
    shippable state. Covers five parallel data streams (A1-A5) and one blocked stream (E).
    DS work is the critical path — nothing in the DE/RD portal layer can proceed on
    ADV continuous, CLA continuous, or Advisors stacked bar until DS commits and
    updates data_contract.xml.
  </objective>

  <references>
    <ref>docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
    <ref>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</ref>
    <ref>data/black_diamond/scripts/gold/</ref>
  </references>

  <scope>
    <files>
      <!-- Stream A1 -->
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <!-- Stream A2 -->
      <!-- (same publisher file, separate section) -->
      <!-- Stream A3 -->
      <file action="modify">data/black_diamond/scripts/gold/10_build_advisor_rolling_flows.py</file>
      <!-- Stream A4 -->
      <file action="verify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
      <!-- Stream A5 (investigation only, no code change expected unless mapping absent) -->
      <!-- Stream E (audit only until thread completes) -->
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A1 — adv_drill in timeseries_chart.json                   -->
    <!-- ================================================================ -->
    <requirement id="A1.1">
      Add adv_drill to bd-portal-publisher lambda_function.py output.
      Structure mirrors geo_drill exactly:
        adv_drill: Record&lt;architect_key, CumulativeChartView&gt;
      where CumulativeChartView.categories = the architect's top clients (relationships),
      and CumulativeChartView.data = cumulative NNA time series per client.
      Use the same date range and data density as geo_drill.
    </requirement>
    <requirement id="A1.2">
      Limit to the top clients per architect by AUA (same cardinality cap as geo_drill's
      city cap — up to 10 clients per architect). If an architect has fewer than 2 clients,
      omit from adv_drill (not meaningful for a chart series).
    </requirement>
    <requirement id="A1.3">
      Update data_contract.xml to document adv_drill: output shape, S3 key, how architect
      keys map to rel_architect_lookup, and client grain definition.
      Mark data_contract.xml update as complete BEFORE handing to DT for deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries in timeseries_chart.json              -->
    <!-- ================================================================ -->
    <requirement id="A2.1">
      Design and implement cla_timeseries output. This is the highest DS effort item.
      Output structure to add to timeseries_chart.json:
        cla: {
          total: CumulativeChartView          // categories: ['nmnc', 'nmec']
          geo: CumulativeChartView            // categories: top states
          adv: CumulativeChartView            // categories: top architects
          geo_drill: Record&lt;state, CumulativeChartView&gt;  // per-city breakdown
          // no adv_drill for CLA — architect is terminal grain
        }
      CumulativeChartView.data values = NMNC AUM and NMEC AUM (absolute dollars) per date.
    </requirement>
    <requirement id="A2.2">
      Classify each relationship as NMNC (new client, green) or NMEC (existing client, blue)
      using accounts_dimension_latest and/or account open dates + advisor assignment history.
      Confirm classification logic with DE before committing — send DE a quick written
      confirmation of the NMNC/NMEC classification logic and get acknowledgment.
    </requirement>
    <requirement id="A2.3">
      Determine whether cla_timeseries lives in script 09 (EC2 gold layer) or in the
      publisher Lambda. Document the decision in data_contract.xml with rationale.
      Either location is acceptable; the criterion is: does the data require per-row
      gold table access (script 09) or can it be assembled from existing publisher inputs?
    </requirement>
    <requirement id="A2.4">
      Update data_contract.xml with cla_timeseries output shape, S3 key, grain definitions,
      and NMNC/NMEC classification logic.
      Mark update complete BEFORE handing to DT.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A3 — Stacked bar + 1Y rolling data for Advisors tab       -->
    <!-- ================================================================ -->
    <requirement id="A3.1">
      Update script 10 (10_build_advisor_rolling_flows.py) to produce period-anchored
      aggregated inflows/outflows/nna_net per advisor for the stacked bar chart:
        stacked_bar: {
          architects: { qtd: AdvisorBarEntry[], ytd: AdvisorBarEntry[], '1y': AdvisorBarEntry[], '3y': AdvisorBarEntry[], max: AdvisorBarEntry[] }
          implementors: { qtd: AdvisorBarEntry[], ytd: AdvisorBarEntry[], '1y': AdvisorBarEntry[], '3y': AdvisorBarEntry[], max: AdvisorBarEntry[] }
        }
      AdvisorBarEntry = { name: str, inflows: float, outflows: float, nna_net: float }
      Period definitions:
        qtd = sum from start of current calendar quarter to today
        ytd = sum from Jan 1 of current year to today
        1y  = sum from exactly 1 year ago to today
        3y  = sum from exactly 3 years ago to today
        max = inception to today
    </requirement>
    <requirement id="A3.2">
      Produce rolling_1y output: 1-year trailing NNA per advisor as daily time series,
      extended to cover the full 3Y and Max x-axis windows for the secondary line chart:
        rolling_1y: {
          architects: AdvisorRollingSeries[]   // each: { name, data: [{date, value}...] }
          implementors: AdvisorRollingSeries[]
        }
      Rolling window is FIXED at 1 year (each date point = trailing 365 days from that date).
      Date range must cover at least 3 years of history for 3Y view.
    </requirement>
    <requirement id="A3.3">
      Update data_contract.xml with new advisor_rolling_flows.json shape, replacing or
      addending the current contract entry for script 10 output.
      Mark update complete BEFORE handing to DT.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A4 — Bell curve math verification                          -->
    <!-- ================================================================ -->
    <requirement id="A4.1">
      Verify that commit 8247c6d0 correctly implemented |abs| for negative NNA accounts
      in script 09's bell curve percentile threshold calculation.
      Check: open partner_analytics/header_metrics.json from S3 and inspect the
      distribution field for the NNA view's negative (outflow) segment.
      Confirm P10/P25/Median/P75/P90 thresholds are non-degenerate (not all zero,
      not symmetric mirrors of the positive side).
    </requirement>
    <requirement id="A4.2">
      If the fix did NOT land correctly: write a targeted patch to script 09 and
      coordinate with 0.4.0_DT to deploy the EC2 script update.
      If the fix DID land: document the verification result in your session log
      with the specific values observed in header_metrics.json.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A5 — opal-users-v2 advisor identity mapping               -->
    <!-- ================================================================ -->
    <requirement id="A5.1">
      Investigate the schema of the opal-users-v2 DynamoDB table:
        - What fields identify an advisor (e.g., userId, email, advisorId, firmId)?
        - What is the partition key / sort key structure?
      Do NOT modify the table. Read-only investigation.
    </requirement>
    <requirement id="A5.2">
      Determine whether a mapping from opal-users-v2 identity fields to
      accounts_dimension_latest.architect or rel_architect_lookup.parquet already exists.
      Options:
        (a) Direct field match (userId == some gold layer key)
        (b) Email-based lookup (email matches advisor record in gold layer)
        (c) No existing mapping — new data registration step required
      Document findings in your session log. This is the linchpin for Books tab auth gating.
    </requirement>
    <requirement id="A5.3">
      Surface findings to COO and CTO in your session log. If option (c) — flag as
      a blocker for Stream J (firmId auth refactor) and Books tab gating.
      No code change required from this investigation alone.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM E — Books data contract audit (BLOCKED by Stream D)        -->
    <!-- ================================================================ -->
    <requirement id="E.1">
      BLOCKED: Do not begin Stream E until the Books tab design thread (Stream D)
      has completed and you have a thread receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      Stream D thread will establish which L2/L3/L4 fields are needed for the Books tab.
    </requirement>
    <requirement id="E.2">
      After Stream D thread completes: audit bd-portal-advisor-publisher/lambda_function.py
      to determine which L4 fields (holdings lots, cost basis, tax liability) are already
      published vs. absent from clients/{clientKey}.json S3 output.
      Reference scripts: 03_build_holdings_lots.py, 05b_build_account_performance.py,
      06_build_client_tax_liability.py — confirm their outputs flow into the publisher.
    </requirement>
    <requirement id="E.3">
      Produce a written gap list: which L4 fields exist in the gold layer but are not
      currently in the publisher output. Include this in your session log and in
      data_contract.xml as a pending section.
      Update data_contract.xml with the L4 Books contract BEFORE handing to DT for Stream F deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">adv_drill is present in timeseries_chart.json S3 output with correct structure (verified by DT deploy + spot-check).</criterion>
    <criterion id="2">cla_timeseries is present in timeseries_chart.json with nmnc and nmec AUM series at total/geo/adv/geo_drill grains.</criterion>
    <criterion id="3">advisor_rolling_flows.json has stacked_bar (5 periods x 2 role types) and rolling_1y (daily, 3Y+ history).</criterion>
    <criterion id="4">Bell curve verification documented in session log; patch applied and deployed if fix was absent.</criterion>
    <criterion id="5">opal-users-v2 mapping investigation findings documented in session log before Books thread runs.</criterion>
    <criterion id="6">data_contract.xml updated for A1, A2, A3 before each respective DT deploy.</criterion>
    <criterion id="7">Stream E complete: L4 gap list in session log + data_contract.xml updated with Books L4 contract (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT begin Stream E until Stream D thread receipt is in your threads/ folder.</constraint>
    <constraint>data_contract.xml must be updated and committed BEFORE signaling DT to deploy any Lambda change. This is a quality gate.</constraint>
    <constraint>Confirm NMNC/NMEC classification logic with DE in writing before committing cla_timeseries implementation.</constraint>
    <constraint>Do NOT use emojis in any script, Lambda, or log output. Plain ASCII only.</constraint>
    <constraint>Do NOT deploy directly. All EC2 and Lambda deploys go through 0.4.0_DT. Hand off via your session log next steps.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>NOTE: You have no prior session logs. The Books thread (Stream D) cannot run until you have produced at least one session log from your activation. Complete Streams A1-A5 first, write your session log, then the COO will schedule Stream D.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="Stream E blocked until D completes"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="A2 NMNC/NMEC logic requires DE written acknowledgment before commit"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py updated with adv_drill + cla_timeseries</deliverable>
    <deliverable type="commit">10_build_advisor_rolling_flows.py updated with stacked_bar + rolling_1y output</deliverable>
    <deliverable type="document">data_contract.xml updated with A1, A2, A3 shapes before each DT deploy</deliverable>
    <deliverable type="document">Session log with A4 bell curve verification result + A5 opal-users-v2 mapping findings</deliverable>
    <deliverable type="document">data_contract.xml updated with Books L4 contract (post-thread, Stream E)</deliverable>
  </deliverables>
</task_order>
```
