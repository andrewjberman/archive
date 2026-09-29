"""HVST-b-1 AC4 (AMENDMENT 1, row AMGT_HARVST-Z-S40) -- NO LEAD THE ROUND-12 L9 GRADED AS NAMING ITS BURST
REGRESSES. READ-ONLY (S3 GET only). In memory over the landed data with the NEW rule: for each served event
that is KEPT (same security, same span), print the served lead and the rebuilt lead; PASS only if every kept
event's rebuilt lead EQUALS its served lead. Prints the story each of BA 09-08's tier-A headlines lands in and
the term that linked them (or refused the link). Also loads the b-1 rule AS FIRST MERGED (git show of the
worker's b-1 commit f41a4f3a36, in memory only) to show BA 09-08 FAILS there.
"""
import os
import subprocess
import sys
import types

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import lib.research.harvest.publication_gold as g  # noqa: E402

PATH = "lib/research/harvest/publication_gold.py"
MERGED_B1 = "f41a4f3a36"
merged = types.ModuleType("publication_gold_b1_merged")
merged.__file__ = os.path.join(ROOT, PATH)
exec(compile(subprocess.check_output(["git", "show", "%s:%s" % (MERGED_B1, PATH)]).decode("utf-8"), PATH, "exec"),
     merged.__dict__)

served = g._latest_gold_snapshot_rows(g.GOLD_EVENT_TABLE)
mention = g._latest_gold_snapshot_rows(g.GOLD_TABLE)
headlines = g._headline_by_article_key()
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = headlines.get(row.get("article_key"))
    enriched.append(row)
new = g.event_rows(enriched)
old = merged.event_rows(enriched)
print("served events: %d   rebuilt (NEW rule): %d   rebuilt (b-1 as first merged, %s): %d   mention rows: %d"
      % (len(served), len(new), MERGED_B1, len(old), len(mention)))


def by_span(events):
    out = {}
    for e in events:
        out.setdefault((e["security_key"], e["first_day"], e["last_day"]), []).append(e)
    return out


new_by, old_by = by_span(new), by_span(old)

print("\n=== EVERY SERVED EVENT: served lead vs rebuilt lead ===")
kept = 0
regress = []
for s in sorted(served, key=lambda e: (e["security_key"], e["first_day"])):
    key = (s["security_key"], s["first_day"], s["last_day"])
    hit = new_by.get(key, [])
    old_hit = old_by.get(key, [])
    print("\n%s %s..%s" % key)
    print("  SERVED lead : %s" % s["lead_headline"])
    if not hit:
        print("  NEW rule    : event GONE (no story qualifies on that span) -- not a kept event")
        continue
    kept += 1
    e = hit[0]
    same = e["lead_article_key"] == s["lead_article_key"]
    print("  REBUILT lead: %s   equals served: %s" % (e["lead_headline"], same))
    if old_hit:
        print("  (b-1 as first merged: %s   equals served: %s)"
              % (old_hit[0]["lead_headline"], old_hit[0]["lead_article_key"] == s["lead_article_key"]))
    if not same:
        regress.append(key)
print("\nkept events: %d of %d served; leads equal served on %d of %d kept" % (kept, len(served), kept - len(regress), kept))

# ---- BA 09-08: story each tier-A headline lands in, and the linking term ----
print("\n=== BA_US_Equity 2026-09-08: the story each tier-A headline lands in ===")
ba = [r for r in enriched if r["security_key"] == "BA_US_Equity" and r["signal_tier"] in ("A", "B")]
stories = g._security_stories(ba)
ba_a = [r for r in ba if r["signal_tier"] == "A" and str(g._day_of(r["published_utc"])) == "2026-09-08"]
tier_a_all = [r for r in ba if r["signal_tier"] == "A"]
names = g._security_name_tokens([(g._story_tokens(r["title"]), g._day_of(r["published_utc"])) for r in tier_a_all])
terms = {r["article_key"]: g._story_terms(g._story_tokens(r["title"]), names) for r in ba_a}
print("security name stems dropped: %s" % sorted(names or ()))
for r in sorted(ba_a, key=g._event_sort_key):
    idx = [i for i, st in enumerate(stories) if any(x["article_key"] == r["article_key"] for x in st)]
    members = [x["title"] for st in stories for x in st if any(y["article_key"] == r["article_key"] for y in st)]
    print("  %-8s %s\n     terms %s\n     lands in story #%s with %d headline(s): %s"
          % (g._row_publisher(r), r["title"], sorted(terms[r["article_key"]]), idx[0] if idx else None,
             len(members), members))
print("pairwise shared terms:")
for i, a in enumerate(sorted(ba_a, key=g._event_sort_key)):
    for b in sorted(ba_a, key=g._event_sort_key)[i + 1:]:
        sh = sorted(terms[a["article_key"]] & terms[b["article_key"]])
        verdict = "TIGHT (>= 2 shared terms) -> linked" if len(sh) >= 2 else "one plain word -> link REFUSED (a tight pair exists)"
        print("  %s ~ %s : %s   %s" % (g._row_publisher(a), g._row_publisher(b), sh, verdict))

ba_key = ("BA_US_Equity", g._day_of(ba_a[0]["published_utc"]), g._day_of(ba_a[0]["published_utc"]))
ba_served = [s for s in served if (s["security_key"], s["first_day"], s["last_day"]) == ba_key][0]
ba_new = new_by.get(ba_key, [])
ba_old = old_by.get(ba_key, [])
ba_ok = bool(ba_new) and ba_new[0]["lead_article_key"] == ba_served["lead_article_key"] \
    and ba_new[0]["lead_headline"] == "Boeing Delivers 51 Jets in August, Lowest in Four Months"
old_fails = bool(ba_old) and ba_old[0]["lead_article_key"] != ba_served["lead_article_key"]
print("\nBA 09-08 NEW rule: lead = %r -> keeps served lead: %s" % (ba_new[0]["lead_headline"] if ba_new else None, ba_ok))
print("BA 09-08 b-1 as first merged: lead = %r -> FAILS (lead moves): %s"
      % (ba_old[0]["lead_headline"] if ba_old else None, old_fails))

ok = not regress and kept >= 1 and ba_ok and old_fails
print("\nAC4 kept=%d regressions=%d BA09-08 keeps lead=%s base fails=%s -> %s"
      % (kept, len(regress), ba_ok, old_fails, "PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
