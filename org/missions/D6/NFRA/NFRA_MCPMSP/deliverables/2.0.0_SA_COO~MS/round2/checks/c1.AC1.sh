#!/usr/bin/env bash
# MS-c-1 AC1 (the reader census): deliverables/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_census.json is valid JSON with
#   call_sites_scanned (int, the denominator), readers[] (each {file, line, bucket, prefixes, identity}),
#   iam_statements[] (each {policy, resources}); it names the three measured readers (app/query_v0.py,
#   integrations/portal_index/integration.py, integrations/opal_discover/integration.py) with identity
#   "gateway-instance-role", and readers <= call_sites_scanned.
. "$(dirname "$0")/_root.sh"
F="$R2/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_census.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$F" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print('not JSON: %s verdict=NO' % e); sys.exit(0)
rd = d.get('readers') or []; den = d.get('call_sites_scanned'); iam = d.get('iam_statements') or []
shape = isinstance(den, int) and all(isinstance(r, dict) and {'file','line','bucket','prefixes','identity'} <= set(r) for r in rd) and all(isinstance(s, dict) and {'policy','resources'} <= set(s) for s in iam)
need = ['app/query_v0.py', 'integrations/portal_index/integration.py', 'integrations/opal_discover/integration.py']
found = [n for n in need if any(n in str(r.get('file','')) and r.get('identity') == 'gateway-instance-role' for r in rd)]
ok = shape and len(found) == 3 and isinstance(den, int) and len(rd) <= den and len(iam) >= 1
print('call_sites_scanned=%s readers=%d iam_statements=%d known_readers=%d/3 shape=%s verdict=%s' % (den, len(rd), len(iam), len(found), shape, 'OK' if ok else 'NO'))
EOF
)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
