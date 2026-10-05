#!/usr/bin/env bash
# OPLGTW OG-rl-6 AC3 (A1, Phase C; CTO R14 @b478972fec, msg 29402): /yearinreview is SERVED behind the /sprint identity
# wall on the deployed release: the host's four kit files (app/server.py, app/yearinreview_view.py,
# app/static/yearinreview/index.html, tests/test_yearinreview_view.py) equal the manifest's deployed_commit bytes; an
# UNAUTHENTICATED public GET https://mcp.opalinvest.dev/yearinreview is redirected (302) to login.microsoftonline.com
# (the ALB OIDC wall); and a host-local GET with NO identity header is refused 401 (the app's own wall). The signed-in
# 200 is Andrew's act at his browser and is not graded here.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
F="app/server.py app/yearinreview_view.py app/static/yearinreview/index.html tests/test_yearinreview_view.py"
want=""; for f in $F; do want="$want$(git show "$c:$GW/$f" 2>/dev/null | md5sum | cut -c1-32)  $f
"; done
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/server.py app/yearinreview_view.py app/static/yearinreview/index.html tests/test_yearinreview_view.py 2>&1; echo LOCAL_CODE=$(curl -s -o /dev/null -w %{http_code} http://localhost:8080/yearinreview)"]}'
eq=0; for f in $F; do w=$(printf '%s' "$want" | grep "  $f\$" | cut -c1-32); h=$(printf '%s\n' "$SSM_OUT" | grep "  $f\$" | cut -c1-32); [ -n "$h" ] && [ "$h" = "$w" ] && eq=$((eq+1)); done
lc=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^LOCAL_CODE=\([0-9]*\).*/\1/p')
pub=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' --max-time 20 https://mcp.opalinvest.dev/yearinreview)
pc=${pub%% *}; pr=${pub#* }
redir=no; [ "$pc" = 302 ] && printf '%s' "$pr" | grep -q 'login.microsoftonline.com' && redir=yes
echo "deployed_commit ${c:0:10}; host kit files equal the release bytes: $eq of 4; public unauthenticated GET: $pc to login.microsoftonline.com=$redir; host-local no-identity GET: ${lc:-none}"
[ "$eq" = 4 ] && [ "$redir" = yes ] && [ "$lc" = 401 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
