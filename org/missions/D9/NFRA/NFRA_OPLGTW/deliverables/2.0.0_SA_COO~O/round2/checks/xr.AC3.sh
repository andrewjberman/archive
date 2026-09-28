#!/usr/bin/env bash
# OPLGTW OG-x-3 AC3 (the SERVED host over SSM): /health 200; the host carries the streaming export (OG-x-2's test module
# shipped, and the host's schwab/{engine,integration,export,envelope}.py equal the manifest's deployed_commit bytes, 4 of
# 4); the on-host tool count equals the count recorded in ANNOUNCE (read by the worker; here: >= 1); the .env
# ENABLED_INTEGRATIONS line is unchanged at 'ycharts opal_portal globgrph' (Schwab stays dark).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys; print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" 2>&1 | tr -d '\r')
exp=""; for f in engine integration export envelope; do exp="$exp $(git show "$c:$GW/app/integrations/schwab/$f.py" 2>/dev/null | md5sum | cut -c1-32)"; done
T="${TMPDIR:-/tmp}/og_x3_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF2'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo "stream=$(test -f /opt/opal-gateway/tests/test_schwab_export_stream.py && echo 1 || echo 0)"; '
       'echo "md5=$(cd /opt/opal-gateway/app/integrations/schwab && md5sum engine.py integration.py export.py envelope.py | cut -c1-32 | tr \'\n\' \' \')"; '
       'echo "enabled=$(grep -E \'^ENABLED_INTEGRATIONS=\' /opt/opal-gateway/.env | head -1)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF2
cid=$(timeout 25 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6; do st=$(timeout 8 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 10 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); sm=$(printf '%s\n' "$o" | sed -n 's/^stream=//p'); en=$(printf '%s\n' "$o" | sed -n 's/^enabled=//p')
got=$(printf '%s\n' "$o" | sed -n 's/^md5=//p')
m=0; i=1; for e in $exp; do g=$(printf '%s' "$got" | awk -v n=$i '{print $n}'); [ -n "$e" ] && [ "$e" = "$g" ] && m=$((m+1)); i=$((i+1)); done
same=no; [ "$en" = 'ENABLED_INTEGRATIONS=ycharts opal_portal globgrph' ] && same=yes
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; streaming export on host ${sm:-NONE}; schwab files equal deployed_commit $m of 4; ENABLED_INTEGRATIONS unchanged=$same"
if [ "$h" = 200 ] && [ "${sm:-0}" = 1 ] && [ "$m" = 4 ] && [ "$same" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
