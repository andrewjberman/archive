#!/usr/bin/env bash
# OA-f-11 AC3 (acceptance, CTO ruling R5; runs only after Andrew's elevated apply): the WFP wall is LIVE and does exactly
# its job. Reads the worker's F11_ACCEPTANCE.json (the E6 procedure re-run, TCP connect only):
#   arms   Opal_Agent 8194 in REFUSED|TIMEOUT and 8790 OPEN; Opal_MSP 8194 in REFUSED|TIMEOUT and 8790 OPEN;
#          operator 8194 OPEN (the control: DAPI is up)
#   apply  the record carries the elevated run's read-back: apply_verify lists >= 3 'VERIFY: ... OK' lines (sublayer + 2 filters)
#   r1     the two inert R1 Firewall rules are GONE (0 opal_runtime_block_dapi_8194_* rules, read live here)
. "$(dirname "$0")/_root.sh"
J="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~26/F11_ACCEPTANCE.json"
r1=$(timeout 60 powershell -NoProfile -Command "@(Get-NetFirewallRule -DisplayName 'opal_runtime_block_dapi_8194_*' -ErrorAction SilentlyContinue).Count" 2>&1 | tr -d '\r' | tail -1)
if [ -f "$J" ]; then
  arms=$(python - "$J" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
r = {(a.get("account"), int(a.get("port", 0))): a.get("result") for a in d.get("arms", [])}
v = sum(1 for l in d.get("apply_verify", []) if str(l).startswith("VERIFY:") and str(l).rstrip().endswith("OK"))
ok = (r.get(("Opal_Agent", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_Agent", 8790)) == "OPEN"
      and r.get(("Opal_MSP", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_MSP", 8790)) == "OPEN"
      and r.get(("operator", 8194)) == "OPEN" and v >= 3)
print(f"agent 8194={r.get(('Opal_Agent',8194))} 8790={r.get(('Opal_Agent',8790))}; msp 8194={r.get(('Opal_MSP',8194))} 8790={r.get(('Opal_MSP',8790))}; operator 8194={r.get(('operator',8194))}; apply VERIFY OK lines={v}; arms ok={'yes' if ok else 'no'}")
PY
)
else arms="F11_ACCEPTANCE.json absent; arms ok=no"; fi
echo "R1 Firewall rules still present: ${r1:-?}; $arms"
if [ "$r1" = 0 ] && printf '%s' "$arms" | grep -q 'arms ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
