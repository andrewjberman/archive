#!/usr/bin/env bash
# DSGN_AMGTV1 round 3, AV-r-3 AC2 -- the DIFFERENCE CONTROL for FWD-30's page/export parity harness: keyed on data, it must
# still FAIL when the export genuinely differs. One export "ABSENT -- <reason>" line (a line the harness counts) is deleted from a copy of AMGT_RESAPP's served rich
# export (1299_HK_Equity), and the harness is run against that copy: it must exit non-zero with ABSENCES missing>0 or extra>0.
# A harness that passes this copy has been made blind, not re-keyed.
# usage: bash <this>   (from the repo root of the worktree under test)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
FX="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures"
RICH="$FX/1299_HK_Equity.rich.md"
T="$(mktemp)"; M="$(mktemp --suffix=.md)"; trap 'rm -f "$T" "$M"' EXIT
n=$(grep -cE "ABSENT[[:space:]]*--[[:space:]]*." "$RICH")
[ "$n" -gt 0 ] || { echo "PARITY CONTROL: the export fixture carries no absence line to delete (n=0) -- control not runnable"; exit 1; }
line=$(grep -nE "ABSENT[[:space:]]*--[[:space:]]*." "$RICH" | head -1 | cut -d: -f1)
sed "${line}d" "$RICH" > "$M"
( cd portal && timeout 110 node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs \
    --fixture "$FX/served_fixture.1299_HK_Equity.json" --rich "$M" ) > "$T" 2>&1; rc=$?
abs=$(grep -E "^ABSENCES " "$T")
( cd portal && timeout 110 node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs     --fixture "$FX/served_fixture.1299_HK_Equity.json" --rich "$RICH" ) > "$T.base" 2>&1
abs0=$(grep -E "^ABSENCES " "$T.base"); rm -f "$T.base"
r0=$(echo "$abs0" | grep -oE "rich=[0-9]+" | cut -d= -f2); r1=$(echo "$abs" | grep -oE "rich=[0-9]+" | cut -d= -f2)
echo "deleted export line $line (an 'ABSENT -- ' line, $n in the export); export absences $r0 -> $r1; harness rc=$rc; $abs"
[ -n "$r0" ] && [ -n "$r1" ] && [ "$r1" -lt "$r0" ] || { echo "PARITY CONTROL: the deletion did not move the export's absence count -- control not exercised"; exit 1; }
if [ "$rc" != "0" ] && echo "$abs" | grep -qE "missing=[1-9]|extra=[1-9]"; then
  echo "PARITY CONTROL: a deleted export absence is caught: YES"; exit 0
fi
echo "PARITY CONTROL: a deleted export absence is caught: NO"; exit 1
