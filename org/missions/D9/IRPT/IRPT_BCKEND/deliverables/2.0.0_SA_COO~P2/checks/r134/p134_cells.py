"""IRPT_BCKEND round 134 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB134-1  IB-pr-436  nine mutual funds by 85 days: an independent daily NAV for each, and per fund how many days the
                      custodian's mark equals the NAV of the day, of the prior trading day, of both, or of neither (CTO msg 5157).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB134-1-AC1  exactly the nine funds, each with its fund-days split with no remainder into: equals the day's NAV only, equals
               the prior day's NAV only, equals both (the NAV did not move), equals neither, no NAV found.
  IB134-1-AC2  the NAV source is stated (which reader, unadjusted, the window, the days found per fund), and the control holds:
               for a security the anchor DOES carry, the same reader's close equals the anchor's close on the days compared.
  IB134-1-AC3  the account-day effect is counted with no remainder, and no account id is in the outputs.
The counts are UNMEASURED by the issuer; the checks grade sums, the fund set and the control.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~294/"
OUT = D + "IB134-1_fund_nav_basis.json"
READ = D + "IB134-1_FUND_NAV_BASIS_READ.md"
FUNDS = ("FLCOX", "MFEIX", "CEMIX", "FSGGX", "FSMAX", "FXNAX", "FSPGX", "CDSIX", "FPNIX")
PARTS = ("equals_day_nav_only", "equals_prior_day_nav_only", "equals_both_nav_unchanged", "equals_neither", "no_nav_found")
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB134"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    funds = a.get("funds")
    if cid == "IB134-1-AC1":
        if not isinstance(funds, list) or sorted(x.get("ticker") for x in funds) != sorted(FUNDS):
            fail("funds must be exactly %s" % (FUNDS,))
        tot = dict.fromkeys(PARTS, 0)
        for x in funds:
            if any(not isinstance(x.get(k), int) for k in PARTS + ("fund_days_with_a_mark", "fund_days_with_more_than_one_mark")):
                fail("%s lacks an integer count" % x["ticker"])
            if sum(x[k] for k in PARTS) != x["fund_days_with_a_mark"]:
                fail("%s: the five outcomes sum to %d, fund-days with a mark is %d" % (x["ticker"], sum(x[k] for k in PARTS), x["fund_days_with_a_mark"]))
            for k in PARTS:
                tot[k] += x[k]
        if a.get("totals") != tot:
            fail("totals %r is not the funds' sum %r" % (a.get("totals"), tot))
        if not a.get("many_marks_rule") or not a.get("tolerance"):
            fail("many_marks_rule and tolerance are not stated")
        print("OK: 9 of 9 funds; fund-days: %s" % tot)
    elif cid == "IB134-1-AC2":
        s = a.get("nav_source") or {}
        if not s.get("name") or not s.get("read_by") or s.get("adjusted") is not False or not s.get("first_date") or not s.get("last_date"):
            fail("nav_source needs name, read_by, adjusted false, first_date and last_date")
        if not isinstance(funds, list) or any(not isinstance(x.get("nav_days_found"), int) or not isinstance(x.get("nav_days_needed"), int) for x in funds):
            fail("each fund needs nav_days_needed and nav_days_found")
        c = a.get("control") or {}
        if not c.get("security") or not isinstance(c.get("days_compared"), int) or c["days_compared"] < 20 \
                or not isinstance(c.get("days_equal"), int) or c.get("carried_by_anchor") is not True:
            fail("control needs a security the anchor carries, with at least 20 days compared and the days equal")
        if c["days_equal"] < 0.9 * c["days_compared"] and not c.get("difference_explained"):
            fail("the control reads %d of %d equal and no explanation is given" % (c["days_equal"], c["days_compared"]))
        if "is_fund_close_the_nav_of_that_day" not in a:
            fail("is_fund_close_the_nav_of_that_day is not answered (with its claim)")
        print("OK: source %s; %d of %d NAV days found over the nine; control %s equal on %d of %d days" % (
            s["name"], sum(x["nav_days_found"] for x in funds), sum(x["nav_days_needed"] for x in funds),
            c["security"], c["days_equal"], c["days_compared"]))
    elif cid == "IB134-1-AC3":
        e = a.get("account_day_effect") or {}
        keys = ("account_days_whose_only_outside_anchor_rows_are_these_funds", "every_mark_equals_day_nav_or_both",
                "one_or_more_equals_prior_day_only", "one_or_more_neither_or_no_nav")
        if any(not isinstance(e.get(k), int) for k in keys) or e[keys[1]] + e[keys[2]] + e[keys[3]] != e[keys[0]]:
            fail("account_day_effect does not split with no remainder")
        if not isinstance(e.get("of_those_holding_no_other_ungradeable_kind"), int) or a.get("claims_regraded") is not False:
            fail("of_those_holding_no_other_ungradeable_kind must be stated and claims_regraded must be false")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: %d account-days hold only these funds outside the anchor: %d on the day's NAV, %d with a prior-day mark, %d with neither or no NAV" % (
            e[keys[0]], e[keys[1]], e[keys[2]], e[keys[3]]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
