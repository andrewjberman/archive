#!/usr/bin/env bash
# _pin.sh -- sourced AFTER _root.sh by a round-2 re-cut check that must run FILES of the nested move (OA-t-3's gate and
# fence). It materialises opal_ai at $OA_NESTED_PIN in a throwaway DETACHED worktree ($PT) and removes it on exit.
# The pin, never the nested HEAD: round 2's E2 and E7 edit moved files after the move by design (decomposition R2.3).
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent at $(pwd)/opal_ai"; echo "RESULT: FAIL"; exit 1; }
git -C opal_ai cat-file -e "${OA_NESTED_PIN}^{commit}" 2>/dev/null \
  || { echo "opal_ai pin $OA_NESTED_PIN unresolved (run: git -C opal_ai fetch origin)"; echo "RESULT: FAIL"; exit 1; }
# NOT under TMPDIR/TEMP/TMP: the fence allowlists those roots for writes, so a pin materialised there would make
# t3.AC3's "edit own prompt -> DENY" arm pass through the tmp allowance and read as a fence defect.
PT="${HOME:?HOME unset}/.oa_pin_$$"
_pin_cleanup() { git -C opal_ai worktree remove --force "$PT" >/dev/null 2>&1; rm -rf "$PT"; git -C opal_ai worktree prune >/dev/null 2>&1; }
trap _pin_cleanup EXIT
git -C opal_ai worktree add -q --detach "$PT" "$OA_NESTED_PIN" >/dev/null 2>&1 \
  || { echo "cannot materialise opal_ai@$OA_NESTED_PIN at $PT"; echo "RESULT: FAIL"; exit 1; }
