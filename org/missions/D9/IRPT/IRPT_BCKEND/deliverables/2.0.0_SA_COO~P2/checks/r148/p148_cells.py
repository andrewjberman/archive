"""IRPT_BCKEND round 148 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY, counts-only order:
  IB148-1  IB-pr-452  the sizing under PRD v0.42 (signed): nine admitted pairs under BOTH guard sentences; the same with five
                      named securities not graded by the second witness; and how many securities of the nine pairs, outside
                      the first witness, repeat their bar on more than half their days (CTO msg 5724).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB148-1-AC1  the reproduction holds first (IB-pr-445's seven-plus-Inst sizing under the first guard sentence alone), and the
               two new sizings are printed and each adds up (four claims sum to the account-days present; served + blank ==
               eligible); excluding five securities never frees more account-days than including them.
  IB148-1-AC2  the repeat count: per pair, securities outside the first witness with bars, and those un-graded on more than half
               their days, listed by ticker with their days; the per-pair counts sum to the total and to the list's length.
  IB148-1-AC3  the bounds: one fetch pass, the control as planted, nothing re-graded, no class admitted or excluded by the cell,
               no account id in the outputs.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~308/"
OUT, READ = D + "IB148-1_nine_pair_sizing.json", D + "IB148-1_NINE_PAIR_SIZING_READ.md"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~303/IB142-1_unmoved_bar_guard.json"
SIZINGS = ("nine_pairs_under_both_guard_sentences", "nine_pairs_with_the_five_not_graded")
FIVE = ["ADLYX", "BISOX", "EIBLX", "GPPIX", "OLCYX"]
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB148"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    if cid == "IB148-1-AC1":
        prior = json.loads((root / PRIOR).read_text(encoding="utf-8"))["sizings"]["seven_types_and_inst_under_the_guard"]
        rep = a.get("reproduces_ib_pr_445_seven_and_inst_first_sentence_only") or {}
        if rep.get("reproduces") is not True or (rep.get("read") or {}).get("account_days") != prior["account_days"] \
                or (rep.get("read") or {}).get("freed_and_holding_no_other_ungradeable_kind") != prior["freed_and_holding_no_other_ungradeable_kind"]:
            fail("the seven-plus-Inst sizing under the first guard sentence alone does not reproduce IB-pr-445's")
        z = a.get("sizings") or {}
        if set(z) != set(SIZINGS):
            fail("sizings must be exactly %s" % (SIZINGS,))
        for k in SIZINGS:
            s = z[k]
            ad, sr = s.get("account_days") or {}, s.get("serving_rule") or {}
            if any(not isinstance(ad.get(c), int) for c in CLAIMS) or sum(ad[c] for c in CLAIMS) != ad.get("present"):
                fail("%s: the four claims do not sum to the account-days present" % k)
            if not all(isinstance(sr.get(x), int) for x in ("eligible", "served", "blank", "accounts_never_served")) \
                    or sr["served"] + sr["blank"] != sr["eligible"] or not isinstance(sr.get("blank_share_percent"), (int, float)):
                fail("%s: served + blank does not equal eligible, or a serving figure is missing" % k)
            if abs(sr["blank_share_percent"] - 100.0 * sr["blank"] / sr["eligible"]) > 0.001:
                fail("%s: blank_share_percent is not blank over eligible" % k)
            if not isinstance(s.get("freed_and_holding_no_other_ungradeable_kind"), int):
                fail("%s: freed_and_holding_no_other_ungradeable_kind missing" % k)
        both, less = z[SIZINGS[0]], z[SIZINGS[1]]
        if less["freed_and_holding_no_other_ungradeable_kind"] > both["freed_and_holding_no_other_ungradeable_kind"] \
                or less["account_days"]["UNGRADEABLE"] < both["account_days"]["UNGRADEABLE"]:
            fail("not grading five securities freed more account-days, or un-graded fewer, than grading them")
        if a.get("the_five_not_graded") != FIVE:
            fail("the_five_not_graded must be exactly %s" % FIVE)
        if not isinstance(a.get("pairs_admitted"), list) or len(a["pairs_admitted"]) != 9:
            fail("pairs_admitted must list the nine pairs as the source writes them")
        print("OK: nine pairs blank %.3f%%, never served %d, freed %d; with the five not graded %.3f%%, %d, %d" % (
            both["serving_rule"]["blank_share_percent"], both["serving_rule"]["accounts_never_served"], both["freed_and_holding_no_other_ungradeable_kind"],
            less["serving_rule"]["blank_share_percent"], less["serving_rule"]["accounts_never_served"], less["freed_and_holding_no_other_ungradeable_kind"]))
    elif cid == "IB148-1-AC2":
        r = a.get("repeating_on_more_than_half_their_days") or {}
        bp, lst = r.get("by_pair"), r.get("securities")
        if not isinstance(bp, dict) or len(bp) != 9 or not isinstance(lst, list) or not isinstance(r.get("total"), int):
            fail("repeating_on_more_than_half_their_days needs by_pair (nine pairs), securities and total")
        for p, x in bp.items():
            if not all(isinstance(x.get(k), int) for k in ("securities_outside_the_first_witness_with_bars", "repeating_on_more_than_half")) \
                    or x["repeating_on_more_than_half"] > x["securities_outside_the_first_witness_with_bars"]:
                fail("%s: per-pair counts missing or inconsistent" % p[-14:])
        if sum(x["repeating_on_more_than_half"] for x in bp.values()) != r["total"] or len(lst) != r["total"]:
            fail("the per-pair counts, the total and the list's length do not agree")
        for x in lst:
            if not x.get("ticker") or not x.get("pair") or not isinstance(x.get("days_with_a_bar"), int) or not isinstance(x.get("days_not_graded"), int) \
                    or 2 * x["days_not_graded"] <= x["days_with_a_bar"]:
                fail("a listed security is not un-graded on more than half its days: %r" % (x.get("ticker"),))
        if not r.get("rule_in_words"):
            fail("the rule is not stated in words")
        missing = [t for t in FIVE if t not in [x["ticker"] for x in lst]]
        if missing and not r.get("of_the_five_not_listed_explained"):
            fail("of the five, %s are not in the list and no explanation is given" % missing)
        print("OK: %d securities of the nine pairs outside the first witness repeat on more than half their days" % r["total"])
    elif cid == "IB148-1-AC3":
        fe = a.get("fetch") or {}
        if not isinstance(fe.get("call_count"), int) or fe.get("tickers_asked_more_than_once") != 0 or fe.get("counted_before_fetching") is not True:
            fail("fetch needs call_count, tickers_asked_more_than_once 0 and counted_before_fetching true")
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the planted control was not read back as planted")
        for k in ("claims_regraded_in_product", "classes_admitted_by_this_cell", "securities_excluded_by_this_cell", "other_sources_asked"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not a.get("what_is_assumed") or not isinstance(a.get("not_established"), list):
            fail("what_is_assumed and not_established must be stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        n = len(re.findall(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text + rd.read_text(encoding="utf-8")))
        if n:
            fail("%d eight-digit token(s) in the outputs: an account id may not be written" % n)
        print("OK: %d call(s), each ticker once; control as planted; nothing re-graded, admitted or excluded; 0 account-id tokens" % fe["call_count"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
