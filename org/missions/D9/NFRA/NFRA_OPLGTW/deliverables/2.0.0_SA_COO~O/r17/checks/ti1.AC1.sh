#!/usr/bin/env bash
# OPLGTW OG-ti-1 AC1 (row Z-W15-S37, CTO round-16 analysis s.4 item 4): the WHOLE schwab test set runs in ONE pytest
# process with 0 setup/collection ERRORS (at the cut: 9-11, all StreamableHTTP RuntimeError), no FAILURE beyond the
# per-file baseline (r17/Q7_SUITE_BASELINE.txt), and at least as many tests collected as the cut's per-file total at CLOUD b91a1a44cf (134 in one process: 122 passed + 1 failed + 11 errors).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
B="$(cd "$(dirname "$0")/.." && pwd)/Q7_SUITE_BASELINE.txt"
export AUDIT_PATH="${TMP:-/tmp}/og_r17_ti1_audit_$$.jsonl"
O="${TMP:-/tmp}/og_r17_ti1_$$.txt"
( cd "$GW" && timeout 1200 python -m pytest tests -k schwab -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O"
restore_audit; rm -f "$AUDIT_PATH"
python - "$(native "$O")" "$(native "$B")" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
base = set(l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#"))
errs = set(m.group(1).replace("\\", "/") for m in re.finditer(r"(?m)^ERROR (\S+)", t))
fails = set(m.group(1).replace("\\", "/") for m in re.finditer(r"(?m)^FAILED (\S+)", t))
m = re.search(r"(\d+) passed", t); passed = int(m.group(1)) if m else 0
coll = passed + len(errs) + len(fails)
new = sorted(fails - base)
print("one process: collected %d; passed %d; errors %d; failures %d; failures beyond baseline %d %s" % (coll, passed, len(errs), len(fails), len(new), new[:5]))
ok = not errs and not new and coll >= 134
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
r=$?; rm -f "$O"; exit $r
