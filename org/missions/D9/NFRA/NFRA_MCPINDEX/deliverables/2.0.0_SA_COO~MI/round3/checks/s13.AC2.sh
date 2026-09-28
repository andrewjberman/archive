#!/usr/bin/env bash
# MX-s-13 AC2 (row Z-S31, R-10): every one of the 5 stepwise scripts in the redaction set still parses (`bash -n`).
. "$(dirname "$0")/_root.sh"
D=infra/aws/ec2/bd-exporter/src/stepwise
ok=0; n=0
for s in run-daily-downloads.sh run-backfill.sh run-allocation-backfill.sh historical-backfill-2014-2020.sh extended-backfill.sh; do
  n=$((n+1))
  if [ -f "$D/$s" ] && bash -n "$D/$s" 2>/dev/null; then ok=$((ok+1)); else echo "  bash -n FAILED or absent: $s"; fi
done
echo "bash -n passes $ok of $n"
if [ "$ok" = 5 ] && [ "$n" = 5 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
