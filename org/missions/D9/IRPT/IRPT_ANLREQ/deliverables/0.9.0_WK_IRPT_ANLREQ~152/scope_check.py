#!/usr/bin/env python3
"""AR351-y-AC3 -- the candidate's scope, read from git (the approver reads this list).

SCOPE-OK prints only when `git diff --name-only origin/PROD <candidate>` lists at least one path and every path is one of the
four the cell names (analysisRequest.ts, AnalysisRequestParts.tsx, TicketCenter.tsx under src/pages/TicketCenter/, and the new
test file under its __tests__/), AND `git diff origin/PROD <candidate> -- src/pages/InvestorReporting src/api` is empty.
Otherwise SCOPE-BAD <why>, exit 1.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PORTAL = ROOT / "portal"
CAND = "cand/dell2/anlreq-filing-hint-did-you-mean"
ALLOWED = {
    "src/pages/TicketCenter/analysisRequest.ts",
    "src/pages/TicketCenter/AnalysisRequestParts.tsx",
    "src/pages/TicketCenter/TicketCenter.tsx",
    "src/pages/TicketCenter/__tests__/filing-hint.test.tsx",
}


def git(args):
    res = subprocess.run(["git", "-C", str(PORTAL)] + args, capture_output=True, text=True)
    if res.returncode != 0:
        print("SCOPE-BAD git failed: " + " ".join(args) + ": " + res.stderr.strip())
        raise SystemExit(1)
    return res.stdout


def main():
    paths = [p for p in git(["diff", "--name-only", "origin/PROD", CAND]).splitlines() if p.strip()]
    if not paths:
        print("SCOPE-BAD the candidate changes no path against origin/PROD")
        return 1
    outside = [p for p in paths if not p.startswith("src/pages/TicketCenter/") or p not in ALLOWED]
    if outside:
        print("SCOPE-BAD paths outside the cell's four: " + ", ".join(outside))
        return 1
    widened = git(["diff", "origin/PROD", CAND, "--", "src/pages/InvestorReporting", "src/api"])
    if widened.strip():
        print("SCOPE-BAD the diff touches src/pages/InvestorReporting or src/api")
        return 1
    print("SCOPE-OK %d paths, all under src/pages/TicketCenter/ and named by the cell; InvestorReporting and src/api diff empty"
          % len(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
