#!/usr/bin/env bash
# OPLGTW OG-rl-6 AC1 (CTO round-16 analysis s.4 item 2), on the SERVED gateway: the host's integration.py equals the
# release head's bytes, and RL6_DOWNLOAD.json (written by the on-host AFTER run) records, through the served
# construction by a SYNTHETIC principal and grant (grants written 0, state store untouched): a dim_asset download that
# was REFUSED before and is OK after; every downloaded CUSIP held by the grant's accounts (unheld 0) beside its
# discriminator (held < the snapshot's asset universe, CVO r16 Q2); an empty-holdings grant REFUSED
# asset_read_denied_unqualified; and the dim_asset query unchanged (OK, the same held set).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r14/checks/_ssm.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL6_DOWNLOAD.json"
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
S="$GW/app/integrations/schwab"; wi=$(git show "$c:$S/integration.py" | md5sum | cut -c1-32)
ssm_run '{"commands":["cd /opt/opal-gateway && md5sum app/integrations/schwab/integration.py"]}'
hi=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^\([0-9a-f]\{32\}\)  app\/integrations\/schwab\/integration.py$/\1/p')
m=no; [ -n "$hi" ] && [ "$hi" = "$wi" ] && m=yes
echo "deployed_commit ${c:0:10}; host integration.py equals the release bytes: $m"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" "$c" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); c = sys.argv[2]
h = d.get("held_check", {})
ok = {"served_release": d.get("served_release") == c,
      "download before refused": str(d.get("before", {}).get("dim_asset_download", "")).startswith("REFUSED"),
      "download after ok": d.get("after", {}).get("dim_asset_download") == "OK",
      "held-only (unheld 0, discriminated)": (h.get("returned", 0) > 0 and h.get("unheld_returned") == 0
                                               and 0 < (h.get("held_cusips_in_dim_position") or 0) < (h.get("asset_universe_cusips") or 0)),
      "empty holdings refused": "asset_read_denied_unqualified" in str(d.get("after", {}).get("empty_holdings_download", "")),
      "query unchanged": d.get("after", {}).get("dim_asset_query") == "OK" and d.get("query_held_equal_download_held") is True,
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
