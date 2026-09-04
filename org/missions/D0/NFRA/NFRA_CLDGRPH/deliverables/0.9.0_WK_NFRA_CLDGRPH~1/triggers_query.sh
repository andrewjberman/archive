#!/usr/bin/env bash
# =============================================================================
# triggers_query.sh -- NFRA_CLDGRPH TO-CG-D-1 / D1-AC5, and TO-CG-D-12 / D12-AC4.
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
# -----------------------------------------------------------------------------
# REPAIRED 2026-09-04 by 0.9.0_WK_NFRA_CLDGRPH~1 on TO-CG-D-12 (row
# NFRA_CLDGRPH-W1-S10). THE TRANSPORT WAS PRODUCING A FALSE ZERO.
#
# The previous version built each SSM command with
#     json.dumps(q).replace("'", "'\"'\"'")
# The `'\''` idiom is only correct INSIDE a single-quoted shell word, but
# json.dumps wraps the value in DOUBLE quotes. Parsed by the host shell, the
# argument that reached `curl --data` was
#     MATCH ... WHERE e.edge_type='"TRIGGERS"' RETURN count(e) AS triggers
# -- the string literal became the 10-character value "TRIGGERS" WITH its
# double quotes. That is a SYNTACTICALLY VALID query which cannot match any
# row, so the server answered `{"rows":[{"triggers":0}]}` with no error, at a
# correct vintage, beside a shape control that passed because it contains no
# string literal. Every WHERE-filtered read through this script was a FALSE
# ZERO, independent of the graph -- measured 2026-09-04 13:2xZ: the same three
# queries carried unmangled returned triggers=171, notifies=41 (the derive's
# own log says NOTIFIES=41) and the three bd-pipeline targets.
#
# THE FIX: the cypher travels as base64 (alphanumeric + / + =, nothing a shell
# can reinterpret), is decoded into a file on the gateway, and curl posts the
# FILE with --data-binary. The queries are unchanged. Each command echoes the
# decoded query before sending it, so the bytes the server evaluated are in the
# output beside its answer and this class of defect cannot hide again.
# -----------------------------------------------------------------------------
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
#    FALSE ZERO -- exactly the silent-zero class row S20 filed. NOTE it contains
#    no string literal, which is why it survived the mangle the repair note
#    above describes: a control must exercise the SAME hazard as the criterion,
#    and this one did not.
# 2. THE CRITERION: the TRIGGERS edge count.
# 3. THE RECORD: the declared bd-pipeline Lambda targets behind those edges.
python - "$WORK/params.json" "$ENDPOINT" <<'PYEOF'
import base64, json, sys
out, endpoint = sys.argv[1], sys.argv[2]
queries = [
    ("NODES (shape control -- a zero here means the transport, not the graph)",
     "MATCH (n) RETURN count(n) AS nodes"),
    ("TRIGGERS (D1-AC5 / D12-AC4)",
     "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' RETURN count(e) AS triggers"),
    ("TRIGGERS targets from opal-data-bd",
     "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN b.node_id AS target ORDER BY target"),
]
cmds = ["echo '===== HEALTH ====='", "curl -sS -m 20 %s/health; echo" % endpoint]
for i, (label, q) in enumerate(queries):
    b64 = base64.b64encode(q.encode("utf-8")).decode("ascii")
    f = "/tmp/cgd1_q%d.cypher" % i
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
