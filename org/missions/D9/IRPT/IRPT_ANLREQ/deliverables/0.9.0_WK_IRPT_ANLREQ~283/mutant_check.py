"""AR383-y-AC2: the mutant. reportRefBody put back to the numeric conversion, one bun run of the new test file, then restore.

The changed file is swapped for the mutant, the new test file is run once, and the original bytes are restored with a
sha256 check. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES, exit 1.
"""
import hashlib
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-283/portal"
TARGET = PORTAL + "/src/pages/TicketCenter/analysisRequest.ts"
NEW_FILE = "src/pages/TicketCenter/__tests__/report-ref-revision-string.test.tsx"
TIMEOUT = 120

GOOD = "{ revision: String(requestRevision) }"
MUTANT = "{ revision: Number.isFinite(Number(requestRevision)) ? Number(requestRevision) : requestRevision }"

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
FAIL_RE = re.compile(r"^\s*(\d+) fail\s*$", re.M)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    with open(TARGET, "rb") as fh:
        original = fh.read()
    original_sha = sha256(original)
    text = original.decode("utf-8")
    if text.count(GOOD) != 1:
        print("MUTANT-SURVIVES the good line is not found exactly once (count=%d)" % text.count(GOOD))
        return 1
    mutated = text.replace(GOOD, MUTANT).encode("utf-8")
    exe = shutil.which("bun")
    if exe is None:
        print("MUTANT-SURVIVES bun not on PATH")
        return 1
    rc = None
    fails = None
    try:
        with open(TARGET, "wb") as fh:
            fh.write(mutated)
        try:
            proc = subprocess.run([exe, "test", NEW_FILE], cwd=PORTAL, capture_output=True, timeout=TIMEOUT)
            rc = proc.returncode
            out = ANSI.sub("", (proc.stdout + proc.stderr).decode("utf-8", errors="replace"))
            found = FAIL_RE.findall(out)
            fails = int(found[-1]) if found else None
        except subprocess.TimeoutExpired:
            rc = 124
    finally:
        with open(TARGET, "wb") as fh:
            fh.write(original)
    with open(TARGET, "rb") as fh:
        restored_sha = sha256(fh.read())
    if restored_sha != original_sha:
        print("MUTANT-SURVIVES restore failed: sha256 %s != %s" % (restored_sha, original_sha))
        return 1
    if rc != 0 and fails is not None and fails > 0:
        print("MUTANT-FIRES new test file rc=%s fail=%s on the numeric-conversion mutant; restored sha256 %s" % (rc, fails, restored_sha))
        return 0
    print("MUTANT-SURVIVES new test file rc=%s fail=%s on the numeric-conversion mutant" % (rc, fails))
    return 1


if __name__ == "__main__":
    sys.exit(main())
