"""HVST-d-1 AC2: the rebuild, IN MEMORY, over the landed silver -- built twice (OLD aliases from the
BASE module, NEW aliases from securities.universe.json) and set beside the SERVED newest snapshots.
Every moved row is attributed ALIAS (new vs old, same silver) or DRIFT (old vs served: silver has
grown / the range extends). S3 GET only: no put, no delete, no vendor call."""
import datetime
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as new_mod  # noqa: E402

AMZN = "AMZN_US_Equity"
CRASH = re.compile(r"cargo|runway|plane|crash|overshoot|miami", re.I)
MENTION_FIELDS = ("signal_tier", "mention_in_title", "mention_in_lead", "mention_count", "blocks_hit", "match_forms")
DAILY_FIELDS = ("articles_total", "tier_a", "tier_b", "tier_c", "tier_d", "mention_count_total",
                "publishers_distinct", "data_status")
DAILY_DERIVED = ("trailing_7d_sum", "trailing_30d_sum", "baseline_30d_sum", "baseline_30d_days", "cumulative_ytd")


def a(text, n=None):
    s = ("" if text is None else str(text)).encode("ascii", "replace").decode("ascii")
    return s[:n] if n else s


def day(r):
    return pg._day_of(r.get("published_utc"))


def pair(r):
    return (r["article_key"], r["security_key"])


def norm(v):
    return sorted(v) if isinstance(v, (list, tuple)) else v


def sig(r, fields):
    return tuple(norm(r.get(f)) for f in fields)


def load_served(client):
    out = {}
    for table in (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE):
        key = _common.newest_snapshot_key(table, client)
        out[table] = (key, pg._latest_gold_snapshot_rows(table, client=client))
    return out


def main():
    client = store._default_client()
    problems = []

    # ---- inputs ------------------------------------------------------------------------------
    print("== INPUTS ==")
    with open(_common.SECURITIES_NEW, "r", encoding="utf-8") as fh:
        sec_new = json.load(fh)
    old_mod = _common.load_old_module()
    sec_old, _ = old_mod.build()
    print("securities NEW=%d (from %s)  OLD=%d (BASE module build over the same pool universe, no sa join)" % (
        len(sec_new), _common.SECURITIES_NEW.split("deliverables")[-1], len(sec_old)))
    assert [s["key"] for s in sec_new] == [s["key"] for s in sec_old], "security lists differ"
    print("every OLD alias list is a prefix of its NEW list: %s" % all(
        n["aliases"][:len(o["aliases"])] == o["aliases"] for o, n in zip(sec_old, sec_new)))
    fresh, _ = new_mod.build()
    print("securities.universe.json == a fresh build() of the module now: %s" % (
        json.loads(json.dumps(fresh, sort_keys=True)) == json.loads(json.dumps(sec_new, sort_keys=True))))

    articles = list(pg._iter_latest_articles(client=client))
    title_of = {x.get("article_key"): x.get("title") for x in articles}
    print("silver articles read (latest per key) = %d" % len(articles))

    served = load_served(client)
    for table, (key, rows) in served.items():
        print("served %-26s key=%s rows=%d" % (table, key, len(rows)))
    print("served pins named by the task order: mention %s ; daily %s" % (
        _common.SERVED_PINS["article_security_mention"], _common.SERVED_PINS["chatter_daily"]))
    for table, pin in (("article_security_mention", _common.SERVED_PINS["article_security_mention"]),
                       ("chatter_daily", _common.SERVED_PINS["chatter_daily"])):
        k = served[table][0] or ""
        print("  %s newest key carries the pin: %s" % (table, pin in k))

    def build(secs):
        rows = []
        for art in articles:
            rows.extend(pg.mention_rows(art, secs))
        for r in rows:
            r["title"] = title_of.get(r["article_key"])
        return rows

    rows_old = build(sec_old)
    rows_new = build(sec_new)
    rows_srv = served[pg.GOLD_TABLE][1]
    for r in rows_srv:
        r["title"] = title_of.get(r["article_key"])
    m_srv = {pair(r): r for r in rows_srv}
    m_old = {pair(r): r for r in rows_old}
    m_new = {pair(r): r for r in rows_new}
    assert len(m_srv) == len(rows_srv) and len(m_old) == len(rows_old) and len(m_new) == len(rows_new), "duplicate pair"

    # ---- (a) mention -------------------------------------------------------------------------
    print("\n== (a) article_security_mention ==")
    print("rows served=%d old=%d new=%d   articles served=%d old=%d new=%d   securities served=%d old=%d new=%d" % (
        len(rows_srv), len(rows_old), len(rows_new),
        len({r['article_key'] for r in rows_srv}), len({r['article_key'] for r in rows_old}), len({r['article_key'] for r in rows_new}),
        len({r['security_key'] for r in rows_srv}), len({r['security_key'] for r in rows_old}), len({r['security_key'] for r in rows_new})))

    drift_added = sorted(set(m_old) - set(m_srv))
    drift_removed = sorted(set(m_srv) - set(m_old))
    drift_changed = sorted(p for p in set(m_old) & set(m_srv) if sig(m_old[p], MENTION_FIELDS) != sig(m_srv[p], MENTION_FIELDS))
    alias_added = sorted(set(m_new) - set(m_old))
    alias_removed = sorted(set(m_old) - set(m_new))
    alias_changed = sorted(p for p in set(m_new) & set(m_old) if sig(m_new[p], MENTION_FIELDS) != sig(m_old[p], MENTION_FIELDS))
    print("DRIFT (old vs served, same alias rule): pairs added=%d removed=%d changed=%d" % (
        len(drift_added), len(drift_removed), len(drift_changed)))
    print("ALIAS (new vs old, same silver):        pairs added=%d removed=%d changed=%d" % (
        len(alias_added), len(alias_removed), len(alias_changed)))
    if alias_removed:
        problems.append("alias change REMOVED %d pairs (rule is additive)" % len(alias_removed))

    print("\nrow delta per security  (served -> old = DRIFT ; old -> new = ALIAS):")
    per_sec = {}
    for name, srv, o, n in (("x", m_srv, m_old, m_new),):
        for s in {p[1] for p in set(srv) | set(o) | set(n)}:
            cs = sum(1 for p in srv if p[1] == s)
            co = sum(1 for p in o if p[1] == s)
            cn = sum(1 for p in n if p[1] == s)
            per_sec[s] = (cs, co, cn)
    moved_secs = {s: v for s, v in per_sec.items() if len(set(v)) > 1}
    for s, (cs, co, cn) in sorted(moved_secs.items()):
        print("  %-22s served=%3d old=%3d new=%3d   drift %+d  alias %+d" % (s, cs, co, cn, co - cs, cn - co))
    print("  securities whose rows move: %d of %d with rows anywhere (%d securities in the universe)" % (
        len(moved_secs), len(per_sec), len(sec_new)))

    def show(p, m, label):
        r = m[p]
        print("  %-6s %-22s %-34s tier=%s title=%s lead=%s forms=%s | %s" % (
            label, p[1], p[0], r["signal_tier"], r["mention_in_title"], r["mention_in_lead"], r["match_forms"],
            a(r.get("title"), 100)))

    co_moved = [p for p in set(m_new) & set(m_old)
                if norm(m_new[p].get("co_mentioned_securities")) != norm(m_old[p].get("co_mentioned_securities"))]
    print("existing pairs whose CO-MENTION list moves under the alias change = %d, across securities %s" % (
        len(co_moved), sorted({p[1] for p in co_moved})))
    print("\nEVERY NEW (article, security) match from the alias change (the false-hit sample source): %d" % len(alias_added))
    for p in alias_added:
        show(p, m_new, "ALIAS+")
    print("\nEVERY existing pair the alias change MOVES (tier / flags / count): %d" % len(alias_changed))
    for p in alias_changed:
        o, n = m_old[p], m_new[p]
        print("  ALIAS~ %-22s %-34s tier %s->%s title %s->%s lead %s->%s count %s->%s forms %s->%s | %s" % (
            p[1], p[0], o["signal_tier"], n["signal_tier"], o["mention_in_title"], n["mention_in_title"],
            o["mention_in_lead"], n["mention_in_lead"], o["mention_count"], n["mention_count"],
            o["match_forms"], n["match_forms"], a(n.get("title"), 90)))
    print("\nDRIFT rows (silver moved since the served build) -- added %d, removed %d, changed %d:" % (
        len(drift_added), len(drift_removed), len(drift_changed)))
    for p in drift_added[:40]:
        show(p, m_old, "DRIFT+")
    if len(drift_added) > 40:
        print("  ... %d more DRIFT+ (same shape); per-security counts are above" % (len(drift_added) - 40))
    for p in drift_removed:
        show(p, m_srv, "DRIFT-")
    for p in drift_changed:
        print("  DRIFT~ %-22s %-34s served=%s old=%s" % (p[1], p[0], sig(m_srv[p], MENTION_FIELDS), sig(m_old[p], MENTION_FIELDS)))

    # ---- (b) AMZN crash articles ---------------------------------------------------------------
    print("\n== (b) AMZN articles: title/lead flags and tiers, served / old / new ==")
    amzn_pairs = sorted({p for p in set(m_srv) | set(m_old) | set(m_new) if p[1] == AMZN},
                        key=lambda p: (str((m_new.get(p) or m_old.get(p) or m_srv.get(p)).get("published_utc")), p[0]))
    crash_pairs = []
    for p in amzn_pairs:
        rs, ro, rn = m_srv.get(p), m_old.get(p), m_new.get(p)
        base = rn or ro or rs
        is_crash = bool(CRASH.search(base.get("title") or ""))
        if is_crash:
            crash_pairs.append(p)

        def f(r):
            return "absent" if r is None else "tier=%s T=%s L=%s n=%s" % (
                r["signal_tier"], int(bool(r["mention_in_title"])), int(bool(r["mention_in_lead"])), r["mention_count"])
        print("  %s %-34s %s %-4s | served: %-26s | old: %-26s | new: %-26s | %s" % (
            "CRASH" if is_crash else "     ", p[0], day(base), base.get("publisher"), f(rs), f(ro), f(rn), a(base.get("title"), 80)))
    print("AMZN pairs listed=%d (crash-pattern headlines marked CRASH=%d)" % (len(amzn_pairs), len(crash_pairs)))

    # ---- (c) daily ----------------------------------------------------------------------------
    print("\n== (c) chatter_daily ==")
    d_srv_rows = served[pg.GOLD_DAILY_TABLE][1]
    srv_end = max(r["day"] for r in d_srv_rows)
    srv_start = min(r["day"] for r in d_srv_rows)
    end = datetime.datetime.now(datetime.timezone.utc).date()
    hits = list(pg._iter_all_listing_hits(client=client))
    print("served daily rows=%d days %s..%s ; rebuild range %s..%s ; listing_hit rows read=%d" % (
        len(d_srv_rows), srv_start, srv_end, pg.BACKFILL_FLOOR, end, len(hits)))
    d_old_rows = pg.daily_rows(rows_old, sec_old, start=pg.BACKFILL_FLOOR, end=end,
                               coverage=pg.publisher_coverage(hits, sec_old))
    d_new_rows = pg.daily_rows(rows_new, sec_new, start=pg.BACKFILL_FLOOR, end=end,
                               coverage=pg.publisher_coverage(hits, sec_new))
    d_srv = {(r["security_key"], r["day"]): r for r in d_srv_rows}
    d_old = {(r["security_key"], r["day"]): r for r in d_old_rows}
    d_new = {(r["security_key"], r["day"]): r for r in d_new_rows}
    print("rows served=%d old=%d new=%d  (%d securities x %d days = %d for the rebuild; the %d extra days are range extension = DRIFT)" % (
        len(d_srv), len(d_old), len(d_new), len(sec_new), (end - pg.BACKFILL_FLOOR).days + 1, len(d_new),
        (end - srv_end).days))

    def moved(x, y, fields, only_days_le=None):
        out = []
        for k in sorted(set(x) & set(y), key=lambda k: (k[0], k[1])):
            if only_days_le and k[1] > only_days_le:
                continue
            if any(x[k][f] != y[k][f] for f in fields) or \
                    round(float(x[k]["mention_score"]), 9) != round(float(y[k]["mention_score"]), 9):
                out.append(k)
        return out

    alias_cells = moved(d_old, d_new, DAILY_FIELDS)
    drift_cells = moved(d_srv, d_old, DAILY_FIELDS, only_days_le=srv_end)
    print("ALIAS: (security, day) cells whose counts move new vs old = %d of %d" % (len(alias_cells), len(d_new)))
    for k in alias_cells:
        o, n = d_old[k], d_new[k]
        print("  ALIAS cell %-22s %s  " % (k[0], k[1]) + "  ".join(
            "%s %s->%s" % (f, o[f], n[f]) for f in DAILY_FIELDS if o[f] != n[f]) +
            ("  mention_score %.1f->%.1f" % (o["mention_score"], n["mention_score"]) if o["mention_score"] != n["mention_score"] else ""))
    print("ALIAS: derived window fields (trailing/baseline/cumulative) that move new vs old = %d cells (cascade of the base cells above)" %
          len(moved(d_old, d_new, DAILY_DERIVED)))
    print("DRIFT: cells moved old vs served on days <= %s = %d of %d" % (srv_end, len(drift_cells), len(d_srv)))
    by_sec = {}
    for k in drift_cells:
        by_sec.setdefault(k[0], []).append(k[1])
    for s, ds in sorted(by_sec.items()):
        print("  DRIFT %-22s %d cells, days %s .. %s" % (s, len(ds), min(ds), max(ds)))

    # ---- (d) event ----------------------------------------------------------------------------
    print("\n== (d) chatter_event ==")
    ev_srv = served[pg.GOLD_EVENT_TABLE][1]
    ev_old = pg.event_rows(rows_old)
    ev_new = pg.event_rows(rows_new)
    print("events served=%d old=%d new=%d   event_id unique: served %s old %s new %s" % (
        len(ev_srv), len(ev_old), len(ev_new),
        len({e['event_id'] for e in ev_srv}) == len(ev_srv), len({e['event_id'] for e in ev_old}) == len(ev_old),
        len({e['event_id'] for e in ev_new}) == len(ev_new)))
    unique_ok = len({e["event_id"] for e in ev_new}) == len(ev_new)
    e_old = {e["event_id"]: e for e in ev_old}
    e_new = {e["event_id"]: e for e in ev_new}
    def members(e, source_rows):
        """The event's member rows AS GRADED in `source_rows` (the build that produced the event)."""
        by_pair = {pair(r): r for r in source_rows}
        return [by_pair[(k, e["security_key"])] for k in e["article_keys"]]

    def brief(e):
        return "%s %s..%s days=%s articles=%s A=%s B=%s pubs=%s lead=%s | %s" % (
            e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"], e["tier_a"],
            e["tier_b"], e["publishers_distinct"], e["lead_article_key"], a(e.get("lead_headline"), 90))

    print("\nEVERY SERVED EVENT and its fate (KEPT = same id AND same member list):")
    fates = {}
    for e in sorted(ev_srv, key=lambda e: (e["security_key"], e["first_day"])):
        eid = e["event_id"]
        in_old, in_new = e_old.get(eid), e_new.get(eid)
        if in_new and list(in_new["article_keys"]) == list(e["article_keys"]):
            fate = "KEPT (same span, lead and members)"
            if not in_old:
                fate += " -- but ABSENT from the OLD build: DRIFT moved it, the alias change restored it"
        else:
            same_sec = [x for x in ev_new if x["security_key"] == e["security_key"]
                        and x["first_day"] <= e["last_day"] and x["last_day"] >= e["first_day"]]
            cause = "ALIAS" if in_old and list(in_old["article_keys"]) == list(e["article_keys"]) else "DRIFT"
            if in_new:
                added = sorted(set(in_new["article_keys"]) - set(e["article_keys"]))
                dropped = sorted(set(e["article_keys"]) - set(in_new["article_keys"]))
                fate = "MEMBERS CHANGED (%s): +%s -%s" % (cause, added, dropped)
            elif same_sec:
                fate = "RE-CUT (%s) into: %s" % (cause, "; ".join(brief(x) for x in same_sec))
            else:
                fate = "LOST (%s): no new event on %s overlaps its span" % (cause, e["security_key"])
        fates[eid] = fate
        print("  SERVED %s" % brief(e))
        print("     FATE: %s" % fate)
    print("served events with a named fate: %d of %d" % (len(fates), len(ev_srv)))
    if len(fates) != len(ev_srv):
        problems.append("a served event has no fate")

    new_only = [e for e in ev_new if e["event_id"] not in {x["event_id"] for x in ev_srv}]
    print("\nEVERY NEW EVENT (in the new build, not served): %d" % len(new_only))
    amzn_new_events = []
    for e in new_only:
        origin = "DRIFT (also in the OLD build)" if e["event_id"] in e_old else "ALIAS (not in the OLD build)"
        if e["security_key"] == AMZN:
            amzn_new_events.append(e)
        print("  NEW EVENT [%s] %s" % (origin, brief(e)))
        mem = members(e, rows_new)
        tier_a_pubs = sorted({pg._row_publisher(r) for r in mem if r["signal_tier"] == "A"})
        print("     span %s..%s days=%d articles=%d tier-A publishers=%s lead=%s" % (
            e["first_day"], e["last_day"], e["days_span"], e["articles_total"], tier_a_pubs, e["lead_article_key"]))
        for r in mem:
            print("       %s %-4s tier=%s %-34s %s" % (day(r), pg._row_publisher(r), r["signal_tier"], r["article_key"], a(r.get("title"), 100)))
    print("removed vs OLD build by the alias change: %s" % sorted(set(e_old) - set(e_new)))

    # ---- (e) Z-W40-S1 -------------------------------------------------------------------------
    print("\n== (e) row AMGT_HARVST-Z-W40-S1: the name-detection step over AMZN ==")
    amzn_rows = [r for r in rows_new if r["security_key"] == AMZN and r["signal_tier"] in ("A", "B")]
    ordered = sorted(amzn_rows, key=pg._event_sort_key)
    stems = [pg._story_tokens(r.get("title")) for r in ordered]
    days = [day(r) for r in ordered]
    tier_a_idx = [i for i, r in enumerate(ordered) if r["signal_tier"] == "A"]
    titled = [i for i in tier_a_idx if stems[i]]
    names = pg._security_name_tokens([(stems[i], days[i]) for i in tier_a_idx])
    print("AMZN tier A/B rows (new)=%d ; tier-A rows=%d ; titled tier-A=%d (sample floor %d, name floor: >=%d/%d of them on >=%d days)" % (
        len(ordered), len(tier_a_idx), len(titled), pg._STORY_NAME_MIN_SAMPLE, pg._STORY_NAME_SHARE_NUM,
        pg._STORY_NAME_SHARE_DEN, pg._STORY_NAME_MIN_DAYS))
    print("tokens the name-detection step STRIPS for AMZN = %s" % (sorted(names) if names is not None else "None (sample under the floor: nothing is stripped)"))
    stripped_note = []
    for i in tier_a_idx:
        r = ordered[i]
        terms = pg._story_terms(stems[i], names)
        stripped_note.append((r["article_key"], sorted(stems[i]), sorted(terms)))
        print("  tier-A %s %-4s %-34s stems=%s -> terms after strip=%s | %s" % (
            days[i], pg._row_publisher(r), r["article_key"], sorted(stems[i]), sorted(terms), a(r.get("title"), 70)))
    stories = pg._security_stories(amzn_rows)
    crash_keys = {p[0] for p in crash_pairs}
    print("AMZN stories (%d): %s" % (len(stories), [[r["article_key"] for r in s] for s in stories]))
    in_event = {k for e in [x for x in ev_new if x["security_key"] == AMZN] for k in e["article_keys"]}
    crash_in_event = sorted(crash_keys & in_event)
    print("AMZN crash-pattern articles (tier of any kind) = %d ; of them in an AMZN event = %d : %s" % (
        len(crash_keys), len(crash_in_event), crash_in_event))
    survives = bool(amzn_new_events) and len(crash_in_event) >= 2
    print("the crash burst SURVIVES the name-detection step: %s" % survives)
    if not survives:
        problems.append("Z-W40-S1: the AMZN crash burst does not form an event after the alias change (BLOCKING row, not a fix here)")

    print("\n== VERDICT ==")
    for label, res in (("(a) printed", True), ("(b) printed", True), ("(c) printed", True), ("(d) printed", True),
                       ("(e) printed", True), ("every served event's fate named", len(fates) == len(ev_srv)),
                       ("every new-build event_id unique", unique_ok),
                       ("a NEW AMZN event exists", bool(amzn_new_events)),
                       ("alias change is additive (removed 0 pairs)", not alias_removed)):
        print("CHECK %-44s %s" % (label, "PASS" if res else "FAIL"))
        if not res:
            problems.append(label)
    for p in problems:
        print("PROBLEM: %s" % p)
    print("AC2 %s" % ("PASS" if not problems else "FAIL"))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
