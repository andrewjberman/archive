# IB64-1 -- the 1,961 granted accounts NOT_IN_DIRECTORY: which, where, why (worker ~144, 2026-10-07)

Recomputed from the sources (not from IRPT_CUSTDY's output): ownership map 7,022 distinct granted accounts (all 49financial; 190
advisors) minus the served directory `irpt-dir/49financial/2026-10-05/1.0` (4,696 entries, 7,652 account ids) through the repo's own
projection (`_ids` seam + mint) = 5,061 in the directory, **1,961 not in it** (equals IRPT_CUSTDY's figure). Inflection has no ownership
map object (404), cottonwood's map (`opal-data-cot`) holds 0 advisors; so 0 granted accounts at either. Census:
`IB64-1_directory_coverage.json`; rebuild: `build_ib64_1_census.py` (read-only).

| reason | n | why absent | what I would change in the directory build |
|---|---|---|---|
| BD_KEY_ABSENT_FROM_EVERY_BRIDGE_SOURCE | 1,447 | the map's Black Diamond key is in no xref partition (53), no fee-role partition (53), no `fact_bd_allocation`/`fact_taxsma_report`; no path to a Schwab id exists, so the directory (built from `dim_relationship`, `directory_runner.build_49f`) cannot carry them | Nothing in the directory build can fix this: the grant's source (ownership-map producer, `d08_firm_ownership_map.py`) names keys the identity bridge never saw. Find where those keys originate and either add them to `dim_account_xref` or drop the grant. Until then FWD-1 reads them from the map and shows no name. |
| XREF_UNRESOLVED_NO_SCHWAB_MATCH | 343 | xref row exists, `schwab_account_id` null (`match_method=unresolved`); its account number matches no `dim_account` account | Fix the xref match upstream (BD silver `dim_account_xref`); the seam (`custodian_key_seam.json`, 826 None values removed by pr-339) cannot map a null. |
| XREF_UNRESOLVED_NUMBER_IN_DIM_ACCOUNT_ONLY | 139 | as above, but the xref's account number IS a `dim_account` Schwab account that `dim_relationship` lacks (carried, absent from feed) | Same upstream fix; if matched, still absent until the account is back in the feed (next row). |
| ACCOUNT_CARRIED_ABSENT_FROM_FEED_NOT_IN_RELATIONSHIP | 32 | seam maps them to Schwab ids that are in `dim_account` (open, `absent_from_feed_since` 2026-06-25..08-10, carried by `a00_dim_account.py` ~318-327) but not in `dim_relationship`, because `a01_dim_relationship.py:228` builds the account universe from `fact_acc` (today's feed) | Have the directory also emit an account-only entry for `dim_account` rows carried absent-from-feed (the build's `unmapped` branch already shapes one), or accept them as no-entry by design. |
| FENCE_COTTONWOOD_BUCKET_DENIED | 0 | declared; `opal-data-cottonwood` is 403, but no granted cottonwood account exists (row W144-S1) | none |
| UNEXPLAINED | 0 | every account placed | none |

No change is made by this order.
