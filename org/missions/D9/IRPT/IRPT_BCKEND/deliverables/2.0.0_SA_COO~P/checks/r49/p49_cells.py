"""Round 49 (IRPT_BCKEND ~P) -- S324 (PRD v0.27 ruling 28: a PATH B performance export names its narrative as NOT_ATTACHED) and
W100-S2 (CTO batch 247: one read-only readers census of the 49F perfrp leaf).

Usage: python <this file> <repo_root> <criterion_id>
  IB49-1-AC1  (S324) export/tests/test_bundle_narrative_state.py passes at least 3 tests and names NOT_ATTACHED: a PLATINUM
              (PATH B) frozen bundle carries narrative_state NOT_ATTACHED with a non-empty narrative_reason; the ExportBundle
              schema refuses a PLATINUM bundle without it; a client-report bundle is unchanged. Base: FAIL (no test).
  IB49-1-AC2  (S324 regression) test_bundle_report_ref.py, test_export_path_b.py and test_packaged_contracts_match_docs.py pass,
              0 failed. Base: PASS.
  IB49-2-AC1  (W100-S2) the census file CENSUS exists with: the leaf key, surfaces (a list, each with what was searched and a
              denominator), verdict NO_READER or LIVE_READER, and evidence; and the investigation channel carries a row added
              since base naming IRPT_BCKEND-W100-S2. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "b77b84cbb4"
EXP = "infra/aws/lambda/investor-reporting/export/"
CENSUS = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~121/W100S2_READERS_CENSUS.json"
CHANNEL = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"


def pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"] + files, cwd=str(root / EXP), capture_output=True, text=True,
                       timeout=600)
    out = (r.stdout or "") + (r.stderr or "")
    p = re.search(r"(\d+) passed", out)
    f = re.search(r"(\d+) failed", out)
    return r.returncode, int(p.group(1)) if p else 0, int(f.group(1)) if f else 0, out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB49"))
        sys.exit(1)

    if cid == "IB49-1-AC1":
        t = root / EXP / "tests/test_bundle_narrative_state.py"
        if not t.is_file():
            fail("no export/tests/test_bundle_narrative_state.py")
        if "NOT_ATTACHED" not in t.read_bytes().decode("utf-8"):
            fail("the test never names NOT_ATTACHED")
        rc, p, f, out = pytest(root, ["tests/test_bundle_narrative_state.py"])
        if rc or p < 3 or f:
            fail("pytest: %s" % out[-400:])
        print("OK: %d tests passed" % p)
    elif cid == "IB49-1-AC2":
        files = ["tests/test_bundle_report_ref.py", "tests/test_export_path_b.py", "tests/test_packaged_contracts_match_docs.py"]
        rc, p, f, out = pytest(root, files)
        if rc or f or p == 0:
            fail("pytest: %s" % out[-400:])
        print("OK: %d regression tests passed, 0 failed" % p)
    elif cid == "IB49-2-AC1":
        c = root / CENSUS
        if not c.is_file():
            fail("no %s" % CENSUS)
        d = json.loads(c.read_bytes().decode("utf-8"))
        for k in ("leaf", "surfaces", "verdict", "evidence"):
            if not d.get(k):
                fail("census lacks %r" % k)
        if d["verdict"] not in ("NO_READER", "LIVE_READER"):
            fail("verdict %r" % d["verdict"])
        if not isinstance(d["surfaces"], list) or any(not s.get("searched") or s.get("denominator") is None for s in d["surfaces"]):
            fail("each surface needs 'searched' and a 'denominator'")
        base = subprocess.run(["git", "show", "%s:%s" % (BASE, CHANNEL)], cwd=str(root), capture_output=True).stdout.decode("utf-8")
        now = (root / CHANNEL).read_bytes().decode("utf-8")
        added = now[len(base):] if now.startswith(base) else now
        if "IRPT_BCKEND-W100-S2" not in added:
            fail("no row added since base names IRPT_BCKEND-W100-S2")
        print("OK: verdict %s over %d surface(s); a channel row names W100-S2" % (d["verdict"], len(d["surfaces"])))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
