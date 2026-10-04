#!/usr/bin/env bash
# OG-rl-5 PHASE B verify (step 5), written at Phase A, never run against a deploy by the Phase A worker.
# usage:  rl5_verify.sh before <state.json>
#         rl5_verify.sh after  <state.json> <40-hex deployed sha>
# `before` saves the host's BEFORE reads (MainPID, tool list, .env key NAMES; no value is ever read or stored) -- keep the state file OUT of
# the repository (e.g. <worktree>/.scratch/rl5_before.json). `after` (run IMMEDIATELY after safe-ec2-deploy.sh returns) runs the host checks,
# the AFTER run (paging pages, served census, asset held-check, download control) and writes RL5_PAGING.json beside this file, then runs
# the floor: rl4.AC1.sh and ht.AC2.sh. Any FAIL: roll back (ANNOUNCE_OG-rl-5.md), re-verify, close ROLLED BACK.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~15}"
case "$1" in
  before) python "$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/rl5_verify.py" || echo "$HERE/rl5_verify.py")" before "$2"; exit $? ;;
  after) ;;
  *) echo "usage: rl5_verify.sh before <state.json> | after <state.json> <deployed sha>"; exit 2 ;;
esac
[ -n "$3" ] || { echo "after needs the 40-hex deployed sha as the third argument"; exit 2; }
python "$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/rl5_verify.py" || echo "$HERE/rl5_verify.py")" after "$2" --served-release "$3"; rc=$?
ROOT="$(cd "$HERE" && git rev-parse --show-toplevel)"
cd "$ROOT" || exit 9
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
echo "--- rl4.AC1.sh ---"; out1=$(bash "$C/r14/checks/rl4.AC1.sh" 2>&1); rc1=$?; printf '%s\n' "$out1"
echo "--- ht.AC2.sh ---"; out2=$(bash "$C/hxteams/checks/ht.AC2.sh" 2>&1); rc2=$?; printf '%s\n' "$out2"
echo "rl5_verify: host + AFTER checks rc=$rc; rl4.AC1 rc=$rc1; ht.AC2 rc=$rc2"
[ "$rc" = 0 ] && [ "$rc1" = 0 ] && [ "$rc2" = 0 ]
