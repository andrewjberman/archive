#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC2 (CTO ruling AC2), against the SERVED gateway:
#  1. the host's app/teams_route.py sha256 equals db92656c72's blob (f4705400...);
#  2. .env holds 50 keys (48 + TEAMS_BEARER + TEAMS_BEARER_LABELS), TEAMS_BEARER non-empty, the label 'teamsassist',
#     both TAXSMA_WORKBOOK_ values still non-empty;
#  3. GET https://mcp.opalinvest.dev/hx/teams/x with no bearer is refused BY THE APP (401 or 404, never a 3xx);
#  4. GET / still answers 302 (the ALB sign-in is untouched for everything else).
# Values are never printed; .env is never sourced (row Z-S32).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/hxteams/checks"
. "$H/../../r13/checks/_ssm.sh"
n=0; WANT="f470540078a23b8a874e0bebd2fa67cad7e23a82c1aa513c6f904e012ae87337"
ssm_run "$(python "$(native "$H/_ht_host.py")" | tr -d '\r')"
echo "ssm $SSM_ID status=$SSM_STATUS"; printf '%s\n' "$SSM_OUT"
have=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^HOST teams_route_sha256 //p')
if [ "$have" = "$WANT" ]; then echo "arm 1 host teams_route.py = db92656c72 (${WANT:0:12}): OK"; n=$((n+1)); else echo "arm 1 host teams_route.py (want ${WANT:0:12}, have ${have:0:12}): FAIL"; fi
if printf '%s\n' "$SSM_OUT" | grep -qE "^HOST env_keys 50 teams_bearer_present True teams_bearer_empty False teams_labels_ok True tax_nonempty True$"; then
  echo "arm 2 .env 50 keys, TEAMS_BEARER non-empty, label teamsassist, Tax keys intact: OK"; n=$((n+1)); else echo "arm 2 .env shape: FAIL"; fi
c3=$(curl -s -o /dev/null -w '%{http_code}' https://mcp.opalinvest.dev/hx/teams/x | tr -d '\r')
case "$c3" in 401|404) echo "arm 3 /hx/teams/x no bearer -> $c3 (app refusal, no redirect): OK"; n=$((n+1));; *) echo "arm 3 /hx/teams/x no bearer -> $c3: FAIL";; esac
c4=$(curl -s -o /dev/null -w '%{http_code}' https://mcp.opalinvest.dev/ | tr -d '\r')
if [ "$c4" = 302 ]; then echo "arm 4 / -> 302 (sign-in intact): OK"; n=$((n+1)); else echo "arm 4 / -> $c4: FAIL"; fi
echo "SERVED ARMS $n of 4"
[ "$n" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
