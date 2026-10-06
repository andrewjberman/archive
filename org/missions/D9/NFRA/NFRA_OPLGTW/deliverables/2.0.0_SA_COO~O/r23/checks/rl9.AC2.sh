#!/usr/bin/env bash
# OPLGTW OG-rl-9 AC2 (R30.3): the post-release read is ga1.AC2, run UNAMENDED -- this wrapper only invokes it.
exec bash "$(dirname "$0")/../../r22/checks/ga1.AC2.sh"
