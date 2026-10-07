"""IRPT_BCKEND round 68 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of cell IB-pr-349 (the EMERGENCY release of IB-pr-343 to
irpt-export-render at pin b921635dad, laptop applier 0.7.0_AE_CloudOps~I; CTO half @adaf13fec6 + amendment 1 @4493cf1800).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Finishes inside 120 s (reads one file and one live CodeSha256).

  IB68-1-AC1  the committed IB68-1_release_after_reads.json reads: pin b921635dad; census changed members EXACTLY the nine both halves
              name; built_sha == live CodeSha256 (re-read live by this check); replan_changes 0; existing_export_refused true;
              new_export_ready true with admitted_read_log_lines >= 1; performance_ready and analysis_ready true; live_entry_sha256
              starts fc241d806ecc; outside_principal_refused true and opal_caller_served true; ledger_closed true; rolled_back false.
              Base: FAIL (no file).
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/deliverables/0.7.0_AE_CloudOps~I/IB68-1_release_after_reads.json"
PIN = "b921635dad"
NINE = {"entry.py", "receipt.py", "bundle.py", "finalize_on_read.py", "handler.py", "retained_export.py", "narrative_submit.py",
        "submit_service.py", "submit_installed.py"}
TRUE_KEYS = ("existing_export_refused", "new_export_ready", "performance_ready", "analysis_ready", "outside_principal_refused",
             "opal_caller_served", "ledger_closed")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB68"))
        sys.exit(1)

    if cid != "IB68-1-AC1":
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r is not %s" % (d.get("pin"), PIN))
    if set(d.get("census_changed_members") or []) != NINE:
        fail("census members %r != the nine signed" % sorted(d.get("census_changed_members") or []))
    if d.get("rolled_back") is not False:
        fail("rolled_back is %r" % d.get("rolled_back"))
    for k in TRUE_KEYS:
        if d.get(k) is not True:
            fail("%s is %r" % (k, d.get(k)))
    if not isinstance(d.get("admitted_read_log_lines"), int) or d["admitted_read_log_lines"] < 1:
        fail("no admitted-read log line")
    if d.get("replan_changes") != 0:
        fail("replan_changes %r" % d.get("replan_changes"))
    if not str(d.get("live_entry_sha256", "")).startswith("fc241d806ecc"):
        fail("live entry.py sha %r" % d.get("live_entry_sha256"))
    aws = str(root / ".tools" / "aws")
    r = subprocess.run(["bash", aws, "lambda", "get-function-configuration", "--function-name", "irpt-export-render", "--query",
                        "CodeSha256", "--output", "text"], capture_output=True, timeout=100)
    live = r.stdout.decode("utf-8", "replace").strip()
    if r.returncode or not live:
        fail("live CodeSha256 unreadable rc %d" % r.returncode)
    built = str(d.get("built_sha", ""))
    if built not in (live, base64.b64decode(live).hex()):
        fail("built %r != live CodeSha256 %r" % (built, live))
    print("OK: pin %s, 9 of 9 members, live CodeSha256 == built, every after-read holds" % PIN)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
