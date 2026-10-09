#!/usr/bin/env bash
# OPLGTW OG-rl-15 AC1 (round 32 item 6, release r29: RELEASE + NEVER-2 + DRAIN-BACK + FLOOR): the manifest's
# deployed_commit descends from live r28 aa75078e1b; the host's shipped files equal the release bytes (source-only
# tests/, the deploy tool's own deploy-to-ec2.sh and ops/, and runbooks/ excluded, rows Z-W28-S4/S28); the ledger entry
# nfra-oplgtw-gateway-release-r29 is committed and its sentinel gone; after the drain-back CLOUD equals live for the
# gateway tree except the CLOUD-only runbooks/SCHWAB_PILOT_RUNBOOK.md; the floor holds -- rl4.AC1 against the r29 key
# set (ENV_KEYS_R29.txt, 52 names: r17b + MAIL_SENDER_DOMAIN_TABLE) and ht.AC2 at 52 keys.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
SLUG="nfra-oplgtw-gateway-release-r29"; LIVE0="aa75078e1b72a28219e6148d3ec8e9bf705ea111"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
desc=no; [ "$c" != "$LIVE0" ] && git merge-base --is-ancestor "$LIVE0" "$c" 2>/dev/null && desc=yes
L=$( [ "$desc" = yes ] && git diff --name-only "$LIVE0" "$c" -- "$GW" | sed "s#^$GW/##" | grep -v '^runbooks/' | grep -v '^tests/' | grep -v '^ops/' | grep -v '^deploy-to-ec2\.sh$' | tr '\n' ' ')
n=0; eq=0
if [ -n "$L" ]; then
  cmd=$(python -c "import json,sys;print(json.dumps({'commands':['cd /opt/opal-gateway && md5sum '+sys.argv[1]]}))" "$L" | tr -d '\r')
  ssm_run "$cmd"
  for f in $L; do n=$((n+1)); w=$(git show "$c:$GW/$f" 2>/dev/null | md5sum | cut -c1-32); h=$(printf '%s\n' "$SSM_OUT" | grep "  $f\$" | cut -c1-32); [ -n "$h" ] && [ "$h" = "$w" ] && eq=$((eq+1)); done
fi
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
CLOUD_ONLY="runbooks/SCHWAB_PILOT_RUNBOOK.md app/admin_api.py app/admin_fabric.py app/refs/fabric_boxes.json tests/test_admin_fabric.py app/teams_route.py tests/test_teams_route.py app/server.py"   # A7 D1: MP-x-1 and CT-i-11, excluded from r29
ndiff=$(git diff --name-only "$c" HEAD -- "$GW" | sed "s#^$GW/##" | while read -r p; do case " $CLOUD_ONLY " in *" $p "*) ;; *) echo "$p";; esac; done | grep -c .)
echo "deployed=${c:0:10} descends from aa75078e1b=$desc; host shipped files equal the release bytes: $eq of $n"
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent; gateway files differing live..CLOUD after drain-back (listed CLOUD-only paths excluded) $ndiff"
f1=no; RL4_ENV_KEYS_BASELINE="$D/r32/ENV_KEYS_R29.txt" bash "$D/r14/checks/rl4.AC1.sh" >/dev/null 2>&1 && f1=yes
f2=no; HT_ENV_KEYS_COUNT=52 bash "$D/hxteams/checks/ht.AC2.sh" >/dev/null 2>&1 && f2=yes
echo "floor: rl4.AC1 $f1; ht.AC2 $f2"
[ "$desc" = yes ] && [ "$n" -ge 1 ] && [ "$eq" = "$n" ] && [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$ndiff" = 0 ] && [ "$f1" = yes ] && [ "$f2" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
