"""IRPT_BCKEND round 127 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one read-only DIRECT-ACT order:
  IB127-1  IB-pr-429  the per account-day date-basis claim the CTO ruled (msg 4825), counted: how many account-days read
                      OWN_DATE, PRIOR_CLOSE or NOT_GRADED, and the share of account-days the serving rule blanks.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB127-1-AC1  every account-day present is given exactly one claim, and NOT_GRADED is split by its reason with no
               remainder. Base: FAIL (no file).
  IB127-1-AC2  the serving rule is counted on the account-days that could carry a return (a prior trading-day partition
               exists for that account): served + blank == eligible, the blanks are split by reason with no remainder,
               and the share is stated. Base: FAIL (no file).
  IB127-1-AC3  the daily needs of the instrument are listed, and the control reads as planted with no account id in the
               outputs. Base: FAIL (no file).
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~288/"
OUT = D + "IB127-1_account_day_claims.json"
READ = D + "IB127-1_ACCOUNT_DAY_CLAIMS_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB127"))
        sys.exit(1)

    def ints(d, keys, where):
        if not all(isinstance(d.get(k), int) and d[k] >= 0 for k in keys):
            fail("%s %r" % (where, {k: d.get(k) for k in keys}))

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)

    if cid == "IB127-1-AC1":
        c = a.get("account_days") or {}
        ints(c, ("present", "OWN_DATE", "PRIOR_CLOSE", "NOT_GRADED"), "account_days")
        if c["OWN_DATE"] + c["PRIOR_CLOSE"] + c["NOT_GRADED"] != c["present"] or c["present"] <= 0:
            fail("claims sum to %d, %d account-days present" % (c["OWN_DATE"] + c["PRIOR_CLOSE"] + c["NOT_GRADED"], c["present"]))
        ng = a.get("not_graded_by_reason") or {}
        if not ng or not all(isinstance(v, int) for v in ng.values()) or sum(ng.values()) != c["NOT_GRADED"]:
            fail("not_graded_by_reason %r does not sum to %d" % (ng, c["NOT_GRADED"]))
        if not isinstance(a.get("days"), int) or a["days"] < 80 or not isinstance(a.get("accounts"), int):
            fail("days %r accounts %r" % (a.get("days"), a.get("accounts")))
        if not a.get("claim_rule"):
            fail("no claim_rule stating how an account-day with both own and prior rows is claimed")
        print("OK: %d account-days over %d days and %d accounts, one claim each: OWN_DATE %d, PRIOR_CLOSE %d, NOT_GRADED %d %s" % (
            c["present"], a["days"], a["accounts"], c["OWN_DATE"], c["PRIOR_CLOSE"], c["NOT_GRADED"], ng))
    elif cid == "IB127-1-AC2":
        s = a.get("serving_rule") or {}
        ints(s, ("eligible", "served", "blank"), "serving_rule")
        if s["served"] + s["blank"] != s["eligible"] or s["eligible"] <= 0:
            fail("served %d + blank %d != eligible %d" % (s["served"], s["blank"], s["eligible"]))
        br = s.get("blank_by_reason") or {}
        if not br or not all(isinstance(v, int) for v in br.values()) or sum(br.values()) != s["blank"]:
            fail("blank_by_reason %r does not sum to %d" % (br, s["blank"]))
        share = s.get("blank_share_percent")
        if not isinstance(share, (int, float)) or abs(share - 100.0 * s["blank"] / s["eligible"]) > 0.06:
            fail("blank_share_percent %r does not equal blank / eligible" % share)
        acc = s.get("accounts") or {}
        ints(acc, ("with_eligible_days", "never_served", "always_served", "sometimes_served"), "serving_rule.accounts")
        if acc["never_served"] + acc["always_served"] + acc["sometimes_served"] != acc["with_eligible_days"]:
            fail("serving_rule.accounts classes do not sum")
        print("OK: %d eligible account-days: %d served, %d blank (%.1f%%) %s; accounts never served %d of %d" % (
            s["eligible"], s["served"], s["blank"], share, br, acc["never_served"], acc["with_eligible_days"]))
    elif cid == "IB127-1-AC3":
        needs = a.get("instrument_daily_needs") or []
        if len(needs) < 2 or not all(n.get("need") and n.get("where_from") and n.get("by_when") for n in needs):
            fail("instrument_daily_needs %r" % needs)
        c = a.get("control") or {}
        if c.get("planted") is None or c.get("read") != c.get("planted") or not c.get("planted"):
            fail("control %r" % c)
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        for name, body in ((OUT, text), (READ, rd.read_text(encoding="utf-8"))):
            m = ACCOUNT_ID.search(body)
            if m:
                fail("%s carries an account id shaped token at offset %d" % (name, m.start()))
        print("OK: %d daily needs listed; the control reads as planted; 0 account-id tokens in the 2 outputs" % len(needs))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
