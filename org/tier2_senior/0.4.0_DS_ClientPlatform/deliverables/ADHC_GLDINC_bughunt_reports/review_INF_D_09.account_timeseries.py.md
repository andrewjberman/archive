# REVIEW -- INF_D_09.account_timeseries.py

- script: `data/inf/scripts/gold/INF_D_09.account_timeseries.py`
- verdict: **issues-found**
- runs_in_incremental: True
- findings: 4

## Finding 1 -- [medium/unguarded-read/both]
- **Location:** `data/inf/scripts/gold/INF_D_09.account_timeseries.py:149 (load_account_performance)`
- **Mechanism:** s3.get_object(Key=ACCOUNT_PERF_KEY='gold/timeseries/account_performance.parquet') at line 149 has NO NoSuchKey guard, unlike _load_anchor_cache (125-133) which catches it. On an absent key it raises ClientError -> only the top-level except at 348 catches it -> sys.exit(1) -> hard-fails the no-timeout gold chain. The intended 'run INF_C_03 first' safety net at 326-328 (`if df.empty: return 1`) is UNREACHABLE for a missing key, because get_object raises before df is ever created; that guard only fires for a present-but-empty parquet. Exposure is highest in CHAIN_INCREMENTAL: D_09 IS in CHAIN_INCREMENTAL (dispatch line 340) but its producer INF_C_03 is NOT, so nothing recreates the parquet in the incremental path.
- **Failure scenario:** account_performance.parquet has never been produced (first environment bring-up) or was deleted/rotated, and an incremental (or full) chain runs -> get_object raises NoSuchKey -> sys.exit(1) -> chain aborts. In full mode this also strands the 7 downstream scripts that follow D_09 in CHAIN_COMPUTE (INF_D_05/D_06/D_07/D_07a/D_08/D_05a/D_06a).
- **Proposed fix:** Wrap the get_object/read_parquet in try/except mirroring _load_anchor_cache: on a NoSuchKey/ClientError, log 'ERROR: account_performance missing -- run INF_C_03 first' and return an empty DataFrame so the empty-guard at 326 produces a controlled exit (or a SKIP), rather than an uncaught crash.

## Finding 2 -- [medium/empty-null-handling/both]
- **Location:** `data/inf/scripts/gold/INF_D_09.account_timeseries.py:155 (household_id-only notna filter) + :157 (account_id astype) + :259 (int(account_id))`
- **Mechanism:** account_id in account_performance.parquet is nullable Int64 (INF_C_03 line 272 calls coerce_id_columns, which does pd.to_numeric(errors='coerce').astype('Int64') -> a non-numeric account_id becomes <NA>). D_09 line 155 filters ONLY household_id.notna(), never account_id. Line 156 defensively casts household_id via .astype(int).astype(str) (int-first), but line 157 casts account_id with a bare .astype(str).str.strip(). A <NA> account_id therefore renders as the literal string '<NA>' (verified), becomes a groupby key, and if that group is not all-zero it reaches line 259 int(account_id)=int('<NA>') which raises ValueError (verified) inside _publish_one -> re-raised by f.result() at 274 -> uncaught in publish_account_timeseries/main -> sys.exit(1) -> chain abort. The int-first defense the author applied to household_id was NOT applied to account_id (asymmetry).
- **Failure scenario:** A canonical_performance row carries a non-numeric/garbage account_id AND a valid household_id sourced directly from the perf partition (so the acct_dim merge-miss does not null household_id). coerce -> account_id=<NA>; the row survives the household_id-only 155 filter; nonzero total_aua -> account not skipped at 251; int('<NA>') at 259 -> ValueError -> whole chain aborts.
- **Proposed fix:** Filter account_id notna alongside household_id at line 155 (e.g. df = df[df['account_id'].notna() & df['household_id'].notna()]), OR give account_id the same int-first treatment and guard int(account_id) at 259.

## Finding 3 -- [low/empty-null-handling/both]
- **Location:** `data/inf/scripts/gold/INF_D_09.account_timeseries.py:220 (publish_account_timeseries) via _build_quarters (:79-97)`
- **Mechanism:** If df['date'].max() precedes DATASET_FLOOR_QUARTER (2020Q2), _build_quarters returns [] because start_q is floored to 2020Q2 while end_q < 2020Q2, so the `while q <= end_q` loop never runs (verified: start_q 2020Q2 > end_q 2019Q4). Line 220 then indexes quarters[0][0] and quarters[-1][0] -> IndexError -> uncaught -> sys.exit(1). The df-non-empty guard at 326 does not cover an all-pre-2020 dataset.
- **Failure scenario:** A corrupted/truncated or test account_performance.parquet whose max date is before 2020-04-01 -> quarters=[] -> IndexError on line 220 aborts the chain. Not reachable with normal 2020+ live data, but a latent hard-fail.
- **Proposed fix:** After building quarters, add `if not quarters: log('no quarters in range'); return 0` before the line 220 index access.

## Finding 4 -- [low/incremental-full-break/incremental]
- **Location:** `data/inf/scripts/gold/INF_D_09.account_timeseries.py:160 (data_as_of) + :219 (quarter derivation); dependency on ACCOUNT_PERF_KEY not refreshed in incremental`
- **Mechanism:** D_09 is in CHAIN_INCREMENTAL (dispatch line 340) but its sole source INF_C_03 (gold/timeseries/account_performance.parquet) is NOT, so in incremental mode D_09 re-derives quarters and data_as_of from a stale parquet (the last full-run max date) and re-emits the same account timeseries. Values are self-consistent (data_as_of honestly reports the stale date) but the L4 account-detail chart lags other artifacts refreshed by the incremental run, and cannot gain a newly-crossed quarter until a full run.
- **Failure scenario:** A quarter boundary is crossed and only incremental chains run before the next CHAIN_FULL -> the account-level timeseries data_as_of and latest quarter stay behind household/other served artifacts refreshed that cycle (cross-artifact vintage skew, no wrong numbers).
- **Proposed fix:** Inherent to the documented incremental design ('assumes A/B/C gold outputs exist'); daily CHAIN_FULL bounds the skew. If fresher intraday account timeseries is required, add INF_C_03 to CHAIN_INCREMENTAL or drop D_09 from the incremental chain. Low priority.
