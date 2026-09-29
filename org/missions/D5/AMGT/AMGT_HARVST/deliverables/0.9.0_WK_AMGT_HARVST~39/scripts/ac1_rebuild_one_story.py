"""HVST-b-2 AC1: rebuild chatter_event gold ONE STORY PER EVENT; the STOP limb on the SERVED plane.

THE ONE WRITING SCRIPT OF THIS CELL. It runs the EXISTING producer (`publication_gold.main build-event`,
the CLI code path) exactly ONCE: one conditional put (IfNoneMatch="*"), no delete of any kind, no other
table, no vendor call, no code change. Two guards, both BEFORE any put, so a re-run cannot add a second part:
  1. BEFORE state must be the signed pair's premise (5 parts, newest date=2026-09-29/part-20260929T002311Z.parquet
     with 8 events);
  2. the in-memory build must be the outcome the never-widen halves read from the merged rule (7 events;
     BA 2026-08-26 gone; the 7 others kept with the same span and the SAME lead).
Otherwise it refuses with exit 2 and NO PUT.
"""
import datetime
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SECURITIES = os.path.join(REPO, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~4/securities.json")
TABLE = pg.GOLD_EVENT_TABLE
EXPECT_PARTS = 5
EXPECT_NEWEST_SUFFIX = "date=2026-09-29/part-20260929T002311Z.parquet"
EXPECT_EVENTS = 8
EXPECT_AFTER = 7
SIX = [("992_HK_Equity", "2026-02-12"), ("992_HK_Equity", "2026-05-22"), ("992_HK_Equity", "2026-08-13"),
       ("COST_US_Equity", "2026-09-14"), ("HD_US_Equity", "2026-08-18"), ("NVDA_US_Equity", "2026-06-01")]
GONE = ("BA_US_Equity", "2026-08-26")
failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def list_parts(client):
    """{key: etag} for every parquet part, and the keys sorted by (date, key) as readers do."""
    etags = {}
    pfx = store.table_prefix("amgt", "gold", TABLE)
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=pfx):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                etags[o["Key"]] = o["ETag"]
    keys = sorted(etags, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))
    return etags, keys


def span(r):
    return "%s..%s" % (r["first_day"], r["last_day"])


client = store._default_client()

# ---- (a) BEFORE ------------------------------------------------------------------------------
before_etags, before_keys = list_parts(client)
before_newest = before_keys[-1]
before_rows = pg._latest_gold_snapshot_rows(TABLE, client=client)
print("(a) BEFORE: %d parquet parts under the prefix; newest key = s3://%s/%s" % (len(before_keys), store.HARVEST_BUCKET, before_newest))
for k in before_keys:
    print("      part: %s  ETag=%s" % (k, before_etags[k]))
print("(a) BEFORE newest snapshot event count = %d (expected %d)" % (len(before_rows), EXPECT_EVENTS))
for r in before_rows:
    print("      %-16s %s id=%s lead=%s" % (r["security_key"], span(r), r["event_id"], r["lead_article_key"]))
if len(before_keys) != EXPECT_PARTS or not before_newest.endswith(EXPECT_NEWEST_SUFFIX) or len(before_rows) != EXPECT_EVENTS:
    print("REFUSED: BEFORE state is not the signed premise (%d parts, newest ...%s, %d events). NO PUT MADE. File a BLOCKING row."
          % (EXPECT_PARTS, EXPECT_NEWEST_SUFFIX, EXPECT_EVENTS))
    sys.exit(2)

# ---- guard 2: the in-memory outcome must be the halves' expected outcome ----------------------------
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headlines = pg._headline_by_article_key(client=client)
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = headlines.get(row.get("article_key"))
    enriched.append(row)
row_of = {(r["security_key"], r["article_key"]): r for r in enriched}
predicted = pg.event_rows(enriched)


def tier_a_keys(ev):
    return frozenset(k for k in ev["article_keys"] if row_of[(ev["security_key"], k)]["signal_tier"] == "A")


served_by_span = {(r["security_key"], str(r["first_day"]), str(r["last_day"])): r for r in before_rows}
pred_by_span = {(e["security_key"], str(e["first_day"]), str(e["last_day"])): e for e in predicted}
expect_ok = len(predicted) == EXPECT_AFTER and len({e["event_id"] for e in predicted}) == EXPECT_AFTER
for key, s in served_by_span.items():
    p = pred_by_span.get(key)
    if (key[0], key[1]) == GONE:
        expect_ok = expect_ok and p is None
    else:
        expect_ok = expect_ok and p is not None and p["lead_article_key"] == s["lead_article_key"]
print("(a2) PRE-PUT in-memory outcome: %d events (expected %d), BA 2026-08-26 gone, the 7 others kept with unchanged lead: %s"
      % (len(predicted), EXPECT_AFTER, expect_ok))
if not expect_ok:
    print("REFUSED: the in-memory outcome is not the one the never-widen halves read. NO PUT MADE. File a BLOCKING row.")
    sys.exit(2)

# ---- (b) the producer, verbatim ---------------------------------------------------------------
receipts = []
_orig_write_gold = pg.write_gold


def _recording_write_gold(*a, **kw):
    receipt = _orig_write_gold(*a, **kw)
    receipts.append(receipt)
    print("(b) write_gold receipt: %s" % json.dumps(receipt, sort_keys=True))
    return receipt


pg.write_gold = _recording_write_gold
as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
argv = ["build-event", "--securities-json", SECURITIES, "--as-of", as_of]
print("(b) producer: publication_gold.main(%r)" % (argv,))
try:
    rc = pg.main(argv)  # prints the producer's own JSON line
except store.HarvestStoreError as exc:
    print("HarvestStoreError (READ-BACK MISMATCH branch), verbatim: %s" % exc)
    print("STOP: the distrusted object stays (no delete permitted); it is superseded later.")
    sys.exit(3)
print("(b) producer returned rc=%r; write_gold calls = %d" % (rc, len(receipts)))
check("exactly ONE put (one write_gold call)", len(receipts) == 1)
receipt = receipts[0]
check("receipt rows == %d" % EXPECT_AFTER, receipt["rows"] == EXPECT_AFTER,
      "rows=%s content_length=%s" % (receipt["rows"], receipt["content_length"]))

# ---- (c) AFTER, re-read from S3 -----------------------------------------------------------------
after_etags, after_keys = list_parts(client)
after_newest = after_keys[-1]
after_rows = pg._latest_gold_snapshot_rows(TABLE, client=client)
print("(c) AFTER: %d parquet parts; newest key = %s" % (len(after_keys), after_newest))
check("newest snapshot IS the one just written", after_newest == receipt["key"], "newest=%s receipt=%s" % (after_newest, receipt["key"]))
check("exactly one part added", len(after_keys) == len(before_keys) + 1 and set(before_keys) < set(after_keys),
      "%d -> %d" % (len(before_keys), len(after_keys)))
check("newest snapshot (via _latest_gold_snapshot_rows) carries %d events" % EXPECT_AFTER,
      len(after_rows) == EXPECT_AFTER, "n=%d" % len(after_rows))

# ---- (d) every prior served event -> what it became; the SIX ----------------------------------------
print("(d) every prior served event and what it became (denominator %d):" % len(before_rows))
fate_of = {}
for s in sorted(before_rows, key=lambda r: (r["security_key"], r["first_day"])):
    s_a = tier_a_keys(s)
    hits = [e for e in after_rows if e["security_key"] == s["security_key"]
            and any(k in s_a for k in e["article_keys"])]
    if not hits:
        fate = "GONE"
    elif len(hits) == 1:
        e = hits[0]
        fate = "KEPT (same span: %s, same tier-A membership: %s, lead unchanged: %s, articles_total %d -> %d, tier_a %d -> %d)" % (
            (e["first_day"], e["last_day"]) == (s["first_day"], s["last_day"]), tier_a_keys(e) == s_a,
            e["lead_article_key"] == s["lead_article_key"], s["articles_total"], e["articles_total"],
            s["tier_a"], e["tier_a"])
    else:
        fate = "SPLIT into %d" % len(hits)
    fate_of[(s["security_key"], str(s["first_day"]))] = (fate, hits)
    print("      %-16s %s  ->  %s" % (s["security_key"], span(s), fate))
served_six = {(r["security_key"], str(r["first_day"])): r for r in before_rows}
six_ok = 0
for key in SIX:
    s = served_six[key]
    hits = [e for e in after_rows if e["security_key"] == key[0] and (e["first_day"], e["last_day"]) == (s["first_day"], s["last_day"])]
    ok = len(hits) == 1 and tier_a_keys(hits[0]) == tier_a_keys(s)
    six_ok += 1 if ok else 0
    print("      SIX %-16s %s: exactly one served event with the same span and tier-A membership: %s" % (key[0], key[1], ok))
check("the SIX one-company events each EXACTLY ONE served event, same span, same tier-A membership", six_ok == 6, "%d of 6" % six_ok)
ba = fate_of.get(GONE, ("?", []))
print("(d) BA_US_Equity 2026-08-26 (expected gone): %s" % ba[0])
print("(d) new event_ids (all moved, 7 of 7?): %d of %d new ids absent from the prior snapshot"
      % (len({e["event_id"] for e in after_rows} - {r["event_id"] for r in before_rows}), len(after_rows)))

# ---- (e) ids unique --------------------------------------------------------------------------------
ids = [e["event_id"] for e in after_rows]
check("every event_id unique", len(ids) == len(set(ids)), "%d ids, %d distinct" % (len(ids), len(set(ids))))

# ---- (f) every prior part still exists with its ETag unchanged --------------------------------------
n_ok = 0
for k in before_keys:
    head = client.head_object(Bucket=store.HARVEST_BUCKET, Key=k)
    same_etag = head["ETag"] == before_etags[k] and after_etags.get(k) == before_etags[k]
    n_ok += 1 if same_etag else 0
    print("(f) %s ETag before=%s HEAD=%s unchanged=%s" % (k, before_etags[k], head["ETag"], same_etag))
check("ALL %d prior parts exist at their own keys with ETag unchanged" % len(before_keys), n_ok == len(before_keys), "%d of %d" % (n_ok, len(before_keys)))

print("S3 KEY WRITTEN: s3://%s/%s" % (store.HARVEST_BUCKET, receipt["key"]))
print("RESULT: %s (%d failure(s))" % ("FAIL" if failures else "PASS", len(failures)))
sys.exit(1 if failures else 0)
