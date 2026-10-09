#!/usr/bin/env bash
# MP-r-2 AC3 (SERVED, on the host): /health=200 (control); with NO identity, GET /api/admin/fabric/overlap, /gitstate,
# /calls and POST /api/admin/fabric/calls/close each answer 401 or 403 (the owner gate covers every new route on the served
# code); and the served modules' own _compute functions, run from the host's venv under the instance role against the LIVE
# store, read >=1 box each -- overlap deploys 'read', gitstate 'recorded', calls 'published' -- each in at most 30 s.
. "$(dirname "$0")/_root.sh"
T="${TMPDIR:-/tmp}/mp_r2_ac3_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/checks/_r2_probe.py "$T/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
h=$(v /health); o=$(v overlap); g=$(v gitstate); c=$(v calls); x=$(v close)
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 'overlap_s=' || echo "compute: $(printf '%s\n' "$SSM_OUT" | tail -1)")
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$h; no-identity overlap=$o gitstate=$g calls=$c close(POST)=$x; $line"
ok=$(python -c "
import re, sys
m = re.search(r'overlap_s=([0-9.]+) deploys_read=(\d+) gitstate_s=([0-9.]+) recorded=(\d+) calls_s=([0-9.]+) published=(\d+)', sys.argv[1])
print('yes' if m and all(float(m.group(i)) <= 30 for i in (1, 3, 5)) and all(int(m.group(i)) >= 1 for i in (2, 4, 6)) else 'no')" "$line")
gate=yes; for s in "$o" "$g" "$c" "$x"; do case "$s" in 401|403) ;; *) gate=no;; esac; done
if [ "$SSM_ST" = Success ] && [ "$h" = 200 ] && [ "$gate" = yes ] && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
