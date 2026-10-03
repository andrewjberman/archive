#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC4 (CTO ruling AC4, the regression floor) on the SERVED gateway and the committed record:
#  1. /hx/mail/x and /hx/transcripts/x with no bearer answer as on 3a7d6a7dc8: 404 from the app (measured 17:5xZ
#     2026-10-02, body 'Not Found'; the CTO ruling's '401' was the request's /hx/mail/x claim, re-measured), never a 3xx;
#  2. GET /ms/taxsma-workbook with no bearer still returns the route's own UNAUTHORIZED_CAPABILITY (as on 3a7d6a7dc8),
#     and the host's app/taxsma_workbook.py equals db92656c72's blob (Z-S41, 56d4f490...);
#  3. NEVER-2: the ledger entry for nfra-oplgtw-hx-teams-release is committed and its sentinel gone;
#  4. NARROW: the manifest's deployed_commit descends from 3a7d6a7dc8 and ships ONLY the release set (app/teams_route.py,
#     tests/test_teams_route.py, app/config.py, app/server.py, app/taxsma_workbook.py, deploy-to-ec2.sh).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/hxteams/checks"
. "$H/../../r13/checks/_ssm.sh"
n=0; SLUG="nfra-oplgtw-hx-teams-release"; LIVE0="3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7"
TAXWANT="56d4f49017e4c17f721c8613e57195cfe341b7b6e0e1f96bc3524999a65f83a7"
cm=$(curl -s -o /dev/null -w '%{http_code}' https://mcp.opalinvest.dev/hx/mail/x | tr -d '\r')
ct=$(curl -s -o /dev/null -w '%{http_code}' https://mcp.opalinvest.dev/hx/transcripts/x | tr -d '\r')
if [ "$cm" = 404 ] && [ "$ct" = 404 ]; then echo "arm 1 /hx/mail/x $cm, /hx/transcripts/x $ct: OK"; n=$((n+1)); else echo "arm 1 /hx/mail/x $cm, /hx/transcripts/x $ct: FAIL"; fi
body=$(curl -s -o - -w '\n%{http_code}' https://mcp.opalinvest.dev/ms/taxsma-workbook | tr -d '\r'); tc=$(printf '%s\n' "$body" | tail -1)
ssm_run "$(python "$(native "$H/_ht_host.py")" | tr -d '\r')"
have=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^HOST taxsma_workbook_sha256 //p')
if printf '%s\n' "$body" | grep -q "UNAUTHORIZED_CAPABILITY" && [ "$have" = "$TAXWANT" ]; then echo "arm 2 Tax route no-bearer UNAUTHORIZED_CAPABILITY ($tc); host taxsma_workbook.py = db92656c72 (${TAXWANT:0:12}): OK"; n=$((n+1)); else echo "arm 2 Tax route ($tc) / host module (have ${have:0:12}): FAIL"; fi
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
if [ "$entry" -ge 1 ] && [ "$sent" = no ]; then echo "arm 3 ledger entry files at HEAD=$entry; sentinel at HEAD=$sent: OK"; n=$((n+1)); else echo "arm 3 ledger entry files at HEAD=$entry; sentinel at HEAD=$sent: FAIL"; fi
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
desc=no; [ "$c" != "$LIVE0" ] && git merge-base --is-ancestor "$LIVE0" "$c" 2>/dev/null && desc=yes
allowed=$(printf '%s\n' app/teams_route.py tests/test_teams_route.py app/config.py app/server.py app/taxsma_workbook.py deploy-to-ec2.sh | sed "s|^|$GW/|" | sort -u)
shipped=$( [ "$desc" = yes ] && git diff --name-only "$LIVE0" "$c" -- "$GW" | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
nf=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
echo "deployed=$c descends from 3a7d6a7dc8=$desc; gateway files shipped $nship, outside the release set $nf"
if [ "$desc" = yes ] && [ "$nship" -ge 5 ] && [ "$nf" = 0 ]; then echo "arm 4 narrow release: OK"; n=$((n+1)); else echo "arm 4 narrow release: FAIL"; fi
echo "FLOOR ARMS $n of 4"
[ "$n" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
