"""IRPT_BCKEND round 111 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ruling D1-S8 AMENDMENT 2; rows D2-W269-S1/S2):
  IB111-1  IB-pr-410  IB-pr-403 fixed (SmartX CUSIP nodes keep `ticker=` for display and classification) + the 49F-ONLY narrow
                      bundle rebuilt on the post-IB-pr-404 bytes (e56 + fixed holdings_49f.py); packet + replay; supersedes IB-pr-410 (worker ~273)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB111-1-AC1  `pytest tests/test_holdings_49f.py -k smartx_cusip` >= 4 pass (incl. one named `..._keeps_ticker...`) and the 49F +
               SmartX suites pass. Base: FAIL (no keeps_ticker test).
  IB111-1-AC2  census C: build_only rc 0 on a clean tree; ONE artifact, firm 49financial, base_sha256 == IB-pr-402's built 49F bytes,
               built twice identical, changed members (SHA256SUMS aside) == exactly holdings_snapshot.py + holdings_49f.py. Base: FAIL.
  IB111-1-AC3  replay R + packet P: verdicts identical/expected-diff; `fwd14_gate_unchanged` and `smartx_class_parity` identical;
               `symbol_miss_cusip_fallback` expected-diff; >= 1 negative control; P names Branch A, Branch B, the base and built sha256.
               Base: FAIL (no R).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~273/"
BASE = "3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901"
MEMBERS = sorted(["data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
                  "data/assets/scripts/gold/investor_reporting/holdings_49f.py"])


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
        print("%s FAIL" % (cid or "IB111"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB111-1-AC1":
        t = "data/assets/scripts/gold/investor_reporting/tests/"
        rc, n, last = pyt(root, t + "test_holdings_49f.py", "-k", "smartx_cusip")
        if rc != 0 or n < 4:
            fail("-k smartx_cusip rc %d: %s" % (rc, last))
        rc, n2, last2 = pyt(root, t + "test_holdings_49f.py", "-k", "keeps_ticker")
        if rc != 0 or n2 < 1:
            fail("-k keeps_ticker rc %d: %s" % (rc, last2))
        rc, n3, last3 = pyt(root, t + "test_holdings_49f.py", t + "test_smartx_valuation.py")
        if rc != 0:
            fail("suites rc %d: %s" % (rc, last3))
        print("OK: %s; suites %s" % (last, last3))
    elif cid == "IB111-1-AC2":
        c = load(W + "IB111-1_49f_bundle_census.json")
        bo, arts = c.get("build_only") or {}, c.get("artifacts") or []
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or len(arts) != 1:
            fail("census %r / %d artifact(s)" % (bo, len(arts)))
        a = arts[0]
        if a.get("firm") != "49financial" or a.get("base_sha256") != BASE or a.get("built_twice_identical") is not True \
                or not a.get("built_sha256"):
            fail("artifact %r" % {k: a.get(k) for k in ("firm", "base_sha256", "built_twice_identical", "built_sha256")})
        ch = sorted(m for m in a.get("changed_members") or [] if not m.endswith("SHA256SUMS"))
        if ch != MEMBERS:
            fail("changed members %r" % ch)
        print("OK: one 49F bundle on the post-404 base; changes exactly holdings_snapshot.py + holdings_49f.py")
    elif cid == "IB111-1-AC3":
        arms = load(W + "IB111-1_49f_bundle_replay.json").get("arms") or []
        by = {x.get("name"): x.get("verdict") for x in arms}
        if not arms or not all(v in ("identical", "expected-diff") for v in by.values()):
            fail("arms %r" % by)
        for name, want in (("fwd14_gate_unchanged", "identical"), ("smartx_class_parity", "identical"),
                           ("symbol_miss_cusip_fallback", "expected-diff")):
            if by.get(name) != want:
                fail("%s reads %r" % (name, by.get(name)))
        if not any(x.get("negative_control") for x in arms):
            fail("no negative control")
        c = load(W + "IB111-1_49f_bundle_census.json")
        pp = root / (W + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-410.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        built = str(((c.get("artifacts") or [{}])[0]).get("built_sha256") or "")
        for s in ("Branch A", "Branch B", BASE, built):
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: %d arms; FWD-14 gate and SmartX class parity identical; packet names both branches and both sha256" % len(arms))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
