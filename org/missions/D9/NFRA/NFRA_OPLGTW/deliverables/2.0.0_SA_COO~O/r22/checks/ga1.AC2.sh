#!/usr/bin/env bash
# OPLGTW OG-ga-1 AC2 (REAL C3 DOWNLOAD): GA1_DOWNLOAD.json records an on-host dim_asset prepare_download for the REAL
# holder read from the store (no synthetic principal, no in-memory grant) that returned held CUSIPs only; its body
# digest is found in the SSM invocation's own output, so the file is the host's answer and not a transcription.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/GA1_DOWNLOAD.json"
[ -f "$F" ] || { echo "GA1_DOWNLOAD.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r cid iid dig ok <<<"$(python - "$(native "$F")" <<'PY' | tr -d '\r'
import hashlib, json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body") or {}
h = b.get("held_check") or {}
ok = (b.get("synthetic_principal") is False and b.get("grant_source") == "store" and b.get("dim_asset_download") == "OK"
      and int(h.get("returned", 0)) >= 1 and int(h.get("unheld_returned", -1)) == 0 and b.get("grants_written") == 0)
print(d.get("ssm_command_id", "NONE"), d.get("instance_id", "NONE"),
      hashlib.sha256(json.dumps(b, sort_keys=True).encode("utf-8")).hexdigest(), "yes" if ok else "no")
PY
)"
out=$(bash .tools/aws ssm get-command-invocation --command-id "$cid" --instance-id "$iid" --region us-east-1 \
      --query '[Status,StandardOutputContent]' --output text 2>&1 | tr -d '\r')
st=$(printf '%s\n' "$out" | head -1 | awk '{print $1}')
found=no; printf '%s\n' "$out" | grep -q "GA1_DIGEST $dig" && found=yes
echo "body fields held-only real-holder download: $ok; ssm status ${st:-NONE}; digest in host output: $found"
[ "$ok" = yes ] && [ "$st" = Success ] && [ "$found" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
