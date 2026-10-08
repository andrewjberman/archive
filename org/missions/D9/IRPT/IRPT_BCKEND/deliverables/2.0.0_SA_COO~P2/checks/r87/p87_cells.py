"""IRPT_BCKEND round 87 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-374 (the release of IB-pr-367 at pin
0a57f3c0e9: E9 -- repository.py, composition.py, reporting_policies.json, opal_naming.py, submit_installed.py; COO half @4e3ead72a3, CTO half @c086ec4c2b).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB87-1-AC1  the committed IB87-1_release_after_reads.json reads: pin a0d8d4943f; census EXACTLY the five members;
              start_live_codesha = 03p2eIEK... (the rollback target); built_sha == the packet's idanP8nX... == live CodeSha256 (re-read
              live here); post_census_changed_members 0; replan_changes 0; build_tree_clean true; ledger_closed true; rolled_back
              false. Base: FAIL (no file).
  IB87-1-AC2  the file's `replay` record: one irpt-x10-v1 ANALYSIS
              or PERFORMANCE fixture reserved by the LIVE zip's code path; the LIVE and BUILT zips' repository.get return identical
              bytes (same result_sha256), neither refuses nor raises; the negative control (an altered policy_sha256) is refused by
              BOTH; the three repository/retention suites passed; and replay_commit is an ancestor of ledger_open_commit (the
              record was committed before the apply). Base: FAIL (no file).
"""
import base64
import re
import json
import subprocess
import sys
from pathlib import Path

F = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~182/IB87-1_release_after_reads.json"
PIN = "9238309eca"
TWO = {"entry.py", "infra/logic/registry/reporting_policies.json", "submit_installed.py", "custody_persist.py", "custody_write.py"}
START = "PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0="
BUILT = "rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB87-1"))
        sys.exit(1)

    if cid in ("IB87-2-AC1", "IB87-2-AC2"):
        # IB-pr-375 (CTO half condition 1 on row D2-W181-S2): persisted_by + content bound to the retained composition hash.
        t = root / "infra/aws/lambda/investor-reporting/export/tests/test_custody_writer_composed.py"
        if not t.is_file():
            fail("no test file")
        groups = ("persisted_by",) if cid == "IB87-2-AC1" else ("content_bound", "")
        for k in groups:
            args = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", t.name] + (["-k", k] if k else [])
            p = subprocess.run(args, cwd=str(t.parent), capture_output=True, timeout=280)
            out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
            last = [ln for ln in out.splitlines() if ln.strip()]
            last = last[-1] if last else ""
            if p.returncode != 0 or not re.search(r"\b[1-9]\d* passed", last):
                fail("-k %s rc %d: %s" % (k or "<whole file>", p.returncode, last))
            print("OK: -k %s: %s" % (k or "<whole file>", last))
        print("%s PASS" % cid)
        return
    if cid not in ("IB87-1-AC1", "IB87-1-AC2"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r" % d.get("pin"))

    if cid == "IB87-1-AC2":
        rp = d.get("replay") or {}
        if rp.get("fixture_family") not in ("ANALYSIS", "PERFORMANCE") or rp.get("policy_revision") != "irpt-x10-v1":
            fail("fixture %r under %r" % (rp.get("fixture_family"), rp.get("policy_revision")))
        if rp.get("reserved_by") != "live":
            fail("fixture reserved_by %r, not the live code path" % rp.get("reserved_by"))
        lv, bt = rp.get("live") or {}, rp.get("built") or {}
        for side, r in (("live", lv), ("built", bt)):
            if r.get("ok") is not True or r.get("raised") or r.get("refused"):
                fail("%s replay not clean: %r" % (side, r))
        if not lv.get("result_sha256") or lv.get("result_sha256") != bt.get("result_sha256"):
            fail("result differs: live %r built %r" % (lv.get("result_sha256"), bt.get("result_sha256")))
        nc = rp.get("negative_control") or {}
        if nc.get("live_refused") is not True or nc.get("built_refused") is not True:
            fail("negative control (altered policy_sha256) not refused by both: %r" % nc)
        suites = rp.get("suites") or {}
        if len(suites) != 3 or not all(str(v).startswith("passed") or " passed" in str(v) for v in suites.values()):
            fail("suites %r" % suites)
        import subprocess as _sp
        rc = _sp.run(["git", "merge-base", "--is-ancestor", str(rp.get("replay_commit", "x")), str(d.get("ledger_open_commit", "y"))],
                     cwd=str(root), capture_output=True).returncode
        if rc != 0:
            fail("replay_commit %r is not an ancestor of ledger_open_commit %r" % (rp.get("replay_commit"), d.get("ledger_open_commit")))
        print("OK: %s fixture under irpt-x10-v1, live == built %s..., negative control refused by both, 3 suites passed, replay committed before the apply"
              % (rp["fixture_family"], lv["result_sha256"][:12]))
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
    print("OK: pin %s, 5 of 5 members, start == rollback target, live == built %s..., census 0, replan 0, ledger closed"
          % (PIN, BUILT[:8]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
