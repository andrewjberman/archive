#!/usr/bin/env python
"""AC2 -- HVST-y-3: FOUR DISTINGUISHABLE RENDERS of `TimelinePanel.tsx`, proved over
CONSTRUCTED inputs: quiet-COMPLETE (a real zero day), PARTIAL, DENIED, and A FAILED CALL.

This script runs the offline harness
`portal/src/pages/SecurityAnalysis/__harness__/timelineFourStates.harness.cjs`, which renders
the ACTUAL `TimelinePanel.tsx` (via `react-dom/server`, `@tanstack/react-query`'s `useQuery`
stubbed to a controlled per-arm response, `recharts`' `BarChart`/`Bar` stubbed only enough to
invoke the component's own real `shape` function per data row) four times, once per arm, and
prints the encoding + the predicate that separates each arm from the other three.

If the render cannot run, this prints which step failed and its error text and exits non-zero.
"""
import json
import os
import subprocess
import sys

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "..", ".."))
PORTAL_DIR = os.path.join(WORKSPACE_ROOT, "portal")
HARNESS_REL = "src/pages/SecurityAnalysis/__harness__/timelineFourStates.harness.cjs"


def main():
    harness_path = os.path.join(PORTAL_DIR, HARNESS_REL)
    if not os.path.isfile(harness_path):
        print(f"FAIL at STEP 1 (locate harness): not found: {harness_path}")
        sys.exit(1)
    print(f"STEP 1 -- harness located: {harness_path}")

    try:
        result = subprocess.run(
            ["node", HARNESS_REL], cwd=PORTAL_DIR, capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        print(f"FAIL at STEP 2 (run harness): timed out: {exc}")
        sys.exit(1)
    except FileNotFoundError as exc:
        print(f"FAIL at STEP 2 (run harness): {exc}")
        sys.exit(1)

    print("STEP 2 -- harness stdout:")
    print(result.stdout)
    if result.stderr:
        print("STEP 2 -- harness stderr:", result.stderr)
    print(f"STEP 2 -- harness exit code: {result.returncode}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"FAIL at STEP 3 (parse harness output): {exc}")
        sys.exit(1)

    print(f"STEP 3 -- result: {payload.get('result')}")
    print(f"STEP 3 -- distinguishable_count: {payload.get('distinguishable_count')}")
    for arm, enc in payload.get("encodings", {}).items():
        print(f"STEP 3 -- arm '{arm}': {json.dumps(enc)}")
    if payload.get("failures"):
        print("STEP 3 -- FAILURES:", payload["failures"])

    ok = result.returncode == 0 and payload.get("result") == "PASS" and payload.get("distinguishable_count") == "4 of 4"
    print(f"AC2 VERDICT: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
