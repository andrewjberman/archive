"""IRPT_BCKEND round 89 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-377 (the r61 directory release applied by
0.7.0_AE_CloudOps~DELL2: irpt-directory-refresh (refresh.py; handler.py pinned to 48313e9c0e) then irpt-directory-search (entry.py,
expiry.py, trading_calendar.py), at release pin 4710b8007b; packet @0c3d443030 + COO half, CTO half @74e91285b4).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB89-1-AC1  the after-reads file A reads: pin 4710b8007b; refresh census members EXACTLY {refresh.py} and search EXACTLY
              {entry.py, expiry.py, trading_calendar.py}; for each function built_sha == live CodeSha256 (re-read live here),
              post-census 0 and replan 0; ledger_closed true for the activation legs; rolled_back false. Base: FAIL (no file).
  IB89-1-AC2  A records the five-arm controlled-clock drive against the DEPLOYED modules: rc 0 and 5 of 5 arms passed.
              Base: FAIL (no file).
"""
import json
import subprocess
import sys
from pathlib import Path

F = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~DELL2/IB89-1_r61_release_after_reads.json"
PIN = "4710b8007b"
WANT = {"irpt-directory-refresh": {"refresh.py"},
        "irpt-directory-search": {"entry.py", "expiry.py", "trading_calendar.py"}}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB89-1"))
        sys.exit(1)

    if cid not in ("IB89-1-AC1", "IB89-1-AC2"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r" % d.get("pin"))
    if cid == "IB89-1-AC2":
        dr = d.get("five_arm_drive") or {}
        if dr.get("rc") != 0 or dr.get("arms_passed") != 5 or dr.get("arms_total") != 5 or dr.get("against") != "deployed":
            fail("five_arm_drive %r" % dr)
        print("OK: five-arm controlled-clock drive 5 of 5 against the deployed modules")
        print("%s PASS" % cid)
        return
    if d.get("rolled_back") is not False or d.get("ledger_activation_legs_closed") is not True:
        fail("rolled_back %r ledger_activation_legs_closed %r" % (d.get("rolled_back"), d.get("ledger_activation_legs_closed")))
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv
    fns = d.get("functions") or {}
    for fn, want in WANT.items():
        r = fns.get(fn) or {}
        if set(r.get("census_changed_members") or []) != want:
            fail("%s census %r" % (fn, r.get("census_changed_members")))
        if r.get("post_census_changed_members") != 0 or r.get("replan_changes") != 0:
            fail("%s post census %r replan %r" % (fn, r.get("post_census_changed_members"), r.get("replan_changes")))
        p = subprocess.run(bash_argv(str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", fn,
                                     "--query", "CodeSha256", "--output", "text"), capture_output=True, timeout=60)
        live = p.stdout.decode("utf-8", "replace").strip()
        if p.returncode or not live or live != r.get("built_sha"):
            fail("%s live %r != built %r" % (fn, live, r.get("built_sha")))
    print("OK: pin %s, refresh 1 + search 3 members, live == built for both, census 0, replan 0, activation legs closed" % PIN)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
