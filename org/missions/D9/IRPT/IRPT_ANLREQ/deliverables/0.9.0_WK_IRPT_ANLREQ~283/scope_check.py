"""AR383-y-AC3: the candidate touches only the record body and its type.

Prints SCOPE-OK only when git diff --name-only 4d4dc68cae cand/dell2/anlreq-report-ref-revision-string lists only
src/pages/TicketCenter/analysisRequest.ts, src/api/endpoints/tickets.ts and paths under src/pages/TicketCenter/__tests__/
(and at least one path); otherwise SCOPE-BAD <why>, exit 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-283/portal"
BASE = "4d4dc68cae"
BRANCH = "cand/dell2/anlreq-report-ref-revision-string"
ALLOWED_EXACT = {
    "src/pages/TicketCenter/analysisRequest.ts",
    "src/api/endpoints/tickets.ts",
}
ALLOWED_PREFIX = "src/pages/TicketCenter/__tests__/"


def main():
    try:
        proc = subprocess.run(
            ["git", "-C", PORTAL, "diff", "--name-only", BASE, BRANCH],
            capture_output=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("SCOPE-BAD git diff timed out (rc 124)")
        return 1
    if proc.returncode != 0:
        print("SCOPE-BAD git diff rc=%s: %s" % (proc.returncode, proc.stderr.decode("utf-8", errors="replace").strip()))
        return 1
    names = [line.strip() for line in proc.stdout.decode("utf-8", errors="replace").splitlines() if line.strip()]
    if not names:
        print("SCOPE-BAD the diff lists no paths (denominator 0)")
        return 1
    bad = [n for n in names if n not in ALLOWED_EXACT and not n.startswith(ALLOWED_PREFIX)]
    if bad:
        print("SCOPE-BAD paths outside the grant: %s" % ", ".join(bad))
        return 1
    print("SCOPE-OK %d paths: %s" % (len(names), ", ".join(names)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
