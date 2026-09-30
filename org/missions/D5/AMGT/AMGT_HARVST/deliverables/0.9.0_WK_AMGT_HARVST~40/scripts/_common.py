"""Shared READ-ONLY loader for HVST-c-1 (S3 GET only; no put, no delete, no vendor call).
Reads the newest article_security_mention snapshot and the silver headlines EXACTLY as build_event does."""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

# The IN-SAMPLE securities: the one-story rule was tuned in three generations on the 8 events of these five.
IN_SAMPLE = frozenset(("BA_US_Equity", "992_HK_Equity", "COST_US_Equity", "HD_US_Equity", "NVDA_US_Equity"))
FROZEN_AT = "2026-09-29T06:26Z"  # the b-2 put; a capture dated after this is held-out by time


def load():
    client = store._default_client()
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
    headlines = pg._headline_by_article_key(client=client)
    rows = []
    for r in mention:
        r = dict(r)
        r["title"] = headlines.get(r.get("article_key"))
        rows.append(r)
    return rows, len(headlines)


def is_ab(r):
    return r.get("signal_tier") in ("A", "B")


def day(r):
    return pg._day_of(r.get("published_utc"))


def held_out(r):
    return r.get("security_key") not in IN_SAMPLE


def pop_stats(rows):
    ab = [r for r in rows if is_ab(r)]
    days = sorted(d for d in (day(r) for r in rows) if d is not None)
    return {
        "rows": len(rows),
        "ab_rows": len(ab),
        "articles": len({r.get("article_key") for r in rows}),
        "ab_articles": len({r.get("article_key") for r in ab}),
        "securities": len({r.get("security_key") for r in rows}),
        "ab_securities": len({r.get("security_key") for r in ab}),
        "range": "%s..%s" % (days[0], days[-1]) if days else "none",
    }


def fmt_stats(name, s):
    return ("%-11s rows=%d  tier-A/B rows=%d  distinct articles=%d (A/B %d)  securities=%d (with A/B rows %d)  published %s"
            % (name, s["rows"], s["ab_rows"], s["articles"], s["ab_articles"], s["securities"], s["ab_securities"], s["range"]))
