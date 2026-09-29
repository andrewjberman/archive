"""HVST-c-1 AC1 -- the held-out denominator and what event_rows forms on it. READ-ONLY (S3 GET only)."""
import _common as c
from _common import pg

rows, n_head = c.load()
print("newest mention snapshot: %d rows; silver headlines: %d; titled rows: %d" % (len(rows), n_head, sum(1 for r in rows if r["title"])))
ins = [r for r in rows if not c.held_out(r)]
out = [r for r in rows if c.held_out(r)]
print("\n=== POPULATIONS ===")
print(c.fmt_stats("IN-SAMPLE", c.pop_stats(ins)), " [%s]" % ", ".join(sorted(c.IN_SAMPLE)))
print(c.fmt_stats("HELD-OUT", c.pop_stats(out)))
allday = sorted(d for d in (c.day(r) for r in rows) if d is not None)
print("newest capture date in the snapshot: %s ; rule frozen at %s -> captures after the freeze: %d rows"
      % (allday[-1], c.FROZEN_AT, sum(1 for r in rows if c.day(r) is not None and str(c.day(r)) > "2026-09-29")))
print("tier counts held-out:", {t: sum(1 for r in out if r.get("signal_tier") == t) for t in sorted({r.get('signal_tier') for r in out}, key=str)})

# the rule, exactly as build_event applies it, over the WHOLE snapshot; keep the held-out securities' events
events = pg.event_rows(rows)
ho_events = [e for e in events if e["security_key"] not in c.IN_SAMPLE]
print("\nevent_rows over the whole snapshot: %d events (%d in-sample, %d held-out)"
      % (len(events), len(events) - len(ho_events), len(ho_events)))

row_of = {(r["security_key"], r["article_key"]): r for r in rows}
print("\n=== HELD-OUT EVENTS THE RULE FORMS ===")
if not ho_events:
    print("(none)")
for e in ho_events:
    arts = [row_of[(e["security_key"], k)] for k in e["article_keys"]]
    pubs = sorted({pg._row_publisher(r) for r in arts if r["signal_tier"] == "A"})
    print("\n== %s %s..%s lead=%s | %s\n   tier-A publishers: %s" % (e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"], e["lead_headline"], pubs))
    for r in arts:
        print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))

# NEAR-MISSES: held-out STORIES (rule's own grouping) with >= 2 tier-A/B articles that did not become an event
print("\n=== HELD-OUT STORIES WITH >= 2 TIER-A/B ARTICLES THAT DID NOT QUALIFY ===")
by_sec = {}
for r in out:
    if c.is_ab(r) and c.day(r) is not None:
        by_sec.setdefault(r["security_key"], []).append(r)
in_event = {(e["security_key"], k) for e in ho_events for k in e["article_keys"]}
near = []
for sec in sorted(by_sec):
    for story in pg._security_stories(by_sec[sec]):
        if len(story) < 2:
            continue
        if all((sec, r["article_key"]) in in_event for r in story):
            continue
        near.append((sec, story))
for i, (sec, story) in enumerate(near, 1):
    a = [r for r in story if r["signal_tier"] == "A"]
    pubs = sorted({pg._row_publisher(r) for r in a})
    dcount = {}
    for r in story:
        dcount[c.day(r)] = dcount.get(c.day(r), 0) + 1
    reasons = []
    if len(a) < 1:
        reasons.append("no tier-A article")
    # per-day qualification reasons, exactly the rule's two tests
    day_reasons = []
    for d in sorted(dcount):
        rs = [r for r in story if c.day(r) == d]
        pa = {pg._row_publisher(r) for r in rs if r["signal_tier"] == "A"}
        why = []
        if len(rs) < pg.EVENT_MIN_ARTICLES:
            why.append("too few articles (%d < %d)" % (len(rs), pg.EVENT_MIN_ARTICLES))
        if len(pa) < pg.EVENT_MIN_PUBLISHERS:
            why.append("too few tier-A publishers (%d < %d)" % (len(pa), pg.EVENT_MIN_PUBLISHERS))
        day_reasons.append("%s: %s" % (d, "; ".join(why) if why else "QUALIFIES"))
    print("\n[NM%d] %s  %d articles (A=%d B=%d) over %d day(s)  tier-A publishers=%s" % (i, sec, len(story), len(a), len(story) - len(a), len(dcount), pubs))
    print("   per-day: " + " | ".join(day_reasons))
    for r in story:
        print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))
print("\nnear-miss stories (held-out, >=2 A/B articles, none/not all in an event): %d" % len(near))

# SUPPLEMENT (not the rule's stories): the rule only builds stories around tier-A articles, so a cluster with
# NO tier-A article is never a story and cannot appear above. List every held-out same-security cluster of
# >= 2 distinct tier-A/B articles (consecutive published days apart <= max_gap+1) that is not in an event.
print("\n=== SUPPLEMENT: held-out same-security clusters of >= 2 distinct tier-A/B articles within the merge window, NOT in an event (the rule never forms a story without a tier-A article) ===")
sup = []
for sec in sorted(by_sec):
    rs = sorted({r["article_key"]: r for r in by_sec[sec]}.values(), key=lambda r: (r["published_utc"], r["article_key"]))
    cl = []
    for r in rs:
        if cl and (c.day(r) - c.day(cl[-1])).days <= pg.EVENT_MAX_GAP_DAYS + 1:
            cl.append(r)
        else:
            if len(cl) >= 2:
                sup.append((sec, cl))
            cl = [r]
    if len(cl) >= 2:
        sup.append((sec, cl))
for i, (sec, cl) in enumerate(sup, 1):
    a = [r for r in cl if r["signal_tier"] == "A"]
    pubs = sorted({pg._row_publisher(r) for r in a})
    spandays = (c.day(cl[-1]) - c.day(cl[0])).days + 1
    if len(a) == 0:
        why = "no tier-A article, so no story and no tier-A publisher"
    elif len(pubs) < pg.EVENT_MIN_PUBLISHERS:
        why = "too few tier-A publishers (%d < %d)" % (len(pubs), pg.EVENT_MIN_PUBLISHERS)
    else:
        why = "has >= 2 tier-A publishers; check the story grouping"
    print("\n[SUP%d] %s  %d articles (A=%d B=%d) over %d day(s)  tier-A publishers=%s  reason: %s"
          % (i, sec, len(cl), len(a), len(cl) - len(a), spandays, pubs, why))
    for r in cl:
        print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))
print("\nsupplement clusters: %d (largest: %d articles)" % (len(sup), max([len(cl) for _s, cl in sup] or [0])))
hs = c.pop_stats(out)
print("\nVERDICT: held-out events: %d over %d held-out securities (%d held-out securities carry tier-A/B rows; %d held-out rows, %d tier-A/B)"
      % (len(ho_events), len({e['security_key'] for e in ho_events}), hs["ab_securities"], hs["rows"], hs["ab_rows"]))
if not ho_events:
    print("The held-out pass is NOT a precision grade (0 events formed on the held-out population); the round-13 pass stays IN-SAMPLE. What the held-out read can test here is RECALL -- see the %d near-miss stories (rule's own grouping), the %d supplement clusters (no tier-A article) and AC4." % (len(near), len(sup)))
