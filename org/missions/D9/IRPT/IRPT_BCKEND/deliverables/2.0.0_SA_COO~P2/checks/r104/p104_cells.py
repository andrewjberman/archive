"""IRPT_BCKEND round 104 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ruling @03521b4de0, row MDPF_SECCLASS-D1-S8):
  IB104-1  IB-pr-403  49F SmartX-path SECURITY nodes carry the source's CUSIP as security_id; a node with none is LISTED, never given an
                      invented id (worker ~267)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB104-1-AC1  `pytest tests/test_holdings_49f.py -k smartx_cusip` passes >= 2 tests. Base: FAIL (0 selected).
  IB104-1-AC2  test_holdings_49f.py and test_smartx_valuation.py pass in full. Base: PASS (control; 44 passed).
  IB104-1-AC3  census K (worker ~267, a real 49F read, counts only): smartx_security_nodes == with_cusip + listed_no_cusip,
               with_cusip >= 1, invented == 0, and the source column read is named. Base: FAIL (no K).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

T = "data/assets/scripts/gold/investor_reporting/tests/"
K = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~267/IB104-1_smartx_cusip_census.json"


def pyt(root, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(root), capture_output=True,
                       timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB104"))
        sys.exit(1)

    if cid == "IB104-1-AC1":
        rc, n, last = pyt(root, T + "test_holdings_49f.py", "-k", "smartx_cusip")
        if rc != 0 or n < 2:
            fail("-k smartx_cusip rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB104-1-AC2":
        rc, n, last = pyt(root, T + "test_holdings_49f.py", T + "test_smartx_valuation.py")
        if rc != 0:
            fail("suites rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB104-1-AC3":
        f = root / K
        if not f.is_file():
            fail("no %s" % K)
        k = json.loads(f.read_text(encoding="utf-8"))
        tot, wc, ln, inv = (k.get(x) for x in ("smartx_security_nodes", "with_cusip", "listed_no_cusip", "invented"))
        if not all(isinstance(x, int) for x in (tot, wc, ln, inv)):
            fail("counts %r" % k)
        if tot != wc + ln or wc < 1 or inv != 0 or not k.get("source_column"):
            fail("census %r" % {x: k.get(x) for x in ("smartx_security_nodes", "with_cusip", "listed_no_cusip", "invented", "source_column")})
        print("OK: %d SmartX security nodes: %d CUSIP, %d listed, 0 invented" % (tot, wc, ln))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
