#!/usr/bin/env bash
# F10-AC3 -- NFRA_CLDGRPH.TO-CG-F-10 / cell CG-s-30, 0.9.0_WK_NFRA_CLDGRPH~6.
# Thin bounded launcher; the measurement is f10_regen.py (F-8 f8_regen_idempotent.sh reused).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
timeout 240 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~6/f10_regen.py
RC=$?
echo "PY_RC=${RC}"
exit ${RC}
