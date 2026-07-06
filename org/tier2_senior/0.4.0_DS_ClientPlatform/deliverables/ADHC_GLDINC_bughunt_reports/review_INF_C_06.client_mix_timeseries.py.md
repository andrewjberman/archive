# REVIEW -- INF_C_06.client_mix_timeseries.py

- script: `data/inf/scripts/gold/INF_C_06.client_mix_timeseries.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 1

## Finding 1 -- [low/empty-null-handling/full]
- **Location:** `data/inf/scripts/gold/INF_C_06.client_mix_timeseries.py:149 (guard at :86, dropna at :92)`
- **Mechanism:** The emptiness guard `if cp is None or cp.empty: return 0` (line 86) executes BEFORE `cp = cp.dropna(subset=['date'])` (line 92). If the loaded parquet is non-empty but EVERY value in the 'date' column is unparseable, `pd.to_datetime(errors='coerce')` turns them all to NaT and the dropna empties `cp` AFTER the guard has already passed. `firm_ts` is then an empty DataFrame, and line 149 `data_as_of = firm_ts['date'].max().strftime('%Y-%m-%d')` calls `.max()` on an empty datetime series, yielding NaT. `pd.NaT` is not JSON-serializable, so `json.dumps(output)` at line 162 raises TypeError, which propagates to the top-level `except` (line 175) -> sys.exit(1) -> the no-timeout gold chain HARD-ABORTS. (In pandas builds where NaT.strftime returns the string 'NaT' instead, no crash occurs but a degenerate artifact is served: empty firm_timeseries/advisor_timeseries with data_as_of='NaT'.)
- **Failure scenario:** INF_C_02 (or a future refactor) writes client_performance.parquet with a non-empty but fully-corrupt/unparseable 'date' column (e.g. all dates written as an unexpected string format, or all NaT). C_06 passes the line-86 non-empty check, then dropna empties the frame, then line 149 does `.max().strftime()` on the empty frame -> NaT -> json.dumps TypeError -> uncaught -> sys.exit(1) aborts the entire full gold chain (all downstream INF_C_07..INF_D_* never run). Under the current strong C_02 datetime64 contract this trigger is unlikely, which is why severity is low; the defect is that the emptiness guard is placed on the wrong side of the NaT-drop.
- **Proposed fix:** Re-check emptiness after the date coercion/dropna: insert `if cp.empty: log('WARN: no valid dates after NaT-drop'); return 0` immediately after line 92, and/or guard line 149 (`mx = firm_ts['date'].max(); data_as_of = mx.strftime('%Y-%m-%d') if pd.notna(mx) else None`).
