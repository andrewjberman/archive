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
# AMENDMENT 1 (issuer, OA-f-11): the installer's sublayer VERIFY compares weight == 0xFFFF exactly, and on a box whose
# top sublayer weights are held by an EDR it can never pass. The sublayer is then proven from the ELEVATED WFP dump instead:
# F11_SUBLAYER_EVIDENCE.json must show it present + persistent and holding BOTH BLOCK filters (V4+V6, 8194, IS_LOOPBACK,
# both SIDs), and both filter VERIFY lines must read OK.
import os
evp = os.path.join("org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~AI/round2", "F11_SUBLAYER_EVIDENCE.json")
fv = sum(1 for l in d.get("apply_verify", []) if "block_v" in str(l) and str(l).rstrip().endswith("OK"))
ev_ok = False
if os.path.exists(evp):
    e = json.load(open(evp, encoding="utf-8"))
    fl = e.get("filters_in_sublayer", [])
    ev_ok = (e.get("sublayer", {}).get("persistent") is True and len(fl) == 2
             and {f.get("layer") for f in fl} == {"FWPM_LAYER_ALE_AUTH_CONNECT_V4", "FWPM_LAYER_ALE_AUTH_CONNECT_V6"}
             and all(f.get("action_block") and f.get("port_8194") and f.get("is_loopback_flag") and len(f.get("sids", [])) == 2 for f in fl))
apply_ok = v >= 3 or (fv == 2 and ev_ok)
ok = (r.get(("Opal_Agent", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_Agent", 8790)) == "OPEN"
      and r.get(("Opal_MSP", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_MSP", 8790)) == "OPEN"
      and r.get(("operator", 8194)) == "OPEN" and apply_ok)
print(f"agent 8194={r.get(('Opal_Agent',8194))} 8790={r.get(('Opal_Agent',8790))}; msp 8194={r.get(('Opal_MSP',8194))} 8790={r.get(('Opal_MSP',8790))}; operator 8194={r.get(('operator',8194))}; apply VERIFY OK lines={v} (filters {fv}, sublayer evidence={'yes' if ev_ok else 'no'}); arms ok={'yes' if ok else 'no'}")
PY
)
else arms="F11_ACCEPTANCE.json absent; arms ok=no"; fi
echo "R1 Firewall rules still present: ${r1:-?}; $arms"
if [ "$r1" = 0 ] && printf '%s' "$arms" | grep -q 'arms ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
