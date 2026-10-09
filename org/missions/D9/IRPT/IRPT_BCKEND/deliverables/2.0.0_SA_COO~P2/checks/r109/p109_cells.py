"""IRPT_BCKEND round 109 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ADDENDUM 18, msg 3272; row D2-S46):
  IB109-1  IB-pr-408  the investor-reporting _contracts red list: every red test bisected to the cell that broke it, then FIXED, or NAMED
                      with that cell's owner and its expected green commit (worker ~271)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB109-1-AC1  red list L: one entry per test that fails at the BASE commit L.base, each {test, first_red_commit (resolvable),
               cell, owner, disposition FIXED|NAMED}, a NAMED entry also carrying expected_green. Base: FAIL (no L).
  IB109-1-AC2  run `pytest _contracts -rf` now: the failing set equals exactly the NAMED entries of L (every FIXED test passes, nothing
               new is red). Base: FAIL (no L).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
L = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~271/IB109-1_contracts_red_list.json"


def red(cwd):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", "_contracts"], cwd=str(cwd),
                       capture_output=True, timeout=580)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    found = set()
    for line in out.splitlines():
        m = re.match(r"FAILED (\S+)", line.strip())
        if m:
            found.add(m.group(1).replace("\\", "/").split(" - ")[0])
    return found


def norm(t):
    return str(t).replace("\\", "/")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB109"))
        sys.exit(1)

    f = root / L
    if not f.is_file():
        fail("no %s" % L)
    lst = json.loads(f.read_text(encoding="utf-8"))
    entries = lst.get("entries") or []

    if cid == "IB109-1-AC1":
        if not lst.get("base") or not entries:
            fail("no base or no entries")
        for e in entries:
            if not all(e.get(k) for k in ("test", "first_red_commit", "cell", "owner")) or e.get("disposition") not in ("FIXED", "NAMED"):
                fail("entry %r" % e)
            if e["disposition"] == "NAMED" and not e.get("expected_green"):
                fail("NAMED without expected_green: %s" % e["test"])
            rc = subprocess.run(["git", "-C", str(root), "cat-file", "-e", str(e["first_red_commit"]) + "^{commit}"], capture_output=True)
            if rc.returncode != 0:
                fail("first_red_commit not resolvable: %s" % e["first_red_commit"])
        if len(lst.get("base_red") or []) != len(entries):
            fail("%d entries vs %d red at base" % (len(entries), len(lst.get("base_red") or [])))
        print("OK: %d red test(s) attributed (%d FIXED, %d NAMED)" % (
            len(entries), sum(e["disposition"] == "FIXED" for e in entries), sum(e["disposition"] == "NAMED" for e in entries)))
    elif cid == "IB109-1-AC2":
        now = {norm(t) for t in red(root / IR)}
        named = {norm(e["test"]) for e in entries if e.get("disposition") == "NAMED"}
        if now != named:
            fail("red now %s vs NAMED %s" % (sorted(now - named), sorted(named - now)))
        print("OK: red now == NAMED (%d)" % len(now))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
