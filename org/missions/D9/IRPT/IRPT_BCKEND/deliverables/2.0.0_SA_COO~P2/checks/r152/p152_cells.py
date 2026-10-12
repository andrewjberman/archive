"""IRPT_BCKEND round 152 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD-ONLY order with AWS reads, nothing released:
  IB152-1  IB-pr-456  the release read for `commentary_requested` (IB-pr-455 merged @0322231fc8): every function that packages
                      the changed members, each built from a candidate map and set beside its live package; every member that
                      would move; every reader of the accepted record at HEAD (CTO msg 5863: "the pair names every reader of
                      the accepted record with one read through each").

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB152-1-AC1  the functions: found by subtraction over the whole source map (entries counted), each with its live digest, its
               rollback version, and two byte-identical candidate builds; nothing uploaded or applied.
  IB152-1-AC2  per function, EVERY member whose bytes differ between live and built is listed with its owning commits and
               classed; the three changed members are placed in each; a member that moves and is not one of the three is named
               as a RIDER; the minimal-release question is answered per function with one of three words.
  IB152-1-AC3  the readers of the accepted record re-counted at this cell's base, each with the read the pair would make through
               it; the replay arms show a submission WITHOUT the member is accepted exactly as live accepts it; the bounds held.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~312/"
OUT, PACKET = D + "IB152-1_release_read.json", D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-456.md"
B64 = re.compile(r"^[A-Za-z0-9+/]{43}=$")
MINIMAL = ("ONLY_THE_CHANGED_MEMBERS_MOVE", "RIDERS_MOVE_WITH_THEM", "CANNOT_BE_BUILT_ALONE")
CHANGED = ("submission.py", "acceptance.py", "AnalysisSubmissionRequest.schema.json")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB152"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    fns = a.get("functions")
    if not isinstance(fns, list) or not fns:
        fail("functions is empty")
    if cid == "IB152-1-AC1":
        c = a.get("source_map_census") or {}
        if not all(isinstance(c.get(k), int) for k in ("entries_scanned", "entries_packaging_a_changed_member")) \
                or c["entries_packaging_a_changed_member"] != len(fns) or not c.get("how_found"):
            fail("source_map_census needs entries_scanned, entries_packaging_a_changed_member equal to the functions listed, and how_found")
        for x in fns:
            n = x.get("function")
            if not n or not B64.match(str(x.get("live_code_sha256") or "")) or not x.get("live_read_at_utc"):
                fail("%s: live_code_sha256 and live_read_at_utc" % n)
            if not x.get("rollback_version_id") and not x.get("rollback_version_absent_reason"):
                fail("%s: rollback_version_id, or why none was found" % n)
            b = x.get("build") or {}
            if b.get("outcome") not in ("BUILT", "DID_NOT_BUILD"):
                fail("%s: build.outcome must be BUILT or DID_NOT_BUILD" % n)
            if b["outcome"] == "BUILT" and (not B64.match(str(b.get("built_sha256") or "")) or b.get("built_twice_identical") is not True):
                fail("%s: a BUILT function needs built_sha256 and built_twice_identical true" % n)
            if b["outcome"] == "DID_NOT_BUILD" and not b.get("why"):
                fail("%s: DID_NOT_BUILD needs why" % n)
        for k in ("uploads_made", "applies_made", "real_source_map_edits", "product_source_edits", "vendor_calls_made"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        print("OK: %d of %d map entries package a changed member: %s" % (len(fns), c["entries_scanned"], ", ".join(x["function"] for x in fns)))
    elif cid == "IB152-1-AC2":
        for x in fns:
            n = x.get("function")
            if (x.get("build") or {}).get("outcome") != "BUILT":
                continue
            mv = x.get("moved_members")
            if not isinstance(mv, list) or any(not m.get("member") or not isinstance(m.get("owning_commits"), list)
                                                or m.get("class") not in ("served", "inert") or not m.get("one_line")
                                                or not isinstance(m.get("is_one_of_the_three"), bool) for m in mv):
                fail("%s: moved_members must list each member with owning_commits, class, one_line and is_one_of_the_three" % n)
            pc = x.get("changed_members_packaged")
            if not isinstance(pc, dict) or set(pc) != set(CHANGED) or any(v not in ("moves", "not_packaged", "packaged_and_does_not_move") for v in pc.values()):
                fail("%s: changed_members_packaged must place each of %s" % (n, CHANGED))
            riders = [m["member"] for m in mv if not m["is_one_of_the_three"]]
            if x.get("riders") != riders:
                fail("%s: riders must be exactly the moved members that are not one of the three" % n)
            q = x.get("minimal_release")
            if q not in MINIMAL or (q == "ONLY_THE_CHANGED_MEMBERS_MOVE" and riders) or (q == "RIDERS_MOVE_WITH_THEM" and not riders):
                fail("%s: minimal_release must be one of %s and agree with riders" % (n, MINIMAL))
            if not isinstance(x.get("added_members"), list) or not isinstance(x.get("removed_members"), list):
                fail("%s: added_members and removed_members" % n)
        if not isinstance(a.get("entanglements"), list):
            fail("entanglements (other held or unreleased work a release here would carry) is not stated")
        print("OK: " + "; ".join("%s %s (%d moved, %d riders)" % (x["function"], x.get("minimal_release", x["build"]["outcome"]),
                                                               len(x.get("moved_members") or []), len(x.get("riders") or [])) for x in fns))
    elif cid == "IB152-1-AC3":
        r = a.get("readers_of_the_accepted_record_at_base") or {}
        rd = r.get("readers")
        if not r.get("base_commit") or not isinstance(rd, list) or not rd or any(
                not x.get("reader") or ":" not in str(x.get("code_line") or "") or not x.get("function_or_surface")
                or not x.get("read_the_pair_makes_through_it") for x in rd):
            fail("readers_of_the_accepted_record_at_base needs base_commit and each reader with code_line, function_or_surface and read_the_pair_makes_through_it")
        if not isinstance(r.get("production_readers"), int) or not isinstance(r.get("difference_from_ib_pr_453"), list):
            fail("production_readers and difference_from_ib_pr_453 must be stated")
        arms = (a.get("replay") or {}).get("arms")
        if not isinstance(arms, list) or not arms or any(x.get("verdict") not in ("identical", "expected-diff") or not x.get("name") for x in arms):
            fail("replay.arms must each read identical or expected-diff")
        if not any(x.get("negative_control") for x in arms):
            fail("no replay arm is a negative control")
        if not any(x.get("submission_without_the_member") is True and x.get("verdict") == "identical" for x in arms):
            fail("no arm shows a submission WITHOUT the member accepted identically by live and built")
        if not (root / PACKET).is_file():
            fail("no %s" % PACKET)
        if not isinstance(a.get("not_exercised"), list):
            fail("not_exercised is not stated")
        print("OK: %d reader(s) at %s (%d production); %d replay arm(s); packet written" % (len(rd), str(r["base_commit"])[:10], r["production_readers"], len(arms)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
