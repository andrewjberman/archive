"""HVST-ca-1, the issuer's real run: one wsj job refused as expired, renewed in-profile, ended complete.

Run from the root of a LINKED WORKTREE of the merged head, never the main tree (it would otherwise
touch the main tree's browser profile). It copies the main tree's saved wsj session file into the
worktree's runtime (so the job starts from a stored token), leaves the worktree's browser profile
empty (so the account check reads logged out), then runs one job WITHOUT --no-sign-in. The worker's
expiry branch must renew inside the profile and replay the pair. Last line: `AC3 RESULT: PASS` or
`AC3 RESULT: FAIL <why>` / `AC3 RESULT: NEEDS-PERSON`. No secret value is printed.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PUBLISHER = "wsj"
TICKER = "BA"


def main_root():
    out = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return Path(out).parent.resolve()


def newest_run(runtime):
    rows = sorted((runtime / "runs").glob("*-" + PUBLISHER + "-*.json"), key=lambda p: p.stat().st_mtime)
    return json.loads(rows[-1].read_text(encoding="utf-8")) if rows else None


def main():
    root = Path.cwd().resolve()
    main = main_root()
    if root == main:
        print("AC3 RESULT: FAIL run from a linked worktree, not the main tree")
        return 2
    source = main / ".runtime" / "opal-data-harvest" / "secrets" / (PUBLISHER + ".dpapi")
    runtime = root / ".runtime" / "opal-data-harvest"
    if not source.exists():
        print("AC3 RESULT: FAIL no saved %s session file in the main tree" % PUBLISHER)
        return 2
    (runtime / "secrets").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, runtime / "secrets" / source.name)
    profile = runtime / "browser-profiles" / PUBLISHER
    if profile.exists():
        shutil.rmtree(profile)
    command = [sys.executable, "-m", "lib.opal_data_harvest", "run", "--tickers", TICKER,
               "--publishers", PUBLISHER, "--max-jobs", "1"]
    proc = subprocess.run(command, cwd=str(root), timeout=1500)
    run = newest_run(runtime)
    if run is None:
        print("AC3 RESULT: FAIL no job record, collector rc=%s" % proc.returncode)
        return 1
    renewal = run.get("profile_renewal") or {}
    accepted = len(run.get("accepted") or [])
    detected = renewal.get("operator_input_detected")
    print("STATUS=%s ACCEPTED=%d AUTH_REFRESHES=%s RENEWED=%s OPERATOR_INPUT_DETECTED=%s" % (
        run.get("status"), accepted, run.get("auth_refreshes"), renewal.get("renewed"), detected))
    if detected is True:
        print("AC3 RESULT: NEEDS-PERSON")
        return 1
    ok = (run.get("status") == "complete_candidates" and accepted > 0 and run.get("auth_refreshes") == 1
          and renewal.get("renewed") is True and detected is False)
    print("AC3 RESULT: PASS" if ok else "AC3 RESULT: FAIL job did not end complete after one renewal")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
