"""Shared READ-ONLY helpers for HVST-f-2 (S3 GET only; no put, no delete, no vendor call)."""
import contextlib
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402,F401  (used as c.store by the ac scripts)


@contextlib.contextmanager
def old_rule():
    """The name-detection rule BEFORE HVST-f-2: no alias bound (headline frequency alone)."""
    saved = pg._alias_stems
    pg._alias_stems = lambda rows: None
    try:
        yield
    finally:
        pg._alias_stems = saved


def name_stems(rows, bounded):
    """The stems `_security_stories` strips for ONE security's tier A/B rows, old (bounded=False) or new."""
    ordered = sorted(rows, key=pg._event_sort_key)
    tier_a = [r for r in ordered if r.get("signal_tier") == "A"]
    pairs = [(pg._story_tokens(r.get("title")), pg._day_of(r.get("published_utc"))) for r in tier_a]
    names = pg._security_name_tokens(pairs, pg._alias_stems(ordered) if bounded else None)
    return None if names is None else sorted(names)


def show_events(events):
    if not events:
        print("    (0 events)")
    for e in events:
        print("    %s %s..%s articles=%d (A=%d B=%d) days=%d publishers=%d lead=%s | %s"
              % (e["security_key"], e["first_day"], e["last_day"], e["articles_total"], e["tier_a"], e["tier_b"],
                 e["days_span"], e["publishers_distinct"], e["lead_article_key"], e["lead_headline"]))
        print("      members: %s" % list(e["article_keys"]))
