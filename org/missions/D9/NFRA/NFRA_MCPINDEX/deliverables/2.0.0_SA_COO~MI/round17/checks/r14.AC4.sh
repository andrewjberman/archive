#!/usr/bin/env bash
# MX-r-14 AC4 (FWD-22 live: the round 17 catalog on the SERVED host): the DEPLOYED app/refs/DATA_CATALOG.yaml is version 0.5 with 78 harvest rows and 216 table rows
# (each with a key_template, 5 retired), 304 rows in all with a non-empty nl_tags on every one (44 marked inferred) and a firm field on exactly 24; its bytes (md5)
# equal this tree's catalog, and every read_tool it names is a tool the deployed commit serves (tool_census.py of this tree, equal to the deployed tree once the
# ledger closes). Probe r14_ac4_host.py over SSM, as r13.AC4.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_r14_ac4_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/r14_ac4_host.py")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
cmd = ('echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/r14_ac4_host.py; chmod 644 /tmp/r14_ac4_host.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r14_ac4_host.py 2>&1 | tail -6; rm -f /tmp/r14_ac4_host.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
if [ -n "$R14_AC4_HOST_OUT" ]; then o=$(tr -d '\r' < "$R14_AC4_HOST_OUT"); st=PLANTED; cid=PLANTED   # the issuer's cut-time planted arms only
else
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 30); do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
fi
rm -rf "$T"
c=$(printf '%s\n' "$o" | sed -n 's/^CATALOG //p'); tl=$(printf '%s\n' "$o" | sed -n 's/^TOOLS //p'); hm=$(printf '%s\n' "$o" | sed -n 's/^MD5 //p')
[ -n "$c" ] || echo "INSTRUMENT: no CATALOG line with status=${st:-NONE}; fetched output head: $(printf '%s' "$o" | head -c 300 | tr '\n' ' ')"
echo "HOST CATALOG $c; md5 ${hm:-none}"
lm=$(python -c "import hashlib,sys; print(hashlib.md5(open('infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml','rb').read()).hexdigest())" | tr -d '\r')
cen=$(timeout 120 python workflows/atom_decomposition/tool_census.py 2>/dev/null | python -c "import sys,json; print(','.join(sorted(t['tool'] for t in json.load(sys.stdin)['tools'])))" | tr -d '\r')
unserved=""; for t in $(printf '%s' "$tl" | tr ',' ' '); do case ",$cen," in *",$t,"*) ;; *) unserved="$unserved $t";; esac; done
echo "tree md5 $lm; read_tool names $(printf '%s' "$tl" | tr ',' '\n' | grep -c .), unserved by the deployed commit:${unserved:- none}"
ok=1
[ "$c" = "version=0.5 harvest=78 table=216 key_template=216 retired=5 rows=304 nl_tags=304 inferred=44 firm=24" ] || ok=0
[ -n "$hm" ] && [ "$hm" = "$lm" ] || ok=0
[ -z "$unserved" ] || ok=0
if [ "$ok" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
