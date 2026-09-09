#!/bin/bash
# D8-AC4 -- IS THERE A LOCAL GRAPH DATABASE ON THE SECOND MACHINE?
#
# The second machine is the gateway EC2 host i-07dccb1615503ac99 (the issuer's substitution for
# site Z, stated in the face and graded at D8-AC5). This is a READ: `hostname`, `find`, `wc`.
# Nothing is written on that host by this script.
#
# WHY THE PAYLOAD IS BUILT BY PYTHON AND NOT BY THE SHELL. The command this criterion needs
# contains a bare `/` argument, and MSYS/Git-Bash rewrites a lone `/` in argv into the Git
# installation root -- so `find / -xdev` typed as a shell argument would silently search
# C:/Program Files/Git and return a confident zero about the WRONG filesystem. Handing the
# payload to the CLI as `--cli-input-json file://...` keeps the path out of argv entirely.
#
# THREE READINGS, BECAUSE ONE ZERO CANNOT CARRY THIS CLAIM.
#   GATEWAY_LOCAL_DB_COUNT   -- the criterion's own arm: any `kuzu_nessie_db*` on the root
#                               filesystem to depth 6. `2>/dev/null` there discards permission
#                               noise on a find whose COUNT is the verdict (the face says so);
#                               the count itself is printed and never suppressed.
#   GATEWAY_FIND_DENOMINATOR -- how many paths that same find actually walked. A zero over a
#                               denominator of zero is a DEAD FIND (wrong root, no permission,
#                               no such host), not an absence, and the two read identically.
#   GATEWAY_PROBE_CONTROL    -- the SAME verb, the SAME root, the SAME depth, on a name that IS
#                               present on any Linux host (`hosts`). It must return non-zero.
# AND ONE UNSCOPED READING, because a check scoped to the name the cell retires cannot see a
# local graph under a different name:
#   GATEWAY_ANY_KUZU_COUNT   -- any path matching `*kuzu*` at all. Reported, not graded.
#
# Exit: 0 = the arm printed and every control behaved; 1 = a control was dead or the invocation
# failed; 2 = BLOCKED (no command id, or the poll never reached a terminal status).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

INSTANCE="i-07dccb1615503ac99"
TMP="$(mktemp -d)"
PAYLOAD="$TMP/ssm_payload.json"

python - "$PAYLOAD" "$INSTANCE" <<'PY'
import json
import sys

payload_path, instance = sys.argv[1], sys.argv[2]
commands = [
    "echo GATEWAY_HOST=$(hostname)",
    "echo GATEWAY_UTC=$(date -u +%FT%TZ)",
    "echo GATEWAY_FIND_DENOMINATOR=$(find / -xdev -maxdepth 6 2>/dev/null | wc -l)",
    "echo GATEWAY_LOCAL_DB_COUNT=$(find / -xdev -maxdepth 6 -name 'kuzu_nessie_db*' 2>/dev/null | wc -l)",
    "echo GATEWAY_ANY_KUZU_COUNT=$(find / -xdev -maxdepth 6 -name '*kuzu*' 2>/dev/null | wc -l)",
    "echo GATEWAY_PROBE_CONTROL=$(find / -xdev -maxdepth 6 -name 'hosts' 2>/dev/null | wc -l)",
]
json.dump({
    "InstanceIds": [instance],
    "DocumentName": "AWS-RunShellScript",
    "Comment": "NFRA_CLDGRPH TO-CG-D-8 D8-AC4 local-DB absence read (READ only)",
    "Parameters": {"commands": commands},
}, open(payload_path, "w"), indent=2)
PY

CID="$(timeout 60 .tools/aws ssm send-command --cli-input-json "file://$PAYLOAD" \
        --query 'Command.CommandId' --output text | tr -d '\r')"
if [ -z "$CID" ] || [ "$CID" = "None" ]; then
  echo "BLOCKED: ssm send-command returned no CommandId -- nothing was measured on the second machine"
  exit 2
fi
echo "SSM_COMMAND_ID=$CID"
echo "SSM_INSTANCE=$INSTANCE"

STATUS="Pending"
for _ in $(seq 1 12); do
  sleep 5
  STATUS="$(timeout 60 .tools/aws ssm get-command-invocation --command-id "$CID" \
            --instance-id "$INSTANCE" --query 'Status' --output text 2>/dev/null | tr -d '\r')"
  case "$STATUS" in Success|Failed|Cancelled|TimedOut) break ;; esac
done
echo "SSM_STATUS=$STATUS"
if [ "$STATUS" != "Success" ]; then
  echo "BLOCKED: the SSM invocation did not reach Success (status=$STATUS); no absence is claimed"
  exit 2
fi

OUT="$(timeout 60 .tools/aws ssm get-command-invocation --command-id "$CID" \
       --instance-id "$INSTANCE" --query 'StandardOutputContent' --output text | tr -d '\r')"
echo "--- StandardOutputContent (verbatim, from the second machine) ---"
echo "$OUT"
echo "--- end ---"

DENOM="$(echo "$OUT"  | grep '^GATEWAY_FIND_DENOMINATOR=' | cut -d= -f2)"
CONTROL="$(echo "$OUT" | grep '^GATEWAY_PROBE_CONTROL='   | cut -d= -f2)"
COUNT="$(echo "$OUT"   | grep '^GATEWAY_LOCAL_DB_COUNT='  | cut -d= -f2)"

if [ -z "${COUNT:-}" ]; then
  echo "BLOCKED: the second machine returned no GATEWAY_LOCAL_DB_COUNT line"
  exit 2
fi
if [ "${DENOM:-0}" -le 0 ]; then
  echo "GATEWAY_FIND_DEAD -- the find walked $DENOM path(s); a zero over an empty walk is a dead"
  echo "  instrument, not an absence"
  exit 1
fi
if [ "${CONTROL:-0}" -le 0 ]; then
  echo "GATEWAY_PROBE_CONTROL=DEAD -- the same verb on the same root found 0 'hosts'; the zero"
  echo "  above measures a broken find, not a clean host"
  exit 1
fi

echo "GATEWAY_PROBE_CONTROL_VERDICT=FIRED -- the same find verb, same root, same depth, returned"
echo "  $CONTROL hit(s) for a name that IS present, over a walk of $DENOM path(s), so the arm's"
echo "  zero is an absence and not a dead instrument"
exit 0
