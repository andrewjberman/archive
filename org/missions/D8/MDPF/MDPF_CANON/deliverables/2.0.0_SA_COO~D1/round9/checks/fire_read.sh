#!/usr/bin/env bash
# MDPF_CANON round 9 -- the first-fire readback in ONE command (2.0.0_SA_COO~D1; read-only, writes nothing to AWS).
#
#   bash fire_read.sh gold        after the 2026-10-15 13:30Z gold fire (read from 13:40Z): the three acceptance reads of the
#                                 round-7 pair (CN-h-1 frontier counts, CN-l-1 Other Models row) and the round-9 pair (CN-p-1 Trend groups)
#   bash fire_read.sh publisher   after the 13:50Z publisher fire (read from 14:00Z): the CN-j-1 history leaf (H9)
#
# Every tool prints its own verdict line; this wrapper prints the command, the tool's last two lines and its exit code, and
# never converts a failing exit into a pass. The pin is the CN-p-1 deploy pin read by the R9 arm (run.code.commit).
set -u
ROOT="$(git rev-parse --show-toplevel)" || { echo "ERROR: not in a git work tree"; exit 2; }
R7="$ROOT/org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks"
R9="$ROOT/org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round9/checks"
PIN="8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f"
rc_all=0
run() {
  local label="$1"; shift
  echo "== $label"
  echo "   \$ $*"
  out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" | tail -n 2 | sed 's/^/   /'
  echo "   exit=$rc"
  [ "$rc" -eq 0 ] || rc_all=1
}
case "${1:-}" in
  gold)
    run "CN-h-1 frontier counts (arms F1-F6)" python "$R7/r7_frontier_readback.py" read
    run "CN-l-1 Other Models row (6 of 6)"     python "$R7/r7_cn_l_1.py" real
    run "CN-p-1 Trend groups (R1-R11, R9 = the manifest, commit must equal the pin)" python "$R9/r9_trend_groups_readback.py" read --pin "$PIN"
    ;;
  publisher)
    run "CN-j-1 history leaf (H9)" python "$R7/r7_history_readback.py" read
    ;;
  *)
    echo "usage: bash fire_read.sh gold|publisher"; exit 2 ;;
esac
echo "FIRE-READ $1: $([ "$rc_all" -eq 0 ] && echo 'every tool exited 0' || echo 'AT LEAST ONE TOOL EXITED NON-ZERO (read its lines above)')"
exit "$rc_all"
