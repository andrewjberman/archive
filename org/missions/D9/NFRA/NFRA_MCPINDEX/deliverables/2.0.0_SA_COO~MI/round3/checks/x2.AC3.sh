#!/usr/bin/env bash
# MX-x-2 AC3 (the catalog is never hand-edited): re-running the emitter reproduces the committed DATA_CATALOG.yaml,
# except the two build-stamp lines it always rewrites. The emitter writes IN PLACE and takes no arguments, so this check
# backs the file up first and restores those exact bytes after, whatever happens.
. "$(dirname "$0")/_root.sh"
C="$GW/app/refs/DATA_CATALOG.yaml"
B="${TMPDIR:-/tmp}/x2ac3_$$.yaml"
cp -p "$C" "$B" || { echo "cannot back up $C"; echo "RESULT: FAIL"; exit 1; }
trap 'cp -p "$B" "$C"; rm -f "$B"' EXIT
emit=$( (cd workflows/atom_decomposition && timeout 300 python emit_catalog_v02.py) 2>&1 | tr -d '\r'); erc=$?
d=$(diff <(grep -vE '^(# BUILT BY: |built_at_git_head: )' "$B") <(grep -vE '^(# BUILT BY: |built_at_git_head: )' "$C") | grep -cE '^[<>]')
echo "emitter rc=$erc; differing lines outside the build stamp: $d"
if [ "$erc" = 0 ] && [ "$d" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
