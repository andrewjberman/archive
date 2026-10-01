#!/usr/bin/env bash
# OG-tr-1 PHASE B verify (row NFRA_OPLGTW-Z-W15-S18): usage  tr_verify.sh before|after <state.json>
# `before` saves the host's BEFORE reads; `after` runs the AFTER reads, every comparison, and then tr.AC1.sh (the served arms).
# Run `after` IMMEDIATELY after safe-ec2-deploy.sh returns. Any FAIL: roll back, re-verify, close ROLLED BACK.
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPAL_AGENT_SERIAL="${OPAL_AGENT_SERIAL:-0.9.0_WK_NFRA_OPLGTW~15}"
python "$(command -v cygpath >/dev/null 2>&1 && cygpath -w "$HERE/tr_verify.py" || echo "$HERE/tr_verify.py")" "$1" "$2"; rc=$?
[ "$1" = "after" ] || exit $rc
echo "--- tr.AC1.sh ---"
bash "$HERE/../2.0.0_SA_COO~O/trnspt/checks/tr.AC1.sh"; rc2=$?
echo "tr_verify: host checks rc=$rc, tr.AC1 rc=$rc2"
[ "$rc" = 0 ] && [ "$rc2" = 0 ]
