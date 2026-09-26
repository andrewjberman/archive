#!/usr/bin/env bash
# MX-s-3 AC1 (the RUNNING bytes, not the self-report): the live opal-assets-silver-etf zip, downloaded from
# get-function's Code.Location and sha256-checked against the function's own CodeSha256, holds an etf_conversion.py
# with at least 1 occurrence of _convert_trueshares_holdings, and its LastModified is after this order's issue.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
T="${TMPDIR:-/tmp}/mx_s3_ac1_$$"; mkdir -p "$T"
timeout 60 "$AWS" lambda get-function --function-name opal-assets-silver-etf --output json > "$T/fn.json" 2>/dev/null
out=$(python - "$T" <<'EOF' 2>&1 | tr -d '\r'
import base64, hashlib, io, json, sys, urllib.request, zipfile
t = sys.argv[1]
try:
    fn = json.load(open(t + '/fn.json', encoding='utf-8'))
except Exception:
    print('get-function FAILED'); raise SystemExit(0)
cfg = fn['Configuration']
body = urllib.request.urlopen(fn['Code']['Location'], timeout=60).read()
sha_ok = base64.b64encode(hashlib.sha256(body).digest()).decode() == cfg['CodeSha256']
z = zipfile.ZipFile(io.BytesIO(body))
names = [n for n in z.namelist() if n.split('/')[-1] == 'etf_conversion.py']
hits = sum(z.read(n).decode('utf-8', 'replace').count('_convert_trueshares_holdings') for n in names)
after = cfg['LastModified'] > '2026-09-26T03:40'
print('LastModified=%s after-issue=%s zip-sha==CodeSha256=%s etf_conversion.py files=%d converter occurrences=%d'
      % (cfg['LastModified'], 'yes' if after else 'no', 'yes' if sha_ok else 'no', len(names), hits))
print('OK' if (sha_ok and after and names and hits >= 1) else 'NOT-OK')
EOF
)
rm -rf "$T"
printf '%s\n' "$out" | head -1
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
