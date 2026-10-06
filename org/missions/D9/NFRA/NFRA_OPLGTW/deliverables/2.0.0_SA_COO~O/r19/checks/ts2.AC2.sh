#!/usr/bin/env bash
# OPLGTW OG-ts-2 AC2 (row Z-W25-S3): two schwab export runs launched CONCURRENTLY (tests/test_schwab_export.py and
# tests/test_schwab_export_stream.py, each its own process, started together) BOTH finish with no failure beyond the
# per-file baseline and no FileNotFoundError -- each process uses its own export directory. The collision is
# intermittent, so the concurrent run alone does not discriminate (it PASSed pre-cut); the MECHANISM is graded by the
# named test tests/test_schwab_export.py::test_ogts2_export_dir_per_process (the export directory a test process uses
# is unique to that process), which must pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_schwab_export.py test_ogts2_export_dir_per_process; rn=$?
B="$(cd "$(dirname "$0")/../../r17" && pwd)/Q7_SUITE_BASELINE.txt"
O1="${TMP:-/tmp}/og_r19_ts2c1_$$.txt"; O2="${TMP:-/tmp}/og_r19_ts2c2_$$.txt"
( cd "$GW" && AUDIT_PATH="${TMP:-/tmp}/og_r19_c1_$$.jsonl" timeout 600 python -m pytest tests/test_schwab_export.py -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O1" &
p1=$!
( cd "$GW" && AUDIT_PATH="${TMP:-/tmp}/og_r19_c2_$$.jsonl" timeout 600 python -m pytest tests/test_schwab_export_stream.py -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O2" &
p2=$!
wait $p1; wait $p2
restore_audit; rm -f "${TMP:-/tmp}/og_r19_c1_$$.jsonl" "${TMP:-/tmp}/og_r19_c2_$$.jsonl"
python - "$(native "$O1")" "$(native "$O2")" "$(native "$B")" <<'PY'
import re, sys
base = set(l.strip() for l in open(sys.argv[3], encoding="utf-8") if l.strip() and not l.startswith("#"))
bad = []; fnf = 0; passed = 0
for p in sys.argv[1:3]:
    t = open(p, encoding="utf-8", errors="replace").read()
    fnf += t.count("FileNotFoundError")
    bad += sorted(set(m.group(2).replace("\\", "/") for m in re.finditer(r"(?m)^(FAILED|ERROR) (\S+)", t)) - base)
    m = re.search(r"(\d+) passed", t); passed += int(m.group(1)) if m else 0
print("concurrent export runs: passed %d; failures beyond baseline %d %s; FileNotFoundError %d" % (passed, len(bad), bad[:3], fnf))
ok = passed > 0 and not bad and fnf == 0
sys.exit(0 if ok else 1)
PY
r=$?; rm -f "$O1" "$O2"
[ "$rn" = 0 ] && [ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
