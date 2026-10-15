"""IRPT_BCKEND workstream ~PJ round 4 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the TRANSPLANT release candidates of the three per-firm holdings bundles.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB228-1  IB-pr-590  per firm, the bundle built from the firm's MINTING pin with ONLY the exemption changes TRANSPLANTED into holdings_snapshot.py and publication.py, BUILD ONLY, tested offline, compared with the live bundle
    AC1  the identity and the pins: base commit, read date, the overlay pin an ancestor of HEAD carrying the absent_at_source A, B and C blocks, each firm's minting pin one of the two IB-pr-549 pins
    AC2  per firm: the live and candidate hashes differ, the changed members are EXACTLY the two overlaid files (each recomputed from git at the overlay pin; for the transplant the recomputed value is the sha256 of the transplanted file the record states), every other closure member equal to the live bundle's
    AC3  per firm the offline tests run on the overlay tree (passed, failed 0), notes, the six counters 0, no long digit run
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r218"))
import p196_cells as P6  # noqa: E402
import p218_cells as P8  # noqa: E402

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~434/IB228-1_holdings_transplant_candidate.json"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
PUB = "infra/aws/lambda/investor-reporting/holdings/publication.py"
FIRMS = ("49financial", "cottonwood", "inflection")
MINTING = {"49financial": "b1d354cfc9341168a3b4c316a344876ce0049b97", "cottonwood": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f",
           "inflection": "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f"}
fail, load, is_int = P6.fail, P6.load, P6.is_int


def git(*a):
    return subprocess.run(["git", "-C", str(P6.ROOT), *a], capture_output=True, timeout=60)


def ac1(r):
    P8.identity(r)
    pin = r.get("overlay_pin")
    if not re.fullmatch(r"[0-9a-f]{40}", str(pin)):
        fail("overlay_pin must be a 40-hex commit")
    if git("merge-base", "--is-ancestor", pin, "HEAD").returncode != 0:
        fail("the overlay pin must be an ancestor of HEAD")
    p = git("show", "%s:%s" % (pin, HS))
    if p.returncode != 0 or not all(b"BEGIN ABSENT-AT-SOURCE-" + x in p.stdout for x in (b"A", b"B", b"C")):
        fail("holdings_snapshot.py at the overlay pin must carry the ABSENT-AT-SOURCE A, B and C blocks")
    if not isinstance(r.get("firms"), dict) or sorted(r["firms"]) != sorted(FIRMS):
        fail("firms must hold exactly %s" % (FIRMS,))
    for f in FIRMS:
        if r["firms"][f].get("minting_pin") != MINTING[f]:
            fail("%s: minting_pin must be the IB-pr-549 pin %s" % (f, MINTING[f]))
    print("OK: identity; the overlay pin carries the exemption blocks; minting pins as IB-pr-549")


def ac2(r):
    for f in FIRMS:
        e = r["firms"][f]
        for k in ("live_bundle_sha256", "candidate_bundle_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(e.get(k, ""))):
                fail("%s.%s must be a 64-hex sha256" % (f, k))
        if e["live_bundle_sha256"] == e["candidate_bundle_sha256"]:
            fail("%s: the candidate must differ from the live bundle" % f)
        total = P8.count(e.get("members_total"), f + ".members_total")
        ch = e.get("changed_members")
        if not isinstance(ch, list) or sorted(m.get("repo_path") for m in ch) != sorted([HS, PUB]):
            fail("%s: the changed members must be EXACTLY holdings_snapshot.py and publication.py (anything else moving is a STOP)" % f)
        for m in ch:
            art = m.get("artifact")
            if not isinstance(art, str) or not art.startswith("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/transplant/"):
                fail("%s: %s needs its transplanted file committed under the worker's transplant/ folder (artifact)" % (f, m.get("repo_path")))
            fp = P6.ROOT / art
            if not fp.is_file() or hashlib.sha256(fp.read_bytes()).hexdigest() != m.get("sha256_transplanted"):
                fail("%s: %s sha256_transplanted is not the sha256 of the committed transplanted file" % (f, m.get("repo_path")))
            if m.get("repo_path") == HS:
                txt = fp.read_bytes()
                if b"BEGIN ABSENT-AT-SOURCE-A" not in txt or b"BEGIN ABSENT-AT-SOURCE-B" not in txt or b"BEGIN ABSENT-AT-SOURCE-C" not in txt:
                    fail("%s: the transplanted holdings_snapshot.py must carry the ABSENT-AT-SOURCE A, B and C blocks" % f)
                if b"allow_older_date" in txt or b"ONE-DATE-ASSERT" in txt:
                    fail("%s: the transplanted holdings_snapshot.py must not carry the one-date bypass" % f)
        if e.get("members_equal_to_live") != total - 2:
            fail("%s: members_equal_to_live must equal members_total minus the two transplanted (%d)" % (f, total - 2))
        t = e.get("transplant") or {}
        if t.get("one_date_bypass_absent") is not True:
            fail("%s: the candidate must NOT carry the unreleased one-date bypass (allow_older_date / ONE-DATE-ASSERT): transplant.one_date_bypass_absent must be true" % f)
        want_port = (f == "49financial")
        if t.get("cusip_port_present") is not want_port:
            fail("%s: the CUSIP port must stay as the minting pin has it (present for 49financial, reversed for the others): transplant.cusip_port_present must be %s" % (f, want_port))
        if not (is_int(t.get("foreign_diff_lines")) and 0 <= t["foreign_diff_lines"] <= 40):
            fail("%s: transplant.foreign_diff_lines (changed lines outside the exemption blocks against the minting pin's file) must be an integer 0 to 40" % f)
        P8.text(t.get("foreign_diff_reading"), 60, f + ".transplant.foreign_diff_reading")
    print("OK: per firm exactly the two overlaid members differ from the live bundle")


def ac3(r):
    for f in FIRMS:
        t = r["firms"][f].get("overlay_tests") or {}
        if not (is_int(t.get("passed")) and t["passed"] >= 1 and t.get("failed") == 0):
            fail("%s.overlay_tests must read passed >= 1 and failed 0 (the offline tests run on the overlay tree)" % f)
    P8.ac3(r)


CHECKS = {"IB228-1-AC1": lambda: ac1(load(REC)), "IB228-1-AC2": lambda: ac2(load(REC)), "IB228-1-AC3": lambda: ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p228_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
