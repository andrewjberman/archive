"""HVST-a-3 AC1 -- the NEW lead rule over the LANDED data, IN MEMORY. READ-ONLY (S3 GET only).

Reads the newest article_security_mention snapshot and the silver headlines exactly as build_event
does, builds event rows with the new rule, compares to the SERVED newest chatter_event snapshot.
"""
import os
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import lib.research.harvest.publication_gold as g  # noqa: E402

FIELDS = ["event_id", "security_key", "composite_figi", "first_day", "last_day", "days_span",
          "articles_total", "tier_a", "tier_b", "publishers_distinct", "article_keys"]

served = g._latest_gold_snapshot_rows(g.GOLD_EVENT_TABLE)
mention = g._latest_gold_snapshot_rows(g.GOLD_TABLE)
headlines = g._headline_by_article_key()
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = headlines.get(row.get("article_key"))
    enriched.append(row)
new = g.event_rows(enriched)

print("served events: %d   new in-memory events: %d   mention rows: %d   silver headlines: %d"
      % (len(served), len(new), len(mention), len(headlines)))
served_by_id = {r["event_id"]: r for r in served}
new_by_id = {r["event_id"]: r for r in new}
by_sec_key = {}
for r in enriched:
    by_sec_key[(r["security_key"], r["article_key"])] = r

a_ok = set(served_by_id) == set(new_by_id) and len(served) == len(new) == 8
b_ok = True
moved_rows = []
n_equal = 0
for e in sorted(new, key=lambda e: (e["security_key"], e["first_day"])):
    s = served_by_id.get(e["event_id"])
    print("\n== %s  %s..%s  event_id=%s" % (e["security_key"], e["first_day"], e["last_day"], e["event_id"][:16]))
    arts = [by_sec_key[(e["security_key"], k)] for k in e["article_keys"]]
    stories = g._event_stories(arts)
    max_a = 0
    lead_story_a = None
    for i, st in enumerate(stories, 1):
        n_a = sum(1 for r in st if r["signal_tier"] == "A")
        max_a = max(max_a, n_a)
        if any(r["article_key"] == e["lead_article_key"] for r in st):
            lead_story_a = n_a
        print("  story %d: tier-A=%d  articles=%d" % (i, n_a, len(st)))
        for r in st:
            print("      %s %s | %s" % (r["signal_tier"], r["article_key"], r["title"]))
    old_head = s["lead_headline"] if s else None
    moved = bool(s) and s["lead_article_key"] != e["lead_article_key"]
    print("  OLD lead (served): %s" % old_head)
    print("  NEW lead         : %s" % e["lead_headline"])
    print("  moved: %s   lead's story tier-A=%s (max over stories=%d)" % (moved, lead_story_a, max_a))
    if lead_story_a != max_a:
        b_ok = False
    if s:
        same = all(s[f] == e[f] for f in FIELDS)
        n_equal += 1 if same else 0
        print("  non-lead fields equal served: %s" % same)
        if not same:
            a_ok = False
    moved_rows.append((e["security_key"], str(e["first_day"]), moved))

base_equal = sum(1 for e in new if served_by_id.get(e["event_id"]) and served_by_id[e["event_id"]]["lead_article_key"] == e["article_keys"][0])
print("\nBASE CHECK: served lead == the OLD rule's lead (sorted-first article): %d of %d" % (base_equal, len(new)))
print("\n(a) event_id set equal, 8 of 8 non-lead field sets equal served: %s  (%d of %d equal)" % (a_ok and n_equal == 8, n_equal, len(new)))
print("(b) every new lead in a max-tier-A story: %s" % b_ok)
c_ok = ("BA_US_Equity", "2026-09-08", True) in moved_rows
print("(c) BA_US_Equity 2026-09-08 lead moved: %s   (moved events: %d of %d: %s)"
      % (c_ok, sum(1 for m in moved_rows if m[2]), len(moved_rows), [m[:2] for m in moved_rows if m[2]]))
ok = a_ok and n_equal == 8 and b_ok and c_ok
print("AC1 %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
