#!/usr/bin/env bash
# OPLGTW OG-bi-1 AC1 (CTO ruling msg 31231, row Z-W28-S24): the gateway deploy's dashboard install FAILS on a cache miss
# and never fetches. Four named tests in tests/test_deploy_install_no_fetch.py, none of which runs bun or opens a socket:
# (01) against a cache holding every lockfile entry the pre-check passes and prints `<n> of <n>` entries present;
# (02) NEGATIVE CONTROL: with ONE lockfile entry absent from a COPY of the cache the pre-check exits non-zero, names
# the missing package and version, and the install command is never reached; (03) deploy-to-ec2.sh runs the pre-check
# BEFORE its install line on every branch that reaches the install; (04) the script's install line cannot run when
# the pre-check failed (the two are one guarded sequence, not two independent lines).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_deploy_install_no_fetch.py test_ogbi1_ac01 test_ogbi1_ac02 test_ogbi1_ac03 test_ogbi1_ac04; r=$?
restore_audit
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
