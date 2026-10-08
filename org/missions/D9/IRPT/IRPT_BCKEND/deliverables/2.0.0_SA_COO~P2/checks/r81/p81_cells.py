"""IRPT_BCKEND round 81 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-368 (the release of IB-pr-367 at pin
a0d8d4943f: irpt-export-render repository.py + retention.py; COO half @764a0abf3c, CTO half @275e506034 with its four conditions).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB81-1-AC1  the committed IB81-1_release_after_reads.json reads: pin a0d8d4943f; census EXACTLY repository.py + retention.py;
              start_live_codesha = 03p2eIEK... (the rollback target); built_sha == the packet's idanP8nX... == live CodeSha256 (re-read
              live here); post_census_changed_members 0; replan_changes 0; build_tree_clean true; ledger_closed true; rolled_back
              false. Base: FAIL (no file).
  IB81-1-AC2  the same file's retained-read regression (CTO half condition 1): pre_read and post_read name one existing retained
              ANALYSIS or PERFORMANCE report, both answered ok, with the same report_id, revision and body_sha256, and
              type_error false. Base: FAIL (no file).
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

F = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~176/IB81-1_release_after_reads.json"
PIN = "a0d8d4943f"
TWO = {"repository.py", "retention.py"}
START = "03p2eIEKU9iSIOe5GYDbkbisapqAjULUyAPA/Wcxrfc="
BUILT = "idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB81-1"))
        sys.exit(1)

    if cid not in ("IB81-1-AC1", "IB81-1-AC2"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r" % d.get("pin"))

    if cid == "IB81-1-AC2":
        a, b = d.get("pre_read") or {}, d.get("post_read") or {}
        if a.get("report_kind") not in ("ANALYSIS", "PERFORMANCE"):
            fail("pre_read report_kind %r" % a.get("report_kind"))
        for side, r in (("pre_read", a), ("post_read", b)):
            if r.get("ok") is not True:
                fail("%s not ok: %r" % (side, r.get("outcome")))
        for k in ("report_kind", "report_id", "revision", "body_sha256"):
            if not a.get(k) or a.get(k) != b.get(k):
                fail("%s differs or is empty: pre %r post %r" % (k, a.get(k), b.get(k)))
        if d.get("type_error") is not False:
            fail("type_error is %r" % d.get("type_error"))
        print("OK: retained %s read back by reference, same report_id, revision and body before and after" % a["report_kind"])
        print("%s PASS" % cid)
        return

    if set(d.get("census_changed_members") or []) != TWO:
        fail("census members %r" % sorted(d.get("census_changed_members") or []))
    if d.get("start_live_codesha") != START:
        fail("start CodeSha256 %r is not the signed rollback target" % d.get("start_live_codesha"))
    if d.get("built_sha") != BUILT:
        fail("built %r is not the packet's %s" % (d.get("built_sha"), BUILT))
    for k, v in (("post_census_changed_members", 0), ("replan_changes", 0), ("build_tree_clean", True),
                 ("ledger_closed", True), ("rolled_back", False)):
        if d.get(k) != v:
            fail("%s is %r" % (k, d.get(k)))
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv
    r = subprocess.run(bash_argv(str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name",
                                 "irpt-export-render", "--query", "CodeSha256", "--output", "text"), capture_output=True, timeout=60)
    live = r.stdout.decode("utf-8", "replace").strip()
    if r.returncode or not live:
        fail("live CodeSha256 unreadable rc %d" % r.returncode)
    if live != BUILT and base64.b64decode(live).hex() != base64.b64decode(BUILT).hex():
        fail("live CodeSha256 %r != built %s" % (live, BUILT))
    print("OK: pin %s, 2 of 2 members, start == rollback target, live == built %s..., census 0, replan 0, ledger closed"
          % (PIN, BUILT[:8]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
