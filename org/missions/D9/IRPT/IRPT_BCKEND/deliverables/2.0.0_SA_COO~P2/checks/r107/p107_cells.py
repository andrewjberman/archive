"""IRPT_BCKEND round 107 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ruling D1-S8 AMENDMENT 2 @b58f09e1b8, msg 3107):
  IB107-1  IB-pr-406  49F-ONLY narrow holdings bundle on the post-IB-pr-404 bytes: holdings_snapshot.py + 01e843ce2e (dell1's e62/e56
                      CUSIP fallback) and holdings_49f.py + IB-pr-403; packet + replay (worker ~269)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB107-1-AC1  census C: build_only rc 0 on a clean tree; ONE artifact, firm 49financial, base_sha256 == IB-pr-402's built 49F bytes,
               built twice identical, changed members (SHA256SUMS aside) == exactly holdings_snapshot.py + holdings_49f.py. Base: FAIL.
  IB107-1-AC2  replay R: verdicts identical/expected-diff; `fwd14_gate_unchanged` identical; `symbol_miss_cusip_fallback`
               expected-diff; >= 1 negative control. Base: FAIL (no R).
  IB107-1-AC3  packet P names Branch A, Branch B, the base sha256 and the built sha256. Base: FAIL (no P).
"""
import json
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~269/"
BASE = "3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901"
MEMBERS = sorted(["data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
                  "data/assets/scripts/gold/investor_reporting/holdings_49f.py"])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB107"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB107-1-AC1":
        c = load(W + "IB107-1_49f_bundle_census.json")
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
    elif cid == "IB107-1-AC2":
        arms = load(W + "IB107-1_49f_bundle_replay.json").get("arms") or []
        by = {x.get("name"): x.get("verdict") for x in arms}
        if not arms or not all(v in ("identical", "expected-diff") for v in by.values()):
            fail("arms %r" % by)
        if by.get("fwd14_gate_unchanged") != "identical" or by.get("symbol_miss_cusip_fallback") != "expected-diff":
            fail("named arms %r / %r" % (by.get("fwd14_gate_unchanged"), by.get("symbol_miss_cusip_fallback")))
        if not any(x.get("negative_control") for x in arms):
            fail("no negative control")
        print("OK: %d arms; FWD-14 gate identical; CUSIP fallback fires on a symbol miss" % len(arms))
    elif cid == "IB107-1-AC3":
        c = load(W + "IB107-1_49f_bundle_census.json")
        pp = root / (W + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-406.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        built = str(((c.get("artifacts") or [{}])[0]).get("built_sha256") or "")
        for s in ("Branch A", "Branch B", BASE, built):
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: packet names both branches, the base and the built sha256")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
