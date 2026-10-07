"""IRPT_BCKEND round 67 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cells IB-pr-347 (who can reach the export read now,
CTO ruling msg 525) and IB-pr-348 (E-P8 criterion 4: case-insensitive null-likes, IRPT_CUSTDY round-4 analysis msg 512).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB67-1-AC1  the committed IB67-1_export_reach.json names its sources (the grants/policy store and the principal store) and the export
              routes, prints a denominator of principals read, and states non_opal_reach as a number equal to the principals listed
              under it; each listed principal carries its class and the grant that reaches the route. Base: FAIL (no file).
  IB67-2-AC1  _ids tests pass, and a test names each null-like spelling 'none', 'NONE', 'NaN', 'NULL', 'null' (case-insensitive guard).
              Base: FAIL (the guard is case-sensitive; no such test).
  IB67-G-<n>  A GUARD for slot ~<n>: that worker's own commits touch only its grant. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "8d7577866e"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
IDS = "infra/aws/lambda/investor-reporting/_ids"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
GRANTS = {
    "148": (CH, TO + "347.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~148/"),
    "149": (IDS + "/ids.py", IDS + "/tests/", CH, TO + "348.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~149/"),
}
SPELLINGS = ("none", "NONE", "NaN", "NULL", "null")


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB67"))
        sys.exit(1)

    if cid == "IB67-1-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~148/IB67-1_export_reach.json"
        if not f.is_file():
            fail("no IB67-1_export_reach.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        if not d.get("sources") or not d.get("routes"):
            fail("sources or routes missing")
        if not isinstance(d.get("principals_read"), int) or d["principals_read"] <= 0:
            fail("no positive principals_read denominator")
        listed = d.get("non_opal_principals") or []
        if not isinstance(d.get("non_opal_reach"), int) or d["non_opal_reach"] != len(listed):
            fail("non_opal_reach %r != principals listed %d" % (d.get("non_opal_reach"), len(listed)))
        for p in listed:
            if not p.get("class") or not p.get("grant"):
                fail("a listed principal lacks its class or the grant that reaches the route")
        print("OK: non_opal_reach=%d of %d principals read" % (d["non_opal_reach"], d["principals_read"]))
    elif cid == "IB67-2-AC1":
        tests = list((root / IDS / "tests").glob("test_*.py"))
        text = "\n".join(t.read_text(encoding="utf-8") for t in tests)
        missing = [s for s in SPELLINGS if ("'%s'" % s) not in text and ('"%s"' % s) not in text]
        if missing:
            fail("no _ids test names the spelling(s) %s" % missing)
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/"], root / IDS)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("_ids suite: %s" % last)
        print("OK: every spelling tested; _ids %s" % last)
    elif cid.startswith("IB67-G-"):
        slot = cid.rsplit("-", 1)[1]
        grant = GRANTS.get(slot)
        if not grant:
            fail("unknown slot %r" % slot)
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~%s" % slot, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~%s's grant" % (len(changed), slot))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
