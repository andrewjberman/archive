"""HVST-ab-2 AC2 (issuer check, read-only): the 11 bbg story-id articles are SERVED with their mention pairs, the 11
hash-keyed empty rows stay INERT, and the company query for Lenovo returns them.

PASS requires:
- the newest served snapshot (read the way the timeline route reads it) equals the signed expected rows;
- `mention_count` is an integer >= 1 on every served row;
- every one of the 11 story ids has >= 1 served pair (FWD-2);
- 0 served pairs on an empty bbg row (CTO ruling @803ea38a9e);
- the timeline DAY route's own handler (`scoped_amgt._serve_timeline`, in-process at the checked-out code, reading the
  served S3 gold and silver) lists every 992_HK story-id pair whose day is on or after the page floor
  (`publication_gold.BACKFILL_FLOOR`, where `chatter_daily` rows begin), with a non-empty headline. A pair published
  before the floor is served in gold but has no day on the page by design; it is counted and named, not required.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab2_common as c  # noqa: E402

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402

LENOVO = "992_HK_Equity"


def pair_day(r):
    """The route's own day rule (`_timeline_article_loader`: `publication_gold._day_of(published_utc)`)."""
    return pg._day_of(r["published_utc"]).isoformat() if r.get("published_utc") is not None else "None"


def day_listing(day):
    resp = scoped_amgt._serve_timeline(LENOVO, day, {})
    body = resp.get("body")
    body = json.loads(body) if isinstance(body, str) else (body or {})
    return resp.get("statusCode"), body


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "ab2_before.json"))
    served = c.served_rows()
    got = c.norm_rows(served)
    if got != before["expected_rows"]:
        failures.append("served snapshot != signed expected rows (%d vs %d)" % (len(got), len(before["expected_rows"])))
    bad = [r for r in served if not isinstance(r.get("mention_count"), int) or r.get("mention_count") < 1]
    print("served rows: %d; mention_count missing or < 1: %d" % (len(served), len(bad)))
    if bad:
        failures.append("%d served row(s) lack a mention_count >= 1" % len(bad))
    by_key = collections.defaultdict(list)
    for r in served:
        by_key[r.get("article_key")].append(r)
    lacking = [s for s in c.STORY_IDS if not by_key.get(s)]
    print("story ids served with >= 1 pair: %d of %d" % (len(c.STORY_IDS) - len(lacking), len(c.STORY_IDS)))
    if lacking:
        failures.append("%d story id(s) have no served pair (first %s)" % (len(lacking), lacking[0]))
    empty = set(c.empty_bbg_keys())
    reach = [r for r in served if r.get("article_key") in empty]
    print("INERT: empty bbg rows %d; served pairs on them %d" % (len(empty), len(reach)))
    if reach:
        failures.append("STOP: %d served pair(s) on an empty bbg row" % len(reach))
    lenovo_all = [r for s in c.STORY_IDS for r in by_key.get(s, []) if r.get("security_key") == LENOVO]
    floor = pg.BACKFILL_FLOOR.isoformat()
    pre = [r for r in lenovo_all if pair_day(r) < floor]
    lenovo = [r for r in lenovo_all if pair_day(r) >= floor]
    print("992_HK story-id pairs: %d; before the page floor %s: %d (%s); on or after it: %d"
          % (len(lenovo_all), floor, len(pre), sorted(pair_day(r) for r in pre), len(lenovo)))
    days = sorted({pair_day(r) for r in lenovo})
    listed = 0
    for day in days:
        status, body = day_listing(day)
        arts = body.get("articles") or []
        keys = {a.get("article_key"): a for a in arts}
        want = [r.get("article_key") for r in lenovo if pair_day(r) == day]
        for k in want:
            a = keys.get(k)
            ok = status == 200 and a is not None and bool((a.get("headline") or a.get("title") or "").strip())
            listed += ok
            if not ok:
                failures.append("the day route for %s does not list %s with a headline (status %s)" % (day, k, status))
        print("  %s: route status %s, articles %d, story-id pairs listed %d of %d"
              % (day, status, len(arts), sum(1 for k in want if k in keys), len(want)))
    print("company query (day route) lists %d of %d 992_HK story-id pairs" % (listed, len(lenovo)))
    if not lenovo:
        failures.append("no 992_HK story-id pair on or after the page floor is served")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
