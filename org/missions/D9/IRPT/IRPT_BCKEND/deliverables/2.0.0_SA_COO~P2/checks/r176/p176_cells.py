"""IRPT_BCKEND round 176 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB176-1  IB-pr-509  READ-ONLY census of the per-firm holdings packages the runner host installs (CTO round-176 analysis section 1 and 2 item 1)
    AC1  the record's shape and arithmetic: one package per firm the runner builds (the BUILDERS firms), each member row's equal flag agrees with its hashes, denominators printed
    AC2  the check re-derives from git: every member's head_member_sha256 is the blob at HEAD; each package carries the guard's whole closure; every differing member carries an explanation (commits since the object was written, an end-of-line-only difference, a historical blob it equals, or an explicit unattributed flag)
    AC3  where the two merged changes land is cited, the bundle map agrees with the guard's keys, the bound counters read 0 and every ETag is unchanged
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
RUNNER = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~361/IB176-1_holdings_packages_census.json"
BOUND_ZERO = ("aws_writes_made", "objects_uploaded", "functions_invoked", "ssm_commands_sent", "hosts_started", "accounts_written", "figures_written")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB176"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_sha(x):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{64}", x) is not None


def builders_firms():
    src = (ROOT / RUNNER).read_text(encoding="utf-8")
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "BUILDERS" for t in node.targets):
            return sorted(k.value for k in node.value.keys)
    fail("BUILDERS not found in %s" % RUNNER)


def closure():
    sys.path.insert(0, str(ROOT / ".tools"))
    import safe_deploy_core as sdc
    return sorted(sdc._IRPT_HOLDINGS_CLOSURE)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB176-1":
        fail("unknown criterion %r" % CID)
    r = load(CENSUS)
    pk = r.get("packages") or []
    if arm == "AC1":
        want = builders_firms()
        got = sorted(p.get("firm_id") for p in pk)
        if got != want:
            fail("the packages must be exactly the BUILDERS firms %s, read %s" % (want, got))
        den = r.get("denominator") or {}
        if den.get("firms_in_builders") != len(want) or den.get("packages_read") != len(pk):
            fail("denominator must read firms_in_builders %d and packages_read %d, reads %s" % (len(want), len(pk), den))
        for p in pk:
            for k in ("bucket", "key", "etag", "last_modified"):
                if not str(p.get(k, "")).strip():
                    fail("%s: %s is required" % (p.get("firm_id"), k))
            mem = p.get("members") or []
            if not mem:
                fail("%s: no member rows" % p.get("firm_id"))
            for m in mem:
                if not is_sha(m.get("live_member_sha256")) or not is_sha(m.get("head_member_sha256")):
                    fail("%s member %r needs 64-hex live_member_sha256 and head_member_sha256" % (p.get("firm_id"), m.get("name")))
                if m.get("equal") is not (m["live_member_sha256"] == m["head_member_sha256"]):
                    fail("%s member %r: the equal flag disagrees with its hashes" % (p.get("firm_id"), m.get("name")))
            if p.get("members_differing") != sum(1 for m in mem if m.get("equal") is False):
                fail("%s: members_differing must equal the rows with equal false" % p.get("firm_id"))
        print("OK: %d firm package(s), %s" % (len(pk), [(p["firm_id"], len(p["members"]), p["members_differing"]) for p in pk]))
    elif arm == "AC2":
        clo = closure()
        for p in pk:
            names = set()
            for m in p.get("members") or []:
                rp = m.get("repo_path")
                if not rp:
                    continue
                names.add(rp)
                rc = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:%s" % rp], capture_output=True, timeout=60)
                if rc.returncode != 0:
                    fail("%s is not a blob at HEAD" % rp)
                h = hashlib.sha256(rc.stdout).hexdigest()
                if h != m.get("head_member_sha256") and h != m.get("head_member_sha256_lf_normalised"):
                    fail("%s: head_member_sha256 is not the blob at HEAD" % rp)
                if m.get("equal") is False and not (
                        m.get("commits_since_live") or m.get("eol_only_difference") is True
                        or m.get("live_matches_blob_at_commit") or m.get("unattributed") is True):
                    fail("%s/%s differs and carries no explanation (commits_since_live, eol_only_difference, live_matches_blob_at_commit or unattributed true)" % (p.get("firm_id"), rp))
            absent = sorted(set(clo) - names)
            if sorted(absent) != sorted(p.get("closure_absent_from_package") or []):
                fail("%s: the guard's closure members missing from the package rows %s must equal closure_absent_from_package %s" % (p.get("firm_id"), absent[:3], p.get("closure_absent_from_package")))
        print("OK: head hashes are the blobs at HEAD; each package carries the %d-member closure" % len(clo))
    elif arm == "AC3":
        fx = r.get("fix_locations") or []
        need = {"temp_file_fix", "account_id_builder"}
        if {x.get("change") for x in fx} != need:
            fail("fix_locations must name exactly %s" % sorted(need))
        for x in fx:
            if not x.get("repo_path") or not re.fullmatch(r"[0-9a-f]{7,40}", str(x.get("commit", ""))):
                fail("fix_locations %s needs repo_path and commit" % x.get("change"))
            if not isinstance(x.get("in_closure"), bool) or not isinstance(x.get("differs_in_firms"), list):
                fail("fix_locations %s needs in_closure (bool) and differs_in_firms (list)" % x.get("change"))
        bm = r.get("bundle_map") or {}
        if bm.get("agrees_with_guard") is not True or not bm.get("source"):
            fail("bundle_map must cite its source and agree with the guard's keys (agrees_with_guard true)")
        for k in BOUND_ZERO:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        for p in pk:
            if not p.get("etag") or p.get("etag") != p.get("etag_after"):
                fail("%s: the ETag after the census must equal the one before" % p.get("firm_id"))
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        print("OK: fix locations cited; bundle map agrees; bound counters 0; ETags unchanged")
    else:
        fail("unknown criterion")
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
