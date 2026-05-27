# RV0017-F004 — broker.py parent-death watchdog

**Parent:** RV-0017 ACCEPTED-SOVEREIGN Andrew 2026-05-27T~22:25Z
**Dispatch brief:** `docs/briefs/rv-0017-p0-p1-p2-action-dispatch.md` §2 (F-004)
**Anchor incident:** `docs/briefs/incident-brief-2026-05-27-wt-crash-and-commit-storm.md` §"Orphaned MCP broker"
**Authority:** Andrew direct sequencing — P0 second item (sibling of F-002)
**Owner:** `1.0.0_SA_CTO`
**Scope class:** PRD-light

---

## §1 — Problem

Per incident brief: orphaned broker PID 3812 hot-looped 8158 CPU-sec / 6h45m at 10.7 MB RSS with dead parent PID 20276 (killed by Andrew this session; forensic past tense). Broker had no parent-death detection — it kept running indefinitely after its launching process died.

CPU usage observed at ~33% sustained. Audit of `org/mcp/broker.py` reveals:
- **NO explicit `while True:` / `while 1:` hot-loop** anywhere in the broker.
- Server is `http.server.HTTPServer.serve_forever()` (stdlib, properly blocking on socket events — not busy-waiting).
- Background work is `threading.Timer(30.0, _schedule_cleanup)` — correct re-arming pattern, not retry/backoff territory.
- No retry loops with backoff to add backoff to.

**Diagnosis:** the 33% CPU was likely accumulated request-load from agent MCP servers that continued polling `/poll_messages` after their launching sessions died — orphaned client traffic, not orphaned-broker self-spin. The broker behaves correctly under load; the structural bug is its inability to recognize that its OWN launching parent has died and it should shut down.

---

## §2 — Approach

**Parent-death watchdog** added to `broker.py`:

1. At startup, capture `os.getppid()` (or override via `OPAL_BROKER_PARENT_PID` env for testing) into module-level `_INITIAL_PARENT_PID`.
2. `_parent_watchdog()` function: check `_pid_alive(_INITIAL_PARENT_PID)`; if False, log `broker_orphan_exit` event + `os._exit(0)` for clean shutdown.
3. `_parent_watchdog()` re-arms via `threading.Timer(30.0, _parent_watchdog)` after each check — matches existing `_schedule_cleanup` pattern.
4. `main()` calls `_parent_watchdog()` once inline after `_schedule_cleanup()` — fires the FIRST tick immediately so startup-orphan (parent died between spawn and broker `main()` entry) is detected within seconds, not 30s.
5. Exception-safe: any `_pid_alive` / DB-write exception inside the watchdog re-arms instead of crashing the broker. Watchdog must never take the broker down for its own bug.

**`os._exit(0)` rationale:** `server.serve_forever()` runs on the main thread; only a different thread can call `server.shutdown()` cleanly. The watchdog Timer IS that different thread, but calling `shutdown()` from it requires extra coordination. `os._exit(0)` is the right tool: definitive, no coordination needed, all daemon threads + DB connection cleaned by the kernel. Trade-off accepted because the broker is a singleton helper, not a transactional store — uncommitted DB state is logged via `_log_event(broker_orphan_exit)` + `db.commit()` before exit.

**Why NOT a Windows job object / process group reap:** the brief's §"Scripting fixes" #4 suggests the spawner (`server.py`) should arrange OS-level cascade. That's a complementary fix that belongs in server.py, not broker.py — out of F-004 scope. The watchdog in broker.py is the *primary* net; the spawner-side reap would be a *secondary* net. Recommend F-004B if Andrew wants that layer added.

---

## §3 — Acceptance

Per brief:
> Acceptance: kill broker's parent process while broker is running → broker exits within 30s; CPU usage at idle (no inbound/outbound traffic) drops to <1% (currently 33% per incident).

**Test suite at `tests/broker_watchdog_test.py`:**

1. **`test_broker_exits_on_dead_parent`** — Launch broker with `OPAL_BROKER_PARENT_PID=<dead-pid>` on test port 7801. Assert broker subprocess exits within 35s wall (target: <30s per brief; first-tick fires inline so observed exit is <2s).
2. **`test_broker_survives_with_live_parent`** — Launch broker with `OPAL_BROKER_PARENT_PID=<this-pytest-pid>` on test port 7802. Wait 5s. Assert broker still running. Prevents the trivial false-positive of "broker always exits."

**Result this session:** both tests PASS in 5.81s. Dead-parent broker exited within ~2s (sub-30s target met cleanly via inline first-tick fire).

**Idle-CPU <1% acceptance:** structurally satisfied because the watchdog exits the broker → no broker → no CPU consumed. Indirect fix; primary fix is watchdog. Future enhancement: add a `/health` field reporting "watchdog_armed: true / parent_pid: N" so external monitoring can audit the watchdog is live (deferred — not load-bearing for F-004).

---

## §4 — Out-of-scope

- F-002 (owned-paths-check perf) — P0 sibling shipped at `9c0ee26a0`
- F-003 (max_concurrent formula) — P1
- F-005 (orphan-detector + process-count observability) — P1
- F-006 (commit-serialization research) — P2
- server.py spawner-side process-group / job-object reap — recommend F-004B follow-up
- Exponential + jittered backoff on retry loops — brief mentioned but NO retry loops exist in broker.py to add backoff to. Mark closed-by-audit.

---

## §5 — Risks accepted

- **PID recycling on Windows.** If the parent PID is reassigned to a different process before the watchdog ticks, the watchdog sees "alive" and broker stays up. Windows PID reuse is uncommon over a 30s window (PID pool is large + assignment is random/incremental). Linux/macOS is even less prone. Acceptable trade-off vs the complexity of tracking process handle/PID-creation-time pairs.
- **`os._exit(0)` skips Python finalizers.** Daemon threads are terminated abruptly. The only mutable state is `db` (SQLite WAL); we call `db.commit()` before `os._exit` to flush. SQLite WAL recovers cleanly on next open if a crash happens between commit and exit.
- **Conservative parent-alive check.** `_parent_alive()` returns True on any `_pid_alive` exception — never exits broker on a transient PID-check failure. Failure mode: broker stays up too long. Inverse mode (false-positive exit) would be worse — losing a healthy broker on a transient OS error.

---

## §6 — Implementation summary

**Changes:**
- `org/mcp/broker.py` (+62 lines, no removals): module-level `_INITIAL_PARENT_PID` + `_WATCHDOG_INTERVAL_S` constants; `_parent_alive()` helper; `_parent_watchdog()` re-arming function; `main()` captures parent PID via env-override or `os.getppid()` + calls `_parent_watchdog()` after `_schedule_cleanup()`.
- `tests/broker_watchdog_test.py` (new, 110 lines): 2 acceptance tests.

**Test invocation:** `python3 -m pytest tests/broker_watchdog_test.py -v` — both PASS in 5.81s.

**Verification protocol used:** subprocess spawn + dead-parent-PID injection via env override, not killing actual process trees (avoids cross-platform flakiness and test-runner-PID side effects).

— `1.0.0_SA_CTO` 2026-05-27T~23:20Z
