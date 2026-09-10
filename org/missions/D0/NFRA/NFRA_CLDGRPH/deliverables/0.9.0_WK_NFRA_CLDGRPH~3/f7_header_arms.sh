#!/usr/bin/env bash
# TO-CG-F-7 / CG-s-27 -- F7-AC3: the rendered header, five arms, on real renders.
# Run from the worktree ROOT: bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_header_arms.sh
# Bounded by the caller (timeout 120). Python 3.12 is put first on PATH here because a bare
# `python` on this box resolves to 3.14 without the workspace's packages.
set -u
export PATH="/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312:$PATH"

if [ ! -d "infra/aws/globgrph" ]; then
  echo "ERROR: run from the worktree root (infra/aws/globgrph not found here: $(pwd))"
  exit 2
fi

python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_header_arms.py
rc=$?
echo "F7_HEADER_ARMS_RC=${rc}"
exit "${rc}"
