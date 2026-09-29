#!/usr/bin/env bash
# AMGT_RESAPP round 50, AMGT-yy-1 AC3 -- the value-comparing grade reads three named SERVED names value-equal. The sweep prints ONE line
#   FWD-30 GRADE: equal E of I identified names; values equal V of I; unidentified U of F folders; keyed on: data-attributes
# PASS when I == 3 and E == V == I and the sweep exits 0. The full 96-folder run is the issuer's at the drain.
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" timeout 115 python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py \
  --served --live --require-cases --only AMD_US_Equity,ASML_NA_Equity,BABA_US_Equity \
  --cache "$T/cache" --out "$T/out.tsv" > "$T/log" 2>&1
rc=$?
python - "$T/log" "$rc" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r"^FWD-30 GRADE: equal (\d+) of (\d+) identified names; values equal (\d+) of (\d+);.*keyed on: (\S+)", text, re.M)
if not m:
    print("no value-bearing 'FWD-30 GRADE:' line (sweep rc=%s):" % sys.argv[2])
    print("\n".join(l for l in text.splitlines() if l.startswith("FWD-30 GRADE")) or "\n".join(text.strip().splitlines()[-3:]))
    print("THE GRADE COMPARES VALUES ON THE NAMED SET: NO")
    sys.exit(1)
e, i, v, i2 = (int(m.group(n)) for n in (1, 2, 3, 4))
print(m.group(0))
ok = i == 3 and i2 == i and e == i and v == i and sys.argv[2] == "0"
print("THE GRADE COMPARES VALUES ON THE NAMED SET: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
PY
