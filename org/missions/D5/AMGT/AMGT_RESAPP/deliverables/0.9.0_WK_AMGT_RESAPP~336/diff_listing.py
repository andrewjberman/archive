"""Diff two list_prefixes.py outputs by VersionId. usage: py -3.12 diff_listing.py <before.json> <after.json> <KEY>
Prints ADDED / REMOVED version lines and STOP if an added key sits outside the four prefixes."""
import json
import sys

before, after, key = sys.argv[1:4]
b = json.load(open(before))
a = json.load(open(after))
prefixes = list(a)
added = removed = 0
outside = []
for p in prefixes:
    bv = {x["version_id"]: x for x in b.get(p, [])}
    av = {x["version_id"]: x for x in a.get(p, [])}
    for vid, x in av.items():
        if vid not in bv:
            added += 1
            print("ADDED   %s VersionId %s LastModified %s size %s latest %s" % (x["key"], vid, x["last_modified"], x["size"], x["is_latest"]))
            if not any(x["key"].startswith(q) for q in prefixes):
                outside.append(x["key"])
    for vid, x in bv.items():
        if vid not in av:
            removed += 1
            print("REMOVED %s VersionId %s" % (x["key"], vid))
    for vid, x in av.items():
        if vid in bv and bv[vid]["is_latest"] != x["is_latest"]:
            print("LATEST-FLAG %s VersionId %s %s -> %s" % (x["key"], vid, bv[vid]["is_latest"], x["is_latest"]))
print("DIFF %s: added %d removed %d keys-outside-four-prefixes %d" % (key, added, removed, len(outside)))
sys.exit(1 if (removed or outside) else 0)
