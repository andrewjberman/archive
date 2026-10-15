"""AR365-y-AC2 -- the one mutant: the notice rendering removed from the changed file, one bun run of the new test file, restored by sha256.

The mutant swaps the guard of FilingNotice so the component renders nothing for any input (`lines.length >= 0` in place of
`lines.length === 0`). MUTANT-FIRES only when that run FAILS; MUTANT-SURVIVES otherwise, exit 1. The original bytes are
restored and their sha256 is checked after the run.
"""
import hashlib
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-162/portal"
TARGET = PORTAL + "/src/pages/TicketCenter/AnalysisRequestParts.tsx"
NEW_FILE = "src/pages/TicketCenter/__tests__/filing-notice.test.tsx"
ANCHOR = b"if (lines.length === 0) return null"
MUTANT = b"if (lines.length >= 0) return null"
TIMEOUT_S = 300


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    bun = shutil.which("bun")
    if bun is None:
        print("MUTANT-SURVIVES bun is not on PATH")
        sys.exit(1)
    with open(TARGET, "rb") as fh:
        original = fh.read()
    original_sha = sha(original)
    hits = original.count(ANCHOR)
    if hits != 1:
        print("MUTANT-SURVIVES anchor found %d times, expected 1; no mutant written" % hits)
        sys.exit(1)
    mutated = original.replace(ANCHOR, MUTANT)
    result = None
    try:
        with open(TARGET, "wb") as fh:
            fh.write(mutated)
        try:
            p = subprocess.run([bun, "test", NEW_FILE], cwd=PORTAL, capture_output=True, text=True, timeout=TIMEOUT_S)
            result = (p.returncode, p.stdout + p.stderr)
        except subprocess.TimeoutExpired:
            result = (124, "timeout")
    finally:
        with open(TARGET, "wb") as fh:
            fh.write(original)
    with open(TARGET, "rb") as fh:
        restored_sha = sha(fh.read())
    if restored_sha != original_sha:
        print("MUTANT-SURVIVES restore check failed: sha256 %s != %s" % (restored_sha, original_sha))
        sys.exit(1)
    rc, text = result
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    summary = [ln.strip() for ln in text.splitlines() if ln.strip().endswith(("pass", "fail"))]
    if rc != 0:
        print("MUTANT-FIRES mutant rc=%d; restored sha256 %s matches; summary: %s" % (rc, restored_sha[:16], " | ".join(summary[-2:])))
        sys.exit(0)
    print("MUTANT-SURVIVES mutant run passed (rc=0); restored sha256 %s matches" % restored_sha[:16])
    sys.exit(1)


if __name__ == "__main__":
    main()
