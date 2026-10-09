"""AMGT_RESAPP round-82 PREP -- a relevance (mention) field on the header feed's items (DSGN round-58 R6 ask 2).

  python r82_feed.py --crit AC1 [--where local|deployed]

AC1: GET /security/<key>/overlay for AMD_US_Equity and BA_US_Equity -> the `feed` block:
  F1 the route answers 200 and the feed is SERVED with items (denominator printed);
  F2 every item carries `mentions`, an integer >= 0 (gold article_security_mention's own mention_count, the count the
     "In the news" card already serves through top_band);
  F3 `most_discussed_basis` no longer reads ABSENT: it names the measured basis.
Verdict: R82 FEED AC1 SERVED: YES|NO (exit 0|1). At the base (live aAkcp2l1, 2026-10-09) it reads NO.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r82_call import caller, say  # noqa: E402

KEYS = ("AMD_US_Equity", "BA_US_Equity")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    get = caller(a.where)
    r1 = r2 = r3 = True
    for key in KEYS:
        code, body = get("/security/%s/overlay" % key)
        feed = (body or {}).get("feed") or {}
        items = feed.get("items") or []
        bad = [i.get("article_key") for i in items
               if not (isinstance(i.get("mentions"), int) and not isinstance(i.get("mentions"), bool) and i["mentions"] >= 0)]
        basis = str(feed.get("most_discussed_basis") or "")
        r1 &= say(code == 200 and feed.get("coverage_status") == "SERVED" and len(items) > 0,
                  "F1 %s overlay %s, feed %s, items %d" % (key, code, feed.get("coverage_status"), len(items)))
        r2 &= say(bool(items) and not bad, "F2 %s items carrying an integer mentions: %d of %d" % (key, len(items) - len(bad), len(items)))
        r3 &= say(bool(basis) and not basis.upper().startswith("ABSENT"), "F3 %s most_discussed_basis: %r" % (key, basis[:80]))
    ok = r1 and r2 and r3
    print("R82 FEED AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
