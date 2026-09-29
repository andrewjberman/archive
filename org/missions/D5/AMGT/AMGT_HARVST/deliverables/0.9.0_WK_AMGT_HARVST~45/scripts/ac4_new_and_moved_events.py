"""HVST-g-2 AC4 (JUDGMENT -- PRESENTED, NOT GRADED; no verdict is printed or implied). Read-only, S3 LIST/GET only.
(1) Every NEW or MOVED served event (newest chatter_event part vs the part it replaced, recorded by the dry step),
    with security, span, lead, tier-A publishers and every headline. If there are none, that is printed with its
    denominator.
(2) Because the alias rule is what moved: from the SERVED new mention part, every tier-A/B row that is new or newly
    tier-A/B against the replaced part, grouped by the form that matched, with the headline and the words around
    the match, so the CVO has served rows to read."""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    client = G.store._default_client()
    with open(G.BEFORE_JSON, "r", encoding="utf-8") as fh:
        before = json.load(fh)
    parts = G.list_parts(client)
    articles = {r["article_key"]: r for r in pg._iter_latest_articles(client=client)}
    print("== HVST-g-2 AC4 (JUDGMENT: presented, not graded; no verdict) ==")
    print("Question for the CVO at L9: is each event / each added tier-A/B hit ONE story about its own company, and does the lead name that story?")

    # ---------------- (1) events ----------------
    ev_before_key = before["tables"][pg.GOLD_EVENT_TABLE]["newest_key"]
    ev_after_key = parts[pg.GOLD_EVENT_TABLE][-1]["key"]
    b_e = {r["event_id"]: r for r in G.read_rows(client, ev_before_key)}
    a_e = {r["event_id"]: r for r in G.read_rows(client, ev_after_key)}
    new_ids = [i for i in a_e if i not in b_e]
    moved_ids = [i for i in a_e if i in b_e and C.diff_fields(b_e[i], a_e[i])]
    print("\n== (1) NEW or MOVED served events ==")
    print("replaced newest part: %s (%d events)\nnew newest part:      %s (%d events)" % (ev_before_key, len(b_e), ev_after_key, len(a_e)))
    print("denominator: %d events in the new served part; NEW=%d MOVED=%d (kept unchanged=%d); served events gone=%d" % (
        len(a_e), len(new_ids), len(moved_ids), len(a_e) - len(new_ids) - len(moved_ids), len([i for i in b_e if i not in a_e])))
    for label, ids in (("NEW", new_ids), ("MOVED", moved_ids)):
        for i in ids:
            e = a_e[i]
            print("  %s event %s %s span %s..%s (days_span=%d) articles=%d tier_a=%d tier_b=%d publishers=%d" % (
                label, i[:12], e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"], e["tier_a"], e["tier_b"], e["publishers_distinct"]))
            print("    lead: %s" % C.a(e["lead_headline"]))
            for ak in e["article_keys"]:
                art = articles.get(ak, {})
                print("    - [%s] %s" % (ak.split("|")[0][:24], C.a(art.get("title"))))
    if not new_ids and not moved_ids:
        print("  0 new or moved events of %d served: the served events are the 8 that were served before, row for row." % len(a_e))

    # ---------------- (2) new / newly tier-A/B rows ----------------
    print("\n== (2) tier-A/B mention rows that are NEW or NEWLY tier-A/B in the served new mention part ==")
    mb_key = before["tables"][pg.GOLD_TABLE]["newest_key"]
    ma_key = parts[pg.GOLD_TABLE][-1]["key"]
    b_m = {(r["article_key"], r["security_key"]): r for r in G.read_rows(client, mb_key)}
    a_rows = G.read_rows(client, ma_key)
    print("replaced newest part: %s (%d rows)\nnew newest part:      %s (%d rows; tier-A/B rows: %d)" % (
        mb_key, len(b_m), ma_key, len(a_rows), sum(1 for r in a_rows if r["signal_tier"] in ("A", "B"))))
    old_sec = C.sec_map(C.load_json(C.OLD_PATH))
    new_sec = C.sec_map(C.load_json(C.NEW_PATH))
    brands = C.brand_forms_by_security()
    picked = []
    for r in a_rows:
        if r["signal_tier"] not in ("A", "B"):
            continue
        k = (r["article_key"], r["security_key"])
        b = b_m.get(k)
        if b is None:
            picked.append((r, b, "NEW ROW"))
        elif b["signal_tier"] not in ("A", "B"):
            picked.append((r, b, "NEWLY tier-%s (was %s)" % (r["signal_tier"], b["signal_tier"])))
    print("denominator: %d tier-A/B rows served; %d are new or newly tier-A/B" % (sum(1 for r in a_rows if r["signal_tier"] in ("A", "B")), len(picked)))
    groups = collections.defaultdict(list)
    for r, b, why in picked:
        art = articles.get(r["article_key"])
        added, _lost = C.added_spans(art, old_sec[r["security_key"]], new_sec[r["security_key"]], brands) if art else ([], [])
        if not added:
            groups[("(no added span: the tier moved through the row's counts/share)", "-")].append((r, why, None))
            continue
        forms_seen = set()
        for sp in added:
            f = (sp["class"], sp["form"])
            groups[f].append((r, why, sp))
            forms_seen.add(f)
    print("groups by form (class, form): %d; row-form pairs: %d" % (len(groups), sum(len(v) for v in groups.values())))
    for (cls, form), items in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print("\n-- form %s '%s': %d hits in %d rows" % (cls, C.a(form), len(items), len({(i[0]["article_key"], i[0]["security_key"]) for i in items})))
        for r, why, sp in items:
            art = articles.get(r["article_key"], {})
            print("  [%s tier %s | %s] %s | %s | title=%s lead=%s count=%d | %s" % (
                why, r["signal_tier"], r["publisher"], r["security_key"], C.a(art.get("title"), 140),
                r["mention_in_title"], r["mention_in_lead"], r["mention_count"], "match_forms=%s" % C.a(r["match_forms"])))
            if sp:
                print("       %s '%s' in %s: %s" % (sp["class"], C.a(sp["matched"]), sp["where"], C.context(sp["text"], sp["offset"], sp["end"])))
    print("\n(AC4 is a JUDGMENT: these are the served rows; no verdict is recorded here.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
