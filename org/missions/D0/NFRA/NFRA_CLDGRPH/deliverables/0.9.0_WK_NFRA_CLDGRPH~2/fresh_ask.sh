#!/bin/bash
# NFRA_CLDGRPH CG-x-5 / TO-CG-D-6 -- FWD-5 EXERCISED.
# A machine that has never held the graph proves the LOCAL DB IS ABSENT, then asks ONCE and
# is answered by the SERVED projection on the first try, then proves the DB IS STILL ABSENT
# (a reader did not become a builder). Written by 0.9.0_WK_NFRA_CLDGRPH~2.
# It creates nothing under infra/aws/globgrph/ and runs no engine: the only ask is the thin
# client .tools/comp-kuzu, whose transport is the gateway's /graph/cypher route.
set -u

WS="$(git rev-parse --show-toplevel)"
cd "$WS" || exit 9
TMPD="$WS/.scratch/wk2"
mkdir -p "$TMPD"

DB="infra/aws/globgrph/kuzu_nessie_db"

db_state() {
  if [ -e "$DB" ]; then echo present; else echo absent; fi
}
db_census() {
  ls infra/aws/globgrph/ | grep -c kuzu_nessie_db
}

CYPHER="MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t"

echo "TS_START=$(date -u +%FT%TZ)"
echo "HOSTNAME=$(hostname)"
echo "MACHINE=worktree $WS"
echo "QUESTION=How many CloudNodes of each node_type does the estate hold?"
echo "CYPHER=$CYPHER"
echo "DB_NAME_CENSUS_BEFORE=$(db_census)"
echo "LOCAL_DB_BEFORE=$(db_state)"

echo "--- ASK 1: comp-kuzu --json (THE FIRST TRY) ---"
timeout 120 bash "$WS/.tools/comp-kuzu" --json "$CYPHER" > "$TMPD/ask1.out" 2> "$TMPD/ask1.err"
RC1=$?
echo "FIRST_TRY_RC=$RC1"
echo "--- ASK 1 stdout (the comparison object) ---"
cat "$TMPD/ask1.out"
echo "--- ASK 1 stderr (the disclosure) ---"
cat "$TMPD/ask1.err"

echo "--- ASK 2: comp-kuzu table mode (same statement) ---"
timeout 120 bash "$WS/.tools/comp-kuzu" "$CYPHER" > "$TMPD/ask2.out" 2> "$TMPD/ask2.err"
RC2=$?
echo "TABLE_RC=$RC2"
cat "$TMPD/ask2.out"
echo "--- ASK 2 stderr (the disclosure) ---"
cat "$TMPD/ask2.err"

echo "DB_NAME_CENSUS_AFTER=$(db_census)"
echo "LOCAL_DB_AFTER=$(db_state)"
echo "TS_END=$(date -u +%FT%TZ)"
exit $RC1
