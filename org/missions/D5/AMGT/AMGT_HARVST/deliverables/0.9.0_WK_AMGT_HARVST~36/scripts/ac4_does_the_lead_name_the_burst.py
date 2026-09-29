"""HVST-a-4 AC4 (JUDGMENT -- PRESENTED, NOT GRADED). READ-ONLY (S3 GET only).

Read from S3, not from the builder: the SERVED newest chatter_event snapshot gives each event lead and
article_keys; the newest article_security_mention snapshot + silver headlines give each article tier and
title. Stories are HVST-a-3 stated grouping (publication_gold._event_stories), applied to the served
event own articles. Nothing here is a verdict: the CVO (3.0.0_SA_CVO~Z, L9) grades whether the lead names
what the burst was about.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

# The worker OWN READING of the headlines, printed as evidence for the CTO open question ("is a
# multi-story day one event?"). It is not a grade of the lead. Keyed by (security, first_day).
SAME_OR_UNRELATED = {
    ("992_HK_Equity", "2026-02-12"): "SAME company event (Lenovo fiscal Q3 results day: an earnings beat and a PC-share/memory-cost remark from the same results)",
    ("992_HK_Equity", "2026-05-22"): "SAME company event for the two tier-A stories (Lenovo fiscal Q4 results); the tier-B story is an UNRELATED market wrap (European indexes)",
    ("992_HK_Equity", "2026-08-13"): "SAME company event (Lenovo fiscal Q1 results)",
    ("BA_US_Equity", "2026-08-26"): "UNRELATED (an FAA Dreamliner inspection order vs a Boeing-subsidiary Wisk vertiport groundbreaking)",
    ("BA_US_Equity", "2026-09-08"): "UNRELATED tier-A stories (a Miami runway overshoot incident vs August delivery numbers); the tier-B story is an UNRELATED analyst-rating roundup",
    ("COST_US_Equity", "2026-09-14"): "SAME company event (Costco motor-oil price hike and purchase limits)",
    ("HD_US_Equity", "2026-08-18"): "SAME company event (Home Depot earnings)",
    ("NVDA_US_Equity", "2026-06-01"): "SAME company event (Nvidia PC push)",
}

client = store._default_client()
served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headlines = pg._headline_by_article_key(client=client)
by_sec_key = {}
for r in mention:
    r = dict(r)
    r["title"] = headlines.get(r.get("article_key"))
    by_sec_key[(r["security_key"], r["article_key"])] = r

print("served newest chatter_event snapshot: %d events; mention rows %d; silver headlines %d" % (len(served), len(mention), len(headlines)))
multi = 0
under_notes = []
over_notes = []
for ev in sorted(served, key=lambda e: (e["security_key"], e["first_day"])):
    arts = [by_sec_key[(ev["security_key"], k)] for k in ev["article_keys"]]
    stories = pg._event_stories(arts)
    is_multi = len(stories) > 1
    multi += 1 if is_multi else 0
    key = (ev["security_key"], str(ev["first_day"]))
    reading = SAME_OR_UNRELATED[key]
    print("\n== %s  %s..%s  event_id=%s" % (ev["security_key"], ev["first_day"], ev["last_day"], ev["event_id"][:16]))
    print("  stories under the a-3 grouping: %d (%s)" % (len(stories), "MULTI-STORY" if is_multi else "one story"))
    for i, st in enumerate(stories, 1):
        n_a = sum(1 for r in st if r["signal_tier"] == "A")
        print("  story %d: tier-A=%d, articles=%d" % (i, n_a, len(st)))
        for r in st:
            print("      %s %s | %s" % (r["signal_tier"], r["article_key"], r["title"]))
    print("  SERVED LEAD: %s | %s" % (ev["lead_article_key"], ev["lead_headline"]))
    print("  same company event or unrelated (worker reading of the headlines, evidence not verdict): %s" % reading)

    # grouping diagnostics, both directions
    a_rows = [r for r in arts if r["signal_tier"] == "A"]
    raw = [pg._story_tokens(r["title"]) for r in a_rows]
    ubiq = frozenset.intersection(*raw) if raw else frozenset()
    kept = [t - ubiq for t in raw]
    if len(a_rows) >= 3:
        print("  tier-A tokens dropped as ubiquitous: %s" % sorted(ubiq))
        for i in range(len(a_rows)):
            for j in range(i + 1, len(a_rows)):
                shared_raw = raw[i] & raw[j]
                shared_kept = kept[i] & kept[j]
                linked = len(shared_kept) >= pg._STORY_MIN_SHARED_TOKENS
                print("  tier-A pair %s ~ %s: shared before drop=%s, after drop=%s -> %s"
                      % (a_rows[i]["article_key"][:14], a_rows[j]["article_key"][:14], sorted(shared_raw),
                         sorted(shared_kept), "LINKED" if linked else "not linked"))
                if len(shared_kept) == 1:
                    over_notes.append((ev["security_key"], str(ev["first_day"]), sorted(shared_kept)))
        n_a_stories = sum(1 for st in stories if any(r["signal_tier"] == "A" for r in st))
        if reading.startswith("SAME") and n_a_stories > 1:
            under_notes.append((ev["security_key"], str(ev["first_day"]), len(a_rows), n_a_stories))

print("\n== DIRECTION OF ERROR, beside each other (CTO half s.4 and COO half s.7) ==")
print("multi-story events under the grouping: %d of %d" % (multi, len(served)))
print("UNDER-MERGE (3+ tier-A events that read as ONE company story to the worker but group as several): %s"
      % ["%s %s: %d tier-A articles -> %d tier-A stories" % u for u in under_notes])
print("OVER-MERGE RISK (3+ tier-A events where a tier-A link rests on exactly ONE shared token): %s"
      % ["%s %s via %s" % o for o in over_notes])
print("Only events with 3+ tier-A articles can have their lead changed by the grouping; the lead of a 2-tier-A event is the same under any grouping.")
print("JUDGMENT PRESENTED, NO VERDICT RECORDED. Oracle: 3.0.0_SA_CVO~Z at L9.")
