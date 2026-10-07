#!/usr/bin/env bash
# OPLGTW OG-rl-7 AC1 under A1 (CTO R22: OA-e-10 reverted), on the SERVED gateway: the host's app/server.py,
# app/admin_refusals.py and app/integrations/schwab/envelope.py equal the release head's bytes; server.py at the
# release equals live 37be3485db's (the /login path is UNCHANGED); and RL7_SENDER.json (the after-read) shows the
# admin-refusals listing taking sender fields from entry args only (present -> as given; absent -> null), synthetic.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL7_SENDER.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
L="app/server.py app/admin_refusals.py app/integrations/schwab/envelope.py"
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/server.py app/admin_refusals.py app/integrations/schwab/envelope.py"]}'
eq=0; for f in $L; do w=$(git show "$c:$GW/$f" 2>/dev/null | md5sum | cut -c1-32); h=$(printf '%s\n' "$SSM_OUT" | grep "  $f\$" | cut -c1-32); [ -n "$h" ] && [ "$h" = "$w" ] && eq=$((eq+1)); done
sv=no; [ "$(git show "$c:$GW/app/server.py" | md5sum | cut -c1-32)" = "$(git show "37be3485db:$GW/app/server.py" | md5sum | cut -c1-32)" ] && sv=yes
echo "deployed_commit ${c:0:10}; host shipped app files equal the release bytes: $eq of 3; server.py equals live 37be3485db: $sv"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" "$c" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); c = sys.argv[2]
ok = {"served_release": d.get("served_release") == c,
      "sender from entry args": d.get("after", {}).get("with_sender_args") == "AS_GIVEN",
      "sender null when absent": d.get("after", {}).get("without_sender_args") == "NULL",
      "grants_written 0": d.get("grants_written") == 0}
for k, v in ok.items():
    print("%s: %s" % (k, v))
sys.exit(0 if all(ok.values()) else 1)
PY
prc=$?
[ "$eq" = 3 ] && [ "$sv" = yes ] && [ "$prc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
