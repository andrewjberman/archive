"""R18P1-AC3 -- the candidate's scope, for the approver who reads a client-facing page candidate.

Prints SCOPE-OK only when the candidate branch differs from base_tip in exactly the four paths of the cell, and the diff of
TicketCenter.tsx adds no line that mentions trade_request, TradeRequestForm or analysis_request. Otherwise SCOPE-BAD <why>, exit 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-tckt-vnext-42/portal"
BASE_TIP = "9e637fe51ebfa6322910cc032945a1e755e9ea13"
CANDIDATE = "cand/dell2/tckt-meeting-request"
EXPECTED = sorted([
    "src/api/endpoints/tickets.ts",
    "src/pages/TicketCenter/MeetingRequestParts.tsx",
    "src/pages/TicketCenter/TicketCenter.tsx",
    "src/pages/TicketCenter/__tests__/meeting-request.test.tsx",
])
TICKET_CENTER = "src/pages/TicketCenter/TicketCenter.tsx"
FORBIDDEN = ("trade_request", "TradeRequestForm", "analysis_request")


def git(*args):
    proc = subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=60)
    if proc.returncode != 0:
        print("SCOPE-BAD git %s rc=%s %s" % (" ".join(args), proc.returncode, proc.stderr.strip()[:200]))
        sys.exit(1)
    return proc.stdout


def main():
    paths = sorted(line.strip() for line in git("diff", "--name-only", BASE_TIP, CANDIDATE).splitlines() if line.strip())
    if paths != EXPECTED:
        print("SCOPE-BAD paths differ from the four named: got %s" % paths)
        sys.exit(1)
    diff = git("diff", "-U0", BASE_TIP, CANDIDATE, "--", TICKET_CENTER)
    added = [line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
    hits = [line for line in added if any(tok in line for tok in FORBIDDEN)]
    if hits:
        print("SCOPE-BAD %d added TicketCenter.tsx line(s) mention a forbidden token: %s" % (len(hits), hits[0].strip()[:120]))
        sys.exit(1)
    print("SCOPE-OK 4 of 4 named paths; TicketCenter.tsx %d added lines, 0 mention %s" % (len(added), ", ".join(FORBIDDEN)))
    sys.exit(0)


if __name__ == "__main__":
    main()
