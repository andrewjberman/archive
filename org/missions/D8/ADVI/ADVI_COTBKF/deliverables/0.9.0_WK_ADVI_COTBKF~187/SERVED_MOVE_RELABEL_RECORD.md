# SERVED_MOVE_RELABEL_RECORD (ADVI_COTBKF CB-cs-1, round 97)

Counts only. The JSON beside this file carries the same figures in the fixed keys.

**Measured: yes.** The regrade (current code, served settings) and the build ran with rc 0. The control compared
every pre-existing served column with the build, row-aligned on the key.

**Control result: 3 of 3 tables equal** on every pre-existing column (0 rows differing, max_abs_diff 0.0,
0 key misaligned rows, 0 type mismatches). `run_commit` is excluded and differs on every row (served
`6f70d5cc01bb2e196266799a657be6d0b2dc8a16`, built `14793ce1882921b8da023c99e9512879d0d451c1`).

| table | served rows | built rows | columns compared | rows differing | pre_existing_equal |
|---|---|---|---|---|---|
| daily_returns | 1,691,729 | 1,691,729 | 5 | 0 | true |
| account_day_value | 21,102,041 | 21,102,041 | 6 | 0 | true |
| month_grades | 82,593 | 82,593 | 18 | 0 | true |

Served VersionIds and LastModified equal round 96's record for all three keys (read once each, read-only).

**Added columns:** `use_class` and `porting_verdict`, on all three tables, and nothing else.

| table | use_class | porting_verdict |
|---|---|---|
| daily_returns | NOT_YAHOO 1,022,467; NOT_FOR_ACTIVE 667,974; INACTIVE_USE 1,288 | NOT_YAHOO 1,022,467; UNVERIFIED 669,262 |
| account_day_value | NOT_YAHOO 17,392,999; NOT_FOR_ACTIVE 3,688,916; INACTIVE_USE 20,126 | NOT_YAHOO 17,392,999; UNVERIFIED 3,709,042 |
| month_grades | NOT_YAHOO 49,376; NOT_FOR_ACTIVE 33,150; INACTIVE_USE 67 | NOT_YAHOO 49,376; UNVERIFIED 33,217 |

account_day_value: 729 distinct accounts have at least one NOT_FOR_ACTIVE row.

**Yahoo points:**
- Price input: 1,049,193 replaced points (`yahoo_finance`, `as_traded_close`) and 477,980 re-derived days
  (`linear_interpolation`, `as_traded_close`). These equal the regrade's PRICE-BASIS line.
- New price file (`security_day_price.parquet`, carries `source`): 1,325,110 distinct cusip-days name
  `yahoo_finance`; 705,133 name `linear_interpolation`. All 2,130,163 (cusip, date) keys are unique.
- account_day_value `price_source`: 0 rows name a Yahoo source. The column is the store name in served and built
  alike (`cottonwood-silver-canonical-prices`, `cash-at-par`, `cottonwood-gold-canonical-holdings`,
  `etfs-bbg-testpull-ticker-history`, or null).

**Reconciliation of the labels to the price file:** 4,038,997 priced account_day_value rows sit on a
Yahoo-sourced (cusip, date) key. Of these, 329,955 are `cash-at-par` rows, which the builder never labels
(cash is excluded by design). 4,038,997 - 329,955 = 3,709,042, the exact count of rows whose `use_class` is not
NOT_YAHOO. Every labelled row sits on a Yahoo-sourced key. The 709 keyed rows with a null close are unlabelled.

**CB97cs1-AC2 fails as written:** `LABELS adv_rows=21102041 yahoo_source_rows=0 labelled_rows=3709042 equal=False`.
The check reads `price_source`, which never names a Yahoo source. Surprise row: ADVI_COTBKF-D1-W187-S1.

**Corrections made during the run:** an earlier labels pass counted both Yahoo sources under the
`yahoo_finance` key (2,030,243). The per-source counts above are the corrected ones.

Scratch directories hold the per-account values and stay off git: `C:/Dev/ajb_workspace/.scratch/cotbkf_r97/`.
