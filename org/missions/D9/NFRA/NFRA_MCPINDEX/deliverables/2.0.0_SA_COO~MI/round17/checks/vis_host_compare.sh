#!/usr/bin/env bash
# vis_host_compare.sh -- the issuer's one real run of MX-c-19's outcome on the SERVED host (MX-r-14, round 17): the firm-visibility matrix (vis_matrix.py: every silver row x six
# principals, through _silver_answer) is run ON the gateway host under its own venv and its own deployed catalog, and its summary compared with the same run on the cut tree
# (git archive of the deploy-only commit given as $1, default the live ref in EC2_MANIFEST). Read-only. Prints both VIS lines and RESULT.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
CUT="${1:-$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')}"
T="${TMPDIR:-/tmp}/mx_vis_$$"; mkdir -p "$T/cut"
git archive "$CUT" infra/aws/ec2/opal-gateway | tar -x -C "$T/cut"
local_line=$(python "$(native "$H/vis_summary.py")" "$(native "$T/cut/infra/aws/ec2/opal-gateway")" | tr -d '\r' | grep '^VIS ')
python - "$T/params.json" "$(native "$H/vis_matrix.py")" "$(native "$H/vis_summary.py")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
cmd = ('echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/vis_matrix.py; echo ' + b(sys.argv[3]) + ' | base64 -d > /tmp/vis_summary.py; chmod 644 /tmp/vis_matrix.py /tmp/vis_summary.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user env VIS_MATRIX=/tmp/vis_matrix.py ./.venv/bin/python /tmp/vis_summary.py /opt/opal-gateway 2>&1 | tail -3; rm -f /tmp/vis_matrix.py /tmp/vis_summary.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 30); do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
host_line=$(printf '%s\n' "$o" | grep '^VIS ' | tail -1)
rm -rf "$T"
echo "CUT  ($CUT): $local_line"
echo "HOST (ssm $cid $st): ${host_line:-none: $(printf '%s' "$o" | head -c 300 | tr '\n' ' ')}"
if [ -n "$local_line" ] && [ "$local_line" = "$host_line" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
