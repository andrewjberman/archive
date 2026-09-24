#!/usr/bin/env bash
# OA-w-1 AC2 (seam, REAL neighbour = the GitHub remote): the mapping initialises opal_ai from the remote at the gitlink.
. "$(dirname "$0")/_root.sh"
out=$(timeout 100 git submodule update --init opal_ai 2>&1); rc=$?
h=$(git -C opal_ai rev-parse HEAD 2>/dev/null || echo NONE)
top=$(git -C opal_ai rev-parse --show-toplevel 2>/dev/null || echo NONE)
echo "submodule update rc=$rc; opal_ai HEAD=$h; opal_ai toplevel=$top"
[ "$rc" = 0 ] || echo "$out" | tail -3
if [ "$rc" = 0 ] && [ "$h" = "90ca424fc7551019cc493847637258adf3c1c4b5" ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
