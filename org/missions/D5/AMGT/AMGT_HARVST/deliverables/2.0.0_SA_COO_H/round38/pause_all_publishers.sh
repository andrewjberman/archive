#!/usr/bin/env bash
# READIED PAUSE for AMGT_HARVST collection on every publisher (CTO msg 28725, CARD_HARVST_PUBLISHER_TERMS_20261002.md).
# Flip it ONLY on Andrew's answer (a) to that card. Collection is UNCHANGED until then: pausing on anyone else's word
# would override his standing RULE.
#
#   bash pause_all_publishers.sh --dry-run   prints the live collectors and what the flip would do; changes nothing
#   bash pause_all_publishers.sh --flip      the pause: writes the STOP set and waits for the drivers to stop
#
# The STOP set:
#   .runtime/harvest-backfill/STOP     the stop file every running backfill driver was launched with (--stop-file);
#                                      a driver checks it between jobs, records stopped_by_operator, and exits
#   .runtime/harvest-backfill/STOP_<P> one operator marker per publisher (sa bbg wsj barrons ft), so that no driver
#                                      is relaunched on a publisher while its marker stands
# Nothing is deleted and nothing is killed: the in-flight job finishes and the driver exits at its boundary.
# To reverse: remove the files (Andrew's word), then relaunch as before.
set -u
ROOT=$(git rev-parse --show-toplevel) || exit 2
BF="$ROOT/.runtime/harvest-backfill"
MODE="${1:---dry-run}"
PUBS="sa bbg wsj barrons ft"

collectors() {
  # Every live python running the harvest package or the backfill driver. Windows' own process table is read
  # through PowerShell, because MSYS ps cannot see native processes.
  powershell.exe -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'opal_data_harvest' } | ForEach-Object { '{0} {1}' -f \$_.ProcessId, (\$_.CommandLine -replace '\s+',' ').Substring(0,[Math]::Min(160,(\$_.CommandLine -replace '\s+',' ').Length)) }" | tr -d '\r'
}

echo "MODE $MODE   at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "LIVE COLLECTORS (pid, command):"
C=$(collectors); if [ -n "$C" ]; then printf '%s\n' "$C" | sed 's/^/  /'; else echo "  none"; fi
echo "STOP SET NOW:"
for f in STOP $(for p in $PUBS; do printf 'STOP_%s ' "$(echo "$p" | tr a-z A-Z)"; done); do
  if [ -e "$BF/$f" ]; then echo "  $f present"; else echo "  $f absent"; fi
done
TASK=$(powershell.exe -NoProfile -Command "(Get-ScheduledTask -TaskName 'Opal Data Harvest - Local Publications' -ErrorAction SilentlyContinue).State" | tr -d '\r')
echo "SCHEDULED TASK 'Opal Data Harvest - Local Publications': ${TASK:-not found}"

if [ "$MODE" != "--flip" ]; then
  echo "DRY RUN: --flip would write $BF/STOP and STOP_<P> for: $PUBS; then wait for the live drivers to exit."
  exit 0
fi

STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for f in STOP $(for p in $PUBS; do printf 'STOP_%s ' "$(echo "$p" | tr a-z A-Z)"; done); do
  [ -e "$BF/$f" ] || printf 'paused %s on Andrew answer (a), CARD_HARVST_PUBLISHER_TERMS_20261002.md\n' "$STAMP" > "$BF/$f"
done
echo "FLIPPED at $STAMP: the STOP set is written."
# Wait up to 30 min for every driver to reach its job boundary and exit.
n=0
while [ $n -lt 120 ]; do
  C=$(collectors)
  [ -z "$C" ] && break
  sleep 15; n=$((n+1))
done
if [ -n "$(collectors)" ]; then
  echo "STILL RUNNING after $((n*15))s -- a job has not reached its boundary:"; collectors | sed 's/^/  /'; exit 1
fi
echo "PAUSED: 0 live collectors after $((n*15))s."
for ck in "$BF"/*_checkpoint.json; do
  python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print('  %s stopped_by_operator=%s at %s'%(sys.argv[1].split('/')[-1],d.get('stopped_by_operator'),d.get('stopped_by_operator_at')))" "$ck"
done
