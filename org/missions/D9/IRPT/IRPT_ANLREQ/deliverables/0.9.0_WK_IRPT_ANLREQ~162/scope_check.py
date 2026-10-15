"""AR365-y-AC3 -- the scope of the candidate branch: only src/pages/TicketCenter/ paths, and the Investor Reporting and api trees empty.

Prints SCOPE-OK only when `git diff --name-only 50db1eb4 cand/dell2/anlreq-filing-notice` lists only paths under src/pages/TicketCenter/
(and at least one), and `git diff 50db1eb4 cand/dell2/anlreq-filing-notice -- src/api src/pages/InvestorReporting` is empty; otherwise
SCOPE-BAD <why>, exit 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-162/portal"
BASE = "50db1eb4"
BRANCH = "cand/dell2/anlreq-filing-notice"
ALLOWED = "src/pages/TicketCenter/"


def git(args):
    p = subprocess.run(["git", "-C", PORTAL] + args, capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def main():
    rc, out, err = git(["diff", "--name-only", BASE, BRANCH])
    if rc != 0:
        bad("git diff --name-only rc=%d: %s" % (rc, err.strip()))
    paths = [ln for ln in out.splitlines() if ln.strip()]
    if not paths:
        bad("no path changed on %s against %s" % (BRANCH, BASE))
    outside = [p for p in paths if not p.startswith(ALLOWED)]
    if outside:
        bad("paths outside %s: %s" % (ALLOWED, ", ".join(outside)))

    rc, out, err = git(["diff", BASE, BRANCH, "--", "src/api", "src/pages/InvestorReporting"])
    if rc != 0:
        bad("git diff of src/api and src/pages/InvestorReporting rc=%d: %s" % (rc, err.strip()))
    if out.strip():
        bad("src/api or src/pages/InvestorReporting changed: %d diff bytes" % len(out))

    print("SCOPE-OK %d paths, all under %s; src/api and src/pages/InvestorReporting unchanged" % (len(paths), ALLOWED))
    sys.exit(0)


if __name__ == "__main__":
    main()
