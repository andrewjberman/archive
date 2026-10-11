"""IRPT_BCKEND round 140 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB140-1  IB-pr-443  the five one-day-off security-days of IB-pr-441: a THIRD dated value beside both witnesses, and for each
                      which witness sits on the wrong day or that it cannot be told; and whether the first witness's partition
                      for the window's last day is the prior day's (CTO msg 5501).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB140-1-AC1  exactly the five security-days are tabled, the two the CTO names among them, each with both witnesses' values for
               the day and the days either side and its third dated value (or that none exists).
  IB140-1-AC2  each has ONE verdict (the first witness off, the second witness off, or cannot be told) with its claim; a verdict
               that names a witness cites the evidence that decides it.
  IB140-1-AC3  the last-day question is answered with its counts and claim; the fetch was one pass; the control reads as planted;
               no class is admitted; no account id in the outputs.
The verdicts are UNMEASURED by the issuer; "cannot be told" passes as well as a named witness.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~301/"
OUT = D + "IB140-1_five_days_third_value.json"
READ = D + "IB140-1_FIVE_DAYS_THIRD_VALUE_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
VERDICTS = ("FIRST_WITNESS_OFF", "SECOND_WITNESS_OFF", "CANNOT_BE_TOLD")
CLAIMS = ("measured", "inferred", "held", "absent")
NAMED = {("MEIIX", "2026-07-02"), ("MISIX", "2026-10-09")}
TICKERS = {"MEIIX", "MISIX", "SHM", "PZA"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB140"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    days = a.get("security_days")
    if not isinstance(days, list):
        fail("security_days is not a list")
    if cid == "IB140-1-AC1":
        keys = {(d.get("ticker"), d.get("date")) for d in days}
        if len(days) != 5 or len(keys) != 5:
            fail("%d security-day(s) tabled (%d distinct); five are expected" % (len(days), len(keys)))
        if not NAMED <= keys or not {k[0] for k in keys} <= TICKERS:
            fail("the tabled days %r do not hold the two named days, or name a ticker outside %r" % (sorted(keys), sorted(TICKERS)))
        if a.get("the_five_are_those_of_ib_pr_441") is not True:
            fail("the record does not say the five are those of IB-pr-441's one-day-off detail")
        for d in days:
            for w in ("first_witness", "second_witness"):
                v = d.get(w) or {}
                if any(k not in v for k in ("prior_day", "day", "next_day")):
                    fail("%s %s: %s lacks prior_day, day or next_day" % (d.get("ticker"), d.get("date"), w))
            t = d.get("third_value") or {}
            if t.get("found") not in (True, False) or (t["found"] and not t.get("values")) or (not t["found"] and not t.get("where_looked")):
                fail("%s %s: third_value needs found, and its values or where it was looked for" % (d.get("ticker"), d.get("date")))
        print("OK: 5 of 5 security-days tabled with both witnesses over three days; a third value found on %d" % sum(
            1 for d in days if d["third_value"]["found"]))
    elif cid == "IB140-1-AC2":
        n = dict.fromkeys(VERDICTS, 0)
        for d in days:
            v = d.get("verdict")
            if v not in VERDICTS or d.get("claim") not in CLAIMS or not d.get("reason"):
                fail("%s %s: verdict %r, claim %r, or no reason" % (d.get("ticker"), d.get("date"), v, d.get("claim")))
            if v != "CANNOT_BE_TOLD" and not d.get("deciding_evidence"):
                fail("%s %s names a witness and cites no deciding evidence" % (d.get("ticker"), d.get("date")))
            if v != "CANNOT_BE_TOLD" and d["claim"] == "absent":
                fail("%s %s names a witness on an absent claim" % (d.get("ticker"), d.get("date")))
            n[v] += 1
        if a.get("verdict_counts") != n:
            fail("verdict_counts %r is not the table's %r" % (a.get("verdict_counts"), n))
        print("OK: verdicts over the five: %s" % n)
    elif cid == "IB140-1-AC3":
        q = a.get("last_day_first_witness_partition") or {}
        if q.get("is_the_prior_days") not in (True, False, None) or "is_the_prior_days" not in q or q.get("claim") not in CLAIMS:
            fail("last_day_first_witness_partition needs is_the_prior_days (true, false or null) and a claim")
        if any(not isinstance(q.get(k), int) for k in ("securities_compared", "equal_to_second_witness_same_day", "equal_to_second_witness_prior_day")):
            fail("last_day_first_witness_partition lacks its three counts")
        if q["is_the_prior_days"] is None and q["claim"] != "absent":
            fail("an untold last-day answer must carry the claim absent")
        fe = a.get("fetch") or {}
        calls = fe.get("calls")
        if not isinstance(calls, list) or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
            fail("fetch.calls must list every call with its ticker count, none over 50")
        if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0:
            fail("the fetch is not one pass")
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the control does not read as planted")
        if a.get("classes_admitted_by_this_cell") != 0 or a.get("other_sources_asked") != 0:
            fail("classes_admitted_by_this_cell and other_sources_asked must both be 0")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: last day: is the prior day's = %r (%s), %d compared; %d call(s); control as planted; 0 account-id tokens" % (
            q["is_the_prior_days"], q["claim"], q["securities_compared"], len(calls)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
