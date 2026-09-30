#!/usr/bin/env bash
# AMGT_RESAPP round 54, AMGT-ad-4 AC2 -- with the grader reading an UNRESOLVED header figure's raw digits, the served sweep over three names
# -- TSM (the round-53 close's one NOT_OK: HEADER CURR_ENTP_VAL, unit UNRESOLVED on both sides) and two controls (ASML_NA_Equity,
# AMD_US_Equity) reads values equal 3 of 3 and 0 differing value facts. (The full 96-name re-grade is the issuer's real run at the drain.)
# usage: bash <this>   (from the repo root; read-only Invokes; its own temp cache)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" timeout 115 python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py \
  --served --live --require-cases --only TSM_US_Equity,ASML_NA_Equity,AMD_US_Equity --cache "$T/cache" --out "$T/out.tsv" > "$T/log" 2>&1
rc=$?
python - "$T/log" "$rc" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
g = re.search(r"^FWD-30 GRADE: equal (\d+) of (\d+) identified names; values equal (\d+) of (\d+)", text, re.M)
v = re.search(r"value facts over \d+ compared names: compared=(\d+) differ=(\d+)", text)
print(g.group(0) if g else "no 'FWD-30 GRADE:' line (sweep rc=%s)" % sys.argv[2])
print(v.group(0) if v else "no value-facts line")
ok = bool(g and v) and int(g.group(2)) == 3 and int(g.group(3)) == 3 and int(v.group(2)) == 0 and int(v.group(1)) > 0
print("TSM AND TWO CONTROLS READ VALUES-EQUAL: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
PY
