#!/usr/bin/env bash
# OPLGTW OG-tb-1 AC1 (analysis round 12 s.5 item 6; NFRA_MCPINDEX round-6 L8 packet s.4): each of the 9 named OPLGTW
# red tests either PASSES on this tree now, or is NAMED in RED_TESTS_R13.json with a non-empty reason. Accounted 9 of 9.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~18/RED_TESTS_R13.json"
export AUDIT_PATH="${TMP:-/tmp}/og_r13_tb_audit_$$.jsonl"
T="tests/test_browser_oidc.py::test_oga3_ac01 tests/test_browser_oidc.py::test_oga3_ac07 tests/test_principal_cutover.py::test_oga2_ac04
tests/test_data_entitlement_guard.py::test_ogz1_ac05 tests/test_data_entitlement_guard.py::test_ogz1_ac08 tests/test_entitlement_admin.py::test_ogz2_ac06
tests/test_schwab_audit.py::test_ogo1_ac07 tests/test_schwab_engine.py::test_ogq1_ac07 tests/test_schwab_export_stream.py::test_ogx4_ac03"
res=""
for t in $T; do
  o=$(cd "$GW" && timeout 300 python -m pytest "$t" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r=$?
  if [ "$r" = 0 ] && printf '%s\n' "$o" | grep -qE "^1 passed"; then res="$res$t PASS"$'\n'; else res="$res$t FAIL"$'\n'; fi
done
restore_audit; rm -f "$AUDIT_PATH"
RF="${TMP:-/tmp}/og_r13_tb_res_$$.txt"; printf '%s' "$res" > "$RF"
python - "$(native "$F")" "$(native "$RF")" <<'EOF'
import json, os, sys
names = {}
if os.path.exists(sys.argv[1]):
    names = json.load(open(sys.argv[1], encoding="utf-8"))
p = n = 0; un = []
for line in open(sys.argv[2], encoding="utf-8").read().splitlines():
    t, st = line.rsplit(" ", 1)
    e = names.get(t, {})
    if st == "PASS": p += 1
    elif e.get("status") == "NAMED" and str(e.get("reason", "")).strip(): n += 1
    else: un.append(t)
print("9 red tests: passing now %d; named with a reason %d; unaccounted %d %s" % (p, n, len(un), un))
ok = (p + n == 9) and not un
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
EOF
rc=$?; rm -f "$RF"; exit $rc
