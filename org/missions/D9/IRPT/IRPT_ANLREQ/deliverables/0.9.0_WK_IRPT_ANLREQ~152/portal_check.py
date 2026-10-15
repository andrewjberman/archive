#!/usr/bin/env python3
"""AR351-y-AC1 -- bun test on the new filing-hint file and on the whole src/pages/TicketCenter folder, in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when every case (a) to (g) of the new file
passes and the folder has 0 failed. Otherwise prints PORTAL-TESTS-BAD <why> and exits 1. Counts come from bun's JUnit
report (one <testcase> per test; a failed case carries a <failure> or <error> child), never from the colour summary.
"""
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]          # the workspace worktree: .../deliverables/<serial>/ is 7 levels down
PORTAL = ROOT / "portal"
NEW_FILE = "src/pages/TicketCenter/__tests__/filing-hint.test.tsx"
FOLDER = "src/pages/TicketCenter"
CASES = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)"]
SCRATCH = ROOT / ".scratch"


def run_junit(target, name):
    """Run bun test on target from the portal worktree; return the list of (name, file, failed) per testcase."""
    SCRATCH.mkdir(exist_ok=True)
    out = SCRATCH / name
    if out.exists():
        out.unlink()
    subprocess.run(
        ["bun", "test", target, "--reporter=junit", f"--reporter-outfile={out}"],
        cwd=str(PORTAL), capture_output=True, text=True, timeout=300,
    )
    if not out.exists():
        return None
    rows = []
    for tc in ET.parse(out).getroot().iter("testcase"):
        failed = any(child.tag in ("failure", "error") for child in tc)
        rows.append((tc.get("name") or "", tc.get("file") or "", failed))
    return rows


def main():
    new = run_junit(NEW_FILE, "portal_check_new.xml")
    if new is None:
        print("PORTAL-TESTS-BAD no junit report for the new test file")
        return 1
    new_rows = [r for r in new if "filing-hint" in r[1]]
    if len(new_rows) == 0:
        print("PORTAL-TESTS-BAD the new test file ran no cases")
        return 1
    missing = [c for c in CASES if not any(r[0].startswith(c) for r in new_rows)]
    if missing:
        print("PORTAL-TESTS-BAD cases not found in the new file: " + ",".join(missing))
        return 1
    failing_new = [r[0][:60] for r in new_rows if r[2]]
    if failing_new:
        print("PORTAL-TESTS-BAD new-file cases failing: " + " | ".join(failing_new))
        return 1
    folder = run_junit(FOLDER, "portal_check_folder.xml")
    if folder is None:
        print("PORTAL-TESTS-BAD no junit report for the TicketCenter folder")
        return 1
    failing_folder = [r[0][:60] for r in folder if r[2]]
    if failing_folder:
        print(f"PORTAL-TESTS-BAD {len(failing_folder)} failing in the folder: " + " | ".join(failing_folder))
        return 1
    new_passed = sum(1 for r in new_rows if not r[2])
    folder_passed = sum(1 for r in folder if not r[2])
    print(f"PORTAL-TESTS-OK {new_passed} new, {folder_passed} folder, 0 failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
