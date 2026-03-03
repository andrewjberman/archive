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
    Implement all data-layer additions for AdvisorIntelligence completion. Streams A1, A2,
    and A3 require Pattern 0 alignment threads to run FIRST — the thread receipts define
    the exact JSON shapes and TypeScript interfaces DS must implement. Do NOT implement
    A1/A2/A3 based on this task order's descriptions alone; the thread receipt is the
    binding specification. Streams A4 and A5 have no interface dependency and start
    immediately. Stream E is blocked by the Books tab design thread (Stream D).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref type="data-contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py</file>
      <file action="verify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A4 — Snapshot NNA bell curve math verification            -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A4.1">
      Verify that commit 8247c6d0 correctly implemented |abs| for negative NNA accounts
      in script 09's bell curve percentile threshold calculation.
      Open partner_analytics/header_metrics.json from S3 and inspect the distribution
      field for the NNA view's outflow segment.
      Confirm P10/P25/Median/P75/P90 thresholds are non-degenerate: not all zero,
      not symmetric mirrors of the positive side.
    </requirement>
    <requirement id="A4.2">
      If the fix did NOT land: write a targeted patch to script 09 and coordinate with
      0.4.0_DT to deploy the EC2 script update.
      If the fix DID land: document the verification result in your session log with
      the specific threshold values observed in header_metrics.json.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A5 — opal-users-v2 advisor identity investigation         -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A5.1">
      Investigate the schema of the opal-users-v2 DynamoDB table (read-only):
        - What fields identify an advisor (userId, email, advisorId, firmId)?
        - What is the partition key / sort key structure?
    </requirement>
    <requirement id="A5.2">
      Determine whether a mapping from opal-users-v2 identity fields to
      accounts_dimension_latest.architect or rel_architect_lookup.parquet already exists:
        (a) Direct field match
        (b) Email-based lookup
        (c) No existing mapping — new data registration step required
      Document findings in your session log. This is the linchpin for Books tab auth gating.
      If option (c): flag as a blocker and surface to COO and CTO before any auth work proceeds.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A1 — adv_drill in timeseries_chart.json                   -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A1.1">
      GATE: Do not implement adv_drill until the Pattern 0 alignment thread
      (2026-03-03-continuous-nna-cla-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt is the binding specification for the adv_drill JSON shape,
      S3 key pattern, cardinality constraints, and date range. Implement exactly what
      was agreed in the thread — not what is described in the PRD or this task order.
    </requirement>
    <requirement id="A1.2">
      In the thread, you are the knowledge source. Describe what per-architect and
      per-client NNA data currently exists in the gold layer. Name specific parquet
      files, column names, and cardinality. Let DE specify the TypeScript interface
      and RD specify the chart constraint — then converge on the exact shape.
    </requirement>
    <requirement id="A1.3">
      After thread completes: implement adv_drill in bd-portal-publisher/lambda_function.py
      per the agreed contract. Update data_contract.xml with the agreed shape, S3 key,
      and grain definitions BEFORE signaling DT to deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries in timeseries_chart.json              -->
    <!-- BLOCKED: run Pattern 0 thread first (same thread as A1)          -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A2.1">
      GATE: Same as A1 — do not implement cla_timeseries until the thread receipt from
      2026-03-03-continuous-nna-cla-alignment is in your threads/ folder.
      The thread defines: NMNC/NMEC classification logic (agreed with DE and RD),
      the exact JSON structure, grain definitions (total/geo/adv/geo_drill),
      and whether implementation lives in script 09 (EC2) or the publisher Lambda.
    </requirement>
    <requirement id="A2.2">
      In the thread, surface what NMNC/NMEC classification data currently exists in
      the gold layer. Do NOT assume the classification. Name the specific field or
      derivation logic and let all three agents agree on the definition in the thread.
      Do not commit any classification logic until DE has confirmed it matches how
      CLA is currently defined in header_metrics.json.
    </requirement>
    <requirement id="A2.3">
      After thread completes: implement cla_timeseries per the agreed contract.
      Update data_contract.xml BEFORE signaling DT to deploy.
      Note: adv_drill and cla_timeseries should deploy together in one publisher update
      (Stream B1) to minimize deploy events.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A3 — Stacked bar + 1Y rolling for Advisors tab            -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A3.1">
      GATE: Do not modify script 10 until the Pattern 0 alignment thread
      (2026-03-03-advisors-stacked-bar-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt defines: the exact output schema for advisor_rolling_flows.json,
      how outflows are encoded (sign convention vs separate field), what period-anchored
      aggregation is feasible given available history, and the TypeScript interface
      DE and RD agreed on.
    </requirement>
    <requirement id="A3.2">
      In the thread, describe what script 10 currently computes, what parquet columns
      carry inflows vs outflows vs net NNA, and what date history is available.
      Be specific about whether inflows and outflows are tracked separately in the
      source data or only as net NNA. Let DE and RD shape the output contract from
      what you describe as feasible.
    </requirement>
    <requirement id="A3.3">
      After thread completes: implement the agreed stacked_bar and rolling_1y output
      in script 10. Update data_contract.xml BEFORE signaling DT for Stream B2 deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM E — Books data contract audit (BLOCKED by Stream D)       -->
    <!-- ================================================================ -->
    <requirement id="E.1">
      BLOCKED: Do not begin Stream E until the Books design thread
      (2026-03-03-books-tab-design) completes and you have a receipt in your threads/ folder.
      In that thread, you are the knowledge source. Read the advisor-publisher Lambda and
      scripts 03, 05b, and 06 carefully. Describe precisely what each script produces
      and which of those outputs currently flow into the publisher vs remain gold-layer only.
    </requirement>
    <requirement id="E.2">
      After thread: produce a gap list (what L4 fields exist in gold but are absent from
      the publisher output). Add to data_contract.xml as a pending Books L4 section.
      Implement the publisher additions. Update data_contract.xml to complete status
      BEFORE signaling DT for Stream F deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">A4: Bell curve verification result in session log with actual threshold values; patch applied if needed.</criterion>
    <criterion id="2">A5: opal-users-v2 mapping findings documented in session log; option (c) flagged to COO if no mapping exists.</criterion>
    <criterion id="3">A1: adv_drill implemented per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="4">A2: cla_timeseries implemented per thread receipt; classification logic agreed in thread; data_contract.xml updated.</criterion>
    <criterion id="5">A3: advisor_rolling_flows.json updated per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="6">E: L4 publisher gap list produced and closed; data_contract.xml updated (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>A1, A2, A3 are BLOCKED until Pattern 0 thread receipts are in your threads/ folder. Do not implement from PRD descriptions alone — the thread contract supersedes the PRD's suggested shapes.</constraint>
    <constraint>data_contract.xml must be updated and committed BEFORE signaling DT to deploy any Lambda change. This is a non-negotiable quality gate.</constraint>
    <constraint>Do NOT deploy directly. Hand off to 0.4.0_DT via your session log next steps with the commit hash of your code change.</constraint>
    <constraint>Do NOT use emojis in any script, Lambda, or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>Start A4 and A5 in your first session. These have no thread dependency.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-continuous-nna-cla-alignment" status="pending" note="A1 and A2 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-advisors-stacked-bar-alignment" status="pending" note="A3 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-books-tab-design" status="pending" note="E blocked until thread receipt"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 09 verification result (and patch if needed)</deliverable>
    <deliverable type="document">Session log with A5 opal-users-v2 findings</deliverable>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py: adv_drill + cla_timeseries per thread receipt (A1+A2)</deliverable>
    <deliverable type="commit">10_generate_advisor_rolling_flows.py: stacked_bar + rolling_1y per thread receipt (A3)</deliverable>
    <deliverable type="document">data_contract.xml updated for A1, A2, A3 (before each DT deploy)</deliverable>
    <deliverable type="document">data_contract.xml updated with Books L4 contract (post-thread, Stream E)</deliverable>
  </deliverables>
</task_order>
```
