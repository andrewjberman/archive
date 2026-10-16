"""MP-pf-4 AC2 seam probe: the breakdown handler's segment reader run over the REAL repo catalog, never a plant.
Prints one line:
  real catalog: tool_index_rows=<n> firm_keys_outside_tool_index=<n> pairs_from_tool_index=<n> pairs_returned=<n> extra_pairs=<n>
  - firm_keys_outside_tool_index: mappings OUTSIDE the top-level `tool_index` list that carry a `firm` key (the owning-firm
    keys of channel, silver and portal rows: same key name, a different meaning). It is the trap; 0 would make the probe vacuous.
  - pairs_from_tool_index: the distinct (vendor, firm) pairs read by an independent walk of the `serves` lists of the
    tool_index rows (a row counts once per distinct tool).
  - pairs_returned: the distinct pairs the handler's own `_segment_fields_for` returns for every tool_index tool.
  - extra_pairs: pairs the handler returned that the independent walk did not find. Must be 0.
Run from the workspace root; it adds the gateway directory to sys.path itself."""
import os
import sys

GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
import yaml  # noqa: E402

from app import admin_gateway_breakdown as B  # noqa: E402

with open(B.CATALOG_YAML, encoding="ascii") as fh:
    doc = yaml.safe_load(fh)
rows = doc.get("tool_index") if isinstance(doc, dict) else None
rows = rows if isinstance(rows, list) else []

firm_outside = 0


def walk(node, inside_tool_index):
    global firm_outside
    if isinstance(node, dict):
        if not inside_tool_index and "firm" in node:
            firm_outside += 1
        for k, v in node.items():
            walk(v, inside_tool_index)
    elif isinstance(node, list):
        for v in node:
            walk(v, inside_tool_index)


for k, v in (doc.items() if isinstance(doc, dict) else []):
    walk(v, k == "tool_index")

names, indep, seen = [], set(), set()
for row in rows:
    if not isinstance(row, dict) or not isinstance(row.get("tool"), str) or row["tool"] in seen:
        continue
    seen.add(row["tool"])
    names.append(row["tool"])
    serves = row.get("serves")
    for el in serves if isinstance(serves, list) else []:
        if isinstance(el, dict):
            v = el.get("vendor")
            f = el.get("firm")
            indep.add((v.strip() if isinstance(v, str) and v.strip() else "unresolved",
                       f.strip() if isinstance(f, str) and f.strip() else "unresolved"))

got = B._segment_fields_for(names)
returned = {p for pairs in got.values() for p in pairs if p != ("unresolved", "unresolved")}
extra = returned - indep
print("real catalog: tool_index_rows=%d firm_keys_outside_tool_index=%d pairs_from_tool_index=%d pairs_returned=%d extra_pairs=%d"
      % (len(names), firm_outside, len(indep), len(returned), len(extra)))
