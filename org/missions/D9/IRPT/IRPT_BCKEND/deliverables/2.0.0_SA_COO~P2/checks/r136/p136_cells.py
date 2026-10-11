"""IRPT_BCKEND round 136 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB136-1  IB-pr-438  the same reader over ALL the securities the anchor does not carry, one pass: how many return data, and the
                      ACCOUNT-DAYS freed when every security a day holds is graded; the blank share under v0.36 (CTO msg 5211).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB136-1-AC1  every security is in exactly one class (no ticker to ask with; asked and data returned; asked and no data), the
               fetch was one pass (each ticker asked once, no call over 50 tickers), and FPNIX is named among the no-data ones.
  IB136-1-AC2  every account-day that holds an outside-anchor row is in exactly one outcome, the freed ones are counted, and the
               sizing under v0.36 adds up: four claims sum to the account-days present, served + blank == eligible.
  IB136-1-AC3  the rows equal only to the prior day's NAV and the account-days they blank are counted; the control holds; no
               account id is in the outputs; nothing is re-graded in the product.
Every count is UNMEASURED by the issuer; the checks grade sums, the one-pass bound and the control. Two figures of earlier reads
(734 securities; 76,796 account-days present) bind only when the record says the same account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~296/"
OUT = D + "IB136-1_all_securities_nav_effect.json"
READ = D + "IB136-1_ALL_SECURITIES_NAV_EFFECT_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
OUTCOMES = ("every_security_at_day_nav_or_unchanged", "one_or_more_at_prior_day_nav_only", "one_or_more_at_neither",
            "one_or_more_with_no_nav")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB136"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    same = a.get("same_account_days_read") is True
    if not same and not a.get("source_difference_explained"):
        fail("same_account_days_read is not true and the record does not say why")
    if cid == "IB136-1-AC1":
        s = a.get("securities") or {}
        keys = ("total", "no_ticker_to_ask_with", "asked_data_returned", "asked_no_data")
        if any(not isinstance(s.get(k), int) for k in keys) or s[keys[1]] + s[keys[2]] + s[keys[3]] != s["total"]:
            fail("securities does not split with no remainder")
        if same and s["total"] < 734:
            fail("the same account-days are said to be read, yet %d securities are counted, fewer than 734" % s["total"])
        fe = a.get("fetch") or {}
        calls = fe.get("calls")
        if not isinstance(calls, list) or not calls or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
            fail("fetch.calls must list every call with its ticker count, none over 50")
        if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0:
            fail("the calls ask %d tickers, distinct asked is %r, asked more than once is %r" % (
                sum(c["tickers"] for c in calls), fe.get("distinct_tickers_asked"), fe.get("tickers_asked_more_than_once")))
        nod = a.get("no_data_securities")
        if not isinstance(nod, list) or len(nod) != s[keys[3]]:
            fail("no_data_securities must list each asked security that returned no data")
        if "FPNIX" not in {x.get("ticker") for x in nod} and not a.get("fpnix_note"):
            fail("FPNIX is neither among the no-data securities nor explained")
        print("OK: %d securities: %d with no ticker, %d returned data, %d returned none; %d call(s), each ticker asked once" % (
            s["total"], s[keys[1]], s[keys[2]], s[keys[3]], len(calls)))
    elif cid == "IB136-1-AC2":
        e = a.get("account_day_effect") or {}
        if any(not isinstance(e.get(k), int) for k in OUTCOMES + ("account_days_holding_an_outside_anchor_row",
                                                                 "freed_and_holding_no_other_ungradeable_kind")):
            fail("account_day_effect lacks an integer count")
        if sum(e[k] for k in OUTCOMES) != e["account_days_holding_an_outside_anchor_row"]:
            fail("the four outcomes sum to %d, the account-days holding an outside-anchor row are %d" % (
                sum(e[k] for k in OUTCOMES), e["account_days_holding_an_outside_anchor_row"]))
        if e["freed_and_holding_no_other_ungradeable_kind"] > e[OUTCOMES[0]]:
            fail("more account-days are freed than hold every security at the day's NAV")
        z = a.get("sizing_under_v036") or {}
        ad, sv = z.get("account_days") or {}, z.get("serving_rule") or {}
        if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)) or sum(ad[k] for k in CLAIMS) != ad["present"]:
            fail("sizing_under_v036.account_days does not sum to present")
        if same and ad["present"] != 76796:
            fail("the same account-days are said to be read, yet present is %d" % ad["present"])
        if any(not isinstance(sv.get(k), int) for k in ("eligible", "served", "blank", "accounts_never_served")) \
                or sv["served"] + sv["blank"] != sv["eligible"] or not isinstance(sv.get("blank_share_percent"), (int, float)):
            fail("sizing_under_v036.serving_rule is incomplete or does not add up")
        if not z.get("what_is_assumed"):
            fail("sizing_under_v036.what_is_assumed is not stated")
        print("OK: %d of %d account-days freed (%d with no other ungradeable kind); sized blank share %.1f%% of %d; never served %d" % (
            e[OUTCOMES[0]], e["account_days_holding_an_outside_anchor_row"], e["freed_and_holding_no_other_ungradeable_kind"],
            sv["blank_share_percent"], sv["eligible"], sv["accounts_never_served"]))
    elif cid == "IB136-1-AC3":
        p = a.get("prior_day_rows") or {}
        if any(not isinstance(p.get(k), int) for k in ("rows_equal_only_to_prior_day_nav", "rows_with_a_nav", "days_they_fall_on",
                                                       "account_days_they_blank")):
            fail("prior_day_rows lacks an integer count")
        c = a.get("control") or {}
        if not c.get("security") or c.get("carried_by_anchor") is not True or not isinstance(c.get("days_compared"), int) \
                or c["days_compared"] < 20 or not isinstance(c.get("days_equal"), int):
            fail("control needs a security the anchor carries with at least 20 days compared")
        if c["days_equal"] < 0.9 * c["days_compared"] and not c.get("difference_explained"):
            fail("the control reads %d of %d equal and no explanation is given" % (c["days_equal"], c["days_compared"]))
        if a.get("claims_regraded_in_product") is not False or a.get("other_sources_asked") != 0:
            fail("claims_regraded_in_product must be false and other_sources_asked 0")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: %d of %d rows sit only at the prior day's NAV, on %d day(s), blanking %d account-day(s); control %s equal on %d of %d" % (
            p["rows_equal_only_to_prior_day_nav"], p["rows_with_a_nav"], p["days_they_fall_on"], p["account_days_they_blank"],
            c["security"], c["days_equal"], c["days_compared"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
