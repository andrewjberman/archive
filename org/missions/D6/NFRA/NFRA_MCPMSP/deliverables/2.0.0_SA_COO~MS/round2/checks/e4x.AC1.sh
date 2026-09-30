#!/usr/bin/env bash
# MS-rx-1 AC1 (reconstructed from the record ALONE): deliverables/0.9.0_WK_NFRA_MCPMSP~8/r2_e4x_replay.md has the four
# sections "## Asked", "## Looked up", "## Allowed and refused", "## Answered", each non-empty, and cites the record's
# three object keys; and its "## Asked" section contains the first user turn of the record's transcript.jsonl verbatim
# (read from S3 at the address in MS-rn-1's run file) -- the replay is the record's, not a recollection.
. "$(dirname "$0")/_root.sh"
F="$R2/0.9.0_WK_NFRA_MCPMSP~8/r2_e4x_replay.md"; RUN="$R2/0.9.0_WK_NFRA_MCPMSP~6/r2_e4r_run.json"
for f in "$F" "$RUN"; do [ -f "$f" ] || { echo "$f absent"; echo "RESULT: FAIL"; exit 1; }; done
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_e4x.XXXXXX")"
base=$(python -c "
import json,sys;sys.path.insert(0,'.');import lib.opal_naming as n
r=json.load(open(sys.argv[1],encoding='utf-8'))
print(n.address('gateway', r['firm'], 'bronze', 'msp_runs', r['date']) + '/' + r['run_id'])
" "$RUN" 2>&1 | tr -d '\r' | tail -1)
timeout 60 "$AWS" s3 cp "$base/transcript.jsonl" "$(native "$T/t.jsonl")" >/dev/null 2>&1
res=$(python - "$F" "$T/t.jsonl" <<'EOF' 2>&1 | tr -d '\r'
import json, re, sys
md = open(sys.argv[1], encoding='utf-8').read()
secs = {}
for name in ('Asked', 'Looked up', 'Allowed and refused', 'Answered'):
    m = re.search(r'^## %s\s*\n(.*?)(?=^## |\Z)' % re.escape(name), md, re.S | re.M)
    secs[name] = (m.group(1).strip() if m else '')
cites = sum(1 for o in ('transcript.jsonl', 'audit.jsonl', 'manifest.json') if o in md)
first = ''
try:
    for l in open(sys.argv[2], encoding='utf-8'):
        d = json.loads(l)
        if d.get('type') == 'user' or (d.get('message') or {}).get('role') == 'user':
            c = (d.get('message') or {}).get('content')
            first = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in (c or []) if isinstance(x, dict))
            break
except Exception:
    pass
asked_ok = bool(first.strip()) and first.strip()[:200] in secs['Asked']
ok = all(secs.values()) and cites == 3 and asked_ok
print('sections_nonempty=%d/4 object_cites=%d/3 asked_matches_record=%s verdict=%s' % (sum(1 for v in secs.values() if v), cites, asked_ok, 'OK' if ok else 'NO'))
EOF
)
rm -rf "$T"
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
