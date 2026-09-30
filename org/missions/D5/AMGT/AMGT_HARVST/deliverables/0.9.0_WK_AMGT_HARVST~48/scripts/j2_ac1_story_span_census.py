"""HVST-j-2 AC1 -- THE STORY-SPAN CENSUS (row Z-W41-S1). MEASUREMENT ONLY: S3 LIST/GET only; no put, no delete,
no vendor call, no lib/ edit, no gold write. The CTO rules the rule at round 20's analysis; this script records NO
verdict on whether the candidate is right.

CANDIDATE SPAN RULE (lives ONLY in this file; `candidate_event_rows` below):
  "SAME STORY" = exactly the served rule's story test: `publication_gold._security_stories` -- one security's tier
      A/B mention rows linked by headline-term overlap (name stems dropped, earnings class terms, tight-cluster
      refusal, link window max_gap_days + 1 = 2 days). Not re-implemented, called.
  "CONSECUTIVE"   = a story-day is a UTC day (`publication_gold._day_of`) on which the story has at least one
      tier A or B article. Two story-days are consecutive when the number of EMPTY days between them is at most
      `publication_gold.EVENT_MAX_GAP_DAYS` (= 1, the served rule's own section-1b tolerance). A maximal chain of
      consecutive story-days is ONE story-run.
  THE CANDIDATE: each story-run is ONE event iff the RUN AS A WHOLE qualifies under the served thresholds
      (>= EVENT_MIN_ARTICLES tier A/B articles, from >= EVENT_MIN_PUBLISHERS distinct publishers that each
      contribute at least one tier-A article of the run). Its span is [first story-day, last story-day]; its
      members are every tier A/B article of the story on those days; its lead is the earliest tier-A article
      (`_event_sort_key`, as served); its event_id is `publication_gold._event_id` of (security, first, last, lead).
  WHAT DIFFERS FROM THE SERVED RULE: the served rule tests qualification PER DAY and spans only from qualifying
      day to qualifying day; the candidate tests it per RUN and spans the whole run. Story test, thresholds,
      lead, ordering, id function and tier filter are the served ones.
  An informational sensitivity line is also printed at gap 0 (strictly calendar-adjacent story-days).

INPUTS (today's, nothing rebuilt): the newest served article_security_mention part + silver headlines
(`publication_gold._iter_latest_articles`), through the producer's own readers; compared with the newest served
chatter_event part."""
import datetime
import io
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "..", "j2_census_result.json")
FIXTURE_SEC = "AMZN_US_Equity"


def a(text, n=None):
    s = ("" if text is None else str(text)).encode("ascii", "backslashreplace").decode("ascii")
    return s[:n] if n else s


def canon(v):
    if isinstance(v, datetime.datetime):
        return v.astimezone(datetime.timezone.utc).isoformat() if v.tzinfo else v.isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, (list, tuple)):
        return [canon(x) for x in v]
    return v


def newest_part(client, table):
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    keys.sort(key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))
    return keys[-1], len(keys)


def read_rows(client, key):
    raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def candidate_event_rows(mention_rows, gap=pg.EVENT_MAX_GAP_DAYS, min_articles=pg.EVENT_MIN_ARTICLES,
                         min_publishers=pg.EVENT_MIN_PUBLISHERS):
    """The CANDIDATE (see the module header). Same skeleton as `publication_gold.event_rows`; only the span
    joining differs: qualification per story-RUN, span = the whole run."""
    by_security, figi = {}, {}
    for row in mention_rows:
        if row.get("signal_tier") not in pg._EVENT_QUALIFYING_TIERS:
            continue
        if pg._day_of(row.get("published_utc")) is None:
            continue
        by_security.setdefault(row.get("security_key"), []).append(row)
        if row.get("security_key") not in figi and row.get("composite_figi") is not None:
            figi[row.get("security_key")] = row.get("composite_figi")
    events = []
    for sec in sorted(by_security):
        for story in pg._security_stories(by_security[sec], gap):
            day_rows = {}
            for row in story:
                day_rows.setdefault(pg._day_of(row.get("published_utc")), []).append(row)
            days = sorted(day_rows)
            runs, start, end = [], days[0], days[0]
            for d in days[1:]:
                if (d - end).days - 1 <= gap:
                    end = d
                else:
                    runs.append((start, end))
                    start = end = d
            runs.append((start, end))
            for first_day, last_day in runs:
                members = []
                for d in pg._date_range(first_day, last_day):
                    members.extend(day_rows.get(d, []))
                members.sort(key=pg._event_sort_key)
                if len(members) < min_articles:
                    continue
                if len({pg._row_publisher(r) for r in members if r.get("signal_tier") == "A"}) < min_publishers:
                    continue
                lead = members[0]
                events.append({
                    "event_id": pg._event_id(sec, first_day, last_day, lead.get("article_key")),
                    "security_key": sec, "composite_figi": figi.get(sec),
                    "first_day": first_day, "last_day": last_day, "days_span": (last_day - first_day).days + 1,
                    "articles_total": len(members),
                    "tier_a": sum(1 for r in members if r.get("signal_tier") == "A"),
                    "tier_b": sum(1 for r in members if r.get("signal_tier") == "B"),
                    "publishers_distinct": len({pg._row_publisher(r) for r in members}),
                    "lead_article_key": lead.get("article_key"), "lead_headline": lead.get("title"),
                    "article_keys": [r.get("article_key") for r in members],
                })
    events.sort(key=lambda e: (e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"]))
    return events


def classify(served, cand):
    """{served event_id: (status, [candidate ids touching it])}, plus the NEW candidate ids.
    KEPT = one candidate, same event_id and same members; MERGED = a candidate holding this and >= 1 other
    served event; CHANGED = touched by candidate(s) but not KEPT or MERGED; GONE = no candidate shares an article."""
    s_sets = {e["event_id"]: set(e["article_keys"]) for e in served}
    c_sets = {e["event_id"]: set(e["article_keys"]) for e in cand}
    out, merged_cands = {}, set()
    for c_id, c_set in c_sets.items():
        if sum(1 for s in s_sets.values() if s & c_set) >= 2:
            merged_cands.add(c_id)
    for s in served:
        touch = [c_id for c_id, c_set in c_sets.items() if c_set & s_sets[s["event_id"]]]
        if not touch:
            st = "GONE"
        elif any(t in merged_cands for t in touch):
            st = "MERGED"
        elif len(touch) == 1 and touch[0] == s["event_id"] and c_sets[touch[0]] == s_sets[s["event_id"]]:
            st = "KEPT"
        else:
            st = "CHANGED"
        out[s["event_id"]] = (st, touch)
    new_ids = [c_id for c_id, c_set in c_sets.items() if not any(c_set & s for s in s_sets.values())]
    return out, new_ids, merged_cands


def main():
    client = store._default_client()
    ev_key, ev_parts = newest_part(client, pg.GOLD_EVENT_TABLE)
    mn_key, mn_parts = newest_part(client, pg.GOLD_TABLE)
    served = read_rows(client, ev_key)
    mention = read_rows(client, mn_key)
    arts = {r["article_key"]: r for r in pg._iter_latest_articles(client=client)}
    enriched = [dict(r, title=arts.get(r["article_key"], {}).get("title")) for r in mention]
    title = lambda k: arts.get(k, {}).get("title")  # noqa: E731
    row_of = {(r["article_key"], r["security_key"]): r for r in mention}

    print("== HVST-j-2 AC1: THE STORY-SPAN CENSUS (row Z-W41-S1) -- measurement only, no verdict ==")
    print("inputs: served event part %s (%d parts; %d events)" % (ev_key, ev_parts, len(served)))
    print("        served mention part %s (%d parts; %d rows; tier A/B rows %d); silver articles %d" % (
        mn_key, mn_parts, len(mention), sum(1 for r in mention if r["signal_tier"] in ("A", "B")), len(arts)))
    print("        titled mention rows: %d of %d" % (sum(1 for r in enriched if r["title"]), len(enriched)))

    # ---------------- (a) BASELINE ----------------
    current = pg.event_rows(enriched)
    current_rt = pa.Table.from_pylist(current, schema=pg.GOLD_EVENT_SCHEMA).to_pylist()
    s_by = {r["event_id"]: r for r in served}
    c_by = {r["event_id"]: r for r in current_rt}
    diffs = []
    for k in sorted(set(s_by) | set(c_by)):
        x, y = s_by.get(k), c_by.get(k)
        if x is None or y is None:
            diffs.append("event_id %s only in %s" % (k[:12], "served" if y is None else "current-rule rebuild"))
            continue
        for f in sorted(set(x) | set(y)):
            if canon(x.get(f)) != canon(y.get(f)):
                diffs.append("event %s field %s: served=%s rebuild=%s" % (k[:12], f, a(canon(x.get(f))), a(canon(y.get(f)))))
    n_equal = sum(1 for k in s_by if k in c_by and not any(canon(s_by[k].get(f)) != canon(c_by[k].get(f)) for f in set(s_by[k]) | set(c_by[k])))
    base_ok = (not diffs and len(s_by) == len(served) and len(c_by) == len(current_rt) and len(served) == len(current_rt))
    print("\n== (a) BASELINE: event_rows under the CURRENT rule vs the SERVED newest chatter_event part ==")
    print("served events=%d (distinct ids %d); current-rule rebuild events=%d (distinct ids %d)" % (
        len(served), len(s_by), len(current_rt), len(c_by)))
    print("(a) baseline row-by-row equal: %d of %d served events equal in every field" % (n_equal, len(served)))
    for d in diffs:
        print("   DIFF %s" % d)
    print("(a) %s" % ("HOLDS" if base_ok else "FAILS -- CENSUS INVALID"))

    # ---------------- (b) candidate ----------------
    print("\n== (b) THE CANDIDATE RULE, verbatim ==")
    for line in __doc__.split("CANDIDATE SPAN RULE", 1)[1].split("INPUTS (today's", 1)[0].splitlines():
        print("   " + ("CANDIDATE SPAN RULE" + line if line == " (lives ONLY in this file; `candidate_event_rows` below):" else line))

    cand = candidate_event_rows(enriched)
    cand_rt = pa.Table.from_pylist(cand, schema=pg.GOLD_EVENT_SCHEMA).to_pylist()
    cand0 = candidate_event_rows(enriched, gap=0)

    def members(e):
        for k in e["article_keys"]:
            r = row_of[(k, e["security_key"])]
            print("      - %s | tier %s | %s | %s | %s" % (pg._day_of(r["published_utc"]), r["signal_tier"], r["publisher"], a(title(k), 110), a(k.split("|")[0][:24])))

    def show(e, tag):
        print("   %s event %s %s span %s..%s (days_span=%d) articles=%d tier_a=%d tier_b=%d publishers=%d" % (
            tag, e["event_id"][:12], e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"],
            e["tier_a"], e["tier_b"], e["publishers_distinct"]))
        print("      lead: %s" % a(e["lead_headline"]))
        members(e)

    # ---------------- (c) fixture ----------------
    print("\n== (c) THE AMZN FIXTURE (%s) ==" % FIXTURE_SEC)
    amzn_rows = [r for r in enriched if r["security_key"] == FIXTURE_SEC and r["signal_tier"] in ("A", "B")]
    stories = pg._security_stories(amzn_rows)
    print("AMZN tier A/B rows=%d; stories under the served story test=%d (informational -- the candidate reuses these)" % (len(amzn_rows), len(stories)))
    for i, st in enumerate(stories):
        print("   story %d: %d rows, days %s..%s" % (i, len(st), pg._day_of(st[0]["published_utc"]), max(pg._day_of(r["published_utc"]) for r in st)))
        for r in st:
            print("      . %s | tier %s | %s | %s" % (pg._day_of(r["published_utc"]), r["signal_tier"], r["publisher"], a(r["title"], 100)))
    cur_amzn = [e for e in current_rt if e["security_key"] == FIXTURE_SEC]
    cand_amzn = [e for e in cand_rt if e["security_key"] == FIXTURE_SEC]
    print("AMZN events under the CURRENT rule: %d" % len(cur_amzn))
    for e in cur_amzn:
        show(e, "CURRENT")
    print("AMZN events under the CANDIDATE: %d" % len(cand_amzn))
    for e in cand_amzn:
        show(e, "CANDIDATE")
    print("(informational sensitivity, gap 0 = strictly calendar-adjacent story-days) AMZN events: %d" % len([e for e in cand0 if e["security_key"] == FIXTURE_SEC]))
    for e in cand0:
        if e["security_key"] == FIXTURE_SEC:
            print("   gap0 event %s span %s..%s articles=%d lead: %s" % (e["event_id"][:12], e["first_day"], e["last_day"], e["articles_total"], a(e["lead_headline"], 80)))

    # ---------------- (d) delta ----------------
    print("\n== (d) THE SERVED-EVENT DELTA under the candidate (denominator %d served events) ==" % len(served))
    status, new_ids, merged_cands = classify(served, cand_rt)
    c_by_id = {e["event_id"]: e for e in cand_rt}
    counts = {"KEPT": 0, "MERGED": 0, "CHANGED": 0, "GONE": 0}
    for s in served:
        st, touch = status[s["event_id"]]
        counts[st] += 1
        print("   %-7s %s %s served span %s..%s articles=%d -> candidate %s" % (
            st, s["event_id"][:12], s["security_key"], s["first_day"], s["last_day"], s["articles_total"],
            ", ".join("%s(%s..%s,%d)" % (t[:12], c_by_id[t]["first_day"], c_by_id[t]["last_day"], c_by_id[t]["articles_total"]) for t in touch) or "-"))
    print("   COUNTS of %d served: KEPT=%d MERGED=%d CHANGED=%d GONE=%d  (sum %d); NEW candidate events=%d; candidate events total=%d" % (
        len(served), counts["KEPT"], counts["MERGED"], counts["CHANGED"], counts["GONE"], sum(counts.values()), len(new_ids), len(cand_rt)))
    print("   MERGED candidate events (one candidate holding >= 2 served events): %d" % len(merged_cands))
    listed = [c for c in cand_rt if c["event_id"] in merged_cands] + [c for c in cand_rt if c["event_id"] in new_ids]
    changed_cands = {t for s in served for t in status[s["event_id"]][1] if status[s["event_id"]][0] == "CHANGED"}
    print("   members of every NEW, MERGED (and, for completeness, CHANGED) candidate event:")
    for c in listed:
        show(c, "MERGED" if c["event_id"] in merged_cands else "NEW")
        if c["event_id"] in merged_cands:
            print("      merges served events: %s" % ", ".join(s["event_id"][:12] for s in served if set(s["article_keys"]) & set(c["article_keys"])))
    for c in cand_rt:
        if c["event_id"] in changed_cands and c["event_id"] not in merged_cands:
            show(c, "CHANGED")
    if not listed and not changed_cands:
        print("   (none: 0 NEW, 0 MERGED, 0 CHANGED of %d served)" % len(served))
    for s in served:
        st, touch = status[s["event_id"]]
        if st == "GONE":
            print("   GONE served event members:")
            print("      %s %s" % (s["event_id"][:12], s["security_key"]))
    st0, new0, mg0 = classify(served, cand0)
    c0 = {k: 0 for k in counts}
    for v in st0.values():
        c0[v[0]] += 1
    print("   (informational sensitivity, gap 0) COUNTS of %d served: KEPT=%d MERGED=%d CHANGED=%d GONE=%d; NEW=%d" % (
        len(served), c0["KEPT"], c0["MERGED"], c0["CHANGED"], c0["GONE"], len(new0)))

    # ---------------- (e) uniqueness ----------------
    ids = [e["event_id"] for e in cand_rt]
    uniq = len(ids) == len(set(ids))
    print("\n== (e) EVENT_ID UNIQUENESS under the candidate ==")
    print("(e) candidate events=%d, distinct event_ids=%d -> %s" % (len(ids), len(set(ids)), "UNIQUE" if uniq else "DUPLICATES"))
    # a candidate must not put one article in two events of the same security
    seen, dup = {}, 0
    for e in cand_rt:
        for k in e["article_keys"]:
            if (e["security_key"], k) in seen:
                dup += 1
            seen[(e["security_key"], k)] = e["event_id"]
    print("    (informational) article memberships shared by two candidate events of one security: %d" % dup)

    result = {"served_event_key": ev_key, "served_mention_key": mn_key, "baseline_equal": n_equal, "served_events": len(served),
              "baseline_ok": base_ok, "counts": counts, "new": len(new_ids), "merged_candidate_events": len(merged_cands),
              "candidate_events": len(cand_rt), "ids_unique": uniq,
              "amzn_current": [{"span": [str(e["first_day"]), str(e["last_day"])], "articles": e["articles_total"]} for e in cur_amzn],
              "amzn_candidate": [{"span": [str(e["first_day"]), str(e["last_day"])], "articles": e["articles_total"]} for e in cand_amzn]}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\nAC1 RESULT: %s" % ("PASS" if (base_ok and uniq) else "FAIL%s" % ("" if base_ok else " (baseline INVALID)")))
    return 0 if (base_ok and uniq) else 1


if __name__ == "__main__":
    sys.exit(main())
