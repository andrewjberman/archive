"""Shared core for HVST-i-1 (copied from ~45/scripts/_common.py, paths changed; HVST-g-1 text follows)

Originally: shared core for HVST-g-1 (S3 GET/LIST only: no put, no delete, no vendor call).

OLD  = round 18's securities file, deliverables/0.9.0_WK_AMGT_HARVST~45/securities.universe.json (read only).
NEW  = deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json (HVST-i-1's own output).
Both are run through the SAME publication_gold functions at HEAD, in memory, over the same silver, so a
difference between them is the alias rule and nothing else. The SERVED newest parts are read beside them so
a row that moves is attributed ALIAS (new vs old, same silver) or DRIFT (old vs served: the silver has
grown or the range extends)."""
import datetime
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow as pa  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

DELIV = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
OLD_PATH = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~45", "securities.universe.json")
NEW_PATH = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~46", "securities.universe.json")
BRAND_PATH = os.path.join(REPO, "lib", "research", "harvest", "whole_brand_aliases.json")
SEED = 20260929

SCHEMAS = {pg.GOLD_TABLE: pg.GOLD_MENTION_SCHEMA, pg.GOLD_DAILY_TABLE: pg.GOLD_DAILY_SCHEMA,
           pg.GOLD_EVENT_TABLE: pg.GOLD_EVENT_SCHEMA}


def a(text, n=None):
    """ASCII-only rendering (offsets are computed before this is applied)."""
    s = ("" if text is None else str(text)).encode("ascii", "backslashreplace").decode("ascii")
    return s[:n] if n else s


def canon(v):
    if isinstance(v, datetime.datetime):
        return v.astimezone(datetime.timezone.utc).isoformat() if v.tzinfo else v.isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, (list, tuple)):
        return [canon(x) for x in v]
    return v


def canon_row(r):
    return {k: canon(v) for k, v in r.items()}


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def roundtrip(rows, table):
    return pa.Table.from_pylist(list(rows), schema=SCHEMAS[table]).to_pylist()


def newest_key(table, client):
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    if not keys:
        return None, 0
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1], len(keys)


def fetch(client=None):
    """(articles, listing_hits, served) -- served = {table: (newest key, parts, rows)}. S3 GET/LIST only."""
    client = client or store._default_client()
    articles = sorted(pg._iter_latest_articles(client=client), key=lambda r: r["article_key"])
    hits = list(pg._iter_all_listing_hits(client=client))
    served = {}
    for table in (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE):
        key, parts = newest_key(table, client)
        served[table] = (key, parts, pg._latest_gold_snapshot_rows(table, client=client))
    return articles, hits, served


def build_memory(securities, articles, hits, as_of):
    """{table: rows} built in memory through the producers' own functions, each row round-tripped through
    the table's arrow schema so it compares like-for-like with what parquet returns."""
    title_of = {x.get("article_key"): x.get("title") for x in articles}
    mention = []
    for art in articles:
        mention.extend(pg.mention_rows(art, securities))
    mention_rt = roundtrip(mention, pg.GOLD_TABLE)
    coverage = pg.publisher_coverage(hits, securities)
    daily = pg.daily_rows(mention_rt, securities, start=pg.BACKFILL_FLOOR, end=as_of, coverage=coverage)
    enriched = []
    for r in mention_rt:
        r = dict(r)
        r["title"] = title_of.get(r.get("article_key"))
        enriched.append(r)
    event = pg.event_rows(enriched)
    return {pg.GOLD_TABLE: mention_rt, pg.GOLD_DAILY_TABLE: roundtrip(daily, pg.GOLD_DAILY_TABLE),
            pg.GOLD_EVENT_TABLE: roundtrip(event, pg.GOLD_EVENT_TABLE)}, enriched


def diff_fields(x, y):
    """Sorted field names that differ between two rows (None = absent row)."""
    if x is None or y is None:
        return None
    return sorted(k for k in set(x) | set(y) if canon(x.get(k)) != canon(y.get(k)))


def spans_with_forms(text, aliases, exact):
    """[(start, end, matched text, form label, kind)] for ONE text under the matcher's own pattern
    (`publication_gold._span_pattern`); kind is 'ticker' when the exact-case alternative won the span."""
    pat = pg._span_pattern(aliases, exact)
    if pat is None or not text:
        return []
    ordered = sorted([(x, re.compile(re.escape(x), re.I), "alias") for x in aliases if x]
                     + [(x, re.compile(re.escape(x)), "ticker") for x in exact if x],
                     key=lambda p: len(p[0]), reverse=True)
    out = []
    for m in pat.finditer(text):
        label, _rx, kind = next(o for o in ordered if o[1].fullmatch(m.group(0)))
        out.append((m.start(), m.end(), m.group(0), label, kind))
    return out


def texts_of(article):
    """[(where, text)] exactly as the matcher reads them: the title, then each block."""
    out = [("title", article.get("title") or "")]
    for i, block in enumerate(article.get("text_blocks") or []):
        out.append(("block %d" % i, block or ""))
    return out


def brand_forms_by_security():
    """{security_key: {casefolded brand}} of the shipped whole-brand list (to name a span's class)."""
    out = {}
    for e in load_json(BRAND_PATH)["whole_brands"]:
        out.setdefault(e["security_key"], set()).add(e["brand"].casefold())
    return out


def added_spans(article, old_sec, new_sec, brands):
    """(added, lost) span lists for one (article, security): a span the NEW alias set finds that the OLD did
    not (with its form class), and a span the OLD found that the NEW does not (should be none)."""
    old_al = pg._security_aliases(old_sec)
    old_ex = pg._security_exact_aliases(old_sec)
    new_al = pg._security_aliases(new_sec)
    new_ex = pg._security_exact_aliases(new_sec)
    added, lost = [], []
    for idx, (where, text) in enumerate(texts_of(article)):
        o = spans_with_forms(text, old_al, old_ex)
        n = spans_with_forms(text, new_al, new_ex)
        oset = {(s, e) for s, e, *_ in o}
        nset = {(s, e) for s, e, *_ in n}
        for s, e, m, label, kind in n:
            if (s, e) not in oset:
                if kind == "ticker":
                    cls = "ticker"
                elif label.casefold() in brands.get(new_sec["security_key"], set()):
                    cls = "whole_brand"
                else:
                    cls = "alias"
                added.append({"where": where, "block": idx - 1 if idx else None, "offset": s, "end": e, "matched": m,
                              "form": label, "class": cls, "text": text})
        for s, e, m, label, kind in o:
            if (s, e) not in nset:
                lost.append({"where": where, "offset": s, "matched": m, "form": label})
    return added, lost


def context(text, s, e, w=70):
    lo, hi = max(0, s - w), min(len(text), e + w)
    return a(("..." if lo else "") + text[lo:s] + "[[" + text[s:e] + "]]" + text[e:hi] + ("..." if hi < len(text) else ""))


def sec_map(securities):
    return {s["security_key"]: s for s in securities}
