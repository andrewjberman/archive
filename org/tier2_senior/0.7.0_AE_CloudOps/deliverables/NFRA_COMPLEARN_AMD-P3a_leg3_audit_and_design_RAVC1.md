# NFRA_COMPLEARN AMD-P3a — leg-3 producer robustness: AUDIT + design decision (RAVC1 → CTO~A)

**Author:** `0.7.0_AE_CloudOps~B` (Andrew-cleared lane, this session) · **Date:** 2026-07-10
**TO:** `org/projects/NFRA_COMPLEARN/task_orders/NFRA_COMPLEARN.AMD-P3a.leg3-producer-robustness.md` (pending @ `48a78887d`)
**Arch-gate:** `1.0.0_SA_CTO~A` · **Decomposer/track:** `2.0.0_SA_COO~A` · **Boundary:** zero bd/49F/Schwab.
**Grounding vintage:** all `file:line` citations resolve `@ 1fc318f31` (cited files clean in working tree at audit time). Live-state citations are AWS reads taken 2026-07-10 ~19:2x–19:3x UTC.

---

## 0. TL;DR

Leg-3 "reads as CLOSED and is not" for **exactly one load-bearing reason**: the freshness gate is **BUILT + deployed + Active + actions-enabled, but has NEVER been exercised** (invariant #2's "census of survived failures" trap). The false "nightly Fargate emit" claim was **already source-confirmed UNWIRED and corrected** on 2026-07-02 (0.8.0 base, Option A). So the amendment is a **hardening + prove-it** pass, not a from-scratch build.

**Headline deliverable = EXERCISE the alarm** (drive it stale, observe OK→ALARM + SNS fire, recover). Plus: an accuracy fix to a declarative-drift comment, a LOUD host-only disclosure, and closing the downstream "terminal-lies-to-artifact" gap at the serving layer.

**Design decision for CTO~A (§4):** cloud-ship-git-tracked-3 vs host-local-all-5. **My recommendation: host-local-all-5** (already the CTO-ratified 07-08 design), for 5 grounded reasons. Presented with the cloud-ship option in full so CTO~A rules.

---

## 1. The 5 behavior sources — audit (git-tracked vs irreducibly host-only)

Ground truth via `git check-ignore` (live, this session). The emitter `tool_activity_emit.py` wires **4 source files → 5 partition-sources**:

| Partition source | Source file | `git check-ignore` | Cloud-emittable? | Emitter wiring |
|---|---|---|---|---|
| `rolling_log` | `org/compiler-tools-log.md` | **git-TRACKED** | yes (in git) | `parse_rolling_log` @ emit.py:230 |
| `rolling_log_summary` | `org/compiler-tools-log.md` | **git-TRACKED** | yes (in git) | `parse_rolling_log` @ emit.py:249 |
| `session_log` | `org/tier*/logs/**/*.md` | **git-TRACKED** | yes (in git) | `parse_session_logs` @ emit.py:340 |
| `telemetry` | `org/mcp/agent_telemetry/*.jsonl` | **GITIGNORED / host-only** | **NO** | `parse_telemetry` @ emit.py:263 |
| `rail` | `org/mcp/comp-which-rail.log` | **GITIGNORED / host-only** | **NO** | `parse_rail` @ emit.py:297 |

**Host-only = 2 of 5 partitions (2 of 4 files).** Git-tracked = 3 of 5 partitions (from 2 files).

### FINDING D-1 (declarative drift, in-scope) — the "3 of 5" claim is wrong on two counts
`tool_activity.tf:17-18 @ 1fc318f31` asserts *"3 of the 5 behavior sources (comp-which-rail.log, comproute-routing.jsonl, agent_telemetry/*.jsonl) are gitignored."* But:
1. `comproute-routing.jsonl` is **NOT a wired source** — the emitter reads only `compiler-tools-log.md`, `agent_telemetry/*.jsonl`, `comp-which-rail.log`, and session logs (`emit.py:491-494`). (`comproute-routing.jsonl` was a *proposed* leg-4 sink — see the 0.8.0~E ↔ 0.8.0 thread 07-01 — never ingested here.)
2. The true host-only count is **2 of 5 partitions**, not 3.

Same imprecise "3 of 5" text is duplicated in **three places**: `tool_activity.tf:17-18`, `tool_activity_freshness/lambda_function.py:5`, `tool_activity_emit_local.sh:6-7`. All three name the unwired `comproute-routing.jsonl`. → Fix all three to the accurate "2 of 5" + drop the unwired file (rides the chosen option).

---

## 2. The "nightly Fargate emit" claim — sweep + resolution status

**The catalog "nightly Fargate emit" does NOT exist and was already source-confirmed UNWIRED** (0.8.0 base, 2026-07-02, inbox `1.0.0_SA_CTO/read/20260702T202311Z...`): *Dockerfile CMD=`derive_runner.py` only; `tool_activity_emit.py` is NOT in the image COPY set; no EventBridge rule matches tool/activity/behavior.* The false comment was corrected the same day (Option A).

Full residual sweep (grep `nightly.*(Fargate|EventBridge)|AUTO-REFRESHES|never materialized` over `*.tf`, this session):

| Location `@ 1fc318f31` | Claim | Verdict |
|---|---|---|
| `tool_activity.tf:19-21` | *quotes* the old false claim to explain it was removed; states emit "was NEVER materialized" | **COMPLIANT** — documents the fix; asserts no live emit. Invariant #1 OK. |
| `comp_learns_producer.tf:149` | "nightly Fargate producer refresh of **comp_learns_status.json** at 04:00 UTC" | **TRUE** — verified LIVE: rule `opal-globgrph-comp-learns-producer-nightly` ENABLED cron(0 4); served JSON `LastModified 2026-07-10 04:00:59 GMT` (ran today). This is the STATUS surface, **not** the catalog. |
| `item2a.tf:2,432` | "Nightly Fargate derive-runner at 02:00 UTC" | out-of-scope (Estate plane); not asserting a tool_activity emit. |
| `stitch-produce.tf:14` | "The nightly Fargate derive-runner is REPO-LESS" | **TRUE + load-bearing** for §4 (the cloud runner has no ajb repo). |

### FINDING D-2 (sibling false claim, OUT of TO scope — flag only)
`glue_code_heat.tf:8 @ 1fc318f31` asserts the **code_heat** catalog *"AUTO-REFRESHES with the nightly emit."* But `code_heat` parquet `LastModified = 2026-07-08 18:45 GMT` — **~2 days stale right now** (same failure mode this TO fixes for tool_activity), and 0.8.0 base already flagged 07-02 that `code_heat_emit` is *"also not in the COPY set — the Change plane looks similarly seed-only."* This is the **Change plane**, not my Behavior-plane TO scope (invariant #1 binds my producer). **Flagging to CTO~A** — recommend a sibling TO; not touching it here.

**Net:** within tool_activity scope, invariant #1 ("make the claim true or delete it") is **already satisfied** by the 07-02 correction. My remaining work on it = the D-1 accuracy fix + confirm-no-regression.

---

## 3. The freshness gate — LIVE state (the real gap)

All verified live this session:

| Component | State | Evidence |
|---|---|---|
| Lambda `opal-globgrph-tool-activity-freshness` | **Active**, py3.12, 128MB/30s, LastModified 2026-07-02T21:47Z | `get-function-configuration` |
| Hourly probe rule | ENABLED, `rate(1 hour)` | `tool_activity_freshness.tf:119-123` |
| Metric `Opal/ToolActivity ParquetAgeHours` | **publishing** — age climbing ~1h/probe (last emit ~6.6h ago; all 5 partitions vintage `2026-07-10 12:51Z`) | `get-metric-statistics` |
| Alarm `opal-globgrph-tool-activity-stale` | threshold 30h, `treat_missing_data=breaching`, `ActionsEnabled=true`, → `critical_surface_alerts` SNS | `describe-alarms` |
| **Alarm state** | **OK — StateReason cites a 07-06 datapoint; NEVER transitioned to ALARM** | `describe-alarms` StateUpdated `1783356482` (2026-07-06) |

The Lambda logic (`lambda_function.py:33-66`) is **sound**: HEADs the rail parquet → age; on 404 → `age=1e6` (maximally stale, fires); `missing-data=breaching` so a dead monitor also fires. The mechanism is correct. **It has simply never been shown to fire.**

### The trap, precisely
An alarm built, wired, and left OK is indistinguishable from an alarm that *cannot* fire. Invariant #2 (AC-L3a) demands it be **exercised by going stale and OBSERVING the alarm** — the only oracle that discriminates "works" from "looks configured." That is the headline deliverable.

### FINDING D-3 (coverage — AC-L3b) — the alarm watches ONLY `rail`
The freshness Lambda HEADs `source=rail/tool_activity.parquet` only (`tool_activity_freshness.tf:21`). Since a single `emit()` run writes all 5 partitions atomically-ish (same `computed_at`), rail is a valid **sentinel** for all host-only sources today — but that "rail proxies telemetry" fact is **implicit and undisclosed**. AC-L3b wants *every host-only source disclosed with an alarm, none silently absent*. → make rail's sentinel role explicit + LOUD (§5 B2), and decide (CTO~A) whether telemetry warrants its own probe.

### FINDING D-4 (the terminal-lies mask, at the SERVING layer)
`comp_learns_produce.py:189-190 @ 1fc318f31` stamps the status JSON with **its own** `computed_at = now_ts` (produce time), and **never reads the catalog's `MAX(computed_at)` vintage**. So the nightly Fargate status producer will happily read a 5-day-stale catalog via Trino and emit a status JSON that *looks* fresh. **This is the exact "correct-but-unwired + terminal-lies-to-artifact" mask** the amendment names — one layer downstream of the catalog. The catalog freshness alarm (§3) catches host-death, but the status surface does not *carry* the catalog's staleness. → §5 B4 (coordinate w/ 0.8.0~E, who owns `comp_learns_produce.py`).

### FINDING D-5 (CTO-contract gap — host trigger doesn't git-sync)
The CTO-ratified 07-08 contract (inbox `0.7.0.../20260708T193330Z`) requires *"(1) git-fetch+sync to origin HEAD BEFORE compute."* `tool_activity_emit_local.sh @ 1fc318f31` does `git rev-parse` but **no fetch/sync** — so on a host whose checkout lags origin, the git-tracked partitions reflect a stale tree AND stamp a stale `repo_head_sha`. Small fix (add a best-effort `git fetch`+sync before the emit); flagging ownership (emitter-adjacent shell — likely 0.8.0~E authors, I wire).

---

## 4. DESIGN DECISION for CTO~A — cloud-ship-git-tracked-3 vs host-local-all-5

The amendment frames scope-1 as a per-source choice: **cloud-ship** (EventBridge→Fargate) the git-tracked sources vs **explicit-host-local-with-alarm** the host-only ones.

### Option A — host-local-all-5 (RECOMMENDED)
Keep a single host-local emitter for all 5 partitions; make the host-only constraint LOUD; prove the alarm. **Rationale (grounded):**
1. **Already CTO-ratified.** The 07-08 contract specifies a host-local session-close hook that "self-heals with fabric activity." Cloud-ship would contradict a ratified design.
2. **Single-writer = single vintage.** The parquet's parity columns `repo_head_sha`/`computed_at` (`emit.py:497-499`, `_assert_parity` fail-closed at `:436`) must be **DISTINCT-per-catalog** for the comp-drift sweep (schema docstring `emit.py:27-29`). Two writers → mixed vintages across partitions → breaks the invariant.
3. **Can never be fully cloud-fresh anyway.** 2 of 5 (rail, telemetry — the richest demand signals) are irreducibly host-only. Cloud-shipping the git-tracked 3 leaves the demand signal host-dependent; the alarm still fires on host-death regardless. Marginal value: low.
4. **The Fargate runner is REPO-LESS** (`stitch-produce.tf:14`). Cloud-shipping git-tracked sources requires the drift-producer 2-leg hybrid (GH-Action on push:CLOUD → source.zip→S3, then EventBridge→CodeBuild). Real infra for an **observability substrate** (the TO itself: *"not a served pipeline artifact"*).
5. **The incident was SILENT staleness.** The fix for *silent* is *LOUD* (the alarm) — not *survival-via-cloud*. Making the alarm provably loud closes the actual failure.

### Option B — cloud-ship-git-tracked-3 (feasible, presented fairly)
Stand up a nightly EventBridge→CodeBuild (drift-producer/stitch 2-leg pattern) that emits ONLY `rolling_log`/`rolling_log_summary`/`session_log` from a git-tracked source.zip; host emits telemetry+rail. **Makes a "nightly cloud emit" claim genuinely TRUE for the git-tracked portion.** Cost: a GH-Action workflow + OIDC role + CodeBuild + EventBridge + S3 source-zip; **must** solve the split-vintage hazard (e.g. the cloud emit writes only its 3 partitions and the comp-drift sweep is taught partitions can differ in vintage — a schema-contract change). Buys: git-tracked partitions survive host-death fresh; alarm still fires for rail/telemetry.

**My recommendation: Option A.** But this is CTO~A's arch-gate (it touches the parity-vintage invariant). Whichever is chosen, §5 B1–B5 ride it.

---

## 5. Build plan (rides CTO~A's ruling) — mapped to acceptance criteria

- **B1 — claim honesty (AC-L3a, invariant #1).** Fix D-1 "3 of 5"→"2 of 5" + drop unwired `comproute-routing.jsonl` in `tool_activity.tf`, `lambda_function.py`, `tool_activity_emit_local.sh`. Confirm no residual catalog-Fargate claim. Flag D-2 (code_heat sibling) to CTO~A.
- **B2 — LOUD host-only disclosure (AC-L3b).** Emitter prints/manifests each source's plane (host-only vs git-tracked) at emit time; make rail's sentinel role for all host-only sources explicit; (CTO~A decides telemetry's own probe).
- **B3 — EXERCISE the freshness gate (AC-L3a, headline).** Drive the REAL alarm to ALARM (PutMetricData `ParquetAgeHours`>30, or invoke the Lambda against a synthetic-stale key), OBSERVE OK→ALARM + SNS delivery, capture evidence, recover to OK. **Announced first** (a real `critical_surface_alerts` notification will fire — that's the proof).
- **B4 — close the terminal-lies gap (D-4).** The nightly status producer reads catalog `MAX(computed_at)`, stamps `catalog_vintage` + a stale flag (loud) or refuses (hard gate). Owner = 0.8.0~E (`comp_learns_produce.py`); I coordinate + wire any infra alarm on the status-vs-catalog vintage gap.
- **B5 — git-sync contract gap (D-5).** Add best-effort git fetch+sync before compute in the host trigger. Coordinate ownership.

All diffs route to CTO~A before landing. RAVC COO~A on completion.
