# X2 GLOBAL BASIS -- what the combined `global` figure is made of, as emitted at 2026-10-08

Cell CN-c-1 (round 3, M7 recut, FWD-3). This file replaces the round-2 basis at `org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~5/X2_GLOBAL_BASIS.md`, which is not edited. It is a plain statement of what the served objects contain on the as-of date. It does not argue that the figure is safe and it proposes no fix.

AS-OF: 2026-10-08
DENOMINATOR: global by_model entries read = 41 (20 in aggregate-aua-timeseries, 14 in account-distribution, 7 in aum-metrics); series keys read = 17 per-date arrays of the 29 top-level keys of global aggregate-aua-timeseries

# Field families

| family | min firms | entries | evidence |
|---|---|---|---|
| headline sums | 3 | 2 | aggregate-aua-timeseries: `opal_aggregate_aua` and `model_aua`, per-date arrays read at the index of 2026-10-08 |
| by_model | 0 | 41 | aggregate-aua-timeseries `by_model.<key>.account_count[idx]` and `.model_value[idx]` (20); account-distribution `by_model.<name>.account_count` (14); aum-metrics `by_model[].account_count` (7) |
| non_model_aua | 1 | 1 | aggregate-aua-timeseries `non_model_aua[idx]` |
| inflection_non_model_aua | 1 | 1 | aggregate-aua-timeseries `inflection_non_model_aua[idx]` |

# Single-firm entries

Held at one firm = a nonzero `account_count` at the as-of in exactly one firm scope, under the match rule in Method. Value equal = the global value equals that one firm's value (boolean only, no figure printed).

- aggregate-aua-timeseries: 10 single-firm entries of 20 entries read; 10 of the 10 have a value equal to the one firm's value.
- account-distribution: 9 single-firm entries of 14 entries read; 2 of the 9 have a total_aum equal to the one firm's value.
- aum-metrics: 2 single-firm entries of 7 entries read; 2 of the 2 have an aum equal to the one firm's value.

aggregate-aua-timeseries (entry; one firm; account_count at 2026-10-08; value equal):
- Opal 15/85 Income Portfolio (`opal_15_85_income_portfolio`); cottonwood; 1; yes
- 50/50 INT/LTC (`opal_blend_5050_int_ltc`); inflection; 160; yes
- 50/50 ST/INT (`opal_blend_5050_st_int`); inflection; 23; yes
- Opal Fixed Income (`opal_fixed_income`); cottonwood; 2; yes
- Opal Income Portfolio - Gillham (`opal_income_portfolio_gillham`); cottonwood; 1; yes
- Opal Moderate Income (`opal_moderate_income`); cottonwood; 1; yes
- Opal Moderate Income Portfolio (`opal_moderate_income_portfolio`); cottonwood; 13; yes
- Opal Moderate Income Tax Efficient (`opal_moderate_income_tax_efficient`); cottonwood; 3; yes
- Opal Muni Sleeve (`opal_muni_sleeve`); cottonwood; 1; yes
- PFDE (`pfde`); cottonwood; 4; yes

account-distribution (entry; one firm; account_count at 2026-10-08; value equal):
- Opal 15/85 Income Portfolio; cottonwood; 1; no
- Opal Fixed Income; cottonwood; 2; no
- Opal Income Portfolio - Gillham; cottonwood; 1; no
- Opal Moderate Income; cottonwood; 1; no
- Opal Moderate Income Portfolio; cottonwood; 13; no
- Opal Moderate Income Tax Efficient; cottonwood; 3; no
- Opal Muni Sleeve; cottonwood; 1; no
- 50/50 INT/LTC (global name Opal Blend 5050 Int Ltc); inflection; 162; yes
- 50/50 ST/INT (global name Opal Blend 5050 St Int); inflection; 23; yes

aum-metrics (entry; one firm; account_count at 2026-10-08; value equal):
- 50/50 INT/LTC (global name Opal Blend 5050 Int Ltc); inflection; 160; yes
- 50/50 ST/INT (global name Opal Blend 5050 St Int); inflection; 23; yes

# Method

Objects read. All twelve objects were read with read-only `s3api get-object` from bucket `opal-data-assets`: `portal/gold/mdpf/<scope>/aum-metrics/2026-10-08.json`, `.../account-distribution/2026-10-08.json` and `.../aggregate-aua-timeseries/2026-10-08.json` for each of `global`, `49financial`, `inflection` and `cottonwood`. Every object exists for 2026-10-08, so no 2026-10-09 object was substituted. The as-of index is 492 in the global and cottonwood timeseries and 483 in the 49financial and inflection timeseries (both dates equal 2026-10-08).

Match rule, aggregate-aua-timeseries. Entries are matched by the by_model key, which is the same key in every scope and corresponds to the `model_key` of `data/mdpf/scripts/gold/mdpf_model_registry.json`. One key is not in the registry: cottonwood carries `divz` (display name Dividend SMA), while global carries `opal_div_sma` (display name Dividend SMA). `divz` is matched by display name only, which is not a key match, so it is counted as read and unmatched. The unmatched `divz` is not counted as holding `opal_div_sma`.

Match rule, account-distribution and aum-metrics. These objects are keyed by display name, which differs between scopes. Names are matched by the renames recorded in the registry `_changelog` (v4): Ultra Short-Term to Ultra-Short Term; Short-Term to Short Term; Intermediate to Intermediate Term; Long-Term Conservative to Long Term; Long-Term Aggressive to Ultra-Long Term. The two 50/50 blends (global `Opal Blend 5050 Int Ltc` and `Opal Blend 5050 St Int`, and inflection `50/50 INT/LTC` and `50/50 ST/INT`) are matched by inspection, since no registry row carries the snapshot spelling; they affect two entries in each snapshot object. All other names are exact display-name equal.

Held at a firm. A firm holds an entry when its account_count is nonzero at the as-of. A null account_count is not held. Value equal is compared within a relative tolerance of 1e-6 and reported as yes or no.

Counts of the aggregate-aua-timeseries by_model (20 global entries). Two are null at the as-of (`opal_income`, `opal_moderate_income_portfolio_tax_efficient`), so they carry no figure and are excluded from min firms. Two are non-null at the as-of and held by no firm (`opal_growth_sma`, 45 accounts; `opal_div_sma`, 40 accounts). One is held by two firms (`tax`: 49financial and cottonwood). Five are held by all three firms (`opal_intermediate`, `opal_long_term_aggressive`, `opal_long_term_conservative`, `opal_short_term`, `opal_ultra_short_term`). Ten are held by one firm (listed above). Two plus two plus one plus five plus ten is twenty.

The single-firm count. This method gives 10 single-firm entries in aggregate-aua-timeseries. The cell text cites 12 by_model entries held at one firm. The 6 entries at three or fewer accounts are reproduced (1, 2, 1, 1, 3, 1 accounts, among the ten listed above). The count of 12 is not reproduced: matching `divz` by display name would make 11, and the union of single-firm names across the three global by_model objects is 10. The two null entries are not single-firm entries under this rule.

Zero-firm entries with a non-null figure. `opal_growth_sma` and `opal_div_sma` carry a non-null global value and a nonzero global account_count at 2026-10-08, and no firm scope holds either entry at that date (49financial's last nonzero account_count for both is at 2026-07-17). Measured: the global account_count at 2026-10-08 equals the global account_count at 2026-07-17, and both equal the 49financial value at 2026-07-17; the global model_value at 2026-10-08 is not equal to the global model_value at 2026-07-17. For these two entries, min firms at the as-of is 0. The by_model min firms of 0 is the fewest firms over the entries carrying a non-null global figure at the as-of.

Headline sums. The family is `opal_aggregate_aua` and `model_aua`. Min firms is 3 because all three firm legs are non-null at the as-of. Measured: the global `model_aua` at 2026-10-08 equals the sum of the three firms' `model_aua` (equal). For `opal_aggregate_aua`, the four legs the fold reads at the as-of (49financial model and non-model, inflection model, cottonwood model) are all non-null, which gives the three-firm composition the fold states (`dim_mdpf_aggregate_aua_timeseries.py:2424-2425`). Measured and not resolved here: at 2026-10-08 the global `opal_aggregate_aua` is not equal to the global `model_aua` plus `non_model_aua` within 0.011; the identity the fold states at `dim_mdpf_aggregate_aua_timeseries.py:2257` holds on 460 of the 484 non-null dates of the global axis. The size of the gap is not characterised here. `account_count_total` is a count, is not in the headline family, and is not equal to the sum of the three firm totals at the as-of (measured, not printed).

Non-model series. `non_model_aua` at the as-of equals the 49financial `non_model_aua` (equal), so min firms is 1. `inflection_non_model_aua` at the as-of equals the inflection `non_model_aua` (equal); the firm objects carry no field of that name, so min firms is 1 and the single firm is inflection.

Build times. The account-distribution objects carry different generated_at stamps: global and inflection at 2026-10-08T13:31Z, cottonwood at 2026-10-09T13:31Z. The snapshot value comparisons may therefore cross build times.

Not read. Nothing among the twelve objects was left unread. No other scope, no bronze input and no AWS write was read or made. The fold's code is cited by line only where a count or identity is stated.

Client data. No account id and no dollar figure is printed in this file. Account counts per entry are printed as the entries' own counts.
