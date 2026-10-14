"""AR317-y-AC3 -- scope of the portal candidate (TO-AR-y-317, worker 0.9.0_WK_IRPT_ANLREQ~127).

Prints SCOPE-OK only when `git diff --name-only origin/PROD <candidate>` is exactly the three source paths of the cell,
and `git diff origin/PROD <candidate> -- src/pages/InvestorReporting/tabs` is empty (the Opal-internal tab is untouched).
Otherwise prints SCOPE-BAD <why> and exits 1. Read-only: no fetch, no push, no checkout.
"""
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-127/portal"
CANDIDATE = "cand/dell2/anlreq-commentary-always-requested"
EXPECTED = {
    "src/pages/TicketCenter/analysisRequest.ts",
    "src/pages/InvestorReporting/contracts/submission-request.ts",
    "src/pages/TicketCenter/__tests__/analysis-commentary-always-requested.test.ts",
}
TABS = "src/pages/InvestorReporting/tabs"


def git(args):
    git_bin = shutil.which("git")
    if git_bin is None:
        return None, "git is not on PATH"
    try:
        proc = subprocess.run([git_bin, "-C", PORTAL] + args, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, "git timed out"
    out = proc.stdout.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        return None, "git rc=%d: %s" % (proc.returncode, proc.stderr.decode("utf-8", errors="replace").strip())
    return out, None


def main():
    names, err = git(["diff", "--name-only", "origin/PROD", CANDIDATE])
    if err:
        print("SCOPE-BAD " + err)
        return 1
    paths = set(line.strip() for line in names.splitlines() if line.strip())
    if paths != EXPECTED:
        print("SCOPE-BAD changed paths are %s; expected exactly %s" % (sorted(paths), sorted(EXPECTED)))
        return 1
    tabs, err = git(["diff", "origin/PROD", CANDIDATE, "--", TABS])
    if err:
        print("SCOPE-BAD " + err)
        return 1
    if tabs.strip():
        print("SCOPE-BAD the Opal-internal tab differs from origin/PROD")
        return 1
    print("SCOPE-OK %d paths: %s; tabs diff empty" % (len(paths), ", ".join(sorted(paths))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
