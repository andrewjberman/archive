# REVIEW -- INF_D_04b.client_publishers.py

- script: `data/inf/scripts/gold/INF_D_04b.client_publishers.py`
- verdict: **issues-found**
- runs_in_incremental: True
- findings: 5

## Finding 1 -- [high/merge-dedup/both]
- **Location:** `data/inf/scripts/gold/INF_D_04b.client_publishers.py:257 (df.merge(hh_map, on='account_id', how='inner')); abort at 258-260 + main:395-397`
- **Mechanism:** Holdings are inner-joined to the household dim to attach household_id. Any holdings account_id that is not present in the latest silver/api_dims/household partition is SILENTLY dropped. If the entire join yields 0 rows, load_canonical_holdings returns an empty DataFrame, main hits `if lots.empty: return 1`, and the no-timeout D-chain hard-fails at INF_D_04b.
- **Failure scenario:** A newly-onboarded account A123 appears in gold/canonical/holdings_{date}.parquet (positions land first) but the household dim (built by a SEPARATE external cron: pull_orion_households.py + build_household_dim.py, not in the dispatch chain) has not yet ingested it. The inner merge at line 257 drops every A123 lot; that household's composition.json mix percentages and total_mv are understated with NO error logged. Worse in incremental: holdings is from the last full run while the household dim refreshes on its own cron, so the two drift out of alignment between full runs.
- **Proposed fix:** Do a LEFT join and surface unmatched-account MV as a logged diagnostic + a reconciliation assertion (compare joined MV vs raw holdings MV per firm), rather than an inner join that silently discards accounts. For the abort path, distinguish 'holdings absent' (fail-loud) from 'holdings present but 0 matched households' (investigate the dim, do not silently under-serve).

## Finding 2 -- [medium/type-issue/both]
- **Location:** `data/inf/scripts/gold/INF_D_04b.client_publishers.py:247 and :211 (account_id normalized via .astype(str).str.strip()) feeding the join at :257`
- **Mechanism:** account_id is normalized to a join key with a bare .astype(str) on BOTH sides independently. pandas renders a float64 column as '12345.0' but an int64/str column as '12345'. If the two sources read account_id with different pandas dtypes, the string keys mismatch and the inner join returns 0 rows.
- **Failure scenario:** If INF_B_00 writes account_id such that it reads back as float64 (any NaN in the column upcasts int->float on parquet read), df['account_id'].astype(str) yields '12345.0' while the household dim (int/str source) yields '12345'. The inner merge at 257 matches 0 rows -> load returns empty -> main returns 1 -> the whole no-timeout D-chain hard-fails at INF_D_04b. The same mismatch silently zeros the assets_v2 classifier join (line 170), leaving asset_class all '' and mix={} even on the populated path.
- **Proposed fix:** Canonicalize account_id numerically before stringifying (e.g. pd.to_numeric(...).astype('Int64').astype('string'), or a shared _norm_account_id helper used identically on holdings, the household dim, and the classifier) so int/float/str all collapse to the same key.

## Finding 3 -- [medium/other/both]
- **Location:** `data/inf/scripts/gold/INF_D_04b.client_publishers.py:360 (_write_json_s3 -> s3.put_object) and :366 (f.result())`
- **Mechanism:** publish_composition fans 32 concurrent S3 writes and calls f.result() with no per-household try/except. Any single put_object exception (transient throttle/5xx, SlowDown, connection reset) is re-raised by f.result(), is uncaught in publish_composition, propagates to main's outer except, and sys.exit(1) aborts the chain.
- **Failure scenario:** Under a large household count x 32 write workers, one s3.put_object hits a transient 503 SlowDown and raises. f.result() at line 366 re-raises inside the as_completed loop; nothing catches it; main's except -> sys.exit(1). Some composition.json artifacts are already written and the rest are not, leaving a PARTIAL/inconsistent client-composition publish, and the entire D-chain fails at INF_D_04b from a single transient write error.
- **Proposed fix:** Wrap _publish_one in try/except (return a failure tuple), tally failures, and add a bounded retry on put_object; only fail the step if the failure rate exceeds a threshold, so a transient single-object error cannot abort the chain or half-publish.

## Finding 4 -- [medium/incremental-full-break/incremental]
- **Location:** `data/inf/scripts/gold/INF_D_04b.client_publishers.py:217-265 (load_canonical_holdings reads latest gold/canonical/holdings) vs orion-gold-dispatch.sh:340 (CHAIN_INCREMENTAL omits INF_B_00)`
- **Mechanism:** The only MV source is the latest gold/canonical/holdings_*.parquet. In CHAIN_INCREMENTAL, INF_B_00 (canonical_holdings) does NOT run, so holdings is pinned to the last FULL run's date, while the incremental chain refreshes silver + INF_D_00 header aggregates to the current date. INF_D_04b rewrites composition.json with generated_at=now but data_as_of=stale.
- **Failure scenario:** Incremental runs on 07-06 while the last full run was 07-05. INF_D_04b serves composition.json with data_as_of=07-05 mix/MV, but INF_D_00's header AUA on the same client page is fresher. Because generated_at (and S3 LastModified) advance, a freshness monitor keyed on mtime reports the artifact CURRENT while its data silently lags; if full runs are skipped/fail for several days the composition drifts further with no chain error.
- **Proposed fix:** Either exclude INF_D_04b from CHAIN_INCREMENTAL (composition depends on B-stage holdings that incremental does not rebuild), or gate it to skip/emit a staleness warning when holdings data_as_of trails the current silver date, so a stale-holdings composition is not published as if fresh.

## Finding 5 -- [low/schema-column/both]
- **Location:** `data/inf/scripts/gold/INF_D_04b.client_publishers.py:247-249 (unguarded df['account_id']/df['ticker']/df['market_value']) vs the defensive df.get('ticker', ...) at :253`
- **Mechanism:** load_canonical_holdings hard-indexes df['account_id'], df['ticker'], df['market_value'] with no column-existence guard, so a missing/renamed core column raises KeyError and aborts the no-timeout chain. This also contradicts the line-253 fallback df.get('ticker', pd.Series([''] * len(df))), which implies ticker may be absent but is dead code because line 248 already hard-indexes df['ticker'].
- **Failure scenario:** A future INF_B_00 schema change renames or drops the ticker (or market_value) column; line 248 df['ticker'].astype(str) raises KeyError before line 253's defensive df.get is ever reached -> INF_D_04b crashes and aborts the D-chain, with the 'graceful ticker-missing' path never able to run.
- **Proposed fix:** Validate required columns up front (assert set(['account_id','ticker','market_value']) <= set(df.columns) with a clear error) OR use df.get(...) consistently; remove the misleading dead-code fallback at line 253 or make the real read tolerate a missing ticker.
