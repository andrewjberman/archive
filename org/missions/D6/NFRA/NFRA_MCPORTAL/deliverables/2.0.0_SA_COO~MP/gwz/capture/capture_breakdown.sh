#!/usr/bin/env bash
# capture_breakdown.sh -- ONE served capture of the /gateway breakdown at the live gateway release (CVO ADJUDICATION_v15.Z, row Z-C-S66; "host-side, as OG-ap-50 did").
# Read-only: SSM RunShellScript on the gateway host runs _host_probe.py with the host's venv (the handler's own _compute; no write anywhere).
# Usage: capture_breakdown.sh <out.json>. Prints status and the capture's sizes; the file holds the scrubbed capture plus the live release it was taken at.
. "$(dirname "$0")/../../pc/checks/_root.sh"
OUT="${1:?usage: capture_breakdown.sh <out.json>}"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
dc=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
python - "$(dirname "$0")/_host_probe.py" "$T/params.json" <<'PY'
import json, sys
src = open(sys.argv[1], encoding="utf-8").read()
cmd = "cd /opt/opal-gateway && ./.venv/bin/python - <<'EOF'\n" + src + "\nEOF"
json.dump({"commands": [cmd], "executionTimeout": ["110"]}, open(sys.argv[2], "w"))
PY
ssm_run "$T/params.json"
line=$(printf '%s\n' "$SSM_OUT" | grep '^CAPTURE=' | tail -1)
echo "ssm status=$SSM_ST cmd=$SSM_CID manifest deployed_commit=${dc:0:10} out_bytes=${#SSM_OUT} capture_line=$([ -n "$line" ] && echo yes || echo no)"
[ -n "$line" ] || { printf '%s\n' "$SSM_OUT" | tail -5 | cut -c1-300; echo "RESULT: FAIL"; exit 1; }
python - "$OUT" "$dc" "${line#CAPTURE=}" <<'PY'
import json, sys
cap = json.loads(sys.argv[3])
json.dump({"taken_for": "CVO ADJUDICATION_v15.Z row Z-C-S66 (MP-z-6 AC2 re-grade input)", "manifest_deployed_commit": sys.argv[2], "capture": cap},
          open(sys.argv[1], "w", encoding="ascii"), indent=1, sort_keys=True)
t = cap["totals"]
print("capture: gateway_read_at=%s catalog_md5_12=%s channels=%d segmented=%d totals=%s" % (cap["gateway_read_at"], cap["catalog_md5_12"], len(cap["channels"]),
      sum(1 for c in cap["channels"] if c["segmented"]), json.dumps(t)))
PY
echo "RESULT: PASS"
