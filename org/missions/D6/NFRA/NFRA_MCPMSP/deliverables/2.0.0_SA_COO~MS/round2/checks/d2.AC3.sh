#!/usr/bin/env bash
# MS-d-2 AC3 (the SERVED host, live over SSM, with its control): /health answers 200; the md5 of each of
# /opt/opal-gateway/app/{internal_role,sender_gate,admin_refusals}.py equals that file's blob at the manifest's
# deployed_commit; /opt/opal-gateway/.env carries exactly one INTERNAL_READER_ROLE_ARN line and exactly one
# MSP_CALLING_IDENTITIES line (values never printed); round 1's modules are still served (tenant_registry.py present).
. "$(dirname "$0")/_root.sh"
c=$(git show "HEAD:infra/aws/ec2/EC2_MANIFEST.json" | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" 2>/dev/null | tr -d '\r')
want=""; for f in internal_role sender_gate admin_refusals; do m=$(git show "$c:$G/app/$f.py" 2>/dev/null | md5sum | cut -c1-32); want="$want $f=$m"; done
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_d2_ac3.XXXXXX")"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'for f in internal_role sender_gate admin_refusals; do echo "$f=$(md5sum /opt/opal-gateway/app/$f.py 2>/dev/null | cut -c1-32)"; done; '
       'echo "r1=$(test -f /opt/opal-gateway/app/tenant_registry.py && echo present || echo absent)"; '
       'echo "irr=$(grep -c "^INTERNAL_READER_ROLE_ARN=" /opt/opal-gateway/.env 2>/dev/null)"; '
       'echo "msp=$(grep -c "^MSP_CALLING_IDENTITIES=" /opt/opal-gateway/.env 2>/dev/null)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s/^$1=//p"; }
ok=1; got=""; for f in internal_role sender_gate admin_refusals; do l=$(v $f); w=$(printf '%s' "$want" | tr ' ' '\n' | sed -n "s/^$f=//p"); r=MISMATCH; [ -n "$l" ] && [ "$l" = "$w" ] && r=match; got="$got $f=$r"; [ "$r" = match ] || ok=0; done
echo "ssm command=$SSM_CID status=$SSM_ST; deployed_commit=$c; /health=$(v health);$got; tenant_registry=$(v r1); INTERNAL_READER_ROLE_ARN lines=$(v irr); MSP_CALLING_IDENTITIES lines=$(v msp)"
if [ "$(v health)" = 200 ] && [ "$ok" = 1 ] && [ "$(v r1)" = present ] && [ "$(v irr)" = 1 ] && [ "$(v msp)" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
