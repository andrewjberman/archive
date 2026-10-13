#!/usr/bin/env bash
# MP-z-5 AC2 (SERVED, on the host): /health=200 (control); with NO identity, GET /api/admin/gateway/breakdown and the
# deep links /control-plane, /open-calls, /gateway each answer 401 or 403 (owner-gated, NOT 404 -- the Z-S41 fix is
# served); an unlisted path answers 404; and the served module's _compute, run from the host's venv under the instance
# role, returns >=2 channels, >=1 tool, 0 duplicate tools, >=1 channel with a holder and grant_store read, in <= 30 s.
. "$(dirname "$0")/_root.sh"
T="${TMPDIR:-/tmp}/mp_z5_ac2_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/fwd20/checks/_z5_probe.py "$T/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
h=$(v /health); b=$(v breakdown); cp=$(v /control-plane); oc=$(v /open-calls); gw=$(v /gateway); nx=$(v /no-such-page-z5)
line=$(printf '%s\n' "$SSM_OUT" | grep -m1 'breakdown_s=' || echo "compute: $(printf '%s\n' "$SSM_OUT" | tail -1)")
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$h; no-identity breakdown=$b /control-plane=$cp /open-calls=$oc /gateway=$gw; unlisted=$nx; $line"
ok=$(python -c "
import re, sys
m = re.search(r'breakdown_s=([0-9.]+) channels=(\d+) tools=(\d+) dup_tools=(\d+) channels_held=(\d+) grant_store=(\w+)', sys.argv[1])
print('yes' if m and float(m.group(1)) <= 30 and int(m.group(2)) >= 2 and int(m.group(3)) >= 1 and int(m.group(4)) == 0 and int(m.group(5)) >= 1 and m.group(6) == 'read' else 'no')" "$line")
gate=yes; for s in "$b" "$cp" "$oc" "$gw"; do case "$s" in 401|403) ;; *) gate=no;; esac; done
if [ "$SSM_ST" = Success ] && [ "$h" = 200 ] && [ "$gate" = yes ] && [ "$nx" = 404 ] && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
