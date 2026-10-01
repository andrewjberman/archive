#!/usr/bin/env bash
# OA-f-10 AC3 (acceptance, CTO ruling R2.3; runs only after Andrew's apply): the wall is LIVE and does exactly its job.
#   live  both rules exist and are enabled, read from the firewall itself: one per account, Outbound, Block, TCP,
#         RemotePort 8194, LocalUser naming that account's live SID
#   arms  F10_ACCEPTANCE.json (the E6 procedure re-run, TCP connect only): Opal_Agent 8194 != OPEN and 8790 OPEN;
#         Opal_MSP 8194 != OPEN and 8790 OPEN; operator 8194 OPEN (the control: DAPI is up)
. "$(dirname "$0")/_root.sh"
J="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~25/F10_ACCEPTANCE.json"
live=$(timeout 90 powershell -NoProfile -Command '
$n = 0
foreach ($a in @("Opal_Agent","Opal_MSP")) {
  $sid = (Get-LocalUser -Name $a -ErrorAction SilentlyContinue).SID.Value
  if (-not $sid) { continue }
  foreach ($r in @(Get-NetFirewallRule -Direction Outbound -Action Block -Enabled True -ErrorAction SilentlyContinue)) {
    $pf = $r | Get-NetFirewallPortFilter; $sf = $r | Get-NetFirewallSecurityFilter
    if ($pf.Protocol -eq "TCP" -and "$($pf.RemotePort)" -eq "8194" -and "$($sf.LocalUser)" -match [regex]::Escape($sid)) { $n++; break }
  }
}
$n' 2>&1 | tr -d '\r' | tail -1)
if [ -f "$J" ]; then
  arms=$(python - "$J" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
r = {(a.get("account"), int(a.get("port", 0))): a.get("result") for a in d.get("arms", [])}
ok = (r.get(("Opal_Agent", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_Agent", 8790)) == "OPEN"
      and r.get(("Opal_MSP", 8194)) in ("REFUSED", "TIMEOUT") and r.get(("Opal_MSP", 8790)) == "OPEN"
      and r.get(("operator", 8194)) == "OPEN")
print(f"agent 8194={r.get(('Opal_Agent',8194))} 8790={r.get(('Opal_Agent',8790))}; msp 8194={r.get(('Opal_MSP',8194))} 8790={r.get(('Opal_MSP',8790))}; operator 8194={r.get(('operator',8194))}; arms ok={'yes' if ok else 'no'}")
PY
)
else arms="F10_ACCEPTANCE.json absent; arms ok=no"; fi
echo "live 8194 block rules matching an account SID: ${live:-?} of 2; $arms"
if [ "$live" = 2 ] && printf '%s' "$arms" | grep -q 'arms ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
