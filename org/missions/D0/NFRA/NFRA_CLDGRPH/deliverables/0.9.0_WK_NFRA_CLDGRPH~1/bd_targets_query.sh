#!/usr/bin/env bash
# =============================================================================
# bd_targets_query.sh -- NFRA_CLDGRPH TO-CG-D-12 / D12-AC5.
#
# The sibling of triggers_query.sh, same transport, one question: WHICH Lambdas
# do the opal-data-bd bucket's TRIGGERS edges reach.
#
#   MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode)
#   WHERE e.edge_type = 'TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd'
#   RETURN b.node_id AS target ORDER BY target
#
# The served projection is only reachable from inside the VPC through Cloud Map
# (projection.opal-globgrph.local), so the read goes through the gateway
# instance i-07dccb1615503ac99 by SSM -- the shape TO-CG-C-1 established.
#
# Prints the served JSON response WHOLE, beside the pointer VINTAGE the answer
# was read at and a SHAPE CONTROL (a query that must answer non-zero on any
# live graph). Without the control an empty target list and a dead transport
# read identically -- the silent-zero class this whole cell exists to close.
#
# THE CYPHER TRAVELS AS BASE64 and is posted from a FILE with --data-binary.
# A cypher STRING LITERAL cannot survive shell re-quoting inside an SSM command
# document: the shape this project inherited, json.dumps(q) then replacing the
# single quote with the '\'' idiom, is correct only inside a SINGLE-quoted word
# and json.dumps emits a DOUBLE-quoted one, so the host shell handed curl
# `e.edge_type='"TRIGGERS"'` -- a valid, unmatchable query and a clean FALSE
# ZERO with no error and a correct vintage (row NFRA_CLDGRPH-W1-S10). base64 is
# alphanumeric + / + = : there is nothing left for a shell to reinterpret. Each
# query is echoed AS THE SERVER RECEIVED IT beside its answer, so the bytes that
# were evaluated are always in the output.
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
WORK="${TMPDIR:-/tmp}/cgd12-bdtargets-$$"
mkdir -p "$WORK"

if [ ! -x "$AWS" ]; then
  echo "ERROR: aws shim not found at $AWS -- failing closed, not falling back to a bare aws." >&2
  exit 2
fi

python - "$WORK/params.json" "$ENDPOINT" <<'PYEOF'
import base64, json, sys
out, endpoint = sys.argv[1], sys.argv[2]
queries = [
    ("NODES (shape control -- a zero here means the transport, not the graph)",
     "MATCH (n) RETURN count(n) AS nodes"),
    ("BD TARGETS (D12-AC5)",
     "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN b.node_id AS target ORDER BY target"),
    ("BD TRIGGERS edges with their source bucket",
     "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN a.node_id AS source, b.node_id AS target ORDER BY target"),
]
cmds = ["echo '===== HEALTH (the vintage this answer is read at) ====='",
        "curl -sS -m 20 %s/health; echo" % endpoint]
for i, (label, q) in enumerate(queries):
    b64 = base64.b64encode(q.encode("utf-8")).decode("ascii")
    f = "/tmp/cgd12_bd_q%d.cypher" % i
    cmds.append("echo '===== %s ====='" % label)
    cmds.append("printf %%s %s | base64 -d > %s" % (b64, f))
    cmds.append("echo '--- query as the server received it ---'; cat %s; echo" % f)
    cmds.append("curl -sS -m 20 -H 'Content-Type: text/plain' --data-binary @%s %s/cypher; echo" % (f, endpoint))
    cmds.append("rm -f %s" % f)
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
