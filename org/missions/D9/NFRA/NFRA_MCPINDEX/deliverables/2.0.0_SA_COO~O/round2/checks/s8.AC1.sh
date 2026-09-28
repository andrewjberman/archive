#!/usr/bin/env bash
# MX-s-8 AC1 (repo bytes): each of the 4 vendored mirror_conversion.py copies carries BOTH source fixes --
# Z-S3's pandas-3 string-dtype arm in to_arrow and Z-S25's exactly-empty -> None in _numeric_or_raise -- and none
# carries the old bare guard `float64" and df[c].dtype == object`.
. "$(dirname "$0")/_root.sh"
V="${VENDOR_ROOT:-infra/aws/lambda/opal-assets}"
both=0; old=0; n=0
for f in blackdiamond etf eclipse orion; do
  p="$V/opal-assets-silver-$f/mirror_conversion.py"
  [ -f "$p" ] || { echo "MISSING $p"; continue; }
  n=$((n+1))
  a=$(grep -c 'pd.api.types.is_string_dtype(df\[c\].dtype)' "$p"); b=$(grep -c 'if v == "":' "$p")
  [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && both=$((both+1))
  grep -q 'float64" and df\[c\].dtype == object' "$p" && old=$((old+1))
done
echo "vendored copies=$n both fixes $both of $n old guard $old"
if [ "$n" -eq 4 ] && [ "$both" -eq 4 ] && [ "$old" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
