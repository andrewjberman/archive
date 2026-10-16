#!/usr/bin/env bash
# MP-pf-4 SERVED ARM (CTO round-2 analysis, cell S1 items ii; the ISSUER runs it at close, never a worker, and only once OG-ap-23 reads deployed). PASS needs ALL of:
#   1. EC2_MANIFEST services.opal-gateway deployed_commit CARRIES THE PF HANDLER BY CONTENT: its blobs of app/admin_gateway_breakdown.py and app/admin_people.py equal the blobs at 54a75d46ba
#      (the merge of MP-pe-1, MP-pf-1, MP-pf-3) and its blob of tests/test_admin_gateway_breakdown.py equals the one at 8ef1398867 (MP-pf-4's merge). NEVER by ancestry: a release is built by taking files whole
#      onto the live base, so merge-base --is-ancestor is false by construction (CLAUDE.md 22a; the first run of this check at the live 3d5c9c8bf1 read `descends: no` for exactly that reason).
#      Control: the blobs at the OLD live d577e0e7297b must DIFFER from them (else the comparison cannot discriminate);
#   2. mcportal_commit descends from 421f8fb (the page of PF round 2), read in the mcportal repo;
#   3. the SERVED `_compute` on the host (one read-only SSM command, _s1_served_probe.py) lists at least one segment under opal-data-assets or opal-data-bd
#      whose pair is not (unresolved, unresolved), and prints its denominator: channels, tools, segments per bucket.
# Prints the measured deployed_commit and mcportal_commit and the denominator either way. At the base (before OG-ap-23) it FAILs on 1.
. "$(dirname "$0")/../../pc/checks/_root.sh"
read -r DEP MCP < <(python -c "import json;g=json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway'];print(g.get('deployed_commit',''),g.get('mcportal_commit',''))" | tr -d '\r')
GWP=infra/aws/ec2/opal-gateway; d1=no; same=0; ctl=0
if [ -n "$DEP" ]; then
  for spec in "app/admin_gateway_breakdown.py 54a75d46ba" "app/admin_people.py 54a75d46ba" "tests/test_admin_gateway_breakdown.py 8ef1398867"; do
    set -- $spec
    a=$(git rev-parse "$DEP:$GWP/$1" 2>/dev/null); b=$(git rev-parse "$2:$GWP/$1" 2>/dev/null); o=$(git rev-parse "d577e0e7297b:$GWP/$1" 2>/dev/null)
    [ -n "$a" ] && [ "$a" = "$b" ] && same=$((same+1)); [ -n "$b" ] && [ "$b" != "$o" ] && ctl=$((ctl+1))
  done
fi
[ "$same" = 3 ] && [ "$ctl" = 3 ] && d1=yes
MC="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/mcportal"
d2=no; [ -n "$MCP" ] && git -C "$MC" merge-base --is-ancestor 421f8fb "$MCP" 2>/dev/null && d2=yes
echo "deployed_commit=$DEP carries the PF handler by content: $d1 (3 files equal: $same of 3; control, differ from the old live: $ctl of 3); mcportal_commit=$MCP descends from 421f8fb: $d2"
T="${TMPDIR:-/tmp}/mp_pf4_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks/_s1_served_probe.py "$(cygpath -m "$T")/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 '^S1 ' || echo "no S1 line")
echo "ssm command=$SSM_CID status=$SSM_ST; $(printf '%s' "$line" | cut -c1-1500)"
real=$(python -c "
import json, sys
s = sys.argv[1]
try: d = json.loads(s[3:])
except Exception: print('no'); sys.exit()
segs = [p for b in ('opal-data-assets', 'opal-data-bd') for p in d['segments'].get(b, [])]
print('yes' if any((p[0], p[1]) != ('unresolved', 'unresolved') for p in segs) else 'no')" "$line")
echo "a segment with a resolved pair is served: $real"
if [ "$d1" = yes ] && [ "$d2" = yes ] && [ "$SSM_ST" = Success ] && [ "$real" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
