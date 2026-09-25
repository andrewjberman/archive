#!/usr/bin/env bash
# MP-a-1 AC3 (R-2's branch, picked from the measurement): the deployed writer's MCPORTAL_OWNER_KEY_CLAIM and
# MCPORTAL_OWNER_KEY equal the claim the gateway's latest OWNER-HEADER-CLAIMS journal line proves the ALB carries -- oid
# when that line's oid is not ABSENT, otherwise sub -- and its value, read live over SSM on i-07dccb1615503ac99.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_a1_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = 'journalctl -u opal-gateway --no-pager -o cat | grep "OWNER-HEADER-CLAIMS" | tail -1'
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
line=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r' | grep 'OWNER-HEADER-CLAIMS' | tail -1)
envj=$(timeout 30 "$AWS" lambda get-function-configuration --function-name "$nm" --query Environment.Variables --output json 2>/dev/null | tr -d '\r')
rm -rf "$T"
res=$(printf '%s\n%s\n' "$line" "$envj" | python -c "
import json, re, sys
raw = sys.stdin.read().split('\n', 1)
line = raw[0]; env = {}
try:
    env = json.loads(raw[1]) or {}
except Exception:
    pass
oid = (re.search(r'\boid=(\S+)', line) or [None, 'NONE'])[1]
sub = (re.search(r'\bsub=(\S+)', line) or [None, 'NONE'])[1]
want = ('oid', oid) if oid not in ('ABSENT', 'NONE') else ('sub', sub)
have = (env.get('MCPORTAL_OWNER_KEY_CLAIM', 'UNSET'), env.get('MCPORTAL_OWNER_KEY', 'UNSET'))
ok = want[1] not in ('ABSENT', 'NONE') and have[0] == want[0] and have[1].lower() == want[1].lower()
print('line=%s want_claim=%s have_claim=%s value_match=%s' % ('yes' if line.strip() else 'no', want[0], have[0], 'yes' if ok else 'no'))
" 2>&1 | tr -d '\r')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; $res"
if printf '%s' "$res" | grep -q 'line=yes' && printf '%s' "$res" | grep -q 'value_match=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
