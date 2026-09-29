#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t3.AC1.sh (2.0.0_SA_COO~AI). ONE amendment: the gate runs from a detached opal_ai worktree at $OA_NESTED_PIN (_pin.sh), and the
# difference-control plant goes into THAT checkout, never the nested HEAD.
# OA-t-3 AC1 (the launch gate, seam against the REAL wrong account + difference control): run as THIS account (a local
# Administrator that can read the workspace), launch-gate.ps1 must REFUSE naming PROBE-READABLE and ADMIN-GROUP, and must
# NOT name CHECKOUT-DIRTY while the checkout is clean (arm 1); with one planted untracked file in the checkout it must
# ALSO name CHECKOUT-DIRTY (arm 2). The plant is removed afterwards.
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/_pin.sh"
G="$PT/opal/runtime/launch-gate.ps1"
[ -f "$G" ] || { echo "$G absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/oa_t3_ac1_$$"; mkdir -p "$T/state"
head=$(git -C "$PT" rev-parse HEAD)
python - "$T/cfg.json" "$(cygpath -w "$PT")" "$(cygpath -w "$T/state")" "$(cygpath -w "$(pwd)/CLAUDE.md")" "$head" <<'EOF'
import json, sys
json.dump({"checkout_dir": sys.argv[2], "state_dir": sys.argv[3], "workspace_probe_file": sys.argv[4], "prod_ref": sys.argv[5]},
          open(sys.argv[1], "w", encoding="utf-8"))
EOF
run() { timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$G")" -Config "$(cygpath -w "$T/cfg.json")" 2>&1 | tr -d '\r'; }
o1=$(run); r1=$?
PL="$PT/.oa_t3_ac1_plant_$$"; : > "$PL"
o2=$(run); r2=$?
rm -f "$PL"; rm -rf "$T"
l1=$(printf '%s\n' "$o1" | grep -m1 '^GATE: ' || echo "(no GATE line)")
l2=$(printf '%s\n' "$o2" | grep -m1 '^GATE: ' || echo "(no GATE line)")
echo "arm1 rc=$r1 $l1"; echo "arm2 rc=$r2 $l2"
has() { printf '%s' "$1" | grep -qw -- "$2"; }
if [ "$r1" != 0 ] && [ "$r2" != 0 ] && has "$l1" REFUSE && has "$l1" PROBE-READABLE && has "$l1" ADMIN-GROUP && ! has "$l1" CHECKOUT-DIRTY \
   && has "$l2" CHECKOUT-DIRTY && has "$l2" PROBE-READABLE && has "$l2" ADMIN-GROUP; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
