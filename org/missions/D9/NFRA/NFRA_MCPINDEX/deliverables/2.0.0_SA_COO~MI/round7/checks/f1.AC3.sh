#!/usr/bin/env bash
# MX-f-1 AC3: bd_silver_allocations and bd_silver_unrealized carry the weekly basis in the gold freshness config.
. "$(dirname "$0")/_root.sh"
out=$(python - <<'EOF' 2>&1 | tr -d '\r'
import sys, yaml
rows = yaml.safe_load(open('data/black_diamond/scripts/gold/gold_freshness_config.yaml', encoding='utf-8'))
rows = rows if isinstance(rows, list) else (rows.get('artifacts') or [])
bad = 0
for a in ('bd_silver_allocations', 'bd_silver_unrealized'):
    r = next((x for x in rows if isinstance(x, dict) and x.get('artifact_id') == a), {})
    ok = r.get('freshness_basis') == 'trading-day-frontier' and str(r.get('cadence')) == 'weekly' and r.get('weekly_production_weekday')
    bad += not ok
    print('%s %s: basis=%s cadence=%s weekday=%s' % ('OK:' if ok else 'MISSING:', a, r.get('freshness_basis'), r.get('cadence'), r.get('weekly_production_weekday')))
sys.exit(0 if bad == 0 else 1)
EOF
); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
