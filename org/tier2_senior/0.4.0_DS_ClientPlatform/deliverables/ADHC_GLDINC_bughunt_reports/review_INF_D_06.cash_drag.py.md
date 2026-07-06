# REVIEW -- INF_D_06.cash_drag.py

- script: `data/inf/scripts/gold/INF_D_06.cash_drag.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 4

## Finding 1 -- [medium/merge-dedup/full]
- **Location:** `build_window_rows lines 479-481 (household_id skip) + line 469 (accts_dim left-merge)`
- **Mechanism:** accts_dim is LEFT-merged onto the per-account frame, then any row whose household_id is NaN is silently `continue`-skipped. household_id is NaN for (a) any account present in gold/holdings but absent from gold/dimensions/accounts_dimension_latest.parquet, or (b) any account whose household_id is null in the dim (orphan / unmapped accounts). The drop is completely silent -- no WARN, no dropped-count log -- so a shrinking panel is invisible.
- **Failure scenario:** A newly-opened account (or an account with no HH mapping) appears in gold/holdings (INF_B_01) but is missing / null-household in the INF_A_00 accounts_dimension snapshot. That account, which may hold material cash, is silently omitted from every cash_drag_{window}.json. This directly violates the module's stated contract ('Every account appears, no threshold filter'), and a regression that drops HH mappings from the dim would silently shrink the served panel with no signal.
- **Proposed fix:** After the merges, count rows with null household_id and emit a WARN (e.g. 'WARN [{window}]: N accounts dropped for missing household_id') before the skip; optionally emit household_id as a nullable/sentinel rather than dropping, or fail loud if the drop fraction exceeds a threshold.

## Finding 2 -- [low/merge-dedup/full]
- **Location:** `build_window_rows line 467 (snap.merge(avg_df, how='inner'))`
- **Mechanism:** current_cash/aua come from a SINGLE latest healthy snapshot partition (`snap`), inner-joined to `avg_df` (accounts with holdings anywhere in the window). The inner join emits only the intersection, so any account present in the window's holdings but absent from that one latest partition is dropped from ALL windows.
- **Failure scenario:** An account that was fully liquidated and closed a few days before data_as_of held large cash during the qtd/ytd/1y/max window. It is absent from the single latest snapshot partition, so the inner join drops it and its window cash-drag never appears -- again contradicting 'every account appears', most visibly for the historical (max/1y) windows where closed-but-formerly-active accounts silently vanish.
- **Proposed fix:** If closed accounts should appear for historical windows, LEFT-join avg_df to a union of window accounts and fill current_cash/aua = 0 (or last-known) for accounts absent from the latest snapshot; otherwise document that this panel is intentionally current-open-accounts-only and reconcile the docstring.

## Finding 3 -- [low/unguarded-read/full]
- **Location:** `load_accounts_dim line 151 (_read_s3_parquet(ACCTS_DIM_KEY)) -> _read_s3_parquet line 109 (s3.get_object)`
- **Mechanism:** The accounts_dimension read has NO try/except (unlike _load_holdings_day_raw/_summary and the transactions read, which all catch and return None/empty). A NoSuchKey / read error propagates to the main() top-level `except Exception` -> sys.exit(1). Under the dispatcher, all gold steps run with no timeout and hard-fail the chain on any non-zero exit, so this aborts the whole gold run at INF_D_06a.
- **Failure scenario:** INF_A_00 succeeds (so the chain reaches D_06a) but writes only a dated key and not the `gold/dimensions/accounts_dimension_latest.parquet` alias, or the alias is renamed/first-run-absent. The unguarded get_object raises NoSuchKey -> the chain FAILS at INF_D_06a and every downstream D step is skipped. Practically ordering-protected (A_00 precedes in full mode) but undefended relative to the script's other reads.
- **Proposed fix:** Wrap the accounts-dim read in try/except and degrade gracefully (emit a WARN and treat labels/household as empty, or fail with a clear ERROR message naming the missing key) rather than letting a raw NoSuchKey bubble to the chain-fatal handler.

## Finding 4 -- [low/type-issue/full]
- **Location:** `load_accounts_dim lines 158-169 (default pd.Series([''] * len(dim)) + label_df.apply)`
- **Mechanism:** After `dim = dim.dropna(subset=['account_id','household_id'])` (line 154) the frame has a GAPPED index. If a label column is entirely absent, `dim.get('reg_type', pd.Series([''] * len(dim)))` returns a default Series with a fresh RangeIndex (0..n-1), which no longer aligns to dim's gapped index. Building label_df from a mix of a gapped-index (present) column and a RangeIndex (absent) column aligns on the index union, so the subsequent `.apply(...)` result reindexes incorrectly when assigned back to dim['account_label'].
- **Failure scenario:** The accounts_dimension snapshot lacks the reg_type (or registration_name) column entirely. account_label values become misaligned / NaN-derived and mostly collapse to None. Cosmetic only (label is emitted as `str(... or '') or None` and never feeds a served number or merge key), and it does not crash -- but the labels silently degrade. If BOTH reg columns are present (the normal case) there is no bug.
- **Proposed fix:** Reset the index before building labels (`dim = dim.reset_index(drop=True)` after the dropna) or construct the default Series with dim's index (`pd.Series('', index=dim.index)`) so present/absent columns align identically.
