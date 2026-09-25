#!/usr/bin/env bash
# MX-b-2 AC1 (C-S15): the emitter's opening docstring paragraph (its first 4 lines at HEAD) names refs/DATA_CATALOG.yaml
# as what the script writes, and no longer names the staged file DATA_CATALOG.v0.2.staged.yaml.
. "$(dirname "$0")/_root.sh"
E="workflows/atom_decomposition/emit_catalog_v02.py"
h=$(git show "HEAD:$E" 2>/dev/null | tr -d '\r' | sed -n 1,4p)
[ -n "$h" ] || { echo "$E absent at HEAD"; echo "RESULT: FAIL"; exit 1; }
live=$(printf '%s\n' "$h" | grep -c 'refs/DATA_CATALOG\.yaml'); staged=$(printf '%s\n' "$h" | grep -c 'staged')
echo "emitter lines 1-4: names refs/DATA_CATALOG.yaml=$live; mentions the staged file=$staged"
if [ "$live" -ge 1 ] && [ "$staged" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
