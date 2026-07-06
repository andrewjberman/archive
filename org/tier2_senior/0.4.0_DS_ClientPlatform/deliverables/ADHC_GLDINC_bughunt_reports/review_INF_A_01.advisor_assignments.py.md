# REVIEW -- INF_A_01.advisor_assignments.py

- script: `data/inf/scripts/gold/INF_A_01.advisor_assignments.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 3

## Finding 1 -- [medium/merge-dedup/full]
- **Location:** `data/inf/scripts/gold/INF_A_01.advisor_assignments.py:141 (drop_duplicates, with coerce at :127)`
- **Mechanism:** account_id is coerced with pd.to_numeric(errors='coerce').astype('Int64') (line 127), so any non-numeric/blank account_id becomes <NA>. df.drop_duplicates(subset=['account_id']) (line 141) treats every <NA> as equal to every other <NA> and keeps only the FIRST such row, silently discarding all other accounts whose account_id failed to parse. Rows with <NA> account_id are NOT removed by the dropna at line 136 (that only drops <NA> rep_id).
- **Failure scenario:** An accounts_v2 silver partition (e.g. a Bug-B-adjacent or schema-drift vintage the 14-day walk-back can select) contains 3 accounts with blank/non-numeric account_id. All 3 coerce to <NA>; drop_duplicates keeps 1 and drops 2. Those 2 accounts vanish from gold/dimensions/advisor_assignments.parquet, so downstream advisor rollups (INF_C_07 advisor_attribution, INF_D_00f advisor_nna_canonical) inner-joining on account_id under-count by those accounts' AUA with no error. Empirically reproduced: input account_id [<NA>,<NA>,100,100,101] -> 3 output rows, one distinct <NA> account dropped.
- **Proposed fix:** Explicitly drop <NA> account_id rows before dedup (df = df.dropna(subset=['account_id'])), or assert no account_id is <NA> post-coerce and fail loud, so a parse failure is not masked as a duplicate collapse.

## Finding 2 -- [low/empty-null-handling/full]
- **Location:** `data/inf/scripts/gold/INF_A_01.advisor_assignments.py:128,132-136`
- **Mechanism:** rep_id is coerced with pd.to_numeric(errors='coerce') (line 128); a present-but-non-numeric rep_id becomes <NA> and is then dropped by df.dropna(subset=['rep_id']) (line 136). The WARN at line 134 attributes ALL dropped rows to 'account not in INFLECTION_REP_IDS allowlist', conflating a data-quality coercion failure with an intended allowlist exclusion. The account is silently removed and the log misdirects diagnosis.
- **Failure scenario:** accounts_v2 rep_id leaks a non-numeric value for account 12345 (e.g. a rep name 'Keil' or empty string from an upstream column-order/quality bug). to_numeric -> <NA> -> account 12345 dropped from advisor_assignments; its AUA is orphaned from every advisor rollup, while the WARN reports it as 'not in allowlist', masking the real cause. Verified: to_numeric(['Keil','']) -> [<NA>,<NA>]; dropna removes those rows.
- **Proposed fix:** Distinguish genuinely-null rep_id from coercion failures: compute the count of non-null-but-non-numeric rep_ids separately and log/alarm on it distinctly rather than folding it into the allowlist WARN and silently dropping.

## Finding 3 -- [low/schema-column/full]
- **Location:** `data/inf/scripts/gold/INF_A_01.advisor_assignments.py:127,128,146`
- **Mechanism:** build_advisor_assignments accesses df['account_id'] (127), df['rep_id'] (128) and df['rep_name'] (146) directly. rep_name only exists if the rename at 121-124 found 'representative_name' in the source (rename silently no-ops on a missing key). Unlike the output-column selection (152-155) which guards presence, these required-source columns are unguarded, so a missing one raises KeyError -> uncaught -> sys.exit(1) -> hard-fails the no-timeout compute chain and fires the ChainFailed alarm. (Fail-loud, not silent; and INF_A_00 has the identical dependency and runs immediately before, so it would abort first.)
- **Failure scenario:** accounts_v2 silver recently added/renamed representative_name; a Bug-B empty-partition cadence forces the walk-back (up to WALK_BACK_MAX_DAYS=14) to a pre-rename partition with >=100 rows. The rename is a no-op, df['rep_name'] at line 146 raises KeyError, and the gold chain aborts.
- **Proposed fix:** Validate presence of the required source columns (account_id, rep_id, representative_name) right after load with an explicit clear error, or guard rep_name access the same way output_cols availability is checked.
