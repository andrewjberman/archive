#!/usr/bin/env bash
# graph_query.sh -- NFRA_CLDGRPH TO-CG-D-2 (D2-AC3), THE EXERCISE FROM A NON-GATEWAY SEAT.
#
# This laptop seat is NOT the gateway host and is NOT inside vpc-0cc0c6a75e54605e3, so it cannot
# reach http://projection.opal-globgrph.local:8181 at all. It holds AWS credentials, reads the
# STATIC capability bearer from Secrets Manager with them, and asks the PUBLIC gateway over HTTPS:
#
#   POST https://mcp.opalinvest.dev/graph/cypher   (Authorization: Bearer <capability>)
#   body: one Cypher statement as text/plain
#
# A pass prints the projection service's OWN answer verbatim -- rows plus the vintage / age_line /
# manifest_sha256 / artifact_prefix the SERVICE stamped, never a vintage this script invented.
#
# The bearer is read into a shell variable and NEVER echoed, never written to a file, never put in
# a commit. Bounded: curl -m 20. ASCII only.
set -uo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
AWS="${REPO_ROOT}/.tools/aws"
SECRET_ID="opal/mcp/graph-read-token"
URL="https://mcp.opalinvest.dev/graph/cypher"
STATEMENT="MATCH (n) RETURN count(n) AS nodes"

BEARER="$("$AWS" secretsmanager get-secret-value --secret-id "$SECRET_ID" \
  --region us-east-1 --query SecretString --output text)"
if [ -z "$BEARER" ]; then
  echo "BLOCKED: could not read the capability bearer from $SECRET_ID (no value)" >&2
  exit 4
fi

echo "SEAT: $(hostname) (NOT the gateway host i-07dccb1615503ac99, NOT in the VPC)"
echo "POST $URL"
echo "STATEMENT: $STATEMENT"
echo "--- response ---"
curl -sS -m 20 -X POST \
  --header "Authorization: Bearer ${BEARER}" \
  --header "Content-Type: text/plain" \
  --data "$STATEMENT" \
  --write-out '\nHTTP_STATUS:%{http_code}\n' \
  "$URL"
RC=$?
echo "curl rc=$RC"
exit $RC
