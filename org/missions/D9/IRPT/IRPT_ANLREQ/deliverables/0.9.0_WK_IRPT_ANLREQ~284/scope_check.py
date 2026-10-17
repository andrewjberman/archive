#!/usr/bin/env python3
"""AR384-y-AC3: only the two test files move between the order's base and the candidate.

Prints `SCOPE-OK` only when `git diff --name-only 4d4dc68cae cand/dell2/anlreq-test-lint-fixes` lists
exactly the two test files; otherwise `SCOPE-BAD <why>` and exit 1.
"""
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-284/portal"
BASE = "4d4dc68cae"
CAND = "cand/dell2/anlreq-test-lint-fixes"
EXPECT = sorted([
    "src/pages/TicketCenter/__tests__/filing-hint.test.tsx",
    "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx",
])


def main():
    p = subprocess.run(["git", "-C", PORTAL, "diff", "--name-only", BASE, CAND], capture_output=True)
    if p.returncode != 0:
        print(f"SCOPE-BAD git diff rc={p.returncode} for {BASE} {CAND}")
        sys.exit(1)
    got = sorted(line for line in p.stdout.decode("utf-8", "replace").splitlines() if line.strip())
    if got != EXPECT:
        print(f"SCOPE-BAD diff lists {got!r}, expected {EXPECT!r}")
        sys.exit(1)
    print("SCOPE-OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
