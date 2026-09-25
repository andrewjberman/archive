"""AC2 -- AFTER state, same instrument as AC0, DELTA printed per publisher."""
import json
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))
from _common import PUBLISHERS, client, silver_listing_hit_counts, bronze_news_listing_object_counts

before_path = os.path.join(".scratch", "s1", "ac0_before.json")
with open(before_path, "r", encoding="utf-8") as f:
    before = json.load(f)

c = client()
silver_after = silver_listing_hit_counts(c)
bronze_after = bronze_news_listing_object_counts(c)

print("AC2 AFTER STATE (same instrument as AC0)")
print("five-publisher denominator: %d (%s)" % (len(PUBLISHERS), ", ".join(PUBLISHERS)))
print("silver listing_hit rows per publisher -- BEFORE / AFTER / DELTA:")
for p in PUBLISHERS:
    b = before["silver_listing_hit_rows"].get(p, 0)
    a = silver_after.get(p, 0)
    print("  %-8s %5d  %5d  %+d" % (p, b, a, a - b))
print("bronze news_listing objects per publisher -- BEFORE / AFTER / DELTA:")
for p in PUBLISHERS:
    b = before["bronze_news_listing_objects"].get(p, 0)
    a = bronze_after.get(p, 0)
    print("  %-8s %5d  %5d  %+d" % (p, b, a, a - b))

sa_before = before["sa_listing_hit_before"]
sa_after = silver_after.get("sa", 0)
sa_delta = sa_after - sa_before
print("sa listing_hit delta (signed): %+d (before=%d, after=%d)" % (sa_delta, sa_before, sa_after))
if sa_delta == 0:
    print("sa listing_hit delta is ZERO -- reported as a legitimate outcome, not explained away.")

after = {
    "silver_listing_hit_rows": {p: silver_after.get(p, 0) for p in PUBLISHERS},
    "bronze_news_listing_objects": {p: bronze_after.get(p, 0) for p in PUBLISHERS},
    "sa_listing_hit_after": sa_after,
    "sa_listing_hit_delta": sa_delta,
}
out_path = os.path.join(".scratch", "s1", "ac2_after.json")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(after, f, indent=2)
print("wrote %s" % out_path)
