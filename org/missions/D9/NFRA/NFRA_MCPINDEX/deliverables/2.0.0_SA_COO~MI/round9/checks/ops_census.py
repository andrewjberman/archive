"""ops_census.py -- MX-o-1 / MX-o-2 AC1 instrument (PRD v0.8 FWD-19, contract 2: the source is found, never assumed).

Grades a reader cell's census file. The census is the cell's FIRST act: every candidate producer, each with its own
denominator, and the surviving source read once.
Usage: python ops_census.py <census.json> <trade_rec|billing>

Required shape:
  {"reader": "trade_rec"|"billing",
   "candidates": [{"producer", "location", "denominator" (int), "denominator_of" (what was counted),
                   "served" (bool), "reason"}...],          # at least 2 candidates
   "verdict": "SERVED"|"GAP",
   "source": {"producer", "location", "read_once_at" (UTC ISO), "rows_read" (int)}   # when SERVED
   "owner": "<project code or 'unowned'>"                    # when GAP
   "probe_scope": "<firm or master the live probe reads>"    # when SERVED
  }
Prints every violation, then one summary line. Offline, read-only.
"""
import json
import sys

path, reader = sys.argv[1], sys.argv[2]
try:
    c = json.load(open(path, encoding="utf-8"))
except Exception as exc:  # noqa: BLE001
    print("census unreadable at %s: %s" % (path, type(exc).__name__))
    sys.exit(1)
bad = []
if c.get("reader") != reader:
    bad.append("reader %r != %r" % (c.get("reader"), reader))
cands = c.get("candidates") or []
if len(cands) < 2:
    bad.append("candidates %d (at least 2: a census names every candidate producer, never one assumed)" % len(cands))
for i, k in enumerate(cands):
    for f in ("producer", "location", "denominator", "denominator_of", "served", "reason"):
        if f not in k:
            bad.append("candidate %d missing %s" % (i, f))
    if not isinstance(k.get("denominator"), int):
        bad.append("candidate %d denominator %r is not an int" % (i, k.get("denominator")))
    if not isinstance(k.get("served"), bool):
        bad.append("candidate %d served %r is not a bool" % (i, k.get("served")))
v = c.get("verdict")
if v not in ("SERVED", "GAP"):
    bad.append("verdict %r is not SERVED|GAP" % v)
if v == "SERVED":
    s = c.get("source") or {}
    for f in ("producer", "location", "read_once_at", "rows_read"):
        if f not in s:
            bad.append("SERVED source missing %s" % f)
    if not isinstance(s.get("rows_read"), int) or s.get("rows_read", 0) < 1:
        bad.append("SERVED source rows_read %r (the surviving source is read once, >= 1 row)" % s.get("rows_read"))
    if not any(k.get("served") for k in cands):
        bad.append("verdict SERVED but no candidate reads served=true")
    if not str(c.get("probe_scope") or "").strip():
        bad.append("SERVED census names no probe_scope")
if v == "GAP":
    if not str(c.get("owner") or "").strip():
        bad.append("GAP census names no owner (a project code or 'unowned')")
    if any(k.get("served") for k in cands):
        bad.append("verdict GAP but a candidate reads served=true")
for b in bad:
    print("VIOLATION: " + b)
print("census %s: candidates %d, each with a denominator %d of %d; verdict %s; violations %d"
      % (reader, len(cands), sum(1 for k in cands if isinstance(k.get("denominator"), int)), len(cands), v, len(bad)))
sys.exit(0 if not bad else 1)
