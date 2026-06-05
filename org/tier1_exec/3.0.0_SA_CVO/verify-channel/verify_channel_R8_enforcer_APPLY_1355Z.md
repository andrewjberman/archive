# /verify-channel (Mode A) — R8 universal idle-aware cap — APPLY-VERIFY (R8 is LIVE)

**archetype:** VALIDATE
**Agent:** 3.0.0_SA_CVO · 2026-06-05 ~1355Z · COO ask (`20260605T135124Z`) — complete verdict to gate Andrew apply-confirm.
**R8 STATE: LIVE.** Enforcer Lambda deployed 13:40:50Z (post R8 commit `4caa6d458` 13:18Z); runs every 5 min via EventBridge.

## Verdict: **PASS on deploy + logic + enum-structure; ONE LIVE FLAG (inf-gold) — R8 close is CONDITIONAL on AE confirming inf-gold's compute-CPU profile. Do NOT relay "false-reap risk zero" to Andrew until that resolves.**

## Mechanical (live-verified)
| Check | Evidence | Result |
|---|---|---|
| deployed == R8 code | Lambda LastModified 2026-06-05T13:40:50Z (post commit 13:18Z); env signature = universal model | MATCH |
| env vars | `IDLE_CEILING_HOURS=3.0`, `IDLE_CPU_THRESHOLD=3.0`, `MAX_RUNTIME_HOURS=0` | PASS |
| allowlists gone | NO `EXCLUDED_INSTANCES` / `IDLE_CEILING_INSTANCES` env vars present | PASS |
| idle-test logic | `all(Maximum<3% every 5-min bucket / 3h)` + Maximum-not-avg + None-on-gap + `AutoShutdown=disabled` exempt | poll-gap-safe (verify_channel_R8_enforcer_STAGED_1352Z.md) |

## Fleet enum (the sharp test) — independent live read
**Running (2):**
- `i-03343a60` demo-transform-runner — 37-39% MAX/bucket. Active, safe. ✓
- **`i-0ed5afded2ebd4ed4` inf-gold-layer-runner — LIVE FLAG.** Launched 13:00:48Z; **every 5-min bucket <3% since launch** (max 2.92% @13:00 boot, 2.71% @13:10, then flat ~0.3%); zero buckets ≥3%; AutoShutdown=null. **3h reap-mark = 16:00:48Z (~2h out).** No compute spike yet = pre-compute idle-wait (gold awaiting upstream silver/bronze). If it stays <3% to 16:00Z, R8 reaps it mid-nightly.

**Stopped:** all batch runners (bd-*, inf-bronze, inf-exporter, mdpf-daily, historical-prices x8, seeking-alpha, smartx, qa-runners). The one persistent SERVICE — `moltbot` — carries `AutoShutdown=disabled` (correctly exempt). **No untagged always-on low-CPU EC2 service exists** — COO's architectural claim (services are Lambda, not EC2) CONFIRMED. 3 spot-checked regions (us-west-2 / us-east-2 / eu-west-1) empty, corroborating the 17-region sweep.

## The inf-gold flag — disposition (CONDITIONAL, time-sensitive)
- R8 does NOT introduce new risk here: inf-gold was ALREADY under the identical W4 idle-ceiling pre-R8 (`IDLE_CEILING_INSTANCES`); R8 just universalizes the same 3h/3% logic. So if inf-gold survives normally under the prior ceiling, it survives R8.
- BUT I cannot certify it will spike >3% before 16:00:48Z. **AE owns inf-gold's profile — ASK: does inf-gold's gold compute reliably register ≥3% in ≥1 bucket before its 3h mark on a normal night, or can it run I/O-bound <3% / idle-wait-for-upstream past 16:00Z?** If the latter, it needs `AutoShutdown=disabled` OR a longer ceiling OR confirmation it self-stops first. It is running NOW, so the 16:00Z reap is live THIS run, not just tonight.
- bd-gold zero-idle-window: AE-attested (10d); bd-gold stopped now; validates tonight's nightly.

## Routing
To COO + AE (P1, time-sensitive ~2h): R8 deploy + logic + enum all sound; the ONE open item is inf-gold's live <3% profile vs its 16:00:48Z reap-mark. AE confirm-or-tag before I can call R8 false-reap-risk fully closed. Live reap behavior otherwise validates on tonight's nightly (C1, no ad-hoc).

## RESOLUTION (AE answer 14:01Z + CVO independent verify)
- **Residual CONFIRMED REAL** (not "~zero"). AE (inf-gold owner) live evidence: `i-0ed5` running `orion-gold-dispatch.sh --chain full` on `pull_inflection_performance_rest.py` = **48min wall / 12s CPU-time = network-I/O-bound**; the orion gold chain CAN legitimately sit <3% past 3h. Canonical "untagged legit I/O-bound job genuinely <3% >3h" residual class.
- **Self-shutdown VERIFIED independently** (read artifact `orion-gold-dispatch.sh:1400` auto-shutdown-after-all-modes + `:1229-1230` `sudo shutdown -h +2`, qa-tier-only skip) → `AutoShutdown=disabled` tag is SAFE (run self-terminates on completion; no always-on cost).
- **Timing corrected:** i-0ed5 logged a **7.48% bucket ~14:00Z** → spares it AT the 16:00:48Z evaluation (spike in the 3h lookback). Real danger slides to **~17:00Z+** if still running + no further spikes. Hard-deadline framing relaxed; tag still warranted (intermittent-spike reliance is fragile).
- **Mitigation routed:** (1) AE applies `AutoShutdown=disabled` on i-0ed5 (its authority; CVO verifies-not-gates infra). (2) DURABLE (R3-adjacent, ENDORSED): standing `AutoShutdown=disabled` launch tag for orion/inf gold runners — they self-shutdown, so the external reaper only risks false-reaps on I/O-bound phases.
- **R8 CLOSE STATUS:** mechanical+logic+enum PASS; close pending (a) i-0ed5 tag lands, (b) durable launch-tag policy decided. NOT a clean "risk zero" — the enum catch prevented a future-night inf-gold false-reap.

— 3.0.0_SA_CVO
