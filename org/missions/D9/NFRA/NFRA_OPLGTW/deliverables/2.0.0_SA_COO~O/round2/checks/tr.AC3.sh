#!/usr/bin/env bash
# OPLGTW OG-t-2 AC3 (the SERVED host over SSM): /health 200; the host's app/tier.py reads no email roster and its
# app/ratelimit.py lists the browser callback in AUTH_PATHS (shipped); the .env ENABLED_INTEGRATIONS line is unchanged.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/og_t2_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo "roster=$(grep -c MASTER_ADMIN_EMAILS /opt/opal-gateway/app/tier.py)"; '
       'echo "authpath=$(grep -c schwab/download/callback /opt/opal-gateway/app/ratelimit.py)"; '
       'echo "enabled=$(grep -E \'^ENABLED_INTEGRATIONS=\' /opt/opal-gateway/.env | head -1)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 25 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6; do st=$(timeout 8 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 10 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); ro=$(printf '%s\n' "$o" | sed -n 's/^roster=//p'); ap=$(printf '%s\n' "$o" | sed -n 's/^authpath=//p'); en=$(printf '%s\n' "$o" | sed -n 's/^enabled=//p')
# A2 (row Z-W12-S4): 'unchanged' means the live value before the release, six ids at 42c52ed4d9; override with
# OG_T2_ENABLED_BEFORE when the worker's step-8 BEFORE read differs.
EXP="${OG_T2_ENABLED_BEFORE:-ycharts opal_portal globgrph opal_discover portal_index schwab}"
same=no; [ "$en" = "ENABLED_INTEGRATIONS=$EXP" ] && same=yes
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; email roster reads on host ${ro:-NONE}; callback in AUTH_PATHS ${ap:-NONE}; ENABLED_INTEGRATIONS unchanged=$same"
if [ "$h" = 200 ] && [ "$ro" = 0 ] && [ "${ap:-0}" -ge 1 ] && [ "$same" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
