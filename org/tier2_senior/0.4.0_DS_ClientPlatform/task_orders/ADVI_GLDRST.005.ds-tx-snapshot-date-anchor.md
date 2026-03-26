<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-005-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>pending</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Fix the TX snapshot date anchor mismatch in bd-portal-publisher and
    ensure all gold scripts use a consistent date determination methodology.

    Two sub-problems:
    1. Publisher snapshot view uses global max date across all countries;
       continuous view uses US-only max date. This creates a ~$17M gap
       in state-level AUA comparisons (Texas).
    2. Scripts 03/05/05b each independently determine "latest date" from
       different sources. A single authoritative date anchor should be
       established per gold run.
  </objective>

  <context>
    TX discrepancy documented in docs/architecture/ADVI_segment_analytics_variance.md.

    Publisher snapshot path (line 1794):
      geo_latest = geo[geo['date'] == geo['date'].max()]
      # Uses global max date across ALL countries

    Publisher continuous view (lines 657-661):
      geo_us = geo[geo['country'].isin(...)]
      latest_date_geo = geo_us['date'].max()
      # Uses US-only max date

    Fix: align snapshot to US-only max date.

    Script date determination:
    - run_gold_layer.sh passes --start-date to script 02 (8 days ago for incremental)
    - Script 03: snapshot_date = pd.Timestamp.now().normalize()
    - Script 05/05b: latest_date = result['date'].max() (from positions_cube)
    - These can diverge if a gold run spans midnight or if positions_cube
      has different latest dates than the current wall-clock date
  </context>

  <scope>
    <files>
      <file action="diagnostic">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="modify">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS1: Diagnose and document the publisher date anchor mismatch.
      Confirm the ~$17M TX gap is caused by the global vs US-only max
      date divergence. Propose the fix (US-only max date for both views)
      and document in session log. The actual Lambda code change is DT
      scope (.007) — DS provides the fix specification.
    </requirement>

    <requirement id="2">
      WS2: Add a --run-date flag to run_gold_layer.sh that is passed
      to all scripts as the authoritative date anchor. Scripts that
      currently determine their own "today" should accept this flag
      and use it if provided, falling back to auto-detection if not.

      This ensures all scripts in a single gold run agree on what
      "today" means, even if the run spans midnight.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">WS1: Publisher date anchor fix fully specified with line numbers</criterion>
    <criterion id="2">WS2: --run-date flag accepted by run_gold_layer.sh and propagated to scripts</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify publisher Lambda code (DT scope for .007)</constraint>
    <constraint>--run-date flag must be optional (auto-detect if not provided)</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">Publisher date anchor fix specification for DT</deliverable>
    <deliverable type="commit">run_gold_layer.sh --run-date flag + script plumbing</deliverable>
  </deliverables>
</task_order>
