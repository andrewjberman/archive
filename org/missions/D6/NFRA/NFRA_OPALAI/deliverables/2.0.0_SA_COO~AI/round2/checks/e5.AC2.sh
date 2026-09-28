#!/usr/bin/env bash
# OA-e-5 AC2 (the SERVED seam, not the self-report): the commit the file says the gateway serves is the one the host
# serves NOW -- /opt/opal-gateway/app/tools.py read LIVE over SSM has the md5 of that commit's app/tools.py -- and the
# file's gap_b_in_served flag equals whether that commit's app/tools.py carries the gap-B retry (by content).
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~14/E5_TEAMS_WATCH_REMEASURE.json"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
sc=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('served_commit',''))" "$F" 2>/dev/null | tr -d '\r')
gb=$(python -c "import json,sys;print(str(json.load(open(sys.argv[1],encoding='utf-8')).get('gap_b_in_served','')).lower())" "$F" 2>/dev/null | tr -d '\r')
git cat-file -e "${sc}^{commit}" 2>/dev/null || { echo "served_commit '$sc' does not resolve"; echo "RESULT: FAIL"; exit 1; }
want=$(git show "$sc:infra/aws/ec2/opal-gateway/app/tools.py" | md5sum | awk '{print $1}')
# Gap B is read BY CONTENT (the _get_messages retry that marks a page select_fallback), never by the ancestry of the
# laptop fix 678891171b: the served release carries it on a release branch, where that commit is not an ancestor
# (measured at the cut: fe94911257 serves the fallback, and 678891171b is NOT its ancestor).
anc=false; git show "$sc:infra/aws/ec2/opal-gateway/app/tools.py" | grep -q 'select_fallback' && anc=true
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids "$GW_INSTANCE" --document-name AWS-RunShellScript \
  --parameters 'commands=["md5sum /opt/opal-gateway/app/tools.py || echo MISSING"]' --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""
for i in 1 2 3 4 5 6 7 8 9 10; do
  st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query Status --output text 2>/dev/null | tr -d '\r')
  [ "$st" = Success ] || [ "$st" = Failed ] && break
  sleep 3
done
got=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query StandardOutputContent --output text 2>/dev/null | tr -d '\r' | awk '{print $1}' | head -1)
echo "served_commit=$sc md5=$want; live md5=${got:-NONE} (ssm status ${st:-NONE}); gap-B in served (content) measured=$anc file=$gb"
if [ -n "$got" ] && [ "$got" = "$want" ] && [ "$anc" = "$gb" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
