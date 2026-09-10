#!/usr/bin/env bash
# NFRA_CLDGRPH CG-s-38 / H3-AC4 -- the egress hold, proven. The probe is python; this
# wrapper exists so the criterion's invocation is the one the task order names. Both files
# are excluded BY NAME from the probe's own corpus (they carry the patterns as literals).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/h3_no_apply.py
