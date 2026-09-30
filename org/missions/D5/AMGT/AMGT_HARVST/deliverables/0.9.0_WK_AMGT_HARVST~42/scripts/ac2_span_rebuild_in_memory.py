"""HVST-e-1 AC2: the span-count change proved IN MEMORY over today's silver with the pinned securities.
OLD matcher (CLOUD base b8c8214ce5, via git show) vs NEW matcher (worktree), set beside the SERVED newest
snapshots. Every moved row is attributed SPAN (new vs old) or DRIFT (old vs served). S3 GET/LIST only."""
import collections
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402

NEW = C.NEW
MENTION_WATCH = ("mention_count", "signal_tier", "signal_weight", "match_forms")
STRUCT = ("mention_in_title", "mention_in_lead", "blocks_hit", "first_mention_block", "blocks_total")
DIRECT = ("articles_total", "tier_a", "tier_b", "tier_c", "tier_d", "mention_score", "mention_count_total")
NEVER_MOVES = ("articles_total", "publishers_distinct", "data_status", "publishers_covered", "publishers_enabled",
               "first_published_utc", "last_published_utc", "tier_a", "tier_b")


def index(rows, table):
    kf = C.KEYS[table]
    d = {kf(r): C.canon_row(r) for r in rows}
    return d, len(d) != len(rows)


def main():
    client = C.store._default_client()
    served, newest = {}, {}
    print("== INPUTS ==")
    print("securities (pinned, READ ONLY): %s" % C.SECURITIES.split("deliverables/")[-1])
    print("OLD matcher = %s:%s   NEW matcher = worktree %s" % (C.BASE, C.MODULE_PATH, C.MODULE_PATH))
    for t in C.TABLES:
        newest[t] = C.parts(t, client)[-1]
        served[t] = NEW._latest_gold_snapshot_rows(t, client=client)
        print("served newest %-26s %s ETag=%s rows=%d" % (t, C.short(newest[t][0]), newest[t][1], len(served[t])))
    securities = C.load_securities()
    articles, title_of, hits = C.read_inputs(client)
    srv_daily_end = max(r["day"] for r in served[NEW.GOLD_DAILY_TABLE])
    as_of = srv_daily_end
    print("securities=%d  silver articles=%d  listing hits=%d" % (len(securities), len(articles), len(hits)))
    print("in-memory daily day range ends at the served daily table's last day = %s (served part as-of %s)" % (
        as_of, NEW._DATE_PARTITION_RE.search(newest[NEW.GOLD_DAILY_TABLE][0]).group(1)))
    old_mod = C.load_old_module()
    old = C.memory(old_mod, securities, articles, title_of, hits, as_of)
    new = C.memory(NEW, securities, articles, title_of, hits, as_of)
    fails = []

    # ------------------------------------------------------------------ (a) mention
    t = NEW.GOLD_TABLE
    s, sd = index(served[t], t)
    o, od = index(old[t], t)
    n, nd = index(new[t], t)
    print("\n== (a) article_security_mention ==")
    print("rows: served=%d old=%d new=%d  duplicate keys served/old/new=%s/%s/%s" % (len(s), len(o), len(n), sd, od, nd))
    added = sorted(set(n) - set(o))
    removed = sorted(set(o) - set(n))
    print("rows ADDED by the span change=%d  REMOVED by the span change=%d" % (len(added), len(removed)))
    if added or removed or sd or od or nd:
        fails.append("(a) rows added/removed/duplicated")
    drift_keys = set(s) ^ set(o)
    drift_rows = [(k, C.diff_fields(s[k], o[k])) for k in sorted(set(s) & set(o)) if C.diff_fields(s[k], o[k])]
    print("DRIFT (old matcher vs served): keys only in one side=%d  rows with any field different=%d" % (
        len(drift_keys), len(drift_rows)))
    for k in sorted(drift_keys):
        print("  DRIFT key only in %s: %s" % ("served" if k in s else "old", k))
    for k, f in drift_rows:
        print("  DRIFT %s fields=%s" % (k, f))
    moved = [(k, C.diff_fields(o[k], n[k])) for k in sorted(set(o) & set(n)) if C.diff_fields(o[k], n[k])]
    print("SPAN (new matcher vs old): rows with any field different=%d of %d" % (len(moved), len(n)))
    field_hist = collections.Counter(f for _k, fs in moved for f in fs)
    print("fields moved (row counts): %s" % dict(sorted(field_hist.items())))
    other = {f: c for f, c in field_hist.items() if f not in MENTION_WATCH}
    print("fields moved OTHER than mention_count/signal_tier/signal_weight/match_forms: %s" % (other or "none"))
    struct_moved = {f: sum(1 for k, fs in moved if f in fs) for f in STRUCT}
    print("title/lead/blocks_hit moves: mention_in_title=%d mention_in_lead=%d blocks_hit=%d (also first_mention_block=%d blocks_total=%d)" % (
        struct_moved["mention_in_title"], struct_moved["mention_in_lead"], struct_moved["blocks_hit"],
        struct_moved["first_mention_block"], struct_moved["blocks_total"]))
    if struct_moved["mention_in_title"] or struct_moved["mention_in_lead"] or struct_moved["blocks_hit"]:
        fails.append("(a) title/lead/blocks_hit moved")
    print("\nevery moved row (security | article | field: old -> new | attribution | headline):")
    per_sec = collections.OrderedDict()
    for k, fs in moved:
        art, sec = k
        attribution = "SPAN"
        if k in s and C.diff_fields(s[k], o[k]):
            attribution += "+DRIFT(old!=served on %s)" % C.diff_fields(s[k], o[k])
        elif k not in s:
            attribution += "+DRIFT(not served)"
        vals = "; ".join("%s: %r -> %r" % (f, o[k][f], n[k][f]) for f in fs)
        print("  %s | %s | %s | %s | %s" % (sec, art, vals, attribution, C.a(title_of.get(art), 90)))
        rec = per_sec.setdefault(sec, {"count_moved": 0, "tier_moved": 0, "tiers": collections.Counter()})
        rec["count_moved"] += "mention_count" in fs
        if "signal_tier" in fs:
            rec["tier_moved"] += 1
            rec["tiers"]["%s->%s" % (o[k]["signal_tier"], n[k]["signal_tier"])] += 1
    print("\nPER-SECURITY (rows whose mention_count moves | rows whose tier moves | tier moves):")
    for sec in sorted(per_sec):
        r = per_sec[sec]
        print("  %-16s mention_count moved=%d  tier moved=%d  %s" % (sec, r["count_moved"], r["tier_moved"], dict(r["tiers"])))
    tot_count = sum(r["count_moved"] for r in per_sec.values())
    tot_tier = sum(r["tier_moved"] for r in per_sec.values())
    print("TOTAL: mention_count moved on %d of %d rows across %d securities; tier moved on %d rows" % (
        tot_count, len(n), len(per_sec), tot_tier))
    print("tier-move mix: %s" % dict(collections.Counter(
        "%s->%s" % (o[k]["signal_tier"], n[k]["signal_tier"]) for k, fs in moved if "signal_tier" in fs)))
    ab_moved = [k for k, fs in moved if n[k]["signal_tier"] in ("A", "B") or o[k]["signal_tier"] in ("A", "B")]
    print("moved rows touching tier A or B (old or new): %d" % len(ab_moved))

    # ------------------------------------------------------------------ (b) daily
    t = NEW.GOLD_DAILY_TABLE
    s, sd = index(served[t], t)
    o, od = index(old[t], t)
    n, nd = index(new[t], t)
    print("\n== (b) chatter_daily (as-of %s; served last day %s) ==" % (as_of, srv_daily_end))
    print("cells: served=%d old=%d new=%d  duplicate keys=%s/%s/%s  keys only-in-one-side old-vs-new=%d served-vs-new=%d" % (
        len(s), len(o), len(n), sd, od, nd, len(set(o) ^ set(n)), len(set(s) ^ set(n))))
    if set(o) ^ set(n):
        fails.append("(b) cell keys differ old vs new")
    span_cells = [(k, C.diff_fields(o[k], n[k])) for k in sorted(set(o) & set(n)) if C.diff_fields(o[k], n[k])]
    drift_cells = [(k, C.diff_fields(s[k], o[k])) for k in sorted(set(s) & set(o)) if C.diff_fields(s[k], o[k])]
    print("DRIFT cells (old matcher vs served): %d" % len(drift_cells))
    dcols = collections.Counter(f for _k, fs in drift_cells for f in fs)
    print("  drift columns: %s" % dict(sorted(dcols.items())))
    dsec = collections.Counter(k[0] for k, _fs in drift_cells)
    print("  drift cells per security: %s" % dict(sorted(dsec.items())))
    for k, fs in drift_cells[:60]:
        print("  DRIFT %s %s cols=%s" % (k[0], k[1], fs))
    if len(drift_cells) > 60:
        print("  ... %d more DRIFT cells not listed (per-security counts above)" % (len(drift_cells) - 60))
    print("SPAN cells (new matcher vs old): %d of %d" % (len(span_cells), len(n)))
    scols = collections.Counter(f for _k, fs in span_cells for f in fs)
    print("  span columns (cell counts): %s" % dict(sorted(scols.items())))
    ssec = collections.defaultdict(list)
    for k, fs in span_cells:
        ssec[k[0]].append((k[1], fs))
    for sec in sorted(ssec):
        cells = ssec[sec]
        print("  %s: %d cells, days %s..%s" % (sec, len(cells), cells[0][0], cells[-1][0]))
        rolling = []
        for day, fs in cells:
            direct = [f for f in fs if f in DIRECT]
            if direct:
                print("    %s DIRECT cols: %s | also moves %s" % (
                    day, "; ".join("%s: %r -> %r" % (f, o[(sec, day)][f], n[(sec, day)][f]) for f in direct),
                    [f for f in fs if f not in DIRECT]))
            else:
                rolling.append(day)
        if rolling:
            print("    %d further cells move only through trailing/baseline/cumulative windows (first %s, last %s)" % (
                len(rolling), rolling[0], rolling[-1]))
    for k, fs in span_cells:
        bad = [f for f in fs if f in NEVER_MOVES]
        if bad:
            fails.append("(b) unexpected column moved by the span change: %s %s %s" % (k[0], k[1], bad))
    beyond = [k for k in n if k[1] > srv_daily_end]
    print("cells beyond the served last day in the new build: %d" % len(beyond))

    # ------------------------------------------------------------------ (c) event
    t = NEW.GOLD_EVENT_TABLE
    s, sd = index(served[t], t)
    o, od = index(old[t], t)
    n, nd = index(new[t], t)
    print("\n== (c) chatter_event ==")
    print("events: served=%d old=%d new=%d" % (len(s), len(o), len(n)))
    kept_srv = moved_srv = 0
    for eid in sorted(s):
        e = s[eid]
        if eid not in n:
            moved_srv += 1
            print("  FINDING served event MOVED (id absent in new build): %s %s %s..%s lead=%s" % (
                eid[:12], e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"]))
        elif C.diff_fields(e, n[eid]):
            moved_srv += 1
            print("  FINDING served event MOVED (fields %s): %s %s" % (C.diff_fields(e, n[eid]), eid[:12], e["security_key"]))
        else:
            kept_srv += 1
            print("  KEPT %s %s %s..%s articles=%d lead=%s" % (eid[:12], e["security_key"], e["first_day"], e["last_day"],
                                                             e["articles_total"], e["lead_article_key"]))
    only_new = sorted(set(n) - set(s))
    for eid in only_new:
        e = n[eid]
        print("  FINDING event in the new build and NOT served: %s %s %s..%s lead=%s" % (
            eid[:12], e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"]))
    srv_vs_old = [eid for eid in sorted(set(s) | set(o)) if eid not in s or eid not in o or C.diff_fields(s[eid], o[eid])]
    span_ev = [eid for eid in sorted(set(o) | set(n)) if eid not in o or eid not in n or C.diff_fields(o[eid], n[eid])]
    print("served events KEPT=%d MOVED=%d of %d; new-only=%d" % (kept_srv, moved_srv, len(s), len(only_new)))
    print("DRIFT (old matcher vs served) events differing: %d ; SPAN (new vs old) events differing: %d" % (len(srv_vs_old), len(span_ev)))
    if moved_srv or only_new or span_ev:
        fails.append("(c) an event moved: FINDING")

    # ------------------------------------------------------------------ (d) unique ids
    print("\n== (d) event_id unique ==")
    for label, rows in (("served", served[t]), ("old", old[t]), ("new", new[t])):
        ids = [r["event_id"] for r in rows]
        print("%-6s event_id: %d rows, %d distinct -> %s" % (label, len(ids), len(set(ids)), "UNIQUE" if len(ids) == len(set(ids)) else "NOT UNIQUE"))
        if len(ids) != len(set(ids)):
            fails.append("(d) event_id not unique in %s" % label)

    print()
    for f in fails:
        print("FAIL: %s" % f)
    print("AC2 %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
