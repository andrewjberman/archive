"""IRPT_BCKEND round 145 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY, counts-only order:
  IB145-1  IB-pr-449  what the second witness's bar is when it MOVES after a repeated run (CTO msg 5624, PRD v0.40): for the
                      overlap securities of the two fund pairs left out, the first moved bar after each repeated run, beside the
                      anchor; and, for the six institutional securities that repeat on more than half their days, their moved days.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB145-1-AC1  for each of the two pairs: securities, repeated runs, and every run's first moved day placed in exactly one of
               five outcomes, no remainder; the guard-on totals of IB-pr-445 for the pair are reproduced first.
  IB145-1-AC2  the six securities: each with its days with a bar, unmoved, moved (summing), and its held rows on moved days
               placed in exactly one of three outcomes, no remainder; the six are those IB-pr-445 named.
  IB145-1-AC3  the bounds held: one fetch pass with each ticker asked once, a planted control read back, nothing re-graded,
               no class admitted, no account id in the outputs.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~306/"
OUT, READ = D + "IB145-1_first_moved_bar.json", D + "IB145-1_FIRST_MOVED_BAR_READ.md"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~303/IB142-1_unmoved_bar_guard.json"
PAIRS = ("Securities Issued by Registered Investment Companies or Business Development Companies / Inst",
         "Securities Issued by Registered Investment Companies or Business Development Companies / Not Available")
RUN_OUTCOMES = ("equals_the_anchor_same_day", "equals_the_anchor_prior_day", "equals_neither", "no_anchor_that_day", "no_moved_day_in_window")
ROW_OUTCOMES = ("equals_the_bar_same_day", "equals_the_bar_prior_day", "equals_neither")
SIX = ("ADLYX", "BISOX", "EIBLX", "GPPIX", "JSOSX", "OLCYX")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB145"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    if cid == "IB145-1-AC1":
        prior = json.loads((root / PRIOR).read_text(encoding="utf-8"))["overlap_by_type_under_the_guard"]
        by = a.get("first_moved_bar_by_pair") or {}
        for p in PAIRS:
            x = by.get(p)
            if not isinstance(x, dict):
                fail("pair missing: %s" % p)
            rep = x.get("reproduces_ib_pr_445_under_the_guard") or {}
            for k in ("equal", "one_day_off", "neither", "no_bar", "not_graded_under_the_guard"):
                if rep.get(k) != prior[p].get(k):
                    fail("%s: %s is %r, IB-pr-445 read %r" % (p[-14:], k, rep.get(k), prior[p].get(k)))
            o = x.get("first_moved_day_after_a_run") or {}
            if set(o) != set(RUN_OUTCOMES) or any(not isinstance(v, int) or v < 0 for v in o.values()):
                fail("%s: outcomes must be exactly %s" % (p[-14:], RUN_OUTCOMES))
            if not isinstance(x.get("repeated_runs"), int) or sum(o.values()) != x["repeated_runs"]:
                fail("%s: the outcomes do not sum to repeated_runs" % p[-14:])
            if not isinstance(x.get("securities"), int) or not isinstance(x.get("securities_with_a_repeated_run"), int) \
                    or x["securities_with_a_repeated_run"] > x["securities"]:
                fail("%s: securities and securities_with_a_repeated_run" % p[-14:])
            if not isinstance(x.get("days_in_runs"), int) or x["days_in_runs"] < x["repeated_runs"]:
                fail("%s: days_in_runs is below the number of runs" % p[-14:])
        if not a.get("run_rule_in_words") or not a.get("first_moved_day_rule_in_words"):
            fail("the run rule and the first-moved-day rule are not stated in words")
        print("OK: " + "; ".join("%s: %d run(s) %s" % (p.split(" / ")[-1], by[p]["repeated_runs"], by[p]["first_moved_day_after_a_run"]) for p in PAIRS))
    elif cid == "IB145-1-AC2":
        named = json.loads((root / PRIOR).read_text(encoding="utf-8"))["inst_under_the_guard"]["securities_ungraded_on_more_than_half_their_days"]
        if not all(t in json.dumps(named) for t in SIX):
            fail("the prior record does not name the six this check expects")
        six = a.get("the_six") or {}
        if set(six) != set(SIX):
            fail("the_six must be keyed by exactly %s" % (SIX,))
        for t, x in six.items():
            if not all(isinstance(x.get(k), int) for k in ("days_with_a_bar", "days_unmoved", "days_moved", "days_with_no_prior_bar")):
                fail("%s: day counts missing" % t)
            if x["days_unmoved"] + x["days_moved"] + x["days_with_no_prior_bar"] != x["days_with_a_bar"]:
                fail("%s: unmoved + moved + no-prior-bar does not sum to days with a bar" % t)
            o = x.get("held_rows_on_moved_days") or {}
            if set(o) != set(ROW_OUTCOMES) or not isinstance(x.get("rows_held_on_moved_days"), int) or sum(o.values()) != x["rows_held_on_moved_days"]:
                fail("%s: held rows on moved days must fall in exactly %s and sum" % (t, ROW_OUTCOMES))
            if x.get("anchor_carries_it") is not False and "anchor_carries_it" in x and not isinstance(x.get("anchor_carries_it"), bool):
                fail("%s: anchor_carries_it must be a boolean" % t)
        print("OK: " + "; ".join("%s moved %d of %d, rows %s" % (t, six[t]["days_moved"], six[t]["days_with_a_bar"],
                                                            list(six[t]["held_rows_on_moved_days"].values())) for t in SIX))
    elif cid == "IB145-1-AC3":
        fe = a.get("fetch") or {}
        if not isinstance(fe.get("call_count"), int) or fe.get("tickers_asked_more_than_once") != 0 or fe.get("counted_before_fetching") is not True:
            fail("fetch needs call_count, tickers_asked_more_than_once 0 and counted_before_fetching true")
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the planted control was not read back as planted")
        if a.get("claims_regraded_in_product") != 0 or a.get("classes_admitted_by_this_cell") != 0 or a.get("other_sources_asked") != 0:
            fail("claims_regraded_in_product, classes_admitted_by_this_cell and other_sources_asked must each be 0")
        if not isinstance(a.get("not_established"), list):
            fail("not_established is not stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        n = len(re.findall(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text + rd.read_text(encoding="utf-8")))
        if n:
            fail("%d eight-digit token(s) in the outputs: an account id may not be written" % n)
        print("OK: %d call(s), each ticker once; control as planted; nothing re-graded, no class admitted; 0 account-id tokens" % fe["call_count"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
