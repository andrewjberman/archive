#!/usr/bin/env bash
# OPLGTW OG-rl-5 AC1 (CTO round-15 analysis R9, item 2), on the SERVED gateway: the host's query.py and datasets.json
# equal the release head's bytes, and RL5_PAGING.json (written by the on-host run) records a rows-mode page of
# dim_position AND of dim_asset that SUCCEEDED on a qualified snapshot after the release, where the same request was
# REFUSED before it, run by a SYNTHETIC principal and grant with grants written 0 and the state store untouched.
# AMENDED A3 (CTO R12 @261571c07e): the host contract equals the release's deploy copy; the served census AFTER reads
# servable snapshots at both masters with 0 lacking an R9 column; the dim_asset rows page returns only CUSIPs held by the
# grant's accounts (0 unheld); a dim_asset prepare_download still REFUSES asset_policy_selection_unavailable (control).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL5_PAGING.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
S="$GW/app/integrations/schwab"; wq=$(git show "$c:$S/query.py" | md5sum | cut -c1-32); wd=$(git show "$c:$S/datasets.json" | md5sum | cut -c1-32)
wc=$(git show "$c:$GW/deploy/NFRA_OPLGTW_CONTRACT.json" | md5sum | cut -c1-32)
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/integrations/schwab/query.py app/integrations/schwab/datasets.json deploy/NFRA_OPLGTW_CONTRACT.json"]}'
hq=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  app\/integrations\/schwab\/query.py$/\1/p')
hd=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  app\/integrations\/schwab\/datasets.json$/\1/p')
hc=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  deploy\/NFRA_OPLGTW_CONTRACT.json$/\1/p')
m=no; [ "$hq" = "$wq" ] && [ "$hd" = "$wd" ] && [ "$hc" = "$wc" ] && m=yes
echo "deployed_commit ${c:0:10}; host query.py + datasets.json + contract equal the release bytes: $m"
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
      "state_store_written false": d.get("state_store_written") is False,
      "census after servable at both masters": all((d.get("census_after", {}).get("servable_by_master", {}).get(k) or 0) > 0 for k in ("08242234", "08335338")),
      "census after lacking 0": d.get("census_after", {}).get("lacking_or_blank") == 0,
      "dim_asset held-only (unheld returned 0)": d.get("dim_asset_held_check", {}).get("returned", 0) > 0 and d.get("dim_asset_held_check", {}).get("unheld_returned") == 0,
      "dim_asset download refused": str(d.get("after_dim_asset_download", "")).startswith("REFUSED") and "asset_policy_selection_unavailable" in str(d.get("after_dim_asset_download", ""))}
for k, v in ok.items():
    print("%s: %s" % (k, v))
sys.exit(0 if all(ok.values()) else 1)
PY
prc=$?
[ "$m" = yes ] && [ "$prc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
