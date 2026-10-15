"""AR-y-363 criterion AR363-y-AC3: the candidate branch touches only src/pages/TicketCenter/ in the portal repository.

Prints SCOPE-OK only when `git -C <portal> diff --name-only origin/PROD cand/dell2/anlreq-filing-decision-tree` lists only paths
under src/pages/TicketCenter/, and `git diff origin/PROD cand/dell2/anlreq-filing-decision-tree -- src/api src/pages/InvestorReporting`
is empty. Otherwise prints SCOPE-BAD <why> and exits 1. ASCII output only.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-160/portal"
BASE = "origin/PROD"
CANDIDATE = "cand/dell2/anlreq-filing-decision-tree"
FOLDER = "src/pages/TicketCenter/"
READ_ONLY = ["src/api", "src/pages/InvestorReporting"]


def git(*args):
    proc = subprocess.run(["git", "-C", PORTAL] + list(args), capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def main():
    rc, out, err = git("diff", "--name-only", BASE, CANDIDATE)
    if rc != 0:
        bad("git diff --name-only failed rc=%d: %s" % (rc, err.strip()))
    paths = [p for p in out.splitlines() if p.strip()]
    if not paths:
        bad("no changed paths listed for %s against %s" % (CANDIDATE, BASE))
    outside = [p for p in paths if not p.startswith(FOLDER)]
    if outside:
        bad("paths outside %s: %s" % (FOLDER, ", ".join(outside)))
    rc, out, err = git("diff", BASE, CANDIDATE, "--", *READ_ONLY)
    if rc != 0:
        bad("git diff of the read-only folders failed rc=%d: %s" % (rc, err.strip()))
    if out.strip():
        bad("the read-only folders carry %d diff lines" % len(out.splitlines()))
    print("SCOPE-OK %d paths, all under %s; %s unchanged" % (len(paths), FOLDER, " and ".join(READ_ONLY)))
    sys.exit(0)


if __name__ == "__main__":
    main()
