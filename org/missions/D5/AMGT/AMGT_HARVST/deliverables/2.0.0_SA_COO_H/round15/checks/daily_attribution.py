"""HVST-d-2 COO half, the CTO's condition (msg 26512): every chatter_daily move attributed ALIAS or DRIFT
PER SECURITY, with the new --as-of named. Compares EVERY column of the served daily schema (not a
subset). ALIAS = new aliases vs old aliases over today's silver; DRIFT = old aliases today vs the SERVED
part (days <= the served end), plus the day-range extension past it. S3 GET only."""
import collections
import datetime
import json
import sys

sys.path.insert(0, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~41/scripts")
import _common  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def run(as_of):
    client = store._default_client()
    with open(_common.SECURITIES_NEW, "r", encoding="utf-8") as fh:
        sec_new = json.load(fh)
    sec_old, _ = _common.load_old_module().build()
    articles = list(pg._iter_latest_articles(client=client))
    hits = list(pg._iter_all_listing_hits(client=client))

    def mention(secs):
        rows = []
        for art in articles:
            rows.extend(pg.mention_rows(art, secs))
        return rows

    old = pg.daily_rows(mention(sec_old), sec_old, start=pg.BACKFILL_FLOOR, end=as_of,
                        coverage=pg.publisher_coverage(hits, sec_old))
    new = pg.daily_rows(mention(sec_new), sec_new, start=pg.BACKFILL_FLOOR, end=as_of,
                        coverage=pg.publisher_coverage(hits, sec_new))
    srv = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE, client=client)
    d_srv = {(r["security_key"], r["day"]): r for r in srv}
    d_old = {(r["security_key"], r["day"]): r for r in old}
    d_new = {(r["security_key"], r["day"]): r for r in new}
    cols = sorted(set(srv[0]) - {"security_key", "day"})
    srv_end = max(k[1] for k in d_srv)

    def differs(x, y):
        return [c for c in cols if x.get(c) != y.get(c)]

    alias = collections.defaultdict(lambda: collections.Counter())
    for k in set(d_old) & set(d_new):
        for c in differs(d_old[k], d_new[k]):
            alias[k[0]][c] += 1
    alias_cells = collections.Counter(k[0] for k in set(d_old) & set(d_new) if differs(d_old[k], d_new[k]))
    drift = collections.Counter(k[0] for k in set(d_srv) & set(d_old) if differs(d_srv[k], d_old[k]))
    drift_cols = collections.Counter(c for k in set(d_srv) & set(d_old) for c in differs(d_srv[k], d_old[k]))
    ext = [k for k in d_new if k[1] > srv_end]
    ext_nonzero = collections.Counter(k[0] for k in ext if any(d_new[k].get(c) for c in (
        "articles_total", "mention_count_total", "trailing_7d_sum", "trailing_30d_sum", "cumulative_ytd")))
    lost = sorted(set(d_srv) - set(d_new))

    print("as_of=%s  served end=%s  columns compared=%d %s" % (as_of, srv_end, len(cols), cols))
    print("rows served=%d old=%d new=%d  extension rows (day > %s)=%d  served keys absent from new=%d" % (
        len(d_srv), len(d_old), len(d_new), srv_end, len(ext), len(lost)))
    print("ALIAS cells per security (new vs old, any column, all days): %s" % dict(alias_cells))
    for s in sorted(alias):
        print("  ALIAS %-18s columns moved: %s" % (s, dict(alias[s])))
    print("DRIFT cells per security (old vs served, days <= %s, any column): %d cells %s" % (
        srv_end, sum(drift.values()), dict(drift)))
    print("DRIFT columns: %s" % dict(drift_cols))
    print("EXTENSION rows carrying a non-zero count or window (new build, day > %s): %d, per security %s" % (
        srv_end, sum(ext_nonzero.values()), dict(ext_nonzero)))


if __name__ == "__main__":
    run(datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now(datetime.timezone.utc).date())
