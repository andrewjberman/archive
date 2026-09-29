#!/usr/bin/env bash
# OA-e-7 AC2 (built, row Z-S20 / R-4): opal_ai's own gate passes standalone AND reports ruff's REAL finding count.
# The nested repo at ${OA_NESTED_REF:-HEAD} is exported to a scratch dir (a standalone copy, no workspace), and
#   run 1: `bash opal/checks/run_checks.sh` must end `CHECKS: PASS`;
#   run 2 (difference control): with one planted unused import (opal/zz_planted_ruff.py), its ruff line must read
#          `ruff: FAIL (N findings)` with N >= 1 and N equal to ruff's OWN count of the same copy (concise format).
# Both runs have colour OFF (NO_COLOR=1, FORCE_COLOR/CLICOLOR_FORCE unset): this shell forces ANSI colour into piped
# ruff output, which would make any line-anchored count read 0 whatever the gate does.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
unset FORCE_COLOR CLICOLOR_FORCE; export NO_COLOR=1
# The pinned ruff (the version the CI installs, ci.yml ruff==0.16.9) runs FIRST on PATH, so the gate and the own-count
# grade what CI grades; the box's own ruff 0.15.11 finds nothing and hid Z-S20 here.
export PATH="/c/tmp/ruff-0.16.9/bin:$PATH"
rv=$(ruff --version 2>/dev/null | tr -d '')
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/e7ac2_$$")"; mkdir -p "$T"
git -C opal_ai archive "$REF" | tar -x -C "$T" 2>/dev/null
if [ ! -f "$T/opal/checks/run_checks.sh" ]; then echo "run_checks.sh absent at opal_ai $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; fi
r1=$(cd "$T" && timeout 50 bash opal/checks/run_checks.sh 2>&1 | tr -d '\r' | tail -1)
printf 'import os\n' > "$T/opal/zz_planted_ruff.py"
r2=$(cd "$T" && timeout 50 bash opal/checks/run_checks.sh 2>&1 | tr -d '\r' | grep -m1 '^ruff:')
own=$(cd "$T" && timeout 30 ruff check --target-version py39 --output-format concise opal 2>/dev/null | tr -d '\r' | grep -cE '^opal[/\\][^:]+:[0-9]+:[0-9]+: ')
rm -rf "$T"
n=$(printf '%s' "$r2" | sed -n 's/^ruff: FAIL (\([0-9][0-9]*\) findings).*/\1/p')
echo "[$rv] opal_ai $REF: clean run last line='$r1'; planted run '${r2%% -- *}'; reported=${n:-none} ruff-own=$own"
if [ "$rv" = "ruff 0.16.9" ] && [ "$r1" = "CHECKS: PASS" ] && [ -n "$n" ] && [ "$n" -ge 1 ] && [ "$n" = "$own" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
