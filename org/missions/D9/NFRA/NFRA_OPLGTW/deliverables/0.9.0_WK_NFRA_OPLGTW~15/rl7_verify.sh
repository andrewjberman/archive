#!/usr/bin/env bash
# OG-rl-6 PHASE C (A1 steps 16 and 20) verify, extended from rl6_verify.sh, written at Phase C-A and never run against a deploy by the Phase C-A worker.
# usage:  rl7_verify.sh before <state.json>
#         rl7_verify.sh after  <state.json> <40-hex deployed sha>
# `before` saves the host's BEFORE reads (MainPID, tool list, .env key NAMES, the host-local /yearinreview code, the r17 download read on the live
# release); keep the state file OUT of the repository (<worktree>/.scratch/). `after` (run IMMEDIATELY after safe-ec2-deploy.sh returns) runs the host
# checks (md5 96 files, 65 tools, 50 env key names, /health 200), the host-local 401 and the public 302, the r17 download behaviour re-read (writes
# RL6_DOWNLOAD.json only on a full pass), then the floor: rl6.AC1.sh, rl4.AC1.sh and ht.AC2.sh. Any FAIL: roll back (ANNOUNCE_OG-rl-6-C.md), re-verify,
# close ROLLED BACK.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~15}"
PY="$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/rl7_verify.py" || echo "$HERE/rl7_verify.py")"
case "$1" in
  before) python "$PY" before "$2"; exit $? ;;
  after) ;;
  *) echo "usage: rl7_verify.sh before <state.json> | after <state.json> <deployed sha>"; exit 2 ;;
esac
[ -n "$3" ] || { echo "after needs the 40-hex deployed sha as the third argument"; exit 2; }
python "$PY" after "$2" --served-release "$3"; rc=$?
ROOT="$(cd "$HERE" && git rev-parse --show-toplevel)"
cd "$ROOT" || exit 9
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
echo "--- rl6.AC1.sh ---"; out0=$(bash "$C/r17/checks/rl6.AC1.sh" 2>&1); rc0=$?; printf '%s\n' "$out0"
echo "--- rl4.AC1.sh ---"; out1=$(bash "$C/r14/checks/rl4.AC1.sh" 2>&1); rc1=$?; printf '%s\n' "$out1"
echo "--- ht.AC2.sh ---"; out2=$(bash "$C/hxteams/checks/ht.AC2.sh" 2>&1); rc2=$?; printf '%s\n' "$out2"
echo "rl7_verify: host + AFTER checks rc=$rc; rl6.AC1 rc=$rc0; rl4.AC1 rc=$rc1; ht.AC2 rc=$rc2"
[ "$rc" = 0 ] && [ "$rc0" = 0 ] && [ "$rc1" = 0 ] && [ "$rc2" = 0 ]
