# ADHC_TRIGMRK — Trigger-Marker Race-Surface Mitigation (Inflection Gold Pipeline)
**PRD v0.1 — 0.6.1_AE_PartnerETL — 2026-05-14**

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

## §3 — Target Architecture

Three architectural levers; this PRD scopes all three for atomic hardening:

### 3.1 — Lever A: Install `inf-gold-dispatcher.service` systemd daemon (closes race surface #2)

Persistent daemon on `inf-gold-layer-runner` that polls trigger markers when EC2 is running:

- **Polling interval:** 30s (matches existing telemetry sync cadence; cheap)
- **Read targets:** `s3://opal-data-inf/gold/trigger-mode.json` + `gold/trigger-pending.json`
- **On pending marker present:**
  1. Read mode marker
  2. Verify mode marker timestamp is fresh (≤300s old; reject stale per Lever C)
  3. Acquire dispatch lock (S3 conditional-put `gold/dispatch-lock.json` with chain_in_flight=true)
  4. `aws s3 cp dispatch.sh /tmp/` + `bash dispatch.sh --chain {mode} --bg`
  5. Delete pending marker on successful dispatch
- **On lock conflict:** skip cycle; daemon resumes next poll
- **systemd unit:** `Restart=on-failure`, `StartLimitBurst=3`, `User=ec2-user`, journalctl-tagged

**Implementation surface:**
- `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-gold-dispatcher.sh` (~80 LOC bash)
- `infra/aws/ec2/inf-gold-layer-runner/systemd/inf-gold-dispatcher.service` (unit file)
- EC2_MANIFEST.json updated with new service entry
- Deploy via `safe-ec2-deploy.sh inf-gold-layer-runner deploy.sh` (S3 artifact model per Rule 12)

### 3.2 — Lever B: Lambda pre-write `chain_in_flight` check (closes race surface #1)

Lambda extends current logic:

```python
# Pseudocode — current flow:
write_mode_marker(mode)
if ec2_stopped:
    start_instances()
else:
    write_pending_marker()

# Pseudocode — hardened flow:
if read_dispatch_lock().chain_in_flight:
    # Refuse to write markers — would race with in-flight chain
    return {"statusCode": 409, "body": "Chain in flight; reject duplicate trigger"}

if read_mode_marker().is_stale(>300s):
    # Stale marker from earlier failure — clear it before writing fresh
    delete_mode_marker()

write_mode_marker(mode, source=actual_invocation_source)
if ec2_stopped:
    start_instances()
else:
    write_pending_marker()
```

**Implementation surface:**
- `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py` (extension; ~40 LOC added)
- IAM extension: read+conditional-put on `gold/dispatch-lock.json` (already has S3 access to bucket; just adds key path)
- Unit tests: stale-marker rejection, lock-held rejection, fresh path

### 3.3 — Lever C: Mode-marker `source` provenance fix (closes auxiliary issue)

Lambda detects invocation source from `event` shape and writes accurate `source` field:

| Event shape | Source value |
|-------------|--------------|
| EventBridge cron (`source: "aws.events"`, `detail-type: "Scheduled Event"`) | `"cron"` |
| Direct lambda-invoke (no event source) | `"direct"` |
| S3 ObjectCreated (`source: "aws.s3"`) | `"s3-event-{detail.bucket.name}-{detail.object.key}"` |
| SNS / other | `"sns"` / fallback `"unknown"` |

**Implementation surface:**
- 1 function in `inf-gold-trigger/lambda_function.py`: `detect_invocation_source(event) -> str`
- Mode-marker JSON gains accurate provenance; downstream telemetry + forensics trustable

### 3.4 — Architecture comparison: pending-marker pattern preserved vs replaced

| Option | Pros | Cons |
|--------|------|------|
| **Option A: Preserve pending-marker pattern + add daemon (this PRD)** | Lambda code minimal change; EC2 daemon is small new artifact; backward-compat with cold-start path | Adds systemd unit to manage; daemon failure becomes new failure surface |
| Option B: Lambda → SSM RunCommand directly (skip markers entirely) | No daemon needed; Lambda-to-EC2 RPC is canonical AWS pattern | Lambda needs SSM:SendCommand IAM; larger Lambda payload; loses S3 audit trail of trigger events |
| Option C: EventBridge → SSM RunCommand directly | Cleanest; no Lambda; no daemon | Loses Lambda's preconditional logic (stale-marker check, mode resolution); larger TF surface |

**Recommendation (Option A — pending-marker + daemon):** preserves the audit trail (`gold/trigger-mode.json` + `gold/trigger-pending.json` as canonical records of WHO asked for WHAT mode), adds minimal new surface, matches existing BD-pipeline precedent. Levers B + C are independent additions that work regardless of which option is chosen.

---

## §4 — Empirical Acceptance Criteria

| AC | Condition | Pass Signal |
|----|-----------|-------------|
| AC1 | Lambda invoke with EC2 hot, no in-flight chain | Daemon picks up pending marker within ≤60s; chain fires; `chain_in_flight` lock acquired |
| AC2 | Lambda invoke with EC2 stopped, no in-flight chain | Existing cold-start path unchanged; chain fires within ≤90s (StartInstances + boot sequence) |
| AC3 | Lambda invoke with chain in-flight (`chain_in_flight=true`) | Lambda returns 409; mode marker NOT overwritten; no double-fire |
| AC4 | Stale mode marker from prior failure (>300s old) | Lambda deletes stale marker before writing new; no race with daemon |
| AC5 | EC2 cold-start with stale marker from prior failure (>300s old) | Boot script reads marker, rejects as stale, waits for fresh marker (current behavior unchanged) |
| AC6 | Daemon polls but no pending marker | Daemon idles; no spurious dispatch |
| AC7 | Daemon failure (process killed) | systemd restarts within ≤30s; `StartLimitBurst=3` prevents flap |
| AC8 | Mode-marker `source` field on direct lambda-invoke | Reads `"direct"`, NOT `"cron"` (auxiliary issue closed) |
| AC9 | Mode-marker `source` field on EventBridge cron fire | Reads `"cron"` (unchanged) |
| AC10 | Mode-marker `source` field on S3 aggregator event fire | Reads `"s3-event-opal-data-inf-silver/_silver_complete/..."` |
| AC11 | Empirical regression test against today's incident #3 chain | Re-fire identical scenario (EC2 hot, mode=gold-d) → chain TERMINAL within ≤300s wall (matches DS~D SSM-direct precedent 279s) |

---

## §5 — Risk Surface

| Risk | Mitigation |
|------|-----------|
| Daemon flap (restart loop) | `StartLimitBurst=3` + `StartLimitIntervalSec=300`; alerts via existing `inf-otp-alert` SNS on daemon-died journalctl pattern |
| Daemon competes with cold-start boot script for marker reads | Boot script remains canonical for cold-start; daemon defers if `/var/run/inf-boot-dispatch.lock` exists; mutual exclusion |
| Lock TTL on stuck chain | `gold/dispatch-lock.json` includes `started_at`; daemon ignores locks >2× expected wall-time (~30min for full chain); auto-clears stale lock |
| Lambda `chain_in_flight` check races with chain-start | Lock is S3 conditional-put with `If-None-Match`; atomic; race-safe |
| ROLLBACK: revert to current behavior cleanly | Disable systemd unit → daemon stops; Lambda extension is feature-flagged via env-var `TRIGMRK_HARDENING_V1=1`; flip to 0 reverts |

---

## §6 — Cross-Project Dependencies

- **Sister to `[[ADHC_BPMVH]]` chain-fire materialization** — every chain fire today exercises this trigger path; BPMVH's chain-fire cadence reveals trigger surface
- **`[[reference_inf_ssm_direct_single_script_runbook]]` workaround** — until TRIGMRK ships, SSM-direct is canonical fallback; banked in memory
- **`[[feedback_lambda_pending_marker_no_daemon]]`** — DS~D-authored memory entry on race surface #2 empirical contrast; banked 2026-05-14 18:30Z
- **`[[ADHC_COMPIL_V4.030]]` comp-pipescript stale-marker** — compiler-side companion tool (COO authored + held in v0.5 batch with `dispatch_held=true`); ships complementarily with ADHC_TRIGMRK operational fix per COO 18:35Z msg
- **`[[ADHC_ORIONPROBE]]`** — sibling AE 0.6.1 project queued post-TRIGMRK per CTO 18:25Z RAVC1 sequence-lock

---

## §7 — Implementation Phases

| Phase | Owner | Wall | Deliverable |
|-------|-------|------|-------------|
| Phase 1 — PRD ratify | AE 0.6.1 draft / COO review / CTO ratify | ~1h | This doc → docs/architecture/ADHC_TRIGMRK.md |
| Phase 2 — TO-001 daemon + Lambda hardening | AE 0.6.1 | ~1d wall | Daemon script + systemd unit + Lambda extension + Terraform updates + EC2_MANIFEST entry |
| Phase 3 — Acceptance regression sweep | AE 0.6.1 | ~2h | AC1-AC11 empirical PASS on QA EC2 + non-prod Lambda alias |
| Phase 4 — PROD deploy + Andrew UAT | AE 0.6.1 | ~30min | Standard Lambda Deployment Sequence (Rule 1-6) + `safe-ec2-deploy.sh` for daemon + `inf-v{X.Y.Z}` tag |
| Phase 5 — Memory + comp-tool registration | AE 0.6.1 | ~30min | Update `[[reference_inf_ssm_direct_single_script_runbook]]` to note TRIGMRK supersession; archive `[[feedback_lambda_pending_marker_no_daemon]]` as resolved |

---

## §8 — Open Questions

1. **Q1: Daemon scope — single-instance or fleet-aware?** Current proposal: single daemon per inf-gold-layer-runner EC2. The BD pipeline has a parallel `bd-gold-layer-runner` with the same trigger pattern; should this PRD scope to inf-only or include BD as a parallel fleet hardening? AE 0.6.0 owns BD; coordination needed.

2. **Q2: Lock TTL — fixed 30min or chain-mode-aware?** Different modes have different expected wall-times (gold-d ~13min, full ~70min). Lock TTL should probably be `2 × max(known_wall_time_for_mode)`. Per-mode lookup table or single conservative ceiling?

3. **Q3: Backward-compat on cold-start path?** Daemon installation changes EC2 startup sequence. Existing cold-start works without daemon; need to verify daemon doesn't interfere with the boot-script-reads-markers path (mutex via `/var/run/` lock proposed; needs test).

4. **Q4: Auxiliary mode-marker `source` fix — separate TO or fold into TO-001?** Lever C is independent of Levers A+B but lightweight (~5 LOC). Fold into TO-001 for atomic ratify, or split as TO-002 for clean scope separation?

5. **Q5: Telemetry integration?** The opal-runner-shared telemetry system has a known wiring gap (`[[reference_opal_runner_shared_telemetry]]`). Should daemon emit telemetry hooks while we're touching the dispatch path? Or defer per AE 0.7 telemetry-coverage TO?

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
- v0.1 — AE 0.6.1_AE_PartnerETL — 2026-05-14 (this draft)
- v0.2 → COO review + CTO architectural ratify (pending)
- v0.3 → CTO canonicalize via git mv to `docs/architecture/ADHC_TRIGMRK.md` per ADHC_OWNPTH
