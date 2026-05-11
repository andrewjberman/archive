<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_INFRUNNERPARITY</id>
    <project>ADHC_INFRUNNERPARITY</project>
    <title>inf-gold-layer-runner boot dispatcher parity with bd-gold-layer-runner — codify the out-of-band-installed `run-gold-layer.sh` + systemd unit into repo + S3; close the AMI-rebuild-loses-dispatcher risk</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~3-4h (live probe + author + Terraform + S3 upload + AMI rebuild verification + memory entry)</estimated_effort>
    <authorized_by>2.0.0_SA_COO 2026-05-11 (drift surfaced by AE 0.7 runner code-sync audit RAVC2 same-day)</authorized_by>
  </metadata>

  <references>
    <ref type="parent_audit">AE 0.7 runner code-sync audit 2026-05-11 — `inf-gold-layer-runner` (i-0ed5afded2ebd4ed4) directory in repo contains NO `run-gold-layer.sh`; bd-gold-layer-runner has `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh` + systemd unit baked via user-data.sh; INF empirically dispatches but the dispatcher script lives on EBS, out-of-band</ref>
    <ref type="reference_pattern">bd-gold-layer-runner: `infra/aws/ec2/bd-gold-layer-runner/{run-gold-layer.sh, user-data.sh, watchdog-shutdown.sh}` — canonical pattern</ref>
    <ref type="inf_state">inf-gold-layer-runner: `infra/aws/ec2/inf-gold-layer-runner/{RUNBOOK.md, user-data.sh, watchdog-shutdown.sh}` — missing run-gold-layer.sh</ref>
    <ref type="memory_entry">`feedback_gold_runner_pull_mechanism_s3.md` (AE 0.7, 2026-05-11) — documents the S3-pull architecture this TO codifies for INF</ref>
    <ref type="live_probe_cmd">aws ssm send-command --instance-ids i-0ed5afded2ebd4ed4 --document-name AWS-RunShellScript --parameters 'commands=["systemctl list-units --type=service --all | grep -i gold","ls /home/ec2-user/inf-gold-layer/scripts/ 2>/dev/null","cat /etc/systemd/system/*.service 2>/dev/null | grep -B1 -A5 ExecStart"]'</ref>
  </references>

  <context>
    The `inf-gold-layer-runner` empirically dispatches the gold chain when its trigger Lambda starts the EC2 — but the source of truth for HOW it dispatches lives on EBS, not in the repo. AE 0.7's audit confirmed:

    - `inf-gold-trigger` Lambda only writes `trigger-mode.json` + calls `ec2.start_instances(i-0ed5afded2ebd4ed4)` — does NOT send any SSM command
    - The EBS-resident dispatcher script + systemd unit handle boot-time chain orchestration
    - Repo's `infra/aws/ec2/inf-gold-layer-runner/user-data.sh` (46 lines) only installs `dnf` packages + watchdog timer — NO dispatcher wiring

    **Configuration management gap.** Working state lives on EBS, persists across stop/start, originated from prior SSM commands. If the AMI is ever rebuilt or the EBS volume replaced, the dispatcher is lost. Silent recovery is impossible without re-running the original (undocumented) SSM commands.

    The bd-gold-layer-runner closes this gap properly: `run-gold-layer.sh` lives in repo + ships via user-data.sh + persists in the AMI build pipeline. This TO ports that pattern to INF.

    **Why medium priority** — the gap doesn't bite TODAY (runner works empirically). It bites the day an AMI rebuild or volume swap happens. Low probability per unit time, high impact per occurrence. Standard config-drift remediation.
  </context>

  <scope>
    <step>
      **Live probe (when instance is running).** SSM the canonical inspection command:
      ```
      aws ssm send-command --instance-ids i-0ed5afded2ebd4ed4 \
        --document-name AWS-RunShellScript \
        --parameters 'commands=["systemctl list-units --type=service --all | grep -i gold","ls /home/ec2-user/inf-gold-layer/scripts/ 2>/dev/null","cat /etc/systemd/system/*.service 2>/dev/null | grep -B1 -A5 ExecStart","cat /home/ec2-user/inf-gold-layer/scripts/*.sh 2>/dev/null","find / -name run-gold-layer.sh 2>/dev/null"]'
      ```
      Capture the live dispatcher script + systemd unit + any helper scripts. This is the ground truth.

      Coordinate with DS or chain-trigger window — instance only running during active dispatch. If genuinely blocked, can start instance via `aws ec2 start-instances` for the probe + immediately stop after (~5min cost).
    </step>

    <step>
      **Author `infra/aws/ec2/inf-gold-layer-runner/run-gold-layer.sh`.** Mirror the bd pattern. Adapt paths:
      - bd: `s3://opal-data-bd/code/runner/` for dispatcher + `s3://opal-data-bd/code/gold/` for chain scripts
      - inf: `s3://opal-data-inf/code/runner/` (NEW PREFIX, may need creation) + `s3://opal-data-inf/code/gold/` for chain scripts

      Key behaviors to preserve:
      - Self-update from S3 at boot (the dispatcher pulls itself)
      - Read `trigger-mode.json` from S3
      - Dispatch the chain via aws s3 sync gold/ + invoke per-script per dispatch order
      - Fire `sudo shutdown -h` on completion
      - Coordinate with watchdog systemd timer (already in repo)

      Diff against live-probe output from Step 1 to ensure no drift.
    </step>

    <step>
      **Add systemd unit to `infra/aws/ec2/inf-gold-layer-runner/user-data.sh`.** Mirror bd's pattern. Make sure the unit:
      - Triggers on boot
      - Pulls `run-gold-layer.sh` from S3 to disk at boot
      - Exec's it
      - Logs to journalctl with grep-able tag

      Idempotent under stop→start cycles.
    </step>

    <step>
      **Upload `run-gold-layer.sh` to `s3://opal-data-inf/code/runner/`** — create the prefix if needed. SSE-AES256 default per memory `feedback_lambda_zip_layout_and_layer_attribution.md` pattern.

      Use safe upload pattern (mechanical `aws s3 cp` + SHA verify; comp-pipescript INF coverage is being fixed by DSFLOW.005 in parallel — until then, manual hashlib check).
    </step>

    <step>
      **Terraform changes if any.** Check `infra/aws/terraform/inf-pipeline/` (or wherever the inf-gold-layer-runner ec2 + IAM is defined). If user-data.sh is templated via Terraform, update there. Otherwise, plain-text userdata update is sufficient.

      Run `terraform plan` from `.tools/terraform.exe` (Windows binary per memory). Expect minimal diff (user-data hash change only). If module-level state issues surface, RAVC1 for direction before applying.

      If 0-diff plan: `terraform apply` to write the new user-data into AWS launch templates. EXISTING instance stays untouched — next stop→start will pick up new user-data via standard AWS behavior (or instance refresh if Auto Scaling Group involvement).

      Tag per protocol: `inf-pipeline-v{X.Y.Z}` or similar.
    </step>

    <step>
      **Verification via AMI rebuild simulation.** Stop existing instance (after current chain run), start it — confirms new user-data path provisions the dispatcher correctly. New boot should match prior behavior; chain dispatch should fire on next `inf-gold-trigger` Lambda invocation.

      If safe to do (off-cycle, no PROD dispatch in flight): manually invoke `inf-gold-trigger` Lambda with a test payload + observe `trigger-mode.json` write + EC2 start + chain log to `s3://opal-data-inf/gold/meta/pipeline-complete.json` lands.

      RAVC the empirical chain-success vs prior baseline.
    </step>

    <step>
      **Update memory entry `feedback_gold_runner_pull_mechanism_s3.md`** (AE 0.7's entry) to remove the "INF parity gap" inline note and replace with "INF parity remediated via ADHC_INFRUNNERPARITY 2026-{date}; pattern now matches bd-gold-layer-runner".

      Add a paragraph documenting the live-probe-then-codify pattern for future drift remediation (standing operational pattern).
    </step>

    <step>
      **Commit + push + RAVC.**
      - Bundle: new run-gold-layer.sh + user-data.sh update + Terraform diff + memory entry update
      - Author: `0.7.0_AE_CloudOps`
      - RAVC payload: live-probe output, diff vs codified version (parity confirmation), Terraform plan/apply outcome, AMI rebuild simulation results
    </step>
  </scope>

  <acceptance_criteria>
    1. **Live probe captured.** Empirical dispatcher script + systemd unit recorded in session log.
    2. **`run-gold-layer.sh` authored** in repo `infra/aws/ec2/inf-gold-layer-runner/`; diff against live-probe = no drift.
    3. **user-data.sh updated** with systemd unit; idempotent under stop→start.
    4. **S3 deploy** to `s3://opal-data-inf/code/runner/`; manual SHA verify.
    5. **Terraform 0-diff plan** post-apply OR documented diff if user-data is templated.
    6. **AMI rebuild simulation PASS** — stop→start picks up new user-data; chain dispatch fires correctly on next trigger.
    7. **Memory entry updated** to reflect remediation.
    8. **RAVC delivered** with empirical chain-success evidence.
  </acceptance_criteria>

  <blocking>
    **Blocked by:** ADHC_DSFLOW.005 completion (per AE 0.7's existing queue plan). DSFLOW.005's comp-pipescript INF coverage fix is helpful here — uses the new INF coverage to verify run-gold-layer.sh S3 deploy.

    **Coordination:** Live probe (Step 1) requires the instance running. Can opportunistically piggyback on the next chain dispatch (likely tomorrow ~06:00 UTC per `inf-gold-trigger` EventBridge cron) OR start manually for the probe.

    **No DS dependency.** Pure AE infrastructure work.
  </blocking>

  <notes>
    **Why codify what's empirically working:** the gap is a known unknown today. Tomorrow it's a discovery-during-incident — and the discovery cost is much higher when something else has gone wrong (AMI rebuild during incident response, EBS volume corruption recovery, etc.).

    **Pattern this represents:** "out-of-band-installed-config persists empirically until it doesn't." Same family as the V4.024 synthetic-workspace-fixture pattern and the regression-guard-alongside-correctness-fix meta-pattern: codify the working state in repo so the next state-loss is recoverable.

    **Not in scope:** changing the chain dispatch behavior, the trigger Lambda, the watchdog timer, or the `inf-gold-qa-runner` configuration. This TO is purely about codifying the existing boot dispatcher.

    **Live-probe-then-codify approach is the safest:** ensures the codified version matches empirical behavior exactly. Don't guess at what the EBS-resident script does; capture it directly.
  </notes>
</task_order>
