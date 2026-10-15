echo START=$(date -u +%H:%M:%SZ)
if ps -eo cmd | grep -E 'gold_dispatch|run_gold_layer|gold-layer' | grep -v grep >/dev/null; then echo "ABORT: a gold process is running"; ps -eo pid,etimes,cmd | grep -E 'gold_dispatch|run_gold_layer|gold-layer' | grep -v grep; exit 20; fi
if aws s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "ABORT: gold/trigger-pending.json waits"; exit 21; fi
aws s3 cp s3://opal-data-bd/code/gold/gold_dispatch.sh /tmp/gold_dispatch.sh --only-show-errors || { echo "ABORT: gold_dispatch.sh pull failed"; exit 22; }
BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single C_06 > /tmp/e102_single.out 2>&1
echo SINGLE-RC=$?
echo "--- C_06 on the box"
md5sum /tmp/gold_layer_scripts/C_06.client_mix_timeseries.py
echo "--- single output, classification noise removed (tail)"
grep -v 'Classification not found' /tmp/e102_single.out | tail -45
echo "--- C06-ROLLING lines"
grep -h 'C06-ROLLING' /tmp/e102_single.out /tmp/gold_logs/*.log 2>/dev/null | sort -u | head -5
ls -la --time-style=full-iso /tmp/gold_logs 2>/dev/null | tail -4
echo END=$(date -u +%H:%M:%SZ)
