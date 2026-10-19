#!/usr/bin/env bash
# host_refused.sh <census.json> <out.json>: run host_refused.py ON the gateway host over SSM (read-only, under the OG-ap-38 guard) and write the per-tier decisions to <out.json>.
# Same transport as round22/host_breakdown.sh: the programs and the tool list travel inline (base64), run under the host's own venv, nothing is written on the host.
CENSUS="${1:?usage: host_refused.sh <census.json> <out.json>}"
OUT="${2:?usage: host_refused.sh <census.json> <out.json>}"
H="$(cd "$(dirname "$0")" && pwd)"
_R="$(git rev-parse --show-toplevel 2>/dev/null)"; cd "$_R" || exit 9
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_rf_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/host_refused.py")" "$(native "$H/../round22/ap38_guard.py")" "$(native "$CENSUS")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
census = json.load(open(sys.argv[4], encoding="utf-8"))
tools = {"tools": [{"tool": t, "channel": ch["id"]} for ch in census["channels"] for t in ch["tools"]]}
tb = base64.b64encode(json.dumps(tools).encode("utf-8")).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/host_refused.py; chmod 644 /tmp/host_refused.py; '
       'echo ' + b(sys.argv[3]) + ' | base64 -d > /tmp/ap38_guard.py; chmod 644 /tmp/ap38_guard.py; '
       'echo ' + tb + ' | base64 -d > /tmp/rf_tools.json; chmod 644 /tmp/rf_tools.json; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/ap38_guard.py 150 /tmp/host_refused.py /opt/opal-gateway /tmp/rf_tools.json 2>&1; echo "RC=${PIPESTATUS[0]}"; '
       'rm -f /tmp/host_refused.py /tmp/ap38_guard.py /tmp/rf_tools.json')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 120 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 60); do st=$(timeout 60 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); case "$st" in Success|Failed|TimedOut|Cancelled) break;; esac; sleep 4; done
timeout 60 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r' > "$T/out.txt"
python - "$T/out.txt" "$OUT" <<'PYEOF'
import base64, gzip, json, sys
lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
print("\n".join(l for l in lines if l.startswith(("health=", "RC=", "TIERS_BYTES", "Traceback", "AP38")) or "Error" in l)[:600])
if "TIERS_B64GZ" not in lines:
    print("RESULT: FAIL (no marker)"); print("\n".join(lines[-12:])[:900]); sys.exit(1)
b64 = lines[lines.index("TIERS_B64GZ") + 1]
body = json.loads(gzip.decompress(base64.b64decode(b64)).decode("utf-8"))
json.dump(body, open(sys.argv[2], "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=False)
print("tools=%d" % len(body.get("tools", [])))
print("RESULT: PASS")
PYEOF
rc=$?
echo "ssm command=${cid:-NONE} status=${st:-NONE}"
rm -rf "$T"
exit $rc
