"""NFRA_IDENTITY.G-A -- replay falsifier + no-regression exercise for the broker PID guard.

Exercises the REAL guard (`server._identity_conflict` / `_pid_alive`) against the
liveness shapes the broker actually stores. Rule 22a: acceptance rests on the guard
FIRING/PASSING, not on reading the code.

  AC1 REPLAY FALSIFIER -- the 2026-07-12/13 SEV, replayed: a session live+registered
       as 1.0.0_SA_CTO (PID 2508) claims 0.8.0_AE_CloudComp -> MUST refuse + name the
       conflict. Falsifier: it registers silently (the pre-guard behaviour).
  AC2 NO-REGRESSION -- (a) same serial + same PID (routine re-register/heartbeat) and
       (b) same serial + FRESH PID after a restart, incumbent process DEAD -> MUST pass.
       Falsifier: the guard refuses a legitimate re-registration (would break every
       agent's startup fabric-wide).
  AC3 SERIAL-HELD -- claimed serial is held by a DIFFERENT, STILL-ALIVE process ->
       MUST refuse (this is what protected the real 0.8.0 lane from the phantom).
  AC4 FAIL-OPEN -- an incumbent whose PID is dead must NOT block (covered by AC2b).

Run: python org/mcp/test_identity_guard.py
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server  # noqa: E402  (the real broker module)

NOW = time.time()
MY_PID = os.getpid()          # a PID that is definitely ALIVE (this process)
DEAD_PID = 999999             # a PID that is definitely not running


def live(pid, secs_ago=3):
    return {"pid": pid, "last_seen_epoch": NOW - secs_ago, "summary": ""}


def check(name, got_conflict, want_conflict, detail=""):
    ok = bool(got_conflict) == want_conflict
    print(("  PASS " if ok else "  FAIL ") + name)
    if detail:
        print("        " + detail)
    if got_conflict:
        print("        -> " + got_conflict.splitlines()[0][:110])
    return ok


def main():
    results = []
    print("NFRA_IDENTITY.G-A -- broker PID identity guard, exercised\n")

    # --- AC1: THE REPLAY FALSIFIER (the actual SEV) ---------------------------
    # A session running as 1.0.0_SA_CTO at THIS pid claims 0.8.0_AE_CloudComp.
    print("AC1 REPLAY FALSIFIER (the 07-12/13 SEV):")
    sev = {"1.0.0_SA_CTO": live(MY_PID, 3), "0.8.0_AE_CloudComp": live(20004, 5)}
    c = server._identity_conflict("0.8.0_AE_CloudComp", sev, MY_PID)
    results.append(check("PID live as 1.0.0_SA_CTO claims 0.8.0 -> REFUSED",
                         c, True, "the phantom's FIRST registration names the collision"))

    # --- AC2: NO-REGRESSION (the load-bearing one) ---------------------------
    print("\nAC2 NO-REGRESSION (must NOT refuse legitimate registrations):")
    same = {"0.7.0_AE_CloudOps~A": live(MY_PID, 2)}
    c = server._identity_conflict("0.7.0_AE_CloudOps~A", same, MY_PID)
    results.append(check("same serial + same PID (routine re-register/heartbeat) -> ALLOWED",
                         c, False))

    # restart: same serial, FRESH pid; the incumbent entry is still fresh BUT its
    # process is DEAD. A freshness-only guard would refuse this and break the fabric.
    restart = {"0.7.0_AE_CloudOps~A": live(DEAD_PID, 5)}
    c = server._identity_conflict("0.7.0_AE_CloudOps~A", restart, MY_PID)
    results.append(check("same serial + fresh PID after restart (incumbent DEAD) -> ALLOWED",
                         c, False, "the discriminator: incumbent process is gone, not a conflict"))

    # a brand-new serial nobody holds
    c = server._identity_conflict("0.7.0_AE_CloudOps~A", {}, MY_PID)
    results.append(check("first registration, empty liveness -> ALLOWED", c, False))

    # a STALE incumbent under my own serial (quiet > STALE_THRESHOLD) must not block
    stale = {"0.7.0_AE_CloudOps~A": live(DEAD_PID, server.STALE_THRESHOLD + 60)}
    c = server._identity_conflict("0.7.0_AE_CloudOps~A", stale, MY_PID)
    results.append(check("stale incumbent under same serial -> ALLOWED", c, False))

    # --- AC3: SERIAL HELD BY A DIFFERENT *LIVE* PROCESS ----------------------
    print("\nAC3 SERIAL-HELD (protects the real lane from a phantom):")
    held = {"0.8.0_AE_CloudComp": live(MY_PID, 2)}   # MY_PID is alive -> a real holder
    c = server._identity_conflict("0.8.0_AE_CloudComp", held, 424242)
    results.append(check("claimed serial held by a LIVE different PID -> REFUSED", c, True))

    # --- RESIDUAL RISK (documented, not hidden): the fast-respawn window ------
    # If a session DIES but its MCP-server process LINGERS (orphan) and its last
    # heartbeat is still inside STALE_THRESHOLD, a respawn of the SAME serial
    # inside that window is REFUSED by direction-2. Evidence this is narrow: an
    # MCP server DOES exit on session end (3.0.0_SA_CVO~A pid 7704 -> pid_alive
    # False after its session ended), so pid_alive is False on the normal path and
    # the respawn passes. The window only opens for a lingering-orphan process
    # inside 120s. Surfaced to CTO (arch-gate) rather than silently chosen:
    # a hard refuse here protects the real lane from a phantom; an advisory would
    # never block a respawn. This test PINS the current behaviour either way.
    print("\nRESIDUAL (documented): respawn inside 120s while the dead session's")
    print("process still lingers (orphan) -- direction-2 currently REFUSES:")
    linger = {"0.7.0_AE_CloudOps~A": live(MY_PID, 30)}  # 'MY_PID' stands in for a lingering proc
    c = server._identity_conflict("0.7.0_AE_CloudOps~A", linger, 555555)
    print("  behaviour: " + ("REFUSE" if c else "ALLOW") + "  (pinned; CTO rules hard-vs-advisory)")

    # --- AC4: the pid-liveness primitive itself ------------------------------
    print("\nAC4 _pid_alive primitive (the discriminator that saves restarts):")
    alive_ok = server._pid_alive(MY_PID) is True
    dead_ok = server._pid_alive(DEAD_PID) is False
    print(("  PASS " if alive_ok else "  FAIL ") + f"_pid_alive(self={MY_PID}) is True")
    print(("  PASS " if dead_ok else "  FAIL ") + f"_pid_alive({DEAD_PID}) is False")
    results.extend([alive_ok, dead_ok])

    print("\n" + "=" * 64)
    if all(results):
        print(f"ALL {len(results)} CHECKS PASS -- guard refuses the cross, never the restart.")
        return 0
    print(f"FAILURES: {results.count(False)} of {len(results)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
