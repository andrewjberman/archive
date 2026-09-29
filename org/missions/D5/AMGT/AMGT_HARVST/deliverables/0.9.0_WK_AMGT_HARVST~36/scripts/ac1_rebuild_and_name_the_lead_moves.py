"""HVST-a-4 AC1: rebuild chatter_event gold with the plurality lead and name the lead moves.

THE ONE WRITING SCRIPT OF THIS CELL. It runs the EXISTING producer (`publication_gold.main build-event`,
the CLI code path) exactly ONCE: one conditional put (IfNoneMatch="*"), no delete of any kind, no other
table, no vendor call. Guard: if the BEFORE state is not the signed pair's premise (4 parts, newest
date=2026-09-28/part-20260928T210944Z.parquet with 8 events) it refuses BEFORE any put, so a re-run cannot
add a second snapshot.
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
EXPECT_PARTS = 4
EXPECT_NEWEST_SUFFIX = "date=2026-09-28/part-20260928T210944Z.parquet"
EXPECT_EVENTS = 8
FIELDS = ["event_id", "security_key", "composite_figi", "first_day", "last_day", "days_span",
          "articles_total", "tier_a", "tier_b", "publishers_distinct", "article_keys"]
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
    print("      %-16s %s id=%s" % (r["security_key"], span(r), r["event_id"]))
if len(before_keys) != EXPECT_PARTS or not before_newest.endswith(EXPECT_NEWEST_SUFFIX) or len(before_rows) != EXPECT_EVENTS:
    print("REFUSED: BEFORE state is not the signed premise (%d parts, newest ...%s, %d events). NO PUT MADE. File a BLOCKING row."
          % (EXPECT_PARTS, EXPECT_NEWEST_SUFFIX, EXPECT_EVENTS))
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
check("receipt rows == 8", receipt["rows"] == 8, "rows=%s content_length=%s" % (receipt["rows"], receipt["content_length"]))

# ---- (c) AFTER, re-read from S3 -----------------------------------------------------------------
after_etags, after_keys = list_parts(client)
after_newest = after_keys[-1]
after_rows = pg._latest_gold_snapshot_rows(TABLE, client=client)
print("(c) AFTER: %d parquet parts; newest key = %s" % (len(after_keys), after_newest))
check("newest snapshot IS the one just written", after_newest == receipt["key"], "newest=%s receipt=%s" % (after_newest, receipt["key"]))
check("exactly one part added", len(after_keys) == len(before_keys) + 1 and set(before_keys) < set(after_keys),
      "%d -> %d" % (len(before_keys), len(after_keys)))
check("newest snapshot (via _latest_gold_snapshot_rows) carries 8 events", len(after_rows) == 8, "n=%d" % len(after_rows))

# ---- (d) per event: id/span/membership equal, lead OLD -> NEW ------------------------------------
before_by_id = {r["event_id"]: r for r in before_rows}
after_by_id = {r["event_id"]: r for r in after_rows}
check("event_id set equal to the prior snapshot", set(before_by_id) == set(after_by_id) and len(after_rows) == len(before_rows))
n_equal = 0
moved_n = 0
print("(d) per event (denominator %d):" % len(after_rows))
for r in sorted(after_rows, key=lambda r: (r["security_key"], r["first_day"])):
    b = before_by_id.get(r["event_id"])
    if b is None:
        print("      %-16s %s NEW event_id %s NOT in prior snapshot" % (r["security_key"], span(r), r["event_id"]))
        continue
    same = all(b[f] == r[f] for f in FIELDS)
    n_equal += 1 if same else 0
    moved = b["lead_article_key"] != r["lead_article_key"]
    moved_n += 1 if moved else 0
    print("      %-16s %s id=%s" % (r["security_key"], span(r), r["event_id"]))
    print("        id/span/article_keys/counts equal prior: %s (article_keys %d)" % (same, len(r["article_keys"])))
    print("        lead OLD: %s | %s" % (b["lead_article_key"], b["lead_headline"]))
    print("        lead NEW: %s | %s" % (r["lead_article_key"], r["lead_headline"]))
    print("        moved: %s" % ("yes" if moved else "no"))
print("(d) event_id/span/article_keys/counts equal prior: %d of %d; leads moved: %d of %d" % (n_equal, len(after_rows), moved_n, len(after_rows)))
check("event_id, span, membership and counts equal prior 8 of 8", n_equal == 8 and len(after_rows) == 8)
print("(d) the moved leads: %s" % [(r["security_key"], str(r["first_day"])) for r in after_rows
                                    if before_by_id.get(r["event_id"]) and before_by_id[r["event_id"]]["lead_article_key"] != r["lead_article_key"]])

# ---- (e) every prior part still exists with its ETag unchanged ---------------------------------------
n_ok = 0
for k in before_keys:
    head = client.head_object(Bucket=store.HARVEST_BUCKET, Key=k)
    same_etag = head["ETag"] == before_etags[k] and after_etags.get(k) == before_etags[k]
    n_ok += 1 if same_etag else 0
    print("(e) %s ETag before=%s HEAD=%s unchanged=%s" % (k, before_etags[k], head["ETag"], same_etag))
check("ALL %d prior parts exist at their own keys with ETag unchanged" % len(before_keys), n_ok == len(before_keys), "%d of %d" % (n_ok, len(before_keys)))

print("S3 KEY WRITTEN: s3://%s/%s" % (store.HARVEST_BUCKET, receipt["key"]))
print("RESULT: %s (%d failure(s))" % ("FAIL" if failures else "PASS", len(failures)))
sys.exit(1 if failures else 0)
