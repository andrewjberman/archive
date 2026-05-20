<task_order>
  <metadata>
    <id>SXIN_PRODCT.002</id>
    <slug>ae-legacy-emit-in-chain-step</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B, from CTO~B's SXIN architecture ruling -- Option A). SXIN_PRODCT.001's Phase 1 (schedule the legacy emit) is split out here to 0.7.0_AE_CloudOps~B because it edits mdpf-daily-dispatch.sh -- the SAME chain script MDPF_ASSETS.023 edits. CONSOLIDATION: one agent owns both edits to that file. SEQUENCE with MDPF_ASSETS.023: .023 PREPENDS a Stage-0 bronze step; THIS TO APPENDS a post-platinum emit step. Do .023 first (or both in one coherent edit pass), then this -- no two-editor friction. SXIN_PRODCT.001 (0.5.0_AE_OpalETL~B) keeps SXIN Phase 2 (smartx-pipeline cleanup) -- off-script, independent.</dispatch_unblock_condition>
    <project_code>SXIN_PRODCT</project_code>
    <priority>P2 -- productionizes the daily legacy non_model_assets.json emit. Until this lands the legacy emit is fired only on-demand via the MDPF_ASSETS.021 SSM doc (interim bridge).</priority>
    <sla>~0.5d wall -- a focused chain-script edit + S3 re-upload; no Terraform.</sla>
  </metadata>

  <references>
    <ruling>CTO~B 2026-05-20 SXIN architecture ruling -- OPTION A (in-chain step), over Option B (dedicated +45min trigger Lambda). Rationale: a fixed-offset scheduled trigger is the cadence-race anti-pattern MDPF has paid for repeatedly (the 5/19 Cohort-0 incident, the WS-C bronze gap, MDPF_ASSETS.018's whole purpose). An in-chain step runs deterministically when fresh platinum exists, never on a timing guess. "Couples emit to chain success" is correct behavior -- chain fails -> no fresh platinum -> correctly skip the emit. .021's SSM doc + EventBridge framing was the INTERIM bridge; SXIN_PRODCT is the race-free productionization.</ruling>
    <phase0>0.5.0_AE_OpalETL~B SXIN_PRODCT.001 Phase-0 probe (RAVC1 2026-05-20): build_legacy_compat_emit.py reads platinum/mdpf/aggregate_aua/{date}.json which the mdpf daily chain produces -> the emit must run AFTER the WS-A aggregate. The mdpf-daily-runner EC2 is stopped between runs -> a plain EventBridge->SSM SendCommand fails against a stopped instance; the in-chain step runs on the same instance-wake, post-platinum, pre-shutdown.</phase0>
    <chain_script>infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh -- the S3-hosted chain dispatch script. Stages: (Stage 0 bronze -- added by MDPF_ASSETS.023) -> Stage 1 feeders -> Stage 2 WS-E -> Stage 3 WS-A aggregate (writes platinum/mdpf/aggregate_aua/{date}.json) -> Stage 4 rollup.</chain_script>
    <sibling>MDPF_ASSETS.023 (0.7.0_AE_CloudOps~B) -- prepends the Stage-0 orion_model_composition bronze step to the same script. Same agent, same file -- sequence the two edits.</sibling>
  </references>

  <objective>
    Append a post-platinum step to the mdpf daily chain that runs build_legacy_compat_emit.py --upload, so the legacy non_model_assets.json emit is produced deterministically each day from fresh platinum -- replacing the on-demand-only MDPF_ASSETS.021 SSM bridge.
  </objective>

  <context>
    Per CTO~B's Option-A ruling, the legacy emit becomes an in-chain step rather than a separately-scheduled trigger. Add a step to mdpf-daily-dispatch.sh that runs build_legacy_compat_emit.py --upload AFTER the WS-A aggregate (Stage 3) has written today's platinum/mdpf/aggregate_aua/{date}.json.

    GATING (CTO~B placement ruling): gate the emit step on today's platinum aggregate_aua partition being freshly written by Stage 3 -- NOT on Stage-4 rollup success. A Stage-3-OK / Stage-4-fail run still has valid platinum and should still emit. So: place the step immediately after Stage 3, gate it on the Stage-3 platinum write, run it independently of Stage 4's outcome.

    FAILURE SEMANTICS: if Stage 3 did not produce fresh platinum (chain failed before/at Stage 3), the emit step is correctly SKIPPED -- no fresh platinum, nothing to emit. A failure of the emit step itself should log loud (WARN/ERROR) but follow the chain's existing step-failure convention; do not silently swallow it.

    build_legacy_compat_emit.py is DS-owned; it is already S3-deployed (MDPF_ASSETS.017 day-1-zero guard shipped it; the .021 SSM doc S3-pulls + execs it). This TO does NOT modify build_legacy_compat_emit.py -- it only adds the chain-script step that invokes it.

    NO TERRAFORM: this is a script edit to mdpf-daily-dispatch.sh + an S3 re-upload of the chain script (the runner s3-syncs code at boot). No new Lambda, no EventBridge, no IAM, no mdpf-pipeline tag. The MDPF_ASSETS.021 SSM doc + MDPFLegacyEmitInvoker policy become redundant once this lands -- their retirement is a follow-on, not this TO's scope.
  </context>

  <scope>
    <step>Phase 1 -- Read mdpf-daily-dispatch.sh (coordinate with your MDPF_ASSETS.023 edit -- .023 prepends Stage 0; this appends post-Stage-3). Confirm where Stage 3 (WS-A aggregate) writes platinum/mdpf/aggregate_aua/{date}.json and the script's existing step-failure / logging convention.</step>
    <step>Phase 2 -- Add the emit step immediately after Stage 3: gate on today's platinum aggregate_aua/{date}.json freshly written; run build_legacy_compat_emit.py --upload (S3-pull the script the same way the chain pulls its other scripts, or invoke the already-synced copy). Skip cleanly if Stage 3 produced no fresh platinum. Run independently of Stage 4. shellcheck clean; Git Bash / Amazon Linux runtime per the chain's existing conventions.</step>
    <step>Phase 3 -- S3 re-upload the edited mdpf-daily-dispatch.sh to its canonical chain-script S3 location. Re-trigger the mdpf daily chain; confirm the emit step runs post-Stage-3, build_legacy_compat_emit.py --upload executes, non_model_assets.json is refreshed. Also confirm a Stage-3-fail simulation correctly SKIPS the emit.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read of infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh (+ coordinate with the MDPF_ASSETS.023 Stage-0 edit).</run>
        <expect>Stage 3's platinum-write location + the step-failure convention are identified; the .023 Stage-0 edit and this post-Stage-3 edit are non-overlapping insertions into the same file. comp-* N/A -- the mdpf chain scripts are not graph-modeled (documented gap).</expect>
        <if_mismatch>If .023 has not landed yet, sequence: do .023's Stage-0 prepend first, then this append, in one coherent edit pass -- avoid two separate commits racing the same file.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>shellcheck mdpf-daily-dispatch.sh</run>
        <expect>shellcheck exits 0. The emit step is gated on the Stage-3 platinum write, runs independently of Stage 4, and skips cleanly on no-fresh-platinum.</expect>
        <if_mismatch>Fix shellcheck findings; correct the gating if a chain-fail does not skip the emit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Re-trigger the mdpf daily chain; inspect telemetry for the emit step + a simulated Stage-3-fail path.</run>
        <expect>On a clean run: the emit step runs post-Stage-3, build_legacy_compat_emit.py --upload executes, non_model_assets.json refreshed. On a simulated Stage-3 fail: the emit step is SKIPPED (no fresh platinum), logged.</expect>
        <if_mismatch>If the emit runs on stale/absent platinum, the gating is wrong -- fix and re-verify. Do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Forward-only -- adds a daily emit step to the chain. No historical reprocessing; no code change to build_legacy_compat_emit.py itself; no Terraform.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh
    also_in_to: MDPF_ASSETS.023 (0.7.0_AE_CloudOps~B -- SAME agent) prepends a Stage-0 bronze step to this same file. CONSOLIDATED ON ONE AGENT by design (CTO~B ruling) -- sequence the two edits (.023 Stage-0 prepend, then this post-Stage-3 append), ideally one coherent edit pass, to avoid same-file churn. SXIN_PRODCT.001 (0.5.0_AE_OpalETL~B) = SXIN Phase 2 (smartx-pipeline cleanup) -- a different module, independent, no overlap.
    last_write_owner: 0.7.0_AE_CloudOps~B owns mdpf-daily-dispatch.sh edits (this TO + .023).
    required_action: Sequence with .023 on the shared file.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">mdpf-daily-dispatch.sh has a post-Stage-3 step that runs build_legacy_compat_emit.py --upload, gated on today's platinum/mdpf/aggregate_aua/{date}.json being freshly written by Stage 3.</ac>
    <ac id="AC2">The emit step runs independently of Stage 4's outcome (a Stage-3-OK / Stage-4-fail run still emits); it SKIPS cleanly when Stage 3 produced no fresh platinum.</ac>
    <ac id="AC3">shellcheck clean; the edit is non-overlapping with the MDPF_ASSETS.023 Stage-0 edit; the script is S3-re-uploaded to its canonical chain-script location.</ac>
    <ac id="AC4">A re-triggered chain shows the emit step running post-Stage-3 and refreshing non_model_assets.json; a simulated Stage-3 fail correctly skips it.</ac>
    <ac id="AC5">No Terraform change, no new tag (script edit + S3 upload only). No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">mdpf-daily-dispatch.sh post-Stage-3 legacy-emit step, S3-re-uploaded.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT gate the emit on Stage-4 rollup success -- gate on the Stage-3 platinum write. A Stage-3-OK / Stage-4-fail run still has valid platinum and must still emit.</rule>
    <rule>Do NOT schedule the emit on a fixed time offset (the Option-B anti-pattern) -- it is an in-chain step, runs when fresh platinum exists.</rule>
    <rule>Do NOT modify build_legacy_compat_emit.py -- DS-owned; this TO only adds the chain-script step that invokes it.</rule>
    <rule>Do NOT add Terraform / a Lambda / EventBridge -- Option A is a script edit + S3 upload only.</rule>
    <rule>Do NOT make a separate racing commit to mdpf-daily-dispatch.sh -- sequence with your MDPF_ASSETS.023 edit on the same file.</rule>
  </do_not>
</task_order>
