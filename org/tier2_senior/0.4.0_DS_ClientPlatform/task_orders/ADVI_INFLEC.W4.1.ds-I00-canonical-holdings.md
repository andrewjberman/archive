<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.1-I00-holdings</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `data/inflection/scripts/gold/I_00.canonical_holdings.py` — FIFO lot reconstruction from Orion TRN silver. Mirrors `data/black_diamond/scripts/gold/B_01.canonical_holdings.py` pattern (~60-70% reuse per PRD §2). Outputs `gold/canonical/holdings_{date}.parquet` to `opal-data-inf`. No Schwab overlay (single Fidelity custodian, no cross-custodian reconciliation needed).
  </objective>

  <context>PRD §9 W4.1. Inflection has no Schwab NaT complexity but does have the Keil/Keil Financial Partners potential duplicate rep record (PRD §10 Q7 — open; handle with a dedup convention if encountered in silver). Single custodian = simpler FIFO reconstruction than BD. 4.29M transactions (~1/30th BD volume).</context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-pipescript io B_01 (BD precedent)</run>
    <expect>BD I/O pattern. Adapt for inf-pipeline s3 paths.</expect>

    <run>python -m py_compile data/inflection/scripts/gold/I_00.canonical_holdings.py</run>
    <expect>Exit 0.</expect>
    <run>.tools/ds-commit-gate.sh data/inflection/scripts/gold/I_00.canonical_holdings.py</run>
    <expect>Both pass.</expect>

    Phase 2:
    <run>comp-pipescript io I_00</run>
    <expect>0 COLUMN GAPS. All columns accessed are in the silver load list.</expect>

    Phase 3:
    <run>comp-pipescript deployed I_00</run>
    <expect>MATCH after S3 upload to opal-data-inf/code/gold/.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W3.4 silver QA pass."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0 on silver data.
    2. comp-pipescript io: 0 COLUMN GAPS.
    3. ds-commit-gate: both pass.
    4. `gold/canonical/holdings_{date}.parquet` written to opal-data-inf with non-zero rows.
    5. comp-pipescript deployed: MATCH.
    6. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inflection/scripts/gold/I_00.canonical_holdings.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror B_01 pattern, adapt s3 paths to opal-data-inf.</requirement>
    <requirement id="2">No Schwab-specific logic — Fidelity single custodian only.</requirement>
    <requirement id="3">If Keil duplicate reps found: dedup by advisor_key, document in session log, flag to COO.</requirement>
    <requirement id="4">ds-commit-gate + commit + push + S3 upload (DS owns full cycle).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_00.canonical_holdings.py committed + pushed.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT add Schwab overlay logic.</rule>
    <rule>Do NOT skip ds-commit-gate.sh.</rule>
  </do_not>
</task_order>
