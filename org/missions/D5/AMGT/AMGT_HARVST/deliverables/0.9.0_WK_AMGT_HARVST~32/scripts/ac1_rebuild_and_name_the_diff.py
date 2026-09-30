"""HVST-z-1 AC1: rebuild chatter_event gold under the amended C-HV-EVENT-SPINE and name the whole diff.

THE ONE WRITING SCRIPT OF THIS CELL. It runs the EXISTING producer (`publication_gold.main
build-event`, the CLI code path) exactly ONCE: one conditional put (IfNoneMatch="*"), no delete of
any kind, no other table, no vendor call. Guard: if the BEFORE state is not the signed pair's
premise (newest snapshot, 12 rows) it refuses BEFORE any put, so a re-run cannot add a snapshot.
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
failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def list_keys(client):
    keys = []
    pfx = store.table_prefix("amgt", "gold", TABLE)
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=pfx):
        keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))


def span(r):
    return "%s..%s" % (r["first_day"], r["last_day"])


client = store._default_client()

# ---- (a) BEFORE ------------------------------------------------------------------------------
before_keys = list_keys(client)
before_newest = before_keys[-1]
before_rows = pg._latest_gold_snapshot_rows(TABLE, client=client)
print("(a) BEFORE: %d parquet parts under the prefix; newest key = s3://%s/%s" % (len(before_keys), store.HARVEST_BUCKET, before_newest))
for k in before_keys:
    print("      part: %s" % k)
print("(a) BEFORE newest snapshot event count = %d (expected 12)" % len(before_rows))
for r in before_rows:
    print("      %-16s %s id=%s" % (r["security_key"], span(r), r["event_id"]))
if len(before_rows) != 12:
    print("REFUSED: BEFORE event count is %d, not the signed premise of 12. NO PUT MADE. File a BLOCKING row." % len(before_rows))
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
after_keys = list_keys(client)
after_newest = after_keys[-1]
after_rows = pg._latest_gold_snapshot_rows(TABLE, client=client)
print("(c) AFTER: %d parquet parts; newest key = %s" % (len(after_keys), after_newest))
check("newest snapshot IS the one just written", after_newest == receipt["key"], "newest=%s receipt=%s" % (after_newest, receipt["key"]))
check("exactly one part added", len(after_keys) == len(before_keys) + 1 and set(before_keys) < set(after_keys),
      "%d -> %d" % (len(before_keys), len(after_keys)))
check("newest snapshot (via _latest_gold_snapshot_rows) carries 8 events", len(after_rows) == 8, "n=%d" % len(after_rows))
for r in after_rows:
    print("      %-16s %s id=%s" % (r["security_key"], span(r), r["event_id"]))

# ---- (d) the spurious events absent; (e) the two id moves -----------------------------------------
def analyse(before_rows, after_rows):
    after_ids = {r["event_id"] for r in after_rows}
    after_by_sec = {}
    for r in after_rows:
        after_by_sec.setdefault(r["security_key"], []).append(r)
    gone = [r for r in before_rows if r["event_id"] not in after_ids]
    moved, spurious = [], []
    for r in gone:
        # a "move" = the same security has a new event whose span lies inside the old span
        inside = [n for n in after_by_sec.get(r["security_key"], [])
                  if n["first_day"] >= r["first_day"] and n["last_day"] <= r["last_day"]]
        (moved if inside else spurious).append((r, inside))
    print("(d) old events whose event_id is absent from the served AFTER table: %d = %d spurious + %d narrowed"
          % (len(gone), len(spurious), len(moved)))
    print("(d) the SPURIOUS events, ABSENT after the rebuild:")
    for r, _ in spurious:
        print("      ABSENT security_key=%s span=%s event_id=%s (present in AFTER: %s)"
              % (r["security_key"], span(r), r["event_id"], r["event_id"] in after_ids))
    check("exactly 4 spurious events absent", len(spurious) == 4, "n=%d" % len(spurious))
    check("the 4 spurious securities are {992_HK, COST, DELL, MSFT}",
          {r["security_key"].split("_")[0] for r, _ in spurious} == {"992", "COST", "DELL", "MSFT"},
          str(sorted(r["security_key"] for r, _ in spurious)))
    print("(e) the TWO event_id MOVES (a narrowed span is a NEW ROW WITH A NEW ID):")
    moves_by_sec = {r["security_key"]: (r, n) for r, n in moved}
    check("exactly two moves, BA and HD", set(moves_by_sec) == {"BA_US_Equity", "HD_US_Equity"} and len(moved) == 2,
          str(sorted(moves_by_sec)))
    expected_new = {"BA_US_Equity": ("2026-09-08", "2026-09-08"), "HD_US_Equity": ("2026-08-18", "2026-08-18")}
    for sec in ("BA_US_Equity", "HD_US_Equity"):
        if sec not in moves_by_sec:
            continue
        old, news = moves_by_sec[sec]
        check("%s has exactly one narrowed successor" % sec, len(news) == 1)
        new = news[0]
        recomputed = pg._event_id(sec, new["first_day"], new["last_day"])
        print("      %s: old span %s -> new span %s" % (sec, span(old), span(new)))
        print("        OLD event_id = %s" % old["event_id"])
        print("        NEW event_id = %s" % new["event_id"])
        check("%s old != new event_id" % sec, old["event_id"] != new["event_id"])
        check("%s new event_id == publication_gold._event_id(security_key, new_first_day, new_last_day)" % sec,
              new["event_id"] == recomputed, "recomputed=%s" % recomputed)
        check("%s new span == %s..%s" % ((sec,) + expected_new[sec]),
              (str(new["first_day"]), str(new["last_day"])) == expected_new[sec])


analyse(before_rows, after_rows)


# ---- the prior snapshot survives at its own key --------------------------------------------------
head = client.head_object(Bucket=store.HARVEST_BUCKET, Key=before_newest)
print("PRIOR snapshot still EXISTS at its own key: s3://%s/%s ContentLength=%s LastModified=%s"
      % (store.HARVEST_BUCKET, before_newest, head["ContentLength"], head["LastModified"]))
check("prior snapshot exists at its own key (signed radius = one ADDED object)", True)
for k in before_keys:
    client.head_object(Bucket=store.HARVEST_BUCKET, Key=k)
check("ALL %d prior parts still exist" % len(before_keys), True)

print("RESULT: %s (%d failure(s))" % ("FAIL" if failures else "PASS", len(failures)))
sys.exit(1 if failures else 0)
