"""HVST-c-1 AC2 -- the burst-shape census over the WHOLE harvest (all securities in the newest mention snapshot).
READ-ONLY (S3 GET only). Two run definitions are printed, both merged across gaps <= EVENT_MAX_GAP_DAYS empty days:
  (I)  A/B-DAY RUNS: consecutive days carrying ANY tier-A/B article (the broadest reading of a burst);
  (II) QUALIFYING-DAY RUNS: days passing the rule's own day test (>= 2 A/B rows AND >= 2 tier-A publishers),
       story grouping ignored (an upper bound on what a story-blind rule would see).
A burst EXCEEDS the served shape if it holds > 3 articles OR spans > 1 day (the ruling's test). The
LARGER shape the fixture plants is >= 5 articles over >= 2 days."""
import datetime

import _common as c
from _common import pg

rows, _n = c.load()
ab = [r for r in rows if c.is_ab(r) and c.day(r) is not None]
secs = sorted({r["security_key"] for r in rows})
by_sec = {}
for r in ab:
    by_sec.setdefault(r["security_key"], []).append(r)
print("denominator: %d mention rows over %d securities; %d tier-A/B rows over %d securities with A/B rows (%d distinct A/B (security, article) pairs)"
      % (len(rows), len(secs), len(ab), len(by_sec), len({(r["security_key"], r["article_key"]) for r in ab})))

# ---- per (security, day) distribution
sd = {}
for r in ab:
    sd.setdefault((r["security_key"], c.day(r)), {})[r["article_key"]] = r
dist = {}
for k, v in sd.items():
    dist[len(v)] = dist.get(len(v), 0) + 1
print("\n=== tier-A/B articles per (security, day): denominator %d (security, day) cells ===" % len(sd))
for n in sorted(dist):
    print("  %d article(s): %d cells" % (n, dist[n]))
over_day = [(k, v) for k, v in sd.items() if len(v) > 3]
print("cells exceeding 3 articles: %d" % len(over_day))
for (sec, d), v in sorted(over_day, key=lambda kv: kv[0]):
    print("  %s %s  %d articles  [%s]" % (sec, d, len(v), "in-sample" if sec in c.IN_SAMPLE else "HELD-OUT"))


def runs_of(days, gap=pg.EVENT_MAX_GAP_DAYS):
    out, cur = [], []
    for d in sorted(days):
        if cur and (d - cur[-1]).days - 1 <= gap:
            cur.append(d)
        else:
            if cur:
                out.append(cur)
            cur = [d]
    if cur:
        out.append(cur)
    return out


def census(label, qualifying_only):
    print("\n=== %s ===" % label)
    allruns = []
    for sec in sorted(by_sec):
        days = {}
        for (s, d), v in sd.items():
            if s != sec:
                continue
            if qualifying_only:
                pubs = {pg._row_publisher(x) for x in v.values() if x["signal_tier"] == "A"}
                if not (len(v) >= pg.EVENT_MIN_ARTICLES and len(pubs) >= pg.EVENT_MIN_PUBLISHERS):
                    continue
            days[d] = v
        for run in runs_of(days):
            first, last = run[0], run[-1]
            arts = {}
            for (s, d), v in sd.items():
                if s == sec and first <= d <= last:
                    arts.update(v)
            allruns.append((sec, first, last, (last - first).days + 1, len(arts),
                            sorted(arts.values(), key=lambda x: x["published_utc"])))
    print("denominator: %d merged runs over %d securities" % (len(allruns), len({r[0] for r in allruns})))
    shape = {}
    for _s, _f, _l, span, n, _a in allruns:
        shape[(n, span)] = shape.get((n, span), 0) + 1
    print("distribution (articles, days_span): count")
    for k in sorted(shape):
        print("  articles=%d days=%d : %d" % (k[0], k[1], shape[k]))
    exceed = [r for r in allruns if r[4] > 3 or r[3] > 1]
    print("runs exceeding 3 articles OR 1 day: %d" % len(exceed))
    for sec, first, last, span, n, arts in exceed:
        pubs_a = sorted({pg._row_publisher(x) for x in arts if x["signal_tier"] == "A"})
        print("  %s %s..%s  %d articles over %d day(s)  [%s]  tier-A publishers=%s"
              % (sec, first, last, n, span, "in-sample" if sec in c.IN_SAMPLE else "HELD-OUT", pubs_a))
        for x in arts:
            print("       %s %-8s %s | %s" % (x["signal_tier"], pg._row_publisher(x), x["published_utc"], x["title"]))
    large = [r for r in allruns if r[4] >= 5 and r[3] >= 2]
    print("runs of the LARGER shape (>= 5 articles over >= 2 days): %d (held-out: %d)"
          % (len(large), sum(1 for r in large if r[0] not in c.IN_SAMPLE)))
    return allruns, exceed, large


runs1, ex1, lg1 = census("(I) A/B-DAY RUNS (any tier-A/B article), gap <= %d day" % pg.EVENT_MAX_GAP_DAYS, False)
runs2, ex2, lg2 = census("(II) QUALIFYING-DAY RUNS (>=2 A/B rows and >=2 tier-A publishers that day, story-blind), gap <= %d day"
                         % pg.EVENT_MAX_GAP_DAYS, True)

# ---- (III) STORY-LEVEL census: the rule's own story grouping (pg._security_stories), the unit an event is made of
print("\n=== (III) STORY-LEVEL RUNS: the rule's own story grouping per security over the WHOLE snapshot (tier-A/B) ===")
stories = []
for sec in sorted(by_sec):
    for st in pg._security_stories(by_sec[sec]):
        ds = sorted({c.day(r) for r in st})
        for run in runs_of(ds):  # merged runs of the story's own days (gap <= EVENT_MAX_GAP_DAYS)
            arts = [r for r in st if run[0] <= c.day(r) <= run[-1]]
            stories.append((sec, run[0], run[-1], (run[-1] - run[0]).days + 1, len(arts), arts))
print("denominator: %d story-runs over %d securities" % (len(stories), len({x[0] for x in stories})))
shape3 = {}
for _s, _f, _l, span, n, _a in stories:
    shape3[(n, span)] = shape3.get((n, span), 0) + 1
print("distribution (articles, days_span): count")
for k in sorted(shape3):
    print("  articles=%d days=%d : %d" % (k[0], k[1], shape3[k]))
ex3 = [x for x in stories if x[4] > 3 or x[3] > 1]
print("story-runs exceeding 3 articles OR 1 day: %d" % len(ex3))
for sec, first, last, span, n, arts in ex3:
    pubs_a = sorted({pg._row_publisher(x) for x in arts if x["signal_tier"] == "A"})
    print("  %s %s..%s  %d articles over %d day(s)  [%s]  tier-A publishers=%s"
          % (sec, first, last, n, span, "in-sample" if sec in c.IN_SAMPLE else "HELD-OUT", pubs_a))
    for x in arts:
        print("       %s %-8s %s | %s" % (x["signal_tier"], pg._row_publisher(x), x["published_utc"], x["title"]))
lg3 = [x for x in stories if x[4] >= 5 and x[3] >= 2]
print("story-runs of the LARGER shape (>= 5 articles over >= 2 days): %d (held-out: %d)"
      % (len(lg3), sum(1 for x in lg3 if x[0] not in c.IN_SAMPLE)))

events = pg.event_rows(rows)
print("\n=== the rule's SERVED shape: event_rows over the whole snapshot (the served events) ===")
for e in events:
    print("  %s %s..%s articles=%d days=%d" % (e["security_key"], e["first_day"], e["last_day"], e["articles_total"], e["days_span"]))
print("largest served event: %d articles; longest: %d day(s); events exceeding 3 articles or 1 day: %d of %d"
      % (max(e["articles_total"] for e in events), max(e["days_span"] for e in events),
         sum(1 for e in events if e["articles_total"] > 3 or e["days_span"] > 1), len(events)))

print("\n=== VERDICT ===")
n_lg3 = len(lg3)
n_lg3_ho = sum(1 for x in lg3 if x[0] not in c.IN_SAMPLE)
print("bursts exceeding 3 articles or 1 day: %d story-runs (%d held-out); %d A/B-day runs (%d held-out; several stories chained, an upper bound); %d story-blind qualifying-day runs (%d held-out)"
      % (len(ex3), sum(1 for x in ex3 if x[0] not in c.IN_SAMPLE), len(ex1), sum(1 for r in ex1 if r[0] not in c.IN_SAMPLE),
         len(ex2), sum(1 for r in ex2 if r[0] not in c.IN_SAMPLE)))
print("of the LARGER shape (>=5 articles over >=2 days): %d story-runs (%d held-out); %d A/B-day runs (%d held-out); %d qualifying-day runs"
      % (n_lg3, n_lg3_ho, len(lg1), sum(1 for r in lg1 if r[0] not in c.IN_SAMPLE), len(lg2)))
if n_lg3 == 0:
    print("larger burst shape: UNEXERCISED (0 story-level bursts of >=5 articles over >=2 days); no held-out pass stands for it")
else:
    print("larger burst shape: EXERCISED (%d bursts; %d held-out)" % (n_lg3, n_lg3_ho))

# ---- planted fixture (mechanism test only)
print("\n" + "=" * 78)
print("FIXTURE -- MECHANISM TEST, NOT A HELD-OUT GRADE")
print("=" * 78)


def mk(i, pub, tier, dayn, hour, title):
    return {"security_key": "FIXT_US_Equity", "composite_figi": "FIXTURE", "article_key": "%s:fixture-%d" % (pub, i),
            "publisher": pub, "signal_tier": tier,
            "published_utc": datetime.datetime(2026, 9, dayn, hour, 0, tzinfo=datetime.timezone.utc), "title": title}


fx = [
    mk(1, "wsj", "A", 10, 9, "Zorbex Unveils Quantum Battery Plant in Ohio"),
    mk(2, "bbg", "A", 10, 12, "Zorbex Breaks Ground on Quantum Battery Plant"),
    mk(3, "wsj", "A", 11, 9, "Quantum Battery Plant Zorbex Announced Adds Jobs"),
    mk(4, "bbg", "A", 11, 14, "Zorbex Quantum Battery Plant Draws State Subsidy"),
    mk(5, "ft", "A", 12, 8, "Ohio Quantum Battery Plant Zorbex Faces Local Opposition"),
    mk(6, "sa", "B", 12, 10, "Zorbex Quantum Battery Plant: Analyst Roundup"),
]
print("planted: %d articles (tier-A %d, tier-B %d), 3 days (09-10..09-12), publishers %s, one story (Zorbex quantum battery plant)"
      % (len(fx), sum(1 for r in fx if r["signal_tier"] == "A"), sum(1 for r in fx if r["signal_tier"] == "B"),
         sorted({r["publisher"] for r in fx})))
fev = pg.event_rows(fx)
print("event_rows on the fixture: %d event(s)" % len(fev))
for e in fev:
    print("  %s %s..%s articles=%d (A=%d B=%d) days=%d publishers=%d lead=%s | %s"
          % (e["security_key"], e["first_day"], e["last_day"], e["articles_total"], e["tier_a"], e["tier_b"], e["days_span"],
             e["publishers_distinct"], e["lead_article_key"], e["lead_headline"]))
    print("  members: %s" % e["article_keys"])
ok = len(fev) == 1 and fev[0]["articles_total"] == 6 and fev[0]["days_span"] == 3
print("MECHANISM (variant 1, the story is the security's ONLY coverage): the rule %s the planted 6-article / 3-day story as ONE event of 6 articles over 3 days"
      % ("FORMS" if ok else "DOES NOT FORM"))
print("  story split into: %s" % [[r["article_key"] for r in st] for st in pg._security_stories(fx)])
print("  security-name stems the rule strips (5 tier-A headlines on 3 days): %s"
      % sorted(pg._security_name_tokens([(pg._story_tokens(r["title"]), c.day(r)) for r in fx if r["signal_tier"] == "A"])))

# variant 2: the SAME story among the security's other coverage, so the name is only "zorbex"
bg = [
    mk(11, "wsj", "A", 1, 9, "Zorbex Names New Chief Financial Officer"),
    mk(12, "bbg", "A", 3, 9, "Zorbex Shares Fall on Analyst Downgrade"),
    mk(13, "sa", "A", 5, 9, "Zorbex Board Approves Share Buyback"),
    mk(14, "ft", "A", 7, 9, "Zorbex Settles Patent Suit With Rival"),
    mk(15, "wsj", "A", 15, 9, "Zorbex Opens Office in Singapore"),
    mk(16, "bbg", "A", 17, 9, "Zorbex Raises Prices on Enterprise Plans"),
]
fx2 = fx + bg
print("\nvariant 2: the same six story articles plus %d unrelated tier-A Zorbex headlines on 6 other days" % len(bg))
print("  security-name stems stripped: %s"
      % sorted(pg._security_name_tokens([(pg._story_tokens(r["title"]), c.day(r)) for r in fx2 if r["signal_tier"] == "A"])))
fev2 = [e for e in pg.event_rows(fx2)]
print("event_rows on variant 2: %d event(s)" % len(fev2))
for e in fev2:
    print("  %s %s..%s articles=%d (A=%d B=%d) days=%d publishers=%d lead=%s | %s"
          % (e["security_key"], e["first_day"], e["last_day"], e["articles_total"], e["tier_a"], e["tier_b"], e["days_span"],
             e["publishers_distinct"], e["lead_article_key"], e["lead_headline"]))
    print("  members: %s" % e["article_keys"])
ok2 = len(fev2) == 1 and fev2[0]["articles_total"] == 6 and fev2[0]["days_span"] == 3
print("MECHANISM (variant 2): the rule %s the planted story as ONE event of 6 articles over 3 days"
      % ("FORMS" if ok2 else "DOES NOT FORM"))
print("  stories: %s" % [[r["article_key"] for r in st] for st in pg._security_stories(fx2)])
