#!/usr/bin/env bash
# F10-AC5 -- NFRA_CLDGRPH.TO-CG-F-10 / cell CG-s-30, 0.9.0_WK_NFRA_CLDGRPH~6.
# Thin bounded launcher; the measurement is f10_engine_untouched.py.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~6/f10_engine_untouched.py
RC=$?
echo "PY_RC=${RC}"
exit ${RC}
