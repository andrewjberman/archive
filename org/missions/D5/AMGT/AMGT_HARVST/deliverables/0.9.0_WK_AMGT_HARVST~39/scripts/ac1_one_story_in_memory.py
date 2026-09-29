"""HVST-b-1 AC1 -- the ONE-STORY event rule over the LANDED data, IN MEMORY. READ-ONLY (S3 GET only).

Builds event rows with the NEW rule (the working tree's publication_gold) from the newest
article_security_mention snapshot + silver headlines exactly as build_event does, and sets them beside
the SERVED newest chatter_event snapshot. Also loads the BASE module (git show <issuance>:path, in memory
only) to show criterion (c) FAILS at the base on BA_US_Equity 2026-09-08.
"""
import os
import re
import subprocess
import sys
import types

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import lib.research.harvest.publication_gold as g  # noqa: E402

BASE_REF = "8dbea345c9"
PATH = "lib/research/harvest/publication_gold.py"
base = types.ModuleType("publication_gold_base")
base.__file__ = os.path.join(ROOT, PATH)
exec(compile(subprocess.check_output(["git", "show", "%s:%s" % (BASE_REF, PATH)]).decode("utf-8"), PATH, "exec"),
     base.__dict__)

# The six events the round-12 L9 (ADJUDICATION_v20 @19dfdd2579) graded as ONE company event.
SIX = [("992_HK_Equity", "2026-02-12"), ("992_HK_Equity", "2026-05-22"), ("992_HK_Equity", "2026-08-13"),
       ("COST_US_Equity", "2026-09-14"), ("HD_US_Equity", "2026-08-18"), ("NVDA_US_Equity", "2026-06-01")]

served = g._latest_gold_snapshot_rows(g.GOLD_EVENT_TABLE)
mention = g._latest_gold_snapshot_rows(g.GOLD_TABLE)
headlines = g._headline_by_article_key()
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = headlines.get(row.get("article_key"))
    enriched.append(row)
new = g.event_rows(enriched)
row_of = {(r["security_key"], r["article_key"]): r for r in enriched}

print("served events: %d   new in-memory events: %d   mention rows: %d   silver headlines: %d"
      % (len(served), len(new), len(mention), len(headlines)))


def tier_a_keys(event):
    return frozenset(k for k in event["article_keys"] if row_of[(event["security_key"], k)]["signal_tier"] == "A")


print("\n=== EVERY SERVED EVENT AND WHAT IT BECOMES ===")
becomes = {}
for s in sorted(served, key=lambda e: (e["security_key"], e["first_day"])):
    s_a = tier_a_keys(s)
    hits = [e for e in new if e["security_key"] == s["security_key"] and (tier_a_keys(e) & s_a)]
    if not hits:
        fate = "gone"
    elif len(hits) == 1:
        e = hits[0]
        same_span = (e["first_day"], e["last_day"]) == (s["first_day"], s["last_day"])
        same_a = tier_a_keys(e) == s_a
        fate = "kept (same span: %s, same tier-A membership: %s, tier-B %d -> %d)" % (
            same_span, same_a, s["tier_b"], e["tier_b"])
    else:
        fate = "split into %d" % len(hits)
    becomes[(s["security_key"], str(s["first_day"]))] = (fate, hits)
    print("  %-15s %s  ->  %s" % (s["security_key"], s["first_day"], fate))

print("\n=== EVERY NEW EVENT ===")
for e in new:
    print("\n== %s  %s..%s  event_id=%s  A=%d B=%d" % (
        e["security_key"], e["first_day"], e["last_day"], e["event_id"], e["tier_a"], e["tier_b"]))
    pubs = sorted({g._row_publisher(row_of[(e["security_key"], k)]) for k in e["article_keys"]
                   if row_of[(e["security_key"], k)]["signal_tier"] == "A"})
    print("  tier-A publishers: %s" % pubs)
    for k in e["article_keys"]:
        r = row_of[(e["security_key"], k)]
        print("    %s %-8s %s | %s" % (r["signal_tier"], g._row_publisher(r), r["published_utc"].date(), r["title"]))
    print("  LEAD: %s (%s)" % (e["lead_headline"], e["lead_article_key"]))

# (a) the six map to EXACTLY ONE new event, same span, same tier-A membership
print("\n=== (a) THE SIX ONE-COMPANY-EVENT EVENTS ===")
a_pass = 0
served_by = {(s["security_key"], str(s["first_day"])): s for s in served}
for key in SIX:
    s = served_by.get(key)
    fate, hits = becomes.get(key, ("MISSING FROM SERVED", []))
    ok = (s is not None and len(hits) == 1
          and (hits[0]["first_day"], hits[0]["last_day"]) == (s["first_day"], s["last_day"])
          and tier_a_keys(hits[0]) == tier_a_keys(s))
    a_pass += 1 if ok else 0
    print("  %-15s %s  %s  -> %s" % (key[0], key[1], "OK  " if ok else "FAIL", fate))
print("(a) %d of 6" % a_pass)

# (b) every new event_id unique
ids = [e["event_id"] for e in new]
b_ok = len(ids) == len(set(ids))
print("(b) every new event_id unique: %s (%d ids, %d distinct)" % (b_ok, len(ids), len(set(ids))))

# (c) no two headlines in a story linked ONLY by a calendar word.
CAL = set(g._STORY_CALENDAR)


def edges_only_calendar(events, tokens_of, ubiquitous_of):
    """For each event, for each pair of its tier-A headlines that the rule's own link test would join
    (>= 1 shared remaining token), report the pair if EVERY shared token is a calendar word."""
    bad = []
    for e in events:
        arts = [row_of[(e["security_key"], k)] for k in e["article_keys"]]
        a = [r for r in arts if r["signal_tier"] == "A"]
        toks = [tokens_of(r) for r in a]
        ub = ubiquitous_of(e, a, toks)
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                shared = (toks[i] - ub) & (toks[j] - ub)
                if shared and shared <= CAL:
                    bad.append((e["security_key"], str(e["first_day"]), a[i]["title"], a[j]["title"], sorted(shared)))
    return bad


# raw stems INCLUDING calendar words (a tokenizer with no calendar stoplist), so a calendar link is visible
def raw_stems(title):
    out = set()
    for w in re.findall(r"[a-z0-9]+", (title or "").lower()):
        if len(w) >= 3 and w not in g._STORY_STOPWORDS - CAL:
            out.add(g._stem(w))
    return frozenset(out)


def new_ubiquitous(e, a, toks):
    # the security's name as the NEW rule reads it (over ALL the security's tier-A headlines)
    sec = [r for r in enriched if r["security_key"] == e["security_key"] and r["signal_tier"] == "A"]
    names = g._security_name_tokens([(g._story_tokens(r["title"]),
                                      g._day_of(r["published_utc"])) for r in sec])
    return frozenset(names or ())


def base_ubiquitous(e, a, toks):
    return frozenset.intersection(*toks) if toks else frozenset()


bad_new = edges_only_calendar(new, lambda r: raw_stems(r["title"]), new_ubiquitous)
# BASE: the served (8) events are the base rule's events; reproduce its link test on them
bad_base = edges_only_calendar(served, lambda r: base._story_tokens(r["title"]), base_ubiquitous)
# also confirm by the base module's own grouper: the BA 09-08 stories it forms
ba = [s for s in served if (s["security_key"], str(s["first_day"])) == ("BA_US_Equity", "2026-09-08")][0]
ba_arts = [row_of[(ba["security_key"], k)] for k in ba["article_keys"]]
print("\nBASE _event_stories on BA_US_Equity 2026-09-08 (informational):")
for st in base._event_stories(ba_arts):
    print("   base story: %s" % [r["title"] for r in st])
print("(c) NEW rule: pairs linked only by a calendar word: %d %s" % (len(bad_new), bad_new))
print("(c) BASE rule (reproduced link test over the 8 served events): pairs linked only by a calendar word: %d" % len(bad_base))
for b in bad_base:
    print("      BASE FAILS (c): %s %s | %r ~ %r via %s" % b)
c_ok = len(bad_new) == 0 and len(bad_base) >= 1
# every new event's tokens carry no calendar word at all
cal_in_terms = [w for r in enriched for w in g._story_tokens(r["title"]) if w in CAL]
print("calendar words present among the new rule's stems over all %d headlines: %d" % (len(headlines), len(cal_in_terms)))
c_ok = c_ok and not cal_in_terms

print("\n=== BA_US_Equity (named, not required) ===")
for day in ("2026-08-26", "2026-09-08"):
    fate, hits = becomes.get(("BA_US_Equity", day), ("not served", []))
    print("  BA_US_Equity %s: %s" % (day, fate))
    for e in hits:
        print("     new event %s..%s A=%d: %s" % (e["first_day"], e["last_day"], e["tier_a"],
                                                  [row_of[("BA_US_Equity", k)]["title"] for k in e["article_keys"]]))
    if not hits:
        print("     (no new event: no story on that day qualifies)")

ok = a_pass == 6 and b_ok and c_ok
print("\nAC1 (a) %d/6 (b) %s (c) %s -> %s" % (a_pass, b_ok, c_ok, "PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
