<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.7-A-chain-dims</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>active</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author the full A-chain dimensional foundation for the INF gold pipeline:
    `I_A00.accounts_dimension.py`, `I_A01.advisor_assignments.py`,
    `I_A02.fee_rate_history.py`, `I_A03.positions_cube.py`,
    `I_A04.client_dimension.py`.
    These are the foundational dimension tables that every downstream C-chain and D-chain
    script reads. Mirror the BD A_0x scripts exactly, substituting `opal-data-inf`
    for `opal-data-bd` and Orion silver schema for BD silver schema.
    All 5 scripts committed, ds-commit-gate passed, uploaded to
    `s3://opal-data-inf/code/gold/`.
  </objective>

  <context>
    PRD §9 W4. Inflection silver is Orion-native (not BD/Schwab). The A-chain reads
    silver account/advisor/position data. Key differences vs BD:
    - Single custodian (Fidelity only — no Schwab custodian_code branching)
    - 11 advisors (not ~100): advisor_assignments is smaller
    - No cross-custodian account dedup needed
    - Orion silver schema uses `account_id`, `advisor_id`, `rep_code` columns
      (confirmed in W3.4 silver parquet; check actual column names from silver before coding)
    - Keil/Keil Financial Partners dedup: if advisor_id collision on rep_code,
      dedup by earliest `start_date`, flag in session log
    W3.4 silver run must be complete before authoring validation (scripts can be
    authored now; validation against silver in W4.12).
    I_A03.positions_cube.py is the core fact table that feeds C_02 client_performance
    and all downstream aggregates — treat with care.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before authoring):
    <run>comp-pipescript io A_00 (BD precedent)</run>
    <expect>BD I/O columns. Note which silver columns are read — verify INF silver has equivalents.</expect>
    <run>comp-pipescript io A_03</run>
    <expect>positions_cube column requirements — core fact table inputs.</expect>

    Phase 2 (after authoring each script):
    <run>python -m py_compile data/inf/scripts/gold/I_A0N.py</run>
    <expect>Exit 0 for each script.</expect>
    <run>.tools/ds-commit-gate.sh data/inf/scripts/gold/I_A00.accounts_dimension.py data/inf/scripts/gold/I_A01.advisor_assignments.py data/inf/scripts/gold/I_A02.fee_rate_history.py data/inf/scripts/gold/I_A03.positions_cube.py data/inf/scripts/gold/I_A04.client_dimension.py</run>
    <expect>All 5 pass both gates.</expect>

    Phase 3 (after commit + S3 upload):
    <run>comp-pipescript deployed I_A03</run>
    <expect>MATCH on inf-gold-runner.</expect>
    <run>aws s3 ls s3://opal-data-inf/code/gold/ | grep I_A</run>
    <expect>All 5 scripts present.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "I_A03 positions_cube is the critical upstream for I_C02 client_performance
    (W4.9). Do not signal W4.9 start until I_A03 is authored and uploaded."
    dim_advisor_office: AE 0.6.1 will author `gold/dimensions/dim_inf_advisor_office.csv`
    in W4.11 — do NOT hardcode office assignments in I_A01; read from S3 dimension file.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All 5 scripts exit 0 on py_compile.
    2. ds-commit-gate PASS on all 5.
    3. I_A03 positions_cube: column schema matches expected output (account_id, ticker,
       date, units, market_value, custodian — Fidelity only).
    4. No Schwab custodian_code branches in any script.
    5. comp-pipescript deployed: MATCH on inf-gold-runner for all 5.
    6. Session log with: silver column mapping, Keil dedup outcome (if any), S3 upload confirmation.
    7. MCP COO on completion — W4.8 gate signal.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inf/scripts/gold/I_A00.accounts_dimension.py</file>
      <file action="create">data/inf/scripts/gold/I_A01.advisor_assignments.py</file>
      <file action="create">data/inf/scripts/gold/I_A02.fee_rate_history.py</file>
      <file action="create">data/inf/scripts/gold/I_A03.positions_cube.py</file>
      <file action="create">data/inf/scripts/gold/I_A04.client_dimension.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">S3 paths: opal-data-inf throughout. No opal-data-bd reads.</requirement>
    <requirement id="2">Single custodian: remove all Schwab branching from BD mirrors.</requirement>
    <requirement id="3">I_A03 positions_cube: NaT guard on all date columns (d87377a5 mandate).</requirement>
    <requirement id="4">ds-commit-gate + commit + push + S3 upload (opal-data-inf/code/gold/).</requirement>
    <requirement id="5">Session log must map BD silver column names → INF silver column names for each script.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">5 scripts committed + pushed to CLOUD.</deliverable>
    <deliverable type="s3">All 5 uploaded to s3://opal-data-inf/code/gold/.</deliverable>
    <deliverable type="document">Session log with column mapping + Keil dedup note.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT read from opal-data-bd in any INF script.</rule>
    <rule>Do NOT include Schwab custodian logic.</rule>
    <rule>Do NOT skip ds-commit-gate.sh on any script.</rule>
    <rule>Do NOT signal W4.8 until all 5 scripts are uploaded to S3.</rule>
  </do_not>
</task_order>
