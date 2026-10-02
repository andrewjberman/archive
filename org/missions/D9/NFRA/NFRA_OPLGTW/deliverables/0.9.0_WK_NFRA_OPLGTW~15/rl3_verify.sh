#!/usr/bin/env bash
# OG-rl-3 PHASE B verify (row Z-W15-S24): usage  rl3_verify.sh before|after <state.json>
# `before` saves the host's BEFORE reads (run before the act). `after` runs the host reads and every comparison (rl3_verify.py), then
# ht.AC2.sh, ht.AC3.sh and ht.AC4.sh. Run `after` IMMEDIATELY after safe-ec2-deploy.sh returns.
# Any host-check FAIL, any AC2 FAIL, any AC3 FAIL other than GRAPH-SCOPE-MISSING, or an AC4 arm 1 or 2 FAIL: roll back, re-verify, close ROLLED BACK.
# GRAPH-SCOPE-MISSING (502, graph_status 403): do NOT roll back; file a BLOCKING row (disarm_owner 2.0.0_SA_COO~O) and report at once.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~15}"
python "$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/rl3_verify.py" || echo "$HERE/rl3_verify.py")" "$1" "$2"; rc=$?
[ "$1" = "after" ] || exit $rc
C="$HERE/../2.0.0_SA_COO~O/hxteams/checks"
echo "--- ht.AC2.sh ---"; out2=$(bash "$C/ht.AC2.sh" 2>&1); rc2=$?; printf '%s\n' "$out2"
echo "--- ht.AC3.sh ---"; out3=$(bash "$C/ht.AC3.sh" 2>&1); rc3=$?; printf '%s\n' "$out3"
echo "--- ht.AC4.sh (arms 1-2 are the post-deploy arms) ---"; out4=$(bash "$C/ht.AC4.sh" 2>&1); printf '%s\n' "$out4"
a1=$(printf '%s\n' "$out4" | grep -c '^arm 1 .*: OK$'); a2=$(printf '%s\n' "$out4" | grep -c '^arm 2 .*: OK$')
gs=$(printf '%s\n' "$out3" | grep -c 'GRAPH-SCOPE-MISSING')
echo "rl3_verify: host checks rc=$rc; AC2 rc=$rc2; AC3 rc=$rc3 (graph-scope-missing lines $gs); AC4 arm1 ok=$a1 arm2 ok=$a2"
[ "$gs" -gt 0 ] && echo "GRAPH-SCOPE-MISSING: do NOT roll back; BLOCKING row + report at once"
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && { [ "$rc3" = 0 ] || [ "$gs" -gt 0 ]; } && [ "$a1" = 1 ] && [ "$a2" = 1 ]
