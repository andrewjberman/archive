#!/usr/bin/env bash
# OA-f-11 AC4 (R5's persistence arm, the sixth arm of OA-f-11): after a reboot that came AFTER the WFP wall's apply, the wall
# still does its job with nothing re-applied. Reads the worker's F11_PERSISTENCE.json (the OA-f-11 AC3 probe, re-run):
#   boot   the record's boot_time (UTC) is later than OA-f-11's acceptance (2026-10-02T03:02Z), measured_at is later than
#          boot_time, and the box's live LastBootUpTime is not earlier than the record's (the record is of a real boot)
#   arms   Opal_Agent 8194 in REFUSED|TIMEOUT and 8790 OPEN; Opal_MSP 8194 in REFUSED|TIMEOUT and 8790 OPEN;
#          operator 8194 OPEN (the control: DAPI is up, so a refusal is the wall's and not an absent listener)
#   r1     the two R1 Firewall rules are still GONE (0 opal_runtime_block_dapi_8194_* rules, read live here), so the only
#          thing that can refuse an agent on 8194 is the persistent WFP pair
. "$(dirname "$0")/_root.sh"
J="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~26/F11_PERSISTENCE.json"
r1=$(timeout 60 powershell -NoProfile -Command "@(Get-NetFirewallRule -DisplayName 'opal_runtime_block_dapi_8194_*' -ErrorAction SilentlyContinue).Count" 2>&1 | tr -d '\r' | tail -1)
live=$(timeout 60 powershell -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')" 2>&1 | tr -d '\r' | tail -1)
if [ -f "$J" ]; then
  arms=$(python - "$J" "$live" <<'PY'
import json, sys
from datetime import datetime, timezone
def t(s):
    return datetime.strptime(str(s)[:16], "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
d = json.load(open(sys.argv[1], encoding="utf-8"))
apply_acc = t("2026-10-02T03:02")
try:
    boot, meas, live = t(d.get("boot_time")), t(d.get("measured_at")), t(sys.argv[2])
    boot_ok = boot > apply_acc and meas > boot and live >= boot
except Exception as e:
    boot_ok, boot, meas, live = False, d.get("boot_time"), d.get("measured_at"), sys.argv[2]
r = {(a.get("account"), int(a.get("port", 0))): a.get("result") for a in d.get("arms", [])}
ok = (boot_ok and r.get(("Opal_Agent", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_Agent", 8790)) == "OPEN"
      and r.get(("Opal_MSP", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_MSP", 8790)) == "OPEN"
      and r.get(("operator", 8194)) == "OPEN")
print(f"boot {d.get('boot_time')} after apply={'yes' if boot_ok else 'no'}; agent 8194={r.get(('Opal_Agent',8194))} 8790={r.get(('Opal_Agent',8790))}; msp 8194={r.get(('Opal_MSP',8194))} 8790={r.get(('Opal_MSP',8790))}; operator 8194={r.get(('operator',8194))}; arms ok={'yes' if ok else 'no'}")
PY
)
else arms="F11_PERSISTENCE.json absent; arms ok=no"; fi
echo "R1 Firewall rules present: ${r1:-?}; live boot ${live:-?}; $arms"
if [ "$r1" = 0 ] && printf '%s' "$arms" | grep -q 'arms ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
