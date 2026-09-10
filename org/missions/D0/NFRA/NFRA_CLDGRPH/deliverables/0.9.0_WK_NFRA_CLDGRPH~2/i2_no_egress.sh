#!/usr/bin/env bash
# I2-AC4 -- the egress hold honoured, and no number invented.
#
# THREE ARMS, and only the first is a claim about MY acts:
#   1. the git-side write surface: what this order actually changed, from git itself
#   2. the detector: the five held act families counted over everything this order wrote,
#      with a PROBE that must light up every family (a detector that cannot go non-zero
#      is a constant wearing a measurement's clothes)
#   3. the magnitude assertion: every magnitude claim in this order's captures is
#      UNMEASURED, never a manufactured number
set -u
cd "$(dirname "$0")/../../../../../../.." || exit 1

echo "I2-AC4 -- THE EGRESS HOLD, MEASURED"
echo "  TREE        : $(pwd) (branch $(git rev-parse --abbrev-ref HEAD), HEAD $(git rev-parse HEAD))"
echo "  ENVIRONMENT : local worktree only; no AWS call of any kind was made by this order's"
echo "                harnesses -- the producer's three input loaders are replaced with"
echo "                fixtures before build_stitched_graph() runs, so load_aws_layer() (the"
echo "                only S3 read in the producer) is never called"
echo "  GRAIN       : STATIC over authored bytes + git's own diff. It cannot see an act that"
echo "                left no trace in either; the probe states what the detector CAN see."
echo ""
echo "  ARM 1 -- GIT-SIDE WRITE SURFACE (tracked files this order changed):"
git diff --stat -- infra/aws/globgrph/derive_stitch.py | sed 's/^/    /'
echo "    (untracked, this order's deliverables:)"
git status --porcelain -- "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/" | sed 's/^/    /'
echo ""
echo "  ARM 2+3 -- DETECTOR AND PROBE:"
python "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/i2_no_egress_scan.py"
rc=$?
echo ""
echo "  SCAN_RC=${rc}"
exit ${rc}
