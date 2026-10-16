#!/usr/bin/env python3
"""TCKT_VNEXT round 20, cell R20-pt-1 -- the mutant check (criterion R20PT-AC3).

Changes showsMeetingOutcome so that a completed meeting ticket never shows its outcome (the old behaviour), runs the new test file
from the portal worktree, and prints MUTANT-FIRES only when that run FAILS. The source file is restored byte for byte and its sha256
is compared with the sha256 taken before the mutation. Otherwise it prints MUTANT-SURVIVES and exits 1.

Usage: python mutant_check.py   (no arguments; the workspace root and the portal worktree are derived from this file's own path)
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]  # this file sits at <root>/org/missions/D7/TCKT/TCKT_VNEXT/deliverables/<serial>/
PORTAL = ROOT / "portal"
TARGET = PORTAL / "src" / "pages" / "TicketCenter" / "MeetingRequestParts.tsx"
TEST = "src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx"
ORIGINAL = "return ticket.status !== 'completed' || Boolean(ticket.meeting)"
MUTANT = "return ticket.status !== 'completed'"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    raw = TARGET.read_bytes()
    before = sha256(raw)
    print("SHA-BEFORE %s  %s" % (before, TARGET.as_posix()))
    text = raw.decode("utf-8")
    count = text.count(ORIGINAL)
    if count != 1:
        print("MUTANT-SURVIVES anchor-count=%d (expected 1); nothing was changed" % count)
        return 1
    bun = shutil.which("bun")
    if not bun:
        print("MUTANT-SURVIVES bun not on PATH; nothing was changed")
        return 1
    mutated = text.replace(ORIGINAL, MUTANT).encode("utf-8")
    run = None
    timed_out = False
    try:
        TARGET.write_bytes(mutated)
        try:
            run = subprocess.run([bun, "test", TEST], cwd=str(PORTAL), capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            timed_out = True
    finally:
        TARGET.write_bytes(raw)
    after = sha256(TARGET.read_bytes())
    if after != before:
        print("NOT-RESTORED sha256 %s != %s -- restore by hand from git" % (after, before))
        return 2
    print("RESTORED sha256 %s (equal to SHA-BEFORE)" % after)
    if timed_out:
        print("MUTANT-SURVIVES bun test timed out at 120 s: no verdict from the run")
        return 1
    out = ANSI.sub("", run.stdout + run.stderr)
    m = re.search(r"(\d+) fail", out)
    failed = int(m.group(1)) if m else 0
    if run.returncode != 0 and failed > 0:
        print("MUTANT-FIRES rc=%d fail=%d of the new file's tests (the completed ticket's outcome is hidden)" % (run.returncode, failed))
        return 0
    print("MUTANT-SURVIVES rc=%d fail=%d: the mutated source passed the new file" % (run.returncode, failed))
    return 1


if __name__ == "__main__":
    sys.exit(main())
