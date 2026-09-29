"""Shared loader for HVST-e-1 (S3 GET/LIST only: no put, no delete, no vendor call).

The OLD matcher is `publication_gold.py` AT THE CLOUD BASE, read with `git show <BASE>:<path>` and executed
as a throw-away module, so 'old' is the pre-change code itself and never a re-implementation of it. The NEW
matcher is the worktree's `lib.research.harvest.publication_gold`. Everything else (securities, silver) is the
same input for both."""
import copy
import datetime
import json
import os
import subprocess
import sys
import types

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow as pa  # noqa: E402

from lib.research.harvest import publication_gold as NEW  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BASE = "b8c8214ce5"  # the round-16 issuance commit this worktree was cut from (matcher unchanged at it)
MODULE_PATH = "lib/research/harvest/publication_gold.py"
SECURITIES = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                          "0.9.0_WK_AMGT_HARVST~41", "securities.universe.json")
TABLES = (NEW.GOLD_TABLE, NEW.GOLD_DAILY_TABLE, NEW.GOLD_EVENT_TABLE)
SCHEMAS = {NEW.GOLD_TABLE: NEW.GOLD_MENTION_SCHEMA, NEW.GOLD_DAILY_TABLE: NEW.GOLD_DAILY_SCHEMA,
           NEW.GOLD_EVENT_TABLE: NEW.GOLD_EVENT_SCHEMA}
KEYS = {NEW.GOLD_TABLE: lambda r: (r["article_key"], r["security_key"]),
        NEW.GOLD_DAILY_TABLE: lambda r: (r["security_key"], r["day"]),
        NEW.GOLD_EVENT_TABLE: lambda r: (r["event_id"],)}


def load_old_module():
    src = subprocess.run(["git", "show", "%s:%s" % (BASE, MODULE_PATH)], cwd=REPO, check=True,
                         capture_output=True).stdout.decode("utf-8")
    mod = types.ModuleType("publication_gold_BASE")
    mod.__file__ = "git:%s:%s" % (BASE, MODULE_PATH)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def a(text, n=None):
    s = ("" if text is None else str(text)).encode("ascii", "replace").decode("ascii")
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


def load_securities():
    with open(SECURITIES, "r", encoding="utf-8") as fh:
        return json.load(fh)


def roundtrip(rows, table):
    return pa.Table.from_pylist(list(rows), schema=SCHEMAS[table]).to_pylist()


def diff_fields(x, y):
    return sorted(k for k in set(x) | set(y) if canon(x.get(k)) != canon(y.get(k)))


def parts(table, client):
    """[(key, ETag, size)] of every parquet part, sorted the way readers sort (date, key)."""
    prefix = store.table_prefix("amgt", "gold", table)
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                out.append((obj["Key"], obj["ETag"].strip('"'), obj["Size"]))
    return sorted(out, key=lambda p: (NEW._DATE_PARTITION_RE.search(p[0]).group(1), p[0]))


def short(key):
    return key.split("/gold/", 1)[-1].split("/", 1)[-1]


def read_inputs(client):
    """(articles, title_of, listing_hits) -- the landed silver, read once."""
    articles = list(NEW._iter_latest_articles(client=client))
    title_of = {x.get("article_key"): x.get("title") for x in articles}
    hits = list(NEW._iter_all_listing_hits(client=client))
    return articles, title_of, hits


def memory(mod, securities, articles, title_of, hits, as_of):
    """{table: rows} built IN MEMORY through module `mod`'s own functions (the same calls build_mention /
    build_daily / build_event make), every table round-tripped through its arrow schema."""
    mention = []
    for art in copy.deepcopy(articles):
        mention.extend(mod.mention_rows(art, securities))
    mention_rt = roundtrip(mention, NEW.GOLD_TABLE)
    coverage = mod.publisher_coverage(hits, securities)
    daily = mod.daily_rows(mention_rt, securities, start=mod.BACKFILL_FLOOR, end=as_of, coverage=coverage)
    enriched = []
    for r in mention_rt:
        r = dict(r)
        r["title"] = title_of.get(r.get("article_key"))
        enriched.append(r)
    event = mod.event_rows(enriched)
    return {NEW.GOLD_TABLE: mention_rt, NEW.GOLD_DAILY_TABLE: roundtrip(daily, NEW.GOLD_DAILY_TABLE),
            NEW.GOLD_EVENT_TABLE: roundtrip(event, NEW.GOLD_EVENT_TABLE)}
