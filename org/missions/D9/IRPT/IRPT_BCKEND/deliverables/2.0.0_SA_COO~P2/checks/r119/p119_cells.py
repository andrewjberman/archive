"""IRPT_BCKEND round 119 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order:
  IB119-1  IB-pr-421  the fresh vendor performance path no longer requires an installed one-use plan (CTO msg 4416, on
                      Andrew-direct 2026-10-09 "egress open except Bloomberg"); what stays is tested; adapter rebuilt; packet.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB119-1-AC1  performance/tests/test_vendor_use_gate.py holds a test for each of the six named behaviours and that file plus
               test_authorization.py pass. Base: FAIL (no such file).
  IB119-1-AC2  census: adapter built twice identical from one commit, 0 name / attribute / method mismatches, live_before ==
               9kYLdR64..., changed members listed. Base: FAIL (no census).
  IB119-1-AC3  packet names Branch A, Branch B, the built sha256, the rollback digest and S3 version; replay arms all
               identical / expected-diff with the two named arms. Base: FAIL (no packet).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~282/"
TESTS = "infra/aws/lambda/investor-reporting/performance/tests/"
NEW_TEST = TESTS + "test_vendor_use_gate.py"
LIVE_BEFORE = "9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A="
NAMED = ("no_plan_required", "unpackaged_firm_refused", "vendor_account_from_own_mapping",
         "request_firm_and_accounts_are_the_callers", "use_record_logged_each_vendor_call", "cache_hit_never_calls_vendor")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB119"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB119-1-AC1":
        f = root / NEW_TEST
        if not f.is_file():
            fail("no %s" % NEW_TEST)
        names = re.findall(r"^def (test_\w+)", f.read_text(encoding="utf-8"), re.MULTILINE)
        for want in NAMED:
            if not any(want in n for n in names):
                fail("no test named for %r (tests: %d)" % (want, len(names)))
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_vendor_use_gate.py",
                            "test_authorization.py"], cwd=str(root / TESTS), capture_output=True, timeout=100)
        tail = p.stdout.decode("utf-8", "replace").strip().splitlines()[-1:] or [""]
        if p.returncode != 0:
            fail("pytest rc %d: %s" % (p.returncode, tail[0]))
        print("OK: %d tests in the new file, 6 of 6 named behaviours covered; %s" % (len(names), tail[0]))
    elif cid == "IB119-1-AC2":
        c = load(D + "IB119-1_adapter_census.json")
        if c.get("function") != "irpt-performance-adapter" or not c.get("pin") or not c.get("built_sha256"):
            fail("census header %r" % {k: c.get(k) for k in ("function", "pin", "built_sha256")})
        if c.get("built_twice_identical") is not True or c.get("live_before") != LIVE_BEFORE:
            fail("twice %r / live_before %r" % (c.get("built_twice_identical"), c.get("live_before")))
        for k in ("built_signature_mismatched", "built_attribute_mismatched", "built_method_mismatched"):
            if c.get(k) != 0:
                fail("%s = %r" % (k, c.get(k)))
        if not c.get("changed_members"):
            fail("no changed_members")
        print("OK: adapter built twice identical at %s; 0/0/0 mismatches; %d changed members" % (
            str(c["pin"])[:10], len(c["changed_members"])))
    elif cid == "IB119-1-AC3":
        c = load(D + "IB119-1_adapter_census.json")
        pp = root / (D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-421.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        for s in ("Branch A", "Branch B", str(c.get("built_sha256") or ""), LIVE_BEFORE, str(c.get("rollback_version") or "")):
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        arms = load(D + "IB119-1_replay.json").get("arms") or []
        if not arms or not all(a.get("verdict") in ("identical", "expected-diff") for a in arms):
            fail("%d arm(s) or a bad verdict" % len(arms))
        by = {a.get("name"): a.get("verdict") for a in arms}
        if by.get("fresh_vendor_path_no_plan") != "expected-diff" or by.get("cache_hit_no_vendor_call") != "identical":
            fail("named arms %r / %r" % (by.get("fresh_vendor_path_no_plan"), by.get("cache_hit_no_vendor_call")))
        print("OK: packet names both branches, built and rollback; %d replay arms, the two named arms as required" % len(arms))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
