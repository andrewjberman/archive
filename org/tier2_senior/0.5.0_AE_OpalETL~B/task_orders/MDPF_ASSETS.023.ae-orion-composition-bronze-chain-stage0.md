<task_order>
  <metadata>
    <id>MDPF_ASSETS.023</id>
    <slug>ae-orion-composition-bronze-chain-stage0</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <phase3_note>COMPLETE 2026-05-20 (0.5.0_AE_OpalETL~B). Phase 3 verified on chain re-trigger mdpf_daily_20260520_193329 (status=complete): DS~B uploaded the bronze script, Stage 0 ran (STAGE0-BRONZE ok 12s) -- pulled the Orion JWT from SM orion/jwt/current (the OrionJwtReadStage0Bronze grant works), pulled all 9 Opal models, wrote 9 model_*.json + _meta/pull_complete.json to s3://opal-data-mdpf/mdpf/bronze/orion_model_composition/2026-05-20/ (overall=success). AC1-AC6 satisfied. mdpf-pipeline-v1.0.2. RAVC2 to 2.0.0_SA_COO~B.</phase3_note>
    <progress_note>IN FLIGHT 2026-05-20 (0.5.0_AE_OpalETL~B, batch GO). Phase 0 probe done; Phase 1 + Phase 2 SHIPPED: Stage-0 best-effort/non-fatal Orion-bronze step added to mdpf-daily-dispatch.sh (commit afa53a952), runner-role Orion JWT grant terraform-applied + 0-diff + tagged mdpf-pipeline-v1.0.2, dispatch script S3-deployed. BLOCKED for completion on a DS-lane dep: pull_orion_model_composition.py is not yet on s3://opal-data-mdpf/code/scripts/bronze/ (Rule 13) -- MCP'd DS 0.4. Stage 0 WARN-skips non-fatally until it lands. Phase 3 chain-re-trigger verification pending the DS upload (bundled with SXIN_PRODCT.002's). Session log: org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-20/mdpf_assets_023_sxin_prodct_002_mdpf_chain_stage0_and_emit.md.</progress_note>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B, scoped from CTO~B's WS-C bronze-gap diagnosis). Phase-2.5 hardening follow-on -- NOT urgent: Layer 1 (DS Base's resolve_bronze_date roll-forward in the WS-C feeder, commit 7d41d28cd) already makes the daily chain resilient to a missed bronze day. This TO is Layer 2 -- the root-cause fix. Queues in AE 0.7's lane behind the current MDPF/TRSB_LEDGER.009/ADHC_HALTGT/§11 load. COO~B flips to pending + fires GO when the AE 0.7 lane opens.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P3 -- Phase-2.5 hardening. The daily chain is already resilient via the Layer-1 roll-forward; this closes the root cause (no in-chain bronze producer) so a multi-week producer outage cannot silently consume a stale model composition.</priority>
    <sla>~0.5-1d wall (the Orion-API-access probe is the variable).</sla>
  </metadata>

  <references>
    <diagnosis>CTO~B 2026-05-20 (WS-C orion_model_composition bronze-gap, root cause confirmed by direct read of the chain): the mdpf daily chain (infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh) has NO bronze stage -- Stage 1 (feeders) -> Stage 2 (WS-E) -> Stage 3 (WS-A) -> Stage 4 (rollup). The WS-C Stage-1 feeder (build_mdpf_wsc_inflection_feeder.py) consumes Orion model-composition BRONZE, produced by data/mdpf/scripts/bronze/pull_orion_model_composition.py -- which the chain NEVER runs. The 5/18 partition was a one-time manual pull. MDPF_ASSETS.018 chained the WS-C feeder but not the feeder's own upstream bronze -- a one-level-deeper gap, not a .018 defect.</diagnosis>
    <incident>2026-05-20 15:00Z mdpf chain failed at WS-C (no orion_model_composition bronze for 5/20). Layer 1 (DS Base roll-forward, 7d41d28cd) resolved the immediate failure; the 15:12Z re-trigger completed clean. .018 RAVC2-accepted on that clean fire. This TO is the Layer-2 root-cause close.</incident>
  </references>

  <objective>
    Add a best-effort Stage-0 BRONZE step to the mdpf daily chain that runs pull_orion_model_composition.py before Stage 1, so the orion_model_composition bronze the WS-C feeder consumes is refreshed each day in-chain rather than depending on a one-time manual pull. A failed pull is non-fatal -- the WS-C feeder's roll-forward (Layer 1) remains the safety net.
  </objective>

  <context>
    Per CTO~B's diagnosis, the fix is a new Stage 0 in mdpf-daily-dispatch.sh. Four scope points:

    1. NEW STAGE 0 in infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh -- run pull_orion_model_composition.py --upload BEFORE Stage 1 (so the WS-C feeder reads a fresh bronze from S3).
    2. pull_orion_model_composition.py must be present at s3://opal-data-mdpf/code/scripts/bronze/ -- the runner S3-syncs code/scripts/ recursively, so it comes along once uploaded. The bronze-script S3 upload is DS-lane (CLAUDE.md Rule 13 -- DS owns data/*/scripts/bronze/*.py commit->deploy); coordinate with DS 0.4 (DS Base offered the DS side) -- confirm the script is on S3, or have DS upload it, before wiring Stage 0.
    3. THE REAL UNKNOWN (likely the bulk of this TO) -- Orion API access from the runner EC2. The bronze pull hits the Orion API directly (not S3 like the feeder). Confirm the mdpf-daily-runner EC2 has Orion API credentials (Secrets Manager / SSM param) + network egress. MDPF_ASSETS.021 granted only opal-data-inf eclipse S3 read -- the Orion API is a different surface. If credentials/egress are absent, granting them is part of this TO (Terraform iam.tf / Secrets Manager).
    4. FAILURE SEMANTICS -- Stage 0 is BEST-EFFORT / NON-FATAL. A failed pull -> WARN + chain CONTINUES; the WS-C feeder roll-forward absorbs it. Do NOT hard-fail the chain on a bronze-pull failure -- that re-introduces the fragility the roll-forward exists to absorb. Only sustained &gt;7-day staleness is escalation-worthy (the feeder's own staleness-WARN threshold).
  </context>

  <scope>
    <step>Phase 0 -- Probe Orion API access from the mdpf-daily-runner EC2: does it have Orion API credentials (Secrets Manager / SSM param) + network egress? Read iam.tf + the runner instance profile; comp-iam service on the runner role. Confirm pull_orion_model_composition.py is on s3://opal-data-mdpf/code/scripts/bronze/ (coordinate with DS 0.4 if not). This probe determines the bulk of the TO's work.</step>
    <step>Phase 1 -- If Orion API access is absent: grant it via Terraform (iam.tf / Secrets Manager) -- terraform apply, 0-diff replan, tag.</step>
    <step>Phase 2 -- Add Stage 0 to mdpf-daily-dispatch.sh: run pull_orion_model_composition.py --upload before Stage 1, best-effort/non-fatal (failed pull -> WARN, chain continues). Deploy the chain-script change to S3 (same path as the .018 chain-script edit).</step>
    <step>Phase 3 -- Re-trigger the mdpf daily chain; confirm Stage 0 runs, the orion_model_composition bronze for the run date is produced + uploaded, and the WS-C feeder consumes the fresh (not roll-forward) bronze. Also confirm a simulated Stage-0 failure -> WARN + chain continues (non-fatal).</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before write">
      <step>
        <run>comp-iam service for the mdpf-daily-runner instance role + direct read of infra/aws/ec2/mdpf-daily-runner iam.tf + the runner instance profile; `aws s3 ls s3://opal-data-mdpf/code/scripts/bronze/`.</run>
        <expect>A clear yes/no on whether the runner EC2 can reach the Orion API (credentials + egress). The pull_orion_model_composition.py presence on S3 is confirmed (or flagged for DS upload). comp-* does not model the mdpf chain scripts -- iam.tf + the runner profile are read directly (PRD §5-class gap).</expect>
        <if_mismatch>If Orion API access is absent, Phase 1 (grant via Terraform) is in scope. If pull_orion_model_composition.py is not on S3, coordinate the DS-lane upload before wiring Stage 0.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>shellcheck on the modified mdpf-daily-dispatch.sh; if iam.tf changed, comp-iam gaps.</run>
        <expect>shellcheck exits 0; the Stage-0 invocation is non-fatal (a failed pull does not abort the chain -- verify the control flow). comp-iam gaps clean if iam.tf was touched.</expect>
        <if_mismatch>Fix shellcheck findings; if a Stage-0 failure can abort the chain, correct the control flow before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Re-trigger the mdpf daily chain; inspect the run telemetry for Stage 0 + a simulated Stage-0-failure path.</run>
        <expect>Stage 0 runs pull_orion_model_composition.py, the run-date bronze is produced + uploaded, the WS-C feeder consumes the fresh bronze (no roll-forward needed). A simulated Stage-0 failure -> WARN logged + chain CONTINUES (Stages 1-4 still run, WS-C rolls forward).</expect>
        <if_mismatch>If a Stage-0 failure aborts the chain, the non-fatal semantics are wrong -- fix and re-verify. Do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Forward-only -- adds a daily bronze refresh to the chain. No historical reprocessing (the roll-forward already covers historical partitions; existing bronze is not rewritten). Phase 1, if it runs, is Terraform IAM/secrets only.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh ; data/mdpf/scripts/bronze/pull_orion_model_composition.py (DS-lane S3 deploy) ; possibly iam.tf
    also_in_to: MDPF_ASSETS.018 (the chain-integration TO this extends) is COMPLETE -- this is the carved-out Layer-2 follow-on, no overlap. The WS-C feeder roll-forward (DS Base 7d41d28cd) is the Layer-1 safety net this complements.
    last_write_owner: 0.7.0_AE_CloudOps owns the chain script + infra. pull_orion_model_composition.py S3 deploy is DS-lane (Rule 13) -- coordinate with DS 0.4 (DS Base offered).
    required_action: Phase 0 probe FIRST -- the Orion-API-access answer determines whether Phase 1 (Terraform grant) is in scope. Coordinate the bronze-script S3 presence with DS 0.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0 probe documented: a clear finding on Orion API access from the mdpf-daily-runner EC2 (credentials + egress present/absent) and confirmation pull_orion_model_composition.py is on s3://opal-data-mdpf/code/scripts/bronze/.</ac>
    <ac id="AC2">mdpf-daily-dispatch.sh has a Stage 0 that runs pull_orion_model_composition.py --upload before Stage 1; the chain-script change is S3-deployed.</ac>
    <ac id="AC3">Stage 0 is BEST-EFFORT / NON-FATAL: a failed bronze pull logs a WARN and the chain CONTINUES (Stages 1-4 run; WS-C rolls forward). Verified by a simulated Stage-0 failure.</ac>
    <ac id="AC4">A re-triggered chain shows Stage 0 producing + uploading the run-date orion_model_composition bronze, and the WS-C feeder consuming the fresh bronze (no roll-forward).</ac>
    <ac id="AC5">If iam.tf / Secrets Manager changed (Orion API grant): Terraform-only deploy, 0-diff replan, pipeline tag; comp-iam gaps clean.</ac>
    <ac id="AC6">No emoji. shellcheck clean on the modified chain script. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh</file>
    <file action="modify">infra/aws/ec2/mdpf-daily-runner/ (iam.tf / Secrets Manager -- only if Phase 0 finds Orion API access absent)</file>
    <file action="coordinate">data/mdpf/scripts/bronze/pull_orion_model_composition.py (DS-lane S3 deploy -- confirm present or coordinate DS upload)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">Stage-0 bronze step in mdpf-daily-dispatch.sh (+ Terraform Orion-API grant if needed), S3-deployed.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section (Phase 0 probe finding + Phase 3 verification). RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT make a Stage-0 bronze-pull failure hard-fail the chain -- it must be best-effort/non-fatal; the WS-C feeder roll-forward is the safety net. A hard-fail re-introduces the fragility Layer 1 exists to absorb.</rule>
    <rule>Do not deploy infra outside Terraform (CLAUDE.md Rule 1) -- the Orion-API grant, if needed, is terraform apply.</rule>
    <rule>Do not upload pull_orion_model_composition.py yourself if it is a DS-owned bronze script not yet on S3 -- that is DS-lane (Rule 13); coordinate with DS 0.4.</rule>
    <rule>Do not rewrite historical orion_model_composition bronze partitions -- forward-only daily refresh.</rule>
  </do_not>
</task_order>
