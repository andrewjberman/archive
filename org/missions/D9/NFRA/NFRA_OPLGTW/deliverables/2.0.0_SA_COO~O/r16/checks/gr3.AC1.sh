#!/usr/bin/env bash
# OPLGTW OG-gr-3 AC1, AMENDED A1+A2 (rows Z-W22-S3/S4, R9a): the FIVE named tests in tests/test_schwab_grain_r9.py pass, and the
# whole `tests -k schwab` run adds NO failure or error beyond the issuer's recorded baseline (r16/GR3_SUITE_BASELINE.txt,
# 12 ids at CLOUD 5454d04761), with at least as many tests collected as the baseline plus the five new ones (132):
# R9's fixture updates may turn red tests green, never green tests red, and no test is deleted or skipped away.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
B="$(cd "$(dirname "$0")/.." && pwd)/GR3_SUITE_BASELINE.txt"
export AUDIT_PATH="${TMP:-/tmp}/og_r16_gr3_audit_$$.jsonl"
pytest_named tests/test_schwab_grain_r9.py test_oggr3_ac01 test_oggr3_ac02 test_oggr3_ac03 test_oggr3_ac04 test_oggr3_ac05; r1=$?
O="${TMP:-/tmp}/og_r16_gr3_suite_$$.txt"
( cd "$GW" && timeout 1200 python -m pytest tests -k schwab -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O"
restore_audit; rm -f "$AUDIT_PATH"
python - "$(native "$O")" "$(native "$B")" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
base = set(l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#"))
now = set(m.group(2).replace("\\", "/") for m in re.finditer(r"(?m)^(FAILED|ERROR) (\S+)", t))
m = re.search(r"(\d+) passed", t)
passed = int(m.group(1)) if m else 0
coll = passed + len(now)
new = sorted(now - base)
fixed = sorted(base - now)
print("schwab suite: collected (passed+failed+errors) %d; failing now %d; NEW beyond baseline %d %s; baseline fixed %d"
      % (coll, len(now), len(new), new[:5], len(fixed)))
sys.exit(0 if (not new and coll >= 132) else 1)
PY
r2=$?; rm -f "$O"
[ "$r1" = 0 ] && [ "$r2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
