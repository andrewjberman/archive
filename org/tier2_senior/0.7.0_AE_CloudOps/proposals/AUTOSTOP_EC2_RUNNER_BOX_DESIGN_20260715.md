# Auto-start/stop EC2 runner box -- design (S2 ruling 2, Andrew-ratified)

**Author:** 0.7.0_AE_CloudOps | **Date:** 2026-07-15 | **Status:** DESIGN for CTO review -- NO APPLY.
**Authority:** Andrew S2 ruling 2 (~16:5xZ, "Agreed with your rec"), COO dispatch 170100Z. Every apply
rides CTO's gate. **NEW-TERRITORY RULE binds: pure to-add, nothing existing modified.**
**Inputs folded (per COO 170318Z):** D4 connector census (what runs on it), W3 trigger/schedule census
(start mechanism), W2 cost profile (sizing). **rust/polars deferred to Wave-3.**

---

## 1. Purpose -- the EC2 branch of the chunking decision, made concrete

The chunking-lambda architecture (docs/architecture/chunking_lambda_architecture.md Section 6) routes to
**ephemeral auto-start/stop EC2** any heavy process that either (a) is not incrementally chunkable, or
(b) is chunkable but still fails the silver envelope (peak >= 3008 MB no-headroom, or wall >= 600 s), or
(c) is analytics-class that Andrew ruled stays on EC2 for stability (gold runners). This box is that
branch's landing pad for the CONSOLIDATION runner architecture (OPAL_RUNNERS, now re-parented into
OPAL_CONSOLIDATION) -- a single small, ephemeral compute runner that boots on demand, runs one
S3-delivered job, ships its output+logs, and stops itself.

**What it hosts (grounded in D4 + consolidation build plan; the exact host-list rides the consolidation
TOs):** the 49F gold-runner class (thin-A dims / B lots-union / C ports / D publishers per
OPAL_RUNNERS_49F_BUILD_PLAN.md) and any heavy backfill that fails the Lambda envelope (D4 G9 class: a
sweep/backfill whose per-run cost exceeds the 600 s Lambda ceiling). It does NOT replace the existing
per-firm runners (bd-gold-layer-runner, canonical-schwab-runner) -- it is the consolidation's own vehicle,
modeled on them.

**Not in scope (stated):** rust/polars acceleration (Wave-3); any modification to existing buckets,
schedulers, notification configs, or runners (new-territory); the gold job code itself (DS lane).

**Runner-class assumption (Andrew RULING 6, ~17:1xZ, relayed COO 171237Z -- binds this design):** the
consolidation gold-runner class is the STANDARD build (thin-A dims / B lots-union / C ports / D
publishers), NOT a remediation-heavy workstream. Specifically the 1,843 unbridged accounts are a
**mechanical BINARY no-fee column** (dim row exists or not; the vendor-gap-vs-not-fee-paying "why" is
ruled UNKNOWABLE -- no inference anywhere), so the C_08-class build is ONE derived binary column + a
dictionary definition line -- **no remediation workstream exists** (decision-tree framing, AUM-weighting,
and the txn-grain fallback are all superseded/unarmed). **Sizing consequence:** the box does NOT need
compute headroom for a fee-remediation job; the runner-class load is the standard gold build, so W3
right-sizing measures that, not a remediation phantom.

## 2. Lifecycle -- clone the proven self-stop runner (canonical-schwab-runner / bd-gold-layer-runner)

```
[trigger fires] -> SSM AWS-StartEC2Instance -> box BOOTS
  user-data / SSM run-command:
    1. pull job code from s3://<artifact-bucket>/<runner-prefix>/src/   (Rule 12: never inline in SSM)
    2. run the job (S8-gate-style precondition -> build -> verify)
    3. upload output to the monolith silver/gold tree + run log to .../_runlogs/
    4. OS `shutdown -h now`  ->  instance STOPS (not terminates)
[idle] box STOPPED, $0 compute until the next trigger
```

- **Self-stop, no `ec2:*` on the box role:** `instance_initiated_shutdown_behavior = "stop"` means the OS
  shutdown STOPS the instance -- so the box role needs NO `ec2:StopInstances` (confirmed: this is exactly
  how bd-gold-layer-runner + canonical-schwab-runner do it; runner.tf:27, S4_S6b_S8_DESIGN.md:5).
- **Watchdog safety-net:** a max-runtime watchdog (`watchdog-shutdown.sh` pattern) force-stops a hung run
  so a wedged job never bills indefinitely. Bounds the worst-case cost.
- **STOPPED not TERMINATED:** persistent instance (fast warm boot, stable instance-id for the trigger's
  tag condition), zero compute cost while idle. EBS-only idle cost.

## 3. Start mechanism -- from W3's trigger/schedule census

Two supported start edges (pick per the job; W3 census confirms no collision with existing rules):
- **Scheduled** (the common case): `aws_cloudwatch_event_rule` cron -> SSM `AWS-StartEC2Instance`. Cron
  slot chosen from the W3 schedule census to avoid clustering against existing fires (mirror 14:15Z,
  sweeps 16:00Z, bd 03:30/05:00Z, schwab REST 09:45/21:45Z, etc.).
- **Event-driven** (when a fresh upstream success must gate the run, per the canonical-schwab S10->S4
  precedent): an upstream success sentinel event -> same SSM start. PREVENT>DETECT ordering.
- **Start-path IAM (least-privilege, the box never self-starts):** a dedicated trigger role holds
  `ec2:StartInstances` **conditioned on the box's `Name` tag** (+ `ssm:StartAutomationExecution` +
  `iam:PassRole` the automation role). The box role holds NONE of this. (canonical-schwab runner-trigger.tf
  is the exact template.)
- **Sentinel/schedule-absence alarm:** if the start edge never fires in its expected window the job
  silently never runs -- a `TriggeredRules == 0` alarm on `opal-critical-surface-alerts` catches the
  silent-never-fire (hold `treat_missing_data=notBreaching` until first real fire, then flip to breaching).

## 4. Box IAM (Rule 22a discipline -- one --resource-arns per simulate, positive control SEPARATE)

Instance-profile role, least-privilege, monolith-scoped:
| Grant | Scope | Note |
|---|---|---|
| `s3:GetObject` | `<artifact-bucket>/<runner-prefix>/src/*` | pull job code (Rule 12) |
| `s3:PutObject`,`GetObject` (read-back verify) | the runner's OWN silver/gold + `_runlogs/` prefix, AES256-`Condition`ed | write output + logs; NO raw-bronze write (17a) |
| `s3:ListBucket` | conditioned `s3:prefix` = own tree | set-identity / idempotent-skip |
| SSM core (`ssmmessages`,`ec2messages`,`ssm:UpdateInstanceInformation`) | -- | managed-instance run-command channel |
| CloudWatch Logs | own log group | run logs |
| **NO `ec2:*`** | -- | self-stop is OS shutdown; start is the trigger's role |
| **NO cross-firm bucket, NO Door-6 key, NO raw-bronze Put** | -- | fence negatives, 22a-exercised |

**22a proof plan (per grant, at authoring):** `aws iam simulate-principal-policy --policy-source-arn <box-role>
--action-names <action> --resource-arns <EXACT key>` -- ONE resource-arn per call; positive control a
SEPARATE invocation; `--context-entries` for the AES256-conditioned Put; fence negatives (firm bucket,
Door-6 key, raw bronze prefix) each their own call. Ground on live `get-role-policy` after apply (DESIRED
!= APPLIED).

## 5. Deploy path (Rule 12 / EC2_CODE_DEPLOYMENT_STANDARD) + sizing (W2/W3)

- **Code:** authored locally -> `aws s3 cp` to `s3://<artifact-bucket>/<runner-prefix>/src/` -> box pulls
  at boot. NEVER inline Python in SSM, never write code on the VM. Even ad-hoc diagnostics go via S3.
- **Deploy vehicle:** `safe-ec2-deploy.sh` (Rule 7); the box registered in `EC2_MANIFEST.json` (Rule 8).
- **Sizing (W2 cost profile + W3 right-sizing methodology, telemetry-driven, SCHEDULED-nightly only):**
  instance type sized to the measured peak of the heaviest hosted job -- NOT a guess, NOT the yang default.
  Right-size DOWN from telemetry (W3 HARD CONSTRAINT: never a manufactured run to size it).
  **W3 baseline read (2026-07-15, existing scheduled runners -- no manufactured runs):** the estate's
  gold-runner class is uniformly **r-family (memory-optimized)** -- `bd-gold-layer-runner` = r6i.4xlarge
  (16 vCPU / 128 GB; the heavy BD gold 01-10; scheduled-run CPU Max 13-80%/h), `canonical-schwab-runner` =
  r6i.xlarge (4 vCPU / 32 GB); the light download boxes (bd-allocations/-transactions) = t3.medium. This
  confirms the memory-optimized class and gives a concrete range. **Grounded placeholder: r6i.xlarge floor**
  (matches canonical-schwab-runner) -- the consolidation runner-class is LIGHTER than the full BD gold 01-10
  (RULING 6 removed the fee-remediation load; it is thin dims + projections + a binary C_08 column), so the
  32 GB floor is the right start, right-sized from the box's OWN first scheduled run (CloudWatch-agent
  memory telemetry; default EC2 metrics carry CPU/net only, so the box installs the agent to measure its
  own RSS peak). GB-s-equivalent cost is near-zero at idle (STOPPED) -- the box only bills during its run
  window. **W3 TO is thereby satisfied AS this box input (COO 170318Z framing), not as a standalone
  deliverable.**

## 6. EC2_MANIFEST registration (Rule 8) -- draft

A new entry: service name, instance-id (post-first-apply), type, persistent(STOPPED-when-idle), the
SSM start-doc, the S3 src prefix, the self-stop mechanism, owner 0.7.0. Registered in the same change as
the TF (source-of-truth invariant).

## 7. Apply plan (all gated on CTO)

Pure to-add TF module `infra/aws/terraform/<consolidation-runner>/`: instance (STOPPED-behavior=stop) +
instance-profile/role (Section 4) + trigger role + start rule + SSM start-target + absence alarm + SG
(egress-only to S3/SSM endpoints). `terraform plan` pure "to add"; RAVC1 the plan-shape to CTO; apply via
`safe-apply.sh` on his GO; 0-diff; tag; `EC2_MANIFEST` + source-map in the same change. **No apply in this
authoring pass.**

## 8. Open decisions for CTO (RAVC)
1. **Host-list scope:** is this box the consolidation gold-runner vehicle, the heavy-backfill EC2-branch
   pad, or both (one box, job-parameterized)? I lean BOTH (one parameterized box; simplest, matches
   "small box") -- confirm.
2. **Start edge default:** scheduled-cron vs event-sentinel per job -- W3 census supports both; default
   scheduled unless a freshness invariant demands the sentinel (canonical-schwab precedent).
3. **Instance type:** hold for the W3 telemetry read, or set a conservative memory-optimized placeholder
   now and right-size on first scheduled run? (I recommend placeholder + right-size, so the box exists to
   generate its own telemetry.)
4. **Bucket:** which artifact/output bucket -- the monolith `opal-data-assets` (consolidation-native) vs a
   firm bucket. New-territory says monolith unless the output is firm-served platinum.
