#!/usr/bin/env bash
# MX-s-8 AC2 (the RUNNING bytes): for each of the 4 functions, the live zip (get-function Code.Location, sha256 ==
# CodeSha256) holds a mirror_conversion.py with BOTH fixes (Z-S3 string-dtype arm, Z-S25 exactly-empty -> None)
# and without the old bare guard.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
T="${TMPDIR:-/tmp}/mx_s8_ac2_$$"; mkdir -p "$T"; W=$(cygpath -m "$T" 2>/dev/null || echo "$T")
for f in blackdiamond etf eclipse orion; do
  timeout 60 "$AWS" lambda get-function --function-name "opal-assets-silver-$f" --output json > "$T/$f.json"
done
out=$(python - "$W" <<'PY' 2>&1 | tr -d '\r'
import base64, hashlib, io, json, sys, urllib.request, zipfile
t = sys.argv[1]; ok = 0
for f in ('blackdiamond', 'etf', 'eclipse', 'orion'):
    try:
        fn = json.load(open('%s/%s.json' % (t, f), encoding='utf-8'))
    except Exception:
        print('%s get-function FAILED' % f); continue
    cfg = fn['Configuration']
    body = urllib.request.urlopen(fn['Code']['Location'], timeout=60).read()
    sha = base64.b64encode(hashlib.sha256(body).digest()).decode() == cfg['CodeSha256']
    z = zipfile.ZipFile(io.BytesIO(body))
    src = ''.join(z.read(n).decode('utf-8', 'replace') for n in z.namelist() if n.split('/')[-1] == 'mirror_conversion.py')
    new = 'pd.api.types.is_string_dtype(df[c].dtype)' in src and 'if v == "":' in src
    old = 'float64" and df[c].dtype == object' in src
    good = sha and new and not old
    ok += good
    print('%s LastModified=%s sha==CodeSha256=%s both-fixes=%s old-guard=%s' % (f, cfg['LastModified'], sha, new, old))
print('functions carrying the fix %d of 4' % ok)
PY
)
rm -rf "$T"
printf '%s\n' "$out"
if printf '%s\n' "$out" | tail -1 | grep -qx 'functions carrying the fix 4 of 4'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
