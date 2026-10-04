#!/usr/bin/env bash
# AMGT_CORPUS round 35, CRPS-ak-2 (round-34 analysis ruling 1, row Z-S85) -- schedule_induction.ps1 names its interpreter
# explicitly and refuses one that cannot import blpapi. Plan-only: it never runs -Register. The issuer's file.
#   b1 (the plant): with THIS session's PATH (Python314 first, no blpapi), `-Plan -Commit HEAD` prints an arguments line naming
#      ...\Python311\python.exe.
#   b2: `-Plan -Commit HEAD -Python "C:\Program Files\Python314\python.exe"` exits non-zero and prints a REFUSED line naming
#      blpapi.
#   -> lines `AK2 b1 PASS|FAIL ...`, `AK2 b2 PASS|FAIL ...`, then `ak2 build <n>/2`
set -u
TOP=$(git rev-parse --show-toplevel) || { echo "ak2 build 0/2 (no repo)"; exit 1; }
PS1W="$(cygpath -w "$TOP/lib/research/corpus/schedule_induction.ps1" 2>/dev/null || echo "$TOP/lib/research/corpus/schedule_induction.ps1")"
n=0
OUT1=$(timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$PS1W" -Plan -Commit HEAD 2>&1 | tr -d '\r')
ARGS1=$(printf '%s\n' "$OUT1" | grep -E '^PLAN arguments' | head -1)
if printf '%s' "$ARGS1" | grep -q 'Python311\\python.exe'; then echo "AK2 b1 PASS [$ARGS1]"; n=$((n+1)); else echo "AK2 b1 FAIL [${ARGS1:-no PLAN arguments line}]"; fi
OUT2=$(set -o pipefail; timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$PS1W" -Plan -Commit HEAD -Python "C:\\Program Files\\Python314\\python.exe" 2>&1 | tr -d '\r'); RC2=$?
REF2=$(printf '%s\n' "$OUT2" | grep -E 'REFUSED' | grep -i 'blpapi' | head -1)
if [ "$RC2" -ne 0 ] && [ -n "$REF2" ]; then echo "AK2 b2 PASS rc=$RC2 [$REF2]"; n=$((n+1)); else echo "AK2 b2 FAIL rc=$RC2 [$(printf '%s\n' "$OUT2" | tail -1)]"; fi
echo "ak2 build $n/2"
