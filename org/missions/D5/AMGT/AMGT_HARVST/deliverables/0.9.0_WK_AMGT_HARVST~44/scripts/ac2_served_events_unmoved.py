"""HVST-f-2 AC2 -- the SERVED arm. READ-ONLY (S3 GET only). event_rows under the NEW rule over the SERVED newest
article_security_mention snapshot (silver headlines joined exactly as build_event does) vs the SERVED newest
chatter_event snapshot, row by row, every field; then per served security the stripped name stems, old vs new."""
import sys

import _common as c
from _common import pg

client = c.store._default_client()
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headline = pg._headline_by_article_key(client=client)
rows = []
for r in mention:
    r = dict(r)
    r["title"] = headline.get(r.get("article_key"))
    rows.append(r)
served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
print("denominator: %d mention rows over %d securities; %d silver headlines; %d served chatter_event rows"
      % (len(rows), len({r["security_key"] for r in rows}), len(headline), len(served)))


def norm(e):
    return {k: (list(v) if isinstance(v, (list, tuple)) or hasattr(v, "tolist") and not isinstance(v, str) else v)
            for k, v in dict(e).items()}


def key(e):
    return (e["security_key"], e["first_day"], e["last_day"], e["lead_article_key"])


new = [norm(e) for e in pg.event_rows(rows)]
with c.old_rule():
    old = [norm(e) for e in pg.event_rows(rows)]
sv = sorted((norm(e) for e in served), key=key)
new = sorted(new, key=key)
old = sorted(old, key=key)
print("events: served=%d  OLD rule=%d  NEW rule=%d" % (len(sv), len(old), len(new)))
if len(sv) != len(new):
    print("COUNT DIFFERS: served %d vs new %d" % (len(sv), len(new)))
matched = 0
diffs = 0
for s in sv:
    n = next((x for x in new if key(x) == key(s)), None)
    if n is None:
        diffs += 1
        print("  NO NEW ROW for served %s" % (key(s),))
        continue
    fields = sorted(set(s) | set(n))
    bad = [f for f in fields if s.get(f) != n.get(f)]
    if bad:
        diffs += 1
        for f in bad:
            print("  DIFF %s field %s:\n    served=%r\n    new   =%r" % (key(s), f, s.get(f), n.get(f)))
    else:
        matched += 1
        print("  row-equal %s  (%d fields)" % (key(s), len(fields)))
extra = [key(x) for x in new if not any(key(s) == key(x) for s in sv)]
for k in extra:
    print("  NEW ROW with no served row: %s" % (k,))
print("SERVED ARM: %d of %d served rows equal the new rule's rows on every field; %d extra new rows"
      % (matched, len(sv), len(extra)))

print("\nname stems stripped per security, OLD vs NEW (securities with served events, then all with tier-A/B rows)")
by = {}
for r in rows:
    if r.get("signal_tier") in ("A", "B"):
        by.setdefault(r["security_key"], []).append(r)
served_secs = sorted({e["security_key"] for e in sv})
moved = 0
for sec in served_secs + sorted(set(by) - set(served_secs)):
    o, n = c.name_stems(by[sec], False), c.name_stems(by[sec], True)
    moved += o != n
    print("  %s %-16s old=%s new=%s%s" % ("SERVED" if sec in served_secs else "other ", sec, o, n, "" if o == n else "  <-- CHANGED"))
print("securities whose stripped name stems changed: %d of %d" % (moved, len(by)))
sys.exit(0 if matched == len(sv) == len(new) and not extra else 1)
