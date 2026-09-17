"""OGX1-AC29 probe (NFRA_OPLGTW, TO-OG-x-1, worker 0.9.0_WK_NFRA_OPLGTW~5).

The diff of tests/test_principal_cutover.py against this cell's cut base must be EXACTLY one added
ROUTE_CLASS dict-entry line per path named in DOWNLOAD_PATHS.json, and no other line. Run:

    python og_x1.py AC29

Prints each DOWNLOAD_PATHS.json path with the class the diff actually added, then one VERDICT line.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO = _HERE.parents[8]                    # .../ajb_workspace
_TEST_REL = "infra/aws/ec2/opal-gateway/tests/test_principal_cutover.py"
_PATHS_FILE = _HERE.parents[1] / "DOWNLOAD_PATHS.json"
_CUT_BASE = "96ed92aa4d"                    # this cell's hand-off point (OG-q-2/OG-q-3 already drained)
_ENTRY_RE = re.compile(r'^\+\s*"([^"]+)":\s*"([^"]+)",?\s*$')


def _diff_lines() -> list:
    result = subprocess.run(["git", "-C", str(_REPO), "diff", _CUT_BASE, "--", _TEST_REL],
                            capture_output=True, text=True, timeout=60)
    if result.returncode not in (0, 1):
        raise RuntimeError("git diff failed rc=%s stderr=%r" % (result.returncode, result.stderr[:300]))
    return [ln for ln in result.stdout.splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]


def _run_ac29() -> int:
    declared = json.loads(_PATHS_FILE.read_text(encoding="utf-8"))
    want_paths = sorted(p["path"] for p in declared["paths"])
    added = _diff_lines()
    entries = {}
    stray = []
    for line in added:
        m = _ENTRY_RE.match(line)
        if m is None:
            stray.append(line)
            continue
        entries[m.group(1)] = m.group(2)
    for path in want_paths:
        print("%s -> %s" % (path, entries.get(path, "MISSING")))
    if stray:
        print("VERDICT: FAIL-OGX1-AC29 stray_diff_line(s): %r" % (stray,))
        return 1
    if sorted(entries) != want_paths:
        print("VERDICT: FAIL-OGX1-AC29 entries %s != DOWNLOAD_PATHS.json paths %s"
             % (sorted(entries), want_paths))
        return 1
    print("VERDICT: PASS-OGX1-AC29")
    return 0


def main(argv) -> int:
    if len(argv) != 2 or argv[1] != "AC29":
        print("usage: og_x1.py AC29")
        return 2
    return _run_ac29()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
