#!/usr/bin/env python3
"""DRAFT for MSTR review -- _ensure_commit_worker() + _commit_worker_alive() to fold into
org/mcp/server.py (MSTR's BASE_EXEC lane). Mirrors _ensure_broker() EXACTLY: health-check,
else launch the commit-worker daemon DETACHED. Wire it right AFTER the _ensure_broker() call
in the register path, so every agent session ensures the worker up -> a dead worker relaunches
within one session start (the same reliability the broker gets).

This is NOT a standalone module -- it's two functions + one call-site line to paste into
server.py. The `log`, `subprocess`, `sys`, `os`, `time`, `Path` imports already exist there.

MSTR: adapt the pid-liveness check to server.py's existing helper if you have one (the broker's
_parent_alive / _broker_health style) for platform consistency; the version below uses os.kill(0)
which is POSIX-clean but a no-op-ish on native Windows -- so it leans on the heartbeat freshness
as the primary signal (a dead worker stops refreshing worker.hb within its ~1s loop), with the
pid check as a best-effort secondary. The worker's OWN worker.pid singleton is the real
double-launch guard, so a false "alive" only costs one redundant Popen that the loser-exits.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

# In server.py these already exist; shown here for the draft to be self-contained.
_REPO = Path(__file__).resolve().parents[3]           # DRAFT loc; in server.py: parents[2]
COMMIT_WORKER = _REPO / ".tools" / "commit-worker.sh"
CQ_HB_STALE_SEC = 30


def _commit_worker_alive() -> bool:
    """True iff a live commit-worker holds worker.pid with a fresh heartbeat.
    Mirrors cq_worker_alive() in commit_queue_lib.sh (live-pid AND hb < 30s)."""
    try:
        gitdir = subprocess.check_output(
            ["git", "rev-parse", "--absolute-git-dir"], cwd=str(_REPO), text=True
        ).strip()
    except Exception:
        return False
    qroot = Path(gitdir) / "commit-queue"
    pidf, hbf = qroot / "worker.pid", qroot / "worker.hb"
    if not pidf.exists() or not hbf.exists():
        return False
    try:
        pid = int(pidf.read_text().strip())
        hb = int(hbf.read_text().strip())
    except (ValueError, OSError):
        return False
    if time.time() - hb >= CQ_HB_STALE_SEC:            # stale heartbeat -> not alive
        return False
    try:                                               # best-effort pid liveness
        os.kill(pid, 0)                                # MSTR: swap for server.py's helper on win32
        return True
    except (OSError, ProcessLookupError):
        # on native Windows os.kill(0) raises even for a live pid -> fall back to the
        # fresh-heartbeat signal we already confirmed above.
        return sys.platform == "win32"


def _ensure_commit_worker() -> bool:
    """Start the commit-worker daemon if it's not already live. Returns True if available.
    Mirrors _ensure_broker(). Race-safe: the worker's worker.pid singleton makes a concurrent
    double-launch a safe no-op. Call right AFTER _ensure_broker() in register_agent."""
    if _commit_worker_alive():
        return True
    # log.info("Starting commit-worker daemon...")     # (server.py has `log`)
    try:
        if sys.platform == "win32":
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                ["bash", str(COMMIT_WORKER), "--daemon"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS,
            )
        else:
            subprocess.Popen(
                ["bash", str(COMMIT_WORKER), "--daemon"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
        return True
    except Exception:
        # log.warning("commit-worker launch failed: %s", exc)
        return False


# ---- CALL-SITE (paste into server.py's register path, right after _ensure_broker()) ----
#   if _ensure_broker():
#       ... existing broker register ...
#   _ensure_commit_worker()   # <-- ADD: ensure the commit-queue worker is up (best-effort;
#                             #     D6 fallback-to-mutex + the WorkerDown alarm cover a miss)
#
# NB: intentionally NOT gated on SAFE_COMMIT_USE_QUEUE -- ensuring the worker is up while the
# flag is still OFF is harmless (the worker just idles on an empty queue) and means the worker
# is already warm + proven-supervised BEFORE the TO-6 canary flips the flag. Zero cost pre-flip.
