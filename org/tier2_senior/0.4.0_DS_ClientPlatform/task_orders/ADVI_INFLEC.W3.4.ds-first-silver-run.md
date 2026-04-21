<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w3.4-first-silver-run</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Run `convert_orion_to_silver.py` against the uploaded bronze CSVs (W3.3) on `inf-gold-layer-runner` EC2 (W2.1). Validate silver output shape, row counts, and data quality against the schema spec (W3.1). Document Q2 2024 gap coverage.
  </objective>

  <context>PRD §5.3 Phase 1. First silver run is on the runner EC2 via SSM dispatch. DS validates: no NaT date rows in output, rep attribution coverage, row counts vs bronze source, Q2 2024 flag correctness. Blocked on W3.2 (script), W3.3 (bronze data), W2.1 (runner EC2).</context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-pipescript deployed convert_orion_to_silver</run>
    <expect>MATCH — runner has the committed script version.</expect>

    Phase 3:
    <run>aws s3 ls s3://opal-data-inf/silver/ --recursive | head -20</run>
    <expect>transactions/, accounts_dim/, aum_snapshot/ parquet files present.</expect>

    <run>python -c "import pandas as pd; df=pd.read_parquet('s3://opal-data-inf/silver/transactions/latest.parquet'); print(df.dtypes); print(df['transaction_date'].isna().sum(), 'NaT rows')"</run>
    <expect>0 NaT rows in transaction_date. All dtypes match schema spec.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W3.2, W3.3, W2.1. All three must be complete before firing this run."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Silver parquets written for all available date range.
    2. 0 NaT rows in date columns.
    3. Row count logged vs bronze source count (tolerance: exact match except for known dedup rules).
    4. Q2 2024 coverage documented (gap flagged per convention, or absent noted).
    5. Rep attribution check: every transaction has a non-null advisor_key (or firm-bucket-key per convention).
    6. Session log with silver row counts, dtypes, NaT check, Q2 2024 gap status.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">data/inflection/scripts/convert_orion_to_silver.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">comp-pipescript deployed: MATCH before run.</requirement>
    <requirement id="2">If any NaT rows found: fix in W3.2 script first, re-run.</requirement>
    <requirement id="3">Do NOT proceed to W4 until silver QA passes.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with silver QA validation output.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT proceed to gold scripts if silver has NaT dates or schema violations.</rule>
  </do_not>
</task_order>
