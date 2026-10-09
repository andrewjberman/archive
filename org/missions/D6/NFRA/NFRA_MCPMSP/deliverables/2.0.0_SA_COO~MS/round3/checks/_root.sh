#!/usr/bin/env bash
# _root.sh (round 3) -- reuse round 2's helpers (which source round 1's: cd to the worktree root, ssm_run, native, ...),
# then round-3 constants.
_R3_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$_R3_DIR/../../round2/checks/_root.sh"
# the deployed opal-gateway commit at the round-3 cut (infra/aws/ec2/EC2_MANIFEST.json services.opal-gateway.deployed_commit)
GW_DEPLOYED="aa75078e1b72a28219e6148d3ec8e9bf705ea111"
# the last commit to touch .tools/safe-apply.sh before round 3 (the base bytes MS-s-2's difference control runs)
SA_BASE="95d53e2068"
