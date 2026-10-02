#!/usr/bin/env bash
# MX-m-2 AC1 (CTO item 4, measure before build): the census record covers orion, eclipse and smartx; each lists its served
# datasets (key, newest_partition, as_of, rows, catalog_row) with a printed denominator.
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~26/PLATFORM_CENSUS_round7.json"
out=$(python - "$F" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print('record absent or unreadable: %s' % e); sys.exit(1)
bad = 0
for p in ('orion', 'eclipse', 'smartx'):
    e = d.get(p) or {}
    ds = e.get('datasets')
    keys = ('key', 'newest_partition', 'as_of', 'rows', 'catalog_row')
    ok = isinstance(ds, list) and isinstance(e.get('denominator'), int) and e['denominator'] == len(ds) and all(all(k in x for k in keys) for x in ds)
    bad += not ok
    print('%s %s: datasets=%s denominator=%s' % ('OK:' if ok else 'MISSING:', p, len(ds) if isinstance(ds, list) else None, e.get('denominator')))
sys.exit(0 if bad == 0 else 1)
EOF
); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
