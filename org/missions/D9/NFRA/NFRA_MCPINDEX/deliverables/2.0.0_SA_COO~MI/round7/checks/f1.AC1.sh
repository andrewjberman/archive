#!/usr/bin/env bash
# MX-f-1 AC1 (CTO 3a Z-S74 part 2, READ-ONLY): the skip-path record names which path production's bd gold chain takes
# (not_on_path | bypass_flag | config_skipped), with its code line and one SCHEDULED run's log line + date.
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~25/SKIP_PATH_RECORD.json"
out=$(python - "$F" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print('record absent or unreadable: %s' % e); sys.exit(1)
ok = d.get('skip_path') in ('not_on_path', 'bypass_flag', 'config_skipped') and all(d.get(k) for k in ('code_ref', 'run_log_line', 'run_date', 'log_source'))
print('skip_path=%s; code_ref=%s; run_date=%s; log_source=%s' % (d.get('skip_path'), d.get('code_ref'), d.get('run_date'), d.get('log_source')))
sys.exit(0 if ok else 1)
EOF
); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
