"""IRPT_DASHBD round 100 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 7422 ("read how the 11 CASH lots classify, served class per lot and per page").

  DB-b-186 (~151, LOCAL)  a READ: the cash-stem ticker lots in the newest Black Diamond lot snapshot (11 of 1,314,777 in the 2026-10-09 snapshot, anchored by this seat's own read):
                          the canonical row, what the gold classifier returns for the ticker, the class the Advisor Intelligence and Investor Reporting pages serve for it.  DB100-1-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import json
import re
import sys
from pathlib import Path

RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~151/CASH_LOTS_CLASS_READ.json"
ANCHOR_SNAPSHOT = "2026-10-09"
ANCHOR_LOTS = 11
ANCHOR_ROWS = 1314777
RUN = re.compile(r"\d{8,}")
PAGES = ("advisor_intelligence", "investor_reporting")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def nes(v):
    return isinstance(v, str) and v.strip() != ""


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k) not in ("path", "key", "file"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def check(root):
    p = root / RECORD
    need(p.is_file(), "no %s" % RECORD)
    r = json.loads(p.read_bytes().decode("utf-8"))

    lots = r.get("lots") or {}
    need(lots.get("snapshot") == ANCHOR_SNAPSHOT and lots.get("rows_scanned") == ANCHOR_ROWS and lots.get("cash_stem_ticker_lots") == ANCHOR_LOTS,
         "lots %r: the 2026-10-09 snapshot must read %d rows and %d cash-stem ticker lots (this seat's own read)" % (lots, ANCHOR_ROWS, ANCHOR_LOTS))
    need(is_int(lots.get("accounts")) and 1 <= lots["accounts"] <= ANCHOR_LOTS and is_int(lots.get("distinct_tickers")) and lots["distinct_tickers"] >= 1
         and is_int(lots.get("lots_with_description_cash")) and lots["lots_with_description_cash"] <= ANCHOR_LOTS and is_int(lots.get("open_lots")) and is_int(lots.get("closed_lots"))
         and lots["open_lots"] + lots["closed_lots"] <= ANCHOR_LOTS, "lots %r needs accounts, distinct_tickers, lots_with_description_cash, open_lots and closed_lots (their sum at most the lot count)" % lots)

    cr = r.get("canonical_row") or {}
    need(isinstance(cr.get("exists"), bool) and (cr["exists"] is False or (nes(cr.get("asset_class")) and "sub_asset_class" in cr)) and nes(cr.get("read_from")),
         "canonical_row %r: exists, and when true its asset_class and sub_asset_class, and where it was read" % cr)

    gc = r.get("gold_classifier") or {}
    need(isinstance(gc.get("classify"), str) and isinstance(gc.get("classify_with_identity_class"), str) and nes(gc.get("basis")), "gold_classifier %r: classify and classify_with_identity_class (an empty string is the unclassified signal) and the basis in words" % gc)

    sp = r.get("served_per_page")
    need(isinstance(sp, list) and sorted(x.get("page") for x in sp if isinstance(x, dict)) == sorted(PAGES), "served_per_page must hold exactly one entry for each of %s" % (PAGES,))
    for x in sp:
        need(x.get("established") in (True, False) and nes(x.get("store")) and nes(x.get("served_class")) and nes(x.get("read_from")) and is_int(x.get("positions_seen")),
             "served_per_page entry %r: established, store, served_class (or NOT_ESTABLISHED), read_from and positions_seen" % x)
        if x["established"] is False:
            need(x["served_class"] == "NOT_ESTABLISHED" and nes(x.get("reason")), "an entry that is not established says NOT_ESTABLISHED and a reason: %r" % x)
    ir = [x for x in sp if x["page"] == "investor_reporting"][0]
    isc = r.get("investor_reporting_special_case") or {}
    need(nes(isc.get("rule_at")) and isc.get("requires_ticker_and_description_both_cash") in (True, False) and is_int(isc.get("lots_that_meet_it")) and isc["lots_that_meet_it"] <= ANCHOR_LOTS,
         "investor_reporting_special_case %r: rule_at, requires_ticker_and_description_both_cash, lots_that_meet_it" % isc)

    need(nes(r.get("what_the_page_shows_in_words")) and nes(r.get("recommendation")), "what_the_page_shows_in_words and recommendation must be stated")
    rd = r.get("reads") or {}
    need(rd.get("dynamodb_writes") == 0 and rd.get("s3_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads %r" % rd)
    need(r.get("deployed") is False and r.get("pushed") is False and r.get("served_values_changed") is False, "deployed, pushed and served_values_changed must be false")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: %d cash-stem lots in %d accounts read; canonical row exists: %s; IR page served class %s" % (lots["cash_stem_ticker_lots"], lots["accounts"], str(cr["exists"]).lower(), ir["served_class"]))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid == "DB100-1-AC1", "unknown criterion %r" % cid)
        check(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB100"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
