#!/usr/bin/env bash
# MS-a-2 AC2 (the DEPLOYED bytes, resolved by content, never by name): the lambda_function.py inside the package the
# live function name('mcportal',None,'grant-writer','lambda') serves carries register_tenant AND is byte-identical to
# HEAD's infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/lambda_function.py.
. "$(dirname "$0")/_root.sh"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/ms_a2_ac2_$$"; mkdir -p "$T"
url=$(timeout 30 "$AWS" lambda get-function --function-name "$nm" --query Code.Location --output text 2>&1 | tr -d '\r' | tail -1)
git show "HEAD:$MPW_DIR/lambda_function.py" > "$T/head.py" 2>/dev/null
res=$(python - "$url" "$T/head.py" <<'EOF' 2>&1 | tr -d '\r'
import hashlib, io, sys, urllib.request, zipfile
url, head = sys.argv[1], sys.argv[2]
try:
    blob = urllib.request.urlopen(url, timeout=60).read()
    z = zipfile.ZipFile(io.BytesIO(blob))
    live = z.read('lambda_function.py')
except Exception as exc:
    print('download/unzip failed: %s verdict=NO' % type(exc).__name__); sys.exit(0)
h = open(head, 'rb').read()
same = hashlib.sha256(live).hexdigest() == hashlib.sha256(h).hexdigest()
has = b'register_tenant' in live
print('live sha256=%s head sha256=%s identical=%s register_tenant=%s verdict=%s' % (
    hashlib.sha256(live).hexdigest()[:12], hashlib.sha256(h).hexdigest()[:12], same, has, 'OK' if (same and has) else 'NO'))
EOF
)
rm -rf "$T"
echo "function $nm: $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
