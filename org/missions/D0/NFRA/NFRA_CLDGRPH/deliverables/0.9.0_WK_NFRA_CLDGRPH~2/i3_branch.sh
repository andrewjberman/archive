#!/usr/bin/env bash
# I3-AC3 -- THE BRANCH IS STATED AND PROVEN.
#
# The cell offered two branches and both are passes; what cannot pass is a run that does
# not say which it took. This order took LICENCE_MOVED. The arms live in i3_branch_arms.py
# so the proof runs against the producer's OWN module and the pin's OWN drop expression
# rather than a transcript of either.
#
# ENVIRONMENT: local worktree only. No AWS call, no image act, no apply, no publish.
set -u
cd "$(dirname "$0")/../../../../../../.." || exit 1

echo "I3-AC3 -- BRANCH AND PROOF"
echo "  TREE  : $(pwd)"
echo "  BRANCH: $(git rev-parse --abbrev-ref HEAD)   HEAD: $(git rev-parse HEAD)"
echo "  FILE  : the branch's whole change is in infra/aws/globgrph/derive_stitch.py,"
echo "          measured against the ORDER'S BASE 4ff4abd9a4 --"
git diff --stat 4ff4abd9a4d6d2f60fd74fef32ce64158c6bd34b -- infra/aws/globgrph/derive_stitch.py | sed 's/^/          /'
echo ""

python "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/i3_branch_arms.py"
rc=$?
echo ""
echo "  ARMS_RC=${rc}"
exit ${rc}
