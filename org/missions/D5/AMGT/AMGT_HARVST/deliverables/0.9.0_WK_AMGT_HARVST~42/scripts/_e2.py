"""Shared helpers for HVST-e-2: the pair (COO half @604165a591 s.3-4, CTO half @73fce69599) as data, and the checks
that set a table's moved rows against it. Reads only; nothing here writes to S3."""
import collections
import datetime
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402

NEW = C.NEW
AS_OF_ALLOWED = (datetime.date(2026, 9, 29), datetime.date(2026, 9, 30))

# COO half s.3: the BEFORE state at signing (parts, newest key, ETag, rows).
BEFORE_EXPECT = {
    NEW.GOLD_TABLE: (4, "date=2026-09-29/part-20260929T092419Z.parquet", "4a5e91d38405f09d3052343f69a68151", 275),
    NEW.GOLD_DAILY_TABLE: (5, "date=2026-09-29/part-20260929T092435Z.parquet", "561a3bd6513eccacd68dab502a5a3a93", 51952),
    NEW.GOLD_EVENT_TABLE: (7, "date=2026-09-29/part-20260929T092439Z.parquet", "c146a325c98963f965b8b1bd69ca3393", 8),
}

# COO half s.4.1: per security (mention_count moved, match_forms moved, tier moved) over 14 rows.
MENTION_EXPECT = {
    "AMZN_US_Equity": (8, 7, 2), "UPS_US_Equity": (2, 2, 2), "DAL_US_Equity": (1, 1, 1),
    "FDX_US_Equity": (1, 1, 1), "GOOGL_US_Equity": (1, 1, 1), "GOOG_US_Equity": (1, 1, 1),
}
AMZN_TIER_ARTICLES = {"barrons:WP-BAR-0001882188", "sa:4638889"}
MENTION_MOVABLE = {"mention_count", "match_forms", "signal_tier", "signal_weight"}

# COO half s.4.2: SPAN cells per security (212) and the direct columns' cell counts.
DAILY_EXPECT = {"AMZN_US_Equity": 41, "DAL_US_Equity": 65, "GOOGL_US_Equity": 29, "GOOG_US_Equity": 29,
                "UPS_US_Equity": 24, "FDX_US_Equity": 24}
DAILY_DIRECT_CELLS = {"AMZN_US_Equity": (7, 2), "UPS_US_Equity": (2, 2), "DAL_US_Equity": (1, 1),
                      "FDX_US_Equity": (1, 1), "GOOGL_US_Equity": (1, 1), "GOOG_US_Equity": (1, 1)}
DAILY_MOVABLE = {"mention_count_total", "mention_score", "tier_c", "tier_d", "trailing_7d_sum", "trailing_30d_sum",
                 "baseline_30d_sum", "cumulative_ytd"}
SECURITIES_N = 191


def index(rows, table):
    kf = C.KEYS[table]
    return {kf(r): C.canon_row(r) for r in rows}, len(rows)


def check_mention(before_rows, after_rows, title_of=None):
    """(outside: [str], lines: [str]) -- the moved mention rows set against the pair's s.4.1."""
    t = NEW.GOLD_TABLE
    b, bn = index(before_rows, t)
    a, an = index(after_rows, t)
    outside, lines = [], []
    lines.append("rows before=%d after=%d  duplicate keys before/after=%s/%s" % (bn, an, len(b) != bn, len(a) != an))
    if len(b) != bn or len(a) != an:
        outside.append("duplicate (article_key, security_key) in a mention table")
    added, removed = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    lines.append("rows ADDED=%d REMOVED=%d (pair: 0 and 0)" % (len(added), len(removed)))
    for k in added:
        outside.append("mention row ADDED: %s" % (k,))
    for k in removed:
        outside.append("mention row REMOVED: %s" % (k,))
    per = collections.defaultdict(lambda: [0, 0, 0])
    tier_articles = collections.defaultdict(set)
    moved = 0
    for k in sorted(set(a) & set(b)):
        fields = C.diff_fields(b[k], a[k])
        if not fields:
            continue
        moved += 1
        art, sec = k
        head = C.a((title_of or {}).get(art), 80)
        lines.append("  moved %s | %s | %s | %s" % (sec, art, "; ".join("%s: %r -> %r" % (f, b[k][f], a[k][f]) for f in fields), head))
        if sec not in MENTION_EXPECT:
            outside.append("moved row of a security the pair does not name: %s %s fields=%s" % (sec, art, fields))
            continue
        extra = set(fields) - MENTION_MOVABLE
        if extra:
            outside.append("moved row changed columns the pair does not name: %s %s %s" % (sec, art, sorted(extra)))
        if "mention_count" not in fields or not a[k]["mention_count"] < b[k]["mention_count"]:
            outside.append("moved row whose mention_count did not fall: %s %s" % (sec, art))
        per[sec][0] += "mention_count" in fields
        per[sec][1] += "match_forms" in fields
        if "signal_tier" in fields:
            per[sec][2] += 1
            tier_articles[sec].add(art)
            if (b[k]["signal_tier"], a[k]["signal_tier"]) != ("C", "D"):
                outside.append("tier moved other than C->D: %s %s %s->%s" % (sec, art, b[k]["signal_tier"], a[k]["signal_tier"]))
            if "signal_weight" not in fields:
                outside.append("tier moved without signal_weight: %s %s" % (sec, art))
    lines.append("moved rows=%d (pair: 14) over %d securities (pair: 6)" % (moved, len(per)))
    for sec in sorted(set(per) | set(MENTION_EXPECT)):
        got = tuple(per[sec]) if sec in per else (0, 0, 0)
        want = MENTION_EXPECT.get(sec, (0, 0, 0))
        lines.append("  %-16s mention_count moved=%d match_forms moved=%d tier moved=%d  (pair %s) %s" % (
            sec, got[0], got[1], got[2], want, "OK" if got == want else "DIFFERS"))
        if got != want:
            outside.append("COUNT %s (count, forms, tier) = %s, the pair names %s" % (sec, got, want))
    if tier_articles.get("AMZN_US_Equity") != AMZN_TIER_ARTICLES and "AMZN_US_Equity" in per:
        outside.append("AMZN tier-moved articles %s, the pair names %s" % (sorted(tier_articles["AMZN_US_Equity"]), sorted(AMZN_TIER_ARTICLES)))
    if moved != 14:
        outside.append("COUNT moved rows = %d, the pair names 14" % moved)
    return outside, lines


def check_daily(before_rows, after_rows, as_of):
    """(outside, lines) -- the moved daily cells set against the pair's s.4.2 and its as-of branch."""
    t = NEW.GOLD_DAILY_TABLE
    b, bn = index(before_rows, t)
    a, an = index(after_rows, t)
    outside, lines = [], []
    srv_end = max(k[1] for k in b)
    ext_days = (as_of - srv_end).days
    lines.append("cells before=%d after=%d  duplicate keys=%s/%s  before last day=%s as-of=%s" % (
        bn, an, len(b) != bn, len(a) != an, srv_end, as_of))
    if len(b) != bn or len(a) != an:
        outside.append("duplicate (security, day) in a daily table")
    for k in sorted(set(b) - set(a)):
        outside.append("daily cell REMOVED: %s %s" % k)
    ext = [k for k in a if k not in b]
    bad_ext = [k for k in ext if not (srv_end < k[1] <= as_of)]
    lines.append("extension cells=%d (pair: %d = 191 x %d extension days at as-of %s)" % (len(ext), SECURITIES_N * max(ext_days, 0), max(ext_days, 0), as_of))
    for k in bad_ext:
        outside.append("daily cell ADDED outside the extension window: %s %s" % k)
    if len(ext) != SECURITIES_N * max(ext_days, 0):
        outside.append("COUNT extension cells = %d, the pair names %d" % (len(ext), SECURITIES_N * max(ext_days, 0)))
    per = collections.defaultdict(int)
    cols = collections.Counter()
    direct = collections.defaultdict(lambda: collections.Counter())
    for k in sorted(set(a) & set(b)):
        fields = C.diff_fields(b[k], a[k])
        if not fields:
            continue
        sec, day = k
        if sec not in DAILY_EXPECT:
            outside.append("moved cell of a security the pair does not name: %s %s fields=%s" % (sec, day, fields))
            continue
        extra = set(fields) - DAILY_MOVABLE
        if extra:
            outside.append("moved cell changed columns the pair does not name: %s %s %s" % (sec, day, sorted(extra)))
        per[sec] += 1
        for f in fields:
            cols[f] += 1
        for f in ("mention_count_total", "tier_c"):
            if f in fields:
                direct[sec][f] += 1
    lines.append("moved cells=%d (pair: 212)  columns moved (cell counts): %s" % (sum(per.values()), dict(sorted(cols.items()))))
    for sec in sorted(set(per) | set(DAILY_EXPECT)):
        want = DAILY_EXPECT.get(sec, 0)
        wd = DAILY_DIRECT_CELLS.get(sec, (0, 0))
        gd = (direct[sec]["mention_count_total"], direct[sec]["tier_c"]) if sec in direct else (0, 0)
        ok = per[sec] == want and gd == wd
        lines.append("  %-16s moved cells=%d (pair %d)  direct: mention_count_total cells=%d tier cells=%d (pair %s) %s" % (
            sec, per[sec], want, gd[0], gd[1], wd, "OK" if ok else "DIFFERS"))
        if not ok:
            outside.append("COUNT %s cells/direct = %d %s, the pair names %d %s" % (sec, per[sec], gd, want, wd))
    if sum(per.values()) != 212:
        outside.append("COUNT moved daily cells = %d, the pair names 212" % sum(per.values()))
    return outside, lines


def snapshot(client):
    """{table: [(key, etag, size)]} for every parquet part of the three tables."""
    return {t: C.parts(t, client) for t in C.TABLES}


def rows_of(key, client):
    import io

    import pyarrow.parquet as pq
    resp = client.get_object(Bucket=C.store.HARVEST_BUCKET, Key=key)
    return pq.read_table(io.BytesIO(resp["Body"].read())).to_pylist()
