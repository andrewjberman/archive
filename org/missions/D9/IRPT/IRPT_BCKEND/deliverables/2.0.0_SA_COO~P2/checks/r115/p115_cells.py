"""IRPT_BCKEND round 115 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ADDENDUM 19.1, row D2-S56):
  IB115-1  IB-pr-414  the 49financial holdings producer's peak memory: measured on pre-404, 404 and 410 bytes on one harness, and a fix
                      that runs UNDER 85% of 4 GiB with the FWD-14 gate's decisions unchanged (worker ~276)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB115-1-AC1  memory census M: one harness, real 49F inputs, upload disabled; peak_rss_bytes, wall_time_s and table_lookups
               (AMENDMENT 1) for trees pre404, b404, b410 and fix; the
               limit is 0.85 * 4 GiB; fix.peak_rss_bytes < limit, and b404's is >= the limit or its value explains the kill.
               Base: FAIL (no M).
  IB115-1-AC2  the publish-gate and runner suites pass (`-k publish_gate` >= 10 and the gold investor_reporting tests, the
               live-state S71 guard test_rearm_trigger_live excused by name).
               Base: PASS (control).
  IB115-1-AC3  replay R: per firm (49financial, inflection, cottonwood) `fix_vs_b404_gate_decision_<firm>` reads identical (same
               outcome and conditions), >= 1 negative control. Base: FAIL (no R).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~276/"
LIMIT = int(0.85 * 4 * 1024 ** 3)
GOLD = "data/assets/scripts/gold/investor_reporting/tests/"


def pyt(root, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(root), capture_output=True,
                       timeout=580)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB115"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB115-1-AC1":
        m = load(W + "IB115-1_memory_census.json")
        trees = m.get("trees") or {}
        for t in ("pre404", "b404", "b410", "fix"):
            v = (trees.get(t) or {}).get("peak_rss_bytes")
            if not isinstance(v, int) or v <= 0:
                fail("%s peak_rss_bytes %r" % (t, v))
        if m.get("limit_bytes") != LIMIT or not m.get("harness") or m.get("upload") is not False:
            fail("limit %r harness %r upload %r" % (m.get("limit_bytes"), m.get("harness"), m.get("upload")))
        fix = trees["fix"]["peak_rss_bytes"]
        if fix >= LIMIT:
            fail("fix peak %d >= limit %d" % (fix, LIMIT))
        # TO-IB-pr-414 AMENDMENT 1 (CTO ADDENDUM 20 item 1): the e56 cost is graded on the same harness
        for t in ("pre404", "b404", "b410", "fix"):
            if not isinstance(trees[t].get("wall_time_s"), (int, float)) or not isinstance(trees[t].get("table_lookups"), int):
                fail("%s wall_time_s %r table_lookups %r" % (t, trees[t].get("wall_time_s"), trees[t].get("table_lookups")))
        print("OK: peak RSS pre404 %d, b404 %d, b410 %d, fix %d (limit %d)" % tuple(
            [trees[t]["peak_rss_bytes"] for t in ("pre404", "b404", "b410", "fix")] + [LIMIT]))
    elif cid == "IB115-1-AC2":
        rc, n, last = pyt(root, GOLD, "-k", "publish_gate")
        if rc != 0 or n < 10:
            fail("-k publish_gate rc %d: %s" % (rc, last))
        # the live-state S71 guard (test_rearm_trigger_live) reads AWS, not code; excused by name as in rounds 93-101
        rc2, n2, last2 = pyt(root, GOLD, "-k", "not test_rearm_trigger_live")
        if rc2 != 0:
            fail("gold investor_reporting tests rc %d: %s" % (rc2, last2))
        print("OK: publish_gate %s; suite %s" % (last, last2))
    elif cid == "IB115-1-AC3":
        arms = load(W + "IB115-1_gate_decision_replay.json").get("arms") or []
        by = {x.get("name"): x.get("verdict") for x in arms}
        for firm in ("49financial", "inflection", "cottonwood"):
            if by.get("fix_vs_b404_gate_decision_%s" % firm) != "identical":
                fail("%s reads %r" % (firm, by.get("fix_vs_b404_gate_decision_%s" % firm)))
        if not any(x.get("negative_control") for x in arms):
            fail("no negative control")
        print("OK: the fix's gate decision is identical at 3 firms")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
