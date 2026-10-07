#!/usr/bin/env bash
# OPLGTW OG-bi-2 AC1 (CTO ruling msg 31243): the gateway deploy's HOST step no longer upgrades pip. Three named tests in
# tests/test_deploy_host_pip_no_upgrade.py, each a read of deploy-to-ec2.sh's text (nothing is run): (01) no line of the
# script runs pip with `--upgrade` or `-U` naming pip itself; (02) the `pip install --progress-bar off -r requirements.txt`
# line is still there, exactly once, unchanged; (03) NEGATIVE CONTROL: the same reader, given the script's text at the
# commit before this cell, finds the upgrade line (so the reader can see what it claims is gone).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_deploy_host_pip_no_upgrade.py test_ogbi2_ac01 test_ogbi2_ac02 test_ogbi2_ac03; r=$?
restore_audit
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
