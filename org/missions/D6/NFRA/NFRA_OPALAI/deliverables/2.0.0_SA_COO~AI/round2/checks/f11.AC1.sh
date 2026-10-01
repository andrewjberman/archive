#!/usr/bin/env bash
# OA-f-11 AC1 (built, plan + bounds): opal_ai/opal/runtime/provision/wall-dapi-8194-wfp.ps1 at ${OA_F11_REF:-HEAD} -- the
# raw WFP filter pair of CTO ruling R5 (@9d6fbe3e97). Run non-elevated, so no engine is opened and nothing changes:
#   plan   -Plan -> 'COMPILE: OK' (the Add-Type P/Invoke type compiled) then exactly 1 'PLAN: SUBLAYER' line naming
#          PERSISTENT and weight 0xFFFF, and exactly 2 'PLAN: FILTER' lines (one ALE_AUTH_CONNECT_V4, one _V6), each naming
#          BLOCK, PERSISTENT, REMOTE_PORT 8194, IS_LOOPBACK and an SDDL that carries BOTH live SIDs (Opal_Agent, Opal_MSP, read
#          here via Get-LocalUser); no line names 8790
#   elev   real mode AND -Remove from this non-elevated token -> 'ELEVATION REQUIRED', exit 3 each (skipped if elevated)
#   bound  no 'S-1-5-21' literal; P/Invokes fwpuclnt FwpmTransactionBegin0 + FwpmFilterAdd0 + FwpmSubLayerAdd0; carries the
#          pre-act refusal token 'WFP: REFUSE PERMIT-WEIGHT' and removes the R1 rules (opal_runtime_block_dapi_8194_ +
#          Remove-NetFirewallRule); parses; vs r2-dev eeca5ca7d1 the only file changed is this script.
. "$(dirname "$0")/_root.sh"
REF="${OA_F11_REF:-HEAD}"; BASE="eeca5ca7d1"; S="opal/runtime/provision/wall-dapi-8194-wfp.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f11ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$S" > "$T/w.ps1" 2>/dev/null || { echo "wall-dapi-8194-wfp.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
ps() { timeout 90 powershell -NoProfile -ExecutionPolicy Bypass "$@" 2>&1 | tr -d '\r'; }
rc() { timeout 90 powershell -NoProfile -ExecutionPolicy Bypass "$@" >/dev/null 2>&1; echo $?; }
sids=$(ps -Command "(Get-LocalUser -Name Opal_Agent).SID.Value; (Get-LocalUser -Name Opal_MSP).SID.Value")
sa=$(printf '%s\n' "$sids" | sed -n 1p); sm=$(printf '%s\n' "$sids" | sed -n 2p)
plan=$(ps -File "$WT\\w.ps1" -Plan); prc=$(rc -File "$WT\\w.ps1" -Plan)
comp=$(printf '%s\n' "$plan" | grep -c '^COMPILE: OK')
nsub=$(printf '%s\n' "$plan" | grep '^PLAN: SUBLAYER' | grep -i 'PERSISTENT' | grep -i -c '0xFFFF')
f4=$(printf '%s\n' "$plan" | grep '^PLAN: FILTER' | grep -c 'ALE_AUTH_CONNECT_V4')
f6=$(printf '%s\n' "$plan" | grep '^PLAN: FILTER' | grep -c 'ALE_AUTH_CONNECT_V6')
good=$(printf '%s\n' "$plan" | grep '^PLAN: FILTER' | grep -i 'BLOCK' | grep -i 'PERSISTENT' | grep -F '8194' | grep -i 'IS_LOOPBACK' | grep -F "$sa" | grep -F "$sm" | grep -c .)
nfil=$(printf '%s\n' "$plan" | grep -c '^PLAN: FILTER')
n8790=$(printf '%s\n' "$plan" | grep -c '8790')
el=$(ps -Command "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)" | tail -1)
if [ "$el" = "False" ]; then
  r1=$(ps -File "$WT\\w.ps1" | grep -c 'ELEVATION REQUIRED'); c1=$(rc -File "$WT\\w.ps1")
  r2=$(ps -File "$WT\\w.ps1" -Remove | grep -c 'ELEVATION REQUIRED'); c2=$(rc -File "$WT\\w.ps1" -Remove)
else r1=1; c1=3; r2=1; c2=3; fi
lit=$(grep -c 'S-1-5-21' "$T/w.ps1")
pinv=0; for t in fwpuclnt FwpmTransactionBegin0 FwpmFilterAdd0 FwpmSubLayerAdd0; do grep -q "$t" "$T/w.ps1" && pinv=$((pinv+1)); done
refuse=$(grep -c 'WFP: REFUSE PERMIT-WEIGHT' "$T/w.ps1")
r1rm=0; grep -q 'opal_runtime_block_dapi_8194_' "$T/w.ps1" && grep -q 'Remove-NetFirewallRule' "$T/w.ps1" && r1rm=1
pe=$(ps -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\w.ps1',[ref]\$null,[ref]\$e); \$e.Count" | tail -1)
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$S" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: plan rc=$prc COMPILE OK=$comp SUBLAYER persistent 0xFFFF=$nsub FILTER lines=$nfil (V4=$f4 V6=$f6) well-formed=$good lines naming 8790=$n8790; elevated=$el real ELEVATION REQUIRED=$r1 rc=$c1, -Remove ELEVATION REQUIRED=$r2 rc=$c2; S-1-5-21 literals=$lit; P/Invoke tokens=$pinv of 4; PERMIT-WEIGHT refusal=$refuse; removes R1 rules=$r1rm; parse errors=$pe; other files changed vs $BASE=$others"
if [ "$prc" = 0 ] && [ "$comp" -ge 1 ] && [ "$nsub" = 1 ] && [ "$nfil" = 2 ] && [ "$f4" = 1 ] && [ "$f6" = 1 ] && [ "$good" = 2 ] && [ "$n8790" = 0 ] \
   && [ "$r1" -ge 1 ] && [ "$c1" = 3 ] && [ "$r2" -ge 1 ] && [ "$c2" = 3 ] && [ "$lit" = 0 ] && [ "$pinv" = 4 ] && [ "$refuse" -ge 1 ] \
   && [ "$r1rm" = 1 ] && [ "$pe" = 0 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
