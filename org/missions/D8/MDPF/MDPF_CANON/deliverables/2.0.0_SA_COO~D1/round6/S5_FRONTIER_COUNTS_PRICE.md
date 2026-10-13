# MDPF_TAXSMA-S5 -- the frontier counts read a frozen 2026-08-17 distribution: what it is, what moving it costs (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~11:5xZ)

Read-only (head/get). Input: CTO msg 4776, round-5 ADDENDUM 4 item 2. Nothing here is a cell, an order or a commit. Anchors are file:line at HEAD or S3 key.

## 1. What the loader reads, and where it lands

- `load_account_dist_frontier_counts(firm_id)` (`dim_mdpf_aggregate_aua_timeseries.py:769-812`) reads ONE object per scope:
  `s3://opal-data-assets/gold/mdpf_revamp/{firm_id}/account_distribution.json` (`:786`), takes `meta.account_count_by_model_key` (`:809`, keyed by stable
  model_key) and the object's `period` (`:811`, returned under `__as_of__`). Absent (NoSuchKey) -> `{}` and a WARN, the frontier stays honest-None
  (`:793-796`); any other failure raises (C2-sibling fail-loud, `:797-808`).
- Landing: per-firm `:1203` (49financial, inflection) and global `:2520`. The override is `acct[-1] = ad_frontier[mkey]` (`:1232-1233`, `:2622-2623`):
  the LAST date of each `by_model[mkey].account_count` only, for the keys in the map that the builder iterates (global: the fixed 9-key
  `GLOBAL_MODEL_KEYS` tuple, `:2528`). No other date is touched.
- Downstream: `account_count_total` at the last date sums every by_model count (`:2693-2712`), so it moves with the override; the aum-metrics builder
  takes each row's `account_count` from the fold's frontier row and `total.account_count` = SUM of by_model frontier counts
  (`dim_mdpf_aum_metrics.py:27-36`). Measured on the served 2026-10-09 global aum-metrics: total.account_count 8264 = the ts `account_count_total`
  frontier, and its 7 model rows (192, 841, 2034, 3476, 1431, 160, 23) equal the ts frontier counts.
- Vintage check: `frontier_stamp_staleness` (`:876-907`) compares the object's `period` with the axis date IN TRADING DAYS and records a verdict IN-BAND
  on `meta.frontier_count.staleness` (49financial carries it). It DOES NOT refuse (`:880-883`): a stale roster is declared, not blocked. Measured:
  49financial's served ts reads `staleness.as_of 2026-08-17`, `frontier_date 2026-10-09`, verdict STALE. The global and inflection ts objects carry
  no `meta.frontier_count` key at all, so their staleness is not stated in band.

## 2. The price (served 2026-10-09 ts, the staged 2026-08-17 object, the newest A4 distribution 2026-10-12, period 2026-10-12)

Served frontier counts EQUAL the staged object's on every key it maps (global 7 of 7, 49financial 5 of 5, inflection 7 of 7): they are 08-17 rosters
wearing 2026-10-09. A4 = the fresh distribution the lambda built on 2026-10-12. Delta = A4 minus served.

| scope | key | served = staged | A4 (2026-10-12) | delta |
|---|---|---|---|---|
| global | opal_ultra_short_term | 192 | 214 | +22 |
| global | opal_short_term | 841 | 899 | +58 |
| global | opal_intermediate | 2034 | 2106 | +72 |
| global | opal_long_term_conservative | 3476 | 3707 | +231 |
| global | opal_long_term_aggressive | 1431 | 1470 | +39 |
| global | opal_blend_5050_int_ltc | 160 | 162 | +2 |
| global | opal_blend_5050_st_int | 23 | 23 | 0 |
| global | **sum of the 7 overridden keys** | 8157 | 8581 | **+424** |
| 49financial | the 5 core keys | 1606+1387+3279+704+168 | 1638+1424+3494+738+184 | **+334** (32, 37, 215, 34, 16) |
| inflection | the 7 keys | 202+32+90+29+12+160+23 | 209+33+89+30+15+162+23 | **+13** (7, 1, -1, 1, 3, 2, 0) |

Totals at the frontier if the input were the fresh A4: global `account_count_total` 8264 -> 8688 (+424, +5.1%); 49financial 7144 -> 7478, which
EQUALS the A4 distribution total.account_count (7478); inflection 548 -> 561, which EQUALS the A4 total (561). The global ts total is a sum over
by_model including the SMA, tax and custom lines (it is not the distribution's distinct-account total, 8417): a declared basis seam, not
reconciled, and not this change's to reconcile.
Denominators: global 20 by_model lines in the ts, 7 in the staged map, 14 in the A4 map; the 7 overlap and are all in `GLOBAL_MODEL_KEYS`.
Not moved by the override: the 13 other global lines (their counts compose from the legs / overlays and are not in the staged map).

Served fields that would move, from the first fire after the change: ts `by_model[<7 keys>].account_count[-1]` and `account_count_total[-1]` for the
three scopes; `meta.frontier_count.staleness` on 49financial (STALE -> FRESH or a few days); aum-metrics rows' `account_count` and `total.account_count`;
the gold parquet columns of the same cells. The Model Portfolios page's Total Holdings headline reads the A4 DISTRIBUTION's total and blend counts
(already fresh, 2026-10-12), so it does not move with this input.

## 3. Where the input can move to (build ladder)

Order in `build_all` (consolidator): the per-firm ts artifacts and the global ts are built first, with the frontier read at `:1203` / `:2520`; the
distributions are built afterwards by `build_firm_distribution(...)` (`dim_mdpf_account_distribution.py`) from account-level silver values. The
distribution builder does not consume the ts; only the FOLD's `fold_keys` flows ts -> global distribution (CN-f-1, step 3a).

(a) **Read the lambda's own previous A4 distribution** instead of the staged object: change the key at `:786` to the newest
`portal/gold/mdpf/{firm_id}/account-distribution/<date>.json` (list the prefix, take the max key <= the axis date, or the newest), read the same
`meta.account_count_by_model_key` and `period`. One function, about 15 lines, no new writer. Vintage: the previous run's roster; `period` is
declared, so ROW 11 states the lag (A4 2026-10-12 has period 2026-10-12 against a 2026-10-09 axis today: the declared AHEAD_OF_AXIS or lag verdict
is the existing law, and `_assert_cross_axis_coherence` clause (vi) already refuses a foreign-day roster as a gate). Circularity: none new; the
distribution is independent of the ts. After CN-f-1 the global A4 is FOLDED: `meta.account_count_by_model_key` drops the folded keys and gains
`other_models`, so the two blend keys would no longer be mapped and keep their composed-from-legs counts (which equal inflection's: 160 and 23, the
seam of the 162-versus-160 vanishes). The firm scopes' A4 are never folded.
(b) **Build the distribution in-run before the ts**: an unfolded distribution built first, feeding the frontier, then the ts, then the fold, then the
folded distribution: two builds of the distribution per run and a re-ordering of `build_all`. Same vintage as the run (the freshest), but a larger
change to the shared build and to the isolation of Global; not the minimum.
(c) **The lambda writes the staged object itself** (a `stage_put` of the UNFOLDED distribution after the build, taking over stage 6b's role):
the same one-run lag as (a), plus a new writer and a second copy of the distribution in the staging tree that the retirement (M12) must then remove.
It is the most code and keeps the object the CTO wants moved off.

**Recommendation: (a).** It deletes the dependency on a runner object, adds no writer, and keeps the existing declared-staleness mechanism; the
fold interplay is benign. The one design fork to put to the CTO inside it: the `period` of the newest A4 is the RUN date (2026-10-12) while the
ts frontier is the previous trading day (2026-10-09); either accept the declared one-day-ahead roster (the stamp's as-of is declared in band) or
select the newest A4 whose period is <= the axis date (a one-trading-day-older roster, a FRESH verdict at the cost of one more day of lag).
What CN-d-1 and CN-f-1 already do to this path: CN-d-1 added `meta.cottonwood_fold.value_date` / `age_trading_days` to the A4 distribution (the
cottonwood account-units sidecar's own vintage) and does not touch this read; CN-f-1 keeps the STAGED object unfolded "by design" because the runner
CLI passes no fold and the consolidator never writes it, which is moot while stage 6 is dead (the object is frozen at 2026-08-17).

## 4. What the priced pair must name

- **Blast radius:** the last-date `account_count` of the keys named in the table and `account_count_total[-1]` on the ts of the three scopes (global,
  49financial, inflection) from the first new-date fire onward; the same cells in aum-metrics and the gold parquet; `meta.frontier_count` on the
  firm ts. NOT: any value or headline array, any dated key already served (write-once), the staged tree, the A4 distributions themselves.
- **N writers of the property "frontier account_count":** the two override sites `:1232-1233` (per-firm) and `:2622-2623` (global); the SMA
  count-preserve loop (`:2630-2639`, carries a last count under `count_as_of`, unchanged); the W-7 `account_count_total` producer (`:2693-2712`); the
  aum-metrics row and total builder; the gold parquet writer: 6 writers, 5 leaf classes. (Recount at the pin before signing.)
- **Branches:** frontier read present and FRESH/STALE (stamped, builds); absent (WARN, frontier honest-None, a coherence RESET the gate catches); read
  failure (raises, refuses the scope's artifact as today); a roster ahead of the axis (clause (vi) refuses Global alone under CN-d-1's isolation).
- **Rollback per key:** the dated A4 objects are write-once (no prior version; a bad first object is answered by the next fire and the pair's
  branches, never a delete); the code and the lambda package roll back by VersionId as in the CN-d-1 and CN-f-1 orders.
- **The delta table:** section 2, with its denominators, signed by the CTO as the accepted served-number change (+424 global total, +334, +13).
- **Sequencing:** the fold deploy (`ADHOC.canon-r6-fold-deploy`, waiting on W8-S4) changes `dim_mdpf_aggregate_aua_timeseries.py`'s neighbours
  and the same lambda; one change per scheduled fire, so this change is a separate cell and a separate deploy after the fold's first scheduled
  fire has been read (2026-10-14 13:30Z at the earliest), i.e. its first fire is 2026-10-15 at the earliest. It is a code change to one file the
  fold does not touch, so it does not conflict at the merge.

## 5. Not read / not found

The per-firm A4 distributions' `period` semantics against the axis date beyond the one pair measured here; whether any consumer outside the repo
reads the ts frontier counts; the aum-metrics-to-platinum publisher's treatment of `account_count` beyond the equality measured above.
