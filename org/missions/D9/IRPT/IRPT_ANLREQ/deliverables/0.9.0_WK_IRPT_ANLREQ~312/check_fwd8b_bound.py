"""FWD-8b bound check (TO-AR-y-422, criterion AR422-y-AC3). Stdlib only.

Lists the portal paths changed since the AR-y-418 portal commit (the base of this order's portal commits) and prints
FWD8B-BOUND-OK files=<n> only when every changed path is one of the three this order grants, with n of 2 or 3.
Otherwise it prints FWD8B-BOUND-BAD <paths> and exits 1. The portal worktree is the workspace top level plus "portal".
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# The AR-y-418 portal commit: this order's portal commits are the ones after it.
BASE = "c34d3ea5270fcf6a4d5226dc831827f586c9e97e"

ALLOWED = frozenset(
    {
        "src/pages/InvestorReporting/tabs/analysis/OwnedRequestHistory.tsx",
        "src/pages/InvestorReporting/tabs/analysis/NativeSections.tsx",
        "src/pages/InvestorReporting/__tests__/fwd8/retained-sections-report-mode.test.tsx",
    }
)


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if done.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + " rc=" + str(done.returncode) + ": " + done.stderr.strip())
    return done.stdout


def main() -> int:
    here = Path(__file__).resolve().parent
    try:
        workspace = Path(_git(here, "rev-parse", "--show-toplevel").strip())
        portal = workspace / "portal"
        changed = sorted(line for line in _git(portal, "diff", "--name-only", BASE, "HEAD").splitlines() if line)
    except RuntimeError as exc:
        print("FWD8B-BOUND-BAD " + str(exc))
        return 1
    if changed and frozenset(changed) <= ALLOWED and 2 <= len(changed) <= 3:
        print("FWD8B-BOUND-OK files=" + str(len(changed)))
        return 0
    print("FWD8B-BOUND-BAD " + (" ".join(changed) if changed else "(no changed paths)"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
