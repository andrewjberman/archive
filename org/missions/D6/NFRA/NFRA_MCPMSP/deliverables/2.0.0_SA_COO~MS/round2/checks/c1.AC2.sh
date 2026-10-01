#!/usr/bin/env bash
# MS-c-1 AC2 (the DELTA baseline, with its control): deliverables/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json
# lists >= 6 firm-scoped opal-data-portal-v2 keys (each {key, sha256, bytes, captured_at}), covering >= 2 firms; and for
# the first two keys the sha256 of the object as it reads NOW from S3 equals the recorded one (the baseline is the
# served bytes, not a guess).
. "$(dirname "$0")/_root.sh"
F="$R2/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_c1_ac2.XXXXXX")"
keys=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print('\n'.join(k['key'] for k in (d.get('keys') or [])[:2]))" "$F" 2>/dev/null | tr -d '\r')
i=0; for k in $keys; do i=$((i+1)); timeout 60 "$AWS" s3api get-object --bucket opal-data-portal-v2 --key "$k" "$(native "$T/o$i")" >/dev/null 2>&1; done
res=$(python - "$F" "$T" <<'EOF' 2>&1 | tr -d '\r'
import hashlib, json, os, re, sys
d = json.load(open(sys.argv[1], encoding='utf-8')); ks = d.get('keys') or []
shape = all({'key','sha256','bytes','captured_at'} <= set(k) for k in ks)
firms = {m.group(1) for k in ks for m in [re.search(r'/(49financial|inflection|cottonwood)/', k.get('key',''))] if m}
match = 0
for i, k in enumerate(ks[:2], 1):
    p = os.path.join(sys.argv[2], 'o%d' % i)
    if os.path.exists(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == k.get('sha256'):
        match += 1
ok = shape and len(ks) >= 6 and len(firms) >= 2 and match == 2
print('keys=%d firms=%s shape=%s live_sha_match=%d/2 verdict=%s' % (len(ks), sorted(firms), shape, match, 'OK' if ok else 'NO'))
EOF
)
rm -rf "$T"
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
