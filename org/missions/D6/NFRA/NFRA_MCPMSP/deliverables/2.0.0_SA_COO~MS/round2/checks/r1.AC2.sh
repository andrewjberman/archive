#!/usr/bin/env bash
# MS-r-1 AC2 (R-4, the built behaviour, dry): `MCPORTAL_RESOLVE_ONLY=1 bash infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
# resolves the dashboard checkout WITHOUT building or uploading anything and prints exactly one line
# "MCPORTAL-RESOLVED: <dir> @<commit>" whose commit is EC2_MANIFEST.json's services.opal-gateway.mcportal_commit
# (a3bff71ffa at the cut), exiting 0 -- even though the workspace mcportal gitlink is the README-only fa1ff9693b.
. "$(dirname "$0")/_root.sh"
want=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'].get('mcportal_commit',''))" | tr -d '\r')
# SAFETY: a deploy-to-ec2.sh that does not know MCPORTAL_RESOLVE_ONLY would run a REAL deploy (build, upload, SSM).
# Invoke it ONLY when the script itself declares the flag AND exits on it before any aws/ssh/scp call; otherwise FAIL
# without executing anything.
if ! grep -q 'MCPORTAL_RESOLVE_ONLY' "$G/deploy-to-ec2.sh"; then
  echo "deploy-to-ec2.sh does not declare MCPORTAL_RESOLVE_ONLY -- NOT executed (it would deploy)"; echo "RESULT: FAIL"; exit 1
fi
guard=$(python - "$G/deploy-to-ec2.sh" <<'EOF' 2>&1 | tr -d '\r'
import re, sys
t = open(sys.argv[1], encoding='utf-8').read().splitlines()
flag = next((i for i, l in enumerate(t) if 'MCPORTAL_RESOLVE_ONLY' in l and 'exit 0' in ' '.join(t[i:i+40])), None)
first_act = next((i for i, l in enumerate(t) if re.search(r'^\s*[^#]*\b(aws |ssh |scp |safe-ec2)', l)), None)
print('ok' if flag is not None and (first_act is None or flag < first_act) else 'unsafe flag=%s first_act=%s' % (flag, first_act))
EOF
)
if [ "$guard" != ok ]; then echo "resolve-only exit is not before the first aws/ssh/scp act ($guard) -- NOT executed"; echo "RESULT: FAIL"; exit 1; fi
out=$(MCPORTAL_RESOLVE_ONLY=1 timeout 100 bash "$G/deploy-to-ec2.sh" 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -m1 '^MCPORTAL-RESOLVED:')
n=$(printf '%s\n' "$out" | grep -c '^MCPORTAL-RESOLVED:')
got=$(printf '%s' "$line" | sed -nE 's/.* @([0-9a-f]{7,40}).*/\1/p')
built=$(printf '%s\n' "$out" | grep -ciE 'built artifact|uploaded s3://|aws s3 cp')
echo "resolve line: ${line:-NONE} (count=$n, rc=$rc); manifest mcportal_commit=$want; build/upload lines=$built"
if [ "$rc" = 0 ] && [ "$n" = 1 ] && [ -n "$got" ] && [ "${want#$got}" != "$want" ] && [ "$built" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
