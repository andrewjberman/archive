# SERVED-MOVE measured record -- ADVI_COTBKF round 96, CB-cr-1 (worker 0.9.0_WK_ADVI_COTBKF~186)

Counts only. The JSON beside this file (`SERVED_MOVE_MEASURED_RECORD.json`) carries the same figures.

**SERVED-MOVE measured=True equal_tables=3 of 3 added_columns=porting_verdict,use_class**

- Received run data: 20,563 files, 4,478,568,892 bytes (matches the manager's report).
- Local build at the served settings (method_r28, as_traded, three hold CUSIPs, policy interim); the builder's own
  re-derivation checks passed: 1,691,729 day values and 82,593 month grades reproduced.
- Control against the three served objects (one get each, VersionId and LastModified in the JSON):

| table | served rows | built rows | rows differing | max abs diff | pre-existing equal |
|---|---|---|---|---|---|
| daily_returns | 1,691,729 | 1,691,729 | 0 | 0.0 | True |
| account_day_value | 21,102,041 | 21,102,041 | 0 | 0.0 | True |
| month_grades | 82,593 | 82,593 | 0 | 0.0 | True |

- `run_commit`: served 6f70d5cc01bb (every row), built 923f06e998ec (every row). Excluded from the control.
- Added columns in the build, both tables' worth of labels: `use_class` and `porting_verdict` only. Every row of every table reads
  NOT_YAHOO. Accounts with a NOT_FOR_ACTIVE row: 0.
- Finding: the served and built `price_source` carry no yahoo_finance or linear_interpolation value, so no served day is
  Yahoo-priced and the label cannot separate any. Channel row ADVI_COTBKF-D1-W186-S1.
- Not established: see the `not_established` list in the JSON (no pins in the run; current-version reads only; count-and-bytes
  receipt, not a per-file hash; build at HEAD 923f06e998, not the served commit).
