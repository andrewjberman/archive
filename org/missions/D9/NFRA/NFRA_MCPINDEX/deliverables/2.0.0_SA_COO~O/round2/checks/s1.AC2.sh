#!/usr/bin/env bash
# MX-s-1 AC2 (the guard counts the holdings feed, live): for each of DIVZ and IDVZ, trueshares/<fund>/meta/backfill-status.json's
# silver guard reads "missing 0", fact_holdings objects exist under trueshares/<fund>/silver/fact_holdings/, and the
# guard's "expected" is within 2 of the live silver object total, fact_holdings INCLUDED. The slack of 2 covers the
# guard running a day behind the newest partition, measured at the cut: expected 72 vs 73 live, all fact_netassets_page.
# A guard that still ignores holdings would read expected ~= live total - (the holdings count, ~33) and fail.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; B=opal-data-assets; ok=0; line=""; T="${TMPDIR:-/tmp}/mx_s1_ac2_$$"; mkdir -p "$T"
for f in DIVZ IDVZ; do
  timeout 60 "$AWS" s3api get-object --bucket $B --key "trueshares/$f/meta/backfill-status.json" "$(cygpath -w "$T/$f.json")" >/dev/null 2>&1
  det=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['layers']['silver']['guard']['detail'])" "$T/$f.json" 2>/dev/null | tr -d '\r')
  exp=$(printf '%s' "$det" | sed -n 's/.*expected \([0-9]*\).*/\1/p'); mis=$(printf '%s' "$det" | sed -n 's/.*missing \([0-9]*\).*/\1/p')
  # Count keys client-side: length() over a paginated list returns a PAGE count (CLAUDE.md rule 22a, RETRIEVAL).
  keys=$(timeout 90 "$AWS" s3api list-objects-v2 --bucket $B --prefix "trueshares/$f/silver/" --query 'Contents[].Key' --output text 2>/dev/null | tr -d '\r' | tr '\t' '\n' | grep .)
  live=$(printf '%s\n' "$keys" | grep -c .); hold=$(printf '%s\n' "$keys" | grep -c '/fact_holdings/')
  line="$line $f: guard expected=${exp:-?} missing=${mis:-?} live silver=${live} of which fact_holdings=${hold};"
  [ -n "$exp" ] && [ "$mis" = 0 ] && [ "$hold" -gt 0 ] && [ "$exp" -ge $((live - 2)) ] && ok=$((ok+1))
done
rm -rf "$T"
echo "live:$line funds whose guard counts the holdings feed $ok of 2"
if [ "$ok" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
