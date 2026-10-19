#!/usr/bin/env bash
# host_breakdown.sh <out.json>: run host_breakdown.py ON the gateway host over SSM (read-only) and write the served breakdown body to <out.json>.
# Same transport as round18/discover_buckets_host.sh: the program travels inline (base64), runs under the host's own venv, writes nothing on the host.
OUT="${1:?usage: host_breakdown.sh <out.json>}"
H="$(cd "$(dirname "$0")" && pwd)"
_R="$(git rev-parse --show-toplevel 2>/dev/null)"; cd "$_R" || exit 9
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_bd_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/host_breakdown.py")" "$(native "$H/ap38_guard.py")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/host_breakdown.py; chmod 644 /tmp/host_breakdown.py; '
       'echo ' + b(sys.argv[3]) + ' | base64 -d > /tmp/ap38_guard.py; chmod 644 /tmp/ap38_guard.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/ap38_guard.py 150 /tmp/host_breakdown.py /opt/opal-gateway 2>&1; echo "RC=${PIPESTATUS[0]}"; '
       'rm -f /tmp/host_breakdown.py /tmp/ap38_guard.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 120 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 60); do st=$(timeout 60 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); case "$st" in Success|Failed|TimedOut|Cancelled) break;; esac; sleep 4; done
timeout 60 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r' > "$T/out.txt"
python - "$T/out.txt" "$OUT" <<'PYEOF'
import base64, gzip, json, sys
lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
print("\n".join(l for l in lines if l.startswith(("health=", "RC=", "BREAKDOWN_BYTES", "INTEGRATIONS_", "Traceback")) or "Error" in l)[:600])
if "BREAKDOWN_B64GZ" not in lines:
    print("RESULT: FAIL (no marker)"); sys.exit(1)
b64 = lines[lines.index("BREAKDOWN_B64GZ") + 1]
body = json.loads(gzip.decompress(base64.b64decode(b64)).decode("utf-8"))
json.dump(body, open(sys.argv[2], "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=False)
print("channels=%d read_at=%s" % (len(body.get("channels", [])), body.get("read_at")))
print("RESULT: PASS")
PYEOF
rc=$?
echo "ssm command=${cid:-NONE} status=${st:-NONE}"
rm -rf "$T"
exit $rc
