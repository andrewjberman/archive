#!/usr/bin/env bash
# OPLGTW OG-r-4 AC3 (FWD-7 re-measure, analysis round 12 s.5 item 5): CAPACITY_R4.json was measured against the SERVED
# release PINNED at the round-14 cut (4231bd2ddc, deployed_at 2026-10-02T19:23:40Z; OG-rl-4 moves the manifest later in the same round,
# so the grade never reads the moving manifest) -- its served_release equals that commit, engine_md5_equal is true, it ran on the host
# install, wrote nothing to the state store, used synthetic principals, and started after the manifest's deployed_at.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/CAPACITY_R4.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python -c "
import json,sys
s={'deployed_commit':'4231bd2ddc6fd975304ed5a2c097473bdd5b41a5','deployed_at':'2026-10-02T19:23:40Z'}
d=json.load(open(sys.argv[1],encoding='utf-8')); c=d.get('ctx',{})
chk={'served_release equals deployed_commit': d.get('served_release')==s['deployed_commit'],
     'engine_md5_equal': d.get('engine_md5_equal') is True,
     'ran_against_host_install': c.get('ran_against_host_install') is True,
     'state_store_written false': c.get('state_store_written') is False,
     'synthetic_principals': bool(c.get('synthetic_principals')),
     'started after deployed_at': str(d.get('started_utc',''))>=s['deployed_at']}
for k,v in chk.items(): print('%s: %s'%(k,v))
ok=all(chk.values()); print('RESULT: PASS' if ok else 'RESULT: FAIL'); sys.exit(0 if ok else 1)
" "$(native "$F")"
