"""AC0 -- BEFORE state, read from S3 at run time (never copied from the task order)."""
import json
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))
from _common import PUBLISHERS, client, silver_listing_hit_counts, bronze_news_listing_object_counts

c = client()

silver = silver_listing_hit_counts(c)
bronze = bronze_news_listing_object_counts(c)

print("AC0 BEFORE STATE")
print("five-publisher denominator: %d (%s)" % (len(PUBLISHERS), ", ".join(PUBLISHERS)))
print("silver listing_hit rows per publisher (BEFORE):")
for p in PUBLISHERS:
    print("  %-8s %d" % (p, silver.get(p, 0)))
print("bronze news_listing objects per publisher (BEFORE):")
for p in PUBLISHERS:
    print("  %-8s %d" % (p, bronze.get(p, 0)))
print("sa listing_hit count (BEFORE), explicit: %d" % silver.get("sa", 0))

before = {
    "denominator_publishers": len(PUBLISHERS),
    "publishers": list(PUBLISHERS),
    "silver_listing_hit_rows": {p: silver.get(p, 0) for p in PUBLISHERS},
    "bronze_news_listing_objects": {p: bronze.get(p, 0) for p in PUBLISHERS},
    "sa_listing_hit_before": silver.get("sa", 0),
}
out_path = os.path.join(".scratch", "s1", "ac0_before.json")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(before, f, indent=2)
print("wrote %s" % out_path)

# Confirm the deployed persist location: print the bytes at worker.py around the `finally`
# wrapping the per-article loop (row Z-S10's guard is inside this same block).
worker_path = os.path.join("lib", "opal_data_harvest", "worker.py")
with open(worker_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print("")
print("worker.py bytes around the `finally` (1-indexed lines 215-262):")
for i in range(215, 262):
    if i - 1 < len(lines):
        print("%4d| %s" % (i, lines[i - 1].rstrip("\n")))
