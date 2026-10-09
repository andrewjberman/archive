"""IRPT_BCKEND round 93 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-381 (CTO ruling msg 1988 on rows D2-W188-S1/S2:
(a) count every writer of the served directory first; (b) the runner emits source_client_ids and lands carried TERMINATED entries;
(c) the previous state is the served directory; IB-pr-380 + IB-pr-381 ship as ONE release under one pair).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB93-1-AC1  the writers file W lists every writer of latest.json and of directory.json (writer_count = len(writers) >= 1, each with
              name, kind and evidence) and explains the served inflection as_of 2026-10-08 after the failed refresh. Base: FAIL.
  IB93-1-AC2  runner tests `-k terminated_carry_forward` pass (>= 2) and directory tests `-k previous_state_served` pass (>= 2); both
              suites pass whole. Base: FAIL.
  IB93-1-AC3  the replay file R, per firm (inflection, cottonwood), through the built release: READY, terminated_count 1, the carried
              entry present in the landed directory; live REFRESH_FAILED; and the 2026-10-09 fire at inflection finds its previous
              state (previous_found true, false_additions 0). The packet P names the pin, every writer from W, the rollback sha
              RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=, Branch A and Branch B. Base: FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~189/"
W = WK + "IB93-1_directory_writers.json"
R = WK + "IB93-1_release_replay.json"
P = WK + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md"
ROLLBACK = "RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8="
RUNNER = "data/assets/scripts/gold/investor_reporting"
DIRECTORY = "infra/aws/lambda/investor-reporting/directory"


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB93-1"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB93-1-AC1":
        w = load(W)
        writers = w.get("writers") or []
        if not writers or w.get("writer_count") != len(writers):
            fail("writer_count %r vs %d writers" % (w.get("writer_count"), len(writers)))
        for x in writers:
            if not all(str(x.get(k, "")).strip() for k in ("name", "kind", "evidence")):
                fail("writer lacks name/kind/evidence: %r" % x)
        if not str(w.get("served_inflection_1008_explained", "")).strip():
            fail("served_inflection_1008_explained is empty")
        print("OK: %d writer(s): %s" % (len(writers), ", ".join(x["name"] for x in writers)))
    elif cid == "IB93-1-AC2":
        for cwd, sel, n in ((RUNNER, "terminated_carry_forward", 2), (DIRECTORY, "previous_state_served", 2)):
            rc, last = pytest(root / cwd, "tests", "-k", sel)
            m = re.search(r"\b(\d+) passed", last)
            if rc != 0 or not m or int(m.group(1)) < n:
                fail("%s -k %s rc %d: %s" % (cwd, sel, rc, last))
            rc2, last2 = pytest(root / cwd, "tests")
            if rc2 != 0:
                fail("%s suite rc %d: %s" % (cwd, rc2, last2))
            print("OK: %s -k %s: %s; suite: %s" % (cwd, sel, last, last2))
    elif cid == "IB93-1-AC3":
        firms = load(R).get("firms") or {}
        for firm in ("inflection", "cottonwood"):
            r = firms.get(firm) or {}
            b, lv = r.get("built") or {}, r.get("live") or {}
            if b.get("reason_code") in (None, "", "REFRESH_FAILED") or b.get("terminated_count") != 1 \
                    or b.get("carried_in_landed") is not True:
                fail("%s built %r" % (firm, b))
            if lv.get("reason_code") != "REFRESH_FAILED":
                fail("%s live %r" % (firm, lv))
        f9 = (firms.get("inflection") or {}).get("fire_20261009") or {}
        if f9.get("previous_found") is not True or f9.get("false_additions") != 0:
            fail("inflection fire_20261009 %r" % f9)
        if not (root / P).is_file():
            fail("no %s" % P)
        pk = (root / P).read_text(encoding="utf-8")
        pin = str(load(R).get("pin", ""))
        need = [pin, ROLLBACK, "Branch A", "Branch B"] + [x["name"] for x in (load(W).get("writers") or [])]
        for s in need:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: both firms READY terminated 1 carried; inflection 10-09 finds previous; packet names pin %s" % pin)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
