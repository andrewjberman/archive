#!/usr/bin/env bash
# OPLGTW OG-sk-1 AC1 (round 47; the Schwab 0840 move to schwab/49financial/, the CTO's dual-read ruling 20:18Z): the CENSUS of every gateway code path that builds a Schwab prefix or key from the master is COMPLETE against an independent sweep.
# W/SK_CENSUS.json (W = deliverables/0.9.0_WK_NFRA_OPLGTW~177/): {"body": {"scanned": {"gateway_files": n, "tf_files": n, "contract_copies": 2}, "entries": [{"file", "line", "kind", "master_dependent", "edit", "reason"}], "reader_iam": {...}, "fence_points": [...]}}.
# The sweep here (not the worker's): every .py/.json/.yaml/.md file under infra/aws/ec2/opal-gateway/ (app/, deploy/, runbooks/, scripts if any; tests/ is swept too) holding the regex  schwab/|08403355|completion_prefixes|data_prefixes  must appear in the census with at least one entry.
# Prints the denominators: files swept, files with a hit, files in the census, missing from the census (want 0).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~177
[ -f "$W/SK_CENSUS.json" ] || { echo "SK_CENSUS.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$G")" "$(native "$W")" <<'PYEOF'
import json, os, re, sys
G, W = sys.argv[1], sys.argv[2]
d = json.load(open(os.path.join(W, "SK_CENSUS.json"), encoding="utf-8")); d = d.get("body", d)
pat = re.compile(r"schwab/|08403355|completion_prefixes|data_prefixes")
swept = hits = 0
hitfiles = set()
for root, dirs, files in os.walk(G):
    dirs[:] = [x for x in dirs if x not in ("__pycache__", ".pytest_cache", "node_modules", ".git")]
    for f in files:
        if not f.endswith((".py", ".json", ".yaml", ".yml", ".md", ".sh", ".tf")):
            continue
        p = os.path.join(root, f)
        swept += 1
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if pat.search(t):
            hitfiles.add(os.path.relpath(p, G).replace("\\", "/"))
ents = d.get("entries") or []
norm = lambda s: (s or "").replace("\\", "/").replace("infra/aws/ec2/opal-gateway/", "")
incen = {norm(e.get("file")) for e in ents if isinstance(e, dict)}
missing = sorted(hitfiles - incen)
sc = d.get("scanned") or {}
kinds_ok = all(isinstance(e, dict) and e.get("kind") in ("silver_key", "state_key", "bronze_key", "prefix_const", "iam", "contract", "catalog", "test", "doc", "other")
               and e.get("edit") in ("DUAL_READ", "NEW_PATH_ONLY", "NONE") and isinstance(e.get("master_dependent"), bool) and isinstance(e.get("line"), int)
               and isinstance(e.get("reason"), str) and len(e["reason"]) >= 8 for e in ents)
print("independent sweep: %d files swept under the gateway folder, %d hold a Schwab prefix token; census names %d files in %d entries" % (swept, len(hitfiles), len(incen), len(ents)))
print("hit files missing from the census: %d (want 0)%s" % (len(missing), (": " + ", ".join(missing[:8])) if missing else ""))
print("census scanned counts stated: gateway_files %s (sweep %d), contract_copies %s (want 2); every entry carries kind, line, master_dependent, edit and a reason: %s" % (
    sc.get("gateway_files"), swept, sc.get("contract_copies"), "ok" if kinds_ok else "NOT OK"))
ok = not missing and kinds_ok and sc.get("contract_copies") == 2 and isinstance(sc.get("gateway_files"), int) and sc["gateway_files"] >= swept - 40 and len(ents) >= 10
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
