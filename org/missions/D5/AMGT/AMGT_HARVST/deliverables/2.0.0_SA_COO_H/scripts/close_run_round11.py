"""AMGT_HARVST round 11 -- the COO's ONE REAL RUN at close (/dispatch Step 5, report 2 C6).

The round served one outcome path: the rebuilt chatter_event gold (HVST-z-1) read through the newly
wired timeline routes (HVST-z-0). This calls the real entry point, `scoped_amgt.handler`, in-process
with the production loaders, for the validation security, AFTER the rebuild landed, and prints what a
caller of each route receives. It then compares the served events to the newest landed snapshot read
directly. READ-ONLY: S3 LIST/GET only. It does NOT exercise the gateway (row Z-W31-S1: unmounted).
"""
import json
import os
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402

KEY = "992_HK_Equity"
DAY = "2026-05-22"


def call(path, query=None):
    event = {"rawPath": path, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": query}
    t0 = time.time()
    resp = scoped_amgt.handler(event)
    return resp["statusCode"], json.loads(resp["body"]), time.time() - t0


base = "/api/scoped/amgt/security/%s/timeline" % KEY
status, body, secs = call(base)
print("GET %s -> HTTP %s in %.1fs" % (base, status, secs))
series = body.get("series") or []
events = body.get("events") or []
print("  series days: %d (%s .. %s)" % (len(series), series[0]["date"] if series else "-",
                                        series[-1]["date"] if series else "-"))
print("  events served: %d" % len(events))
for e in events:
    print("    %s..%s  articles=%s tierA=%s pubs=%s  lead=%r" % (
        e["first_day"], e["last_day"], e["articles_total"], e["tier_a"],
        e["publishers_distinct"], e["lead_headline"]))

rows = [r for r in pg._latest_gold_snapshot_rows("chatter_event") if r["security_key"] == KEY]
served_spans = sorted((str(e["first_day"]), str(e["last_day"])) for e in events)
gold_spans = sorted((str(r["first_day"]), str(r["last_day"])) for r in rows)
print("  newest landed chatter_event rows for %s: %d -> %s" % (KEY, len(rows), gold_spans))
print("  served spans == landed spans: %s" % (served_spans == gold_spans))
print("  removed spurious span 2026-06-01 absent from served: %s"
      % (("2026-06-01", "2026-06-01") not in served_spans))

day_path = "%s/day/%s" % (base, DAY)
status2, body2, secs2 = call(day_path)
arts = body2.get("articles") or []
print("GET %s -> HTTP %s in %.1fs" % (day_path, status2, secs2))
print("  articles: %d" % len(arts))
for a in arts:
    print("    %s  tier=%s  %r" % (a["publisher"], a["signal_tier"], a["headline"]))

ok = (status == 200 and status2 == 200 and served_spans == gold_spans
      and ("2026-06-01", "2026-06-01") not in served_spans and len(arts) > 0)
print("CLOSE RUN: %s" % ("OK" if ok else "NOT OK"))
sys.exit(0 if ok else 1)
