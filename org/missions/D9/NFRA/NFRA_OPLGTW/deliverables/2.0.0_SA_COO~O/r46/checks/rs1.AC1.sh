#!/usr/bin/env bash
# OPLGTW OG-rs-1 AC1: the hung gateway service is RESTARTED (same code, no deploy) and answers again.
#  - ledger nfra-oplgtw-gateway-restart-20261019 CLOSED at HEAD, sentinel gone;
#  - W/RS1_RESTART.json: health before not 200, health after 200 within 60 s of the restart, the marker equals the live release sha
#    read BEFORE and AFTER (6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c), tools/list 103 before-restart-expectation and after,
#    one process, NRestarts after the restart read, memory before and after (counts only), the host md5 walk differing 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"; slug=nfra-oplgtw-gateway-restart-20261019
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rec=$(python - "$(native "$W/RS1_RESTART.json")" <<'EOF'
import json, sys
SHA = "6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c"
try:
    r = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    print("record absent"); print("NO"); raise SystemExit(0)
hb, ha = r.get("health_before"), r.get("health_after")
ok_h = hb not in (200, "200") and ha in (200, "200") and (r.get("health_after_seconds_from_restart") or 999) <= 60
ok_m = r.get("marker_before") == SHA and r.get("marker_after") == SHA
ok_t = r.get("tools_list_after") == 103
ok_p = r.get("processes_after") == 1 and r.get("nrestarts_after") is not None
ok_d = r.get("host_md5_differ") == 0
print("health before %s, after %s within 60 s: %s; marker equals the live release before and after: %s; tools/list 103: %s; one process: %s; host md5 differ 0: %s"
      % (hb, ha, "yes" if ok_h else "no", "yes" if ok_m else "no", "yes" if ok_t else "no", "yes" if ok_p else "no", "yes" if ok_d else "no"))
print("OK" if (ok_h and ok_m and ok_t and ok_p and ok_d) else "NO")
EOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
echo "$slug: status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
printf '%s\n' "$rec" | sed '$d'
[ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
