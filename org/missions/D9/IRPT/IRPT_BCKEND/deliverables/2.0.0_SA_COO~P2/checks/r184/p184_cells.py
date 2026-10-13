"""IRPT_BCKEND round 184 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB184-1  IB-pr-518  irpt-ycharts-generate CENSUSED and rebuilt against its CURRENT live bytes with the comparison-catalogue release (IB-pr-517), BUILD ONLY, with the never-widen packet
    AC1  the census: built twice identical, 0 signature mismatches, the live sha256 equals the source map's last deployed CodeSha256, the changed members exactly maintained_sources.py and templates.json (recipe.py NOT moved), the real source map restored, nothing uploaded
    AC2  the packet: Branch A, Branch B, the red list, live and built sha256, both halves, rollback, the open-ledger sequencing, the CURRENT live CodeSha256, the four base custody failures named, recipe.py stated as not moved
    AC3  the arms and the ledgers: five models in canonical order served, the four existing entries unchanged, admitted for three firms, an altered copy refused, the open deploy ledgers naming the function, the bound counters
"""
import base64
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~367/IB184-1_release_census.json"
ARMS = D + "0.9.0_WK_IRPT_BCKEND~367/IB184-1_arms_and_ledgers.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~367/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-518.md"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-ycharts-generate"
MEMBERS = ["maintained_sources.py", "templates.json"]
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB184"))
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


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode()


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB184-1" or arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if arm == "AC1":
        rec = load(CENSUS)
        fn = rec.get("functions") or []
        if len(fn) != 1 or fn[0].get("function") != FN:
            fail("functions must hold exactly %s" % FN)
        f = fn[0]
        for k in ("built_sha256", "live_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(f.get(k, ""))):
                fail("%s must be 64-hex" % k)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256")
        if cur != b64_of_hex(f["live_sha256"]):
            fail("live_sha256 must equal the source map's last deployed CodeSha256 for %s (%s): the census is of a STALE live otherwise" % (FN, cur))
        if f.get("built_twice_identical") is not True or f.get("built_signature_mismatched") != 0 or f.get("live_signature_mismatched", 0) != 0:
            fail("built twice identical true and 0 signature mismatches on the built and live zips are required")
        bm, lm = f.get("built_attribute_mismatched"), f.get("live_attribute_mismatched")
        bl, ll = f.get("attribute_mismatch_lines_built"), f.get("attribute_mismatch_lines_live")
        if not is_int(bm) or not is_int(lm) or bm > lm or not isinstance(bl, list) or not isinstance(ll, list) or len(bl) != bm or len(ll) != lm or not set(bl) <= set(ll):
            fail("attribute mismatches: built must not exceed live and every built line must be a live line")
        cm = f.get("changed_members") or []
        names = sorted(str(m.get("name", "")).split("/")[-1] for m in cm)
        if names != MEMBERS:
            fail("the changed members must be exactly %s, read %s (recipe.py or any other member moving is a STOP, not a widening)" % (MEMBERS, names))
        for m in cm:
            if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
                fail("the built member's sha256 must equal the repo blob's at its pin")
        if rec.get("uploaded") is not False or not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
            fail("uploaded false and a pin_commit are required")
        sm = rec.get("source_map") or {}
        if not (sm.get("rows_edited_in_scratch_worktree") == 1 and sm.get("restored") is True and re.fullmatch(r"[0-9a-f]{64}", str(sm.get("sha256_before", ""))) and sm.get("sha256_before") == sm.get("sha256_after_restore")):
            fail("source_map: one staged_from row edited in the scratch worktree, then restored (sha256 before equals after restore)")
        print("OK: %s built twice identical against the CURRENT live; changed members %s; source map restored" % (FN, names))
    elif arm == "AC2":
        pk = ROOT / PACKET
        if not pk.is_file():
            fail("no %s" % PACKET)
        t = pk.read_text(encoding="utf-8", errors="replace")
        for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                          ("the COO half", r"(?i)COO half"), ("the CTO half", r"(?i)CTO half"), ("rollback", r"(?i)rollback|restore the live"),
                          ("the open-ledger sequencing", r"(?i)open (deploy )?ledger"), ("recipe.py stated as not moved", r"(?i)recipe\.py.{0,120}(not moved|NOT moved|unchanged|stays pinned)"),
                          ("the four base custody failures", r"(?i)custody.{0,160}(four|4).{0,80}(base|pre-existing)|(four|4).{0,80}custody")):
            if not re.search(pat, t):
                fail("the packet lacks: %s" % need)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256", "")
        if cur[:12] not in t:
            fail("the packet must name the CURRENT live CodeSha256 (%s...)" % cur[:12])
        if len(t) < 3000:
            fail("the packet is shorter than 3000 characters")
        print("OK: the packet is complete and names the current live CodeSha256")
    else:
        r = load(ARMS)
        led = r.get("open_ledgers_naming_the_function")
        if not isinstance(led, list):
            fail("open_ledgers_naming_the_function must be a list (empty if none)")
        for x in led:
            if not x.get("ledger") or x.get("status") not in ("OPEN", "CLOSED", "SUPERSEDED", "HELD"):
                fail("each ledger needs a name and a status OPEN/CLOSED/SUPERSEDED/HELD")
        want = {"five_models_canonical_order": "five_in_order", "existing_four_entries": "unchanged", "admitted_three_firms": "admitted", "altered_copy": "refused"}
        arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
        if arms != want:
            fail("arms must read %s, read %s" % (want, arms))
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        for k in BOUND_ZERO:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: four arms, %d ledger(s), counters 0" % len(led))
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
