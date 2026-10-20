#!/usr/bin/env bash
# OPLGTW OG-sk-2 AC2: the worker's new tests (tests/test_og_sk2.py, at least 6) pass, and so do the four Schwab neighbours that read the contract and the catalog
# (tests/test_schwab_catalog.py, tests/test_og_ms1.py, tests/test_og_cd1.py, tests/test_schwab_transactions.py; every one passes at the base).
# NOT a neighbour: tests/acceptance/test_local_acceptance.py::test_ogv2_a12 already FAILS at the base (a carried red, not this cell's).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_sk2.py tests/test_schwab_catalog.py tests/test_og_ms1.py tests/test_og_cd1.py tests/test_schwab_transactions.py
rc=$?
restore_audit
exit $rc
