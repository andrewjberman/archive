<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.11-ae-dispatch</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `inf-gold-dispatch.sh` — the run orchestrator for the INF gold pipeline.
    Mirrors `data/black_diamond/scripts/gold/gold_dispatch.sh`.
    Supports `--from {script} --chain {incremental|full}` invocation pattern.
    Also: author `gold/dimensions/dim_inf_advisor_office.csv` and upload to
    `s3://opal-data-inf/gold/dimensions/` (required precondition for I_D00b and I_09).
    Upload inf-gold-dispatch.sh to `s3://opal-data-inf/code/gold/`.
    Register in `infra/aws/ec2/EC2_MANIFEST.json` under inf-gold-layer-runner dispatch script entry.
  </objective>

  <context>
    This TO was deferred from W2.1 ("inf-gold-dispatch.sh --from I_00 --chain full will be
    authored in W3/W4"). AE 0.6.1 is the inflection pipeline ETL lane — responsible for
    dispatch orchestration and artifact staging.

    The dispatch script must:
    1. Accept `--from {I_A00|I_B01|I_C00|I_D00|I_00|...}` to start at any chain step
    2. Accept `--chain {full|incremental}` — full runs entire A→B→C→D chain;
       incremental runs D-chain only (assumes A/B/C gold outputs exist in S3)
    3. Execute scripts sequentially (no parallelism — read-during-write race condition risk)
    4. Chain order: I_A00 → I_A01 → I_A02 → I_A03 → I_A04 →
                    I_B01 → I_B01b → I_B02 → I_B03 →
                    I_C00 → I_C01 → I_C01b → I_C02 → I_C03 → I_C04 → I_C05 → I_C06 → I_C07 → I_C08 →
                    I_D00 → I_D00b → I_D00c → I_D02 → I_D03 → I_D04 → I_09
    5. Incremental chain: I_D00 → I_D00b → I_D00c → I_D02 → I_D03 → I_D04 → I_09
    6. Each script pulled from `s3://opal-data-inf/code/gold/` before run (same S3 pull pattern as BD)
    7. Watchdog: 5-min grace-window pattern (11478af7) — NOT GOLD_KEEP_ALIVE

    dim_inf_advisor_office.csv:
    Inflection has 11 advisors. Columns: advisor_id, advisor_name, office_name, office_city, office_state.
    Source: use Orion advisor data from W3.4 silver to populate. If office data not in silver,
    stub with "Inflection HQ" as office_name for all advisors and log WARNING.
    Upload to: s3://opal-data-inf/gold/dimensions/dim_inf_advisor_office.csv
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>cat data/black_diamond/scripts/gold/gold_dispatch.sh</run>
    <expect>BD dispatch pattern. Mirror for INF with updated chain order and S3 paths.</expect>

    Phase 2:
    <run>bash -n data/inf/scripts/gold/inf-gold-dispatch.sh</run>
    <expect>Syntax valid — exit 0.</expect>
    <run>aws s3 ls s3://opal-data-inf/gold/dimensions/dim_inf_advisor_office.csv</run>
    <expect>Object present.</expect>

    Phase 3:
    <run>comp-pipescript deployed inf-gold-dispatch (once uploaded)</run>
    <expect>MATCH on inf-gold-runner.</expect>
    <run>aws s3 ls s3://opal-data-inf/code/gold/inf-gold-dispatch.sh</run>
    <expect>Object present.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "After dim_inf_advisor_office.csv is uploaded, MCP to DS immediately
    — I_D00b is unblocked. This can happen before the full dispatch script is complete."
    ec2_manifest: "Update inf-gold-layer-runner entry in EC2_MANIFEST.json with
    dispatch_script: s3://opal-data-inf/code/gold/inf-gold-dispatch.sh."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. inf-gold-dispatch.sh: bash -n syntax valid. Supports --from + --chain flags.
    2. Full chain order matches A→B→C→D sequence above (sequential, no parallelism).
    3. Incremental chain: D-chain only.
    4. Each script pulled from S3 before execution (not run from local disk).
    5. Watchdog: 5-min grace-window, NOT GOLD_KEEP_ALIVE.
    6. dim_inf_advisor_office.csv: 11 rows (one per advisor), uploaded to opal-data-inf/gold/dimensions/.
    7. inf-gold-dispatch.sh uploaded to s3://opal-data-inf/code/gold/.
    8. EC2_MANIFEST.json updated with dispatch_script field for inf-gold-layer-runner.
    9. MCP to DS when dim_inf_advisor_office.csv is uploaded (I_D00b precondition met).
    10. MCP COO on full completion — W4.12 validation pass can begin once all scripts authored.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inf/scripts/gold/inf-gold-dispatch.sh</file>
      <file action="create">data/inf/dimensions/dim_inf_advisor_office.csv</file>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Sequential execution — no parallel script runs.</requirement>
    <requirement id="2">S3-pull pattern before run (not local disk execution).</requirement>
    <requirement id="3">Watchdog: grace-window (11478af7). No GOLD_KEEP_ALIVE.</requirement>
    <requirement id="4">dim_inf_advisor_office.csv uploaded BEFORE signaling DS.</requirement>
    <requirement id="5">safe-ec2-deploy.sh for any EC2-side deployment per CLAUDE.md Rule 7.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">inf-gold-dispatch.sh + dim_inf_advisor_office.csv + EC2_MANIFEST.json update committed.</deliverable>
    <deliverable type="s3">Both artifacts uploaded to opal-data-inf.</deliverable>
    <deliverable type="document">Session log: chain order, dim office CSV content, S3 upload confirmation.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT use GOLD_KEEP_ALIVE watchdog pattern.</rule>
    <rule>Do NOT run scripts in parallel.</rule>
    <rule>Do NOT hardcode script paths — pull from S3 on each run.</rule>
  </do_not>
</task_order>
