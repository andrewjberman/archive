#!/usr/bin/env bash
# OA-f-10 AC2 (built): opal_ai/opal/runtime/provision/wall-dapi-8194.ps1 at ${OA_F10_REF:-HEAD} -- the apply script for
# the CTO's R1 wall. Arms:
#   plan  -Plan (default accounts) -> exactly 2 'PLAN: RULE' lines; each names OUTBOUND, BLOCK, TCP, 8194, 127.0.0.0/8 and
#         NO '::1' (AMENDMENT 2, CTO msg 28005: New-NetFirewallRule rejects ::1; bbcomm listens on 127.0.0.1 only, so the rule is 127.0.0.0/8 only), and the LIVE SID of Opal_Agent / Opal_MSP (read here via Get-LocalUser, never from the script); no line names 8790
#   unk   -Plan -Accounts NoSuchAccount -> 'WALL: REFUSE UNKNOWN-ACCOUNT', exit 2
#   elev  real mode from this (non-elevated) token -> 'ELEVATION REQUIRED', exit 3, before any act (skipped, and said so,
#         if this token IS elevated)
#   bound no 'S-1-5-21' literal in the script; it parses; vs r2-dev e69acf7 the only file changed is the script.
. "$(dirname "$0")/_root.sh"
REF="${OA_F10_REF:-HEAD}"; BASE="e69acf7"; S="opal/runtime/provision/wall-dapi-8194.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f10ac2_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$S" > "$T/w.ps1" 2>/dev/null || { echo "wall-dapi-8194.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
ps() { timeout 60 powershell -NoProfile -ExecutionPolicy Bypass "$@" 2>&1 | tr -d '\r'; }
sids=$(ps -Command "(Get-LocalUser -Name Opal_Agent).SID.Value; (Get-LocalUser -Name Opal_MSP).SID.Value")
sa=$(printf '%s\n' "$sids" | sed -n 1p); sm=$(printf '%s\n' "$sids" | sed -n 2p)
plan=$(ps -File "$WT\\w.ps1" -Plan); prc=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\w.ps1" -Plan >/dev/null 2>&1; echo $?)
nrule=$(printf '%s\n' "$plan" | grep -c '^PLAN: RULE ')
good=$(printf '%s\n' "$plan" | grep '^PLAN: RULE ' | grep -i 'OUTBOUND' | grep -i 'BLOCK' | grep -i 'TCP' | grep -F '8194' | grep -F '127.0.0.0/8' | grep -v -F '::1' | grep -c .)
hasA=$(printf '%s\n' "$plan" | grep '^PLAN: RULE ' | grep -c -F "$sa"); hasM=$(printf '%s\n' "$plan" | grep '^PLAN: RULE ' | grep -c -F "$sm")
n8790=$(printf '%s\n' "$plan" | grep -c '8790')
unk=$(ps -File "$WT\\w.ps1" -Plan -Accounts NoSuchAccount | grep -m1 'WALL: REFUSE UNKNOWN-ACCOUNT'); urc=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\w.ps1" -Plan -Accounts NoSuchAccount >/dev/null 2>&1; echo $?)
el=$(ps -Command "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)" | tail -1)
if [ "$el" = "False" ]; then
  eo=$(ps -File "$WT\\w.ps1" | grep -m1 'ELEVATION REQUIRED'); erc=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\w.ps1" >/dev/null 2>&1; echo $?)
else eo="SKIPPED-ELEVATED"; erc=3; fi
lit=$(grep -c 'S-1-5-21' "$T/w.ps1")
pe=$(ps -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\w.ps1',[ref]\$null,[ref]\$e); \$e.Count" | tail -1)
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$S" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: plan rc=$prc PLAN: RULE lines=$nrule well-formed=$good Opal_Agent SID named=$hasA Opal_MSP SID named=$hasM lines naming 8790=$n8790; unknown='${unk:-none}' rc=$urc; elevated=$el real-mode='${eo:-none}' rc=$erc; S-1-5-21 literals=$lit; parse errors=$pe; other files changed vs $BASE=$others"
if [ "$prc" = 0 ] && [ "$nrule" = 2 ] && [ "$good" = 2 ] && [ "$hasA" = 1 ] && [ "$hasM" = 1 ] && [ "$n8790" = 0 ] \
   && [ -n "$unk" ] && [ "$urc" = 2 ] && [ -n "$eo" ] && [ "$erc" = 3 ] && [ "$lit" = 0 ] && [ "$pe" = 0 ] && [ "$others" = 0 ]; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
