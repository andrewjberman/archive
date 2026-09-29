"""HVST-c-1 AC4 (JUDGMENT -- PRESENTED, NOT GRADED). READ-ONLY (S3 GET only).

Part 1: every held-out EVENT the rule forms, with the b-2 AC4 question (is it ONE story about its own company, and
does its lead name it?). Part 2: every held-out NEAR-MISS -- the rule's own stories with >= 2 tier-A/B articles that did
not become an event, and every same-security cluster of >= 2 distinct tier-A/B articles within the merge window that is
in no event -- with all headlines, and the RECALL question. Part 3 (context for the grader): EVERY held-out tier-A/B
row by security, so a burst the two lists above could not see is visible. NO verdict is recorded here: the CVO
(3.0.0_SA_CVO~Z, L9) grades."""
import _common as c
from _common import pg

rows, _n = c.load()
out = [r for r in rows if c.held_out(r)]
events = pg.event_rows(rows)
ho_events = [e for e in events if e["security_key"] not in c.IN_SAMPLE]
row_of = {(r["security_key"], r["article_key"]): r for r in rows}

print("held-out population: %d rows over %d securities (%d tier-A/B rows over %d securities); in-sample securities excluded: %s"
      % (len(out), len({r["security_key"] for r in out}), sum(1 for r in out if c.is_ab(r)),
         len({r["security_key"] for r in out if c.is_ab(r)}), ", ".join(sorted(c.IN_SAMPLE))))

print("\n=== PART 1: HELD-OUT EVENTS (%d) ===" % len(ho_events))
if not ho_events:
    print("(none: the rule forms no event on any held-out security, so there is no held-out event to grade)")
for e in ho_events:
    print("\n== %s %s..%s  LEAD: %s | %s" % (e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"], e["lead_headline"]))
    for k in e["article_keys"]:
        r = row_of[(e["security_key"], k)]
        print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))
print("QUESTION (b-2 AC4): is each event ONE story about its own company, and does its lead name that story?")

print("\n=== PART 2: HELD-OUT NEAR-MISSES ===")
by_sec = {}
for r in out:
    if c.is_ab(r) and c.day(r) is not None:
        by_sec.setdefault(r["security_key"], []).append(r)
in_event = {(e["security_key"], k) for e in ho_events for k in e["article_keys"]}

print("\n-- 2a: the rule's own held-out stories with >= 2 tier-A/B articles that did not qualify --")
n2a = 0
for sec in sorted(by_sec):
    for story in pg._security_stories(by_sec[sec]):
        if len(story) >= 2 and not all((sec, r["article_key"]) in in_event for r in story):
            n2a += 1
            print("\n[2a-%d] %s: %d articles" % (n2a, sec, len(story)))
            for r in story:
                print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))
print("2a count: %d" % n2a)

print("\n-- 2b: same-security clusters of >= 2 distinct tier-A/B articles within the merge window, in no event --")
n2b = 0
for sec in sorted(by_sec):
    rs = sorted({r["article_key"]: r for r in by_sec[sec]}.values(), key=lambda r: (r["published_utc"], r["article_key"]))
    cls, cl = [], []
    for r in rs:
        if cl and (c.day(r) - c.day(cl[-1])).days <= pg.EVENT_MAX_GAP_DAYS + 1:
            cl.append(r)
        else:
            cls.append(cl)
            cl = [r]
    cls.append(cl)
    for cl in cls:
        if len(cl) >= 2:
            n2b += 1
            print("\n[2b-%d] %s: %d articles, tier-A %d" % (n2b, sec, len(cl), sum(1 for r in cl if r["signal_tier"] == "A")))
            for r in cl:
                print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))
print("2b count: %d" % n2b)
print("\nQUESTION (recall): is any of these a real burst of coverage ABOUT ITS OWN COMPANY that the rule declined?")

print("\n=== PART 3: EVERY HELD-OUT TIER-A/B ROW BY SECURITY (context) ===")
for sec in sorted(by_sec):
    rs = sorted(by_sec[sec], key=lambda r: r["published_utc"])
    print("\n%s (%d)" % (sec, len(rs)))
    for r in rs:
        print("     %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))

print("\nJUDGMENT PRESENTED, NO VERDICT RECORDED. For 3.0.0_SA_CVO~Z at L9: (1) is any held-out event ONE story about its own company, its lead naming it (none formed); (2) is any near-miss a real burst about its own company that the rule declined?")
