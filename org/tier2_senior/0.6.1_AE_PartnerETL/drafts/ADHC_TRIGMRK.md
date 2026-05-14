# ADHC_TRIGMRK — Trigger-Marker Race-Surface Mitigation (Inflection Gold Pipeline)
**PRD v0.2 — 0.6.1_AE_PartnerETL — 2026-05-14 ~18:45Z**

> **v0.2 changelog (post COO RAVC1 18:40Z):** §3 restructured around Path 1 vs Path 2 explicit decision section per CTO 18:0XZ architectural framing. **Path 2 (abandon marker; Lambda direct-invokes SSM Run Command) LEAN** absorbed from CTO + COO. Race surfaces #1 + #2 + cron-source-marker-env-default unified as instances of single root pattern — `feedback_phantom_consumer_marker_pattern` (CTO verbatim: "The marker pattern was designed for a daemon that ops never built; rather than build the daemon to satisfy the pattern, abandon the pattern. Single producer/consumer pair is simpler than producer/marker/consumer."). Q1-Q5 resolved per COO. Backwards-compat scope added for in-flight markers at deploy boundary.

**PRD v0.1 — 0.6.1_AE_PartnerETL — 2026-05-14** (3-lever Option A/B/C structure; superseded by v0.2 Path 1/Path 2 framing)

> Authored post 2026-05-14 three-incident empirical anchor: the `inf-gold-trigger` Lambda + EC2 dispatcher contract is fragile in BOTH boot-state directions. Two structurally distinct race surfaces + one auxiliary attribution issue surfaced in a single day. Both surfaces silently produce wrong outcomes (wrong-mode chain fire OR no chain fire at all) without operator-visible failure signals.

---

## §1 — Scope

Eliminate the silent-failure surfaces in the Inflection gold-chain trigger contract between `inf-gold-trigger` Lambda and `inf-gold-layer-runner` EC2. Surface chosen for hardening is the **trigger marker handoff** — the S3 objects (`gold/trigger-mode.json` + `gold/trigger-pending.json`) that the Lambda writes and the EC2 is supposed to read.

**In scope:**
- Race surface #1: stale-marker race — preemptive EC2 boot consumes old marker before a new mode marker is written; chain fires wrong mode
- Race surface #2: no-daemon silent fail — Lambda writes "pending marker" pattern when EC2 already running; no daemon exists on EC2 to read it; chain never fires
- Auxiliary issue: `source` field in mode-marker JSON inherits Lambda env-var default (`"cron"`) even on direct lambda-invoke or S3-event firings; mode-marker provenance assertion isn't structurally sound
- Misleading Lambda response wording: `"EC2 already running - mode marker + pending marker written"` reads as success when it's actually a silent no-op when EC2 is hot

**Out of scope:**
- Replacing the trigger marker pattern wholesale with EventBridge → SSM RunCommand (separate scope; this PRD hardens the existing pattern)
- Replacing the EC2 dispatcher daemon with a Lambda-based chain orchestrator (significantly larger architectural change; viable v2)
- Bronze trigger / silver trigger marker contracts (orthogonal Lambdas; not empirically anchored today)
- ADHC_DSFLOW silver/gold sentinel-file pattern (already shipped; works correctly)

**Non-goals:**
- Removing the EC2-cold-start path entirely (the StartInstances → boot-script read-markers path is the canonical fire mechanism and works correctly when EC2 is stopped)
- Replacing SSM-direct as a workaround mechanism (it works; this PRD makes the Lambda path equally robust)

---

## §2 — Existing State

### 2.1 — `inf-gold-trigger` Lambda contract (current)

`infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py`:
1. Receives invocation payload `{"mode": "full" | "gold-d" | ...}`
2. Reads current EC2 state for `inf-gold-layer-runner` (i-0ed5afded2ebd4ed4)
3. Writes mode marker `s3://opal-data-inf/gold/trigger-mode.json`
4. **Branch A — EC2 stopped:** calls `ec2:StartInstances`; EC2 boot script reads markers and fires chain — **works correctly**
5. **Branch B — EC2 running:** writes pending marker `s3://opal-data-inf/gold/trigger-pending.json`, returns 200 with body `"EC2 already running - mode marker + pending marker written"` — **silent no-op (race surface #2)**

### 2.2 — `inf-gold-layer-runner` EC2 dispatcher (current)

SSM diagnostic 2026-05-14 18:15Z on i-0ed5afded2ebd4ed4 (uptime ~4h, prior chain complete at 14:32Z):

```bash
$ systemctl status inf-gold-dispatcher.service
Unit inf-gold-dispatcher.service could not be found.

$ ps -ef | grep -E "orion-gold-dispatch|inf-gold-dispatcher|systemd-inf"
# empty

$ ls -la /tmp/inf-trigger-*
ls: cannot access '/tmp/inf-trigger-*': No such file or directory

$ journalctl -u inf-gold-dispatcher.service --since "30 minutes ago" --no-pager
# No entries
```

**Finding:** There is no daemon on the EC2 polling for trigger markers in the running state. The boot-script-reads-markers path only fires once per boot. Markers written while EC2 is running sit in S3 unread until the next cold-start cycle.

### 2.3 — Race surface #1 empirical (incident #1 + #2)

**Incident #1 (earlier 2026-05-14):** Preemptive EC2 boot pattern — Lambda fires StartInstances after writing markers, but a prior orphan boot (e.g. from earlier failed chain) reads the OLD marker before the new one lands. Wrong mode fires.

**Incident #2 (`chain_full_20260514_141419`):** Stale-marker race — Lambda wrote new mode marker, EC2 boot raced, read stale marker, fired wrong chain mode. Operator (AE 0.6.1) killed via SSM + re-dispatched correctly per Andrew direct ("lets not do another full run, we should just do the d group run"). 49min recovery delay.

### 2.4 — Race surface #2 empirical (incident #3, 2026-05-14 18:14Z)

Direct Lambda invoke `aws lambda invoke --function-name inf-gold-trigger --payload '{"mode":"gold-d"}'`:
- StatusCode 200, response body: `"EC2 already running - mode marker + pending marker written"`
- Mode marker written: `gold/trigger-mode.json`
- Pending marker written: `gold/trigger-pending.json`
- ~13min elapsed
- Telemetry shows NO new chain run_id
- Old `chain_gold-d_20260514_141936` still authoritative (complete, updated 14:32:59Z)

Resolution path: SSM-direct dispatch on the running EC2 (`aws s3 cp dispatch.sh && bash --chain gold-d --bg`). DS~D fired at 18:20:52Z → `chain_gold-d_20260514_182107` TERMINAL at 18:25Z (279s wall).

### 2.5 — Empirical contrast pair (DS~D evidence msg 18:28Z; banked at `[[feedback_lambda_pending_marker_no_daemon]]`)

| Path | Outcome | Time |
|---|---|---|
| Lambda `inf-gold-trigger` invoke `{mode:"gold-d"}` (EC2 hot) | Silent no-op (pending-marker written, no daemon to read) | 18:14:06Z (~13min elapsed, no chain) |
| SSM-direct `aws s3 cp dispatch.sh && bash --chain gold-d --bg` | Clean fire → terminal in 279s | 18:20:52Z (`chain_gold-d_20260514_182107`) |

### 2.6 — Auxiliary issue: mode-marker `source` provenance

Lambda's `gold/trigger-mode.json` always emits `"source": "cron"` regardless of invocation path (cron EventBridge / direct lambda-invoke / S3-event aggregator). This is a Lambda env-var default. Today's 18:14Z direct invoke wrote `source: "cron"` despite no cron event firing.

**Forensic impact:** mode-marker JSON cannot be trusted as a provenance record. Downstream telemetry / ADHC_TRIGMRK forensics that key off the `source` field will misattribute.

---

## §3 — Target Architecture: Path 1 vs Path 2 Decision

The three defects (race surface #1 stale-marker, race surface #2 no-daemon silent-fail, auxiliary source-provenance) are instances of a single root pattern: **producer/marker/consumer triangulation where the consumer was never built.** Two architectural responses, mutually exclusive at the structural level.

### §3.1 — Path 1: Preserve marker pattern + add daemon

(v0.1 framing; retained for decision-record completeness; **SUPERSEDED by Path 2 — see §3.3**)

Three levers compose:
- **Lever A1:** Install `inf-gold-dispatcher.service` systemd daemon on `inf-gold-layer-runner` polling `gold/trigger-mode.json` + `gold/trigger-pending.json` every 30s; on pending-marker present, verify mode marker freshness (≤300s) + acquire S3 conditional-put dispatch-lock + `bash dispatch.sh --chain {mode} --bg`. (~80 LOC bash + systemd unit + EC2_MANIFEST entry + S3-pull deploy per Rule 12.)
- **Lever B1:** Lambda pre-write `chain_in_flight` lock-check + stale-marker delete (>300s age) before writing fresh mode marker. (~40 LOC Lambda + IAM extension for conditional-put on dispatch-lock.)
- **Lever C1:** Mode-marker `source` provenance detection from event shape (`aws.events` → `"cron"`, no source → `"direct"`, `aws.s3` → `"s3-event-{bucket}-{key}"`). (~5 LOC Lambda.)

**Pros:** preserves S3 audit trail (mode-marker + pending-marker as canonical records of WHO asked for WHAT mode); minimal Lambda code change; backward-compat with cold-start boot-script-reads-markers path.

**Cons:** adds operational surface (systemd unit health, daemon-down recovery, mutex with boot-script); 3 distinct levers needed to close 3 distinct race surfaces; daemon failure becomes a *new* silent-failure surface.

### §3.2 — Path 2: Abandon marker pattern; Lambda direct-invokes SSM Run Command (RECOMMENDED)

Per CTO 18:0XZ architectural framing (verbatim): *"The marker pattern was designed for a daemon that ops never built; rather than build the daemon to satisfy the pattern, abandon the pattern. Single producer/consumer pair is simpler than producer/marker/consumer."*

Single Lambda flow replaces the entire marker handoff:

```python
# inf-gold-trigger Lambda (Path 2 — Lambda direct-invokes SSM Run Command)

def lambda_handler(event, context):
    mode = event.get("mode", "full")
    invocation_source = detect_invocation_source(event)  # Lever C1 retained

    ec2_state = ec2_describe_instances(INF_GOLD_LAYER_RUNNER_ID)
    if ec2_state == "stopped":
        ec2_start_instances(INF_GOLD_LAYER_RUNNER_ID)
        wait_for_instance_running(timeout=120)
        wait_for_ssm_agent_online(timeout=60)
    elif ec2_state != "running":
        return {"statusCode": 503, "body": f"EC2 in transitional state {ec2_state}; retry shortly"}

    # Acquire chain_in_flight lock (S3 conditional-put with If-None-Match)
    lock = acquire_dispatch_lock(mode, invocation_source, ttl=mode_aware_ttl(mode))
    if lock.held_by_other:
        return {"statusCode": 409, "body": f"Chain {lock.run_id} in flight; reject"}

    # Direct invoke — no markers, no daemon
    ssm_response = ssm_send_command(
        instance_id=INF_GOLD_LAYER_RUNNER_ID,
        document="AWS-RunShellScript",
        commands=[
            f"aws s3 cp s3://opal-data-inf/code/gold/orion-gold-dispatch.sh /tmp/",
            f"bash /tmp/orion-gold-dispatch.sh --chain {mode} --bg",
        ],
    )

    return {
        "statusCode": 200,
        "body": {
            "command_id": ssm_response["CommandId"],
            "mode": mode,
            "source": invocation_source,
            "lock_run_id": lock.run_id,
        }
    }
```

**Implementation surface:**
- `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py` — full rewrite (~120 LOC replacing existing ~80 LOC marker-writing logic)
- IAM extension: `ssm:SendCommand` on the inf-gold-layer-runner instance ID + `ec2:DescribeInstances` (already present) + S3 conditional-put on `gold/dispatch-lock.json`
- Lock TTL is **mode-aware** per COO Q2: `gold-d` → 20min lock (~13min wall × 1.5), `full` → 90min lock (~60min wall × 1.5), `incremental` → 15min, fallback → 30min
- Backward-compat: in-flight markers at deploy boundary handled per §3.5
- Lever C1 source provenance retained — emits in Lambda response body + CW Logs, not S3 marker

**Pros:**
- **Race surface #1 collapses:** no markers = no stale-marker race
- **Race surface #2 collapses:** no markers = no consumer needed; SSM RunCommand is the canonical AWS Lambda→EC2 RPC primitive
- **Auxiliary issue collapses:** `source` provenance lives in Lambda response + CW Logs (authoritative), not in a separate S3 marker subject to env-var-default drift
- **Single producer/consumer pair** (Lambda → EC2 via SSM) replaces producer/marker/consumer triangulation
- **No daemon to manage** — no new systemd unit, no daemon-health monitoring, no daemon-down recovery
- **Audit trail preserved differently** — SSM CommandId + CW Logs serve same role as mode-marker JSON; queryable via `aws ssm list-commands`

**Cons:**
- Larger Lambda code change vs Path 1 Lever B1
- Loses S3-marker-as-audit-record convention; audit shifts to SSM CommandId + CW Logs
- Lambda+SSM IAM coupling deeper (Lambda role gains `ssm:SendCommand` scoped to single instance ARN)
- Requires `wait_for_ssm_agent_online` polling in cold-start path (current: marker write is instant; SSM agent boot adds ~30-60s but is required either way for Path 1's daemon-on-boot)

### §3.3 — Decision: Path 2 LEAN (CTO + COO + AE align)

**CTO lean:** Path 2 (verbatim above, 18:0XZ).
**COO endorsement:** Path 2 (msg 18:40Z; "Lever A becomes 'Lambda direct-invokes SSM Run Command on EC2; if EC2 stopped, Lambda first StartInstances then SSM Run Command after EC2 healthy.'").
**AE absorption:** Path 2. Path 1 v0.1 lean was defensive (preserve audit trail) but the audit-trail argument doesn't survive scrutiny — SSM CommandId + CW Logs are equally durable and authoritative.

**Decision-rights:** CTO architectural ratify on dispatch per LEDGEH precedent. Andrew countermand possible during ratify window; framing-decision documented here so Andrew can override at any phase.

### §3.4 — Phantom-consumer pattern banking

The three defects in §2 are not three separate bugs — they are three SYMPTOMS of one root pattern.

**Pattern definition (`feedback_phantom_consumer_marker_pattern`):** A producer (Lambda) emits a marker (S3 JSON) to coordinate with a consumer that was never built (daemon `inf-gold-dispatcher.service`). The pattern reads as a feature ("EC2 already running — mode marker + pending marker written") but is a silent-failure surface — the marker has no reader, the producer's response asserts success based on the *write*, not the *consumption*.

**Generalized rule:** Before emitting a marker, verify the consumer exists.
- **Code-level check:** producer's deployment artifact pinned to a consumer's deployment artifact; cross-reference validated at deploy time
- **Runtime check:** producer's write includes a "consumer-alive" probe (SSM agent ping, daemon heartbeat S3 object, etc.) before declaring success
- **Architectural check:** prefer direct producer/consumer pairs over producer/marker/consumer triangulation when consumer multiplicity isn't needed (this PRD's Path 2 lean)

**Distinct from `feedback_smoking_gun_field_shape_sanity`** (DS~D 2026-05-14; producer/consumer disagree on field shape) — that's wire-protocol divergence. Phantom-consumer is wire-consumer divergence.

**Distinct from ADVI_SHARED.006 wire-protocol divergence** — that's consumer ignoring producer fields. Phantom-consumer is producer assuming a consumer that doesn't exist.

**Banking:** Memory entry `feedback_phantom_consumer_marker_pattern.md` will be authored by AE 0.6.1 post-canonicalize, cross-linked to this PRD + `[[feedback_lambda_pending_marker_no_daemon]]` (DS~D-attributed empirical contrast) + `[[reference_inf_ssm_direct_single_script_runbook]]` (canonical workaround).

### §3.5 — Backwards-compat scope (in-flight markers at deploy boundary)

Path 2 abandons marker pattern entirely. Deploy boundary handling:

**Pre-deploy state:** `gold/trigger-mode.json` + `gold/trigger-pending.json` may exist in S3 (last invocation of v1 Lambda before v2 Lambda deploy). EC2 cold-start boot script still reads them.

**Deploy-day plan:**
1. **Pre-deploy sweep:** AE 0.6.1 runs `aws s3 rm s3://opal-data-inf/gold/trigger-mode.json` + `gold/trigger-pending.json` immediately before `terraform apply` lands new Lambda. Drains in-flight markers.
2. **Boot-script update:** `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-boot-dispatch.sh` shipped in same `safe-ec2-deploy.sh` commit removes marker-read code path; replaced with `aws ssm get-parameter --name /inf/gold/last-trigger-mode` fallback for cold-start mode lookup. (Lambda writes the SSM Parameter on every invoke for cold-start replay.)
3. **Lambda v2 deploy:** atomic terraform apply replaces Lambda function code; new IAM `ssm:SendCommand` policy attached.
4. **Verification:** post-deploy `aws lambda invoke` test fires gold-d chain via Path 2 path. EC2 SSM agent receives command. Chain `chain_gold-d_*` materializes in telemetry. AC1 satisfied empirically.
5. **Rollback plan:** if Path 2 deploy fires regression, `git revert` + `terraform apply` rolls back; SSM Parameter remains usable artifact (orthogonal to Lambda choice).

**Ignore vs drain decision:** **DRAIN** (sweep markers pre-deploy). Ignore-in-place leaves markers in S3 indefinitely — a stale audit artifact + potential confusion for next forensic investigator. Drain is one `aws s3 rm` and clears confusion.

### §3.6 — Source provenance fix (Lever C1; retained in Path 2)

Independent of Path 1/Path 2 choice. Lambda detects invocation source from `event` shape and writes accurate `source` field to:
- Lambda response body (Path 2)
- CW Log structured-log entry (both paths)
- SSM CommandId Comment field (Path 2)

| Event shape | Source value |
|-------------|--------------|
| EventBridge cron (`source: "aws.events"`, `detail-type: "Scheduled Event"`) | `"cron"` |
| Direct lambda-invoke (no event source key) | `"direct"` |
| S3 ObjectCreated (`source: "aws.s3"`) | `"s3-event-{detail.bucket.name}-{detail.object.key}"` |
| SNS (`source: "aws.sns"` or `Records[].EventSource: "aws:sns"`) | `"sns-{topic_arn_short}"` |
| Fallback | `"unknown-{event_keys_csv}"` |

**Implementation:** `detect_invocation_source(event) -> str` helper in `lambda_function.py`. ~15 LOC.

---

---

## §4 — Empirical Acceptance Criteria (Path 2)

| AC | Condition | Pass Signal |
|----|-----------|-------------|
| AC1 | Lambda invoke with EC2 hot, no in-flight chain | Lambda returns 200 with `command_id` populated; SSM `list-commands` confirms command dispatched within ≤30s; chain fires within ≤60s; `chain_in_flight` lock acquired |
| AC2 | Lambda invoke with EC2 stopped, no in-flight chain | Lambda `wait_for_instance_running` + `wait_for_ssm_agent_online` succeed; SSM command dispatched; chain fires within ≤180s (vs prior cold-start ≤90s; SSM-agent-online wait adds ~30-60s) |
| AC3 | Lambda invoke with chain in-flight (lock held) | Lambda returns 409 with body `f"Chain {lock.run_id} in flight; reject"`; no SSM command dispatched; no double-fire |
| AC4 | Lock TTL expiry — stale lock from crashed prior chain | Lock auto-clears at TTL (mode-aware: gold-d 20min, full 90min); next invoke acquires fresh lock |
| AC5 | EC2 transitional state (pending / stopping / shutting-down) | Lambda returns 503 with body `"EC2 in transitional state {state}; retry shortly"`; no SSM command; idempotent retry-safe |
| AC6 | Mode-aware lock TTL behavior | `gold-d` lock holds 20min max; `full` 90min max; `incremental` 15min; fallback 30min |
| AC7 | Lambda response `source` field on direct lambda-invoke | Reads `"direct"`, NOT `"cron"` (auxiliary issue closed; verified in CW Log structured entry) |
| AC8 | Lambda response `source` field on EventBridge cron fire | Reads `"cron"` (unchanged behavior; verified via daily 06:00 UTC `inf-canonical-prices-daily` invocation) |
| AC9 | Lambda response `source` field on S3 aggregator event fire | Reads `"s3-event-opal-data-inf-silver/_silver_complete/..."`; verified via `inf-silver-aggregator` Lambda chain-fire path |
| AC10 | Backward-compat deploy boundary — markers swept pre-deploy | `aws s3 ls s3://opal-data-inf/gold/trigger-*.json` returns empty post-deploy; no stale audit artifacts |
| AC11 | Empirical regression test against today's incident #3 | Re-fire identical scenario (EC2 hot, mode=gold-d) → chain TERMINAL within ≤300s wall (matches DS~D SSM-direct precedent 279s); no manual SSM-direct workaround needed |
| AC12 | SSM CommandId audit trail | `aws ssm list-commands --instance-id i-0ed5afded2ebd4ed4 --filters "key=Status,value=Success"` returns Lambda-dispatched commands tagged with mode + invocation_source + lock_run_id |

---

## §5 — Risk Surface (Path 2)

| Risk | Mitigation |
|------|-----------|
| SSM agent offline on EC2 (e.g. after instance refresh / patch) | Lambda `wait_for_ssm_agent_online` poll with 60s timeout; on timeout return 503; CW alarm on 503 rate >0 |
| SSM `SendCommand` IAM denial | Lambda IAM scoped to `arn:aws:ec2:us-east-1:*:instance/i-0ed5afded2ebd4ed4` only (no wildcard); validated via `comp-iam service inf-gold-trigger` post-deploy |
| Lock TTL on stuck chain | `gold/dispatch-lock.json` includes `started_at` + mode-aware TTL; Lambda `acquire_dispatch_lock` deletes lock older than TTL before fresh acquire |
| Lambda + SSM both acquire lock simultaneously (race) | Lock acquire is S3 conditional-put with `If-None-Match: "*"`; atomic; race-safe per AWS S3 strong-consistency guarantees |
| Backward-compat in-flight markers at deploy boundary | Pre-deploy sweep per §3.5 (`aws s3 rm gold/trigger-*.json`); boot script removed in same deploy commit |
| Cold-start mode lookup post-marker-removal | Lambda writes SSM Parameter `/inf/gold/last-trigger-mode` on every invoke; boot script fallback reads this for cold-start recovery cases |
| ROLLBACK | `git revert` Lambda commit + `terraform apply` rolls back Lambda code + IAM; SSM Parameter remains orthogonal; can re-deploy v1 marker code if needed within ~10min |

---

## §6 — Cross-Project Dependencies

- **Sister to `[[ADHC_BPMVH]]` chain-fire materialization** — every chain fire today exercises this trigger path; BPMVH's chain-fire cadence reveals trigger surface
- **`[[reference_inf_ssm_direct_single_script_runbook]]` workaround** — until TRIGMRK Path 2 ships, SSM-direct is canonical fallback; banked in memory. Post-deploy: SSM-direct still useful for ad-hoc dispatch but Lambda becomes the canonical path
- **`[[feedback_lambda_pending_marker_no_daemon]]`** — DS~D-authored memory entry on race surface #2 empirical contrast; banked 2026-05-14 18:30Z. Mark as RESOLVED post-TRIGMRK Path 2 deploy
- **`[[feedback_phantom_consumer_marker_pattern]]`** — NEW memory entry to author by AE 0.6.1 post-canonicalize (§3.4); generalizes today's anchor as "before emitting a marker, verify the consumer exists." Distinct from `[[feedback_smoking_gun_field_shape_sanity]]` (wire-protocol shape) and ADVI_SHARED.006 wire-protocol divergence
- **`[[ADHC_COMPIL_V4.030]]` comp-pipescript stale-marker** — compiler-side companion tool (COO authored + held in v0.5 batch with `dispatch_held=true`); under Path 2 the marker-surface disappears entirely — coord with COO on whether .030 scope changes or becomes general "phantom consumer" sweep
- **`[[ADHC_ORIONPROBE]]`** — sibling AE 0.6.1 project queued post-TRIGMRK per CTO 18:25Z RAVC1 sequence-lock

---

## §7 — Implementation Phases (Path 2)

| Phase | Owner | Wall | Deliverable |
|-------|-------|------|-------------|
| Phase 1 — PRD ratify | AE 0.6.1 draft v0.2 / COO RAVC1 DONE / CTO architectural ratify pending | ~30min remaining | This doc → docs/architecture/ADHC_TRIGMRK.md (CTO canonicalize) |
| Phase 2 — TO-001 Path 2 Lambda rewrite | AE 0.6.1 | ~4-6h wall | Lambda full rewrite (~120 LOC) + IAM extension (ssm:SendCommand + s3 dispatch-lock) + Terraform updates + SSM Parameter `/inf/gold/last-trigger-mode` + lambda-source-map entry + pre-deploy marker sweep script + boot-script update + EC2_MANIFEST entry |
| Phase 3 — Acceptance regression sweep | AE 0.6.1 | ~2h | AC1-AC12 empirical PASS on QA non-prod Lambda alias + QA EC2 sample; includes today's incident #3 re-fire as AC11 |
| Phase 4 — PROD deploy + Andrew UAT | AE 0.6.1 | ~1h | Standard Lambda Deployment Sequence (Rule 1-6) + `safe-ec2-deploy.sh` for boot-script update + pre-deploy `aws s3 rm gold/trigger-*.json` sweep + `inf-v{X.Y.Z}` tag |
| Phase 5 — Memory banking + cleanup | AE 0.6.1 | ~30min | Author `[[feedback_phantom_consumer_marker_pattern]]`; mark `[[feedback_lambda_pending_marker_no_daemon]]` RESOLVED post-deploy; update `[[reference_inf_ssm_direct_single_script_runbook]]` to note canonical-via-Lambda; cross-reference all 3 in MEMORY.md |

**Total wall:** ~8-10h actual (~1-1.5d budget). Path 2 is more code change than Path 1's incremental Lambda extension but eliminates the daemon-creation phase entirely (Path 1 estimate was ~1d wall + ongoing daemon-health monitoring cost).

---

## §8 — Open Questions (RESOLVED per COO RAVC1 18:40Z)

1. **Q1: Daemon scope — single-instance or fleet-aware?** **RESOLVED: inf-only.** Per COO 18:40Z: BD pipeline doesn't use this marker pattern today; no empirical justification for scope creep. If BD ever surfaces a similar race, separate ADHC project. (Moot under Path 2 anyway — no daemon to scope.)

2. **Q2: Lock TTL — fixed 30min or chain-mode-aware?** **RESOLVED: mode-aware.** Per COO 18:40Z: chain wall-time × 1.5 conservative buffer per mode. Per-mode lookup table baked into Lambda code:
   - `gold-d` → 20min (vs ~13min wall)
   - `full` → 90min (vs ~60min wall)
   - `incremental` → 15min (vs ~10min wall hypothetical post-INFINC)
   - fallback → 30min

3. **Q3: Backward-compat on cold-start path?** **RESOLVED: Path 2 supersedes the question.** Per COO 18:40Z: Path 2 abandons marker → no daemon to mutex, no cold-start to back-compat. Boot-script-reads-markers code path removed in deploy boundary sweep (§3.5). SSM Parameter fallback for cold-start mode lookup.

4. **Q4: Auxiliary mode-marker `source` fix — separate TO or fold into TO-001?** **RESOLVED: fold into TO-001.** Per COO 18:40Z: Lever C1 ~15 LOC; auxiliary forensic is part of the same root pattern (phantom-consumer §3.4); single atomic ship simpler than 2-TO split.

5. **Q5: Telemetry integration during PRD or defer?** **RESOLVED: defer.** Per COO 18:40Z: TRIGMRK scope = fix the race surfaces. Telemetry-to-detect-future-races is separate concern (`[[reference_opal_runner_shared_telemetry]]` partial coverage exists). If TRIGMRK-specific sentinel desired post-deploy (e.g. "Lambda invoke time > 30s without command_id = alarm"), add as P2 follow-on `ADHC_TRIGMRK.002.telemetry-sentinel.md`; NOT in TO-001 scope.

**All 5 resolved. No open Qs blocking TO-001 authoring.**

---

## §9 — Forensic Appendix (Today's 3 Incidents)

### Incident #1 — earlier 2026-05-14

(Empirical detail from prior session log; AE 0.6.1 session continuity post-compaction.)

### Incident #2 — `chain_full_20260514_141419` stale-marker race

(Detail in `org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-14/inf_pipeline_e2e_recovery_and_incremental_brief.md`.)

### Incident #3 — 18:14:06Z Lambda hot-state silent no-op

**Wall:**
- 18:14:06Z — AE 0.6.1 invoked `inf-gold-trigger` Lambda with payload `{"mode":"gold-d"}` per CLAUDE.md Option A from COO 18:04Z
- 18:14:06Z — Lambda returns 200, body `"EC2 already running - mode marker + pending marker written"`
- 18:14:07Z — `gold/trigger-mode.json` + `gold/trigger-pending.json` written to S3
- 18:14:06Z → 18:27:00Z — No new chain run_id appears in telemetry. Old `chain_gold-d_20260514_141936` (complete since 14:32:59Z) remains authoritative
- 18:15:30Z — AE 0.6.1 SSM diagnostic: no dispatcher daemon, no orion-gold-dispatch process, no `/tmp/inf-trigger-*` files, no journalctl entries
- 18:17:45Z — AE 0.6.1 MCP COO with race-surface-#2 diagnostic; COO re-routes chain dispatch to DS~D SSM-direct
- 18:20:52Z — DS~D fires SSM-direct (`aws s3 cp dispatch.sh && bash --chain gold-d --bg`); CommandId `e741f4f4-8eff-4a66-b255-a9458b82c51f`
- 18:21:07Z — Chain `chain_gold-d_20260514_182107` LIVE in telemetry
- 18:25:00Z — Chain TERMINAL clean; 279s wall; all 20 D-stage steps OK; cash_drag perf 22s + NMCOHT nmec_count 0→1 + book.json augment mix=4 validations PASS

**Pending-marker pattern fingerprint (S3-archived 18:14:07Z, unread for 13min):**

```json
// gold/trigger-mode.json
{"snapshot_date": "2026-05-14", "mode": "gold-d", "source": "cron", "written_at": "2026-05-14T18:14:06.010229+00:00"}

// gold/trigger-pending.json
{"pending": true, "reason": "EC2 running at trigger time (source=cron date=2026-05-14)", "written_at": "2026-05-14T18:14:06.130804+00:00"}
```

(Note `source: "cron"` despite direct lambda-invoke — auxiliary issue per §3.3.)

---

**Authoring chain:**
- v0.1 — AE 0.6.1_AE_PartnerETL — 2026-05-14 ~18:35Z (initial 3-lever Option A/B/C framing)
- v0.2 — AE 0.6.1_AE_PartnerETL — 2026-05-14 ~18:45Z (this draft; Path 1 vs Path 2 reframe + Path 2 lean + phantom-consumer banking + Q1-Q5 resolved per COO RAVC1 18:40Z)
- v0.3 → CTO architectural ratify on Path 2 vs Path 1 dispatch + canonicalize via git mv to `docs/architecture/ADHC_TRIGMRK.md` per ADHC_OWNPTH
