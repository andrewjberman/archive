"""HVST-l-2 AC4 (JUDGMENT -- PRESENTED, NO VERDICT; read-only, S3 LIST/GET only): for every CHANGED served event print its
security, span and lead, and every member with publisher, day, tier and guard status. Is it ONE story about its own
company, and does its lead name that story? This script records NO verdict; 3.0.0_SA_CVO~Z grades it at L9."""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    client = G.store._default_client()
    with open(G.BEFORE_JSON, "r", encoding="utf-8") as fh:
        before = json.load(fh)
    parts = G.list_parts(client)
    newest = parts[pg.GOLD_EVENT_TABLE][-1]
    served = G.read_rows(client, before["tables"][pg.GOLD_EVENT_TABLE]["newest_key"])
    new = G.read_rows(client, newest["key"])
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
    titles = pg._headline_by_article_key(client=client)
    m_by = {(r["security_key"], r["article_key"]): r for r in mention}
    print("== HVST-l-2 AC4 (JUDGMENT -- PRESENTED, NO VERDICT): the CHANGED events ==")
    print("BEFORE served part %s (%d events); AFTER newest part %s (%d events); mention rows=%d, silver headlines=%d" % (
        before["tables"][pg.GOLD_EVENT_TABLE]["newest_key"], len(served), newest["key"], len(new), len(mention), len(titles)))
    mapped, _unclaimed = G.map_events(served, new)
    changed = [(s, tg[0]) for s, v, tg in mapped if v == "CHANGED"]
    print("CHANGED served events: %d of %d\n" % (len(changed), len(served)))
    for s, t in changed:
        print("-" * 100)
        print("SECURITY %s" % t["security_key"])
        print("  BEFORE span %s..%s (%d articles) lead=%r" % (s["first_day"], s["last_day"], s["articles_total"], C.a(s.get("lead_headline"))))
        print("  AFTER  span %s..%s (days_span=%s, %d articles, tier A %s / B %s, publishers %s) event_id=%s" % (
            t["first_day"], t["last_day"], t["days_span"], t["articles_total"], t["tier_a"], t["tier_b"], t["publishers_distinct"], t["event_id"][:12]))
        print("  AFTER  lead=%r  (lead_article_key %s)" % (C.a(t.get("lead_headline")), t["lead_article_key"]))
        print("  members (%d):" % len(t["article_keys"]))
        for k in t["article_keys"]:
            m = m_by.get((t["security_key"], k), {})
            guarded = pg._is_guarded(m) if m else None
            day = pg._day_of(m["published_utc"]) if m.get("published_utc") else None
            was_member = "yes" if k in (s.get("article_keys") or []) else "NEW"
            print("    %-9s %s day=%s tier=%s guard=%s (is_roundup=%s co_mention_count=%s) was_in_before_event=%s%s"
                  % (pg._row_publisher(m) if m else "?", k, day, m.get("signal_tier"), "GUARDED" if guarded else "not guarded",
                     m.get("is_roundup"), m.get("co_mention_count"), was_member, "  <- LEAD" if k == t["lead_article_key"] else ""))
            print("        title: %r" % C.a(titles.get(k)))
        print()
    print("QUESTION PRESENTED, NO VERDICT RECORDED: is each ONE story about its own company, and does its lead name that story?")
    print("status: UNVERIFIABLE-BY-INSTRUMENT; graded by 3.0.0_SA_CVO~Z at L9")
    return 0


if __name__ == "__main__":
    sys.exit(main())
