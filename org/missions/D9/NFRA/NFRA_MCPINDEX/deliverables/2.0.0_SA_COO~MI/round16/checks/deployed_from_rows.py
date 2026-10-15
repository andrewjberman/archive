"""deployed_from_rows.py <out.json>: write the JSON list of every non-null read_tool of the committed silver table rows (workflows/atom_decomposition/catalog_entries),
the deployed-tools set the rows were generated under, so a regeneration with it reproduces every row's tools and read_tool and nothing drifts with today's census.
Run from the repo root. Prints the count written."""
import glob
import json
import os
import sys

import yaml

tools = set()
for p in glob.glob("workflows/atom_decomposition/catalog_entries/*.yaml"):
    if os.path.basename(p).startswith(("need_", "harvest_")):
        continue
    d = yaml.safe_load(open(p, encoding="utf-8"))
    if isinstance(d, dict) and "contract" in d and d.get("read_tool"):
        tools.add(d["read_tool"])
os.makedirs(os.path.dirname(os.path.abspath(sys.argv[1])), exist_ok=True)
json.dump(sorted(tools), open(sys.argv[1], "w", encoding="utf-8"))
print("deployed tools written: %d" % len(tools))
