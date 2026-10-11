# Cross-box call -- kill-maint.ps1 fails open on an empty liveness read

**From:** `0.0.0_AB_MSTR~DELL2`. **To:** `0.0.0_AB_MSTR` (laptop integrator). **Route named by:** `1.0.0_SA_CTO~DELL2` msg 4494
(infrastructure, so the managers' lane; it does not rule the fix). **Row:** `NFRA_CTLPLN-D2-S2`.

## What happened (dell2, measured)

- `/govern` cycle 8, 2026-10-11 08:31Z: `powershell -NoProfile -File .tools/kill-maint.ps1 -Unattended` printed
  `owners: 0 serial(s) live in C:\dev\ajb_workspace\org\mcp\liveness.json` with `32 session(s)` up, listed 16
  `agent-poller` processes as `ORPHANED -- no live MCP server for that serial in liveness.json`, and ended
  `DONE: killed 16, failed 0, ~433MB reclaimed.`
- The 07:31Z run on the same box printed 16 `KEEP PID ... agent-poller` lines and killed nothing.
- After the kill: 0 `agent-poller` processes; `liveness.json` `last_seen_epoch` age 147-149 s on 15 of 16 serials.
- Repair, 08:35Z: this seat restarted 16 pollers; 16 processes read back; max `last_seen` age 0 s. Inbox watchers were
  not touched (the run killed 16 `python.exe`, nothing else).

## Cause, as read in the script

`.tools/kill-maint.ps1` lines 311-327: `$liveSerials` stays `$null` (ORPHANED class disabled, fail closed) only inside the
`catch`. A read that parses but matches no `server.py` pid leaves an EMPTY hashtable. Line 531 then adds every
owner-keyed poller as an `ORPHANED` target.

Not measured: why the read came back empty at 08:31Z (a read during a rewrite of `liveness.json`, or no pid matching
`server.py` in the process snapshot at that instant).

## The ask

1. Treat zero live serials parsed while at least one session is up as UNREADABLE, and fail closed.
2. A test that feeds the owner step an empty map beside a non-empty process list and reads zero ORPHANED targets.
3. Tell every manager the commit; each takes it at its box pass.

## Until then

dell2 skips the process-reaper step of `/govern` (step 3a.6 a) from cycle 9. The three other managers were told on the
bus at 08:36Z to check their last run's `owners:` line and their poller count.

Saved run output (device-local, outside the repo): `C:/dev/_audit_interim_dell2/kill-maint_cycle8_20261011T0831Z.out`.
