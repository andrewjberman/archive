"""HVST-ak-3 event-density census. READ-ONLY: no S3 write, no repo edit."""
import datetime
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

OUT = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~91/ak3_event_density.json")


def newest_key(client, table):
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                keys.append(o["Key"])
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1] if keys else None


def main():
    client = store._default_client()
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
    daily = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE, client=client)
    served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
    served_part = newest_key(client, pg.GOLD_EVENT_TABLE)

    hl = pg._headline_by_article_key(client=client)
    enriched = []
    for r in mention:
        r = dict(r)
        r["title"] = hl.get(r.get("article_key"))
        enriched.append(r)
    dry = pg.event_rows(enriched)

    cnt = defaultdict(dict)
    for r in daily:
        cnt[r["security_key"]][r["day"]] = r["articles_total"] or 0

    def spans(events):
        s = defaultdict(list)
        for e in events:
            s[e["security_key"]].append((e["first_day"], e["last_day"]))
        return s
    sp_dry, sp_srv = spans(dry), spans(served)

    def covered(sp, sk, d):
        return any(a <= d <= b for a, b in sp.get(sk, []))

    one = datetime.timedelta(days=1)
    spike = {"2x": 0, "3x": 0}
    cov = {"2x": 0, "3x": 0}
    cov_srv = {"2x": 0, "3x": 0}
    uncovered = {"2x": [], "3x": []}
    spike_list = []
    for sk, days in cnt.items():
        for d, n in days.items():
            if n < 3:
                continue
            base = sum(days.get(d - one * i, 0) for i in range(1, 31)) / 30.0
            for label, k in (("2x", 2), ("3x", 3)):
                if n >= k * base:
                    spike[label] += 1
                    c = covered(sp_dry, sk, d)
                    cov[label] += c
                    cov_srv[label] += covered(sp_srv, sk, d)
                    if not c:
                        uncovered[label].append((sk, d, n, base))
                    if label == "2x":
                        spike_list.append((sk, d))

    # suppression reasons for uncovered spikes (measured from event_rows' own rules, no code change)
    ab = defaultdict(list)
    for r in enriched:
        if r.get("signal_tier") in ("A", "B") and r.get("published_utc") is not None:
            ab[(r["security_key"], pg._day_of(r["published_utc"]))].append(r)

    def reason(sk, d):
        rows = ab.get((sk, d), [])
        if not rows:
            return "no_tier_AB_mention_that_day"
        if all(pg._is_guarded(r) for r in rows):
            return "all_AB_rows_guarded_roundup_no_span"
        if len(rows) < pg.EVENT_MIN_ARTICLES:
            return "below_min_articles_%d_that_day" % pg.EVENT_MIN_ARTICLES
        if len({pg._row_publisher(r) for r in rows if r.get("signal_tier") == "A"}) < pg.EVENT_MIN_PUBLISHERS:
            return "below_min_tierA_publishers_%d_that_day" % pg.EVENT_MIN_PUBLISHERS
        return "thresholds_met_by_day_but_no_event_story_split_or_headline_link"
    reasons = {}
    for label in ("2x", "3x"):
        reasons[label] = dict(Counter(reason(sk, d) for sk, d, n, b in uncovered[label]))

    out = {
        "securities": len({r["security_key"] for r in mention}),
        "mention_rows_read": len(mention),
        "chatter_daily_rows_read": len(daily),
        "served_event_part": served_part,
        "events_served": len(served),
        "events_dry_built": len(dry),
        "puts_sent": 0,
        "spike_definition": "articles_total>=3 and >=k x mean articles_total over prior 30 calendar days (missing=0); k in 2,3",
        "spike_days": spike,
        "spike_days_covered": cov,
        "spike_days_covered_served": cov_srv,
        "uncovered_reasons": reasons,
        "uncovered_examples_2x": [{"security_key": sk, "day": d.isoformat(), "count": n, "baseline": round(b, 3)}
                                  for sk, d, n, b in sorted(uncovered["2x"], key=lambda x: -x[2])[:10]],
        "uncovered_examples_3x": [{"security_key": sk, "day": d.isoformat(), "count": n, "baseline": round(b, 3)}
                                  for sk, d, n, b in sorted(uncovered["3x"], key=lambda x: -x[2])[:10]],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if not k.startswith("uncovered_examples")}, indent=1, sort_keys=True))
    print("DENSITY CENSUS: DONE")


if __name__ == "__main__":
    main()
