"""build_rows.py <census.json> <DATA_CATALOG.yaml> <out rows.json>: the ROWS input of partition_windows.py (round 23, issuer tool).

The rows to measure are exactly the catalog rows that a census tool names in its `indexes` (the rows the applier will link). A table row (silver, portal or harvest
section) gives its bucket and `prefix`; a channel-artifact row (a single served JSON object) gives the catalog's portal bucket and its `key` as the prefix. An id
that names no catalog row (for example the tool_index reference of gateway_query_catalog) is listed in the printed `unresolved` line and left out.
"""
import json
import sys

import yaml

cen = json.load(open(sys.argv[1], encoding="utf-8"))
cat = yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
ids = set()
for t in cen["tools"]:
    ids |= set(t.get("indexes") or [])
table = {}
for sec in ("silver_datasets", "portal_datasets", "harvest_datasets"):
    for r in cat.get(sec) or []:
        if isinstance(r, dict) and r.get("entity"):
            table[r["entity"]] = r
art = {}
for cn, ch in (cat.get("channels") or {}).items():
    for a in ch.get("artifacts") or []:
        if isinstance(a, dict) and a.get("entity") and a.get("key"):
            art[a["entity"]] = a
rows, unresolved, noprefix = [], [], []
for i in sorted(ids):
    if i in table:
        r = table[i]
        if r.get("bucket") and r.get("prefix"):
            rows.append({"entity": i, "bucket": r["bucket"], "prefix": r["prefix"]})
        else:
            noprefix.append(i)
    elif i in art:
        rows.append({"entity": i, "bucket": cat.get("bucket") or "", "prefix": art[i]["key"]})
        if not cat.get("bucket"):
            noprefix.append(i)
    else:
        unresolved.append(i)
rows = [r for r in rows if r["bucket"] and r["prefix"]]
json.dump({"rows": rows}, open(sys.argv[3], "w", encoding="utf-8", newline="\n"), indent=1)
print("ROWS %d linked ids; %d rows written; unresolved %s; no bucket or prefix %s" % (len(ids), len(rows), unresolved, noprefix))
