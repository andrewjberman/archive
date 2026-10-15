# USE_CLASS_SERVE_RECORD (CB-ck-1, 0.9.0_WK_ADVI_COTBKF~178)

- Module: `data/assets/scripts/silver/commonwealth_fwd3_serve.py` at commit `4fe97022a6`, blob `e239f460fb8bd24797ec357ba0f33375f81c5fc8`.
- Label: `use_class` added immediately before `porting_verdict` in `daily_returns`, `account_day_value` and `month_grades`. `porting_verdict` stays the last column (AMENDMENT 1).
- Switch: `--yahoo-active-policy {interim,blank}`, default `interim`. `interim` moves no value. `blank` holds every NOT_FOR_ACTIVE Yahoo-priced CUSIP and is local only; `--apply` refuses it (call 3adb).
- Tests: eight new `use_class` tests in `test_commonwealth_fwd3_serve_use_class.py`; one porting_verdict byte-equal control appended to `test_commonwealth_fwd3_serve.py` (15 added lines, 0 removed).
- Real run: NO_DATA_DIR (no default run data on this box).
- S3 writes: 0. No account number, name or dollar value in this record.
- Not established: the real-data interim comparison, the live index's use_class column, the served effect, the account-id scan (fails closed here). See the JSON `not_established` list.
