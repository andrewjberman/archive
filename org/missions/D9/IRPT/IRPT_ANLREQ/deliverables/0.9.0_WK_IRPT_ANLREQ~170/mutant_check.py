#!/usr/bin/env python3
"""AR-y-378 AC2: the one mutant that must fail.

The mutant leaves the advisor_email member out of the upload call in src/api/endpoints/investor-reporting.ts. The changed
file is swapped in for one bun run of the new test file and restored byte for byte, checked by sha256. Prints MUTANT-FIRES
only when that run FAILS; otherwise MUTANT-SURVIVES and exit 1.
"""
import hashlib
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-170/portal"
TARGET = PORTAL + "/src/api/endpoints/investor-reporting.ts"
NEW_FILE = "src/pages/TicketCenter/__tests__/advisor-email.test.tsx"
MEMBER = b", ...(advisorEmail === undefined ? {} : { advisor_email: advisorEmail })"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def ascii_only(text):
    return "".join(ch if ord(ch) < 128 else "?" for ch in text)


def main():
    with open(TARGET, "rb") as handle:
        original = handle.read()
    original_sha = sha256(original)
    if original.count(MEMBER) != 1:
        print("MUTANT-SURVIVES the member is not found exactly once in the upload call (count=%d)" % original.count(MEMBER))
        return 1
    mutant = original.replace(MEMBER, b"", 1)
    if sha256(mutant) == original_sha:
        print("MUTANT-SURVIVES the mutant did not change the file")
        return 1
    binary = shutil.which("bun") or "bun"
    rc = None
    summary = ""
    try:
        with open(TARGET, "wb") as handle:
            handle.write(mutant)
        proc = subprocess.run([binary, "test", NEW_FILE], cwd=PORTAL, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=300)
        rc = proc.returncode
        lines = [line.strip() for line in ascii_only((proc.stdout or "") + (proc.stderr or "")).splitlines() if line.strip()]
        summary = " | ".join(lines[-3:])[:500]
    except subprocess.TimeoutExpired:
        rc = -1
        summary = "timeout 300 s"
    finally:
        with open(TARGET, "wb") as handle:
            handle.write(original)
    with open(TARGET, "rb") as handle:
        restored_sha = sha256(handle.read())
    if restored_sha != original_sha:
        print("MUTANT-SURVIVES restore check failed: sha256 %s != %s" % (restored_sha, original_sha))
        return 1
    if rc is not None and rc != 0:
        print("MUTANT-FIRES bun test of the new file failed with the advisor_email member removed (rc=%s); "
              "restored sha256 ok %s; tail: %s" % (rc, original_sha[:16], summary))
        return 0
    print("MUTANT-SURVIVES the new file passed with the member removed (rc=%s); restored sha256 ok %s" % (rc, original_sha[:16]))
    return 1


if __name__ == "__main__":
    sys.exit(main())
