# REVIEW -- INF_D_07.concentration_risk.py

- script: `data/inf/scripts/gold/INF_D_07.concentration_risk.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 3

## Finding 1 -- [high/merge-dedup/full]
- **Location:** `data/inf/scripts/gold/INF_D_07.concentration_risk.py:50 (ACCTS_DIM_KEY) + load_accounts_dim():72 + load_latest_holdings() merge/dropna:117-120`
- **Mechanism:** ACCTS_DIM_KEY='silver/accounts_dim/latest.parquet' is a FROZEN-at-2026-04-29 artifact. Its producer (convert_orion_to_silver.py) was decommissioned, and sibling scripts INF_C_09 (lines 125-130), INF_D_00, and INF_D_00c were all repointed off it to the live silver/api_dims/accounts_v2 dim under ADVI_INFREF P1 LEG-1 (2026-06-30); INF_D_07 was NOT repointed. INF_B_01 gold/holdings carries NO household_id column (output cols: date,account_id,ticker,units,price,market_value,price_source,custodian), so the 'if household_id not in df.columns' branch at line 117-118 ALWAYS runs, left-merging today's holdings against the ~2+ month stale account->household map. account_id is int64 on both sides so keys match dtype (no dtype-mismatch 0-row join) -- but any account opened after 2026-04-29 is absent from the frozen dim, gets household_id=NaN, and is DROPPED at line 120 (df.dropna(subset=['household_id'])).
- **Failure scenario:** An account opened 2026-05-15 holding a $2M concentrated single-ticker position is not in the frozen 04-29 dim. On the daily full run its holdings rows are silently dropped: (a) if that account is the household's only account, the entire household VANISHES from platinum/firm/concentration_risk.json (household under-count); (b) if it shares a household with a pre-04-29 account, that household's aua (total_mv) is understated by $2M and its top1_pct/HHI are computed on the partial portfolio -- e.g. a genuinely 'concentrated' household is served as 'diversified'. Silent: no crash, rc=0, wrong served concentration numbers on the portal.
- **Proposed fix:** Repoint ACCTS_DIM_KEY to the live accounts dim exactly as INF_C_09.load_accounts_dim() does: read the latest silver/api_dims/accounts_v2/snapshot_date=*/data.parquet partition and select account_id/household_id, instead of the frozen silver/accounts_dim/latest.parquet.

## Finding 2 -- [low/type-issue/full]
- **Location:** `build_concentration_risk():168-181`
- **Mechanism:** Output household_id is produced per-row via int(hh_id) with a try/except that falls back to str(hh_id). If the source dim's household_id is uniformly numeric the field is int for every row (matches the declared schema household_id:int), but a single non-numeric household_id yields a str for that one row -- a mixed int/str JSON array across households, which a strictly-typed downstream consumer can mis-handle.
- **Failure scenario:** A household_id like 'HH_LEGACY' appears in the accounts dim -> that row emits household_id as the string 'HH_LEGACY' while all other rows emit ints, so a consumer keying on int(household_id) or a typed schema rejects/mis-joins just that row.

## Finding 3 -- [low/empty-null-handling/full]
- **Location:** `main():205-217`
- **Mechanism:** There is no non-empty / row-count floor before upload. If the account->household join collapses to zero surviving rows (extreme case of the stale-dim drop above, or an accounts_dim shape change), build_concentration_risk returns [] and main uploads the literal '[]' JSON with rc=0, silently overwriting a previously-good served concentration_risk.json with an empty artifact and emitting no alarm.
- **Failure scenario:** If a future accounts_dim swap changes household_id dtype/name (or the frozen dim is pruned) so no holdings row keeps a household_id, the chain still exits 0 and publishes an empty platinum/firm/concentration_risk.json, blanking the portal concentration view with no failure signal.
- **Proposed fix:** Add a floor guard before put_object (e.g. raise if len(rows)==0, or assert len(rows) >= a fraction of the prior artifact's row count) so a collapsed join fails loud instead of serving an empty file.
