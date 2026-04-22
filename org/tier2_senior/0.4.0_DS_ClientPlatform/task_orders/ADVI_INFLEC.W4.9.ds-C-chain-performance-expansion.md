<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.9-C-chain-perf</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author the full C-chain performance expansion for INF:
    `I_C00.canonical_performance.py`, `I_C01b.role_aua_backfill.py`,
    `I_C02.client_performance.py`, `I_C03.account_performance.py`,
    `I_C04.validate_aua.py`, `I_C05.client_tax_liability.py`,
    `I_C06.client_mix_timeseries.py`, `I_C07.advisor_attribution.py`,
    `I_C08.advisor_fee_efficiency.py`.
    I_C02 client_performance is the critical upstream for all D-chain platinum publishers.
    Blocked on W4.8 (B-chain + prices) complete.
  </objective>

  <context>
    PRD §9 W4. C-chain computes AUA/NNA/performance aggregates from positions_cube + holdings.
    Key INF differences vs BD:
    - I_C02 client_performance: single Fidelity custodian — no cross-custodian AUA merge
    - I_C07 advisor_attribution: Inflection has 11 advisors, all on one rep_code hierarchy;
      no architect/implementor split needed (PRD §10 Q7 open — default to single role)
    - I_C04 validate_aua: non-blocking; compare gold AUA vs silver allocation totals
    - I_C05 client_tax_liability: Inflection clients are high-net-worth; tax liability
      calculation is expected to be populated (do not short-circuit)
    - I_C08 advisor_fee_efficiency: uses fee_rate_history (I_A02 output); confirm
      Orion exports fee rates in silver (if not, log and stub zeros with WARNING)
    I_C02 is the gating dependency for D-chain (I_D00c, I_D02, I_D04, I_09).
    Do not author W4.10 (D-chain remaining) until I_C02 is complete.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before authoring):
    <run>comp-pipescript io C_02 (BD precedent)</run>
    <expect>C_02 inputs: positions_cube + accounts_dimension. Adapt for INF paths.</expect>
    <run>comp-pipescript io C_07</run>
    <expect>Advisor attribution inputs — note if architect/implementor split logic exists.</expect>

    Phase 2 (after authoring):
    <run>python -m py_compile data/inf/scripts/gold/I_C0N.py</run>
    <expect>Exit 0 for each of the 9 scripts.</expect>
    <run>.tools/ds-commit-gate.sh data/inf/scripts/gold/I_C00.canonical_performance.py data/inf/scripts/gold/I_C01b.role_aua_backfill.py data/inf/scripts/gold/I_C02.client_performance.py data/inf/scripts/gold/I_C03.account_performance.py data/inf/scripts/gold/I_C04.validate_aua.py data/inf/scripts/gold/I_C05.client_tax_liability.py data/inf/scripts/gold/I_C06.client_mix_timeseries.py data/inf/scripts/gold/I_C07.advisor_attribution.py data/inf/scripts/gold/I_C08.advisor_fee_efficiency.py</run>
    <expect>All 9 pass both gates.</expect>

    Phase 3:
    <run>comp-pipescript deployed I_C02</run>
    <expect>MATCH on inf-gold-runner.</expect>
    <run>aws s3 ls s3://opal-data-inf/code/gold/ | grep I_C</run>
    <expect>All 9 C-chain scripts present.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    blocked_on: "W4.8 (B-chain + prices resolution) complete."
    required_action: "After I_C02 is authored and uploaded, message COO immediately —
    D-chain authoring (W4.10) can unblock."
    aua_terminology: Read docs/data/gold_runner_term_definitions.md before writing ANY
    AUA field. Use total_aua / tagged_aua / fee_earning_aua per DDL — managed_aua is DEAD.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All 9 scripts py_compile exit 0 + ds-commit-gate PASS.
    2. I_C02: output schema includes total_aua, fee_earning_aua, tagged_aua — NO managed_aua.
    3. I_C04 validate_aua: non-blocking (exits 0 even if validation warns).
    4. I_C07: no architect/implementor split hardcoded — single advisor role per Inflection structure.
    5. I_C08: if fee_rate_history missing from silver, stubs zeros with WARNING log line (not error).
    6. NaT guard on all date columns in all 9 scripts.
    7. comp-pipescript deployed MATCH on inf-gold-runner.
    8. Session log: AUA field naming audit, fee rate availability note, S3 upload confirmation.
    9. MCP COO on completion — W4.10 gate signal.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inf/scripts/gold/I_C00.canonical_performance.py</file>
      <file action="create">data/inf/scripts/gold/I_C01b.role_aua_backfill.py</file>
      <file action="create">data/inf/scripts/gold/I_C02.client_performance.py</file>
      <file action="create">data/inf/scripts/gold/I_C03.account_performance.py</file>
      <file action="create">data/inf/scripts/gold/I_C04.validate_aua.py</file>
      <file action="create">data/inf/scripts/gold/I_C05.client_tax_liability.py</file>
      <file action="create">data/inf/scripts/gold/I_C06.client_mix_timeseries.py</file>
      <file action="create">data/inf/scripts/gold/I_C07.advisor_attribution.py</file>
      <file action="create">data/inf/scripts/gold/I_C08.advisor_fee_efficiency.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">AUA terminology: total_aua / fee_earning_aua / tagged_aua ONLY. Never managed_aua.</requirement>
    <requirement id="2">NaT guard mandatory on all date joins (d87377a5).</requirement>
    <requirement id="3">Single custodian: no Schwab-specific branches.</requirement>
    <requirement id="4">I_C07 advisor_attribution: no architect/implementor hardcode.</requirement>
    <requirement id="5">ds-commit-gate + commit + push + S3 upload (opal-data-inf/code/gold/).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">9 scripts committed + pushed to CLOUD.</deliverable>
    <deliverable type="s3">Uploaded to s3://opal-data-inf/code/gold/.</deliverable>
    <deliverable type="document">Session log: AUA field audit, fee rate note, S3 confirmation.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT use managed_aua anywhere.</rule>
    <rule>Do NOT hardcode architect/implementor split in I_C07.</rule>
    <rule>Do NOT skip NaT guard on any date column.</rule>
    <rule>Do NOT signal W4.10 until I_C02 is S3-uploaded and MATCH confirmed.</rule>
  </do_not>
</task_order>
