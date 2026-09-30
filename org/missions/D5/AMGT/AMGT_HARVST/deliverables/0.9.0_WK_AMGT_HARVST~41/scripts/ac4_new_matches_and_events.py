"""HVST-d-2 AC4 (JUDGMENT, PRESENTED AND NOT GRADED). Read from S3: the SERVED newest parts against the parts
served before this act (the previous part of each table, by the readers' (date, key) order). No verdict is
printed or recorded here; the grade is 3.0.0_SA_CVO~Z's at L9."""
import random
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _rebuild as R  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SEED = 20260929
LIMIT = 40


def main():
    client = store._default_client()
    ps = {t: R.parts(t, client) for t in R.TABLES}
    cur = {t: ps[t][-1] for t in R.TABLES}
    prev = {t: ps[t][-2] for t in R.TABLES}
    for t in R.TABLES:
        print("%-26s SERVED newest %s ETag=%s  |  previously served %s ETag=%s" % (
            t, R.short(cur[t][0]), cur[t][1], R.short(prev[t][0]), prev[t][1]))
    mention_new = R.read_key(cur[pg.GOLD_TABLE][0], client)
    mention_old = R.read_key(prev[pg.GOLD_TABLE][0], client)
    event_new = R.read_key(cur[pg.GOLD_EVENT_TABLE][0], client)
    event_old = R.read_key(prev[pg.GOLD_EVENT_TABLE][0], client)
    title_of = pg._headline_by_article_key(client=client)

    pair = lambda r: (r["article_key"], r["security_key"])  # noqa: E731
    old_pairs = {pair(r) for r in mention_old}
    new_rows = sorted((r for r in mention_new if pair(r) not in old_pairs), key=lambda r: (r["security_key"], str(r["published_utc"]), r["article_key"]))
    tier_a = [r for r in new_rows if r["signal_tier"] == "A"]
    if len(new_rows) <= LIMIT:
        sample, how = new_rows, "every one (%d, at most %d)" % (len(new_rows), LIMIT)
    else:
        rng = random.Random(SEED)
        rest = [r for r in new_rows if r not in tier_a]
        sample = sorted(tier_a + rng.sample(rest, max(0, LIMIT - len(tier_a))), key=lambda r: (r["security_key"], r["article_key"]))
        how = "%d drawn with seed %d plus all %d tier-A rows" % (LIMIT, SEED, len(tier_a))
    print("\n== AC4 PART 1: NEW (article, security) mention matches, read from the served parts ==")
    print("new matches = %d (%d on tier-A rows); sample = %s" % (len(new_rows), len(tier_a), how))
    print("QUESTION: is each a real mention of that company, or a false hit on a common word? (presented, NOT graded)")
    for i, r in enumerate(sample, 1):
        print("%2d. %-16s %-6s %-44s tier=%s title-hit=%s lead-hit=%s alias(match_forms)=%s count=%s" % (
            i, r["security_key"], r["publisher"], r["article_key"], r["signal_tier"], r["mention_in_title"],
            r["mention_in_lead"], r["match_forms"], r["mention_count"]))
        print("      headline: %s" % R.a(title_of.get(r["article_key"]), 160))

    print("\n== AC4 PART 2: every NEW or MOVED served event ==")
    print("QUESTION: is it ONE story about its own company, and does its lead name that story? (presented, NOT graded)")
    old_ev = {e["event_id"]: e for e in event_old}
    changed = [e for e in event_new if e["event_id"] not in old_ev or R.canon_row(e) != R.canon_row(old_ev[e["event_id"]])]
    by_pair = {pair(r): r for r in mention_new}
    print("served events now = %d (before = %d); new or moved = %d" % (len(event_new), len(event_old), len(changed)))
    for e in changed:
        kind = "NEW" if e["event_id"] not in old_ev else "MOVED"
        members = [by_pair[(k, e["security_key"])] for k in e["article_keys"]]
        pubs = sorted({pg._row_publisher(r) for r in members if r["signal_tier"] == "A"})
        print("%s event %s: %s span %s..%s (%d day) articles=%d tier-A publishers=%s" % (
            kind, e["event_id"][:12], e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"], pubs))
        print("  lead: %s | %s" % (e["lead_article_key"], R.a(e["lead_headline"], 160)))
        for r in members:
            print("  %s %-7s tier=%s %-44s %s" % (str(r["published_utc"])[:10], r["publisher"], r["signal_tier"], r["article_key"],
                                                   R.a(title_of.get(r["article_key"]), 130)))
        also = sorted(k for k in by_pair if k[1] == e["security_key"] and by_pair[k]["signal_tier"] in ("A", "B")
                      and k[0] not in e["article_keys"])
        print("  for context, the same security's other tier-A/B articles outside this event (%d):" % len(also))
        for k in also:
            r = by_pair[k]
            print("    %s %-7s tier=%s %-44s %s" % (str(r["published_utc"])[:10], r["publisher"], r["signal_tier"], k[0], R.a(title_of.get(k[0]), 110)))
    print("\nAC4 PRESENTED (no verdict recorded here; oracle 3.0.0_SA_CVO~Z at L9)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
