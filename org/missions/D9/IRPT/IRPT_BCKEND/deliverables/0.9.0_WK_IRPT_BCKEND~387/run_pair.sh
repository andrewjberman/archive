#!/bin/bash
# Scratch (IB-pr-542): one pair -- base (new pin) build with identity and receipts, then live build on those receipts, then compare.
set -u
R=$1   # run tag, e.g. r1
cd /c/dev/_scratch387
H=/c/dev/_scratch387/cot_harness.py
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
python -I $H build --tree /c/dev/wk-ib542-base --label base_$R --out out/base_$R.json.gz --meta-out out/meta_base_$R.json --identity-out out/id_$R.json.gz --receipts-out out/rec_$R.json || { echo "FAIL base $R"; exit 1; }
python -I $H build --tree /c/dev/_scratch387/live --label live_$R --out out/live_$R.json.gz --meta-out out/meta_live_$R.json --seed out/rec_$R.json || { echo "FAIL live $R"; exit 1; }
python -I $H compare --live out/live_$R.json.gz --base out/base_$R.json.gz --identity out/id_$R.json.gz --out out/cmp_$R.json --out-beyond out/beyond_$R.json.gz || { echo "FAIL compare $R"; exit 1; }
echo "DONE $R"
