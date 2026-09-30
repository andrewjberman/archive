"""Shared loader and comparator for HVST-d-2. Reads S3 (GET/LIST/HEAD only); nothing here writes.

`memory()` builds the three tables IN MEMORY from the securities file and the landed silver, through the
same functions the producers call, and round-trips every row through the table's own arrow schema so
the rows compare like-for-like with what parquet returns. `classify_*` set a rebuilt table against a
served one and mark every moved row INSIDE or OUTSIDE the never-widen pair
(NEVER_WIDEN_HALF_COO_D2.md @ba195dc1c6 s.4, NEVER_WIDEN_ROUND15_D2_CTO_HALF.md @939395dd8d s.1)."""
import datetime
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow as pa  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

DELIVERABLES = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                            "0.9.0_WK_AMGT_HARVST~41")
SECURITIES = os.path.join(DELIVERABLES, "securities.universe.json")
TABLES = (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE)  # build order: each reads the newest of the one before
SCHEMAS = {pg.GOLD_TABLE: pg.GOLD_MENTION_SCHEMA, pg.GOLD_DAILY_TABLE: pg.GOLD_DAILY_SCHEMA,
           pg.GOLD_EVENT_TABLE: pg.GOLD_EVENT_SCHEMA}

# ---- the pair, as the two halves state it ------------------------------------------------------------
AMZN, TSM = "AMZN_US_Equity", "TSM_US_Equity"
CO_ONLY_SECURITIES = frozenset((  # the 14 securities whose rows gain a co-mention entry and nothing else
    "992_HK_Equity", "AAPL_US_Equity", "BAC_US_Equity", "BA_US_Equity", "COST_US_Equity", "HD_US_Equity",
    "INTC_US_Equity", "JNJ_US_Equity", "MU_US_Equity", "NOVN_SW_Equity", "NVDA_US_Equity", "TSLA_US_Equity",
    "ULVR_LN_Equity", "UL_US_Equity"))
CO_ALLOWED_GAIN = frozenset((AMZN, TSM))
EXPECT = {
    "mention_served_rows": 263, "mention_added": 12, "mention_added_amzn": 11, "mention_added_tsm": 1,
    "mention_amzn_changed": 8, "mention_co_only_pairs": 27,
    "daily_served_rows": 50997, "daily_amzn_cells": 161, "daily_tsm_cells": 215,
    "daily_ext_nonzero_at_0929": 280,
    "event_served": 7, "event_new": 1,
}
# BEFORE-state at the cut (COO half s.3): parts, newest key, ETag, rows.
BEFORE_EXPECT = {
    pg.GOLD_TABLE: (3, "date=2026-09-24/part-20260924T105025Z", "0b652726aaef64bad2474eb4cb0bc0d3", 263),
    pg.GOLD_DAILY_TABLE: (4, "date=2026-09-24/part-20260924T105051Z", "cdb4e0a05f4a2e59a96e41e3a680d4ef", 50997),
    pg.GOLD_EVENT_TABLE: (6, "date=2026-09-29/part-20260929T062617Z", "391cfd4bd2509fdfa8380e9dff036b5b", 7),
}
NEW_EVENT = ("AMZN_US_Equity", datetime.date(2026, 9, 7), datetime.date(2026, 9, 7), 3, "barrons:WP-BAR-0001904504")


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


def parts(table, client):
    """[(key, ETag, size)] of every parquet part, sorted the way readers sort (date, key)."""
    prefix = store.table_prefix("amgt", "gold", table)
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                out.append((obj["Key"], obj["ETag"].strip('"'), obj["Size"]))
    return sorted(out, key=lambda p: (pg._DATE_PARTITION_RE.search(p[0]).group(1), p[0]))


def read_key(key, client):
    import io

    import pyarrow.parquet as pq
    resp = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
    return pq.read_table(io.BytesIO(resp["Body"].read())).to_pylist()


def short(key):
    return key.split("/gold/", 1)[-1].split("/", 1)[-1]


def date_of(key):
    return datetime.date.fromisoformat(pg._DATE_PARTITION_RE.search(key).group(1))


def roundtrip(rows, table):
    return pa.Table.from_pylist(list(rows), schema=SCHEMAS[table]).to_pylist()


def memory(securities, as_of, client):
    """{table: rows} built in memory. Same functions as build_mention / build_daily / build_event."""
    articles = list(pg._iter_latest_articles(client=client))
    title_of = {x.get("article_key"): x.get("title") for x in articles}
    mention = []
    for art in articles:
        mention.extend(pg.mention_rows(art, securities))
    mention_rt = roundtrip(mention, pg.GOLD_TABLE)
    hits = list(pg._iter_all_listing_hits(client=client))
    coverage = pg.publisher_coverage(hits, securities)
    daily = pg.daily_rows(mention_rt, securities, start=pg.BACKFILL_FLOOR, end=as_of, coverage=coverage)
    enriched = []
    for r in mention_rt:
        r = dict(r)
        r["title"] = title_of.get(r.get("article_key"))
        enriched.append(r)
    event = pg.event_rows(enriched)
    return {pg.GOLD_TABLE: mention_rt, pg.GOLD_DAILY_TABLE: roundtrip(daily, pg.GOLD_DAILY_TABLE),
            pg.GOLD_EVENT_TABLE: roundtrip(event, pg.GOLD_EVENT_TABLE)}, len(articles), title_of


# ---- classification against the pair --------------------------------------------------------------------

def _diff(x, y):
    return sorted(k for k in set(x) | set(y) if canon(x.get(k)) != canon(y.get(k)))


def classify_mention(served, new):
    pair = lambda r: (r["article_key"], r["security_key"])  # noqa: E731
    s = {pair(r): r for r in served}
    n = {pair(r): r for r in new}
    res = {"served": len(s), "new": len(n), "added": [], "removed": [], "changed": [], "outside": [],
           "dup": (len(s) != len(served)) or (len(n) != len(new))}
    for p in sorted(set(n) - set(s)):
        res["added"].append(p)
        if p[1] not in (AMZN, TSM):
            res["outside"].append("ADDED pair for an unnamed security: %s %s" % p)
    for p in sorted(set(s) - set(n)):
        res["removed"].append(p)
        res["outside"].append("REMOVED pair: %s %s" % p)
    amzn_changed = co_only = 0
    for p in sorted(set(s) & set(n)):
        fields = _diff(s[p], n[p])
        if not fields:
            continue
        res["changed"].append((p, fields))
        if p[1] == AMZN:
            amzn_changed += 1
            continue
        old_co, new_co = list(s[p]["co_mentioned_securities"] or []), list(n[p]["co_mentioned_securities"] or [])
        gained, lost = set(new_co) - set(old_co), set(old_co) - set(new_co)
        if (set(fields) <= {"co_mentioned_securities", "co_mention_count"} and gained and gained <= CO_ALLOWED_GAIN
                and not lost and p[1] in CO_ONLY_SECURITIES):
            co_only += 1
        else:
            res["outside"].append("CHANGED existing row beyond a co-mention gain of AMZN/TSM: %s %s fields=%s gained=%s lost=%s"
                                  % (p[0], p[1], fields, sorted(gained), sorted(lost)))
    res["amzn_changed"], res["co_only"] = amzn_changed, co_only
    added_amzn = sum(1 for p in res["added"] if p[1] == AMZN)
    added_tsm = sum(1 for p in res["added"] if p[1] == TSM)
    res["added_amzn"], res["added_tsm"] = added_amzn, added_tsm
    for label, got, want in (("rows added", len(res["added"]), EXPECT["mention_added"]),
                             ("AMZN rows added", added_amzn, EXPECT["mention_added_amzn"]),
                             ("TSM rows added", added_tsm, EXPECT["mention_added_tsm"]),
                             ("AMZN existing rows changed", amzn_changed, EXPECT["mention_amzn_changed"]),
                             ("co-mention-only pairs", co_only, EXPECT["mention_co_only_pairs"])):
        if got != want:
            res["outside"].append("COUNT %s = %d, the pair names %d" % (label, got, want))
    return res


def classify_daily(served, new, as_of):
    key = lambda r: (r["security_key"], r["day"])  # noqa: E731
    s = {key(r): r for r in served}
    n = {key(r): r for r in new}
    srv_end = max(k[1] for k in s)
    res = {"served": len(s), "new": len(n), "srv_end": srv_end, "as_of": as_of, "outside": [], "moved": {}, "ext": 0,
           "ext_nonzero": 0, "dup": (len(s) != len(served)) or (len(n) != len(new))}
    ext_days = (as_of - srv_end).days
    for k in sorted(set(s) - set(n)):
        res["outside"].append("SERVED cell missing from the rebuild: %s %s" % k)
    cols_moved = {}
    for k in sorted(n):
        if k not in s:
            if srv_end < k[1] <= as_of:
                res["ext"] += 1
                r = n[k]
                if any(r[c] for c in ("articles_total", "mention_score", "trailing_7d_sum", "trailing_30d_sum",
                                      "baseline_30d_sum", "cumulative_ytd")):
                    res["ext_nonzero"] += 1
            else:
                res["outside"].append("NEW cell outside the extension window: %s %s" % k)
            continue
        fields = _diff(s[k], n[k])
        if not fields:
            continue
        if k[0] in (AMZN, TSM):
            res["moved"][k[0]] = res["moved"].get(k[0], 0) + 1
            for f in fields:
                cols_moved[f] = cols_moved.get(f, 0) + 1
        else:
            res["outside"].append("MOVED cell of an unnamed security: %s %s fields=%s" % (k[0], k[1], fields))
    res["cols_moved"] = cols_moved
    if res["ext"] != 191 * ext_days:
        res["outside"].append("COUNT extension rows = %d, the pair names 191 x %d = %d" % (res["ext"], ext_days, 191 * ext_days))
    # The pair's 161 (AMZN) and 215 (TSM) count each security's cells over the WHOLE new range: the cells
    # that moved on days <= the served end, plus one extension cell per extension day (156 + 5, 210 + 5).
    for sec, want in ((AMZN, EXPECT["daily_amzn_cells"]), (TSM, EXPECT["daily_tsm_cells"])):
        got = res["moved"].get(sec, 0) + ext_days
        if got != want + (ext_days - 5):
            res["outside"].append("COUNT %s moved cells + %d extension cells = %d, the pair names %d (at 5 extension days)" % (
                sec, ext_days, got, want))
    if as_of == datetime.date(2026, 9, 29) and res["ext_nonzero"] != EXPECT["daily_ext_nonzero_at_0929"]:
        res["outside"].append("COUNT extension rows with non-zero windows = %d, the pair names %d" % (
            res["ext_nonzero"], EXPECT["daily_ext_nonzero_at_0929"]))
    return res


def classify_event(served, new):
    s = {r["event_id"]: r for r in served}
    n = {r["event_id"]: r for r in new}
    res = {"served": len(served), "new": len(new), "kept": [], "moved": [], "gone": [], "added": [], "outside": [],
           "unique": len(s) == len(served) and len(n) == len(new)}
    for eid in sorted(s):
        if eid not in n:
            res["gone"].append(eid)
            res["outside"].append("SERVED event GONE or re-cut: %s %s %s" % (s[eid]["security_key"], s[eid]["first_day"], eid[:12]))
        elif _diff(s[eid], n[eid]):
            res["moved"].append((eid, _diff(s[eid], n[eid])))
            res["outside"].append("SERVED event MOVED (same id, fields %s): %s" % (_diff(s[eid], n[eid]), s[eid]["security_key"]))
        else:
            res["kept"].append(eid)
    for eid in sorted(set(n) - set(s)):
        e = n[eid]
        res["added"].append(eid)
        got = (e["security_key"], e["first_day"], e["last_day"], e["articles_total"], e["lead_article_key"])
        if got != NEW_EVENT:
            res["outside"].append("NEW event the pair did not name: %s" % (got,))
    if len(res["added"]) != EXPECT["event_new"]:
        res["outside"].append("COUNT new events = %d, the pair names %d" % (len(res["added"]), EXPECT["event_new"]))
    if not res["unique"]:
        res["outside"].append("event_id not unique")
    return res


def print_classification(tag, m, d, e):
    print("  [%s] mention: served=%d new=%d added=%d (AMZN %d, TSM %d) removed=%d AMZN existing rows changed=%d co-mention-only pairs=%d across %d securities" % (
        tag, m["served"], m["new"], len(m["added"]), m["added_amzn"], m["added_tsm"], len(m["removed"]), m["amzn_changed"],
        m["co_only"], len({p[1] for p, f in m["changed"] if p[1] != AMZN})))
    print("  [%s] daily: served=%d new=%d  ALIAS moved cells %s (columns moved %s)  DRIFT on days <= %s: 0 unnamed-security cells %s  extension rows=%d (%s..%s), with non-zero windows/cumulative=%d" % (
        tag, d["served"], d["new"], d["moved"], d["cols_moved"], d["srv_end"],
        "(none)" if not [o for o in d["outside"] if o.startswith("MOVED")] else "PRESENT", d["ext"],
        d["srv_end"] + datetime.timedelta(days=1), d["as_of"], d["ext_nonzero"]))
    print("  [%s] event: served=%d new=%d kept=%d moved=%d gone=%d added=%d ids unique=%s" % (
        tag, e["served"], e["new"], len(e["kept"]), len(e["moved"]), len(e["gone"]), len(e["added"]), e["unique"]))
    for o in m["outside"] + d["outside"] + e["outside"]:
        print("  OUTSIDE THE PAIR [%s]: %s" % (tag, o))
