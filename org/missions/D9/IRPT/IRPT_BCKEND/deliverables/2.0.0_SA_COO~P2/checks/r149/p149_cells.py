"""IRPT_BCKEND round 149 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY, CODE-ONLY order:
  IB149-1  IB-pr-453  which member of a submission, or of its ticket, says commentary is asked for today; where acceptance
                      could read it; every reader of the accepted record (CTO msg 5748).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB149-1-AC1  every member that says, or could say, that commentary is asked for is listed with where it is written and where
               it is read (file:line), for the submission AND for the ticket; or the record says no member says it, with what
               was searched; the answer to "is it told today" is one of three words with its claim.
  IB149-1-AC2  the accepted record: where it is written, its members today, where acceptance runs and what it holds in hand
               there; whether acceptance could read the member, and from what, with its claim.
  IB149-1-AC3  every reader of the accepted record is listed with file:line and what it does with an unknown or absent member;
               counted by kind with no remainder; nothing is proposed for the contract and nothing was requested or run.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~309/"
OUT, READ = D + "IB149-1_commentary_asked_member.json", D + "IB149-1_COMMENTARY_ASKED_MEMBER_READ.md"
CLAIMS = ("measured", "inferred", "held", "absent")
TOLD = ("TOLD_BY_A_MEMBER", "TOLD_ONLY_BY_INFERENCE", "NOT_TOLD")


def at(x):
    return isinstance(x, str) and ":" in x


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB149"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB149-1-AC1":
        for side in ("submission", "ticket"):
            s = a.get(side) or {}
            m = s.get("members_that_say_commentary_is_asked")
            if not isinstance(m, list) or any(not x.get("member") or not at(x.get("written_at")) or not isinstance(x.get("read_at"), list) for x in m):
                fail("%s.members_that_say_commentary_is_asked must list each member with written_at (file:line) and read_at" % side)
            if s.get("told_today") not in TOLD or s.get("claim") not in CLAIMS or not s.get("in_words"):
                fail("%s needs told_today in %s, a claim and in_words" % (side, TOLD))
            if s["told_today"] == "TOLD_BY_A_MEMBER" and not m:
                fail("%s says a member tells it and lists none" % side)
            if not m and not s.get("searched_for"):
                fail("%s lists no member and does not say what was searched for" % side)
        if not isinstance(a.get("what_starts_a_draft_today"), dict) or not at(a["what_starts_a_draft_today"].get("code_line")):
            fail("what_starts_a_draft_today needs in_words and code_line")
        print("OK: submission %s (%s), ticket %s (%s)" % (a["submission"]["told_today"], a["submission"]["claim"],
                                                         a["ticket"]["told_today"], a["ticket"]["claim"]))
    elif cid == "IB149-1-AC2":
        r = a.get("accepted_record") or {}
        if not at(r.get("written_at")) or not isinstance(r.get("members_today"), list) or not r["members_today"] or not r.get("contract_file"):
            fail("accepted_record needs written_at, members_today and contract_file (or the sentence that none declares it)")
        c = a.get("acceptance_could_read_it") or {}
        if c.get("answer") not in (True, False, None) or "answer" not in c or c.get("claim") not in CLAIMS or not c.get("from_what") \
                or not isinstance(c.get("in_hand_at_acceptance"), list) or not at(c.get("code_line")):
            fail("acceptance_could_read_it needs answer, claim, from_what, in_hand_at_acceptance and code_line")
        if c["answer"] is None and c["claim"] != "absent":
            fail("an untold answer must carry the claim absent")
        print("OK: the accepted record has %d member(s) today; acceptance could read it: %r (%s)" % (len(r["members_today"]), c["answer"], c["claim"]))
    elif cid == "IB149-1-AC3":
        rd = a.get("readers_of_the_accepted_record")
        if not isinstance(rd, list) or not rd or any(not x.get("reader") or not at(x.get("code_line")) or not x.get("kind")
                                                    or not x.get("on_an_unknown_or_absent_member") for x in rd):
            fail("readers_of_the_accepted_record must list each reader with code_line, kind and on_an_unknown_or_absent_member")
        by = a.get("readers_by_kind")
        if not isinstance(by, dict) or sum(by.values()) != len(rd):
            fail("readers_by_kind does not account for every reader")
        if not a.get("readers_searched_for") or not isinstance(a.get("not_established"), list):
            fail("readers_searched_for and not_established must be stated")
        for k in ("contract_changes_proposed", "vendor_requests_made", "aws_calls_made", "product_files_edited"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not (root / READ).is_file():
            fail("no %s" % READ)
        print("OK: %d reader(s) of the accepted record, by kind %s; nothing proposed, requested or edited" % (len(rd), by))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
