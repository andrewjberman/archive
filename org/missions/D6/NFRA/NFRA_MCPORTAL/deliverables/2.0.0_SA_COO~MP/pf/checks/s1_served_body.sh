#!/usr/bin/env bash
# S1 item (iii), the issuer's real run: read the SERVED breakdown body over SSM (read-only), redact every holders[].who, and write it as JSON for the real GatewayView to render.
# usage: s1_served_body.sh <out.json>   (the out path is Windows-style, e.g. C:/tmp/s1_body.json). Prints the denominator (channels, tools, segments) and the redaction count; never a raw holder.
. "$(dirname "$0")/../../pc/checks/_root.sh"
OUT="$1"; [ -n "$OUT" ] || { echo "usage: s1_served_body.sh <out.json>"; exit 2; }
T="${TMPDIR:-/tmp}/mp_s1body_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks/_s1_body_probe.py "$(cygpath -m "$T")/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 '^S1BODY ' || true)
echo "ssm command=$SSM_CID status=$SSM_ST; body line bytes=${#line}"
[ -n "$line" ] || { echo "no S1BODY line"; echo "RESULT: FAIL"; exit 1; }
printf '%s' "$line" | python -c "
import base64, gzip, json, sys
b = sys.stdin.read().strip()[len('S1BODY '):]
d = json.loads(gzip.decompress(base64.b64decode(b)).decode('utf-8'))
n = 0
for c in d.get('channels', []):
    for h in c.get('holders') or []:
        n += 1; h['who'] = 'person-%d (redacted)' % n
chs = d['channels']
segs = {c['id']: [(s['vendor'], s['firm'], len(s['tools'])) for s in c['segments']] for c in chs if c.get('segments')}
print('body: read_at=%s channels=%d tools_in_header=%s holders_redacted=%d segments=%s' % (d.get('read_at'), len(chs), sum(len(c['tools']) for c in chs), n, {k: len(v) for k, v in segs.items()}))
json.dump(d, open(sys.argv[1], 'w', encoding='utf-8'))
" "$OUT" && echo "RESULT: READ" || { echo "RESULT: FAIL"; exit 1; }
