"""IRPT_BCKEND round 162 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msg 6362):
  IB162-1  IB-pr-468  the request file for dell1's demand queue: the 878 tickers, 125 trading days, plus daily enrolment.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Both FAIL at base (no file).
  IB162-1-AC1  the request file carries the queue's keys, tier 2, fields ["close"], 878 distinct symbols each with a cusip
               or a stated cusip claim, a start and an end 125 trading days apart, and the daily enrolment.
  IB162-1-AC2  the derivation record: no price fetched, nothing invoked, no account written; the list reproduces 878.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~323/"
REQ, REC = D + "IRPT_BCKEND-AS-TRADED-CLOSES-878.json", D + "IB162-1_request_derivation.json"
KEYS = ("request_id", "tier", "reason", "page", "securities", "fields", "start", "end")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB162"))
        sys.exit(1)

    for p in (REQ, REC):
        if not (root / p).is_file():
            fail("no %s" % p)
    q = json.loads((root / REQ).read_text(encoding="utf-8"))
    r = json.loads((root / REC).read_text(encoding="utf-8"))
    if cid == "IB162-1-AC1":
        miss = [k for k in KEYS if k not in q]
        if miss:
            fail("the request lacks %s" % miss)
        if q["request_id"] != "IRPT_BCKEND-AS-TRADED-CLOSES-878" or q["tier"] != 2 or q["fields"] != ["close"]:
            fail("request_id, tier 2 and fields [\"close\"]")
        s = q["securities"]
        if not isinstance(s, list) or len(s) != 878 or len({x.get("symbol") for x in s}) != 878:
            fail("securities must be 878 entries with 878 distinct symbols (got %s)" % (len(s) if isinstance(s, list) else type(s).__name__))
        for x in s:
            if not x.get("symbol") or not (x.get("cusip") or x.get("cusip_claim") == "absent"):
                fail("every security carries a symbol and a cusip, or cusip_claim absent")
        if r.get("trading_days_start_to_end_inclusive") != 125 or r.get("start") != q["start"] or r.get("end") != q["end"]:
            fail("the record must count 125 trading days from start to end, the request's own dates")
        e = q.get("standing_enrolment")
        if not isinstance(e, dict) or e.get("tier") != 1 or not e.get("in_words"):
            fail("standing_enrolment {tier: 1, in_words}")
        print("OK: 878 securities, %d with a cusip; %s to %s; daily enrolment asked" % (sum(1 for x in s if x.get("cusip")), q["start"], q["end"]))
    elif cid == "IB162-1-AC2":
        for k in ("prices_fetched", "vendor_calls_made", "functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "values_written"):
            if r.get(k) != 0:
                fail("%s must be 0" % k)
        if r.get("tickers_derived") != 878 or not r.get("derivation_in_words") or not r.get("calendar_rule_in_words"):
            fail("tickers_derived 878, derivation_in_words and calendar_rule_in_words")
        if not isinstance(r.get("not_established"), list) or not r.get("base_commit"):
            fail("not_established and base_commit")
        print("OK: the list reproduces 878; no price fetched, nothing invoked, no account written")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
