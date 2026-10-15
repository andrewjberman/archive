"""R18P2-AC3 -- the scope of the Trade Request candidate, for the approver who reads a client-facing page candidate that unwires an engine call.

Prints SCOPE-OK only when all three hold for the candidate branch against base_tip:
  1. the changed paths are exactly the step-2 paths of this order plus the files TO-R18-P1 inherits (the meeting files, and the two
     files both orders touch);
  2. no changed path under src/ is outside src/pages/TicketCenter/ except src/api/endpoints/tickets.ts;
  3. the candidate tree holds no occurrence of submitTradeBody under src/pages/TicketCenter/ (git grep exits 1 for none).
Otherwise prints SCOPE-BAD <why> and exits 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-tckt-vnext-42/portal"
BASE_TIP = "9e637fe51ebfa6322910cc032945a1e755e9ea13"
CANDIDATE = "cand/dell2/tckt-trade-form-upload"
EXPECTED = sorted([
    "src/api/endpoints/tickets.ts",
    "src/pages/TicketCenter/MeetingRequestParts.tsx",
    "src/pages/TicketCenter/TicketCenter.tsx",
    "src/pages/TicketCenter/TradeRequestParts.tsx",
    "src/pages/TicketCenter/__tests__/meeting-request.test.tsx",
    "src/pages/TicketCenter/__tests__/trade-form-upload.test.tsx",
    "src/pages/TicketCenter/__tests__/trade-request.test.tsx",
])
ALLOWED_PREFIX = "src/pages/TicketCenter/"
ALLOWED_OUTSIDE = "src/api/endpoints/tickets.ts"
FORBIDDEN_SYMBOL = "submitTradeBody"


def git(*args, ok_codes=(0,)):
    proc = subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=60)
    if proc.returncode not in ok_codes:
        print("SCOPE-BAD git %s rc=%s %s" % (" ".join(args), proc.returncode, proc.stderr.strip()[:200]))
        sys.exit(1)
    return proc.returncode, proc.stdout


def main():
    _, out = git("diff", "--name-only", BASE_TIP, CANDIDATE)
    paths = sorted(line.strip() for line in out.splitlines() if line.strip())
    if paths != EXPECTED:
        print("SCOPE-BAD changed paths differ from the seven named: got %s" % paths)
        sys.exit(1)
    outside = [p for p in paths if p.startswith("src/") and not p.startswith(ALLOWED_PREFIX) and p != ALLOWED_OUTSIDE]
    if outside:
        print("SCOPE-BAD src/ paths outside the allowed folder: %s" % outside)
        sys.exit(1)
    rc, hits = git("grep", "-n", FORBIDDEN_SYMBOL, CANDIDATE, "--", "src/pages/TicketCenter", ok_codes=(0, 1))
    if rc == 0:
        print("SCOPE-BAD %s is still referenced under src/pages/TicketCenter: %s" % (FORBIDDEN_SYMBOL, hits.strip()[:160]))
        sys.exit(1)
    print("SCOPE-OK 7 of 7 named paths; src/ changes only under src/pages/TicketCenter/ and tickets.ts; "
          "0 references to %s under src/pages/TicketCenter/" % FORBIDDEN_SYMBOL)
    sys.exit(0)


if __name__ == "__main__":
    main()
