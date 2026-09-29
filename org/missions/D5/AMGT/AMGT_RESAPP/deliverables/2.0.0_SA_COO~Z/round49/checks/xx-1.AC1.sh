#!/usr/bin/env bash
# AMGT_RESAPP round 49, AMGT-xx-1 AC1 -- FWD-30's ONE grader (round45/checks/sweep.py) keys every page read on the page's data
# attributes and reads three named SERVED names equal. ASML_NA_Equity and BABA_US_Equity read NOT_OK at round 48's close on page
# WORDING alone (row Z-S305); AMD_US_Equity read OK. The full 96-folder population is the issuer's run at the drain.
# The sweep must print ONE line:  FWD-30 GRADE: equal E of I identified names; unidentified U of F folders; keyed on: data-attributes
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" timeout 115 python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py \
  --served --live --require-cases --only AMD_US_Equity,ASML_NA_Equity,BABA_US_Equity \
  --cache "$T/cache" --out "$T/out.tsv" > "$T/log" 2>&1
rc=$?
grep -E "^[0-9]+/[0-9]+ " "$T/log" | grep -v -E " (None|) CAPTURE_FAILED" | tail -3
python - "$T/log" "$rc" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r"^FWD-30 GRADE: equal (\d+) of (\d+) identified names; unidentified (\d+) of (\d+) folders; keyed on: (\S+)", text, re.M)
if not m:
    print("no 'FWD-30 GRADE:' line (sweep rc=%s); last lines:" % sys.argv[2])
    print("\n".join(text.strip().splitlines()[-3:]))
    print("FWD-30 GRADER KEYED ON DATA ATTRIBUTES READS THE NAMED SET EQUAL: NO")
    sys.exit(1)
e, i, u, f, key = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
print(m.group(0))
ok = key == "data-attributes" and i == 3 and e == i and sys.argv[2] == "0"
print("FWD-30 GRADER KEYED ON DATA ATTRIBUTES READS THE NAMED SET EQUAL: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
PY
