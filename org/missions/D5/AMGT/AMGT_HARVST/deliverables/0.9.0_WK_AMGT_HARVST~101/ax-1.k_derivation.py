"""HVST-ax-1: derive K, the wsj `unselective_after` bound, from the stored wsj run records (read only, no network).

For every finished wsj job with at least one accepted article: the 1-based position, in the record's fetch order, of its
first accepted article (= articles fetched up to and including the accepting fetch; a bound of K lets a job whose first
accept is fetch n run when K >= n); when the record's order does not give it (an accepted article whose fetch key cannot
be found in fetched_keys), the job's total fetched. K = the maximum, rounded UP to the next multiple of 10.
"""
import glob
import json
import sys
from pathlib import Path

RUNS = Path(sys.argv[1] if len(sys.argv) > 1 else
            "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest-wsj/runs")

read = finished = with_accept = by_order = by_total = 0
measures = []
for path in sorted(glob.glob(str(RUNS / "*.json"))):
    rec = json.loads(Path(path).read_text(encoding="utf-8"))
    read += 1
    if rec.get("publisher") != "wsj" or rec.get("status") == "running" or not rec.get("finished_at"):
        continue
    finished += 1
    accepted = rec.get("accepted") or []
    if not accepted:
        continue
    with_accept += 1
    fetched, outcomes = rec.get("fetched_keys") or [], rec.get("fetch_outcomes") or {}
    keys = {a.get("article_key") for a in accepted}
    positions = [i + 1 for i, k in enumerate(fetched) if (outcomes.get(k) or {}).get("article_key") in keys]
    if positions:
        by_order += 1
        measures.append((positions[0], str(rec.get("ticker")), len(fetched)))
    else:
        by_total += 1
        measures.append((len(fetched), str(rec.get("ticker")), len(fetched)))
top = max(measures)
k = ((top[0] + 9) // 10) * 10
if k == top[0]:
    k += 10  # "the next multiple of 10": a maximum already on a multiple is rounded to the multiple above it
print("run records read: %d; finished wsj jobs: %d; with at least one accepted article: %d" % (read, finished, with_accept))
print("measure used: first-accept position in fetch order for %d jobs; total fetched for %d jobs (order not given)" % (by_order, by_total))
print("largest measure: %d (ticker %s, total fetched %d); top five: %s" % (top[0], top[1], top[2], sorted(measures, reverse=True)[:5]))
print("K = %d" % k)
