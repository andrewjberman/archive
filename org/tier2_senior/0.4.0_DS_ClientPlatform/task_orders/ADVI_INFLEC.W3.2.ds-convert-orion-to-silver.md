<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w3.2-silver-script</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>pending</status><!-- GO 2026-04-22 per Andrew directive — assigned to ~A -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `data/inflection/scripts/convert_orion_to_silver.py` per the CTO-approved silver schema spec (W3.1). Reads Orion CSVs from `s3://opal-data-inf/bronze/orion/{date}/`, transforms per spec, writes `silver/transactions/{date}.parquet`, `silver/accounts_dim/{date}.parquet`, `silver/aum_snapshot/{date}.parquet`. Includes Q2 2024 gap flag and NaT guard on all outer-merge joins.
  </objective>

  <context>
    PRD §5.1-§5.2. Blocked on W3.1 CTO sign-off on schema spec. DS authors from spec exactly. Pattern mirrors BD silver scripts in `data/black_diamond/scripts/silver/` — pandas + pyarrow + boto3. Inflection has no Schwab overlay complexity (99.4% Fidelity, single source system). Rep attribution is simpler: per-transaction Rep ID + Rep Name natively map to advisor_key. Q2 2024 gap: rows from 2024-04-01 to 2024-06-30 flagged with `data_gap=True` column if partial data present, or entirely absent with logged warning.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>python -m py_compile data/inflection/scripts/convert_orion_to_silver.py</run>
    <expect>Exit 0. No compile errors.</expect>
    <run>.tools/ds-commit-gate.sh data/inflection/scripts/convert_orion_to_silver.py</run>
    <expect>Both gates pass (py_compile + AST undefined-name scanner).</expect>

    Phase 2:
    <run>comp-pipescript io convert_orion_to_silver</run>
    <expect>COLUMN GAPS: 0. S3-DYNAMIC reads listed. PORTAL CONSUMERS: none yet (silver is upstream, not portal-consumed directly).</expect>

    Phase 3:
    <run>comp-pipescript deployed convert_orion_to_silver</run>
    <expect>MATCH after S3 upload.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W3.1 schema spec sign-off. Blocked on W3.3 (Andrew CSV upload to bronze/) for first real run. Can author + test on sample CSVs before W3.3 if test data available locally."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0 on sample Orion CSV (or real data after W3.3).
    2. Outputs: `silver/transactions/{date}.parquet`, `silver/accounts_dim/{date}.parquet`, `silver/aum_snapshot/{date}.parquet` per schema spec.
    3. comp-pipescript io: 0 COLUMN GAPS.
    4. ds-commit-gate: both checks pass.
    5. NaT guard on all outer-merge joins — date columns coerced before any `int(ds[:4])` style operation.
    6. Q2 2024 gap flagged per spec convention.
    7. Committed + pushed to CLOUD + uploaded to `s3://opal-data-inf/code/silver/`.
    8. comp-pipescript deployed: MATCH.
    9. Session log with comp-pipescript io output + gate results + S3 ls of silver output.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inflection/scripts/convert_orion_to_silver.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W3.1 schema spec CTO sign-off.</requirement>
    <requirement id="2">NaT guard mandatory — lesson from d87377a5 C_01 incident.</requirement>
    <requirement id="3">ds-commit-gate.sh before every commit per CLAUDE.md Rule 14.</requirement>
    <requirement id="4">Commit + push + S3 upload (DS owns full cycle per feedback_ds_commits_ae_deploys.md).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">convert_orion_to_silver.py committed + pushed.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before W3.1 schema spec sign-off.</rule>
    <rule>Do NOT skip NaT guard on any date join.</rule>
    <rule>Do NOT skip ds-commit-gate.sh.</rule>
  </do_not>
</task_order>
