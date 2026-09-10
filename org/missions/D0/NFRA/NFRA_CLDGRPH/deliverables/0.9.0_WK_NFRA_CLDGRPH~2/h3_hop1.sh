#!/usr/bin/env bash
# NFRA_CLDGRPH CG-s-38 / H3-AC3 -- hop 1 decided. The probe is python because two of its
# four arms EXECUTE something (the hand builder, and the buildspec's own extracted block);
# this wrapper exists so the criterion's invocation is the one the task order names.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/h3_hop1_probe.py
