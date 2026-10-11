"""IRPT_BCKEND round 139 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB139-1  IB-pr-442  the sizing under PRD ADDENDUM v0.39: the account-days freed when only securities of an ADMITTED type are
                      graded by the second witness; the blank share and never-served accounts; and what the rest waits on
                      (CTO msg 5453; the addendum's cost bullet).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB139-1-AC1  every security the first witness does not carry is in exactly one class (admitted type with bars; the two fund
               types left out; no type or mixed; another type not admitted; no ticker to ask with; no bar), with no remainder.
  IB139-1-AC2  every account-day holding such a security is in exactly one outcome; the sizing adds up (four claims sum to the
               account-days present; served + blank == eligible); what the blank ones wait on is counted both ways (holding any,
               and waiting only on that one), the second never above the first.
  IB139-1-AC3  the fetch was one pass; the control reads as planted (an admitted security frees its day, a left-out one does
               not); the reviewer's two points are answered (the to-the-cent next-day trades named; the fund trades split by
               pair with no remainder); nothing re-graded in the product; no account id in the outputs.
Every count is UNMEASURED by the issuer. One figure of earlier reads (76,796 account-days present) binds only when the same
account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~300/"
OUT = D + "IB139-1_sizing_under_v039.json"
READ = D + "IB139-1_SIZING_UNDER_V039_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
SEC = ("admitted_type_with_bars", "left_out_type_inst", "left_out_type_ric_not_available", "no_type_or_mixed",
       "another_type_not_admitted", "no_ticker_to_ask_with", "no_bar")
OUTC = ("freed_every_security_admitted_and_at_the_day_close", "admitted_but_one_or_more_at_prior_day_only",
        "admitted_but_one_or_more_at_neither", "holds_a_security_no_witness_may_grade")
WAIT = ("left_out_type_inst", "left_out_type_ric_not_available", "no_type_or_mixed", "another_type_not_admitted",
        "no_ticker_to_ask_with", "no_bar")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB139"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    same = a.get("same_account_days_read") is True
    if not same and not a.get("source_difference_explained"):
        fail("same_account_days_read is not true and the record does not say why")
    if cid == "IB139-1-AC1":
        s = a.get("securities_outside_the_first_witness") or {}
        if any(not isinstance(s.get(k), int) for k in SEC + ("total",)) or sum(s[k] for k in SEC) != s["total"]:
            fail("the seven classes do not sum to the total")
        if not a.get("class_precedence") or not isinstance(a.get("admitted_types"), list) or len(a["admitted_types"]) != 7:
            fail("class_precedence must be stated and admitted_types must list the seven pairs of the addendum")
        if not isinstance(a.get("admitted_by_type"), dict) or sum(a["admitted_by_type"].values()) != s[SEC[0]]:
            fail("admitted_by_type does not sum to the admitted securities with bars")
        print("OK: %d securities outside the first witness: %s" % (s["total"], {k: s[k] for k in SEC}))
    elif cid == "IB139-1-AC2":
        e = a.get("account_day_effect") or {}
        if any(not isinstance(e.get(k), int) for k in OUTC + ("account_days_holding_such_a_security", "freed_and_holding_no_other_ungradeable_kind")):
            fail("account_day_effect lacks an integer count")
        if sum(e[k] for k in OUTC) != e["account_days_holding_such_a_security"] or e["freed_and_holding_no_other_ungradeable_kind"] > e[OUTC[0]]:
            fail("the four outcomes do not sum, or more are freed than hold every security at the day's close")
        z = a.get("sizing_under_v039") or {}
        ad, sv = z.get("account_days") or {}, z.get("serving_rule") or {}
        if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)) or sum(ad[k] for k in CLAIMS) != ad["present"]:
            fail("sizing_under_v039.account_days does not sum to present")
        if same and ad["present"] != 76796:
            fail("the same account-days are said to be read, yet present is %d" % ad["present"])
        if any(not isinstance(sv.get(k), int) for k in ("eligible", "served", "blank", "accounts_never_served")) \
                or sv["served"] + sv["blank"] != sv["eligible"] or not isinstance(sv.get("blank_share_percent"), (int, float)):
            fail("sizing_under_v039.serving_rule is incomplete or does not add up")
        if not z.get("what_is_assumed"):
            fail("sizing_under_v039.what_is_assumed is not stated")
        w = a.get("still_waiting") or {}
        hold, only = w.get("account_days_holding_any") or {}, w.get("account_days_waiting_only_on") or {}
        if sorted(hold) != sorted(WAIT) or sorted(only) != sorted(WAIT):
            fail("still_waiting must count each of %s both ways" % (WAIT,))
        if any(not isinstance(hold[k], int) or not isinstance(only[k], int) or only[k] > hold[k] for k in WAIT):
            fail("a waiting-only count is above its holding-any count, or is not an integer")
        print("OK: %d freed (%d with no other ungradeable kind); sized blank %.1f%% of %d; never served %d" % (
            e[OUTC[0]], e["freed_and_holding_no_other_ungradeable_kind"], sv["blank_share_percent"], sv["eligible"], sv["accounts_never_served"]))
    elif cid == "IB139-1-AC3":
        fe = a.get("fetch") or {}
        calls = fe.get("calls")
        if not isinstance(calls, list) or not calls or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
            fail("fetch.calls must list every call with its ticker count, none over 50")
        if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0:
            fail("the fetch is not one pass")
        c = a.get("control") or {}
        p = c.get("planted") or {}
        if not p or p != c.get("read") or not p.get("admitted_security_at_the_day_close_frees_its_day") \
                or not p.get("left_out_type_does_not_free_its_day"):
            fail("the control does not read as planted, or does not plant the two cases")
        if a.get("claims_regraded_in_product") is not False or a.get("other_sources_asked") != 0:
            fail("claims_regraded_in_product must be false and other_sources_asked 0")
        rp = a.get("reviewer_points") or {}
        nd = rp.get("next_day_only_to_the_cent")
        if not isinstance(nd, list) or any(not x.get("ticker") or not x.get("trade_date") for x in nd) \
                or rp.get("next_day_only_to_the_cent_count") != len(nd):
            fail("reviewer_points.next_day_only_to_the_cent must name each trade's fund and date, with its count")
        tp = rp.get("trades_by_fund_pair")
        if not isinstance(tp, dict) or not tp or any(not isinstance(v, int) for v in tp.values()) \
                or sum(tp.values()) != rp.get("trades_total"):
            fail("reviewer_points.trades_by_fund_pair must split trades_total with no remainder")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: %d call(s), each ticker asked once; control as planted; %d next-day-to-the-cent trade(s) named; %d trades split over %d pair(s); 0 account-id tokens" % (
            len(calls), len(nd), rp["trades_total"], len(tp)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
