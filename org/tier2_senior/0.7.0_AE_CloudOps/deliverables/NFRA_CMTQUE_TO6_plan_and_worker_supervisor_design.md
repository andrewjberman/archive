# NFRA_CMTQUE TO-6 — Plan + Worker-Supervisor Design (for MSTR review)

**Author:** 0.7.0_AE_CloudOps~B · **Date:** 2026-07-06 · **Oversight:** MSTR
**Status of the wave:** TO-1/TO-3/TO-5/TO-2 LANDED (safe-commit is the enqueue-client, flag OFF); TO-4 designed; reap-synergy landed. This is the plan for TO-6 — the ONLY remaining TO.

---

## 1. TO-6 sequencing (MSTR-directed, non-negotiable ordering)

1. **WORKER SUPERVISION FIRST** (§2) — the gating prerequisite. No cutover discussion until the worker is *provably* supervised. A stuck/absent worker on the queue path = every commit hangs to the 120s timeout = fabric-wide commit outage.
2. **Load-test + completeness cases** (§3): (a) concurrency load-test vs the mutex baseline (queue must be correct AND faster under N concurrent committers); (b) fuller ~1338-caller stdout sweep; (c) the DIRECT forced-exit-1 self-scope-contamination case (CVO carry-forward).
3. **CVO-verify + CTO-consult** on the cutover (§4).
4. **CANARY the flip** (§5): `SAFE_COMMIT_USE_QUEUE=1` for ONE agent/lane first, observe a real commit cycle, then widen.
5. **SOVEREIGN paired go** — the fabric-wide flip is an **Andrew + MSTR** paired call (it changes every agent's commit path). Do NOT set the flag fabric-wide until that. `concurrency=1` stays throughout.

The flip is 100% reversible: `SAFE_COMMIT_USE_QUEUE` unset/`0` → the legacy mutex path (byte-for-byte pre-queue, the frozen `safe-commit.legacy-golden.sh` proven by the durable compat-matrix). Rollback = unset one env var.

---

## 2. Worker-supervisor design (the gating prerequisite)

**Goal:** the commit-worker daemon is *reliably present and healthy* on the repo host, so the queue path can be trusted. Mirrors the broker's own supervision (server.py `_ensure_broker` + broker.py `_parent_watchdog` + max-uptime self-restart + singleton), adapted for a bash daemon.

### 2.1 The four mechanisms (mirror of the broker)

| Broker mechanism | Commit-worker analog | Owner/lane |
|---|---|---|
| `_ensure_broker()` launch-if-down at `register_agent` | **`_ensure_commit_worker()`** — health-check `cq_worker_alive`; if down, launch the worker DETACHED (singleton-guarded). Called at the SAME point (every agent session startup). | server.py = **MSTR lane** (coordination); the launcher script = **my .tools lane** |
| Singleton by :7800 bind | `worker.pid` live-PID guard (**already built** in commit-worker.sh `cw_acquire_singleton`) | mine ✓ |
| `_parent_watchdog()` re-arming Timer | worker loop already refreshes `worker.hb`; add a self-check: if the launcher parent is gone AND the queue is idle past a bound, exit clean (orphan hygiene) | mine |
| max-uptime self-restart (`_schedule_cleanup`) | worker self-restart past `CQ_WORKER_MAX_UPTIME_S` (picks up code updates + runs the results/dlq GC cadence — `commit_queue_gc.py`) | mine |

### 2.2 Launch-if-down (`_ensure_commit_worker`) — the reliability core

The broker is kept alive because `_ensure_broker()` runs at EVERY session's `register_agent` — so a dead broker is relaunched within one session start. The commit-worker gets the identical treatment:

- **Where:** a new `_ensure_commit_worker()` in `org/mcp/server.py`, called right after `_ensure_broker()` in the register path. **MSTR lane** — I supply the function + the launcher; MSTR wires + lands it (same as the archive_messages fold). Since agents start frequently, a dead worker is relaunched within one session start — the same reliability the broker enjoys.
- **What it does (race-safe):**
  1. `cq_worker_alive` (live pid AND `worker.hb` fresh <30s) → up, return.
  2. else launch the worker via the launcher script, DETACHED (Windows `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`, stdin/out/err = DEVNULL; POSIX `start_new_session=True`) — byte-for-byte the `_ensure_broker` launch idiom.
  3. The worker's own `cw_acquire_singleton` makes a double-launch a no-op (loser exits) → race-safe even if two sessions ensure simultaneously.
- **Launcher script** (`.tools/commit-worker-launch.sh`, **my lane**): resolves the gitdir, execs `commit-worker.sh --daemon </dev/null >>logfile 2>&1` detached. Rule-16 clean (no setsid — uses the detached-Popen from the python caller, mirroring `_ensure_broker`).

### 2.3 Why supervision is load-bearing for the flip

With the flag OFF (today), a dead worker is harmless (legacy path runs). The moment the flag flips ON, `safe-commit` checks `cq_worker_alive`:
- worker UP → queue path.
- worker DOWN → **D6 fallback to the legacy mutex path** (already built in TO-2) + (TO-4) a DELIVERING WorkerDown alarm.

So even *without* a supervisor, a dead worker degrades to today (never a hard outage) — D6 is the safety net. The SUPERVISOR's job is to make "worker UP" the reliable steady state so the queue's benefits (no mutex storm) actually accrue, and so the fabric isn't silently running on the mutex fallback forever. **Supervision + D6 + the WorkerDown alarm together** are what make the flip safe: a worker death is (a) invisible to callers (D6), (b) auto-healed (ensure-if-down), (c) loud to ops (alarm).

### 2.4 Failure-mode coverage (already-built vs TO-6)

| Failure | Handling | Status |
|---|---|---|
| Worker absent at flip | D6 fallback-to-mutex + ensure-if-down relaunch | D6 built (TO-2); ensure = TO-6 |
| Worker dies mid-commit | PRE_HEAD crash-recovery (landed→recover hash, not-landed→requeue; never double-commit / never lose) | **built + proven (TO-5)** |
| Worker alive but stuck post-enqueue | client waits `SAFE_COMMIT_QUEUE_TIMEOUT` (120s) → exit 3, no blind retry, no fallback-commit (no double-commit) | **built (TO-2)** |
| Two workers race | `worker.pid` singleton guard | **built + proven (TO-1)** |
| results/dlq unbounded growth | `commit_queue_gc.py` (shared reap) on the worker cadence | **built (synergy)**; wire to worker loop = TO-6 |
| Worker orphaned (launcher gone) | parent-watchdog / max-uptime self-restart | TO-6 |

---

## 3. Load-test + completeness (phase 2)

- **Concurrency load-test vs mutex baseline:** spawn N (10, 25, 50) concurrent committers against (a) the legacy mutex path and (b) the queue path (flag-on, live worker). Measure per-commit p50/p95 tail-latency + count `exit 3` timeouts + force-fallbacks + contamination false-aborts. **AC1:** queue lands ALL commits with zero timeouts/storms and lower tail-latency than the mutex. Baseline anchor: raw-git floor ~270ms/commit (measured 2026-07-06); the mutex path adds lock-wait + gate cost under contention — that's the number the queue must beat.
- **Fuller ~1338-caller stdout sweep** (CVO carry-forward): grep the caller surface for any consumer that parses `safe-commit` stdout (CVO's spot sweep found 0; do the exhaustive pass) → confirms the queue-path synth-line is safe fabric-wide.
- **Direct forced-exit-1 contamination case** (CVO carry-forward): add to the compat-matrix. The block is by-design only reachable via a concurrent out-of-band index stage during the mutex window (baseline-IGNORE excludes pre-staged peers), so the case injects a timed concurrent `git add <stray>` into the critical section — the faithful scenario the guard defends — OR a direct unit-test of the `EXTRA = STAGED\IN_SCOPE\BASELINE` computation. Pick the robust one.

## 4. CVO-verify + CTO-consult (phase 3)

CVO re-runs the extended matrix + the load-test evidence. CTO consults on the cutover mechanics (the flag-ON path is the high-stakes moment; his commit-path-safety depth is load-bearing here). Both verdicts → MSTR.

## 5. Canary → sovereign go → fabric-wide (phases 4-5)

- Canary: set `SAFE_COMMIT_USE_QUEUE=1` for ONE lane (e.g. this executor's own `~B`), observe a full real commit cycle through the queue (enqueue → worker → result → hash), confirm the worker + supervisor + alarm all behave, for a bounded window.
- Then the **Andrew + MSTR paired sovereign go** for the fabric-wide flip. Rollback = unset the env var (instant, byte-for-byte legacy).

---

## 6. Open coordination points for MSTR

1. `_ensure_commit_worker()` in server.py is **MSTR's lane** — I supply the function + the launcher (`.tools/commit-worker-launch.sh`) as a draft (like the archive_messages fold); you wire + land it. Confirm you want it in the `register_agent` path (right after `_ensure_broker`).
2. Is a session-startup ensure sufficient, or do you also want a standalone supervisor cron/hook (belt-and-suspenders)? My rec: session-startup ensure (mirrors the broker) + the worker's own max-uptime self-restart is sufficient for v1; a dedicated supervisor is over-engineering given D6 is the safety net.
3. The flip's sovereign-go: you pair with Andrew — I execute the canary + the flip only on that paired go.

**Proposed immediate next step (on your ok):** build the worker-supervisor (the launcher script `.tools/commit-worker-launch.sh` + the `_ensure_commit_worker` draft for your fold) + prove it (kill the worker → next ensure relaunches it, singleton-safe). Then phase 2 (load-test). Holding for your steer.
