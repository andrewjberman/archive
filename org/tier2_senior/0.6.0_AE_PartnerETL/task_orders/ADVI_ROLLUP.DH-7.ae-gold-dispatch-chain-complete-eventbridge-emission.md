<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped bd-v2.24.2 2026-04-16 13:11 UTC -->
    <evidence>
      Commit `1829007a` feat(bd-pipeline): DH-7 emit + IAM. Record-deploy `3b9fbf83` [skip ci].
      Tag `bd-v2.24.2` pushed 2026-04-16 13:11 UTC.
      IAM: aws_iam_role_policy.bd_exporter_events_emit created (events:PutEvents on event-bus/default).
      terraform apply: 1 added. Plan post-apply: No changes.
      S3 upload: s3://opal-data-bd/code/gold/gold_dispatch.sh ETag ab7e1127d3f407b956c5059548a9860f VersionId Fi63twJC8vXJatwxYPHsqJo5DFz6.Dzf.
      Rule 7 pre-flag: CTO cleared 13:10:43Z, COO no-object 13:10:46Z.
      First natural fire: tonight 2026-04-17 04:00 UTC (DH-1/2/3/4/7 ride together).
      Bonus stabilization: chain_exit PIPESTATUS[0] + exit propagation (catches tee-branch silent-success; called out to COO/CTO in MCP COMPLETE for catalog).
    </evidence>

    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P1 (HARD-BLOCKS ADVI_49EXEC.007 EventBridge wiring)</priority>
  </metadata>

  <references>
    <ref type="trigger">Andrew direction 2026-04-15 PM (Option A from AE 0.6 EventBridge query 22:11Z): emit custom EventBridge chain-complete signal from gold_dispatch.sh end-of-chain hook</ref>
    <ref type="ae_proposal">AE 0.6 MCP "RE: gold-chain-complete EventBridge signal — does NOT exist; options laid out" (221116Z)</ref>
    <ref type="downstream_consumer">ADVI_49EXEC.007 (DT EventBridge wiring) waits on this signal existing</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Add a `emit_chain_complete()` helper to `gold_dispatch.sh` end-of-chain. Fires once per successful chain close via `aws events put-events` with structured detail payload (chain_label, completed_at, scripts, mode, exit_code).

    Per AE 0.6 proposal:

    ```bash
    emit_chain_complete() {
      aws events put-events --entries "[{
        \"Source\": \"bd-pipeline.gold-chain\",
        \"DetailType\": \"chain-complete\",
        \"Detail\": \"{\\\"chain_label\\\": \\\"$CHAIN_LABEL\\\", \\\"completed_at\\\": \\\"$(log_ts)\\\", \\\"scripts\\\": \\\"$SCRIPT_IDS\\\", \\\"mode\\\": \\\"$MODE\\\", \\\"exit_code\\\": $EXIT_CODE}\",
        \"EventBusName\": \"default\"
      }]"
    }
    ```

    Hook it into the success path. Failed chains do NOT emit (downstream consumers should not run on partial chain).

    **IAM addition (HARD GATE — runs before script edit):** `events:PutEvents` permission on `default` event bus must be added to the `bd-gold-layer-runner` (PROD) AND `bd-gold-qa-runner` (QA) IAM role/instance profile. If the runners share an IAM role, single update; if not, both. Confirm via `comp-iam service` before editing the dispatcher.

    Future-proof: structured detail payload extends to any downstream Lambda filtering by `detail.mode` (full vs incremental), `detail.chain_label`, etc.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/iam.tf (add events:PutEvents to gold runner role)</file>
    </files>
  </scope>

  <wire_contract>
    EventBridge default bus receives one event per successful chain close: `Source=bd-pipeline.gold-chain`, `DetailType=chain-complete`, `Detail={chain_label, completed_at, scripts, mode, exit_code}`. Failed chains emit nothing. Downstream Lambdas (ADVI_49EXEC.007 first consumer; future v2 Lambdas TBD) filter by source + detail-type + optional detail.mode.
  </wire_contract>

  <acceptance_criteria>
    1. `emit_chain_complete()` helper added to gold_dispatch.sh; called only on success path.
    2. IAM `events:PutEvents` on default bus added to gold runner role(s); `comp-iam service` shows zero MISSING for events action.
    3. `bash -n` exits 0.
    4. Tested via `--single S_00 --dry-run` mode: emit function NOT invoked (dry-run path skips emission).
    5. Tested via real chain close (could be tonight's 04:00 UTC nightly OR a manual `--single S_00` on QA runner): EventBridge event observable in CloudWatch (use `aws events list-rules` + a temporary capture rule for verification, OR check cloudtrail).
    6. Failed chain (artificially injected exit code != 0): no emission (verify via dry-run injection + grep helper invocation).
    7. Terraform 0-diff after iam.tf apply.
    8. Tag `bd-v2.24.2` (next patch in series after bd-v2.24.1) created + pushed `--follow-tags`.
    9. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    10. Rule 7 pre-flag MCP to CTO+COO BEFORE `aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/gold/gold_dispatch.sh` (this is A→D-rerun-sensitive surface).
    11. MCP COMPLETE to COO + CTO with: tag, etag, Terraform diff, sample EventBridge event payload.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws iam list-attached-role-policies --role-name {bd-gold-layer-runner role name}</run>
        <expect>Current policies enumerated; identify which policy ARN to extend with events:PutEvents.</expect>
        <if_mismatch>Locate the actual role.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service bd-gold-layer-runner</run>
        <expect>events:PutEvents currently MISSING (this TO will add it).</expect>
        <if_mismatch>If already present, scope narrows to dispatcher edit only.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'CHAIN_LABEL\|MODE\|SCRIPT_IDS\|EXIT_CODE\|exit_handler\|trap' data/black_diamond/scripts/runner/gold_dispatch.sh | head -10</run>
        <expect>End-of-chain hook site identified; variables available for the emit function.</expect>
        <if_mismatch>Re-baseline hook site.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>Adds events:PutEvents to gold runner role policy; no other unintended drift.</expect>
        <if_mismatch>Investigate.</if_mismatch>
      </step>
      <step>
        <run>terraform apply</run>
        <expect>Apply success.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>0-diff post-apply.</expect>
        <if_mismatch>Drift; fix before tag.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service bd-gold-layer-runner</run>
        <expect>events:PutEvents now present; zero MISSING for events action.</expect>
        <if_mismatch>Patch iam.tf.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new gaps elsewhere.</expect>
        <if_mismatch>Audit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="before S3 upload — RULE 7 PRE-FLAG MANDATORY">
      <step>
        <run>MCP send_message to 1.0.0_SA_CTO + 2.0.0_SA_COO subject "ACCEPTANCE FLEX / RULE 7 PRE-FLAG — DH-7 gold_dispatch.sh upload (chain-complete EB emission)" body cites commit + IAM update + 60-sec don't-object window</run>
        <expect>Pre-flag delivered. Wait 60 seconds. No CTO objection.</expect>
        <if_mismatch>HOLD upload, resolve.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/gold/gold_dispatch.sh &amp;&amp; aws s3api head-object --bucket opal-data-bd --key code/gold/gold_dispatch.sh --query ETag</run>
        <expect>Upload success; ETag matches local md5.</expect>
        <if_mismatch>Retry.</if_mismatch>
      </step>
    </phase>
    <phase id="4" when="after commit + first real chain close">
      <step>
        <run>aws events list-rules --event-bus-name default | grep chain-complete (or temp rule + cloudwatch capture for verification)</run>
        <expect>Event observable post-04:00 UTC chain close.</expect>
        <if_mismatch>Investigate emit function silently failing or IAM gap.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Gates `ADVI_49EXEC.007` (DT EventBridge wiring of `exec-summary-generator` Lambda).
    - bd-pipeline IAM owned by AE; no DT/DS conflict.
    - Tonight's 04:00 UTC nightly chain is the first natural fire to verify emission.
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_ROLLUP.DH-1" description="DH-1 chain definitions land first (clean end-of-chain identification post-rename)" status="complete"/>
  </dependencies>

  <next>
    DH-7 close → unblocks ADVI_49EXEC.007 (DT can write the EventBridge rule pattern matching this signal). Future v2 downstream Lambdas filter by source + detail.mode.
  </next>
</task_order>
