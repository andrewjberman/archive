#!/usr/bin/env bash
# OPLGTW OG-ix-1 AC1 (round 47, P1 handler half / MP's GWZ1.1 contract): the gateway breakdown (app/admin_gateway_breakdown.py _compute) gives every tool that sits in the
# opal-data-assets or opal-data-bd channel an `index_pairs` list: one {"index", "vendor", "firm"} per entry of the tool's own `indexes`, in the same order, the vendor and
# firm being the first two path components of the index's catalog row prefix (the row found by its `entity`, `key` or `index` id; its bucket one of the two segmented buckets);
# an index with no such row reads vendor "unresolved" and firm "unresolved". A tool in any other channel carries NO `index_pairs` key (the older payload shape stays).
# Probe: the REAL tool inventory and the REAL catalog, with a fake grant store (no AWS). The oracle reads the catalog YAML independently of the module.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && MOCK_GRAPH=1 timeout 110 python3 -I - <<'EOF'
import sys, json, os
sys.path.insert(0, ".")
os.environ.setdefault("MOCK_GRAPH", "1")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import admin_gateway_breakdown as bd
    import yaml
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
class Ddb:
    def scan(self, **kw): return {"Items": []}
class Store:
    def get(self, key): return None
doc = yaml.safe_load(open(bd.CATALOG_YAML, encoding="ascii"))
rows = {}
def walk(n):
    if isinstance(n, dict):
        rid = n.get("entity") or n.get("key") or n.get("index")
        if rid and isinstance(n.get("prefix"), str) and isinstance(n.get("bucket"), str):
            rows.setdefault(str(rid), n)
        for v in n.values(): walk(v)
    elif isinstance(n, list):
        for v in n: walk(v)
walk(doc)
SEG = ("opal-data-assets", "opal-data-bd")
def oracle(index):
    r = rows.get(index)
    if r is None or r["bucket"] not in SEG:
        return ("unresolved", "unresolved")
    parts = [p for p in r["prefix"].split("/") if p]
    return (parts[0], parts[1]) if len(parts) >= 2 else ("unresolved", "unresolved")
try:
    body = bd._compute(scan_client=Ddb(), store=Store())
except Exception as exc:
    print("_compute raised %s: %s" % (type(exc).__name__, str(exc)[:140])); print("NO"); sys.exit(0)
seg_tools, other_tools = [], []
for c in body["channels"]:
    (seg_tools if c["id"] in SEG else other_tools).extend(c["tools"])
say("segmented channels hold tools", len(seg_tools) > 0, "%d tool entries" % len(seg_tools))
missing = [t["name"] for t in seg_tools if not isinstance(t.get("index_pairs"), list)]
say("every tool in a segmented channel carries an index_pairs list", not missing, "missing %s" % missing[:5])
bad_shape = [t["name"] for t in seg_tools if isinstance(t.get("index_pairs"), list) and any(set(p) != {"index", "vendor", "firm"} for p in t["index_pairs"])]
say("every element is exactly {index, vendor, firm}", not bad_shape, "bad %s" % bad_shape[:5])
mismatch = [t["name"] for t in seg_tools if isinstance(t.get("index_pairs"), list) and [p["index"] for p in t["index_pairs"]] != t["indexes"]]
say("index_pairs cover the tool's indexes one for one, in the same order", not mismatch, "mismatch %s" % mismatch[:5])
wrong = [(t["name"], p["index"]) for t in seg_tools for p in (t.get("index_pairs") or []) if (p.get("vendor"), p.get("firm")) != oracle(p["index"])]
say("each pair equals the first two components of the catalog row's prefix (else unresolved)", not wrong, "wrong %s" % wrong[:3])
total = sum(len(t.get("index_pairs") or []) for t in seg_tools)
resolved = sum(1 for t in seg_tools for p in (t.get("index_pairs") or []) if p.get("vendor") != "unresolved")
say("some pair resolves to a real vendor and firm", resolved > 0, "%d of %d resolved" % (resolved, total))
leak = [t["name"] for t in other_tools if "index_pairs" in t]
say("tools in other channels carry no index_pairs key", not leak and len(other_tools) > 0, "leak %s" % leak[:5])
try:
    json.dumps(body)
    say("the body serialises", True)
except Exception as exc:
    say("the body serialises", False, type(exc).__name__)
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
