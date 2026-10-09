"""IRPT_BCKEND round 106 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO msg 3088, IRPT_DASHBD ADDENDUM 9.2 (2)):
  IB106-1  IB-pr-405  the owned analysis read returns the persist inputs (artifact_id, composition_sha256, retention policy, persisted
                      report index), re-authorized per request; svc-custody-statement reads it for cottonwood only (worker ~268)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB106-1-AC1  `pytest ops/tests _authz/tests -k persist_inputs` (investor-reporting) passes >= 5 tests. Base: FAIL (0 selected).
  IB106-1-AC2  ops/tests and _authz/tests each pass in full, one pytest session per suite; one pre-existing failure excused by id (D2-S43).
               Base: PASS (control).
  IB106-1-AC3  census C + replay R + packet P (worker ~268): BUILD_ONLY rc 0 on a clean tree, >= 1 artifact with built_sha256; replay
               arms identical/expected-diff with a negative control; packet names Branch A, Branch B, the pin and every built sha256.
               Base: FAIL (no C).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~268/"


def pyt(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True,
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
        print("%s FAIL" % (cid or "IB106"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB106-1-AC1":
        rc, n, last = pyt(root / IR, "ops/tests", "_authz/tests", "-k", "persist_inputs")
        if rc != 0 or n < 5:
            fail("-k persist_inputs rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB106-1-AC2":
        # each suite in its own session: the two trees share test-module names, so one session collides (13 false failures)
        lines = []
        # excused by id: the published /original route is declared by no entry at HEAD (IRPT_BCKEND-D2-S43), not this cell's
        excuse = "not test_every_entry_carries_the_published_route_table_it_serves"
        for suite in ("ops/tests", "_authz/tests"):
            rc, n, last = pyt(root / IR, suite, *(["-k", excuse] if suite.startswith("_authz") else []))
            if rc != 0:
                fail("%s rc %d: %s" % (suite, rc, last))
            lines.append("%s %s" % (suite, last))
        print("OK: " + "; ".join(lines))
    elif cid == "IB106-1-AC3":
        c = load(W + "IB106-1_release_census.json")
        bo, arts = c.get("build_only") or {}, c.get("artifacts") or []
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or not arts or not all(a.get("built_sha256") for a in arts):
            fail("census %r / %d artifact(s)" % (bo, len(arts)))
        arms = load(W + "IB106-1_release_replay.json").get("arms") or []
        if not arms or not all(x.get("verdict") in ("identical", "expected-diff") for x in arms) \
                or not any(x.get("negative_control") for x in arms):
            fail("replay arms")
        pp = root / (W + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-405.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        for s in ["Branch A", "Branch B", str(c.get("pin") or "")] + [str(a["built_sha256"]) for a in arts]:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: census %d artifact(s) + %d arm(s) + packet" % (len(arts), len(arms)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
