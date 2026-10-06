#!/usr/bin/env bash
# OPLGTW OG-rl-7 AC1 (CTO round-18 analysis s.4 item 2; R16), on the SERVED gateway: the host's shipped app files equal
# the release head's bytes (app/server.py, app/admin_refusals.py, app/integrations/schwab/envelope.py), and RL7_LOGIN.json
# (written before and after the act) names who /login admitted over the 30 days before the act (from live audit), the
# configured admit set after, and 0 identities that used /login in the window yet fall outside it (an outsider BLOCKS);
# the after-read shows /login admitting a configured identity's flow and refusing an unconfigured one (synthetic, host-local).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL7_LOGIN.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
L="app/server.py app/admin_refusals.py app/integrations/schwab/envelope.py"
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/server.py app/admin_refusals.py app/integrations/schwab/envelope.py"]}'
eq=0; for f in $L; do w=$(git show "$c:$GW/$f" 2>/dev/null | md5sum | cut -c1-32); h=$(printf '%s\n' "$SSM_OUT" | grep "  $f\$" | cut -c1-32); [ -n "$h" ] && [ "$h" = "$w" ] && eq=$((eq+1)); done
echo "deployed_commit ${c:0:10}; host shipped app files equal the release bytes: $eq of 3"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" "$c" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); c = sys.argv[2]
ok = {"served_release": d.get("served_release") == c,
      "audit window days >= 30": (d.get("window_days") or 0) >= 30,
      "admit set before named": isinstance(d.get("admit_before"), list) and len(d.get("admit_before")) > 0,
      "admit set after named": isinstance(d.get("admit_after"), list) and len(d.get("admit_after")) > 0,
      "outsiders in window 0": d.get("outsiders_in_window") == [],
      "configured identity admitted after": d.get("after", {}).get("configured") == "ADMITTED",
      "unconfigured identity refused after": str(d.get("after", {}).get("unconfigured", "")).startswith("REFUSED"),
      "grants_written 0": d.get("grants_written") == 0}
for k, v in ok.items():
    print("%s: %s" % (k, v))
sys.exit(0 if all(ok.values()) else 1)
PY
prc=$?
[ "$eq" = 3 ] && [ "$prc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
