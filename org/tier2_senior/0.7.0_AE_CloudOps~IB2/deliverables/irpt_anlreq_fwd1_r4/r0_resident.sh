#!/bin/bash
# IRPT_ANLREQ TO-RUN-FWD1 window 4, R0(e): READ ONLY on the resident host, run as root through Systems Manager. Writes nothing.
U=irpt-analysis-resident.service
WD=$(systemctl show -p WorkingDirectory --value $U)
echo "R0e unit=$(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value $U) root=$WD"
PY=$(systemctl show -p ExecStart --value $U | grep -o 'argv\[\]=[^ ]*' | head -1 | cut -d= -f2)
sudo -u "$(systemctl show -p User --value $U)" "$PY" - "$WD" <<'PYEOF'
import json, os, sys
root = sys.argv[1]
b = json.load(open(os.path.join(root, "reports/resident_bindings.json"), encoding="utf-8"))
print("R0e bindings keys:", sorted(b))
print("R0e opal_pricing enabled=%s tiers=%s" % (b["opal_pricing"]["enabled"], b["opal_pricing"].get("tiers")))
for k, v in b.items():
    if "producer" in k.lower():
        print("R0e %s = %s" % (k, json.dumps(v)))
PYEOF
echo "R0e Environment (names only, producer-related values shown):"
systemctl show -p Environment --value $U | tr ' ' '\n' | sed -E 's/=.*//' | sort | tr '\n' ' '; echo
systemctl show -p Environment --value $U | tr ' ' '\n' | grep -i -E 'PRODUCER' | head -3
J=$(journalctl -u $U --utc --since '2026-10-16 18:27:00' --no-pager 2>/dev/null)
echo "R0e journal since 18:27Z lines=$(echo "$J" | wc -l)"
echo "R0e journal securities_info=$(echo "$J" | grep -c -i 'securities_info') lookup=$(echo "$J" | grep -c -i 'lookup') WAF_CHALLENGE=$(echo "$J" | grep -c 'WAF_CHALLENGE') RESOLVE_RETRY=$(echo "$J" | grep -c 'RESOLVE_RETRY') handled_nonzero=$(echo "$J" | grep -c 'IRPT_RESIDENT_POLL handled=[1-9]')"
echo "R0e journal first matching lookup lines (if any, 160 chars):"
echo "$J" | grep -i -E 'securities_info|lookup' | head -3 | cut -c1-160
echo "R0e clock $(date -u +%FT%TZ)"
