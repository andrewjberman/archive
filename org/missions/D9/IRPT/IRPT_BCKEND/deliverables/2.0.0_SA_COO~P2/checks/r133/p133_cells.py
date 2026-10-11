"""IRPT_BCKEND round 133 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB133-1  IB-pr-435  the securities behind OUTSIDE_ANCHOR ranked by the account-days they carry; the cash rule the CTO ruled
                      counted; and whether a price store the estate already holds carries each security's close (CTO msg 5082).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB133-1-AC1  the ranking is whole and adds up: one entry per security, sorted, and the counts of securities that cover half and
               ninety percent of the carried account-days are the ones the list itself gives.
  IB133-1-AC2  the cash rule is counted with no remainder, and the claims re-stated under it sum to the account-days present.
  IB133-1-AC3  every one of the six declared price stores is accounted for (opened or the reason it was not), each security is in
               exactly one coverage class, the control reads as planted, and no account id is in the outputs.
The counts are UNMEASURED by the issuer. Two figures of the re-count (34,437 account-days holding an outside-anchor row; 19,809
cash-flagged account-days) bind only when the record says the same account-days were read.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~293/"
OUT = D + "IB133-1_outside_anchor_coverage.json"
READ = D + "IB133-1_OUTSIDE_ANCHOR_COVERAGE_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
STORES = ("silver-canonical-prices", "gold-canonical-holdings", "rivalfunds-etfs-gold-security-market",
          "etfs-bbg-testpull-ticker-history", "etfs-bbg-fund-daily", "portal-canon-return-daily-values")
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
COVER = ("every_needed_day", "some_needed_days", "no_needed_day")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB133"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB133-1-AC1":
        r = a.get("ranking") or {}
        rows = r.get("securities")
        if not isinstance(rows, list) or not rows:
            fail("ranking.securities is empty")
        counts = [x.get("account_days_carried") for x in rows]
        if any(not isinstance(c, int) or c < 1 for c in counts) or counts != sorted(counts, reverse=True):
            fail("account_days_carried must be positive integers sorted from the largest")
        if len({x.get("security") for x in rows}) != len(rows):
            fail("a security appears twice in the ranking")
        total = sum(counts)
        if r.get("security_account_days_total") != total or r.get("securities") is None or r.get("securities_count") != len(rows):
            fail("the stated total %r or count %r is not the list's (%d, %d)" % (r.get("security_account_days_total"), r.get("securities_count"), total, len(rows)))

        def cover(share):
            run = 0
            for i, c in enumerate(counts, 1):
                run += c
                if run >= share * total:
                    return i
        if r.get("securities_covering_half") != cover(0.5) or r.get("securities_covering_ninety_percent") != cover(0.9):
            fail("half and ninety percent are covered by %d and %d securities, the record says %r and %r" % (
                cover(0.5), cover(0.9), r.get("securities_covering_half"), r.get("securities_covering_ninety_percent")))
        if a.get("same_account_days_read") is True and r.get("account_days_holding_an_outside_anchor_row") != 34437:
            fail("the same account-days are said to be read, yet %r of them hold an outside-anchor row, not 34437" % r.get("account_days_holding_an_outside_anchor_row"))
        if a.get("same_account_days_read") is not True and not a.get("source_difference_explained"):
            fail("different account-days were read and the record does not say why")
        print("OK: %d securities carry %d security-account-days; %d cover half, %d cover ninety percent" % (len(rows), total, cover(0.5), cover(0.9)))
    elif cid == "IB133-1-AC2":
        c = a.get("cash_rule") or {}
        keys = ("account_days_examined", "price_equal_both_days_stays_cash", "price_differs_becomes_OUTSIDE_ANCHOR", "not_comparable")
        if any(not isinstance(c.get(k), int) for k in keys):
            fail("cash_rule needs %s as integers" % (keys,))
        if c[keys[1]] + c[keys[2]] + c[keys[3]] != c[keys[0]]:
            fail("the three outcomes sum to %d, examined is %d" % (c[keys[1]] + c[keys[2]] + c[keys[3]], c[keys[0]]))
        if a.get("same_account_days_read") is True and c[keys[0]] != 19809:
            fail("the same account-days are said to be read, yet %d were examined, not 19809" % c[keys[0]])
        if c[keys[3]] and not c.get("not_comparable_treated_as"):
            fail("%d not-comparable account-day(s) and no stated treatment" % c[keys[3]])
        ad = a.get("account_days_under_the_cash_rule") or {}
        if any(not isinstance(ad.get(k), int) for k in CLAIMS + ("present",)) or sum(ad[k] for k in CLAIMS) != ad["present"]:
            fail("account_days_under_the_cash_rule does not sum to present")
        s = a.get("serving_rule_under_the_cash_rule") or {}
        if any(not isinstance(s.get(k), int) for k in ("eligible", "served", "blank")) or s["served"] + s["blank"] != s["eligible"] \
                or not isinstance(s.get("blank_share_percent"), (int, float)) or not isinstance(s.get("accounts_never_served"), int):
            fail("serving_rule_under_the_cash_rule is incomplete or does not add up")
        if not isinstance(a.get("sixth_reason"), dict) or not isinstance(a["sixth_reason"].get("rows"), int):
            fail("sixth_reason.rows is not stated")
        print("OK: %d cash-flagged account-days: %d stay cash, %d become OUTSIDE_ANCHOR, %d not comparable; blank %.1f%% of %d" % (
            c[keys[0]], c[keys[1]], c[keys[2]], c[keys[3]], s["blank_share_percent"], s["eligible"]))
    elif cid == "IB133-1-AC3":
        st = a.get("stores")
        if not isinstance(st, list):
            fail("stores is not a list")
        ids = [x.get("id", "") for x in st]
        for want in STORES:
            hit = [x for x in st if x.get("id", "").endswith(want)]
            if len(hit) != 1:
                fail("store %s is accounted for %d time(s)" % (want, len(hit)))
            x = hit[0]
            if x.get("opened") is True:
                if any(k not in x for k in ("first_date", "last_date", "price_kind", "security_days_needed", "security_days_found")):
                    fail("opened store %s lacks its window, price_kind or its needed and found counts" % want)
            elif not x.get("not_opened_reason"):
                fail("store %s was not opened and no reason is given" % want)
        cov = a.get("coverage_by_security") or {}
        rows = (a.get("ranking") or {}).get("securities") or []
        if sorted(cov) != sorted(COVER) or sum(cov.values()) != len(rows):
            fail("coverage classes %r sum to %r, the ranking has %d securities" % (sorted(cov), sum(cov.values()) if cov else None, len(rows)))
        if any(x.get("coverage") not in COVER or "best_store" not in x for x in rows):
            fail("a ranked security lacks its coverage class or best_store")
        ctl = a.get("control") or {}
        if not ctl.get("planted") or ctl.get("planted") != ctl.get("read"):
            fail("the control does not read as planted")
        r = root / READ
        if not r.is_file():
            fail("no %s" % READ)
        hits = len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8"))) + len(ACCOUNT_ID.findall(r.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)
        print("OK: %d stores accounted for (%d ids); coverage %s; control as planted; 0 account-id tokens" % (len(STORES), len(ids), cov))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
