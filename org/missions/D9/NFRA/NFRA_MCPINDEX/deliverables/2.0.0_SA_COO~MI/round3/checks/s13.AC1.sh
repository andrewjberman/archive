#!/usr/bin/env bash
# MX-s-13 AC1 (row Z-S31, R-10): no tracked file under infra/aws/ec2/bd-exporter/ carries a NON-EMPTY literal
# BD_PASSWORD value or default. Counts only; no value is ever printed. The detector's own self-test runs first, so a
# broken detector cannot read as a clean tree.
. "$(dirname "$0")/_root.sh"
H="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round3/checks/s13_shape.py"
st=$(python "$H" --self-test 2>&1 | tr -d '\r'); src=$?
out=$(python "$H" infra/aws/ec2/bd-exporter/ 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$st" "$out"
n=$(printf '%s\n' "$out" | sed -n 's/^non-empty BD_PASSWORD literals=\([0-9]*\)$/\1/p')
d=$(printf '%s\n' "$out" | sed -n 's/^DENOMINATOR: \([0-9]*\) .*/\1/p')
if [ "$src" = 0 ] && [ "$rc" = 0 ] && [ -n "$d" ] && [ "$d" -gt 0 ] && [ "$n" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
