#!/usr/bin/env bash
# OPLGTW OG-gp-1 AC2 (round-37, FWD-22): W/CLASSIFICATION.json covers EXACTLY the catalog's assigned rows (recomputed here: rows of opal-data-portal-v2 and opal-data-mdpf with an empty read_tool at the worker's HEAD, minus the rival-funds set staged in OG-ap-22),
# every BUILT row names a tool function that exists in the gateway's app modules, and the built tools answered a read of the real bucket (W/PROBE.json, written by the worker's probe and RE-RUN here).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~109"
[ -f "$W/CLASSIFICATION.json" ] || { echo "CLASSIFICATION.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/CLASSIFICATION.json")" <<'PYEOF'
import glob, json, re, sys, yaml
cls = json.load(open(sys.argv[1], encoding="utf-8")).get("rows", {})
doc = yaml.safe_load(open("infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml", encoding="ascii"))
rows = []
def walk(n):
    if isinstance(n, dict):
        if "entity" in n and "bucket" in n:
            rows.append(n)
        for v in n.values():
            walk(v)
    elif isinstance(n, list):
        for v in n:
            walk(v)
walk(doc)
RIV = ("rivalfunds", "_gold_buying", "_gold_canonical", "_gold_corporate", "_gold_flow", "_gold_holding_contrib", "_gold_holdings_cov", "_gold_input", "_gold_peer", "_gold_research", "_gold_security", "_gold_trade")
buckets = ['opal-data-portal-v2', 'opal-data-mdpf']
assigned = sorted(r["entity"] for r in rows if r["bucket"] in buckets and not r.get("read_tool") and not (r["bucket"] == "opal-data-etfs" and any(x in r["entity"] for x in RIV)))
have = sorted(cls)
ok_set = assigned == have
cnt = {k: sum(1 for v in cls.values() if v.get("class") == k) for k in ("COVERED", "BUILT", "DEFERRED")}
src = "".join(open(f, encoding="utf-8").read() for f in glob.glob("infra/aws/ec2/opal-gateway/app/*.py"))
built = sorted({v.get("tool") for v in cls.values() if v.get("class") == "BUILT" and v.get("tool")})
exist = sum(1 for t in built if t and re.search(r"def\s+%s\s*\(" % re.escape(t), src))
print("classification: assigned %d of %d, covered %d, built %d, deferred %d; set equal %s; built tools defined %d of %d" % (len(assigned), len(have), cnt["COVERED"], cnt["BUILT"], cnt["DEFERRED"], ok_set, exist, len(built)))
print("OK" if ok_set and cnt["COVERED"] + cnt["BUILT"] + cnt["DEFERRED"] == len(assigned) and exist == len(built) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
P="$W/probe_built.py"; pr=0; pn=0
if [ -f "$P" ]; then out=$(timeout 115 python "$P" 2>&1 | tr -d '\r'); printf '%s\n' "$out" | grep -E "^probe built:" | tail -n 2; pn=$(printf '%s\n' "$out" | grep -cE "^probe built: .* answered True"); fi
echo "built tools probed $pn (the worker's probe lines)"
nb=$(printf '%s' "$res" | sed -n 's/.*defined [0-9]* of \([0-9]*\)$/\1/p' | head -1)
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { [ "${nb:-0}" = 0 ] || [ "$pn" -ge "${nb:-0}" ]; } && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
