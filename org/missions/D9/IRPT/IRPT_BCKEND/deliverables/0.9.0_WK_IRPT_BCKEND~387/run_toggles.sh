#!/bin/bash
# Scratch (IB-pr-542 amendment): four toggled builds, twice, on the same receipts (rec_r1).
cd /c/dev/_scratch387
H=/c/dev/_scratch387/cot_harness.py
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
for run in r1 r2; do
for n in account keyed cusip multi; do
  python -I $H build --tree toggle/$n --label tog_${n}_$run --out out/tog_${n}_$run.json.gz --meta-out out/meta_tog_${n}_$run.json --seed out/rec_r1.json || { echo "FAIL $n $run"; exit 1; }
done
done
echo TOGGLES-DONE
