#!/usr/bin/env bash
# MX-r-11 AC3 (FWD-20 PROOF, second instrument): for ONE tool, the catalog's history depth and freshness agree with the
# served artifact as listed by the aws CLI (auto-paginated, counted client-side). Instrument c10_second.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"
T="${TMPDIR:-/tmp}/mx_r10_r11ac3_$$"; mkdir -p "$T"
python "$(native "$H/c10_second.py")" pick "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" 2>&1 | tr -d '\r' > "$T/pick"; prc=$?
cat "$T/pick"
read -r tag tool bucket prefix method depth fresh < "$T/pick"
[ "$prc" = 0 ] && [ "$tag" = PICK ] && [ -n "$fresh" ] || { rm -rf "$T"; echo "pick rc=$prc"; echo "RESULT: FAIL"; exit 1; }
[ "$prefix" = "-" ] && prefix=""
timeout 300 "$AWS" s3api list-objects-v2 --bucket "$bucket" --prefix "$prefix" --query 'Contents[].[Key,LastModified]' --output text > "$T/list.raw" 2> "$T/list.err"; lrc=$?
tr -d '\r' < "$T/list.raw" > "$T/list.tsv"
echo "listing rc=$lrc; lines=$(wc -l < "$T/list.tsv"); stderr: $(head -c 200 "$T/list.err" | tr '\n' ' ')"
out=$(python "$(native "$H/c10_second.py")" grade "$(native "$T/pick")" "$(native "$T/list.tsv")" 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -3
if [ "$lrc" = 0 ] && [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
