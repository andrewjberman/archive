#!/usr/bin/env bash
# OPLGTW OG-bi-3 AC1 (round-28 ruling R46): the bun cache pre-check tests that each entry is COMPLETE, not only that
# its directory exists. Four named tests in tests/test_deploy_install_no_fetch_complete.py, none of which runs bun or
# opens a socket: (01) NEGATIVE CONTROL: an entry whose cache directory EXISTS AND IS EMPTY is reported missing and the
# pre-check exits non-zero; (02) an entry whose directory lacks the completeness mark the cell names (for example a
# package.json naming that package and version) is reported missing; (03) a cache of complete entries passes with
# `<n> of <n>`; (04) the real read: against the real lockfile and the real cache the result equals the first cell's
# count, or every entry now reported missing is named in the cell's record.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_deploy_install_no_fetch_complete.py test_ogbi3_ac01 test_ogbi3_ac02 test_ogbi3_ac03 test_ogbi3_ac04; r=$?
restore_audit
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
