"""HVST-l-1 AC2 -- event_rows under the NEW guard (co_mention_count >= 4 only, as in this worktree's publication_gold)
equals event_rows under the k-1 guard ROW BY ROW, every field, over today's inputs; plus the flag/count mismatch count.
The k-1 guard is obtained by MONKEYPATCHING publication_gold._is_guarded to the old expression
(is_roundup OR co_mention_count >= EVENT_GUARD_CO_MENTIONS) in the same process. S3 LIST/GET only via the producer's
readers (through the j-2 helpers, imported READ ONLY). NO put/delete, no file written."""
import importlib.util
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 8))
sys.path.insert(0, REPO)
import pyarrow as pa  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
J2 = os.path.join(HERE, "..", "..", "0.9.0_WK_AMGT_HARVST~48", "scripts", "j2_ac1_story_span_census.py")
_spec = importlib.util.spec_from_file_location("j2", J2)
j2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(j2)


def old_guard(row):
    return bool(row.get("is_roundup")) or (row.get("co_mention_count") or 0) >= pg.EVENT_GUARD_CO_MENTIONS


def rt(rows):
    return pa.Table.from_pylist(rows, schema=pg.GOLD_EVENT_SCHEMA).to_pylist()


def main():
    client = store._default_client()
    mn_key, mn_parts = j2.newest_part(client, pg.GOLD_TABLE)
    mention = j2.read_rows(client, mn_key)
    arts = {r["article_key"]: r for r in pg._iter_latest_articles(client=client)}
    enriched = [dict(r, title=arts.get(r["article_key"], {}).get("title")) for r in mention]
    print("== HVST-l-1 AC2 == mention part %s (%d parts, %d rows); silver articles %d" % (mn_key, mn_parts, len(mention), len(arts)))
    new_fn = pg._is_guarded
    new = rt(pg.event_rows(enriched))
    pg._is_guarded = old_guard
    try:
        old = rt(pg.event_rows(enriched))
    finally:
        pg._is_guarded = new_fn
    print("events: new guard=%d, k-1 guard=%d" % (len(new), len(old)))
    o_by = {e["event_id"]: e for e in old}
    ident = 0
    for e in new:
        o = o_by.get(e["event_id"])
        same = o is not None and all(j2.canon(e.get(f)) == j2.canon(o.get(f)) for f in set(e) | set(o))
        ident += same
        print("   %s %s %s..%s articles=%d : %s" % ("IDENTICAL" if same else "DIFFERS", e["event_id"][:12], e["security_key"],
                                                    e["first_day"], e["articles_total"], "all fields" if same else "no/unequal k-1 event"))
    order_same = [e["event_id"] for e in new] == [e["event_id"] for e in old]
    mism = [r for r in mention if bool(r.get("is_roundup")) != ((r.get("co_mention_count") or 0) >= 5)]
    print("identical events: %d of %d (k-1 events %d; same order: %s)" % (ident, len(new), len(old), order_same))
    print("mention rows where is_roundup != (co_mention_count >= 5): %d of %d" % (len(mism), len(mention)))
    ok = ident == len(new) == len(old) and len(new) > 0 and order_same and not mism
    print("AC2 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
