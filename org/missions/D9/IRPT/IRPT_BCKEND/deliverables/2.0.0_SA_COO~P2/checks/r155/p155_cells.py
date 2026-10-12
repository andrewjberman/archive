"""IRPT_BCKEND round 155 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order, two measurements (CTO msg 6004):
  IB155-1  IB-pr-459  (1) do the LANDED prices store's yahoo-labelled points equal the unadjusted Close for the 878 tickers, and
                      what is that store's refresh schedule; (2) one read through the performance route's READER for an account
                      whose window holds a non-OK day: days_excluded, claim, absences, as the reader answers.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB155-1-AC1  the store: its address as the code builds it, its object's last-modified reads, its writer and schedule (or "none
               found" with what was searched); the 878 tickers each placed in exactly one of five outcomes, no remainder; the
               ticker-days compared split equal / not equal with no remainder.
  IB155-1-AC2  the route read: which arm was made (the deployed route, or the reader's own code over the served gold, said
               plainly), the window, the non-OK day's status, and the answer's days_excluded, claim and absences; a control
               account with no non-OK day read the same way.
  IB155-1-AC3  the bounds: one fetch pass, nothing written to AWS, no sign-in as a service or a person, no account id in the
               outputs, nothing built or proposed.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~315/"
OUT, READ = D + "IB155-1_two_measurements.json", D + "IB155-1_TWO_MEASUREMENTS_READ.md"
TICKER_OUTCOMES = ("every_compared_day_equal", "some_days_not_equal", "no_yahoo_labelled_point_in_the_store", "not_in_the_store", "no_bar_from_the_reader")
ARMS = ("DEPLOYED_ROUTE", "READER_CODE_OVER_SERVED_GOLD", "NOT_MADE")
CLAIMS = ("measured", "inferred", "held", "absent")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB155"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    if cid == "IB155-1-AC1":
        s = a.get("landed_prices_store") or {}
        if not s.get("address_built_by") or ":" not in str(s.get("address_built_by")) or not s.get("last_modified_utc") or not isinstance(s.get("rows"), int) \
                or not s.get("how_a_point_is_labelled_yahoo"):
            fail("landed_prices_store needs address_built_by (file:line), last_modified_utc, rows and how_a_point_is_labelled_yahoo")
        r = s.get("refresh") or {}
        if r.get("schedule_found") not in (True, False) or r.get("claim") not in CLAIMS or not r.get("searched") \
                or (r["schedule_found"] and (not r.get("writer") or not r.get("schedule_or_trigger"))) or not isinstance(r.get("last_modified_history"), list):
            fail("refresh needs schedule_found, claim, searched, last_modified_history and (when found) writer and schedule_or_trigger")
        t = a.get("tickers") or {}
        o = t.get("outcomes") or {}
        if set(o) != set(TICKER_OUTCOMES) or any(not isinstance(v, int) for v in o.values()) or sum(o.values()) != t.get("asked") or t.get("asked") != 878:
            fail("tickers.outcomes must place each of the 878 tickers in exactly one of %s" % (TICKER_OUTCOMES,))
        d = a.get("ticker_days") or {}
        if not all(isinstance(d.get(k), int) for k in ("compared", "equal", "not_equal")) or d["equal"] + d["not_equal"] != d["compared"] or not d.get("equality_rule"):
            fail("ticker_days: equal + not_equal must sum to compared, with the equality rule stated")
        if not isinstance(a.get("not_equal_by_cause"), dict) or sum(a["not_equal_by_cause"].values()) != d["not_equal"]:
            fail("not_equal_by_cause must account for every unequal ticker-day")
        if a.get("the_store_holds_the_unadjusted_close") not in ("YES_FOR_EVERY_COMPARED_TICKER", "FOR_SOME", "NO", "CANNOT_BE_TOLD"):
            fail("the_store_holds_the_unadjusted_close must be one of the four words")
        print("OK: 878 tickers %s; %d of %d ticker-days equal; the store holds the unadjusted Close: %s; schedule found: %s" % (
            o, d["equal"], d["compared"], a["the_store_holds_the_unadjusted_close"], r["schedule_found"]))
    elif cid == "IB155-1-AC2":
        r = a.get("route_read") or {}
        if r.get("arm") not in ARMS or not r.get("arm_in_words"):
            fail("route_read.arm must be one of %s, with arm_in_words" % (ARMS,))
        if r["arm"] == "NOT_MADE":
            if not r.get("why_not_made"):
                fail("NOT_MADE needs why_not_made")
            print("OK: the route read was not made: stated")
        else:
            for k in ("with_a_non_ok_day", "control_all_ok"):
                x = r.get(k) or {}
                if not x.get("window") or not isinstance(x.get("days_in_window"), int) or not isinstance(x.get("non_ok_days"), int) \
                        or "days_excluded" not in x or "claim" not in x or "absences" not in x or not isinstance(x.get("answer_keys"), list):
                    fail("route_read.%s needs window, days_in_window, non_ok_days, days_excluded, claim, absences and answer_keys" % k)
            if r["with_a_non_ok_day"]["non_ok_days"] < 1 or r["control_all_ok"]["non_ok_days"] != 0:
                fail("the first account must hold a non-OK day and the control none")
            if not r["with_a_non_ok_day"].get("non_ok_status_values") or r.get("chained_over_the_non_ok_day") not in (True, False, None):
                fail("non_ok_status_values and chained_over_the_non_ok_day must be stated")
            if not r.get("entry") or not r.get("reader_code_line") or ":" not in str(r["reader_code_line"]):
                fail("route_read needs the sources.json entry key and reader_code_line")
            print("OK: arm %s; with a non-OK day: days_excluded %r, claim %r; chained over it: %r" % (
                r["arm"], r["with_a_non_ok_day"]["days_excluded"], r["with_a_non_ok_day"]["claim"], r["chained_over_the_non_ok_day"]))
    elif cid == "IB155-1-AC3":
        fe = a.get("fetch") or {}
        if fe.get("tickers_asked_more_than_once") != 0 or fe.get("counted_before_fetching") is not True or not isinstance(fe.get("call_count"), int):
            fail("fetch needs call_count, tickers_asked_more_than_once 0 and counted_before_fetching true")
        for k in ("aws_writes_made", "sign_ins_made", "functions_invoked", "product_files_edited", "builds_proposed", "other_sources_asked"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list):
            fail("not_established is not stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        # AMENDMENT 2 (row IRPT_BCKEND-D2-W315-S1): AC1 requires the store's row count as an integer and the count has eight
        # digits; a count is not an account id. The json's integer VALUES are scrubbed before the test, and so is the same
        # count where the read file writes it; an eight-digit token inside any STRING of the json still fails.
        def strings(o):
            if isinstance(o, dict):
                return " ".join(strings(k) + " " + strings(v) for k, v in o.items())
            if isinstance(o, list):
                return " ".join(strings(v) for v in o)
            return o if isinstance(o, str) else ""
        def ints(o):
            if isinstance(o, dict):
                return [i for v in o.values() for i in ints(v)]
            if isinstance(o, list):
                return [i for v in o for i in ints(v)]
            return [o] if isinstance(o, int) and not isinstance(o, bool) else []
        md = rd.read_text(encoding="utf-8")
        for n in sorted({str(i) for i in ints(a) if len(str(abs(i))) == 8}):
            md = md.replace(n, "<count>")
        if re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", strings(a) + " " + md):
            fail("an eight-digit token is in the outputs: an account id may not be written")
        print("OK: %d call(s), each ticker once; no AWS write, no sign-in, no invoke; nothing built or proposed" % fe["call_count"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
