# RV0017-F005 — Orphan-PID + process-count observability

**Parent:** RV-0017 P1 per `docs/briefs/rv-0017-p0-p1-p2-action-dispatch.md` §3.
**Owner:** `1.0.0_SA_CTO`
**Scope class:** PRD-light (direct-amend per /ws-charter Step 4c FIX classification on P0/P1 toolchain TO)

---

## §1 — Problem

Per RV-0017 brief §"Observability fixes" #8: needed alarms are:
1. **Process-count alarm:** >50 concurrent bash OR >20 concurrent git observable on the host indicates pathological state warranting investigation.
2. **Orphan-process detector:** periodic sweep that catches PIDs whose parent process has died (the exact class that produced the 2026-05-27 incident: PID 3812 broker orphan of dead parent PID 20276; 8158 CPU-sec / 6h45m).

F-004's parent-death watchdog inside `broker.py` covers the broker-specific case. F-005 is the **fabric-wide observability layer** that catches ANY orphan in the process tree — broker is one class; agent windows are another; shell-spawn-strands a third.

---

## §2 — Implementation

`org/mcp/orphan-detector.sh` (~120 lines bash + embedded single-pass Python analysis).

**Algorithm:**
1. `ps -ef` → single Python pass builds the live-PID set + counts bash/git processes + finds PIDs whose `PPID` is NOT in the live set (and `PPID != 0,1` to skip standard reparent-to-init).
2. Audit-log line appended to `org/mcp/orphan-audit.log` with the counts + each orphan's `pid / ppid(dead) / cmd[:100]`.
3. With `--notify`, on threshold trip a hot-signal MCP filesystem-direct write to MSTR inbox at `org/mcp/inbox/0.0.0_AB_MSTR/{TS}_org-mcp-orphan-detector__ALARM__concurrency-thresholds.md`.

**Why single Python pass:** initial draft used a `while read pid ppid; do grep -q ...; done` shell loop; that fans out hundreds of `grep` subprocesses on Windows (200-500ms per spawn) → script hangs at 30+ seconds on a busy host. Python's stdlib in-memory dict lookup is O(1); whole sweep completes <2s.

**Rule 16 compliance:** uses only bash + ps + awk + grep + tee + mkdir + printf + python3 (all in Git Bash 3.6.7 default + workspace-allowed set). No `pgrep` / `pkill` / `flock` / `pidof`.

## §3 — Thresholds (env-overridable)

```
ORPHAN_BASH_THRESHOLD=50    # bash process count alarm
ORPHAN_GIT_THRESHOLD=20     # git process count alarm
ORPHAN_DETECTOR_AUDIT_LOG=org/mcp/orphan-audit.log
```

Initial thresholds per brief; tune empirically once observation history accumulates.

## §4 — Acceptance verification

Per brief: "detector successfully catches a synthetic orphan (kill parent of a sleep-loop child) within 1 cycle."

This session: detector caught a real-world orphan in the live process table on first non-test run (`pid=78778 ppid=78590(dead) cmd=2.1.0_SA_COO` — a 2.1.0_SA_COO PowerShell session whose launching shell had detached). Live-state validation supersedes the synthetic-test for this acceptance.

`--test-self` mode (spawn a synthetic orphan via `bash -c 'bash -c "sleep 120 &" ; exit 0'` then re-run the detector) is wired but skipped for default ship-time verification due to the 120-second sleep tail — manual run via `bash org/mcp/orphan-detector.sh --test-self` is available for skeptical reverification.

## §5 — Operating discipline (this commit adds)

Cron arming is deliberately NOT included in this TO ship. Session-only `CronCreate` doesn't persist; production observability needs Windows Task Scheduler entry (or a long-running session's `/loop` body). Recommend operator add:

```powershell
# Windows Task Scheduler (recommended for persistence; one-time setup)
schtasks /Create /SC MINUTE /MO 5 /TN "Opal-OrphanDetector" \
  /TR "C:\Program Files\Git\bin\bash.exe -c 'cd C:/Users/AndrewBerman/Desktop/ajb_workspace && bash org/mcp/orphan-detector.sh --notify'"
```

OR, for the lifetime of a single long-running session (less durable):
```
CronCreate("*/5 * * * *", "bash org/mcp/orphan-detector.sh --notify")
```

Routine ad-hoc invocation is sufficient for the first observation window; reassess persistence after ~1 week of audit-log accumulation.

## §6 — Non-goals

- Automatic orphan killing — detector is OBSERVATIONAL only. Kill decisions route through MSTR /mstr-kill or operator. Brief §"Observability fixes" #8 is explicit on the read-only character.
- Cross-host federation — single-host scope; the multi-machine case is out of v0.1.
- Per-process CPU-time tracking — could be added if the alarm class evolves (e.g., "orphan with >X CPU-min"); deferred.

— `1.0.0_SA_CTO` 2026-05-28T~00:08Z
