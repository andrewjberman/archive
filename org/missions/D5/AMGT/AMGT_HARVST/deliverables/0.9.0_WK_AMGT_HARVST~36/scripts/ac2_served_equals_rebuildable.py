"""HVST-a-4 AC2: C-HV-GOLD-REBUILDABLE on the SERVED plane. READ-ONLY (S3 GET only).

Builds the event rows IN MEMORY from the same newest mention snapshot (+ silver headlines, as build_event
does) and compares ROW BY ROW, FIELD BY FIELD with the SERVED newest chatter_event snapshot.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

client = store._default_client()
served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headlines = pg._headline_by_article_key(client=client)
enriched = []
for row in mention:
    row = dict(row)
    row["title"] = headlines.get(row.get("article_key"))
    enriched.append(row)
built = pg.event_rows(enriched)

fields = [f.name for f in pg.GOLD_EVENT_SCHEMA]
print("served rows: %d   in-memory rows: %d   mention rows: %d   silver headlines: %d   fields per row: %d"
      % (len(served), len(built), len(mention), len(headlines), len(fields)))
s_by = {r["event_id"]: r for r in served}
b_by = {r["event_id"]: r for r in built}
ids_equal = set(s_by) == set(b_by) and len(s_by) == len(served) and len(b_by) == len(built)
print("event_id sets equal: %s" % ids_equal)
rows_equal = 0
compared = 0
diffs = 0
for eid in sorted(s_by):
    s, b = s_by.get(eid), b_by.get(eid)
    if b is None:
        print("DIFF: event_id %s served but not rebuilt" % eid)
        diffs += 1
        continue
    row_ok = True
    for f in fields:
        compared += 1
        if s[f] != b[f]:
            row_ok = False
            diffs += 1
            print("DIFF: event %s field %s\n   served : %r\n   rebuilt: %r" % (eid, f, s[f], b[f]))
    rows_equal += 1 if row_ok else 0
    print("  %-16s %s..%s  row equal on all %d fields: %s" % (s["security_key"], s["first_day"], s["last_day"], len(fields), row_ok))
for eid in sorted(set(b_by) - set(s_by)):
    print("DIFF: event_id %s rebuilt but not served" % eid)
    diffs += 1
print("rows equal: %d of %d; fields compared: %d; differences: %d" % (rows_equal, len(served), compared, diffs))
ok = ids_equal and rows_equal == len(served) == len(built) == 8 and diffs == 0
print("AC2 %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
