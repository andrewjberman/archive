"""catalog_tools_served.py <catalog.yaml> <tools_census.json>: read-only. Prints the catalog's version and row counts
(the r13.AC4 figures) and the read_tool names the rows name that the census does NOT serve."""

import hashlib
import json
import sys

import yaml

raw = open(sys.argv[1], "rb").read()
cat = yaml.safe_load(raw.decode("ascii"))
served = set(json.load(open(sys.argv[2]))["all"])
rows = [r for k in ("silver_datasets", "portal_datasets") for r in (cat.get(k) or [])]
table = [r for r in rows if isinstance(r, dict) and "contract" in r]
tools = set()
for sec in ("silver_datasets", "portal_datasets", "harvest_datasets"):
    for r in cat.get(sec) or []:
        if isinstance(r, dict) and r.get("read_tool"):
            tools.add(str(r["read_tool"]))
print(
    "CATALOG version=%s harvest=%d table=%d key_template=%d retired=%d"
    % (
        cat.get("version"),
        len(cat.get("harvest_datasets") or []),
        len(table),
        sum(1 for r in table if r.get("key_template")),
        sum(1 for r in table if r.get("retired") is True),
    )
)
print("MD5 %s" % hashlib.md5(raw).hexdigest())
print("read_tool names in the catalog: %d; census serves %d" % (len(tools), len(served)))
print("read_tool names NOT served by the census: %s" % (sorted(tools - served) or "none"))
