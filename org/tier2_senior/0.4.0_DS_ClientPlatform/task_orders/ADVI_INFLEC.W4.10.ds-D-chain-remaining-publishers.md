<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.10-D-chain-remaining</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <completed>2026-04-22</completed>
    <completed_by>0.4.0_DS_ClientPlatform~A</completed_by>
    <commit>f561dd8c</commit>
    <evidence>I_D00/I_D00b/I_D03 authored from scratch (f88ab74d was a false-positive — commit contained W4.3-W4.5 scripts only). py_compile PASS + ds-commit-gate PASS on all 3. MATCH on S3 (local MD5 == S3 ETag). inf-gold-dispatch.sh catalog fixed: I_C00-&gt;canonical_performance.py, I_C01b-&gt;role_aua_backfill.py.</evidence>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author the remaining D-chain platinum publishers for INF:
    `I_D00.portal_aggregates.py`, `I_D00b.portal_timeseries.py`,
    `I_D03.composition_artifacts.py`.
    I_D00c (leaderboard), I_D02 (advisor_client_detail), I_D04 (client_portal_summary)
    were authored in W4.3-W4.5. This TO closes the D-chain gap.
    Blocked on W4.9 (C-chain) complete — D-chain reads I_C02 + I_C07 outputs.
  </objective>

  <context>
    PRD §9 W4. D-chain converts gold aggregates to portal-ready JSON.
    Key INF differences vs BD:
    - I_D00 portal_aggregates: must read I_C02 (client_performance) from opal-data-inf.
      Output shape must be schema-identical to BD portal_aggregates (portal reads same JSON keys).
    - I_D00b portal_timeseries: has precondition on `dim_inf_advisor_office.csv`
      (authored by AE 0.6.1 in W4.11 — coordinate with AE before running).
      Read from `s3://opal-data-inf/gold/dimensions/dim_inf_advisor_office.csv`.
    - I_D03 composition_artifacts: reads I_B01 holdings_lots + I_C07 advisor_attribution.
      Composition JSON must use schema-identical structure to BD D_03 output (portal consumers are shared).
    - dim_advisor_office precondition: do NOT run I_D00b without confirming
      `s3://opal-data-inf/gold/dimensions/dim_inf_advisor_office.csv` exists (check with AE 0.6.1).
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-pipescript io D_00 (BD precedent)</run>
    <expect>D_00 reads C_02 + C_01 + A_00. Adapt for INF paths.</expect>
    <run>comp-pipescript io D_00b</run>
    <expect>dim_advisor_office.csv precondition — verify AE has uploaded INF equivalent.</expect>
    <run>comp-pipescript io D_03</run>
    <expect>Composition I/O — holdings_lots + architect_attribution.</expect>

    Phase 2:
    <run>python -m py_compile data/inf/scripts/gold/I_D00.portal_aggregates.py</run>
    <run>python -m py_compile data/inf/scripts/gold/I_D00b.portal_timeseries.py</run>
    <run>python -m py_compile data/inf/scripts/gold/I_D03.composition_artifacts.py</run>
    <expect>All 3 exit 0.</expect>
    <run>.tools/ds-commit-gate.sh data/inf/scripts/gold/I_D00.portal_aggregates.py data/inf/scripts/gold/I_D00b.portal_timeseries.py data/inf/scripts/gold/I_D03.composition_artifacts.py</run>
    <expect>All pass.</expect>

    Phase 3:
    <run>comp-pipescript deployed I_D00</run>
    <expect>MATCH on inf-gold-runner.</expect>
    <run>aws s3 ls s3://opal-data-inf/code/gold/ | grep I_D</run>
    <expect>I_D00, I_D00b, I_D03 present (alongside existing I_D00c, I_D02, I_D04).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    blocked_on: "W4.9 (C-chain) complete. AE 0.6.1 W4.11 dim_inf_advisor_office.csv upload."
    required_action: "Before authoring I_D00b, confirm with AE 0.6.1 (W4.11) that
    dim_inf_advisor_office.csv is uploaded to s3://opal-data-inf/gold/dimensions/.
    If not ready, author I_D00 + I_D03 first, park I_D00b until AE signals completion."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All 3 scripts py_compile exit 0 + ds-commit-gate PASS.
    2. I_D00 output JSON schema matches BD portal_aggregates shape (same top-level keys).
    3. I_D00b: reads dim_inf_advisor_office.csv from S3, does not hardcode offices.
    4. I_D03 composition artifacts: JSON schema matches BD D_03 (portal components are shared).
    5. comp-pipescript deployed MATCH for all 3 on inf-gold-runner.
    6. Session log: schema parity notes (D_00/D_00b/D_03 vs BD equivalents).
    7. MCP COO on completion — W4.12 validation pass can begin.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inf/scripts/gold/I_D00.portal_aggregates.py</file>
      <file action="create">data/inf/scripts/gold/I_D00b.portal_timeseries.py</file>
      <file action="create">data/inf/scripts/gold/I_D03.composition_artifacts.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Schema-identical JSON output to BD equivalents — zero portal code changes required.</requirement>
    <requirement id="2">I_D00b: read dim_inf_advisor_office.csv from S3, not hardcoded.</requirement>
    <requirement id="3">NaT guard on all date columns.</requirement>
    <requirement id="4">ds-commit-gate + commit + push + S3 upload.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">3 scripts committed + pushed.</deliverable>
    <deliverable type="s3">Uploaded to s3://opal-data-inf/code/gold/.</deliverable>
    <deliverable type="document">Session log with BD schema parity audit.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT hardcode advisor-to-office assignments in I_D00b.</rule>
    <rule>Do NOT deviate from BD JSON schema shape — portal is shared infrastructure.</rule>
    <rule>Do NOT run I_D00b without confirming dim_inf_advisor_office.csv is on S3.</rule>
  </do_not>
</task_order>
