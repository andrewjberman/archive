#!/bin/bash
# TO NFRA_CLDGRPH.TO-CG-D-5 / decomp cell CG-x-1 / PRD FWD-1 acceptance 1.
# ONE wiring question, asked ONCE by a never-compiled seat through the SERVED client.
# Runs no engine, no refresh, no build: it shells `comp-kuzu` and nothing else.
# Print order is load-bearing: TIME_TO_ANSWER_S precedes the VINTAGE line (D5-AC2),
# and PROCS_BEFORE precedes PROCS_AFTER (D5-AC3).
set -u

WS="$(git rev-parse --show-toplevel)"
TMP="$WS/.scratch/wk3-d5"
mkdir -p "$TMP"

ASKER="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_CLDGRPH~3}"
QUESTION="Which Lambda functions does the bd data bucket trigger?"
ENGINE_PAT='kuzu_nessie_load|kuzu_incremental_refresh|derive_runner'

# The statement, built ONCE, in a double-quoted shell variable so the single quotes
# around the two string literals reach the client as SINGLE quotes. Row W1-S10: a
# predecessor's '\'' idiom delivered e.edge_type='"TRIGGERS"' -- valid, unmatchable,
# 0 rows at a correct vintage with no error. The statement is echoed below exactly
# as it is passed, and the same variable is what is passed.
CYPHER="MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN a.node_id AS bucket, b.node_id AS target ORDER BY target"

count_engine() { ps -ef | grep -E "$ENGINE_PAT" | grep -v grep | wc -l | tr -d ' '; }
count_bash()   { ps -ef | grep -E 'bash' | grep -v grep | wc -l | tr -d ' '; }

echo "ASKER=$ASKER"
echo "QUESTION=$QUESTION"
echo "CYPHER_AS_SENT=$CYPHER"
echo "CLIENT=bash .tools/comp-kuzu \"\$CYPHER\"   (one argv element, no shell re-quoting)"
echo "PROCS_PATTERN=$ENGINE_PAT"
echo "PROCS_TABLE_ROWS=$(ps -ef | wc -l | tr -d ' ')"
echo "PROCS_POSCTL_BASH=$(count_bash)"

echo "PROCS_BEFORE=$(count_engine)"

START="$(date +%s.%N)"
( cd "$WS" && bash .tools/comp-kuzu "$CYPHER" ) >"$TMP/out.txt" 2>"$TMP/err.txt" &
QPID=$!

# Sample the process table WHILE the ask is in flight. No sleep: the loop spins for
# exactly the query's lifetime, so the max is a live sample, not a post-hoc one.
DURING=0
while kill -0 "$QPID" 2>>"$TMP/killerr.txt"; do
  C="$(count_engine)"
  if [ "$C" -gt "$DURING" ]; then DURING="$C"; fi
done
wait "$QPID"
CLIENT_RC=$?
END="$(date +%s.%N)"

ELAPSED="$(awk -v s="$START" -v e="$END" 'BEGIN { printf "%.3f", e - s }')"
echo "TIME_TO_ANSWER_S=$ELAPSED"
echo "CLIENT_RC=$CLIENT_RC"

echo "--- ANSWER (client stdout) ---"
cat "$TMP/out.txt"
echo "--- CLIENT STDERR (carries the VINTAGE line) ---"
cat "$TMP/err.txt"
echo "--- end client output ---"

# The count is the CLIENT'S OWN "(N rows)" denominator, not a regex of mine over its
# table: run 1 of this script counted `^opal-data-bd` and printed a FALSE 0 beside a
# true 3-row answer, because every row begins `arn:aws:s3:::opal-data-bd`. A wrong
# arm and a dead arm read identically -- so the tool that produced the rows states it.
echo "ANSWER_ROW_COUNT=$(sed -n 's/^(\([0-9][0-9]*\) rows)$/\1/p' "$TMP/out.txt" | tr -d ' ')"
echo "PROCS_DURING_MAX=$DURING"
echo "PROCS_AFTER=$(count_engine)"
exit 0
