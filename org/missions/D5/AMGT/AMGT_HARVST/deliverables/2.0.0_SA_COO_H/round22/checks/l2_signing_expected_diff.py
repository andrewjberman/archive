"""AMGT_HARVST round 22 -- the issuer's signing read for HVST-l-2's never-widen COO half (read-only).

Builds chatter_event IN MEMORY exactly as publication_gold.build_event does (newest mention part, each row's title
from silver, event_rows) -- minus the write -- and sets it beside the SERVED newest event part: per served event
KEPT / CHANGED / GONE, every new event, every member with its guard status. Also prints the three newest gold keys and
ETags and both readers' state. S3 GET/LIST + Lambda GetFunctionConfiguration only. Writes nothing.
"""
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402

B = "opal-data-harvest"
s3 = boto3.client("s3")

for t in ("article_security_mention", "chatter_daily", "chatter_event"):
    objs = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="amgt/harvest/gold/%s/" % t):
        objs += [o for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]
    objs.sort(key=lambda o: o["Key"])
    print("NEWEST %-25s parts=%d %s ETag=%s" % (t, len(objs), objs[-1]["Key"].split("/", 4)[-1], objs[-1]["ETag"].strip('"')))
lam = boto3.client("lambda", region_name="us-east-1")
c = lam.get_function_configuration(FunctionName="opal-amgt-scoped-api")
print("READER opal-amgt-scoped-api CodeSha256=%s LastModified=%s" % (c["CodeSha256"], c["LastModified"]))
c = lam.get_function_configuration(FunctionName="amgt-resapp-chatter-axis")
print("READER amgt-resapp-chatter-axis CHATTER_AXIS_SOURCE=%s" % c["Environment"]["Variables"].get("CHATTER_AXIS_SOURCE"))

mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
titles = pg._headline_by_article_key()
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = titles.get(row.get("article_key"))
    enriched.append(row)
new = pg.event_rows(enriched)
served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
print("mention rows %d; served events %d; rebuilt events %d; rule EVENT_GUARD_CO_MENTIONS=%s"
      % (len(mention), len(served), len(new), pg.EVENT_GUARD_CO_MENTIONS))
by_member = {}
for e in new:
    for k in e.get("article_keys") or []:
        by_member.setdefault((e["security_key"], k), e)
counts = {"KEPT": 0, "CHANGED": 0, "GONE": 0}
touched = set()
for s in sorted(served, key=lambda r: (r["security_key"], str(r["first_day"]))):
    hits = {id(by_member[(s["security_key"], k)]): by_member[(s["security_key"], k)]
            for k in (s.get("article_keys") or []) if (s["security_key"], k) in by_member}
    if not hits:
        verdict, tgt = "GONE", None
    else:
        tgt = list(hits.values())[0]
        same = all(str(s.get(f)) == str(tgt.get(f)) for f in set(s) | set(tgt))
        verdict = "KEPT" if same and len(hits) == 1 else "CHANGED"
        touched |= set(hits)
    counts[verdict] += 1
    print("%-7s %s %s..%s n=%s lead=%r" % (verdict, s["security_key"], s["first_day"], s["last_day"], s.get("articles_total"),
                                           (s.get("lead_headline") or "")[:70]))
    if verdict == "CHANGED":
        print("    -> %s..%s n=%s id %s -> %s lead=%r" % (tgt["first_day"], tgt["last_day"], tgt.get("articles_total"),
                                                       s["event_id"][:12], tgt["event_id"][:12],
                                                       (tgt.get("lead_headline") or "")[:70]))
news = [e for e in new if id(e) not in touched]
print("COUNTS served=%d KEPT=%d CHANGED=%d GONE=%d NEW=%d rebuilt=%d distinct_ids=%d"
      % (len(served), counts["KEPT"], counts["CHANGED"], counts["GONE"], len(news), len(new),
         len({e["event_id"] for e in new})))
for e in news:
    print("NEW %s %s..%s n=%s lead=%r" % (e["security_key"], e["first_day"], e["last_day"], e.get("articles_total"),
                                          (e.get("lead_headline") or "")[:70]))
