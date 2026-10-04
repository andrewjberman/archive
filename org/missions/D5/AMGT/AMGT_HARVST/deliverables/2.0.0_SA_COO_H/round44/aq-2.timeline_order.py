"""HARVST round 44 HVST-aq-2 -- FWD-5 read: a company's timeline, a picked day, its articles listed strongest first.

READ ONLY: lambda:Invoke of `opal-amgt-scoped-api` (the served route; same event shape as round41/post_act_reads.py) and
reads of the newest gold `article_security_mention` snapshot. No write anywhere but this cell's evidence files.

THE SERVED ORDER KEY (read at HEAD, `lib/research/harvest/timeline_api._dissection_sort_key`, applied by `get_timeline_day`
-> `_serve_dissection`): (signal_tier A < B < C < D, mention_count DESC, published_utc earliest first). "Strongest first"
means: tier-A articles (the company is the subject) before B/C/D, then more mentions of the company before fewer, then the
earlier publication.

Per name (BA_US_Equity and the highest-volume other name in gold), the 3 days with the most gold mention rows (>= 5 each):
  1. the timeline route serves that day on its series (articles_total);
  2. the day route lists the articles; every listed article joins to its gold mention row by (article_key, security_key) and
     serves the gold row's signal_tier and mention_count;
  3. the listed order is non-decreasing in the order key (VIOLATIONS = adjacent pairs out of order);
  4. the day's served article count equals the gold mention rows for that (security, UTC day).
Writes `round44/aq-2.timeline_order.json`. Verdict line: `AQ-2 FWD-5 READ: PASS|FAIL`.
"""
import collections
import datetime
import json
import os
import subprocess
import sys

import boto3

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
FUNCTION, REGION = "opal-amgt-scoped-api", "us-east-1"
PREFIX = "/api/scoped/amgt"
TIER_RANK = {"A": 0, "B": 1, "C": 2, "D": 3}

from lib.research.harvest import publication_gold as pg  # noqa: E402


def call(lam, path, query=None):
    ev = {"rawPath": path, "headers": {"x-firm-id": "opal"}, "queryStringParameters": query,
          "requestContext": {"http": {"method": "GET", "path": path}}}
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode("utf-8"))
    parsed = json.loads(r["Payload"].read())
    try:
        body = json.loads(parsed.get("body") or "null")
    except ValueError:
        body = None
    return parsed.get("statusCode"), body, r.get("FunctionError")


def utc_iso(v):
    if isinstance(v, datetime.datetime):
        if v.tzinfo is not None:
            v = v.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return v.isoformat()
    return str(v)


def order_key(gold_row):
    return (TIER_RANK.get(gold_row.get("signal_tier"), len(TIER_RANK)), -(gold_row.get("mention_count") or 0),
            utc_iso(gold_row.get("published_utc")))


def read_day(lam, key, day, gold_by_key, gold_day_count):
    st, body, fe = call(lam, "%s/security/%s/timeline/day/%s" % (PREFIX, key, day))
    arts = (body or {}).get("articles") or []
    unjoined, field_mismatch, keys_seq = [], [], []
    for a in arts:
        g = gold_by_key.get(a.get("article_key"))
        if g is None:
            unjoined.append(a.get("article_key"))
            keys_seq.append(None)
            continue
        if a.get("signal_tier") != g.get("signal_tier") or a.get("mention_count") != g.get("mention_count"):
            field_mismatch.append(a.get("article_key"))
        keys_seq.append(order_key(g))
    pairs = [(i, keys_seq[i], keys_seq[i + 1]) for i in range(len(keys_seq) - 1)
             if keys_seq[i] is not None and keys_seq[i + 1] is not None]
    violations = [i for i, x, y in pairs if x > y]
    exact_ties = sum(1 for _, x, y in pairs if x == y)
    tiers = [a.get("signal_tier") for a in arts]
    out = {"security_key": key, "day": day, "status": st, "function_error": fe, "served_articles": len(arts),
           "gold_rows_that_day": gold_day_count, "count_equal": len(arts) == gold_day_count, "unjoined": unjoined,
           "served_tier_or_mentions_differ_from_gold": field_mismatch, "order_violations": len(violations),
           "violation_positions": violations, "exact_key_ties": exact_ties,
           "served_tier_sequence": "".join(t or "?" for t in tiers),
           "first_three": [{"tier": a.get("signal_tier"), "mention_count": a.get("mention_count"),
                            "published_utc": a.get("published_utc"), "headline": (a.get("headline") or "")[:90]}
                           for a in arts[:3]]}
    out["pass"] = (st == 200 and len(arts) >= 5 and out["count_equal"] and not unjoined and not field_mismatch
                   and not violations)
    return out


def main():
    lam = boto3.client("lambda", region_name=REGION)
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    per_sec = collections.Counter(r.get("security_key") for r in mention)
    other = next(k for k, _ in per_sec.most_common() if k != "BA_US_Equity")
    names = ["BA_US_Equity", other]
    out = {"read_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "function": FUNCTION,
           "order_key": "(signal_tier A<B<C<D, mention_count DESC, published_utc earliest first)",
           "order_key_source": "lib/research/harvest/timeline_api.py _dissection_sort_key via get_timeline_day",
           "gold_mention_rows": len(mention), "names": {}, "days": []}
    for key in names:
        rows = [r for r in mention if r.get("security_key") == key and r.get("published_utc") is not None]
        by_day = collections.Counter(pg._day_of(r["published_utc"]).isoformat() for r in rows)
        days = [d for d, n in by_day.most_common() if n >= 5][:3]
        gold_by_key = {r.get("article_key"): r for r in rows}
        st, tl, fe = call(lam, "%s/security/%s/timeline" % (PREFIX, key), {"from": min(days), "to": max(days)})
        series = {s.get("date"): s for s in ((tl or {}).get("series") or [])}
        out["names"][key] = {"gold_rows": len(rows), "timeline_status": st, "timeline_function_error": fe,
                             "days_picked": days,
                             "series_articles_total": {d: (series.get(d) or {}).get("articles_total") for d in days}}
        print("%s: gold rows %d; timeline status %s; days %s; series articles_total %s"
              % (key, len(rows), st, days, out["names"][key]["series_articles_total"]))
        for d in days:
            r = read_day(lam, key, d, gold_by_key, by_day[d])
            r["on_timeline_series"] = d in series
            r["pass"] = r["pass"] and r["on_timeline_series"]
            out["days"].append(r)
            print("  %s %s: status %s, served %d, gold %d, unjoined %d, tier/mentions differ %d, order violations %d, "
                  "exact ties %d, tiers %s -> %s"
                  % (key, d, r["status"], r["served_articles"], r["gold_rows_that_day"], len(r["unjoined"]),
                     len(r["served_tier_or_mentions_differ_from_gold"]), r["order_violations"], r["exact_key_ties"],
                     r["served_tier_sequence"], "PASS" if r["pass"] else "FAIL"))
    out["violations_total"] = sum(d["order_violations"] for d in out["days"])
    out["verdict"] = "PASS" if out["days"] and all(d["pass"] for d in out["days"]) else "FAIL"
    json.dump(out, open(os.path.join(HERE, "aq-2.timeline_order.json"), "w", encoding="utf-8"), indent=1, default=str)
    print("DAYS READ: %d; ORDER VIOLATIONS: %d" % (len(out["days"]), out["violations_total"]))
    print("AQ-2 FWD-5 READ: %s" % out["verdict"])
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
