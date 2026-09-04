#!/usr/bin/env bash
# =============================================================================
# triggers_query.sh -- NFRA_CLDGRPH TO-CG-D-1 / D1-AC5.
#
# Reads the TRIGGERS edge count from the LIVE served projection, never a local
# DB. The serving process is only reachable from inside the VPC through Cloud
# Map (projection.opal-globgrph.local), so the read goes through the gateway
# instance by SSM -- the same shape TO-CG-C-1 used (deliverables/
# 0.7.0_AE_CloudOps~T/CG-s-4.serving-service.result.md, "Live exercise").
#
# Prints the served JSON response WHOLE -- the count, its denominator context
# and the pointer vintage the answer was read at -- so the number is never
# quoted without the frame that makes it mean something.
#
# Read-only: three cypher MATCH ... RETURN reads and one /health GET. No write,
# no marker, no pointer, no S3 object.
#
# Rule 16: Git Bash 3.6.7 utilities only. ASCII only.
# =============================================================================
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../../../../../.." && pwd)"
AWS="$REPO_ROOT/.tools/aws"
INSTANCE="i-07dccb1615503ac99"
ENDPOINT="http://projection.opal-globgrph.local:8181"
WORK="${TMPDIR:-/tmp}/cgd1-triggers-$$"
mkdir -p "$WORK"

if [ ! -x "$AWS" ]; then
  echo "ERROR: aws shim not found at $AWS -- failing closed, not falling back to a bare aws." >&2
  exit 2
fi

# --- the three reads -----------------------------------------------------------
# 1. SHAPE CONTROL: a query that must answer non-zero on any live graph. If this
#    returns nothing, the transport is broken and a zero from query 2 would be a
#    FALSE ZERO -- exactly the silent-zero class row S20 filed.
# 2. THE CRITERION: the TRIGGERS edge count.
# 3. THE RECORD: the declared bd-pipeline Lambda targets behind those edges.
Q1='MATCH (n) RETURN count(n) AS nodes'
Q2="MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' RETURN count(e) AS triggers"
Q3="MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN b.node_id AS target ORDER BY target"

# Build the SSM parameters document with python: the commands carry nested
# double quotes and a cypher string, and hand-escaping them through the shell is
# where this call goes wrong silently.
python - "$WORK/params.json" "$ENDPOINT" "$Q1" "$Q2" "$Q3" <<'PYEOF'
import json, sys
out, endpoint, q1, q2, q3 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
def curl(label, q):
    return ("echo '===== %s ====='; "
            "curl -sS -m 20 -H 'Content-Type: text/plain' --data %s %s/cypher; "
            "echo") % (label, json.dumps(q).replace("'", "'\"'\"'"), endpoint)
cmds = [
    "echo '===== HEALTH ====='",
    "curl -sS -m 20 %s/health; echo" % endpoint,
    curl("NODES (shape control -- a zero here means the transport, not the graph)", q1),
    curl("TRIGGERS (D1-AC5)", q2),
    curl("TRIGGERS targets from opal-data-bd", q3),
]
json.dump({"commands": cmds}, open(out, "w"))
print("OK: wrote %s" % out)
PYEOF
[ -s "$WORK/params.json" ] || { echo "ERROR: could not build the SSM parameters document." >&2; exit 2; }

CMD_ID="$("$AWS" ssm send-command \
  --instance-ids "$INSTANCE" \
  --document-name AWS-RunShellScript \
  --parameters "file://$WORK/params.json" \
  --query 'Command.CommandId' --output text | tr -d '\r\n')"

if [ -z "$CMD_ID" ]; then
  echo "ERROR: ssm send-command returned no CommandId." >&2
  exit 3
fi
echo "ssm command id: $CMD_ID  (instance $INSTANCE)"

# --- bounded poll: at most 20 x 6s. A timeout is a RECORDED outcome, never a stall.
i=0
STATUS="Pending"
while [ $i -lt 20 ]; do
  i=$((i + 1))
  sleep 6
  STATUS="$("$AWS" ssm get-command-invocation --command-id "$CMD_ID" --instance-id "$INSTANCE" \
    --query 'Status' --output text 2>/dev/null | tr -d '\r\n')"
  case "$STATUS" in
    Success | Failed | Cancelled | TimedOut) break ;;
  esac
done

echo "ssm invocation status: $STATUS  (poll $i of 20)"
echo "----- StandardOutputContent (whole) -----"
"$AWS" ssm get-command-invocation --command-id "$CMD_ID" --instance-id "$INSTANCE" \
  --query 'StandardOutputContent' --output text
echo "----- StandardErrorContent (whole) -----"
"$AWS" ssm get-command-invocation --command-id "$CMD_ID" --instance-id "$INSTANCE" \
  --query 'StandardErrorContent' --output text

rm -rf "$WORK"
[ "$STATUS" = "Success" ] || exit 4
