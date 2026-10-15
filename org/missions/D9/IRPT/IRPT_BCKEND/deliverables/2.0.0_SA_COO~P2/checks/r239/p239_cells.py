"""IRPT_BCKEND workstream ~PL round 4 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the 49 Financial ADDENDUM 1 release candidate.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB239-1  IB-pr-608  the 49financial bundle built from its MINTING pin with the signed TRANSPLANT files (IB-pr-595) plus ONLY the ABSENT-AT-SOURCE-D spans of IB-pr-604 and IB-pr-607, BUILD ONLY, tested offline, compared with the live bundle
    AC1  identity; the transplant reference equals IB-pr-595's record for 49financial (digest, file shas); the live bundle equals the signed packet's; the minting pin
    AC2  the candidate differs from the live bundle and from the signed transplant digest; the changed members are EXACTLY holdings_snapshot.py and publication.py; publication.py equals the signed
         transplant's; holdings_snapshot.py with every D span stripped equals the signed transplant's file byte for byte; its D spans equal the D spans of HEAD's file
    AC3  the offline tests on the candidate tree (passed, failed 0), notes, the six counters 0, no long digit run
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r218"))
import p196_cells as P6  # noqa: E402
import p218_cells as P8  # noqa: E402

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~444/IB239-1_addendum_candidate.json"
IB595 = P6.D + "0.9.0_WK_IRPT_BCKEND~434/IB228-1_holdings_transplant_candidate.json"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PUB = "infra/aws/lambda/investor-reporting/holdings/publication.py"
ART = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~444/addendum/49financial/"
MINTING = "b1d354cfc9341168a3b4c316a344876ce0049b97"
SPAN = re.compile(r"^[ \t]*# BEGIN ABSENT-AT-SOURCE-D\b.*?^[ \t]*# END ABSENT-AT-SOURCE-D\b[^\n]*\n", re.S | re.M)
fail, load, is_int = P6.fail, P6.load, P6.is_int


def signed():
    """IB-pr-595's record for 49financial and the committed transplanted files it names."""
    r = load(IB595)["firms"]["49financial"]
    files = {}
    for m in r["changed_members"]:
        fp = P6.ROOT / m["artifact"]
        if not fp.is_file() or hashlib.sha256(fp.read_bytes()).hexdigest() != m["sha256_transplanted"]:
            fail("IB-pr-595's committed %s no longer matches its record" % m["repo_path"])
        files[m["repo_path"]] = fp.read_bytes()
    return r, files


def ac1(r):
    P8.identity(r)
    s, _ = signed()
    if r.get("firm") != "49financial" or r.get("minting_pin") != MINTING or s.get("minting_pin") != MINTING:
        fail("firm must be 49financial on the minting pin %s" % MINTING)
    t = r.get("transplant_ref") or {}
    if t.get("candidate_bundle_sha256") != s["candidate_bundle_sha256"]:
        fail("transplant_ref.candidate_bundle_sha256 must equal IB-pr-595's 49financial candidate digest")
    if r.get("live_bundle_sha256") != s["live_bundle_sha256"]:
        fail("live_bundle_sha256 must equal the live bundle IB-pr-595 and the signed packet name")
    print("OK: identity; the transplant reference and the live bundle equal the signed packet's")


def ac2(r):
    s, files = signed()
    cand = r.get("candidate_bundle_sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", str(cand)):
        fail("candidate_bundle_sha256 must be a 64-hex sha256")
    if cand in (r.get("live_bundle_sha256"), s["candidate_bundle_sha256"]):
        fail("the addendum candidate must differ from the live bundle AND from the signed transplant digest (a new digest)")
    total = P8.count(r.get("members_total"), "members_total")
    ch = r.get("changed_members")
    if not isinstance(ch, list) or sorted(m.get("repo_path") for m in ch) != sorted([HS, PUB]):
        fail("the changed members must be EXACTLY holdings_snapshot.py and publication.py (anything else moving is a STOP)")
    got = {}
    for m in ch:
        art = m.get("artifact")
        if not isinstance(art, str) or not art.startswith(ART):
            fail("%s needs its candidate file committed under %s" % (m.get("repo_path"), ART))
        fp = P6.ROOT / art
        if not fp.is_file() or hashlib.sha256(fp.read_bytes()).hexdigest() != m.get("sha256_candidate"):
            fail("%s sha256_candidate is not the sha256 of the committed file" % m.get("repo_path"))
        got[m["repo_path"]] = fp.read_bytes()
    if got[PUB] != files[PUB]:
        fail("publication.py must equal the signed transplant's file byte for byte (the addendum does not touch it)")
    text = got[HS].decode("utf-8")
    if SPAN.sub("", text).encode("utf-8") != files[HS]:
        fail("holdings_snapshot.py with every ABSENT-AT-SOURCE-D span stripped must equal the signed transplant's file byte for byte")
    spans = SPAN.findall(text)
    head = SPAN.findall((P6.ROOT / HS).read_text(encoding="utf-8"))
    if not spans or spans != head:
        fail("the D spans of the candidate (%d) must equal the D spans of HEAD's holdings_snapshot.py (%d) exactly" % (len(spans), len(head)))
    d = r.get("d_spans") or {}
    if d.get("count") != len(spans) or d.get("equal_to_head") is not True or d.get("diff_lines_outside_spans") != 0:
        fail("d_spans must read count %d, equal_to_head true, diff_lines_outside_spans 0" % len(spans))
    if b"allow_older_date" in got[HS] or b"ONE-DATE-ASSERT" in got[HS]:
        fail("the candidate must not carry the one-date bypass")
    if r.get("cusip_port_present") is not True:
        fail("cusip_port_present must be true (49 Financial keeps the port on pin 1)")
    if r.get("members_equal_to_live") != total - 2:
        fail("members_equal_to_live must equal members_total minus 2 (%d)" % (total - 2))
    print("OK: exactly the two members differ from the live bundle; the candidate is the signed transplant plus the %d D spans" % len(spans))


def ac3(r):
    t = r.get("tests") or {}
    if not (is_int(t.get("passed")) and t["passed"] >= 1 and t.get("failed") == 0):
        fail("tests must read passed >= 1 and failed 0 (the offline tests run on the candidate tree)")
    P8.ac3(r)


CHECKS = {"IB239-1-AC1": lambda: ac1(load(REC)), "IB239-1-AC2": lambda: ac2(load(REC)), "IB239-1-AC3": lambda: ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p239_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
