#!/usr/bin/env bash
# OG-rl-13 PHASE B verify (form step 6 / 11), written at Phase A, never run against a deploy by the Phase A worker.
# usage:  r27_verify.sh before <state.json>
#         r27_verify.sh after  <state.json> <40-hex deployed sha>
# `before` saves the host's BEFORE reads (also the route neighbour pages' values; MainPID, tool list, .env key NAMES and per-key value sha256 digests; no value is ever read as text or stored) on the installed live code --
# keep the state file OUT of the repository (e.g. <worktree>/.scratch/r27_before.json). `after` (run IMMEDIATELY after safe-ec2-deploy.sh returns) runs the host checks (health, shipped md5 (3 files differ from live), tool list unchanged at 66, the four ROUTE arms (chart_404, chart_400, day_page_unchanged, audit_page_unchanged),
# .env names and value digests), then the floor: rl4.AC1.sh (51-name baseline r17/ENV_KEYS_R17B.txt)
# and ht.AC2.sh (51 keys). The post-deploy reads (RL13_ALLOW / RL13_FLOOR) are r27_postdeploy.sh, run right after. Any FAIL: roll back (ANNOUNCE_OG-rl-13.md), re-verify, close ROLLED BACK.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~28}"
PYF="$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/r27_verify.py" || echo "$HERE/r27_verify.py")"
case "$1" in
  before) python "$PYF" before "$2"; exit $? ;;
  after) ;;
  *) echo "usage: r27_verify.sh before <state.json> | after <state.json> <deployed sha>"; exit 2 ;;
esac
[ -n "$3" ] || { echo "after needs the 40-hex deployed sha as the third argument"; exit 2; }
python "$PYF" after "$2" --served-release "$3"; rc=$?
ROOT="$(cd "$HERE" && git rev-parse --show-toplevel)"
cd "$ROOT" || exit 9
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
echo "--- rl4.AC1.sh (baseline r17/ENV_KEYS_R17B.txt) ---"; out1=$(RL4_ENV_KEYS_BASELINE="$C/r17/ENV_KEYS_R17B.txt" bash "$C/r14/checks/rl4.AC1.sh" 2>&1); rc1=$?; printf '%s\n' "$out1"
echo "--- ht.AC2.sh (51 keys) ---"; out2=$(HT_ENV_KEYS_COUNT=51 bash "$C/hxteams/checks/ht.AC2.sh" 2>&1); rc2=$?; printf '%s\n' "$out2"
echo "r27_verify: host + AFTER checks rc=$rc; rl4.AC1 rc=$rc1; ht.AC2 rc=$rc2"
[ "$rc" = 0 ] && [ "$rc1" = 0 ] && [ "$rc2" = 0 ]
