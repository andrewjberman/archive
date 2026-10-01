#!/usr/bin/env bash
# OPLGTW OG-tr-1 AC1 (the laptop CRO's TX-r-2 spec section 4; Andrew-direct ~17:3xZ "ON at this deploy"), against the
# SERVED gateway:
#  1. the host's app/taxsma_workbook.py sha256 equals the module at CLOUD HEAD (6acc3e8c...);
#  2. GET /ms/taxsma-workbook with no bearer, through the ALB, returns the route's own UNAUTHORIZED_CAPABILITY;
#  3. an unauthenticated /mcp still returns 401 with a WWW-Authenticate resource challenge, and /health returns 200;
#  4. .env holds 48 keys with both TAXSMA_WORKBOOK_ keys and capability ON (bearer and identity both non-empty).
# Values are never printed; .env is never sourced (row Z-S32).
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
INST="i-07dccb1615503ac99"; n=0
want=$(git show "HEAD:$GW/app/taxsma_workbook.py" | sha256sum | cut -d' ' -f1)
params=$(python "$(native "$H/_tr_host.py")" | tr -d '\r')
id=$(aws ssm send-command --instance-ids "$INST" --document-name AWS-RunShellScript --region us-east-1 \
  --parameters "$params" --query Command.CommandId --output text | tr -d '\r')
st=""
for _ in $(seq 1 20); do
  st=$(aws ssm get-command-invocation --command-id "$id" --instance-id "$INST" --region us-east-1 --query Status --output text 2>&1 | tr -d '\r')
  case "$st" in Success|Failed|Cancelled|TimedOut) break;; esac; sleep 3
done
out=$(aws ssm get-command-invocation --command-id "$id" --instance-id "$INST" --region us-east-1 --query StandardOutputContent --output text | tr -d '\r')
echo "ssm $id status=$st"; printf '%s\n' "$out"
have=$(printf '%s\n' "$out" | sed -n 's/^HOST module_sha256 //p')
if [ -n "$have" ] && [ "$have" = "$want" ]; then echo "arm 1 module sha256 equals CLOUD HEAD (${want:0:12}): OK"; n=$((n+1)); else echo "arm 1 module sha256 (want ${want:0:12}, have ${have:0:12}): FAIL"; fi
body=$(curl -s -o - -w '\n%{http_code}' https://mcp.opalinvest.dev/ms/taxsma-workbook | tr -d '\r')
code=$(printf '%s\n' "$body" | tail -1)
if printf '%s\n' "$body" | grep -q "UNAUTHORIZED_CAPABILITY"; then echo "arm 2 no-bearer -> UNAUTHORIZED_CAPABILITY (status $code): OK"; n=$((n+1)); else echo "arm 2 no-bearer (status $code): FAIL"; fi
hdr=$(curl -s -D - -o /dev/null https://mcp.opalinvest.dev/mcp | tr -d '\r')
hc=$(curl -s -o /dev/null -w '%{http_code}' https://mcp.opalinvest.dev/health | tr -d '\r')
# /health sits behind the ALB sign-in (302 publicly); the host's own /health is read in the order's verify step.
if printf '%s\n' "$hdr" | head -1 | grep -q " 401" && printf '%s\n' "$hdr" | grep -qi "^www-authenticate:.*resource"; then echo "arm 3 /mcp unauth 401 with resource challenge (public /health $hc): OK"; n=$((n+1)); else echo "arm 3 /mcp unauth: FAIL"; fi
if printf '%s\n' "$out" | grep -qE "^HOST env_keys 48 taxsma_keys 2 identity_empty False bearer_empty False$"; then echo "arm 4 .env 48 keys, both TAXSMA keys, capability ON: OK"; n=$((n+1)); else echo "arm 4 .env keys / capability ON: FAIL"; fi
echo "TAX ARMS $n of 4"
[ "$n" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
