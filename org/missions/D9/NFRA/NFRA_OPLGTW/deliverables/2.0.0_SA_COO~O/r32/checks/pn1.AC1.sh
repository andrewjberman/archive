#!/usr/bin/env bash
# OPLGTW OG-pn-1 AC1 (CTO~Z AMENDMENT 1 on OG-bh-1, row Z-W46-S3): the RPS section-1 pin extension. Three named tests in
# data/assets/scripts/silver/tests/test_ogpn1_rps_pin.py, offline:
#   (01) the pin names each of the 28 columns the held 08403355 files carry (the list read from a held file's own
#        header, committed as a fixture), and a header carrying a column outside the extended pin still raises
#        SchemaDriftError (the guard is not loosened);
#   (02) a held file's real section-1 rows convert: fact_rps / fact_rps_s2 / dim_position / dim_balance are produced;
#   (03) an 08335338 RPS file (no new columns) converts byte-for-byte as before (same row count, same column set).
# Plus the converter's existing suites whole (no regression): test_schwab_conversion/projections/schemas.py and test_conversion_manifest.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T="data/assets/scripts/silver/tests"
r=0
[ -f "$T/test_ogpn1_rps_pin.py" ] || { echo "$T/test_ogpn1_rps_pin.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$T" && timeout 110 python -m pytest test_ogpn1_rps_pin.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogpn1_ac01 test_ogpn1_ac02 test_ogpn1_ac03; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
echo "pin tests: pytest rc=$rc; named tests passed $p of 3"
[ "$rc" = 0 ] && [ "$p" = 3 ] || r=1
files=$(cd "$T" && ls test_schwab_conversion.py test_schwab_projections.py test_schwab_schemas.py test_conversion_manifest.py 2>/dev/null | tr '\n' ' ')
n=0; for f in $files; do n=$((n+1)); o=$(cd "$T" && timeout 110 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); c=$?; echo "$f: pytest rc=$c; $(printf '%s\n' "$o" | tail -1)"; [ "$c" = 0 ] || r=1; done
echo "regression suites run: $n"
[ "$n" -ge 1 ] || r=1
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
