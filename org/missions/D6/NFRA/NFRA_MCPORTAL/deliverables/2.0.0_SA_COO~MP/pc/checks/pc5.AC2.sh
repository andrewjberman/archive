#!/usr/bin/env bash
# MP-pc-5 AC2 (SERVED, on the host): /health=200 (control); with NO identity, GET /api/admin/people and the deep link
# /people each answer 401 or 403 (owner-gated, not 404); the served admin_people._compute under the instance role returns
# >=2 persons, exactly 1 population row, >=1 tool, every tool's cadence claim "absent", grant_store read, in <= 30 s; and
# the served gitstate shows at least two of the three PC.2 states, one of them "no" (Z-C-S31's fix is served).
. "$(dirname "$0")/_root.sh"
T="${TMPDIR:-/tmp}/mp_pc5_ac2_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pc/checks/_pc5_probe.py "$T/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
h=$(v /health); pe=$(v people); dl=$(v /people)
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 'people_s=' || echo "compute: $(printf '%s\n' "$SSM_OUT" | tail -1)")
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$h; no-identity people=$pe /people=$dl; $line"
ok=$(python -c "
import re, sys
m = re.search(r'people_s=([0-9.]+) persons=(\d+) population=(\d+) tools=(\d+) cadence_absent=(\d+) grant_store=(\w+) refused_states=(\S+)', sys.argv[1])
st = set(m.group(7).split(',')) if m else set()
print('yes' if m and float(m.group(1)) <= 30 and int(m.group(2)) >= 2 and int(m.group(3)) == 1 and int(m.group(4)) >= 1 and int(m.group(5)) == int(m.group(4)) and m.group(6) == 'read' and 'no' in st and len(st) >= 2 else 'no')" "$line")
gate=yes; for s in "$pe" "$dl"; do case "$s" in 401|403) ;; *) gate=no;; esac; done
if [ "$SSM_ST" = Success ] && [ "$h" = 200 ] && [ "$gate" = yes ] && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
