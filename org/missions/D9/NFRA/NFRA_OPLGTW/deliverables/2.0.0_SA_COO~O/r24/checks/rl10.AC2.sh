#!/usr/bin/env bash
# OPLGTW OG-rl-10 AC2 (R32, the login through the DEPLOYED code): RL10_LOGIN.json records an on-host run of the installed
# opal_portal integration's own _PortalSession.token() with the real service secret: login OK, through www.opalinvest.dev,
# no token or credential recorded. Its body digest is found in the SSM invocation's own output (`RL10_DIGEST <sha256>`).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL10_LOGIN.json"
[ -f "$F" ] || { echo "RL10_LOGIN.json absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
read -r cid iid dig ok <<<"$(python - "$(native "$F")" "$c" <<'PY' | tr -d '\r'
import hashlib, json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body") or {}
ok = (b.get("login") == "OK" and b.get("auth_host") == "www.opalinvest.dev" and b.get("installed_code") is True
      and b.get("served_release") == sys.argv[2] and "token" not in b and "password" not in b and "email" not in b)
print(d.get("ssm_command_id", "NONE"), d.get("instance_id", "NONE"),
      hashlib.sha256(json.dumps(b, sort_keys=True).encode("utf-8")).hexdigest(), "yes" if ok else "no")
PY
)"
out=$(bash .tools/aws ssm get-command-invocation --command-id "$cid" --instance-id "$iid" --region us-east-1 \
      --query '[Status,StandardOutputContent]' --output text 2>&1 | tr -d '\r')
st=$(printf '%s\n' "$out" | head -1 | awk '{print $1}')
found=no; printf '%s\n' "$out" | grep -q "RL10_DIGEST $dig" && found=yes
echo "portal login OK through the front door on the served release: $ok; ssm status ${st:-NONE}; digest in host output: $found"
[ "$ok" = yes ] && [ "$st" = Success ] && [ "$found" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
