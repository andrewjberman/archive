"""IRPT_BCKEND round 181 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB181-1  IB-pr-515  irpt-directory-search RE-CENSUSED and rebuilt against its CURRENT live bytes (the 2026-10-13T12:34Z status-rule release moved them), BUILD ONLY, with step 0 and the refreshed never-widen packet
    AC1  the census: built twice identical, 0 signature mismatches, the live sha256 equals the source map's last deployed CodeSha256, handler.py the only changed member, equal to the repo blob at the pin, nothing uploaded
    AC2  the refreshed packet: Branch A, Branch B, the red list, the live and built sha256, the pair's halves, the rollback, the open-ledger sequencing, the CURRENT live CodeSha256
    AC3  step 0 and the replay: the function's directory home read against the builder's, the open deploy ledgers naming the function, the four replay arms, the reach per firm, the bound counters
"""
import base64
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~365/IB181-1_release_census.json"
STEP0 = D + "0.9.0_WK_IRPT_BCKEND~365/IB181-1_step0_and_replay.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~365/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-515.md"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-directory-search"
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB181"))
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
    if cell != "IB181-1":
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
        if names != ["handler.py"]:
            fail("the changed members must be exactly handler.py, read %s (another changed member is a STOP, not a widening)" % names)
        for m in cm:
            if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
                fail("the built member's sha256 must equal the repo blob's at the pin")
        if rec.get("uploaded") is not False or not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
            fail("uploaded false and a pin_commit are required")
        print("OK: %s built twice identical against the CURRENT live; handler.py the only changed member" % FN)
    elif arm == "AC2":
        pk = ROOT / PACKET
        if not pk.is_file():
            fail("no %s" % PACKET)
        t = pk.read_text(encoding="utf-8", errors="replace")
        for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                          ("the pair's halves", r"(?i)COO half"), ("the CTO half", r"(?i)CTO half"), ("rollback", r"(?i)rollback|restore the live"),
                          ("the open-ledger sequencing", r"(?i)open (deploy )?ledger"), ("the superseded packet", r"(?i)IB-pr-499")):
            if not re.search(pat, t):
                fail("the packet lacks: %s" % need)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256", "")
        if cur[:12] not in t:
            fail("the packet must name the CURRENT live CodeSha256 (%s...)" % cur[:12])
        if len(t) < 3000:
            fail("the packet is shorter than 3000 characters")
        print("OK: the refreshed packet is complete and names the current live CodeSha256")
    elif arm == "AC3":
        r = load(STEP0)
        h = r.get("directory_home") or {}
        for k in ("function_reads", "builder_reads", "match", "source"):
            if k not in h:
                fail("directory_home.%s is required" % k)
        if not isinstance(h["match"], bool):
            fail("directory_home.match must be true or false (false means STOP: both homes named in the row)")
        led = r.get("open_ledgers_naming_the_function")
        if not isinstance(led, list):
            fail("open_ledgers_naming_the_function must be a list (empty if none)")
        for x in led:
            if not x.get("ledger") or x.get("status") not in ("OPEN", "CLOSED", "SUPERSEDED", "HELD"):
                fail("each ledger needs a name and a status OPEN/CLOSED/SUPERSEDED/HELD")
        want = {"tail_of_non_head_account": "account_entry", "shared_tail": "two_account_entries", "name_query": "relationship_entry", "entry_without_masks": "unchanged"}
        arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
        if arms != want:
            fail("replay arms must read %s, read %s" % (want, arms))
        reach = r.get("reach") or {}
        if len(reach) != 3:
            fail("reach per firm for 3 firms is required")
        for firm, v in reach.items():
            if not all(is_int(v.get(k)) and v[k] >= 0 for k in ("entries", "entries_with_masks", "accounts", "accounts_tail_addressable_after")):
                fail("reach for %s needs integers" % firm)
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        for k in BOUND_ZERO:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: step 0 recorded (match %s), %d ledger(s), four arms, reach for 3 firms" % (h["match"], len(led)))
    else:
        fail("unknown criterion")
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
