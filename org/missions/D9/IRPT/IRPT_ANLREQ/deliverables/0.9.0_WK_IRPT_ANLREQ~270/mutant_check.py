"""AR31-v-AC3 -- the one mutant of TO IRPT_ANLREQ.TO-AR-v31 (cell AR-v-31), as AMENDMENT 3 rules it.

The mutant removes the PACKAGE condition from the call gate in portal AnalysisRequestParts.tsx (useHopFailureWords): the status
call is then made for a ticket whose package is attached. The new test file is run on the mutated tree; the mutant FIRES only when
the run fails on the named test "makes no status call for a ticket whose package is attached". AnalysisRequestParts.tsx is restored
byte-for-byte in a finally block and the restore is verified by sha256 against the digest taken before the mutation.

Prints MUTANT-FIRES (exit 0) only when the mutated run failed on that test AND the restore verified.
Otherwise prints MUTANT-SURVIVES (the mutant did not fire), MUTANT-RESTORE-FAILED, or a reason, and exits 1.

Run with no arguments. The worktree root is derived from this file's own path (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>/).
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PORTAL = ROOT / "portal"
TARGET = PORTAL / "src" / "pages" / "TicketCenter" / "AnalysisRequestParts.tsx"
TEST = "src/pages/TicketCenter/__tests__/hop-failure-read.test.tsx"
GUARD = b"const wanted = enabled && ticket.ticket_type === 'analysis_request' && !ticket.package"
MUTANT = b"const wanted = enabled && ticket.ticket_type === 'analysis_request'"
FIRED_ON = "makes no status call for a ticket whose package is attached"
STRIP = re.compile(r"\x1b\[[0-9;]*m")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    original = TARGET.read_bytes()
    recorded = sha256(original)
    print("TARGET %s sha256=%s" % (TARGET.as_posix(), recorded))
    hits = original.count(GUARD)
    if hits != 1:
        print("MUTANT-SURVIVES mutation target found %d times (need exactly 1); nothing was changed" % hits)
        return 1
    bun = shutil.which("bun")
    if not bun:
        print("MUTANT-SURVIVES bun not on PATH; nothing was changed")
        return 1

    mutated_failed = False
    fired = False
    out = ""
    try:
        TARGET.write_bytes(original.replace(GUARD, MUTANT))
        print("MUTATED: the package condition removed from the call gate (the status is read for a package-attached ticket)")
        try:
            r = subprocess.run([bun, "test", TEST], cwd=str(PORTAL), capture_output=True, text=True, timeout=110)
            out = STRIP.sub("", r.stdout + r.stderr)
            mutated_failed = r.returncode != 0
            fired = mutated_failed and FIRED_ON in out
            print("MUTATED RUN rc=%d" % r.returncode)
        except subprocess.TimeoutExpired:
            print("MUTATED RUN timed out after 110 s; no verdict from the run")
    finally:
        TARGET.write_bytes(original)

    restored = TARGET.read_bytes()
    restore_ok = sha256(restored) == recorded and restored == original
    print("RESTORED sha256=%s verified=%s" % (sha256(restored), restore_ok))
    summary = [ln for ln in out.splitlines() if re.search(r"^\s*\d+ (pass|fail)$", ln)]
    print("\n".join(summary))
    if not restore_ok:
        print("MUTANT-RESTORE-FAILED %s does not match the recorded digest" % TARGET.as_posix())
        return 1
    if fired:
        print("MUTANT-FIRES the mutated run failed on %r; the restore verified" % FIRED_ON)
        return 0
    print("MUTANT-SURVIVES the mutated run did not fail on %r" % FIRED_ON)
    return 1


if __name__ == "__main__":
    sys.exit(main())
