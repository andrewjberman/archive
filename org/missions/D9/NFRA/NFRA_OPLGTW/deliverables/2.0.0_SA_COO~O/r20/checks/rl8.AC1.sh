#!/usr/bin/env bash
# OPLGTW OG-rl-8 AC1 (CTO R24), on the SERVED gateway: the host's app/server.py (and the audit write site the release
# changed, listed in RL8_LOGIN.json files_shipped) equal the release head's bytes; RL8_LOGIN.json names the /login admit
# set BEFORE and AFTER computed from the tier rule over the current principal population, with lost_nonrestricted EMPTY
# (a principal admitted before and refused after that is not restricted BLOCKS); and the after-read shows, through the
# deployed code with synthetic principals: a non-restricted principal ADMITTED, a restricted one REFUSED, the server-held
# identity ADMITTED, and one /login audit record per request (count matches requests made).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL8_LOGIN.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
L=$(python -c "import json,sys;print(' '.join(json.load(open(sys.argv[1],encoding='utf-8')).get('files_shipped',[])))" "$(native "$F")" | tr -d '\r')
[ -n "$L" ] || L="app/server.py"
cmd=$(python -c "import json,sys;print(json.dumps({'commands':['cd /opt/opal-gateway && md5sum '+sys.argv[1]]}))" "$L" | tr -d '\r')
ssm_run "$cmd"
n=0; eq=0; for f in $L; do n=$((n+1)); w=$(git show "$c:$GW/$f" 2>/dev/null | md5sum | cut -c1-32); h=$(printf '%s\n' "$SSM_OUT" | grep "  $f\$" | cut -c1-32); [ -n "$h" ] && [ "$h" = "$w" ] && eq=$((eq+1)); done
echo "deployed_commit ${c:0:10}; host shipped files equal the release bytes: $eq of $n"
python - "$(native "$F")" "$c" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); c = sys.argv[2]; a = d.get("after", {})
ok = {"served_release": d.get("served_release") == c,
      "admit set before named": isinstance(d.get("admit_before"), list) and len(d["admit_before"]) > 0,
      "admit set after named": isinstance(d.get("admit_after"), list) and len(d["admit_after"]) > 0,
      "lost non-restricted 0": d.get("lost_nonrestricted") == [],
      "non-restricted admitted": a.get("nonrestricted") == "ADMITTED",
      "restricted refused": str(a.get("restricted", "")).startswith("REFUSED"),
      "server-held admitted": a.get("server_held") == "ADMITTED",
      "one audit record per request": isinstance(a.get("requests"), int) and a.get("requests") > 0 and a.get("audit_records") == a.get("requests"),
      "grants_written 0": d.get("grants_written") == 0}
for k, v in ok.items():
    print("%s: %s" % (k, v))
sys.exit(0 if all(ok.values()) else 1)
PY
prc=$?
[ "$n" -ge 1 ] && [ "$eq" = "$n" ] && [ "$prc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
