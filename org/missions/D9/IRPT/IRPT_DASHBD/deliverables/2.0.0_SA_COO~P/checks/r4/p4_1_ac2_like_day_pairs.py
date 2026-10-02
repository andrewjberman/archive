"""DB4-1-AC2 -- the tie-out grades agreement only on like day sets (PRD v0.6 ruling 23): each pair is one of Opal's GAP-FREE
segments, and like_days and abs_diff are what they say.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.json:
  {"pairs": [{"account", "bd_account", "start", "end", "opal_linked_days", "bd_days_held", "like_days", "opal_twr", "bd_twr",
              "abs_diff"}], "like_day_pairs": n, "summary": {...}}
Grades: at least one pair; for each pair, opal_linked_days equals the number of trading days in [start, end] by
lib/trading_calendar.trading_days_between (so the segment is gap-free); like_days == (opal_linked_days == bd_days_held); for a
like-day pair, abs_diff == |opal_twr - bd_twr| within 1e-12 and both returns are numbers; like_day_pairs equals the count of
like-day pairs. Usage: python <this file> <repo_root>
"""
import datetime as dt
import json
import sys
from pathlib import Path

T = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.json"


def fail(msg):
    print("FAIL: " + msg)
    print("DB4-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc
    t = root / T
    if not t.is_file():
        fail("no tie-out record TIEOUT_49F_BLACKDIAMOND_R4.json")
    tie = json.loads(t.read_text(encoding="utf-8"))
    pairs = tie.get("pairs") or []
    if not pairs:
        fail("no pair")
    like = 0
    for x in pairs:
        s, e = dt.date.fromisoformat(x["start"]), dt.date.fromisoformat(x["end"])
        n = len(list(tc.trading_days_between(s, e)))
        if int(x.get("opal_linked_days", -1)) != n:
            fail("%s %s..%s: opal_linked_days %r is not the %d trading days of the segment (not gap-free)"
                 % (x.get("account"), x["start"], x["end"], x.get("opal_linked_days"), n))
        want = int(x["opal_linked_days"]) == int(x.get("bd_days_held", -1))
        if bool(x.get("like_days")) != want:
            fail("%s %s..%s: like_days %r but linked %s vs held %s"
                 % (x.get("account"), x["start"], x["end"], x.get("like_days"), x["opal_linked_days"], x.get("bd_days_held")))
        if want:
            like += 1
            o, b = float(x["opal_twr"]), float(x["bd_twr"])
            if abs(abs(o - b) - float(x["abs_diff"])) > 1e-12:
                fail("%s %s..%s: abs_diff is not |opal_twr - bd_twr|" % (x.get("account"), x["start"], x["end"]))
    if int(tie.get("like_day_pairs", -1)) != like:
        fail("like_day_pairs %r against %d counted" % (tie.get("like_day_pairs"), like))
    print("OK: %d pair(s), every one gap-free by the trading calendar; %d like-day pair(s) graded" % (len(pairs), like))
    print("DB4-1-AC2 PASS")


if __name__ == "__main__":
    main()
