#!/usr/bin/env bash
# OPLGTW OG-ti-2 AC1 (rows Z-W15-S37/S40, CTO round-17 analysis s.4 item 4): isolation FINISHED -- (1) tests/conftest.py
# carries NO per-module reset seam (0 references to the session manager's _has_started flag); (2) the whole schwab set in
# ONE process: 0 errors, no failure beyond r17/Q7_SUITE_BASELINE.txt, collected >= 138 (r17 close); (3) the S40 subset
# (yearinreview, q7 download, rl5 asset query, schwab_query, grain_r9, entitlement_admin::test_ogz2_ac08) in ONE process:
# 0 failed, 0 errors.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
B="$(cd "$(dirname "$0")/../../r17" && pwd)/Q7_SUITE_BASELINE.txt"
seam=$(grep -c '_has_started' "$GW/tests/conftest.py" 2>/dev/null); seam=${seam:-0}
export AUDIT_PATH="${TMP:-/tmp}/og_r18_ti2_audit_$$.jsonl"
O1="${TMP:-/tmp}/og_r18_ti2a_$$.txt"; O2="${TMP:-/tmp}/og_r18_ti2b_$$.txt"
( cd "$GW" && timeout 1200 python -m pytest tests -k schwab -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O1"
( cd "$GW" && timeout 600 python -m pytest tests/test_yearinreview_view.py tests/test_schwab_q7_asset_download.py tests/test_schwab_rl5_asset_query.py tests/test_schwab_query.py tests/test_schwab_grain_r9.py "tests/test_entitlement_admin.py::test_ogz2_ac08" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' ) > "$O2"
restore_audit; rm -f "$AUDIT_PATH"
python - "$(native "$O1")" "$(native "$O2")" "$(native "$B")" "$seam" <<'PY'
import re, sys
def read(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    e = set(m.group(1).replace("\\", "/") for m in re.finditer(r"(?m)^ERROR (\S+)", t))
    f = set(m.group(1).replace("\\", "/") for m in re.finditer(r"(?m)^FAILED (\S+)", t))
    m = re.search(r"(\d+) passed", t); return e, f, (int(m.group(1)) if m else 0)
base = set(l.strip() for l in open(sys.argv[3], encoding="utf-8") if l.strip() and not l.startswith("#"))
e1, f1, p1 = read(sys.argv[1]); e2, f2, p2 = read(sys.argv[2]); seam = int(sys.argv[4])
new = sorted(f1 - base)
print("conftest reset seam refs %d; whole set: collected %d, errors %d, failures beyond baseline %d %s; S40 subset: passed %d, failed %d, errors %d"
      % (seam, p1 + len(e1) + len(f1), len(e1), len(new), new[:3], p2, len(f2), len(e2)))
ok = seam == 0 and not e1 and not new and (p1 + len(e1) + len(f1)) >= 138 and not f2 and not e2 and p2 > 0
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
r=$?; rm -f "$O1" "$O2"; exit $r
