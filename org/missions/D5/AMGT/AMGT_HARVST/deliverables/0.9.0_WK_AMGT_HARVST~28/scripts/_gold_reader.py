"""HVST-x-2 (0.9.0_WK_AMGT_HARVST~27): READ-ONLY loader helpers over LANDED gold/silver, built
for `timeline_api`'s caller contract. NO S3 WRITE, NO S3 DELETE, NO GOLD BUILD -- every function
here calls only existing read paths already exposed by `lib.research.harvest.publication_gold`
and `lib.research.harvest.store` (`_latest_gold_snapshot_rows`, `_iter_latest_articles`), never a
vendor client, never `lib.opal_data_harvest`.

Shared by all three criterion scripts in this cell so the same read happens once per process
where convenient, and so the join logic (mention gold + silver article headline/precision) is
written ONE place rather than three.
"""

import datetime

import lib.research.harvest.publication_gold as pg
import lib.research.harvest.store as store


def default_client():
    return store._default_client()


def load_daily_rows(client=None):
    """Every row of the NEWEST `chatter_daily` gold snapshot -- READ ONLY."""
    client = client or default_client()
    return pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE, client=client)


def load_event_rows(client=None):
    """Every row of the NEWEST `chatter_event` gold snapshot -- READ ONLY."""
    client = client or default_client()
    return pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)


def load_mention_rows(client=None):
    """Every row of the NEWEST `article_security_mention` gold snapshot -- READ ONLY."""
    client = client or default_client()
    return pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)


def load_article_index(client=None):
    """{article_key: silver article row} off the newest silver `article` rows across every
    publisher (`publication_gold._iter_latest_articles`) -- the only place `title` and
    `published_precision` live (the gold mention table never carries them forward)."""
    client = client or default_client()
    index = {}
    for row in pg._iter_latest_articles(client=client):
        key = row.get("article_key")
        if key is not None:
            index[key] = row
    return index


def make_daily_loader(daily_rows):
    """`daily_loader(security_key)` per `timeline_api.get_timeline`'s contract: every
    `chatter_daily` row for this security, from the full loaded snapshot."""
    by_security = {}
    for row in daily_rows:
        by_security.setdefault(row["security_key"], []).append(row)

    def _loader(security_key):
        return list(by_security.get(security_key, []))

    return _loader


def make_event_loader(event_rows):
    """`event_loader(security_key)` per `timeline_api`'s contract: every `chatter_event` row for
    this security."""
    by_security = {}
    for row in event_rows:
        by_security.setdefault(row["security_key"], []).append(row)

    def _loader(security_key):
        return list(by_security.get(security_key, []))

    return _loader


def _joined_article_row(mention_row, article_index):
    """ONE `timeline_api.ARTICLE_FIELDS`-shaped row: the mention gold row's own fields, plus
    `headline`/`published_precision` joined from the silver article row by `article_key` (the
    ONLY place either lives). Absent from the silver index (should not happen for a landed
    mention row, but never assumed) -> `headline`/`published_precision` are honestly `None`
    rather than a KeyError."""
    silver = article_index.get(mention_row.get("article_key")) or {}
    return {
        "article_key": mention_row.get("article_key"),
        "headline": silver.get("title"),
        "publisher": mention_row.get("publisher"),
        "signal_tier": mention_row.get("signal_tier"),
        "mention_count": mention_row.get("mention_count"),
        "mention_in_title": mention_row.get("mention_in_title"),
        "mention_in_lead": mention_row.get("mention_in_lead"),
        "published_utc": mention_row.get("published_utc"),
        "published_precision": silver.get("published_precision"),
    }


def _day_of_utc(published_utc):
    if published_utc is None:
        return None
    if published_utc.tzinfo is None or published_utc.tzinfo.utcoffset(published_utc) is None:
        raise ValueError("_day_of_utc: expected tz-aware published_utc, got naive %r" % (published_utc,))
    return published_utc.astimezone(datetime.timezone.utc).date()


def make_day_article_loader(mention_rows, article_index):
    """`article_loader(security_key, day)` per `timeline_api.get_timeline_day`'s contract: every
    already-joined ARTICLE_FIELDS row for that security on that UTC day, read off the mention gold
    table (never invented, never re-derived from a different join than the daily builder used --
    `_day_of` is the identical day-assignment rule `publication_gold.daily_rows` uses)."""
    by_security_day = {}
    for row in mention_rows:
        day = _day_of_utc(row.get("published_utc"))
        if day is None:
            continue
        by_security_day.setdefault((row.get("security_key"), day), []).append(row)

    def _loader(security_key, day):
        rows = by_security_day.get((security_key, day), [])
        return [_joined_article_row(r, article_index) for r in rows]

    return _loader


def make_event_article_loader(mention_rows, article_index):
    """`article_loader(security_key, event_row)` per `timeline_api.get_timeline_event`'s contract:
    every already-joined ARTICLE_FIELDS row for that event's `article_keys`, matched also on
    `security_key` (a mention row is keyed by (article, security), so the pair is the exact join,
    never article_key alone)."""
    by_security_article = {}
    for row in mention_rows:
        by_security_article.setdefault((row.get("security_key"), row.get("article_key")), row)

    def _loader(security_key, event_row):
        out = []
        for article_key in event_row.get("article_keys") or []:
            row = by_security_article.get((security_key, article_key))
            if row is not None:
                out.append(_joined_article_row(row, article_index))
        return out

    return _loader
