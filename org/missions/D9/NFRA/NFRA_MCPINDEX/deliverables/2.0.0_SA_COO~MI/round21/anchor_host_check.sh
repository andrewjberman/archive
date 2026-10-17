#!/usr/bin/env bash
# anchor_host_check.sh <catalog file> -- read-only, on the gateway host: every tool_index `definition` anchor of the CANDIDATE catalog names its tool within the 5 lines the
# index check (c11_index.definition_ok) allows, in the host's DEPLOYED app tree (/opt/opal-gateway). Ships only the {tool: definition} map (small), nothing is written on the host.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/checks/_root.sh"
CAT="${1:?usage: anchor_host_check.sh <catalog file>}"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_anchor_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$CAT")" <<'PYEOF'
import base64, json, sys, yaml
doc = yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
m = {e["tool"]: e.get("definition") for e in doc["tool_index"] if isinstance(e, dict)}
prog = ("import json,os,sys\nm=json.load(open('/tmp/anchor_map.json'))\nbad=[]\nfor t,d in m.items():\n"
        " try:\n  p,l=str(d).rsplit(':',1); L=open(os.path.join('/opt/opal-gateway',p),encoding='utf-8').read().splitlines(); n=int(l)\n"
        "  ok=any(t in x for x in L[max(0,n-6):n+5])\n except Exception:\n  ok=False\n if not ok: bad.append(t)\n"
        "print('ANCHORS %d of %d name their tool within 5 lines in the deployed tree; misses %d: %s'%(len(m)-len(bad),len(m),len(bad),','.join(bad[:8])))\n")
b = lambda s: base64.b64encode(s).decode()
cmd = ('echo "commit=$(cat /opt/opal-gateway/.deployed_commit 2>/dev/null)"; echo ' + b(json.dumps(m).encode()) + ' | base64 -d > /tmp/anchor_map.json; '
       'echo ' + b(prog.encode()) + ' | base64 -d > /tmp/anchor_check.py; cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/anchor_check.py 2>&1 | tail -4; echo "RC=${PIPESTATUS[0]}"; rm -f /tmp/anchor_map.json /tmp/anchor_check.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 30); do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
printf '%s\n' "$o" | grep -E '^(commit=|ANCHORS|RC=|Traceback|.*Error)' | cut -c1-260
echo "ssm command=${cid:-NONE} status=${st:-NONE}"
if printf '%s\n' "$o" | grep -q '^RC=0' && printf '%s\n' "$o" | grep -qE 'misses 0:'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
