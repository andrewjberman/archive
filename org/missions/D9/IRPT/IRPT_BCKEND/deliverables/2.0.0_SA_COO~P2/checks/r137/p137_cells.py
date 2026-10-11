"""IRPT_BCKEND round 137 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB137-1  IB-pr-439  under PRD ADDENDUM v0.38: the source's instrument-type field; every security BOTH witnesses carry, per
                      type, days equal / one day off / neither; the sizing with funds outside; and a count of fund-dates that
                      carry a priced custodian purchase or redemption (CTO msg 5298).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB137-1-AC1  the instrument-type field is named with its distinct values and counts summing to the rows read, OR the record
               says none exists and that the cell stopped there (both branches are graded).
  IB137-1-AC2  where a type field exists: per instrument type, the security-days of the securities both witnesses carry split
               with no remainder into equal / one day off / neither / no bar; the fetch was one pass; the types whose
               one-day-off column is empty are listed and are exactly those the table shows. Where none exists: the stop is
               stated and no overlap table is present.
  IB137-1-AC3  the sizing under v0.38 adds up (four claims sum to the account-days present; served + blank == eligible; funds are
               not admitted); the fund-transaction count is stated with its source and window, or that no source was found; the
               control holds; no account id is in the outputs.
Every count is UNMEASURED by the issuer. The checks grade sums, the one-pass bound, the listed-versus-shown agreement and the
control. One figure of earlier reads (76,796 account-days present) binds only when the same account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~297/"
OUT = D + "IB137-1_witness_overlap_by_type.json"
READ = D + "IB137-1_WITNESS_OVERLAP_BY_TYPE_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
COLS = ("equal", "one_day_off", "neither", "no_bar")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB137"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    t = a.get("instrument_type_field") or {}
    present = t.get("present")
    if present not in (True, False):
        fail("instrument_type_field.present must be true or false")
    if cid == "IB137-1-AC1":
        if not isinstance(t.get("columns_read"), list) or not t["columns_read"]:
            fail("instrument_type_field.columns_read must list the source's columns that were read")
        if present:
            v = t.get("values")
            if not t.get("name") or not isinstance(v, dict) or not v or any(not isinstance(x, int) for x in v.values()):
                fail("a present type field needs its name and its distinct values with integer counts")
            if sum(v.values()) != t.get("rows_read"):
                fail("the values' counts sum to %d, rows_read is %r" % (sum(v.values()), t.get("rows_read")))
            print("OK: type field %s, %d distinct value(s) over %d rows" % (t["name"], len(v), t["rows_read"]))
        else:
            if a.get("stopped_no_type_field") is not True or not t.get("candidates_examined"):
                fail("with no type field the record must say it stopped and which columns were examined as candidates")
            print("OK: no instrument-type field; %d candidate column(s) examined; the cell stopped there" % len(t["candidates_examined"]))
    elif cid == "IB137-1-AC2":
        o = a.get("overlap_by_type")
        if not present:
            if o:
                fail("no type field exists, yet an overlap table is present")
            print("OK: no type field, so no security is admitted and no overlap table is drawn")
        else:
            if not isinstance(o, dict) or not o:
                fail("overlap_by_type is empty")
            empty = []
            for name, r in o.items():
                if any(not isinstance(r.get(k), int) for k in COLS + ("securities", "security_days")):
                    fail("type %s lacks an integer count" % name)
                if sum(r[k] for k in COLS) != r["security_days"]:
                    fail("type %s: the four columns sum to %d, security_days is %d" % (name, sum(r[k] for k in COLS), r["security_days"]))
                if r["one_day_off"] == 0 and r["equal"] > 0:
                    empty.append(name)
            if sorted(a.get("types_with_an_empty_one_day_off_column") or []) != sorted(empty):
                fail("the listed types %r are not the ones the table shows %r" % (a.get("types_with_an_empty_one_day_off_column"), empty))
            fe = a.get("fetch") or {}
            calls = fe.get("calls")
            if not isinstance(calls, list) or not calls or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
                fail("fetch.calls must list every call with its ticker count, none over 50")
            if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0:
                fail("the fetch is not one pass: the calls' tickers do not equal the distinct tickers asked, or one was asked twice")
            if not a.get("one_day_off_rule") or not a.get("unchanged_price_rule"):
                fail("one_day_off_rule and unchanged_price_rule are not stated")
            print("OK: %d type(s); %d with an empty one-day-off column: %s; %d call(s), each ticker asked once" % (len(o), len(empty), empty, len(calls)))
    elif cid == "IB137-1-AC3":
        z = a.get("sizing_under_v038") or {}
        ad, sv = z.get("account_days") or {}, z.get("serving_rule") or {}
        if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)) or sum(ad[k] for k in CLAIMS) != ad["present"]:
            fail("sizing_under_v038.account_days does not sum to present")
        if a.get("same_account_days_read") is True and ad["present"] != 76796:
            fail("the same account-days are said to be read, yet present is %d" % ad["present"])
        if a.get("same_account_days_read") is not True and not a.get("source_difference_explained"):
            fail("same_account_days_read is not true and the record does not say why")
        if any(not isinstance(sv.get(k), int) for k in ("eligible", "served", "blank", "accounts_never_served")) \
                or sv["served"] + sv["blank"] != sv["eligible"] or not isinstance(sv.get("blank_share_percent"), (int, float)):
            fail("sizing_under_v038.serving_rule is incomplete or does not add up")
        if z.get("mutual_funds_admitted") is not False or not isinstance(z.get("classes_admitted"), list) or not z.get("what_is_assumed"):
            fail("the sizing must say mutual_funds_admitted false, list classes_admitted and state what_is_assumed")
        if not present and z["classes_admitted"]:
            fail("no type field exists, yet classes are admitted in the sizing")
        ft = a.get("fund_transactions") or {}
        if ft.get("source_found") is True:
            if any(k not in ft for k in ("table", "first_date", "last_date")) or any(
                    not isinstance(ft.get(k), int) for k in ("fund_dates_with_a_priced_purchase_or_redemption", "funds", "of_which_inside_the_85_days")):
                fail("fund_transactions needs its table, window and three integer counts")
        elif ft.get("source_found") is False:
            if not ft.get("where_looked"):
                fail("no transaction source was found and the record does not say where it looked")
        else:
            fail("fund_transactions.source_found must be true or false")
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the control does not read as planted")
        if a.get("claims_regraded_in_product") is not False or a.get("other_sources_asked") != 0:
            fail("claims_regraded_in_product must be false and other_sources_asked 0")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: sizing under v0.38: blank %.1f%% of %d, never served %d, classes admitted %s; fund-transaction source found: %s" % (
            sv["blank_share_percent"], sv["eligible"], sv["accounts_never_served"], z["classes_admitted"], ft["source_found"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
