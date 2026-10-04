#!/usr/bin/env bash
# OPLGTW OG-rl-5 AC1 (CTO round-15 analysis R9, item 2), on the SERVED gateway: the host's query.py and datasets.json
# equal the release head's bytes, and RL5_PAGING.json (written by the on-host run) records a rows-mode page of
# dim_position AND of dim_asset that SUCCEEDED on a qualified snapshot after the release, where the same request was
# REFUSED before it, run by a SYNTHETIC principal and grant with grants written 0 and the state store untouched.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL5_PAGING.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
S="$GW/app/integrations/schwab"; wq=$(git show "$c:$S/query.py" | md5sum | cut -c1-32); wd=$(git show "$c:$S/datasets.json" | md5sum | cut -c1-32)
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/integrations/schwab/query.py app/integrations/schwab/datasets.json"]}'
hq=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  app\/integrations\/schwab\/query.py$/\1/p')
hd=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  app\/integrations\/schwab\/datasets.json$/\1/p')
m=no; [ "$hq" = "$wq" ] && [ "$hd" = "$wd" ] && m=yes
echo "deployed_commit ${c:0:10}; host query.py + datasets.json equal the release bytes: $m"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" "$c" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); c = sys.argv[2]
ok = {"served_release": d.get("served_release") == c,
      "dim_position after ok": d.get("after", {}).get("dim_position") == "OK",
      "dim_asset after ok": d.get("after", {}).get("dim_asset") == "OK",
      "dim_position before refused": str(d.get("before", {}).get("dim_position", "")).startswith("REFUSED"),
      "synthetic principal": d.get("synthetic_principal") is True,
      "grants_written 0": d.get("grants_written") == 0,
      "state_store_written false": d.get("state_store_written") is False}
for k, v in ok.items():
    print("%s: %s" % (k, v))
sys.exit(0 if all(ok.values()) else 1)
PY
prc=$?
[ "$m" = yes ] && [ "$prc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
