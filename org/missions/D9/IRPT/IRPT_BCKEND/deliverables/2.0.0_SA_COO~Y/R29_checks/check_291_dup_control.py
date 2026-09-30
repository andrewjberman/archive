#!/usr/bin/env python3
"""IB-yr-291 AC2 -- CONTROL: a duplicate re-delivery still spends ZERO vendor requests.

Runs the estate's own offline suite in a subprocess (netguard for the whole process) and reads
the duplicate_redelivery arm. PASS iff duplicate_outcome == EXISTING_ARTIFACT_REUSED and
duplicate_vendor_requests == 0 and first_vendor_requests >= 4.

Base run (CLOUD HEAD before the cut): PASS -- this is the bound the cell must not move.
Issuer 2.0.0_SA_COO~Y, round 29. ASCII only.
"""
import json
import os
import subprocess
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R29_checks itself; the repo root is parents[8]
SUITE = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "generate",
                     "tests", "run_offline_suite.py")


def main():
    proc = subprocess.run([sys.executable, SUITE], capture_output=True, text=True, timeout=110, cwd=ROOT)
    out = proc.stdout
    if "RESULT-BEGIN" not in out or "RESULT-END" not in out:
        print("FAIL: suite printed no RESULT block (rc=%s)" % proc.returncode)
        print(out[-800:])
        print(proc.stderr[-800:])
        return 1
    body = out.split("RESULT-BEGIN\n", 1)[1].split("\nRESULT-END", 1)[0]
    result = json.loads(body)
    if "suite_error" in result:
        print("FAIL: suite_error:", result["suite_error"][:400])
        return 1
    dup = result["arms"]["v010_three_recipes_one_handler"]["duplicate_redelivery"]
    print("duplicate_redelivery:", json.dumps(dup, sort_keys=True))
    ok = (dup.get("duplicate_outcome") == "EXISTING_ARTIFACT_REUSED"
          and dup.get("duplicate_vendor_requests") == 0
          and isinstance(dup.get("first_vendor_requests"), int) and dup["first_vendor_requests"] >= 4)
    print("PASS" if ok else "FAIL", ": duplicate re-delivery spends 0 vendor requests; first run spent",
          dup.get("first_vendor_requests"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
