"""AMGT_RESAPP round 77 -- AMGT-ba-8: the top band's news-day rule (CTO round-76 analysis @c8bbeeac10, ruling 5).

  --crit AC1|AC2 --where local

AC1 (build): `lib.research.api.top_band.news_items_newest(rows, as_of, window_days=30)` exists and, on plant rows:
    C1 picks the name's NEWEST day with a followable article inside the window, and serves that day's items most-discussed
       first, then newest;
    C2 a name whose only news is older than the window serves items [], day None and items_reason exactly
       "No news in the last 30 days";
    C3 a name with no rows at all serves the same reason (never a band with no words);
    C4 the answer carries `window_days` 30.
AC2 (control): the round-76 plant cases in lib/research/api/tests/test_top_band_provenance.py still pass.
Verdict: R77 BA8 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import datetime
import subprocess
import sys

REASON = "No news in the last 30 days"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC2":
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "lib/research/api/tests/test_top_band_provenance.py"], capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 the existing plant cases pass", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    from lib.research.api import top_band

    fn = getattr(top_band, "news_items_newest", None)
    if not callable(fn):
        clause("C0 top_band.news_items_newest exists", False, "absent")
        return verdict(a, ok)
    as_of = datetime.date(2026, 10, 6)

    def row(days_ago, hour, key, mentions, link=True):
        when = datetime.datetime(2026, 10, 6, hour, 0, tzinfo=datetime.timezone.utc) - datetime.timedelta(days=days_ago)
        return {"article_key": key, "published_utc": when, "url": ("https://example.test/" + key) if link else "",
                "title": "Title " + key, "publisher": "ft", "mention_count": mentions, "security_key": "PLANT_US_Equity"}

    rows = [row(12, 9, "old1", 9), row(3, 8, "b", 2), row(3, 15, "c", 2), row(3, 10, "a", 5), row(2, 11, "nolink", 7, link=False)]
    got = fn(rows, as_of)
    items = got.get("items") or []
    ordered = ([i.get("mentions") for i in items] == [5, 2, 2]
               and (items[1].get("published_utc") or "") > (items[2].get("published_utc") or ""))
    clause("C1 the newest day with a followable article inside the window is chosen and ordered",
           got.get("day") == "2026-10-03" and ordered, f"day {got.get('day')} mentions {[i.get('mentions') for i in items]}")
    old = fn([row(45, 9, "x", 3)], as_of)
    clause("C2 news older than the window reads the plain reason", old.get("items") == [] and old.get("day") is None
           and old.get("items_reason") == REASON, f"{old.get('day')} {old.get('items_reason')!r}")
    none = fn([], as_of)
    clause("C3 a name with no rows reads the same reason", none.get("items") == [] and none.get("items_reason") == REASON,
           f"{none.get('items_reason')!r}")
    clause("C4 the answer carries window_days 30", got.get("window_days") == 30 and none.get("window_days") == 30,
           f"{got.get('window_days')}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R77 BA8 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
