# REVIEW -- INF_D_05.activity_scan.py

- script: `data/inf/scripts/gold/INF_D_05.activity_scan.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 2

## Finding 1 -- [low/unguarded-read/full]
- **Location:** `data/inf/scripts/gold/INF_D_05.activity_scan.py:119 (load_accounts_dim) and :135 (load_latest_aua_canonical), both via _read_s3_parquet at :82-84`
- **Mechanism:** Both gold inputs are read with a bare s3.get_object + pd.read_parquet and no try/except. An absent key raises NoSuchKey; for the accounts dim, a present-but-malformed parquet raises KeyError at :121/:123 (dropna/astype assume account_id + household_id exist). Either propagates to the top-level except in main (:403) which sys.exit(1)s. Gold/D steps run with NO timeout and HARD-FAIL the whole chain on any non-zero exit.
- **Failure scenario:** Invoke `orion-gold-dispatch.sh --chain gold-d` or `gold-cd` (documented contract: 'Assume upstream stages already complete in S3') against a bucket where gold/dimensions/accounts_dimension_latest.parquet or gold/timeseries/client_performance.parquet has not yet been produced (or the accounts dim exists but lacks the account_id column) -> boto3 NoSuchKey / pandas KeyError -> uncaught -> sys.exit(1) -> the entire D chain aborts. NOTE: in the daily CHAIN_FULL/CHAIN_COMPUTE run this is masked because the producers INF_A_00 (accts dim) and INF_C_02 (client_performance) run earlier in the same chain and would themselves hard-fail first if their outputs were unwritable -- so it is not triggered on the normal nightly.
- **Proposed fix:** Guard both reads the way load_all_transactions already guards its list (try/except -> return a typed-empty DataFrame with the expected columns, or a head_object precheck). The build_window_rows empty-state gate (:289) and the outer merges already tolerate an empty accts_dim / hh_aua, so a typed-empty return degrades to an empty-artifact emit instead of aborting the chain.

## Finding 2 -- [low/merge-dedup/full]
- **Location:** `data/inf/scripts/gold/INF_D_05.activity_scan.py:303 (build_window_rows: accts_dim.merge(acct_txn_counts, on='account_id', how='left'))`
- **Mechanism:** The per-window transaction counts are joined with a LEFT join anchored on accts_dim (account->household map, drop_duplicates('account_id')). Any account_id that has transactions in the full-history silver snapshot but is ABSENT from gold/dimensions/accounts_dimension_latest.parquet is silently excluded from the count (left join keeps only accts_dim rows). No crash -- a quietly under-counted served number.
- **Failure scenario:** A household owns an account that was later closed and dropped from the current accounts dimension but still carries historical transactions in the full-history silver/transactions snapshot. In the 'max' and '1y' windows those historical txns are not counted -> that household's txn_count is understated, which flips its activity_score percentile and can mis-segment it as buy_and_hold instead of active. Bounded to accounts missing from the current dim (closed/filtered accounts); the served activity_scan_{max,1y}.json numbers are then quietly low for the affected households.
- **Proposed fix:** If closed-account activity is meant to count, join from the acct_txn_counts side (or outer-join) and resolve orphan account_ids to households via a historical account->household map rather than the current-only dim; if the current-only behavior is intended, document it explicitly so the under-count is not mistaken for a data gap.
