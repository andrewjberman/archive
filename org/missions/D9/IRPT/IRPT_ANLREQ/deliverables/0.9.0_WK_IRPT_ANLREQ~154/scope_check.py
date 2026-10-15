"""AR-y-354 criterion AR354-y-AC3: the candidate changes only src/pages/TicketCenter/ and nothing under the two named folders.

Prints SCOPE-OK <n> paths when (1) every path in git diff --name-only a6b83f692084 <candidate> is under src/pages/TicketCenter/
(and there is at least one), and (2) git diff a6b83f692084 <candidate> -- src/pages/InvestorReporting src/api is empty.
Otherwise SCOPE-BAD <why>, exit 1. ASCII output only.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-154/portal"
BASE = "a6b83f692084"
BRANCH = "cand/dell2/anlreq-filing-hint-keep-equal-pair"
PREFIX = "src/pages/TicketCenter/"


def git(*args):
    return subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True, timeout=120)


def main():
    names = git("diff", "--name-only", BASE, BRANCH)
    if names.returncode != 0:
        print("SCOPE-BAD git diff --name-only rc=%d: %s" % (names.returncode, names.stderr.strip()))
        sys.exit(1)
    paths = [p for p in names.stdout.splitlines() if p.strip()]
    if not paths:
        print("SCOPE-BAD the candidate branch changes no path against the base")
        sys.exit(1)
    outside = [p for p in paths if not p.startswith(PREFIX)]
    if outside:
        print("SCOPE-BAD paths outside %s: %s" % (PREFIX, ", ".join(outside)))
        sys.exit(1)
    named = git("diff", BASE, BRANCH, "--", "src/pages/InvestorReporting", "src/api")
    if named.returncode != 0:
        print("SCOPE-BAD git diff on the named folders rc=%d: %s" % (named.returncode, named.stderr.strip()))
        sys.exit(1)
    if named.stdout.strip():
        print("SCOPE-BAD the diff touches src/pages/InvestorReporting or src/api")
        sys.exit(1)
    print("SCOPE-OK %d paths, all under %s; src/pages/InvestorReporting and src/api unchanged" % (len(paths), PREFIX))
    sys.exit(0)


if __name__ == "__main__":
    main()
