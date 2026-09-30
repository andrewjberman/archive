#!/usr/bin/env bash
# MX-s-15 AC2: tests/test_schwab_transactions.py exits 0 and its 4 named tests pass.
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_schwab_transactions.py test_mx_s15_dataset_registered test_mx_s15_grain_declared test_mx_s15_entitled_like_dims test_mx_s15_reads_one_master_one_date
rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
