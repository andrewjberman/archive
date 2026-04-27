<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.13-first-full-run</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- COMPLETE 20260427T142449Z by 0.6.0_AE_PartnerETL under CTO authorization (0.6.1 offline). I_C00 run 4: 2,408 canonical_performance files (2026-04-27). D-chain exit 0 14:22Z. platinum/firm/leaderboard.json + partner_analytics.json live on S3. RAVC4 delivered. FLAG: platinum/advisors/ has 0 fresh files (I_09 firm-only, quarantine only) — CTO/COO design ruling pending before W5.1. Session log: 0.6.0_AE logs/2026-04-27/inflec_w4.13b_run4.md -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Execute the first full production gold chain run on `inf-gold-layer-runner` via SSM.
    Chain: `inf-gold-dispatch.sh --from I_A00 --chain full`.
    Monitor to completion. Confirm platinum artifacts in `s3://opal-data-inf/platinum/`.
    Signal DS~C (W4.12) to begin validation pass, then signal COO on completion.
    Blocked on W4.11 (dispatch script uploaded) AND W4.12 PASS (validation complete).
    Note: W4.12 runs its own chain; this TO is the PRODUCTION run after W4.12 confirms
    all scripts are correct.
  </objective>

  <context>
    This is the first PRODUCTION gold chain run for Inflection — the moment INF gold data
    appears in S3 for the first time. AE 0.6.1 owns dispatch orchestration for the
    inflection pipeline. DS~C has already validated the chain in W4.12.

    Run order:
    1. AE dispatches via SSM: `inf-gold-dispatch.sh --from I_A00 --chain full`
    2. Monitor CloudWatch log group `/aws/ec2/inf-gold-layer-runner` for completion
    3. Confirm each stage exits 0 (A→B→C→D sequential)
    4. After chain completes: `aws s3 ls s3://opal-data-inf/platinum/firm/` — confirm presence
    5. MCP to DS~C with chain log for final comp-validate review
    6. After DS~C PASS: MCP COO (ADVI_INFLEC platinum LIVE — W5.1 can fire)

    If any script fails mid-chain:
    - Stop immediately. Do NOT re-run from start without DS analysis.
    - MCP DS operator (0.4.0_DS_ClientPlatform) with exact error + log snippet.
    - MCP COO with BLOCKED status.
    - Wait for DS fix + S3 re-upload before re-dispatch from failed step.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-pipescript deployed inf-gold-dispatch</run>
    <expect>MATCH — confirms latest dispatch script is on runner.</expect>
    <run>aws ec2 describe-instances --filters Name=tag:Name,Values=inf-gold-layer-runner --query 'Reservations[*].Instances[*].{State:State.Name}'</run>
    <expect>running (start instance if stopped).</expect>

    Phase 2 (SSM dispatch):
    <run>aws ssm send-command --instance-ids {INF_RUNNER_INSTANCE_ID} --document-name AWS-RunShellScript --parameters commands=["cd /opt/gold && bash inf-gold-dispatch.sh --from I_A00 --chain full >> /var/log/inf-gold/chain_full_$(date +%Y%m%d_%H%M%S).log 2>&1"]</run>
    <expect>Command ID returned. Monitor via aws ssm get-command-invocation until status=Success.</expect>

    Phase 3 (post-run validation):
    <run>aws s3 ls s3://opal-data-inf/platinum/firm/</run>
    <expect>leaderboard.json + partner_analytics.json present.</expect>
    <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | wc -l</run>
    <expect>At least 11 advisor files.</expect>
    <run>comp-validate I_09 --artifact /tmp/partner_analytics_prod.json (download from S3 first)</run>
    <expect>Exit 0.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    blocked_on: "W4.11 (dispatch script + dim_inf_advisor_office.csv uploaded) AND W4.12 (DS~C validation PASS)."
    on_success: "MCP COO: ADVI_INFLEC platinum LIVE. COO will fire W5.1 GO to DE (populate inflection overrides)."
    on_failure: "MCP DS operator immediately with error log. MCP COO with BLOCKED status."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. SSM command exits 0 for the full chain.
    2. platinum/firm/leaderboard.json present in opal-data-inf.
    3. platinum/firm/partner_analytics.json present in opal-data-inf.
    4. platinum/advisors/ contains at least 11 advisor subdirectories.
    5. comp-validate exits 0 on partner_analytics.json.
    6. Chain log committed to `org/tier2_senior/0.6.1_AE_PartnerETL/logs/{date}/inf_gold_chain_full_first_run.md`.
    7. MCP COO: "ADVI_INFLEC platinum LIVE" with S3 artifact inventory.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-21/inf_gold_chain_full_first_run.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Use SSM for dispatch — never SSH directly to EC2 per CLAUDE.md rules.</requirement>
    <requirement id="2">Monitor to completion before declaring success.</requirement>
    <requirement id="3">comp-validate exit 0 required before signaling COO.</requirement>
    <requirement id="4">If any script fails mid-chain: STOP, MCP DS + COO, do not re-run without fix.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with SSM command ID, chain duration, artifact inventory, comp-validate output.</deliverable>
    <deliverable type="signal">MCP COO: PASS (platinum LIVE) or BLOCKED (with failure evidence).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT declare success without comp-validate exit 0.</rule>
    <rule>Do NOT re-run chain from scratch on failure without DS analysis.</rule>
    <rule>Do NOT SSH directly to EC2 — SSM only.</rule>
  </do_not>
</task_order>
