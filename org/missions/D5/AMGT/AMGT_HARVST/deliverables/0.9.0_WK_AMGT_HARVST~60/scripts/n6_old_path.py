"""HVST-n-6: the OLD /timeline/day loaders, copied VERBATIM from
lib/research/api/scoped_amgt.py @d357a9e247 (the round-24 issuance HEAD) lines 4203-4259, plus the
two publication_gold/store readers they call, so the OLD path stays runnable after the fix lands.
Nothing here is imported by production code."""
import io

import pyarrow.parquet as pq

from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
from lib.research.harvest import publication_gold
from lib.research.harvest import store
from lib.research.harvest import timeline_api

_DATE_PARTITION_RE = publication_gold._DATE_PARTITION_RE


def old_latest_gold_snapshot_rows(table, client=None):
    """publication_gold._latest_gold_snapshot_rows @d357a9e247, verbatim."""
    client = client or store._default_client()
    prefix = store.table_prefix("amgt", "gold", table)
    paginator = client.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    if not keys:
        return []
    newest_key = sorted(keys, key=lambda k: (_DATE_PARTITION_RE.search(k).group(1), k))[-1]
    resp = client.get_object(Bucket=store.HARVEST_BUCKET, Key=newest_key)
    raw = resp["Body"].read() if hasattr(resp["Body"], "read") else resp["Body"]
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def old_iter_latest_articles(client=None):
    """publication_gold._iter_latest_articles @d357a9e247, verbatim (store.silver_latest is unchanged)."""
    for _publisher_code, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        latest = store.silver_latest(source, "article", ("article_key",), client=client)
        for row in latest.values():
            yield row


def _timeline_snapshot_rows(table):
    from lib.research.harvest import timeline_api as _t

    try:
        return old_latest_gold_snapshot_rows(table)
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, TimeoutError) or "timeout" in type(exc).__name__.lower():
            raise _t.UpstreamTimeout("{0} read timed out: {1}".format(table, exc)) from exc
        raise


def _timeline_daily_loader(security_key):
    return [r for r in _timeline_snapshot_rows("chatter_daily") if r.get("security_key") == security_key]


def _timeline_silver_articles(article_keys):
    wanted = set(article_keys)
    return {
        row.get("article_key"): row
        for row in old_iter_latest_articles()
        if row.get("article_key") in wanted
    }


def _timeline_article_loader(security_key, day):
    mine = [
        r
        for r in _timeline_snapshot_rows("article_security_mention")
        if r.get("security_key") == security_key
        and r.get("published_utc") is not None
        and publication_gold._day_of(r["published_utc"]) == day
    ]
    if not mine:
        return []
    silver = _timeline_silver_articles([r.get("article_key") for r in mine])
    joined = []
    for row in mine:
        article = silver.get(row.get("article_key")) or {}
        merged = dict(row)
        merged["headline"] = article.get("title")
        merged["published_precision"] = article.get("published_precision")
        joined.append(merged)
    return joined


def get_day(security_key, day_iso):
    return timeline_api.get_timeline_day(security_key, day_iso, _timeline_daily_loader, _timeline_article_loader)
