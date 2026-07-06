# REVIEW -- INF_C_07.advisor_attribution.py

- script: `data/inf/scripts/gold/INF_C_07.advisor_attribution.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 2

## Finding 1 -- [high/other/full]
- **Location:** `main(), lines 300-307 (latest_date = ap['date'].max(); latest = ap[ap['date']==latest_date]; outer merge + total_aua.fillna(0.0))`
- **Mechanism:** account_team.total_aua is taken ONLY from the single global max date in account_performance, with NO completeness/coverage guard. Every account that lacks a row on that exact global max date is pulled in via the how='outer' merge with acct_dim and then fillna(0.0)'d to zero AUA. If the latest date partition is PARTIAL (fewer accounts than the true book), the outer merge silently converts every absent account into total_aua=0 rather than surfacing the gap. All three served views (account_team.total_aua, relationship_team.total_aua, rel_architect_lookup.tagged_aua) derive from this same acct_team, so the under-count propagates to the advisor leaderboard/attribution D-chain.
- **Failure scenario:** INF_API_PULL_PERF is one of the timeout+tolerate-bounded pull steps, so a partial perf pull is a KNOWN, tolerated failure mode. Suppose today's pull writes silver/perf for only 5 of 849 accounts for date=2026-07-06 while the full 849 are on 2026-07-05. INF_C_03 concats it, so account_performance has date=2026-07-06 with 5 accounts. C_07 computes latest_date=2026-07-06, latest=5 rows; the outer merge with acct_dim yields ~844 accounts with total_aua NaN -> fillna(0.0). Served advisor AUA / tagged_aua collapses to near-zero for almost the whole firm with no error and rc=0.
- **Proposed fix:** Do not blindly trust ap['date'].max() as complete. Add a coverage guard before selecting the snapshot: e.g. compare the account count on latest_date against the prior date (or acct_dim count) and fall back to the last date whose coverage is within a tolerance / raise if the latest partition is materially short; or build total_aua from each account's OWN most-recent available row (forward-fill per account) instead of only the single global max date.

## Finding 2 -- [low/schema-column/full]
- **Location:** `main(), line 297: ap['total_aua'] = pd.to_numeric(ap.get('total_aua', 0), errors='coerce').fillna(0.0)`
- **Mechanism:** ap.get('total_aua', 0) returns the scalar default 0 when the 'total_aua' column is absent; pd.to_numeric(0, errors='coerce') then returns a numpy int64 SCALAR (not a Series), and numpy scalars have no .fillna method -> AttributeError. This propagates uncaught to the top-level except (lines 393-397) which prints ERROR and calls sys.exit(1). Because every gold step in the chain runs with no timeout and hard-fails on non-zero exit, this aborts the entire INF gold D-chain.
- **Failure scenario:** A schema regression or upstream change that drops/renames the total_aua column in gold/timeseries/account_performance.parquet (or a hand-built/degraded artifact) causes ap.get('total_aua', 0) to hit the scalar-default branch. INF_C_03 currently guarantees the column (it force-creates total_aua=0.0), so this cannot fire today, but the defensive default is a latent crash rather than the intended graceful zero-fill.
- **Proposed fix:** Handle the missing-column case as a Series, e.g. `s = ap['total_aua'] if 'total_aua' in ap.columns else pd.Series(0.0, index=ap.index); ap['total_aua'] = pd.to_numeric(s, errors='coerce').fillna(0.0)`.
