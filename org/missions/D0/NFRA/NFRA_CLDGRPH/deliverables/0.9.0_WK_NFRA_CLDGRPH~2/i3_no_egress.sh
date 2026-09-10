#!/usr/bin/env bash
# I3-AC4 -- the egress hold honoured AND the retirement not snuck in.
#
# THREE ARMS, and only the first is a claim about MY acts:
#   1. the git-side write surface: what this order actually changed, from git itself
#   2. the detector: the five held act families counted over everything this order wrote,
#      with a PROBE that must light up every family
#   3. the retirement tells: four properties of the worktree bytes that would each go the
#      other way if this cell had performed the retirement instead of making it available
set -u
cd "$(dirname "$0")/../../../../../../.." || exit 1

echo "I3-AC4 -- THE EGRESS HOLD AND THE UNPERFORMED RETIREMENT, MEASURED"
echo "  TREE        : $(pwd) (branch $(git rev-parse --abbrev-ref HEAD), HEAD $(git rev-parse HEAD))"
echo "  ENVIRONMENT : local worktree. This order made READ-ONLY AWS calls (an object listing"
echo "                and six object reads under producers/) and no other AWS call of any"
echo "                kind; they are disclosed by name at the end of the detector output."
echo "  GRAIN       : STATIC over authored bytes + git's own diff. It cannot see an act that"
echo "                left no trace in either; the probe states what the detector CAN see."
echo ""
echo "  ARM 1 -- GIT-SIDE WRITE SURFACE (tracked files this order changed):"
git diff --stat -- infra/aws/globgrph/derive_stitch.py | sed 's/^/    /'
echo "    (the other production file this cell READ, and did not touch:)"
git diff --stat -- infra/aws/globgrph/derive_runner.py | sed 's/^/    /'
echo "    (untracked, this order's deliverables:)"
git status --porcelain -- "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/" | sed 's/^/    /'
echo ""
echo "  ARM 2+3 -- DETECTOR, PROBE AND RETIREMENT TELLS:"
python "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/i3_no_egress_scan.py"
rc=$?
echo ""
echo "  SCAN_RC=${rc}"
exit ${rc}
