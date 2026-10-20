#!/usr/bin/env bash
# OPLGTW OG-fc-1 AC3 (round 47): the worker's new test file tests/test_og_fc1.py passes and the existing client-surface tests that import client_core
# (the adapters' fixtures read firm_segments and the resolve merge) still pass.
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_fc1.py tests/test_og_cl1.py tests/test_og_cl2.py tests/test_og_cl3.py tests/test_og_cl4.py tests/test_og_cl6.py tests/test_og_cl7.py tests/test_og_ch1.py tests/test_og_en4.py tests/test_og_en13.py tests/test_og_en15.py tests/test_og_en17.py tests/test_og_en18.py tests/test_og_en19.py tests/test_og_en20.py tests/test_og_en21.py tests/test_og_en22.py tests/test_og_en24.py
rc=$?; restore_audit
exit $rc
