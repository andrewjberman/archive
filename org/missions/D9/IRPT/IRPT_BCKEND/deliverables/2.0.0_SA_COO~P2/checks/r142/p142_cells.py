"""IRPT_BCKEND round 142 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB142-1  IB-pr-445  the UNMOVED-BAR GUARD: the second witness does not grade a security-day on which its own bar equals its bar
                      for the prior trading day. The overlap table again under that guard, per type; the sizing with the
                      institutional class admitted under the guard; and what the guard un-grades in the seven admitted types
                      (CTO msg 5549). Counts only.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB142-1-AC1  per type, the security-days of the securities both witnesses carry split with no remainder into equal / one day
               off / neither / no bar / not graded under the guard; the types whose one-day-off column is empty under the guard
               are those the table shows; the five one-day-off security-days of the earlier read are each accounted for.
  IB142-1-AC2  three sizings are printed and each adds up (four claims sum to the account-days present; served + blank ==
               eligible): the seven types with no guard, the seven under the guard, the seven plus the institutional class
               under the guard; the guard's cost in the seven types is the first's freed days less the second's, never negative.
  IB142-1-AC3  the fetch was one pass; the control reads as planted (an unmoved bar is not graded; a moved one is); nothing
               re-graded in the product; no class admitted by the cell; no account id in the outputs.
Every count is UNMEASURED by the issuer. One figure of earlier reads (76,796 account-days present) binds only when the same
account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~303/"
OUT = D + "IB142-1_unmoved_bar_guard.json"
READ = D + "IB142-1_UNMOVED_BAR_GUARD_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
COLS = ("equal", "one_day_off", "neither", "no_bar", "not_graded_under_the_guard")
SIZINGS = ("seven_types_no_guard", "seven_types_under_the_guard", "seven_types_and_inst_under_the_guard")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB142"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    same = a.get("same_account_days_read") is True
    if not same and not a.get("source_difference_explained"):
        fail("same_account_days_read is not true and the record does not say why")
    if cid == "IB142-1-AC1":
        o = a.get("overlap_by_type_under_the_guard")
        if not isinstance(o, dict) or not o:
            fail("overlap_by_type_under_the_guard is empty")
        empty = []
        for name, r in o.items():
            if any(not isinstance(r.get(k), int) for k in COLS + ("securities", "security_days")):
                fail("type %s lacks an integer count" % name)
            if sum(r[k] for k in COLS) != r["security_days"]:
                fail("type %s: the five columns sum to %d, security_days is %d" % (name, sum(r[k] for k in COLS), r["security_days"]))
            if r["one_day_off"] == 0 and r["equal"] > 0:
                empty.append(name)
        if sorted(a.get("types_with_an_empty_one_day_off_column_under_the_guard") or []) != sorted(empty):
            fail("the listed types are not the ones the table shows %r" % empty)
        five = a.get("the_five_earlier_one_day_off_security_days")
        if not isinstance(five, list) or len(five) != 5 or any(x.get("under_the_guard") not in COLS for x in five):
            fail("each of the five earlier one-day-off security-days must be placed in one column under the guard")
        if not a.get("guard_rule_in_words"):
            fail("guard_rule_in_words is not stated")
        tot = {k: sum(r[k] for r in o.values()) for k in COLS}
        print("OK: %d type(s); under the guard: %s; empty one-day-off column in %d type(s)" % (len(o), tot, len(empty)))
    elif cid == "IB142-1-AC2":
        z = a.get("sizings") or {}
        if sorted(z) != sorted(SIZINGS):
            fail("sizings must be exactly %s" % (SIZINGS,))
        freed = {}
        for name in SIZINGS:
            s = z[name]
            ad, sv = s.get("account_days") or {}, s.get("serving_rule") or {}
            if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)) or sum(ad[k] for k in CLAIMS) != ad["present"]:
                fail("%s: account_days does not sum to present" % name)
            if same and ad["present"] != 76796:
                fail("%s: the same account-days are said to be read, yet present is %d" % (name, ad["present"]))
            if any(not isinstance(sv.get(k), int) for k in ("eligible", "served", "blank", "accounts_never_served")) \
                    or sv["served"] + sv["blank"] != sv["eligible"] or not isinstance(sv.get("blank_share_percent"), (int, float)):
                fail("%s: serving_rule is incomplete or does not add up" % name)
            if not isinstance(s.get("freed_and_holding_no_other_ungradeable_kind"), int):
                fail("%s: freed_and_holding_no_other_ungradeable_kind is not stated" % name)
            freed[name] = s["freed_and_holding_no_other_ungradeable_kind"]
        g = a.get("guard_cost_in_the_seven_types") or {}
        if g.get("account_days_no_longer_freed") != freed[SIZINGS[0]] - freed[SIZINGS[1]] or g["account_days_no_longer_freed"] < 0:
            fail("the guard's cost %r is not the first sizing's freed days less the second's (%d - %d)" % (
                g.get("account_days_no_longer_freed"), freed[SIZINGS[0]], freed[SIZINGS[1]]))
        if not isinstance(g.get("row_days_not_graded"), int) or not a.get("what_is_assumed"):
            fail("guard_cost_in_the_seven_types.row_days_not_graded and what_is_assumed are not stated")
        print("OK: blank share: seven no guard %.1f%%, seven under the guard %.1f%%, seven and Inst under the guard %.1f%%; the guard un-frees %d account-day(s)" % (
            z[SIZINGS[0]]["serving_rule"]["blank_share_percent"], z[SIZINGS[1]]["serving_rule"]["blank_share_percent"],
            z[SIZINGS[2]]["serving_rule"]["blank_share_percent"], g["account_days_no_longer_freed"]))
    elif cid == "IB142-1-AC3":
        fe = a.get("fetch") or {}
        calls = fe.get("calls")
        if not isinstance(calls, list) or not calls or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
            fail("fetch.calls must list every call with its ticker count, none over 50")
        if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0 \
                or fe["distinct_tickers_asked"] > 1500:
            fail("the fetch is not one pass, or is above the 1,500 stop")
        c = a.get("control") or {}
        p = c.get("planted") or {}
        if not p or p != c.get("read") or not p.get("unmoved_bar_is_not_graded") or not p.get("moved_bar_is_graded"):
            fail("the control does not read as planted, or does not plant the two cases")
        if a.get("claims_regraded_in_product") is not False or a.get("other_sources_asked") != 0 or a.get("classes_admitted_by_this_cell") != 0:
            fail("claims_regraded_in_product must be false, other_sources_asked 0 and classes_admitted_by_this_cell 0")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: %d call(s), %d tickers, each asked once; control as planted with both cases; nothing re-graded; 0 account-id tokens" % (
            len(calls), fe["distinct_tickers_asked"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
