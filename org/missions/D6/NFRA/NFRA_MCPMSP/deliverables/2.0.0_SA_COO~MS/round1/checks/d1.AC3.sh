#!/usr/bin/env bash
# MS-d-1 AC3 (the SERVED host, read live over SSM, with its control): on the gateway instance /health answers 200 (the
# control), the md5 of each of /opt/opal-gateway/app/{tenant_registry,firm_role,admin_tenants}.py equals that file's
# blob at the manifest's deployed_commit (bytes resolved by content), and /opt/opal-gateway/.env carries exactly one
# FIRM_ROLE_ARNS line (its value is never printed).
. "$(dirname "$0")/_root.sh"
c=$(git show "HEAD:infra/aws/ec2/EC2_MANIFEST.json" | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" 2>/dev/null | tr -d '\r')
want=""; for f in tenant_registry firm_role admin_tenants; do m=$(git show "$c:$G/app/$f.py" 2>/dev/null | md5sum | cut -c1-32); want="$want $f=$m"; done
T="${TMPDIR:-/tmp}/ms_d1_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'for f in tenant_registry firm_role admin_tenants; do echo "$f=$(md5sum /opt/opal-gateway/app/$f.py 2>/dev/null | cut -c1-32)"; done; '
       'echo "firm_role_arns_lines=$(grep -c "^FIRM_ROLE_ARNS=" /opt/opal-gateway/.env 2>/dev/null)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"; rm -rf "$T"
h=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^health=//p'); n=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^firm_role_arns_lines=//p')
ok=1; got=""; for f in tenant_registry firm_role admin_tenants; do l=$(printf '%s\n' "$SSM_OUT" | sed -n "s/^$f=//p"); w=$(printf '%s' "$want" | tr ' ' '\n' | sed -n "s/^$f=//p"); got="$got $f=$([ -n "$l" ] && [ "$l" = "$w" ] && echo match || echo MISMATCH)"; [ -n "$l" ] && [ "$l" = "$w" ] || ok=0; done
echo "ssm command=$SSM_CID status=$SSM_ST; deployed_commit=$c; /health=$h;$got; FIRM_ROLE_ARNS lines=$n"
if [ "$h" = 200 ] && [ "$ok" = 1 ] && [ "$n" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
