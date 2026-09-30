"""HVST-e-2 COO half: per-security attribution of every mention and daily move the span count makes, read
from the MERGED matcher at signing. OLD = the pre-round-16 matcher (every alias independently, summed),
reproduced here verbatim; NEW = publication_gold._match_counts at HEAD. Both over today's silver and the
pinned securities, set beside the SERVED newest parts. Also: event_rows over NEW equals the served event part.
S3 GET only."""
import collections
import datetime
import json
import sys

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402

SECURITIES = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~41/securities.universe.json"


def old_match_counts(text, aliases):
    count = 0
    forms = []
    for alias in aliases:
        n = len(pg._alias_pattern(alias).findall(text or ""))
        if n:
            count += n
            forms.append(alias)
    return count, forms


def build(articles, secs, matcher):
    saved = pg._match_counts
    pg._match_counts = matcher
    try:
        rows = []
        for art in articles:
            rows.extend(pg.mention_rows(art, secs))
        return rows
    finally:
        pg._match_counts = saved


def run(as_of):
    with open(SECURITIES, "r", encoding="utf-8") as fh:
        secs = json.load(fh)
    articles = list(pg._iter_latest_articles())
    hits = list(pg._iter_all_listing_hits())
    cov = pg.publisher_coverage(hits, secs)
    old = build(articles, secs, old_match_counts)
    new = build(articles, secs, pg._match_counts)
    srv = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    key = lambda r: (r["article_key"], r["security_key"])  # noqa: E731
    m_old, m_new, m_srv = ({key(r): r for r in x} for x in (old, new, srv))
    mcols = sorted(set(srv[0]) - {"article_key", "security_key"})
    drift_m = [k for k in set(m_old) | set(m_srv) if k not in m_old or k not in m_srv or any(m_old[k].get(c) != m_srv[k].get(c) for c in mcols)]
    span_m = collections.defaultdict(collections.Counter)
    for k in set(m_old) | set(m_new):
        if k not in m_old or k not in m_new:
            span_m[k[1]]["ADDED/REMOVED"] += 1
            continue
        for c in mcols:
            if m_old[k].get(c) != m_new[k].get(c):
                span_m[k[1]][c] += 1
    print("as_of=%s silver articles=%d mention rows served=%d old=%d new=%d" % (as_of, len(articles), len(m_srv), len(m_old), len(m_new)))
    print("MENTION DRIFT (old matcher vs served, all %d columns): %d rows" % (len(mcols), len(drift_m)))
    print("MENTION SPAN moves per security (column -> rows): %d securities" % len(span_m))
    for s in sorted(span_m):
        print("  %-18s %s" % (s, dict(span_m[s])))
    tiers = collections.Counter((k[1], m_old[k]["signal_tier"], m_new[k]["signal_tier"]) for k in set(m_old) & set(m_new)
                                if m_old[k]["signal_tier"] != m_new[k]["signal_tier"])
    print("TIER moves: %s" % {"%s %s->%s" % t: n for t, n in sorted(tiers.items())})

    d_old = {(r["security_key"], r["day"]): r for r in pg.daily_rows(old, secs, start=pg.BACKFILL_FLOOR, end=as_of, coverage=cov)}
    d_new = {(r["security_key"], r["day"]): r for r in pg.daily_rows(new, secs, start=pg.BACKFILL_FLOOR, end=as_of, coverage=cov)}
    d_srv = {(r["security_key"], r["day"]): r for r in pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)}
    dcols = sorted(set(next(iter(d_srv.values()))) - {"security_key", "day"})
    srv_end = max(k[1] for k in d_srv)
    span_d = collections.defaultdict(collections.Counter)
    cells = collections.Counter()
    for k in set(d_old) & set(d_new):
        moved = [c for c in dcols if d_old[k].get(c) != d_new[k].get(c)]
        if moved:
            cells[k[0]] += 1
            for c in moved:
                span_d[k[0]][c] += 1
    drift_d = sum(1 for k in set(d_old) & set(d_srv) if any(d_old[k].get(c) != d_srv[k].get(c) for c in dcols))
    print("DAILY rows served=%d old=%d new=%d served end=%s extension rows=%d served keys absent from new=%d" % (
        len(d_srv), len(d_old), len(d_new), srv_end, sum(1 for k in d_new if k[1] > srv_end), len(set(d_srv) - set(d_new))))
    print("DAILY SPAN cells per security: %s (total %d)" % (dict(cells), sum(cells.values())))
    for s in sorted(span_d):
        print("  %-18s %s" % (s, dict(span_d[s])))
    print("DAILY DRIFT (old matcher vs served, days <= %s, all %d columns): %d cells" % (srv_end, len(dcols), drift_d))

    titles = {a.get("article_key"): a.get("title") for a in articles}
    ev_new = pg.event_rows([dict(r, title=titles.get(r["article_key"])) for r in new])
    ev_srv = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    norm = lambda e: json.dumps({k: (sorted(v) if isinstance(v, list) else v) for k, v in e.items()}, sort_keys=True, default=str)  # noqa: E731
    print("EVENTS served=%d from NEW mention=%d equal row by row: %s" % (
        len(ev_srv), len(ev_new), sorted(map(norm, ev_srv)) == sorted(map(norm, ev_new))))


if __name__ == "__main__":
    run(datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now(datetime.timezone.utc).date())
