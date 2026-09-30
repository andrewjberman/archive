"""HVST-z-0 AC1: both timeline routes serve REAL landed gold, proven against an independent read.

The routes are called in-process through `scoped_amgt.handler` (no seam patched -- the loaders are
the production ones). The independent read is `publication_gold._latest_gold_snapshot_rows`
called directly, then filtered and counted here with no route code in the path.
READ-ONLY: S3 LIST/GET only.
"""
import datetime
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import timeline_api  # noqa: E402

KEY = "992_HK_Equity"  # the validation security (SPEC_SECTION_timeline.md section 8)

# The spec's enumerated lists (SPEC_SECTION_timeline.md section 5), typed here from the spec text,
# NOT read from timeline_api, so the diff is spec vs served rather than module vs module.
SPEC_SERIES = ["date", "mention_score", "articles_total", "tier_a", "tier_b", "tier_c", "tier_d",
               "mention_count_total", "publishers_distinct", "trailing_7d_sum", "trailing_30d_sum",
               "cumulative_ytd", "data_status", "breakout_ratio", "z_score"]
SPEC_EVENT = ["first_day", "last_day", "days_span", "articles_total", "tier_a", "tier_b",
              "publishers_distinct", "lead_article_key", "lead_headline"]
SPEC_ARTICLE = ["article_key", "headline", "publisher", "signal_tier", "mention_count",
                "mention_in_title", "mention_in_lead", "published_utc", "published_precision"]
SPEC_RANGE_TOP = ["security_key", "floor_date", "series", "events"]
SPEC_DAY_TOP = ["security_key", "date", "data_status", "articles"]

failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def call(path, query=None):
    event = {"rawPath": path, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": query}
    resp = scoped_amgt.handler(event)
    return resp["statusCode"], json.loads(resp["body"])


def diff(label, served, spec):
    only_served = sorted(set(served) - set(spec))
    only_spec = sorted(set(spec) - set(served))
    print("  %s: served=%d spec=%d served-minus-spec=%s spec-minus-served=%s"
          % (label, len(set(served)), len(set(spec)), only_served, only_spec))
    check("%s field set equals spec, both directions" % label, not only_served and not only_spec)


# ---- proof the loaders are the production ones, and where they read -------------------------
print("loaders are production: scoped_amgt._timeline_snapshot_rows defined in %s, reads via "
      "publication_gold._latest_gold_snapshot_rows" % scoped_amgt._timeline_snapshot_rows.__module__)
client = store._default_client()
for table in ("chatter_daily", "chatter_event", "article_security_mention"):
    pfx = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=pfx):
        keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    newest = sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
    print("newest landed snapshot of %s (%d parts listed): s3://%s/%s" % (table, len(keys), store.HARVEST_BUCKET, newest))

# ---- INDEPENDENT READ (no route code) ---------------------------------------------------------
ind_daily = [r for r in pg._latest_gold_snapshot_rows("chatter_daily") if r["security_key"] == KEY]
ind_event = [r for r in pg._latest_gold_snapshot_rows("chatter_event") if r["security_key"] == KEY]
ind_mention = [r for r in pg._latest_gold_snapshot_rows("article_security_mention") if r["security_key"] == KEY]
days = sorted(r["day"] for r in ind_daily)
print("independent read: %s chatter_daily rows=%d (first=%s last=%s) chatter_event rows=%d mention rows=%d"
      % (KEY, len(ind_daily), days[0], days[-1], len(ind_event), len(ind_mention)))

# ---- ROUTE 1: range ---------------------------------------------------------------------------
path1 = "/api/scoped/amgt/security/%s/timeline" % KEY
status, body = call(path1)
print("\nROUTE 1: GET %s -> HTTP %d" % (path1, status))
check("range route HTTP 200 and no error key", status == 200 and "error" not in body)
diff("range top-level keys", body.keys(), SPEC_RANGE_TOP)
diff("series entry", body["series"][0].keys(), SPEC_SERIES)
check("every series entry has exactly the spec fields",
      all(set(e) == set(SPEC_SERIES) for e in body["series"]))
if body["events"]:
    diff("event entry", body["events"][0].keys(), SPEC_EVENT)
    check("every event entry has exactly the spec fields", all(set(e) == set(SPEC_EVENT) for e in body["events"]))

served_days = [e["date"] for e in body["series"]]
floor = datetime.date(2026, 1, 1)
in_range = (days[-1] - floor).days + 1
print("  dense day count served=%d, days-in-range denominator (%s..%s)=%d" % (len(served_days), floor, days[-1], in_range))
check("dense: served day count equals days-in-range (no gap)", len(served_days) == in_range)
expected_days = [(floor + datetime.timedelta(days=i)).isoformat() for i in range(in_range)]
check("dense: served dates are exactly every calendar day from the floor", served_days == expected_days)

print("  INDEPENDENT: day count read directly=%d, served=%d; event count read directly=%d, served=%d"
      % (len(ind_daily), len(served_days), len(ind_event), len(body["events"])))
check("day count agrees with the independent read", len(ind_daily) == len(served_days))
check("event count agrees with the independent read", len(ind_event) == len(body["events"]))
ind_by_day = {r["day"].isoformat(): r for r in ind_daily}
stored = [f for f in timeline_api.SERIES_STORED_FIELDS if f != "date"]
mism = [e["date"] for e in body["series"] if any(e[f] != ind_by_day[e["date"]][f] for f in stored)]
check("every served stored field equals the independently-read row (%d days compared)" % len(body["series"]),
      not mism, "mismatched=%s" % mism[:5])
ind_ev = sorted((r["first_day"].isoformat(), r["last_day"].isoformat(), r["lead_headline"]) for r in ind_event)
srv_ev = sorted((e["first_day"], e["last_day"], e["lead_headline"]) for e in body["events"])
check("served events equal independently-read events (first_day, last_day, lead_headline)", ind_ev == srv_ev)
print("  sum(articles_total) served=%d independent=%d"
      % (sum(e["articles_total"] for e in body["series"]), sum(r["articles_total"] for r in ind_daily)))

s2, b2 = call(path1, {"from": "2026-09-01", "to": "2026-09-15"})
print("  sub-range from=2026-09-01 to=2026-09-15: HTTP %d, served days=%d, denominator=15" % (s2, len(b2["series"])))
check("sub-range dense: 15 of 15", s2 == 200 and len(b2["series"]) == 15)

# ---- ROUTE 2: day -----------------------------------------------------------------------------
busy = sorted([r for r in ind_daily if r["articles_total"] > 0], key=lambda r: (-r["articles_total"], r["day"]))[0]
day = busy["day"].isoformat()
path2 = "/api/scoped/amgt/security/%s/timeline/day/%s" % (KEY, day)
status, b3 = call(path2)
print("\nROUTE 2: GET %s -> HTTP %d" % (path2, status))
check("day route HTTP 200 and no error key", status == 200 and "error" not in b3)
diff("day top-level keys", b3.keys(), SPEC_DAY_TOP)
diff("article entry", b3["articles"][0].keys(), SPEC_ARTICLE)
check("every article entry has exactly the spec fields", all(set(a) == set(SPEC_ARTICLE) for a in b3["articles"]))
ind_day_arts = [r for r in ind_mention if pg._day_of(r["published_utc"]).isoformat() == day]
print("  INDEPENDENT: articles on %s read directly=%d, served=%d, chatter_daily articles_total=%d"
      % (day, len(ind_day_arts), len(b3["articles"]), busy["articles_total"]))
check("article count agrees with the independent read", len(ind_day_arts) == len(b3["articles"]))
check("article keys equal the independent read",
      sorted(a["article_key"] for a in b3["articles"]) == sorted(r["article_key"] for r in ind_day_arts))
check("every served headline is joined (non-empty)", all(a["headline"] for a in b3["articles"]))
tiers = [a["signal_tier"] for a in b3["articles"]]
check("strongest-first: tier order non-decreasing A..D", tiers == sorted(tiers))
print("  first rows: %s" % [(a["signal_tier"], a["mention_count"], (a["headline"] or "")[:50]) for a in b3["articles"][:3]])

print("\nRESULT: %s (%d failing checks)" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(1 if failures else 0)
