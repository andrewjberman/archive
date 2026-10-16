#!/usr/bin/env python3
"""AR-y-378 AC3: only the upload call and the Ticket Center may move.

Prints SCOPE-OK only when the candidate branch's changed paths (against the DEV base fcbf2bce) are all under
src/pages/TicketCenter/ or are src/api/endpoints/investor-reporting.ts, there is at least one, and the diff of
src/pages/InvestorReporting against the base is empty. Otherwise SCOPE-BAD <why> and exit 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-170/portal"
BASE = "fcbf2bce"
BRANCH = "cand/dell2/anlreq-advisor-login-email"
UPLOAD_FILE = "src/api/endpoints/investor-reporting.ts"
TICKET_PREFIX = "src/pages/TicketCenter/"


def git(*args):
    proc = subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError("git %s rc=%s: %s" % (" ".join(args), proc.returncode, (proc.stderr or "").strip()[:200]))
    return proc.stdout


def main():
    try:
        names = [line.strip() for line in git("diff", "--name-only", BASE, BRANCH).splitlines() if line.strip()]
        invest = git("diff", BASE, BRANCH, "--", "src/pages/InvestorReporting")
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print("SCOPE-BAD %s" % exc)
        return 1
    if not names:
        print("SCOPE-BAD the branch changes no path against %s" % BASE)
        return 1
    outside = [p for p in names if not (p.startswith(TICKET_PREFIX) or p == UPLOAD_FILE)]
    if outside:
        print("SCOPE-BAD paths outside the grant: %s" % ", ".join(outside))
        return 1
    if invest.strip():
        print("SCOPE-BAD the diff of src/pages/InvestorReporting against %s is not empty" % BASE)
        return 1
    print("SCOPE-OK %d paths, all under %s or %s; src/pages/InvestorReporting diff empty" % (len(names), TICKET_PREFIX, UPLOAD_FILE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
