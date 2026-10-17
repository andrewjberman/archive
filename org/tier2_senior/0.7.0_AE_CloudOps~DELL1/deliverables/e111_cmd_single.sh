echo START=$(date -u +%H:%M:%SZ)
if ps -eo cmd | grep -E 'gold_dispatch|run_gold_layer|gold-layer' | grep -v grep >/dev/null; then echo "ABORT: a gold process is running"; ps -eo pid,etimes,cmd | grep -E 'gold_dispatch|run_gold_layer|gold-layer' | grep -v grep; exit 20; fi
if aws s3api head-object --bucket opal-data-bd --key gold/trigger-pending.json >/dev/null 2>&1; then echo "ABORT: gold/trigger-pending.json waits"; exit 21; fi
aws s3 cp s3://opal-data-bd/code/gold/gold_dispatch.sh /tmp/gold_dispatch.sh --only-show-errors || { echo "ABORT: gold_dispatch.sh pull failed"; exit 22; }
md5sum /tmp/gold_dispatch.sh
BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single E_18 > /tmp/e111_single.out 2>&1
echo SINGLE-RC=$?
echo "--- E_18 on the box"
md5sum /tmp/gold_layer_scripts/E_18.detect_new_securities.py
echo "--- ERROR lines: $(grep -c 'ERROR' /tmp/e111_single.out)"
grep -n 'ERROR' /tmp/e111_single.out | head -10
echo "--- held-out tickers mentioned"
for t in BALCX CIMAX DODBX FSNQX HBLFX JBAWX KAMIX PCEF TRRNX; do echo "$t: $(grep -c "$t" /tmp/e111_single.out)"; done
echo "--- unresolved lines"
grep -i -n 'unresolved' /tmp/e111_single.out | head -20
echo "--- single output tail"
grep -v 'Classification not found' /tmp/e111_single.out | tail -60
echo END=$(date -u +%H:%M:%SZ)
