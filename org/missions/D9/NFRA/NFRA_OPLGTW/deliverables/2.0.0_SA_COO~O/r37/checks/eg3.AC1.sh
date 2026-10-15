#!/usr/bin/env bash
# OPLGTW OG-eg-3 AC1 (round-37 HARVEST-RETIRE, PRD v3.11): the site Z harvest runner is retired -- the live task is Disabled, no cycle_runner process runs,
# the STOP file is present, and the five pin worktrees are still LOCKED (the rollback source).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/EG3_BEFORE.json" ] || { echo "EG3_BEFORE.json absent"; echo "RESULT: FAIL"; exit 1; }
live=$(powershell.exe -NoProfile -Command "\$s = (Get-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle').State; 'STATE=' + \$s; \$n = @(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'lib\.opal_data_harvest\.cycle_runner' }).Count; 'PROCS=' + \$n" | tr -d '\r')
state=$(printf '%s\n' "$live" | sed -n 's/^STATE=//p'); procs=$(printf '%s\n' "$live" | sed -n 's/^PROCS=//p')
stop=$(python - "$(native "$W/EG3_BEFORE.json")" <<'PY'
import json, os, sys
p = json.load(open(sys.argv[1], encoding="utf-8")).get("stop_file", "")
print("yes" if p and os.path.exists(p) else "no")
PY
)
stop=$(printf '%s' "$stop" | tr -d '\r')
locked=0
for pin in 3d88eccbc3 995adcaeaa 1c69fa35a3 c1be67f53c b5a7a3a4b6; do
  git worktree list --porcelain | awk -v p="wk-harvest-runner-pin-$pin" 'BEGIN{RS="";FS="\n"} $1 ~ p {for(i=1;i<=NF;i++) if($i ~ /^locked/) {print "L"; exit}}' | grep -q L && locked=$((locked+1))
done
echo "task state $state; cycle_runner processes $procs; STOP file present $stop; pins locked $locked of 5"
[ "$state" = Disabled ] && [ "$procs" = 0 ] && [ "$stop" = yes ] && [ "$locked" = 5 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
