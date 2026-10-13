#!/usr/bin/env bash
# MP-n-4 AC2 (SERVED, on the host; C17 round-1 analysis E1 criterion 3): /health=200 (control); GET
# /api/admin/fabric/gitstate with NO identity answers 401 or 403; and the SERVED admin_fabric_gitstate._compute, cold (a
# fresh interpreter, empty cache), from the host's venv under the instance role against the LIVE store, prints its
# body-fetch count and reads >=1 box 'recorded' in AT MOST 5 s (round 1's bar was 10 s). Reuses the round-1 probe.
. "$(dirname "$0")/../../cp2/checks/_root.sh"
T="${TMPDIR:-/tmp}/mp_n4_ac2_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/c17/checks/_n1_probe.py "$T/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
h=$(v /health); gs=$(v gitstate)
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 'gitstate_s=' || echo "compute: $(printf '%s\n' "$SSM_OUT" | tail -1)")
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$h; no-identity gitstate=$gs; $line"
ok=$(python -c "
import re, sys
m = re.search(r'gitstate_s=([0-9.]+) body_fetches=(\d+) recorded=(\d+)', sys.argv[1])
print('yes' if m and float(m.group(1)) <= 5 and int(m.group(3)) >= 1 else 'no')" "$line")
case "$gs" in 401|403) gate=yes;; *) gate=no;; esac
if [ "$SSM_ST" = Success ] && [ "$h" = 200 ] && [ "$gate" = yes ] && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
