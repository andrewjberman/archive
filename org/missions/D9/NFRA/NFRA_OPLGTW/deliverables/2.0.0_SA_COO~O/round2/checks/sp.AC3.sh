#!/usr/bin/env bash
# OPLGTW OG-s-1 AC3 (the SERVED host over SSM, counts only): /health 200; the RUNNING gateway process env carries
# SPRINT_VIEW_ALLOWED_EMAILS exactly once with exactly 1 entry (the roster is non-empty, so /sprint no longer fails
# open); the .env ENABLED_INTEGRATIONS line is unchanged at 'ycharts opal_portal globgrph'. No address is printed.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/og_s1_ac3_$$"; mkdir -p "$T"; W=$(cygpath -m "$T" 2>/dev/null || echo "$T")
python - "$W/params.json" <<'EOF'
import json, sys
cmd = ('PID=$(systemctl show -p MainPID --value opal-gateway); '
       'echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'V=$(sudo tr "\\000" "\\n" < /proc/$PID/environ | sed -n "s/^SPRINT_VIEW_ALLOWED_EMAILS=//p"); '
       'echo "keys=$(sudo tr "\\000" "\\n" < /proc/$PID/environ | grep -c "^SPRINT_VIEW_ALLOWED_EMAILS=")"; '
       'echo "entries=$(printf "%s" "$V" | tr "," "\\n" | grep -c "[^[:space:]]")"; '
       'echo "enabled=$(grep -E "^ENABLED_INTEGRATIONS=" /opt/opal-gateway/.env | head -1)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); keys=$(printf '%s\n' "$o" | sed -n 's/^keys=//p'); ent=$(printf '%s\n' "$o" | sed -n 's/^entries=//p'); en=$(printf '%s\n' "$o" | sed -n 's/^enabled=//p')
same=no; [ "$en" = 'ENABLED_INTEGRATIONS=ycharts opal_portal globgrph' ] && same=yes
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; sprint roster keys=$keys entries=$ent; ENABLED_INTEGRATIONS unchanged=$same"
if [ "$h" = 200 ] && [ "$keys" = 1 ] && [ "$ent" = 1 ] && [ "$same" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
