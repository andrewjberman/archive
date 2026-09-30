#!/usr/bin/env bash
# AMGT_RESAPP round 51, AMGT-zz-8 AC2 -- ON THE SERVED PLANE the six names whose export printed an UNRESOLVED unit read values-equal WITH
# units: the served sweep (sweep.py --served) over 6501/9433/8316/8035/8766 JP and TSM US prints values equal 6 of 6 and
# "digits compared, scale unchecked (export unit UNRESOLVED)=0". FWD-30 is REALIZED only on this (CTO round-50 ruling 3).
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" timeout 300 python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py \
  --served --live --require-cases --only 6501_JP_Equity,9433_JP_Equity,8316_JP_Equity,8035_JP_Equity,8766_JP_Equity,TSM_US_Equity \
  --cache "$T/cache" --out "$T/out.tsv" > "$T/log" 2>&1
rc=$?
python - "$T/log" "$rc" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
g = re.search(r"^FWD-30 GRADE: equal (\d+) of (\d+) identified names; values equal (\d+) of (\d+)", text, re.M)
u = re.search(r"scale unchecked \(export unit UNRESOLVED\)=(\d+)", text)
print(g.group(0) if g else "no 'FWD-30 GRADE:' line (sweep rc=%s)" % sys.argv[2])
print("scale unchecked (export unit UNRESOLVED)=%s" % (u.group(1) if u else "not printed"))
ok = bool(g and u) and int(g.group(2)) == 6 and int(g.group(1)) == 6 and int(g.group(3)) == 6 and int(u.group(1)) == 0
print("THE SERVED SIX READ VALUES-EQUAL WITH UNITS: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
PY
