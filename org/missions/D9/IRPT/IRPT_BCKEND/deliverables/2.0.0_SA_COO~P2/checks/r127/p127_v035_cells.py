"""IRPT_BCKEND round 127 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of IB-pr-429's AMENDMENT 2 (READ ONLY):
  IB127-2  IB-pr-429  the date-basis claim of PRD ADDENDUM v0.35 re-counted on the same 85 Cottonwood partitions IB-pr-429 read:
                      one claim per account-day by the ORDERED rule, the ungradeable kinds as a list, and how many days moved from
                      OWN_DATE to UNGRADEABLE (CTO msg 4990).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB127-2-AC1  every account-day has exactly one of the four claims; the moves against IB-pr-429 are stated and add up; where the
               same account-days were read, the repair only blanks more (UNGRADEABLE not below 17,488, OWN_DATE not above 45,247).
  IB127-2-AC2  the serving rule is counted: served + blank == eligible, blanks split by reason with no remainder, the share and
               the never-served accounts stated; every ungradeable day carries one or more of the five kinds.
  IB127-2-AC3  the control reads as planted, and it plants the two cases the repair is about (a day whose graded rows are on
               their own date and which also holds an ungradeable priced row; a day holding two kinds); no account id in the outputs.
The counts themselves are UNMEASURED by the issuer. The two bounds in AC1 are IB-pr-429's measured figures and bind only when the
record says the same account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~288/"
OUT = D + "IB127-2_account_day_claims_v035.json"
READ = D + "IB127-2_ACCOUNT_DAY_CLAIMS_V035_READ.md"
CLAIMS = ("UNGRADEABLE", "PRIOR_DATE", "OWN_DATE", "NOTHING_TO_GRADE")
KINDS = ("ANCHOR_NOT_LANDED", "OUTSIDE_ANCHOR", "NO_CUSIP", "NEITHER_CLOSE", "NEGATIVE_POSITION")
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
OLD = {"present": 76796, "OWN_DATE": 45247, "PRIOR": 425, "ungradeable": 17488, "nothing_to_grade": 13636}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB127-2"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    ad = a.get("account_days") or {}
    if cid == "IB127-2-AC1":
        if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)):
            fail("account_days needs present and the four claims as integers")
        if sum(ad[k] for k in CLAIMS) != ad["present"]:
            fail("the four claims sum to %d, present is %d" % (sum(ad[k] for k in CLAIMS), ad["present"]))
        mv = a.get("moves_against_IB_pr_429") or {}
        need = ("same_account_days_read", "OWN_DATE_to_UNGRADEABLE", "PRIOR_to_UNGRADEABLE", "not_graded_ungradeable_kept",
                "not_graded_nothing_to_grade_kept", "any_other_move")
        if any(k not in mv for k in need):
            fail("moves_against_IB_pr_429 needs %s" % (need,))
        if mv["same_account_days_read"] is True:
            if ad["present"] != OLD["present"]:
                fail("the same account-days are said to be read, yet present is %d, not %d" % (ad["present"], OLD["present"]))
            if ad["UNGRADEABLE"] < OLD["ungradeable"] or ad["OWN_DATE"] > OLD["OWN_DATE"]:
                fail("the repair can only blank more: UNGRADEABLE %d (floor %d), OWN_DATE %d (ceiling %d)" % (
                    ad["UNGRADEABLE"], OLD["ungradeable"], ad["OWN_DATE"], OLD["OWN_DATE"]))
            if mv["any_other_move"] == 0:
                if ad["OWN_DATE"] != OLD["OWN_DATE"] - mv["OWN_DATE_to_UNGRADEABLE"] \
                        or ad["PRIOR_DATE"] != OLD["PRIOR"] - mv["PRIOR_to_UNGRADEABLE"] \
                        or ad["UNGRADEABLE"] != mv["not_graded_ungradeable_kept"] + mv["OWN_DATE_to_UNGRADEABLE"] + mv["PRIOR_to_UNGRADEABLE"]:
                    fail("the stated moves do not add up to the new counts")
            elif not a.get("other_moves_explained"):
                fail("%r other move(s) and no explanation" % mv["any_other_move"])
        elif not a.get("source_difference_explained"):
            fail("different account-days were read and the record does not say why")
        print("OK: %d account-days: UNGRADEABLE %d, PRIOR_DATE %d, OWN_DATE %d, NOTHING_TO_GRADE %d; OWN_DATE to UNGRADEABLE %s" % (
            ad["present"], ad["UNGRADEABLE"], ad["PRIOR_DATE"], ad["OWN_DATE"], ad["NOTHING_TO_GRADE"], mv["OWN_DATE_to_UNGRADEABLE"]))
    elif cid == "IB127-2-AC2":
        s = a.get("serving_rule") or {}
        if any(not isinstance(s.get(k), int) for k in ("eligible", "served", "blank")) or s["served"] + s["blank"] != s["eligible"]:
            fail("serving_rule: served + blank != eligible")
        br = s.get("blank_by_reason") or {}
        if sum(br.values()) != s["blank"]:
            fail("blank_by_reason sums to %d, blank is %d" % (sum(br.values()), s["blank"]))
        acc = s.get("accounts") or {}
        if any(not isinstance(acc.get(k), int) for k in ("with_eligible_days", "never_served", "always_served", "sometimes_served")) \
                or acc["never_served"] + acc["always_served"] + acc["sometimes_served"] != acc["with_eligible_days"]:
            fail("serving_rule.accounts does not partition the accounts with eligible days")
        if not isinstance(s.get("blank_share_percent"), (int, float)):
            fail("blank_share_percent is not stated")
        k = a.get("ungradeable_kinds") or {}
        days = k.get("account_days_holding_each_kind") or {}
        if sorted(days) != sorted(KINDS):
            fail("account_days_holding_each_kind names %r, the five kinds are %r" % (sorted(days), sorted(KINDS)))
        if k.get("ungradeable_days_with_no_kind") != 0 or not isinstance(k.get("days_with_more_than_one_kind"), int):
            fail("ungradeable_days_with_no_kind must be 0 and days_with_more_than_one_kind stated")
        if sum(days.values()) < ad.get("UNGRADEABLE", 0):
            fail("the kinds cover %d day-kinds, fewer than the %d ungradeable days" % (sum(days.values()), ad.get("UNGRADEABLE", 0)))
        if "cash_flagged_priced_outside_anchor" not in a:
            fail("the treatment and count of a cash-flagged priced row outside the anchor is not stated")
        print("OK: %d eligible: %d served, %d blank (%.1f%%); never served %d of %d accounts; %d ungradeable days hold more than one kind" % (
            s["eligible"], s["served"], s["blank"], s["blank_share_percent"], acc["never_served"], acc["with_eligible_days"], k["days_with_more_than_one_kind"]))
    elif cid == "IB127-2-AC3":
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the control does not read as planted")
        p = c["planted"]
        if not p.get("own_rows_with_an_ungradeable_priced_row_reads_UNGRADEABLE") or not p.get("day_with_two_kinds_lists_both"):
            fail("the control does not plant the two cases of the repair")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: the control reads as planted, both repair cases planted; 0 account-id tokens in the 2 outputs")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
