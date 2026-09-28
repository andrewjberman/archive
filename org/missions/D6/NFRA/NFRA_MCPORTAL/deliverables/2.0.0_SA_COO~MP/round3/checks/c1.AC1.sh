#!/usr/bin/env bash
# MP-c-1 AC1 (A1, FWD-1 LIVE, the two writes): inside the close run's window, the writer's own table
# mcportal-grant-changes-table holds, for the ONE colleague named by hash in c1_run.json, a WRITTEN `narrow` followed by
# a WRITTEN `widen`, each carrying `before` and `after`. The colleague is matched by sha256("<tid>/<oid>") so no
# identifier is printed or committed. c1_run.json = {"t0","t1","principal_sha256","raw_dir"}, written by the issuer
# before the spawn.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
RUN="${MP_C1_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~1/c1_run.json}"
tb=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-changes', 'table'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_c1_ac1_$$"; mkdir -p "$T"
timeout 90 "$AWS" dynamodb scan --table-name "$tb" --output json > "$T/scan.json" 2>"$T/err.txt"; rc=$?
res=$(python - "$T/scan.json" "$RUN" "$rc" <<'EOF' 2>&1 | tr -d '\r'
import hashlib, json, sys
try:
    run = json.load(open(sys.argv[2], encoding='utf-8'))
except Exception as e:
    print('no run file: %s' % e); sys.exit(0)
if sys.argv[3] != '0':
    print('scan rc=%s' % sys.argv[3]); sys.exit(0)
items = json.load(open(sys.argv[1], encoding='utf-8')).get('Items', [])
S = lambda it, k: (it.get(k) or {}).get('S', '')
mine = []
for it in items:
    h = hashlib.sha256(('%s/%s' % (S(it, 'tid'), S(it, 'oid'))).encode()).hexdigest()
    if h == run['principal_sha256'] and run['t0'] <= S(it, 'when') <= run['t1'] and S(it, 'verdict') == 'WRITTEN':
        mine.append((S(it, 'when'), S(it, 'action'), bool(S(it, 'before')) and bool(S(it, 'after'))))
mine.sort()
acts = [a for _, a, _ in mine]; full = all(f for _, _, f in mine)
ok = 'narrow' in acts and 'widen' in acts[acts.index('narrow') + 1:] and full if 'narrow' in acts else False
print('table items scanned=%d; colleague WRITTEN in window=%d; sequence=%s; before+after on all=%s; verdict=%s'
      % (len(items), len(mine), ','.join(acts) or 'none', full, 'OK' if ok else 'NO'))
EOF
)
rm -rf "$T"
echo "table $tb: $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
