#!/bin/bash
# D8-AC1 + D8-AC2 -- TWO MACHINES, ONE QUESTION, INSIDE ONE MINUTE.
#
# MACHINE A: this laptop worktree, through `.tools/comp-kuzu --json` -- the thin client, which
#            POSTs one statement to https://mcp.opalinvest.dev/graph/cypher with a Secrets-Manager
#            bearer and prints its VINTAGE line on stderr. No local database.
# MACHINE B: the gateway EC2 host i-07dccb1615503ac99, by SSM, curling the service DIRECTLY at
#            http://projection.opal-globgrph.local:8181/cypher inside the VPC (the exact CG-s-4
#            shape). A machine with no repository and no local graph.
#
# THE TWO PATHS ARE DIFFERENT ON PURPOSE AND THAT IS THE STRENGTH OF THE ARM, not a defect: a
# public HTTPS gateway with a bearer versus an in-VPC plaintext HTTP call to the Cloud Map name.
# Two machines, two transports, ONE served artifact. If both answers agree AND carry the same
# vintage, they cannot be two copies of a graph -- they are one pointer read twice.
#
# THE ORDER OF OPERATIONS IS THE MEASUREMENT. T0 is taken, the SSM send-command is fired (it
# returns as soon as AWS accepts it; the host runs the curl within a second or two), the laptop
# ask runs immediately, and T1 is taken when the laptop answer is in hand. WINDOW_S = T1 - T0 on
# ONE clock -- the laptop's -- so the window never depends on clock agreement between the two
# machines. The gateway's own ExecutionStartDateTime (AWS's clock) is printed beside it and the
# skew is stated rather than assumed away.
#
# WHY PYTHON WRITES THE SSM PAYLOAD: the CLI argv route would hand MSYS/Git-Bash a shell string
# to mangle, and `--cli-input-json file://...` keeps the Cypher and the URL out of argv entirely.
#
# WHAT "EQUAL" MEANS HERE: the two `rows` arrays are compared as CANONICAL JSON (sorted keys,
# no whitespace), so key order and pretty-printing cannot make two identical answers look
# different, nor two different answers look the same. The row count is printed as the
# denominator -- an empty answer compared against another empty answer is EQUAL and vacuous, so
# a zero-row result is refused loudly instead of being scored as agreement.
#
# Exit: 0 = both answers in hand and compared; 1 = the answers disagree, or one is empty;
#       2 = BLOCKED (no command id, no terminal SSM status, or a machine returned nothing).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

INSTANCE="i-07dccb1615503ac99"
CYPHER="MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t"
TMP="$(mktemp -d)"
PAYLOAD="$TMP/ask.json"

python - "$PAYLOAD" "$INSTANCE" "$CYPHER" <<'PY'
import json
import sys

payload_path, instance, cypher = sys.argv[1], sys.argv[2], sys.argv[3]
curl = ("curl -s -X POST -H 'Content-Type: text/plain' --data-binary '%s' "
        "http://projection.opal-globgrph.local:8181/cypher" % cypher)
json.dump({
    "InstanceIds": [instance],
    "DocumentName": "AWS-RunShellScript",
    "Comment": "NFRA_CLDGRPH TO-CG-D-8 D8-AC1/AC2 paired ask (READ only)",
    "Parameters": {"commands": ["echo GATEWAY_UTC=$(date -u +%FT%T.%NZ)", curl]},
}, open(payload_path, "w"), indent=2)
PY

echo "QUESTION=$CYPHER"

# ---- T0, then BOTH asks, then T1 -----------------------------------------------------------
T0="$(python -c 'import time; print(repr(time.time()))')"
T0_UTC="$(date -u +%FT%T.%NZ)"

CID="$(timeout 60 .tools/aws ssm send-command --cli-input-json "file://$PAYLOAD" \
        --query 'Command.CommandId' --output text | tr -d '\r')"
if [ -z "$CID" ] || [ "$CID" = "None" ]; then
  echo "BLOCKED: ssm send-command returned no CommandId -- the second machine was never asked"
  exit 2
fi

timeout 90 bash .tools/comp-kuzu --json "$CYPHER" > "$TMP/laptop.json" 2> "$TMP/laptop.err"
LAPTOP_RC=$?

T1="$(python -c 'import time; print(repr(time.time()))')"
T1_UTC="$(date -u +%FT%T.%NZ)"

echo "SSM_COMMAND_ID=$CID"
echo "T0_LAPTOP_UTC=$T0_UTC"
echo "T1_LAPTOP_UTC=$T1_UTC"
echo "LAPTOP_CLIENT_RC=$LAPTOP_RC"

# ---- collect the gateway answer ------------------------------------------------------------
STATUS="Pending"
for _ in $(seq 1 12); do
  sleep 5
  STATUS="$(timeout 60 .tools/aws ssm get-command-invocation --command-id "$CID" \
            --instance-id "$INSTANCE" --query 'Status' --output text 2>/dev/null | tr -d '\r')"
  case "$STATUS" in Success|Failed|Cancelled|TimedOut) break ;; esac
done
echo "SSM_STATUS=$STATUS"
if [ "$STATUS" != "Success" ]; then
  echo "BLOCKED: the SSM invocation did not reach Success (status=$STATUS); no agreement is claimed"
  exit 2
fi

timeout 60 .tools/aws ssm get-command-invocation --command-id "$CID" --instance-id "$INSTANCE" \
  --query 'StandardOutputContent' --output text | tr -d '\r' > "$TMP/gateway.raw"
EXEC_START="$(timeout 60 .tools/aws ssm get-command-invocation --command-id "$CID" \
              --instance-id "$INSTANCE" --query 'ExecutionStartDateTime' --output text | tr -d '\r')"
echo "GATEWAY_EXEC_START_AWSCLOCK=$EXEC_START"

echo "--- laptop stderr (its own VINTAGE line, verbatim) ---"
cat "$TMP/laptop.err"
echo "--- gateway StandardOutputContent (verbatim, from the second machine) ---"
cat "$TMP/gateway.raw"
echo "--- end ---"

# ---- compare -------------------------------------------------------------------------------
python - "$TMP/laptop.json" "$TMP/laptop.err" "$TMP/gateway.raw" "$T0" "$T1" "$EXEC_START" <<'PY'
import json
import re
import sys
from datetime import datetime, timezone

lap_rows_p, lap_err_p, gw_raw_p, t0, t1, exec_start = sys.argv[1:7]

laptop_rows = json.load(open(lap_rows_p, encoding="utf-8"))
lap_err = open(lap_err_p, encoding="utf-8", errors="replace").read()
m = re.search(r"vintage=([^\s\]]+)", lap_err)
laptop_vintage = m.group(1) if m else "UNREAD"

raw = open(gw_raw_p, encoding="utf-8", errors="replace").read()
gw_utc = None
gm = re.search(r"^GATEWAY_UTC=(\S+)", raw, re.M)
if gm:
    gw_utc = gm.group(1)
body = raw[raw.index("{"):] if "{" in raw else "{}"
gateway = json.loads(body)
gateway_rows = gateway.get("rows") or []
gateway_vintage = gateway.get("vintage") or "UNREAD"


def canon(rows):
    return json.dumps(rows, sort_keys=True, separators=(",", ":"))


equal = canon(laptop_rows) == canon(gateway_rows)
window = float(t1) - float(t0)

print("LAPTOP_ROW_COUNT=%d" % len(laptop_rows))
print("GATEWAY_ROW_COUNT=%d" % len(gateway_rows))
if not laptop_rows or not gateway_rows:
    print("ROWS_EQUAL=REFUSED-EMPTY -- one side returned 0 rows; two empty answers agree "
          "vacuously and that is not what this criterion asks")
    print("WINDOW_S=%.3f" % window)
    sys.exit(1)

print("LAPTOP_VINTAGE=%s" % laptop_vintage)
print("GATEWAY_VINTAGE=%s" % gateway_vintage)
print("VINTAGE_IDENTICAL=%s" % str(laptop_vintage == gateway_vintage).lower())
print("MANIFEST_SHA256_GATEWAY=%s" % (gateway.get("manifest_sha256") or "UNREAD"))
print("ARTIFACT_PREFIX_GATEWAY=%s" % (gateway.get("artifact_prefix") or "UNREAD"))
print("ROWS_EQUAL=%s" % str(equal).lower())
print("WINDOW_S=%.3f" % window)

# The window is one clock's. The gateway's own clock is reported beside it, never folded in.
try:
    es = datetime.strptime(exec_start, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    t0d = datetime.fromtimestamp(float(t0), tz=timezone.utc)
    t1d = datetime.fromtimestamp(float(t1), tz=timezone.utc)
    inside = t0d <= es <= t1d
    print("GATEWAY_EXEC_INSIDE_LAPTOP_WINDOW=%s  (AWS clock %s vs laptop window %s .. %s)"
          % (str(inside).lower(), es.isoformat(), t0d.isoformat(), t1d.isoformat()))
    print("CLOCK_SKEW_NOTE=the window above is measured on the LAPTOP clock alone (T1-T0), so it "
          "does not depend on the two machines agreeing; the AWS-clock line is reported beside "
          "it and, if the two clocks disagree, only that line moves.")
except Exception as exc:   # noqa: BLE001 -- an unparsed timestamp is reported, never swallowed
    print("GATEWAY_EXEC_INSIDE_LAPTOP_WINDOW=UNREAD (%s: %s)" % (type(exc).__name__, exc))

if gw_utc:
    print("GATEWAY_OWN_UTC_AT_ASK=%s" % gw_utc)
sys.exit(0 if equal else 1)
PY
