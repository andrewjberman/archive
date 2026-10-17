#!/usr/bin/env python3
"""AR384-y-AC1: eslint on the two test files at cand/dell2/anlreq-test-lint-fixes.

Lints the COMMITTED blobs at the candidate branch (git show | eslint --stdin), so the verdict is the
candidate content and not whatever the worktree happens to hold. Nothing is written to the worktree.
Prints `LINT-OK 0 errors in 2 files` only when eslint reports 0 errors in both files; otherwise
`LINT-BAD <why>` and exit 1.
"""
import json
import subprocess
import sys

sys.path.insert(0, "C:/dev/wk-irpt-anlreq-284/.tools")
from git_bash_resolver import git_bash  # noqa: E402

PORTAL = "C:/dev/wk-irpt-anlreq-284/portal"
CAND = "cand/dell2/anlreq-test-lint-fixes"
FILES = [
    "src/pages/TicketCenter/__tests__/filing-hint.test.tsx",
    "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx",
]


def bad(why):
    print(f"LINT-BAD {why}")
    sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", PORTAL, *args], capture_output=True)


def main():
    bash = git_bash()
    if not bash:
        bad("no Git Bash resolved (git_bash_resolver returned None)")
    r = git("rev-parse", "--verify", "--quiet", CAND)
    if r.returncode != 0:
        bad(f"branch {CAND} not found in {PORTAL}")
    total = 0
    for path in FILES:
        blob = git("show", f"{CAND}:{path}")
        if blob.returncode != 0:
            bad(f"git show {CAND}:{path} failed rc={blob.returncode}")
        cmd = f"bun x eslint --stdin --stdin-filename {path} -f json"
        p = subprocess.run([bash, "-c", cmd], cwd=PORTAL, input=blob.stdout, capture_output=True)
        out = p.stdout.decode("utf-8", "replace")
        if p.returncode not in (0, 1):
            bad(f"eslint rc={p.returncode} on {path}")
        try:
            data = json.loads(out)
        except ValueError:
            bad(f"eslint output not JSON on {path}: {out[:200]!r}")
        if len(data) != 1:
            bad(f"eslint returned {len(data)} results for one stdin file on {path}")
        n = data[0].get("errorCount", -1)
        if n < 0:
            bad(f"no errorCount for {path}")
        total += n
    if total == 0:
        print(f"LINT-OK 0 errors in {len(FILES)} files")
        sys.exit(0)
    bad(f"{total} eslint error(s) across {len(FILES)} files at {CAND}")


if __name__ == "__main__":
    main()
