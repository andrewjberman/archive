"""c11_index.py -- MX-c-9 AC1 / MX-r-12 instrument (FWD-20 + the durable link key, PRD v0.10 @301af339c7): the DEPLOYED gateway's served tools,
partitioned into three counted members that sum to N.

Usage: python c10_index.py <gateway tree> <catalog yaml> "<enabled integrations, space-separated>"

THE DENOMINATOR N is the served tool list of <gateway tree>: its native tools (app.tools' tool manager, UNFILTERED by
principal) plus every tool the enabled integrations register (integrations.register_enabled), exactly the set
admin_gateway_breakdown._registered_tool_names() reads on the live server. Never a hand-kept list.

THE PARTITION is read from the catalog's `tool_index:` section, exactly one mapping per served tool (`tool: <name>`):
  member  a | b | c
  definition  "<path relative to the gateway dir>:<line>" -- the tool's definition; the tool's name must appear within 5
              lines of it in <gateway tree> (the member is classified from the definition, never the name: CVO note)
  (a) names its catalog index: `read_tool: <the tool>` and `index: <index id>` (round 11: the DURABLE link key, row
      Z-S106 -- a tool_index entry carries NO `entity` and NO `key`, so no row identity appears twice), where the index
      id is the `entity` or `key` of a catalog row OUTSIDE tool_index; AND NFRA_MCPORTAL's own breakdown reader
      (admin_gateway_breakdown._catalog_read_tool_rows, imported from <gateway tree>) resolves the tool to that id; plus
      `history_depth` and `freshness`, each {claim: measured|inferred|absent; measured/inferred carry a non-empty
      `value`; absent carries a non-empty `reason`}. A blank is never a claim.
  (b) reads data but has no index yet: a non-empty `owner` (a project code, or "unowned"); no `read_tool`.
  (c) is not a data read: a non-empty `reason`; no `read_tool`.
Read-only; no network.
"""
import os
import sys

gw, cat_path, enabled = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3].split()
sys.path.insert(0, gw)
os.chdir(gw)
import yaml  # noqa: E402
from app import integrations as integ  # noqa: E402
from app import tools as gw_tools  # noqa: E402

integ.register_enabled(gw_tools.mcp, enabled)
served = sorted({t.name for t in gw_tools.mcp._tool_manager.list_tools()})

with open(cat_path, encoding="ascii") as fh:
    doc = yaml.safe_load(fh)
row_ids: set = set()


def walk(node):
    if isinstance(node, dict):
        rid = node.get("entity") or node.get("key")
        if rid:
            row_ids.add(str(rid))
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


walk({k: v for k, v in doc.items() if k != "tool_index"})
entries: dict = {}
dups = 0
for e in (doc.get("tool_index") or []):
    if isinstance(e, dict) and e.get("tool"):
        dups += str(e["tool"]) in entries
        entries[str(e["tool"])] = e
CLAIMS = {"measured", "inferred", "absent"}


def claim_ok(m) -> bool:
    if not isinstance(m, dict) or m.get("claim") not in CLAIMS:
        return False
    if m["claim"] == "absent":
        return bool(str(m.get("reason") or "").strip())
    return bool(str(m.get("value") or "").strip())


def definition_ok(tool: str, d) -> bool:
    try:
        path, line = str(d).rsplit(":", 1)
        lines = open(os.path.join(gw, path), encoding="utf-8").read().splitlines()
        n = int(line)
    except (ValueError, OSError):
        return False
    return any(tool in x for x in lines[max(0, n - 6):n + 5])


from app import admin_gateway_breakdown as agb  # noqa: E402

agb.CATALOG_YAML = cat_path
panel = agb._catalog_read_tool_rows()
ident = sum(1 for e in (doc.get("tool_index") or []) if isinstance(e, dict) and (e.get("entity") or e.get("key")))
n = len(served)
cnt = {"a": 0, "b": 0, "c": 0}
valid = {"a": 0, "b": 0, "c": 0}
depth = fresh = defs = 0
bad = []
for t in served:
    e = entries.get(t)
    m = str((e or {}).get("member") or "")
    if m not in cnt:
        bad.append("%s(member=%s)" % (t, m or "none"))
        continue
    cnt[m] += 1
    d_ok = definition_ok(t, e.get("definition"))
    defs += d_ok
    if m == "a":
        idx = str(e.get("index") or "")
        link = e.get("read_tool") == t and idx in row_ids and idx in panel.get(t, ())
        dk, fk = claim_ok(e.get("history_depth")), claim_ok(e.get("freshness"))
        depth += dk
        fresh += fk
        ok = link and dk and fk
        why = "link=%d depth=%d fresh=%d" % (link, dk, fk)
    elif m == "b":
        ok = bool(str(e.get("owner") or "").strip()) and not e.get("read_tool")
        why = "owner=%r" % e.get("owner")
    else:
        ok = bool(str(e.get("reason") or "").strip()) and not e.get("read_tool")
        why = "reason=%r" % (str(e.get("reason") or "")[:30])
    valid[m] += ok
    if not (ok and d_ok):
        bad.append("%s(member=%s %s def=%d)" % (t, m, why, d_ok))
stray = sorted(set(entries) - set(served))
total = cnt["a"] + cnt["b"] + cnt["c"]
print("SERVED TOOLS (denominator) N=%d: native+enabled %s" % (n, " ".join(enabled)))
print("PARTITION a=%d (index named, valid %d; depth claim %d; freshness claim %d) b=%d (valid %d) c=%d (valid %d); "
      "sum %d of N=%d; definitions located %d of %d; duplicate entries %d; entries naming an unserved tool %d; "
      "tool_index entries carrying a row identity (entity/key) %d"
      % (cnt["a"], valid["a"], depth, fresh, cnt["b"], valid["b"], cnt["c"], valid["c"], total, n, defs, n, dups,
         len(stray), ident))
for b in bad[:12]:
    print("  MISSING %s" % b)
if len(bad) > 12:
    print("  ... and %d more" % (len(bad) - 12))
ok = (n > 0 and total == n and sum(valid.values()) == n and defs == n and not dups and not stray and cnt["a"] > 0
      and ident == 0)
sys.exit(0 if ok else 1)
