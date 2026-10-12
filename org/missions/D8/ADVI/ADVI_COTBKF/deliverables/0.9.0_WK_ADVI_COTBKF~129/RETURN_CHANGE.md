# ADVI_COTBKF.TO-CB-bv-3 -- the first return number (worker 0.9.0_WK_ADVI_COTBKF~129, round 74)

Nothing was served, applied or written to any bucket. No product file was edited. No vendor call. S3 was read only, and only the reads the chain itself makes. Build outputs are in the worktree's ignored `.scratch/w129/` and are not committed.

## Headline

For the 19 validated funds whose price moved (of 33 validated; the other 14 were already on the cached close and did not move), 1,575 of 107,316 account-days measured in both builds change (residue floor 1e-9 of return): 1,054 under 1 basis point, 425 from 1 to 10, 96 over 10. **This is for the validated funds only and is not the size of the whole defect: 237 of 270 fund series are not validated and are not in this number.**

Only 5 of the 19 moved funds (ANCFX, BALCX, CAIBX, CWGIX, FCNTX) are held on any account-day measured in both builds. The other 14 funds change price, but no measured-in-both account-day holds them.

## 1. The baseline reproduces the served table (read first)

| | served (fwd3_serve_r34) | baseline (this worker, method_r28 at the pin) |
|---|---|---|
| rows | 1,691,729 | 1,691,729 |
| measured rows (non-null return) | 107,316 | 107,316 |
| account-days whose return differs beyond 1e-12 | | 0 |
| measured in one only | | 0 / 0 |
| blank reason differs | | 0 |

`baseline.reproduces = true`. The baseline also equals w104's `fwd3_method_r28/daily_returns.parquet` exactly (0 differing, same measured set, same blank reasons), and its price input has the same sha256 as w104's (`fe9d1c04...`). The price stores were re-read from S3 today (the gold holdings store has 579,580 rows now, 564,563 in w104's cache); that did not reach a return.

## 2. How the two builds were made (no code edit)

The valuation reads its census from the module constant `BASIS_CENSUS` in `commonwealth_daily_valuation.py`; `load_basis_classes(path=None)` falls back to that constant, and the chain passes no path. There is no flag and no environment variable. So both builds run through one scratch wrapper, `.scratch/w129/regrade_wrapper.py`, which imports the valuation module, sets `dv.BASIS_CENSUS = Path(argv[1])`, then calls `commonwealth_sweep_regrade.main(argv[2:])`. The baseline passes the original census path (`.../0.9.0_WK_ADVI_COTBKF~60/price_basis_census.csv`), the variant passes the copy. The two builds differ in the census file alone.

Each leg (`.scratch/w129/run_leg.sh <baseline|variant> <census>`), with `COTBKF_SWEEPS_CONFIG` set to the commonwealth config:

```
python .scratch/w129/regrade_wrapper.py <census csv> --before-list v1 --after-list v1 \
  --before-cash-leg method_r28 --after-cash-leg method_r28 --before-price-basis store --after-price-basis as_traded \
  --data-dir .scratch/w129/<leg> --out .scratch/w129/<leg>_out --cache C:/dev/ajb_workspace/.scratch/advi_cotbkf/cache \
  --price-cache .scratch/w129/price_cache_<leg> --price-input-out .scratch/w129/<leg>_price_input.parquet \
  --split-store-as-of 2026-10-09T11:52:52Z --yahoo-cache C:/dev/ajb_workspace/.scratch/advi_cotbkf/yahoo_census

python data/assets/scripts/silver/commonwealth_fwd3_serve.py --build --data-dir .scratch/w129/<leg> --out .scratch/w129/fwd3_<leg> \
  --grades .scratch/w129/<leg>_out/month_grades_after.parquet --grades-before .scratch/w129/<leg>_out/month_grades_before.parquet \
  --cache C:/dev/ajb_workspace/.scratch/advi_cotbkf/cache --cash-leg method_r28 --price-basis as_traded
```

`--build` writes three local tables (the code's `build` path; the S3 write is the separate `--apply` mode, not run). Split store pin printed by both legs: `as_of=2026-10-09T11:52:52Z listed=32 held=32 sha256=4aca4f1fa311...`; Yahoo cache pin: 3,580 files, sha256 `5b4bb7db...`. Both legs ran in parallel, about 10 minutes for the regrade and 9 for the build; tree head `b6ab4e69c9`.

The analysis is `.scratch/w129/analyze.py`.

### The census copy

The copy is the original `price_basis_census.csv` (3,580 rows, keyed by ticker) with the class of the 19 validated left-on-store tickers set to `dividend_adjusted`. Each of the 19 has a census row (0 without one). A line diff of copy against original shows exactly 19 changed lines, one column (`class`), nothing else:

| ticker | from | to |
|---|---|---|
| ABNFX, AMRMX, ANCFX, AWSHX, BALCX, CAIBX, CPXIX, CWGIX, DFLVX, DFREX, DISVX, FCNTX, FINFX, MEIIX, PRILX, VEIRX, WGIFX, WMFFX | other | dividend_adjusted |
| ACTDX | as_traded | dividend_adjusted |

Original sha256 `65128047...`; copy `c91f33db...`. The price-basis line shows the substituted tickers 911 -> 930 (+19), points replaced +24,643, days re-derived +11,216, days dropped (unbracketed) +76.

## 3. What the variant moved

- Securities whose price differs between baseline and variant: **19, exactly the 19 left-on-store validated funds; other securities moved: 0.** 34,277 security-days have a different close; 60 security-days are dropped (4 each for 11 funds, 2 each for 8); 0 added. In the price input, 76 rows are removed (4 per fund, days the basis cannot bracket by a replaced point on both sides).
- Every one of the 19 moved. 18 moved by a changed closing price (1,424 to 2,088 security-days each) and by dropped days; ACTDX moved only by its 4 dropped days (its census class was already `as_traded`: no closing price differs).
- Control, the 14 already-substituted funds (26,507 security-days): 0 prices changed, 0 days dropped or added.

## 4. The return number

Over the 107,316 account-days measured in both builds (floor: an absolute difference in daily return above 1e-9; 105,632 are exactly equal; 109 differ by a non-zero amount at or below the floor, the largest 1.8e-10, and are not counted):

| | account-days |
|---|---|
| changed | **1,575** |
| under 1 bp (< 0.0001) | 1,054 |
| 1 to 10 bp (0.0001 to 0.001) | 425 |
| over 10 bp (> 0.001) | 96 |
| sum of the three | 1,575 |

Of the 1,054 under 1 bp, 46 are between 1e-9 and 1e-7, 171 between 1e-7 and 1e-6, 837 above 1e-6. The largest change: **882.0 bp on 2025-10-24, fund FCNTX held** (the next two are 881.7 and 216.2 bp).

- Measured in the baseline and blank in the variant: **0**. Blank in the baseline and measured in the variant: **8** (baseline reason DVR_CLOSE_STEP 4, UNPRICED 4). Blank in both with a different reason: 348 (DVR_CLOSE_STEP -> UNPRICED 346, UNPRICED -> DVR_CLOSE_STEP 2).
- Month grades (82,593 account-months, same set in both): verdict changed on 30 (DIFF -> MATCH 25, UNGRADABLE -> MATCH 4, MATCH -> DIFF 1); computed percent changed on 77 (floor 1e-7 percentage points). There is no account-year grade table. A year chain of this worker's own (product of 1+return over the measured days): 1,823 account-years with the same measured days in both builds, 12 change (1 under 1 bp, 4 from 1 to 10, 7 over 10); 4 account-years have different measured days.

## 5. Where the changes sit

By fund (an account-day that held two moved funds is counted under each: 1,214 hold one, 361 hold two, the table sums to 1,936). A fund counts as held on the changed day or the account's previous valued day.

| ticker | account-days changed | under 1 bp | 1 to 10 bp | over 10 bp |
|---|---|---|---|---|
| FCNTX | 792 | 768 | 15 | 9 |
| BALCX | 422 | 229 | 161 | 32 |
| CWGIX | 361 | 57 | 249 | 55 |
| ANCFX | 312 | 42 | 221 | 49 |
| CAIBX | 49 | 15 | 28 | 6 |
| the other 14 moved funds (ABNFX, ACTDX, AMRMX, AWSHX, CPXIX, DFLVX, DFREX, DISVX, FINFX, MEIIX, PRILX, VEIRX, WGIFX, WMFFX) | 0 each | 0 | 0 | 0 |

By year of the changed day: 2022: 613, 2023: 170, 2025: 691, 2026: 101 (none in other years).

On or off a distribution date (custodian posting dates, types dv, dvlt, dvst, dvr, of the moved funds, fund level: 613 dates; ex-dates are not on disk): **on 20, off 1,555.** On a distribution date: 4 under 1 bp, 8 from 1 to 10, 8 over 10 (2022: 14, 2023: 2, 2026: 4). Direction: of all 1,575 the variant return is lower on 747 and higher on 828; on a distribution date lower on 11 and higher on 9; off a date lower on 736 and higher on 819; of the 96 over 10 bp, lower on 52 and higher on 44. The numbers show no one direction.

## Not established

See `not_established` in `RETURN_CHANGE.json`: validated funds only (237 of 270 unsized); only 5 funds carry measured exposure; one build against another, not a statement of which price is right; posting dates not ex-dates; the year line is not a Commonwealth grade; price stores unpinned except the split store; no cause is given for any single change.
