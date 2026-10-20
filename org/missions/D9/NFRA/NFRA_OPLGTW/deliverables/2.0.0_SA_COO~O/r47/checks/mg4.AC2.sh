#!/usr/bin/env bash
# OPLGTW OG-mg-4 AC2: the guard's own tests pass at the new cap (tests/test_og_mg3.py) and so do the neighbours that import app.tools (tests/test_og_tp1.py, tests/test_og_fc1.py).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_mg3.py tests/test_og_tp1.py tests/test_og_fc1.py
rc=$?
restore_audit
exit $rc
