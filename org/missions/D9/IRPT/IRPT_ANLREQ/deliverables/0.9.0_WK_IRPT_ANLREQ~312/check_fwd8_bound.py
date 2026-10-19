"""FWD-8 bound check (TO-AR-y-418, criterion AR418-y-AC3). Stdlib only.

Lists the portal paths the candidate branch changes against its merge-base with origin/DEV and prints
FWD8-BOUND-OK files=2 only when those paths are exactly the two paths this order grants. Otherwise it
prints FWD8-BOUND-BAD <paths> and exits 1. The portal worktree is the workspace top level plus "portal".
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EXPECTED = frozenset(
    {
        "src/pages/InvestorReporting/tabs/analysis/NativeSections.tsx",
        "src/pages/InvestorReporting/__tests__/fwd8/native-sections-report-mode.test.tsx",
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
        base = _git(portal, "merge-base", "HEAD", "origin/DEV").strip()
        changed = sorted(line for line in _git(portal, "diff", "--name-only", base, "HEAD").splitlines() if line)
    except RuntimeError as exc:
        print("FWD8-BOUND-BAD " + str(exc))
        return 1
    if changed and frozenset(changed) == EXPECTED and len(changed) == len(EXPECTED):
        print("FWD8-BOUND-OK files=2")
        return 0
    print("FWD8-BOUND-BAD " + (" ".join(changed) if changed else "(no changed paths)"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
