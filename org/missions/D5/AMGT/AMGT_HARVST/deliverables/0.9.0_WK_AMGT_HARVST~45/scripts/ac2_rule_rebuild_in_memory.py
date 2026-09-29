"""HVST-g-1 AC2: the alias-rule rebuild, IN MEMORY, over today's silver -- OLD aliases (the served securities
file) vs NEW (this cell's securities file), set beside the SERVED newest parts. Every moved row is attributed
ALIAS (new vs old, same silver, same code) or DRIFT (old vs served: the silver has grown or the range extends).
S3 GET/LIST only: no put, no delete, no vendor call."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402

MENTION_KEY = lambda r: (r["article_key"], r["security_key"])  # noqa: E731
DAILY_KEY = lambda r: (r["security_key"], r["day"])  # noqa: E731


def attribution(s, o, n):
    """ALIAS / DRIFT / ALIAS+DRIFT for a key whose served (s), old-rebuild (o) and new-rebuild (n) rows are given
    (None = absent). Only called when s != n."""
    same = lambda x, y: C.canon(x) == C.canon(y)  # noqa: E731
    if same(s, o):
        return "ALIAS"
    if same(n, o):
        return "DRIFT"
    return "ALIAS+DRIFT"


def main():
    problems = []
    old_sec = C.load_json(C.OLD_PATH)
    new_sec = C.load_json(C.NEW_PATH)
    old_by, new_by = C.sec_map(old_sec), C.sec_map(new_sec)
    brands = C.brand_forms_by_security()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    articles, hits, served = C.fetch()
    title_of = {x["article_key"]: x.get("title") for x in articles}
    print("== HVST-g-1 AC2: the alias-rule rebuild in memory (OLD vs NEW aliases, beside the SERVED newest parts) ==")
    print("OLD securities: %s  (%d securities)" % (os.path.relpath(C.OLD_PATH, C.REPO), len(old_sec)))
    print("NEW securities: %s  (%d securities)" % (os.path.relpath(C.NEW_PATH, C.REPO), len(new_sec)))
    print("silver articles (denominator)=%d  listing_hit rows=%d  as_of=%s" % (len(articles), len(hits), as_of))
    for t in (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE):
        key, parts, rows = served[t]
        print("SERVED newest %-26s %s  (parts=%d, rows=%d)" % (t, key, parts, len(rows)))
    if set(old_by) != set(new_by):
        problems.append("securities differ in KEY SET between old and new: %s" % sorted(set(old_by) ^ set(new_by)))
    changed_aliases = [k for k in new_by if new_by[k].get("aliases") != old_by.get(k, {}).get("aliases")]
    print("securities whose alias list differs old->new: %d of %d; whose ticker_aliases differ: %d of %d" % (
        len(changed_aliases), len(new_sec), sum(1 for k in new_by if (new_by[k].get("ticker_aliases") or []) != (old_by.get(k, {}).get("ticker_aliases") or [])), len(new_sec)))

    old_t, old_enriched = C.build_memory(old_sec, articles, hits, as_of)
    new_t, new_enriched = C.build_memory(new_sec, articles, hits, as_of)
    S = {t: served[t][2] for t in served}

    # ============================ (a) article_security_mention ==========================================
    print("\n== (a) article_security_mention ==")
    s_m = {MENTION_KEY(r): r for r in S[pg.GOLD_TABLE]}
    o_m = {MENTION_KEY(r): r for r in old_t[pg.GOLD_TABLE]}
    n_m = {MENTION_KEY(r): r for r in new_t[pg.GOLD_TABLE]}
    print("rows: served=%d  old-rebuild=%d  new-rebuild=%d   (denominators: %d securities x %d articles = %d pairs scanned)" % (
        len(s_m), len(o_m), len(n_m), len(new_sec), len(articles), len(new_sec) * len(articles)))
    drift_rows = [k for k in set(s_m) | set(o_m) if C.canon(s_m.get(k)) != C.canon(o_m.get(k))]
    print("DRIFT (old-rebuild vs served, same aliases): %d rows differ (silver grown since the served build, or the tail of a moved row)" % len(drift_rows))

    # span-level attribution: per FORM and per SECURITY
    by_form, by_sec = {}, {}
    added_by_pair = {}
    lost_total = 0
    for art in articles:
        for key, nsec in new_by.items():
            osec = old_by.get(key)
            if osec is None:
                continue
            add, lost = C.added_spans(art, osec, nsec, brands)
            lost_total += len(lost)
            if lost:
                problems.append("LOST spans for %s / %s: %s" % (art["article_key"], key, lost))
            if not add:
                continue
            added_by_pair[(art["article_key"], key)] = add
            for sp in add:
                f = by_form.setdefault((sp["class"], sp["form"]), {"spans": 0, "pairs": set(), "secs": set()})
                f["spans"] += 1
                f["pairs"].add((art["article_key"], key))
                f["secs"].add(key)
                g = by_sec.setdefault(key, {"spans": 0, "pairs": set(), "forms": {}})
                g["spans"] += 1
                g["pairs"].add((art["article_key"], key))
                g["forms"][sp["form"]] = g["forms"].get(sp["form"], 0) + 1
    total_added = sum(len(v) for v in added_by_pair.values())
    delta_count = sum((n_m[k]["mention_count"] if k in n_m else 0) - (o_m[k]["mention_count"] if k in o_m else 0)
                      for k in set(n_m) | set(o_m))
    new_pairs = [k for k in added_by_pair if k not in o_m]
    print("ADDED MENTIONS (new alias spans the old set did not find): %d spans across %d (article, security) pairs, of which %d are NEW pairs "
          "(the security had 0 mentions in the article under the old aliases); lost spans=%d" % (
              total_added, len(added_by_pair), len(new_pairs), lost_total))
    print("cross-check: sum of mention_count(new) - mention_count(old) over the rebuilt rows = %d; added spans - lost spans = %d  -> %s" % (
        delta_count, total_added - lost_total, "OK" if delta_count == total_added - lost_total else "MISMATCH"))
    if delta_count != total_added - lost_total:
        problems.append("span accounting does not reconcile with mention_count delta")
    print("\n-- per FORM (class, form): added mentions | pairs | securities  [denominator: %d added mentions, %d forms] --" % (
        total_added, len(by_form)))
    for (cls, form), f in sorted(by_form.items(), key=lambda kv: (-kv[1]["spans"], kv[0])):
        print("  %-12s %-10s spans=%-4d pairs=%-4d securities=%s" % (cls, a_(form), f["spans"], len(f["pairs"]), ",".join(sorted(f["secs"]))))
    cls_tot = {}
    for (cls, _f), f in by_form.items():
        cls_tot[cls] = cls_tot.get(cls, 0) + f["spans"]
    print("  by class: %s" % ", ".join("%s=%d" % kv for kv in sorted(cls_tot.items())))
    print("\n-- per SECURITY: added mentions | pairs | forms  [denominator: %d added mentions across %d securities of %d] --" % (
        total_added, len(by_sec), len(new_sec)))
    for key, g in sorted(by_sec.items(), key=lambda kv: (-kv[1]["spans"], kv[0])):
        print("  %-22s spans=%-4d pairs=%-4d forms=%s" % (key, g["spans"], len(g["pairs"]),
                                                          ", ".join("%s x%d" % (f, c) for f, c in sorted(g["forms"].items()))))

    print("\n-- every mention row ADDED or CHANGED, served -> new (attribution against the old rebuild) --")
    moved = sorted(k for k in set(s_m) | set(n_m) if C.canon(s_m.get(k)) != C.canon(n_m.get(k)))
    flips_title = flips_lead = tier_changes = 0
    counts = {"ALIAS": 0, "DRIFT": 0, "ALIAS+DRIFT": 0}
    for k in moved:
        s, o, n = s_m.get(k), o_m.get(k), n_m.get(k)
        att = attribution(s, o, n)
        counts[att] += 1
        head = C.a(title_of.get(k[0]), 90)
        forms = ",".join(sorted({"%s:%s" % (sp["class"], sp["form"]) for sp in added_by_pair.get(k, [])})) or "-"
        if n is None:
            desc = "REMOVED (served row absent from the new rebuild)"
        elif s is None:
            desc = "ADDED tier=%s title=%s lead=%s count=%s" % (n["signal_tier"], n["mention_in_title"], n["mention_in_lead"], n["mention_count"])
        else:
            fields = C.diff_fields(s, n)
            bits = []
            for f in ("signal_tier", "mention_in_title", "mention_in_lead", "mention_count", "match_forms", "co_mentioned_securities"):
                if f in fields:
                    bits.append("%s %s->%s" % (f, C.canon(s[f]), C.canon(n[f])))
            desc = "CHANGED fields=%s | %s" % (fields, "; ".join(bits))
        print("  [%s] %s | %s | forms hit: %s | %s" % (att, k[1], head, forms, desc))
        for sp in added_by_pair.get(k, []):
            print("        + %s '%s' in %s at %d: %s" % (sp["class"], C.a(sp["matched"]), sp["where"], sp["offset"],
                                                         C.context(sp["text"], sp["offset"], sp["end"])))
    print("moved mention rows (served vs new): %d  -> ALIAS=%d DRIFT=%d ALIAS+DRIFT=%d  [denominator: %d served rows, %d new rows]" % (
        len(moved), counts["ALIAS"], counts["DRIFT"], counts["ALIAS+DRIFT"], len(s_m), len(n_m)))
    for k in n_m:
        o, n = o_m.get(k), n_m[k]
        if C.canon(o) == C.canon(n):
            continue
        flips_title += int(n["mention_in_title"] and (o is None or not o["mention_in_title"]))
        flips_lead += int(n["mention_in_lead"] and (o is None or not o["mention_in_lead"]))
        tier_changes += int(o is not None and o["signal_tier"] != n["signal_tier"])
    print("title/lead flips old-rebuild -> new (a NEW pair counts as a flip when the new row has the flag): title flips=%d lead flips=%d tier changes on existing rows=%d" % (
        flips_title, flips_lead, tier_changes))

    # ============================ (b) chatter_daily =====================================================
    print("\n== (b) chatter_daily ==")
    s_d = {DAILY_KEY(r): r for r in S[pg.GOLD_DAILY_TABLE]}
    o_d = {DAILY_KEY(r): r for r in old_t[pg.GOLD_DAILY_TABLE]}
    n_d = {DAILY_KEY(r): r for r in new_t[pg.GOLD_DAILY_TABLE]}
    srv_end = max(k[1] for k in s_d)
    print("cells: served=%d (last day %s)  old-rebuild=%d  new-rebuild=%d  [denominator: %d securities x days]" % (
        len(s_d), srv_end, len(o_d), len(n_d), len(new_sec)))
    alias_cells, drift_cells = {}, {}
    cols_alias = {}
    for k in set(n_d) | set(o_d):
        if C.canon(n_d.get(k)) != C.canon(o_d.get(k)):
            alias_cells.setdefault(k[0], []).append(k[1])
            for f in C.diff_fields(o_d.get(k), n_d.get(k)) or ["(cell absent)"]:
                cols_alias[f] = cols_alias.get(f, 0) + 1
    ext = 0
    for k in set(o_d) | set(s_d):
        if C.canon(o_d.get(k)) != C.canon(s_d.get(k)):
            drift_cells.setdefault(k[0], []).append(k[1])
            if k not in s_d and k[1] > srv_end:
                ext += 1
    print("ALIAS moved cells (new vs old): %d cells across %d securities; columns moved: %s" % (
        sum(len(v) for v in alias_cells.values()), len(alias_cells), dict(sorted(cols_alias.items()))))
    print("DRIFT cells (old-rebuild vs served): %d cells across %d securities (of which %d are extension days after the served last day %s)" % (
        sum(len(v) for v in drift_cells.values()), len(drift_cells), ext, srv_end))
    print("-- per security the cells that move, new vs old (ALIAS): count, first..last day, columns --")
    for sec in sorted(alias_cells, key=lambda s: (-len(alias_cells[s]), s)):
        days = sorted(alias_cells[sec])
        cols = set()
        for d in days:
            cols.update(C.diff_fields(o_d.get((sec, d)), n_d.get((sec, d))) or [])
        print("  %-22s cells=%-4d %s..%s columns=%s   (DRIFT cells for this security: %d)" % (
            sec, len(days), days[0], days[-1], sorted(cols), len(drift_cells.get(sec, []))))
    print("securities with DRIFT cells but no ALIAS cells: %d" % len([s for s in drift_cells if s not in alias_cells]))
    moved_daily = [k for k in set(s_d) | set(n_d) if C.canon(s_d.get(k)) != C.canon(n_d.get(k))]
    att_d = {"ALIAS": 0, "DRIFT": 0, "ALIAS+DRIFT": 0}
    for k in moved_daily:
        att_d[attribution(s_d.get(k), o_d.get(k), n_d.get(k))] += 1
    print("moved daily cells (served vs new): %d -> ALIAS=%d DRIFT=%d ALIAS+DRIFT=%d" % (
        len(moved_daily), att_d["ALIAS"], att_d["DRIFT"], att_d["ALIAS+DRIFT"]))

    # ============================ (c) chatter_event =====================================================
    print("\n== (c) chatter_event ==")
    s_e = {r["event_id"]: r for r in S[pg.GOLD_EVENT_TABLE]}
    o_e = {r["event_id"]: r for r in old_t[pg.GOLD_EVENT_TABLE]}
    n_e = {r["event_id"]: r for r in new_t[pg.GOLD_EVENT_TABLE]}
    print("events: served=%d  old-rebuild=%d  new-rebuild=%d" % (len(s_e), len(o_e), len(n_e)))
    fates = {"KEPT": 0, "MOVED": 0, "GONE": 0}
    for eid in sorted(s_e, key=lambda i: (s_e[i]["security_key"], s_e[i]["first_day"], i)):
        s = s_e[eid]
        if eid not in n_e:
            fate = "GONE"
            recut = [x for x in n_e.values() if x["security_key"] == s["security_key"]
                     and x["first_day"] <= s["last_day"] and x["last_day"] >= s["first_day"]]
            extra = " (re-cut as %s)" % ", ".join(x["event_id"][:12] for x in recut) if recut else " (no overlapping event for the security)"
        else:
            fields = C.diff_fields(s, n_e[eid])
            fate, extra = ("MOVED", " fields=%s" % fields) if fields else ("KEPT", "")
        fates[fate] += 1
        o_fate = "in old-rebuild row-equal" if eid in o_e and not C.diff_fields(s, o_e[eid]) else (
            "in old-rebuild but differs" if eid in o_e else "absent from old-rebuild (DRIFT)")
        print("  SERVED %-5s %-20s %s..%s articles=%d id=%s%s | %s" % (
            fate, s["security_key"], s["first_day"], s["last_day"], s["articles_total"], eid[:12], extra, o_fate))
        print("        lead: %s" % C.a(s["lead_headline"], 110))
    print("served events: %d -> KEPT=%d MOVED=%d GONE=%d  (every served event's fate is named above: %s)" % (
        len(s_e), fates["KEPT"], fates["MOVED"], fates["GONE"], "YES" if sum(fates.values()) == len(s_e) else "NO"))
    if sum(fates.values()) != len(s_e):
        problems.append("a served event has no fate")
    new_events = sorted((n_e[i] for i in n_e if i not in s_e), key=lambda e: (e["security_key"], e["first_day"], e["event_id"]))
    print("NEW events (in the new rebuild, not served): %d" % len(new_events))
    for e in new_events:
        att = "ALIAS+DRIFT" if e["event_id"] in o_e else "ALIAS"
        att = "DRIFT" if (e["event_id"] in o_e) else att
        print("  NEW [%s] %s span %s..%s (days_span=%d) articles=%d tier_a=%d tier_b=%d publishers=%d id=%s" % (
            att, e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"], e["tier_a"],
            e["tier_b"], e["publishers_distinct"], e["event_id"][:12]))
        print("      lead article %s: %s" % (e["lead_article_key"], C.a(e["lead_headline"], 120)))
        for ak in e["article_keys"]:
            print("      - %s | %s" % (ak, C.a(title_of.get(ak), 120)))
    # events of the OLD rebuild that the new one drops or re-cuts (an alias-rule effect, not served)
    lost_old = [i for i in o_e if i not in n_e]
    print("events in the old rebuild that the new rebuild does not carry: %d %s" % (len(lost_old), [i[:12] for i in lost_old]))

    # ============================ (d) Z-W44-S1 re-read ==================================================
    print("\n== (d) Z-W44-S1 re-read: per security the name stems stripped (old vs new rebuild) ==")

    def name_stems(enriched):
        by = {}
        for r in enriched:
            if r.get("signal_tier") in pg._EVENT_QUALIFYING_TIERS and pg._day_of(r.get("published_utc")) is not None:
                by.setdefault(r["security_key"], []).append(r)
        out = {}
        for key, rows in by.items():
            ordered = sorted(rows, key=pg._event_sort_key)
            tier_a = [(pg._story_tokens(r.get("title")), pg._day_of(r.get("published_utc")))
                      for r in ordered if r.get("signal_tier") == "A"]
            names = pg._security_name_tokens(tier_a, pg._alias_stems(ordered))
            out[key] = (None if names is None else sorted(names), len(tier_a), len(ordered))
        return out

    o_n, n_n = name_stems(old_enriched), name_stems(new_enriched)
    keys = sorted(set(o_n) | set(n_n))
    changed = fresh = 0
    print("securities with tier-A/B rows: old-rebuild=%d new-rebuild=%d (union %d) [denominator: %d securities]" % (
        len(o_n), len(n_n), len(keys), len(new_sec)))
    for key in keys:
        o_s, n_s = o_n.get(key), n_n.get(key)
        if o_s is None:
            verdict = "NEW-SECURITY (no tier-A/B row under the old aliases; no old stems to compare)"
            fresh += 1
        elif n_s is not None and o_s[0] == n_s[0]:
            verdict = "same"
        else:
            verdict = "CHANGED"
            changed += 1
        print("  %-22s tierA/AB rows old=%s new=%s | stems stripped old=%s new=%s | %s" % (
            key, "%s/%s" % (o_s[1], o_s[2]) if o_s else "-", "%s/%s" % (n_s[1], n_s[2]) if n_s else "-",
            o_s[0] if o_s else "(no rows)", n_s[0] if n_s else "(no rows)", verdict))
    print("securities whose stripped name stems CHANGED old->new: %d of %d with rows under the old aliases (%d more securities gained tier-A/B rows and have no old stems)" % (
        changed, len(o_n), fresh))

    # ============================ (e) event ids unique ==================================================
    print("\n== (e) event_id uniqueness ==")
    for label, rows in (("served", S[pg.GOLD_EVENT_TABLE]), ("old-rebuild", old_t[pg.GOLD_EVENT_TABLE]),
                        ("new-rebuild", new_t[pg.GOLD_EVENT_TABLE])):
        ids = [r["event_id"] for r in rows]
        ok = len(ids) == len(set(ids))
        print("  %-12s events=%d distinct ids=%d -> %s" % (label, len(ids), len(set(ids)), "UNIQUE" if ok else "DUPLICATE"))
        if not ok:
            problems.append("event_id not unique in %s" % label)
    for label, rows, d in (("served", S[pg.GOLD_TABLE], s_m), ("old-rebuild", old_t[pg.GOLD_TABLE], o_m),
                           ("new-rebuild", new_t[pg.GOLD_TABLE], n_m)):
        ok = len(rows) == len(d)
        print("  %-12s mention rows=%d distinct (article, security) pairs=%d -> %s" % (label, len(rows), len(d), "UNIQUE" if ok else "DUPLICATE"))
        if not ok:
            problems.append("mention pair not unique in %s" % label)

    print("\nSUMMARY (a)-(e) all printed; served event fates named: %s; problems: %d" % (
        "YES" if sum(fates.values()) == len(s_e) else "NO", len(problems)))
    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    print("AC2 RESULT: %s" % ("PASS" if not problems else "FAIL"))
    return 0 if not problems else 1


def a_(x):
    return C.a(x)


if __name__ == "__main__":
    sys.exit(main())
