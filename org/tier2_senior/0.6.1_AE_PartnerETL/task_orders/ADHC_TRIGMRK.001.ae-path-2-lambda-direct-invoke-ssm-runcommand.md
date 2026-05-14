# TO `ADHC_TRIGMRK.001` — Path 2 Lambda direct-invoke SSM Run Command (abandon marker pattern)

| Field | Value |
|---|---|
| **Project** | `ADHC_TRIGMRK` (Trigger-Marker Race-Surface Mitigation) |
| **Owner** | `0.6.1_AE_PartnerETL` |
| **Lane** | AE / inf-pipeline / Lambda + EC2 + SSM + Terraform |
| **Status** | `staged` — dispatch_held=true; gates on COO per-TO dispatch GO |
| **Dispatch_held** | `true` — pending COO dispatch GO post-TO RAVC1 close |
| **Effort** | ~4-6h wall (Path 2 Lambda full rewrite + IAM + TF + boot-script + deploy + AC sweep) |
| **PRD** | `docs/architecture/ADHC_TRIGMRK.md` v0.3 canonical (`f91c79c35` ratified Path 2; T1-T8 folded; AC1-AC14) |

---

## Goal

Eliminate the silent-failure surfaces in the Inflection gold-chain trigger contract by abandoning the producer/marker/consumer triangulation entirely. Replace `inf-gold-trigger` Lambda's S3 marker-write pattern (which has no consumer daemon when EC2 is running) with direct Lambda → SSM Run Command dispatch. Single producer/consumer pair; race surfaces #1 + #2 + auxiliary `source` provenance issue all collapse.

Per PRD §3.2 Path 2 ratified by CTO 18:50Z. Per CTO verbatim: *"The marker pattern was designed for a daemon that ops never built; rather than build the daemon to satisfy the pattern, abandon the pattern."*

---

## Pre-write Phase

Mandatory before writing code (per CLAUDE.md compiler-tools directive):

1. `comp-pipescript deployed inf-gold-trigger` — baseline current Lambda code SHA-MATCH against committed `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py`. Confirm no out-of-band edits.
2. `comp-iam service inf-gold-trigger` — baseline current IAM ops. Expected: `s3:PutObject` on `gold/trigger-*.json`, `ec2:DescribeInstances`, `ec2:StartInstances`. Path 2 will EXTEND not replace this set.
3. `comp-blast inf-gold-trigger` — downstream consumers. Confirm no consumer expects current S3 marker writes (per PRD §2.2 SSM diagnostic; daemon doesn't exist).
4. `comp-routes trace inf-gold-trigger` — full invocation-path map (EventBridge cron + S3 aggregator + direct invoke). Each path must be handled by new `detect_invocation_source(event)` helper.

Optional but recommended:
- Read `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-boot-dispatch.sh` to map current cold-start marker-read flow before removal.
- Read `infra/aws/terraform/inf-pipeline/eventbridge.tf` to identify `inf-canonical-prices-daily` rule for retry-policy attribute add (AC13).

---

## Scope (Path 2 LOCKED per PRD §3.2 + CTO 18:50Z architectural ratify)

### Lambda source (full rewrite)

- `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py` — ~120 LOC replacing existing ~80 LOC marker-writing logic
- New helpers:
  - `detect_invocation_source(event) -> str` per PRD §3.6 table (cron / direct / s3-event / sns / unknown)
  - `mode_aware_ttl(mode) -> int` per PRD §3.2 + AC6: `gold-d` 1200, `full` 5400, `incremental` 900, fallback 1800 (seconds)
  - `acquire_dispatch_lock(mode, source, ttl)` — S3 conditional-put on `s3://opal-data-inf/gold/dispatch-lock.json` with `If-None-Match: "*"` atomic acquire; deletes stale lock older than TTL before fresh acquire; returns lock object with `held_by_other: bool` + `run_id: str`
  - `wait_for_instance_running(instance_id, timeout=120)` — poll `ec2:DescribeInstances` for state=running
  - `wait_for_ssm_agent_online(instance_id, timeout=60)` — poll `ssm:DescribeInstanceInformation` for instance present + PingStatus=Online
- New main flow per PRD §3.2 pseudocode:
  1. Validate event payload `mode` (required; reject if missing or not in {full, gold-d, incremental, gold-a, gold-b, gold-c})
  2. `detect_invocation_source(event)`
  3. `ec2:DescribeInstances` for `inf-gold-layer-runner`
  4. Branch on EC2 state:
     - `stopped` → `ec2:StartInstances` + `wait_for_instance_running` + `wait_for_ssm_agent_online`; on timeout return 503
     - `running` → proceed directly
     - else (pending / stopping / shutting-down / terminated) → return 503 with body `f"EC2 in transitional state {state}; retry shortly"`
  5. `acquire_dispatch_lock(mode, source, ttl)`; if `held_by_other` → return 409 with body `f"Chain {lock.run_id} in flight; reject"`
  6. `ssm:SendCommand` AWS-RunShellScript with commands:
     ```bash
     aws s3 cp s3://opal-data-inf/code/gold/orion-gold-dispatch.sh /tmp/orion-gold-dispatch.sh
     bash /tmp/orion-gold-dispatch.sh --chain {mode} --bg
     ```
  7. On `ssm:SendCommand` success: `ssm:PutParameter` writes `/inf/gold/last-trigger-mode` with new mode value (T4: AFTER CommandId return, NOT before)
  8. Return 200 with body `{command_id, mode, source, lock_run_id, instance_id, ssm_send_command_returned_at}`

### Terraform

- `infra/aws/terraform/inf-pipeline/lambdas.tf` — `inf-gold-trigger` Lambda resource: bump source code SHA, no resource-level changes unless memory/timeout needs upsizing (current sizing TBD via baseline grep; if undersized, set `memory_size = 256` + `timeout = 60` per PRD §7 Phase 2 sizing per CTO Rule 5 deliberation)
- `infra/aws/terraform/inf-pipeline/iam.tf` — `inf-gold-trigger` execution-role policy attachment EXTENDS:
  - `ssm:SendCommand` scoped to **specific instance ARN** `arn:aws:ec2:us-east-1:313476888478:instance/i-0ed5afded2ebd4ed4` (NO wildcard per AC14)
  - `ssm:SendCommand` document scope: `arn:aws:ssm:us-east-1::document/AWS-RunShellScript`
  - `ssm:DescribeInstanceInformation` (for SSM agent online poll)
  - `ssm:PutParameter` scoped to `arn:aws:ssm:us-east-1:313476888478:parameter/inf/gold/last-trigger-mode`
  - `s3:PutObject` + `s3:GetObject` + `s3:DeleteObject` scoped to `arn:aws:s3:::opal-data-inf/gold/dispatch-lock.json` (for atomic-conditional-put + stale-clear)
  - Existing `ec2:DescribeInstances` + `ec2:StartInstances` retained
- `infra/aws/terraform/inf-pipeline/eventbridge.tf` — `inf-canonical-prices-daily` cron target (existing) gains:
  - `dead_letter_config { arn = aws_sqs_queue.inf_gold_trigger_dlq.arn }` (NEW SQS queue resource for DLQ)
  - `retry_policy { maximum_event_age_in_seconds = 60, maximum_retry_attempts = 0 }` per AC13
- `infra/aws/terraform/inf-pipeline/eventbridge.tf` — NEW `aws_sqs_queue.inf_gold_trigger_dlq` resource for AC13 DLQ; minimal config (no FIFO, 14d retention, KMS opal-data-inf bucket key for encryption)
- `infra/aws/terraform/inf-pipeline/main.tf` (or new `ssm.tf` if pattern matches existing pipeline structure) — NEW `aws_ssm_parameter.inf_gold_last_trigger_mode` resource:
  ```hcl
  resource "aws_ssm_parameter" "inf_gold_last_trigger_mode" {
    name  = "/inf/gold/last-trigger-mode"
    type  = "String"
    value = "full"  # bootstrap value; Lambda overwrites on every successful dispatch
    lifecycle {
      ignore_changes = [value]  # Lambda owns; Terraform creates + tags only
    }
    tags = {
      System = "InflectionPipeline"
      Owner  = "inf-gold-trigger-lambda"
    }
  }
  ```

### EC2 boot script

- `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-boot-dispatch.sh` — REMOVE marker-read code path; REPLACE with SSM Parameter fallback:
  ```bash
  # OLD (removed):
  # if [ -f /tmp/inf-trigger-mode.json ]; then mode=$(jq -r .mode /tmp/inf-trigger-mode.json); fi
  
  # NEW:
  # SSM Parameter holds most recent successfully-dispatched mode (Lambda writes
  # post-SendCommand-return per ADHC_TRIGMRK Path 2). Cold-start replay reads
  # this to resume the chain mode if the SSM SendCommand from Lambda doesn't
  # land first (rare; defense-in-depth).
  mode=$(aws ssm get-parameter --name /inf/gold/last-trigger-mode --query 'Parameter.Value' --output text 2>/dev/null || echo "full")
  ```
- Deploy via `safe-ec2-deploy.sh inf-gold-layer-runner deploy.sh` per Rule 12; EC2_MANIFEST.json updated with new script artifact_sha256 + last_deployed_at

### Pre-deploy marker sweep (manual step in deploy runbook)

Documented in `org/tier2_senior/0.6.1_AE_PartnerETL/runbooks/inf-gold-trigger-path-2-deploy.md` (NEW; part of this TO):
```bash
# Pre-deploy sweep: drain in-flight markers per PRD §3.5
aws s3 rm s3://opal-data-inf/gold/trigger-mode.json
aws s3 rm s3://opal-data-inf/gold/trigger-pending.json
# Verify post-sweep:
aws s3 ls s3://opal-data-inf/gold/trigger-*.json  # expect 0 results
```
Timing: immediately before `terraform apply` lands new Lambda + boot-script update.

### Source-map registration (Rule 4)

- New entry OR updated entry in `infra/aws/lambda/ci/lambda-source-map.json` for `inf-gold-trigger`:
  ```json
  "inf-gold-trigger": {
    "source_dir": "infra/aws/lambda/inf-pipeline/inf-gold-trigger",
    "files": ["lambda_function.py"],
    "tf_file": "infra/aws/terraform/inf-pipeline/lambdas.tf",
    "tf_resource": "aws_lambda_function.inf_gold_trigger",
    "artifact_s3_key": "inf-pipeline/inf-gold-trigger.zip",
    "iam_role": "inf-gold-trigger-role"
  }
  ```
  Plus `last_deployed_commit` + `last_deployed_at` + `artifact_sha256` populated by `record-terraform-deploy.sh` on first deploy.

### Deploy cycle (CLAUDE.md Rules 1-6 + 11)

1. Write Lambda source — `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py` (Path 2 full rewrite)
2. Write Terraform — `lambdas.tf` SHA bump + `iam.tf` extension + `eventbridge.tf` retry-policy + NEW `aws_ssm_parameter` + NEW `aws_sqs_queue` DLQ
3. Build zip + upload to S3 — `./infra/aws/terraform/inf-pipeline/build-and-upload.sh` (existing pipeline tooling; per Rule 3 inf-pipeline doesn't use Layers for the trigger Lambda since no external deps)
4. Update source-map per `record-terraform-deploy.sh` OR manual edit
5. **PRE-DEPLOY MARKER SWEEP** — `aws s3 rm s3://opal-data-inf/gold/trigger-*.json` per §3.5
6. `safe-commit.sh --author="0.6.1_AE_PartnerETL <...>" ...` — atomic commit with Lambda source + Terraform + source-map + boot-script
7. `terraform plan -out=inf-trigmrk-v1.tfplan` — expect: Lambda SHA change + IAM policy extension + EventBridge retry-policy/DLQ add + new SSM Parameter + new SQS queue
8. `terraform apply inf-trigmrk-v1.tfplan` — verify ApplyComplete
9. Re-run `terraform plan` — verify 0-diff (Rule 11)
10. Deploy boot-script via `safe-ec2-deploy.sh inf-gold-layer-runner deploy.sh`
11. Tag: `git tag -a inf-v{X.Y.Z+1} -m "feat(inf-trigger): Path 2 Lambda direct-invoke SSM Run Command (ADHC_TRIGMRK.001)"` per Rule 6 (check `git tag -l "inf-v*" | sort -V | tail -5` for next version before tagging)
12. Push with `--follow-tags`
13. Post-deploy: `comp-iam service inf-gold-trigger` exits 0 verification (AC14)

---

## Acceptance Criteria

Per PRD §4 (v0.3 canonical at `docs/architecture/ADHC_TRIGMRK.md`) — all AC1-AC14 must PASS for RAVC2 close.

| AC | Verification step in this TO |
|----|------------------------------|
| **AC1** | Hot-state Lambda invoke test → SSM CommandId populated ≤30s, chain fires ≤60s, dispatch-lock acquired |
| **AC2** | Cold-state Lambda invoke test (EC2 manually stopped first) → `wait_for_*` succeeds; chain fires ≤180s |
| **AC3** | Double-invoke test (`aws lambda invoke` twice in <5s) → second returns 409 with `run_id` cite |
| **AC4** | Stale-lock simulation: PUT `dispatch-lock.json` with `started_at` >TTL-old → next invoke clears + re-acquires |
| **AC5** | Transitional-state simulation: invoke during `pending` (post-StartInstances pre-running) → 503 returned |
| **AC6** | Mode-aware TTL table verified via lock `ttl_seconds` field on each mode invoke |
| **AC7** | Direct `aws lambda invoke` → response body `source: "direct"`; CW Log structured entry matches |
| **AC8** | EventBridge `inf-canonical-prices-daily` cron fire (next 06:00 UTC OR forced via `aws events put-events`) → `source: "cron"` |
| **AC9** | S3 aggregator simulation: PUT `silver/_silver_complete/2026-05-15/positions_v2.json` → aggregator → trigger; `source: "s3-event-..."` |
| **AC10** | Post-deploy `aws s3 ls s3://opal-data-inf/gold/trigger-*.json` returns empty (DRAIN successful). SSM Parameter verified: invoke Lambda mode=gold-d → Parameter reads "gold-d"; invoke twice (second 409) → Parameter unchanged |
| **AC11** | Regression scenario reproduction: stop EC2 + wait >10min + `aws lambda invoke {mode:"gold-d"}` → chain TERMINAL within ≤300s; no manual SSM-direct workaround |
| **AC12** | `aws ssm list-commands --instance-id i-0ed5afded2ebd4ed4 --filters "key=Status,value=Success"` returns recent commands with Comment containing mode + invocation_source + lock_run_id |
| **AC13** | EventBridge double-fire simulation: 2× `put-events` for `inf-canonical-prices-daily` in <5s → second returns 409 → CloudWatch shows 0 retry attempts; SSM list-commands has 1 entry not 2 |
| **AC14** | Post-deploy `comp-iam service inf-gold-trigger` exits 0; output shows no MISSING permissions; `ssm:SendCommand` resource ARN matches the single instance ARN (no wildcard) |

Empirical regression test scripts staged at `.runtmp/ae_06_1_trigmrk_ac_sweep.py` (NEW; this TO's ship gate).

---

## RAVC Posture

- **RAVC1:** TO authored 2026-05-14 ~19:20Z (this file)
- **RAVC2:** dispatch_held=true until CTO RAVC1 close on TO-001 against 7 criteria + COO per-TO dispatch GO
- **RAVC3:** TO progresses on dispatch; AE 0.6.1 ships per CLAUDE.md Rules 1-6 + 11 + 12 + 14a
- **RAVC4:** ship evidence packet to COO (commit hash, tag `inf-v{X.Y.Z+1}`, terraform plan 0-diff, comp-iam post-deploy gate, AC1-AC14 empirical PASS evidence)
- **RAVC5:** COO acceptance gates final RAVC close

---

## Risks + Mitigations

Per PRD §5 (Path 2 risk surface). Highlights:

- **SSM agent offline** — `wait_for_ssm_agent_online` 60s timeout + 503 return + CW alarm on 503-rate>0
- **IAM denial** — `comp-iam service inf-gold-trigger` AC14 verifies post-deploy; scoped to single instance ARN
- **Lock TTL race** — atomic S3 conditional-put with `If-None-Match: "*"`
- **Backward-compat in-flight markers** — pre-deploy DRAIN sweep + boot-script atomic update + SSM Parameter cold-start fallback
- **Rollback** — `git revert` Lambda commit + `terraform apply` reverts in ~10min; SSM Parameter remains orthogonal artifact

---

## Compliance Notes

- **CLAUDE.md Rule 1** (Terraform-only Lambda deploy) — YES (no `aws lambda update-function-code`)
- **CLAUDE.md Rule 2** (Commit before apply) — YES (safe-commit pre-`terraform apply`)
- **CLAUDE.md Rule 3** (Deps in Layers) — N/A for trigger Lambda (no external Python deps beyond stdlib + boto3 baked into runtime)
- **CLAUDE.md Rule 4** (Source-map registered) — YES (existing entry updated OR new entry per inventory)
- **CLAUDE.md Rule 5** (Lambda sized deliberately) — confirm or bump to 256MB/60s per Path 2 wall budget (SSM agent online poll + StartInstances wait can hit ~90s end-to-end in cold-start)
- **CLAUDE.md Rule 6** (Tag after deploy) — YES (`inf-v{X.Y.Z+1}` with `git push --follow-tags`)
- **CLAUDE.md Rule 11** (Verify parity 0-diff) — YES
- **CLAUDE.md Rule 12** (S3 artifact model for EC2 code) — YES (boot-script deployed via `safe-ec2-deploy.sh` S3-pull path)
- **CLAUDE.md Rule 14a** (`safe-commit.sh` per ADHC_OWNPTH.007) — YES (atomic commit with all Path-2 artifacts in pathspec)
- **No emojis in code** (CLAUDE.md "Code Quality") — ASCII only; no Unicode above U+007F in Lambda handler / boot-script / logs

---

## Cross-references

- **PRD:** `docs/architecture/ADHC_TRIGMRK.md` v0.3 canonical (`f91c79c35`; Path 2 ratified; T1-T8 folded; AC1-AC14)
- **Sister AE TO (cross-pipeline):** `ADHC_LEDGEH.001` (AE 0.7 lane; defense-in-depth pair; ships independently)
- **Sister compiler-tool TO:** `ADHC_COMPIL_V4.030 comp-blast --check-consumers` flag extension (retitled per CTO+COO 19:0XZ; commit `a1138700a`; structurally detects phantom-consumer pattern post-deploy via CI)
- **Empirical anchor memory entry:** `[[feedback_lambda_pending_marker_no_daemon]]` (DS~D-authored; 3-evidence-point contrast triple: HOT silent / SSM-direct clean / COLD Lambda clean)
- **Phantom-consumer pattern memory entry:** `[[feedback_phantom_consumer_marker_pattern]]` (COO-authored 11-entry batch; AE provides empirical content)
- **SSM-direct fallback runbook:** `[[reference_inf_ssm_direct_single_script_runbook]]` (canonical pre-Path-2; post-Path-2-ship becomes documented fallback for emergency manual dispatch)
- **Owned-paths cross-lane workflow precedent:** `[[feedback_drafts_delta_canonical_apply_pattern]]` (COO-authored 13th batch entry; AE drafts delta `e9eba80a4` → CTO canonical apply `f91c79c35`)

---

## Versioning

- **v0.1** — 2026-05-14 ~19:20Z — initial author; staged + dispatch_held=true; gates on CTO RAVC1 close + COO per-TO dispatch GO

---

## Sister project coordination

`ADHC_COMPIL_V4.030 comp-blast --check-consumers` ships in parallel via COO v0.5 batch (commit `a1138700a` retitle). Together with this TO:
- TRIGMRK.001 = operational fix (Path 2 Lambda direct-invoke; eliminates the phantom-consumer at the trigger surface)
- COMPIL_V4.030 = diagnostic tool (CI integration detects phantom-consumer pattern at design-time pre-deploy)

If TO ships first, comp-blast --check-consumers can retroactively scan for other phantom-consumer surfaces (Lambda producers writing markers no consumer reads). Pre-commit hook integration suggested by COO for full discipline coverage.

**Defense-in-depth posture:** TO-001 closes today's empirical anchor; .030 prevents reintroduction at design-time.

---

## Phase mapping (PRD §7)

| Phase | This TO scope | Wall |
|-------|--------------|------|
| Phase 1 — PRD ratify | DONE (v0.3 CANONICAL `f91c79c35`) | — |
| **Phase 2 — TO-001 Path 2 Lambda rewrite** | **THIS TO scope** | **~4-6h** |
| Phase 3 — Acceptance regression sweep | AC1-AC14 empirical PASS (this TO's RAVC5 gate) | ~2.5h |
| Phase 4 — PROD deploy + Andrew UAT | Standard Lambda Deployment Sequence + `safe-ec2-deploy.sh` + `inf-v{X.Y.Z}` tag | ~1h |
| Phase 5 — Memory + cross-ref cleanup | Mark `[[feedback_lambda_pending_marker_no_daemon]]` RESOLVED post-deploy; update `[[reference_inf_ssm_direct_single_script_runbook]]` to note canonical-via-Lambda; cross-reference `[[feedback_phantom_consumer_marker_pattern]]` + `[[feedback_drafts_delta_canonical_apply_pattern]]` | ~30min |
