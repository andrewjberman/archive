# BP-c-2 -- the replay re-run on amendment R1.3 (round 3, third seat)

Worker `0.9.0_WK_ADVI_BDPRCE~21`, cell BP-c-2, read at `2026-10-14T05:21:48Z`. Read-only: no served object, no producer
run, no product file changed. Claim: measured. Record: `REPLAY3.json`. Scripts: `unit_map_pairs.py` (the served-unit map),
`replay_r1_amend3.py` (the replay), `verify_partitions.py` (the partition check). Both lists are reproducible from them.

| file | rows or bytes | sha256 |
|---|---|---|
| `BEFORE_AFTER3.csv` | 1,689 served rows, 375,728 bytes | `0dfcd23dd606db5fd6283d6564b09cf8e81e81fdb2138e7e5d60e7ea12bd937a` |
| `ESTIMATED_ROWS3.csv` | 18,397 interpolated rows, 2,669,727 bytes | `8c07ccc1167c816e74b25349bb2532742fa71199cbde372170b01535527c94dc` |
| `UNIT_MAP.csv` | 888 assets | `c47ce738cd1ca34b132d785704a210f5528accacf3dbe4d02c9309c50428435e` |
| `PARTITIONS3.csv` | 1,928 dated partitions | (verifier output) |

## What changed, in plain words

The CTO's amendment 3 says a price may change its value but an asset may not change its unit. Round 2 and the second
seat let the par bond MORGAN STANLEY FIN LLC 0% 05/03/2029 read 1.0 per unit where its served series is per 100, which
is a 100 times move. R1.3 reads each served asset's unit from that asset's own served prices, and withholds a Fixed
Income row whose unit it cannot read instead of guessing. This replay re-runs the amended rule over the served window.
Nothing served is changed.

## The window and the served set

Window 2026-09-16 to 2026-10-13: 20 weekdays. The canonical object was read again: ETag `a88a7030f4506ac7e0cdb844382f9d16`,
LastModified `2026-10-14T04:03:36Z`, 110,077,599 bytes, md5 equal to the ETag. It holds **1,689** `transaction_observed`
rows over **888** assets, with no duplicate asset-date. Against the sets the order names:

- round 2 read 1,657 rows: all 1,657 are still present with their prices; 32 are added;
- the second seat read 1,664 rows (ETag `8eaa29e3...`): 1,658 keys are common, 31 are added, and **6 are gone**
  (the CASH AND MARGIN  INTEREST rows of 2026-09-24, 09-25, 09-29, 09-30, 10-06 and 10-12). Their 21 interpolated rows
  are gone too. Surprise row `ADVI_BDPRCE-D1-W21-S1`.

The served set is therefore the 1,689-row set, and the comparisons below use the 1,658 common keys where a pair is needed.

## Partitions

`PARTITIONS2.csv` (the second seat) verified 1,928 partitions. At this read three cached copies no longer matched their
S3 head-object size (2026-10-02, 2026-10-08, 2026-10-11) and 2026-10-14 was absent from the cache. Four partitions were
fetched with get-object and each md5 equals its head ETag. The final manifest, `PARTITIONS3.csv`, reads 1,926
`VERIFIED_MD5` and 2 `VERIFIED_SIZE_MULTIPART` (multipart ETags cannot be md5-checked; the verifier names them). The
replay keys on these 1,928 partitions. Surprise row `ADVI_BDPRCE-D1-W21-S4`.

## The served-unit map (UNIT_MAP.csv)

Pairs are taken by priority, one source per asset: (1) the served row against the same-date Buy, Sale or reinvestment
trades; (2) for an asset with no such pair, the nearest earlier trade row; (3) for an asset with neither, the lot extract
(sha256 checked: `e7e618d7...2b50b`). The module's `served_unit_map` takes the median per asset over the pairs of that
one source.

| unit | assets | resolved by | assets |
|---|---|---|---|
| per100 | 1 (MORGAN STANLEY FIN LLC 0% 05/03/2029, median 115.995) | same-date trade | 744 |
| per_unit | 827 | nearest earlier trade | 43 |
| unreadable | 60 (59 with no pair, 1 with a between-band median) | lot extract | 42 |
| total | 888 | no pair | 59 |

`served_units` = `{"assets": 888, "per100": 1, "per_unit": 827, "unreadable": 60}`. Against the pooled probe of BP-c-1
(1, 824, 63): ISHARES CORE U.S. AGGREGATE BOND ETF now reads per unit from its 12 same-date trades (the lot pairs no
longer set it), and CALL NVIDIA CORP $250 EXP 10/02/26, VANGUARD FTSE ALL-WORLD EX-US SMALL-CAP ETF and VISTANCE NETWORKS
INC COM read per unit from trades. SIX FLAGS ENTERTAINMENT CORP COM moves the other way (one earlier trade at 0.370, so
unreadable; it is an Equities asset and its rows keep their price). Surprise row `ADVI_BDPRCE-D1-W21-S5`.

## Results

| class | round 2 (1,657) | second seat, R1.2 (1,664) | R1.3 (1,689) |
|---|---|---|---|
| UNCHANGED | 621 | 731 | **747** |
| CHANGED | 539 | 585 | **599** |
| NOW_CARRY_FORWARD | 285 | 160 | **160** |
| NOT_RECOMPUTABLE | 212 | 188 | **183** |

Prices that move: 759 rows (599 changed, 160 carry-forwards), of which 754 differ from the served value (5 carry-forwards
equal it). On the 1,658 common keys, the new price differs between the second seat and R1.3 on one row only, MORGAN
STANLEY on 2026-10-05 (1.0 becomes 100.0). One row changes class with no price change: GLOBAL X S&P 500 TAIL RISK ETF on
2026-10-12, whose served value is now 29.349 where the second seat read 29.34904, so the same R1 price is now UNCHANGED.

Round 2 to R1.3 on the served rows: of round 2's 285 carry-forwards, 43 now price from a trade and move (CHANGED), 81
price from a trade equal to the served value (UNCHANGED), 156 remain carry-forwards, and 5 are withheld.

**unit_changed_rows = 0.** No served CHANGED or NOW_CARRY_FORWARD row has a new/old ratio within 1 percent of 100 or of
0.01.

**unit_withheld_rows = 19.** These are served rows of Fixed Income assets whose unit is unreadable (they have no pair at
all). Each is NOT_RECOMPUTABLE with reason `unit_unreadable`; in the second seat each was `no_earlier_trade`, so no
price is lost. The assets: AMERICAN FUNDS CAPITAL WORLD BD F-3; BARCLAYS BANK PLC 08/19/2030; BARCLAYS BANK PLC
08/26/2031; BNP PARIBAS 01/23/2031; BNP PARIBAS 06/11/2029; BNP PARIBAS 12/03/2029; CITIGROUP GLOBAL MKTS HLDGS IN
05/28/2031; CITIGROUP GLOBAL MKTS HLDGS IN 06/10/2031; CITIGROUP GLOBAL MKTS HLDGS IN 07/29/2030; FRANKLIN CORE PLUS BOND
FUND R6; GS FIN CORP 02/28/2031; GS FIN CORP 03/25/2031; GS FIN CORP 04/10/2031; GS FIN CORP 10/10/2030; GS FIN CORP
12/20/2030; MASCHINENFABRIK BERTHOLD HERML PREF SHS VTG RTS; PIMCO LOW DURATION A; SOCIETE GENERALE 07/07/2031; SOCIETE
GENERALE 09/19/2031.

The other classes: `NOT_RECOMPUTABLE` 183 = 151 `no_earlier_trade`, 19 `unit_unreadable`, 3 `ratio_unrecognised_carry`,
10 `ratio_unrecognised`.

## Par-quoted rows

The eight round-2 `scale_100x` rows: **8 of 8 are UNCHANGED** (`par_quoted_rows` 8, `par_rows_unchanged` 8).

## Withheld census (the comparison the order asks for)

| | second seat (R1.2) | R1.3 |
|---|---|---|
| withheld Fixed Income trade rows, window | 442 | 12,070 |
| assets with a withheld row | 25 | 102 |
| on the 14 served assets (ratio withholds) | 14 assets, 383 rows | 14 assets, 383 rows |
| on the non-served Fixed Income assets | 11 assets, 59 rows (ratio) | 88 assets, 11,687 rows (`unit_unreadable`), including those 11 assets' 59 rows |

The 88 non-served assets are Fixed Income names the served map does not carry. The module reads an asset missing from
the map as unreadable, so their rows are withheld. Nothing served or interpolated uses them. The census is therefore
larger for a reason that changes no list value. Surprise row `ADVI_BDPRCE-D1-W21-S2`.

## Interpolated fates

The 18,397 window canonical `linear_interpolation` rows on the served assets (887 assets) take these fates:

| fate | second seat | R1.3 |
|---|---|---|
| `trade_price` | 29 | **0** |
| `last_traded_date` (carry, with its observation date) | 15,997 | **16,025** |
| `unresolved` | 2,394 | **2,372** |

The three sum to the row count in each case. The `trade_price` rows of the second seat are on 2026-10-12, and their
assets are now observed rows in the object read here; the 16,025 carry rows include 777 dated on days with no
store rows. Unresolved, R1.3: 2,120 `no_earlier_trade`, 126 `unit_unreadable` (Fixed Income assets with an unreadable
unit), 126 `ratio_unrecognised_carry` (a last trade withheld on its ratio). The 51 second-seat rows that are no longer
interpolated are 21 CASH AND MARGIN  INTEREST rows and 30 rows now observed; 28 rows are new.

## MORGAN STANLEY FIN LLC 0% 05/03/2029

- Its only trade in the store with a qualifying or withheld row is the Buy of 2025-05-28, executed at 100.0 (the
  served series is per 100, so the price is kept as executed).
- **2026-10-05 now reads 100.0**, NOW_CARRY_FORWARD from **2025-05-28**, with that observation date. Against the served
  115.995 and the second seat's 1.0.
- The 27 window interpolated rows of the asset (2026-09-16 to 10-13) all carry 100.0 from 2025-05-28 (second seat: 1.0).
- The order names 214 interpolated carries. This read finds 27 in the window and 503 canonical interpolated rows for the
  asset over its history (2025-05-29 to 2026-10-14, of which 476 lie outside the window and are not fated by this
  replay). The basis of 214 is not reproduced. Surprise row `ADVI_BDPRCE-D1-W21-S3`.

## The three largest movers (by price move, carry-forwards and changes)

1. WATSCO INC COM, 2026-09-17: 305.36 becomes 432.39 (+127.03, +41.6 percent). Carry from 2026-04-28.
2. ASML HLDG NV N Y REGISTRY SHS, 2026-09-22: 1,741.1912 becomes 1,650.835 (-90.36, -5.2 percent). Carry from 2026-09-18.
3. MICRON TECHNOLOGY INC COM, 2026-09-22: 1,096.16 becomes 1,032.1201 (-64.04, -5.8 percent). Carry from 2026-09-21.

The largest percentage move is QORVO INC COM, 2026-10-06: 39.772 becomes 79.33 (+99.5 percent), a carry from 2026-04-13.
Its ratio is about 2, not 100, so it is not a unit move; it is stated as measured. The largest percentage move among
changed (trade) rows is REGAN TOTAL RETURN INCOME INSTITUTIONAL, 2026-10-07, +19.7 percent.

## Round 1 rows

The 64 round-1 UNEXPLAINED rows: 60 CHANGED, 4 UNCHANGED. Of the 19 that recompute to 1.0: 17 CHANGED, 2 UNCHANGED.
Each row's amended class and price are in `BEFORE_AFTER3.csv` (columns `round1_class`, `round1_recomputed`, `new_price`).

## Lookback and keying

Mode `trade_date_all_partitions`. Keyed on trade_date across all 1,928 verified partitions (2020-03-06 to 2026-10-14):
1,980 trade dates in the store. The one window weekday with no trade in the store is 2026-10-13 (no partition); its
interpolated rows carry the last trade before it. Late-landed rows: 226,319 in total, 58,226 of them more than one day
late. The 2026-10-14 partition holds 2,921 rows dated in the window and is keyed here, as in the second seat.

## Determinism and the past-date arm

The replay ran in two separate processes. Both wrote `BEFORE_AFTER3.csv` with md5 `3f0de9889ca0748fe0235dadf8834db2`, and
`peer_md5_equal` is true. The in-process second pass is equal too. Past-date arm: for the first 20 CHANGED rows, the
result for the date from trades on or before that date equals the full result, and all 20 use trades on that date only.

## Limits and what stays unknown

- The list keys on a canonical object and a partition set that were rewritten during this read. The 2026-10-14 partition
  is the current day's file and may change again.
- The unit map rests on the pairs available. Each asset's unit is its median ratio over one source (a trade or a lot). A
  unit read from one earlier trade (for example SIX FLAGS, median 0.370) is only as good as that trade.
- Fixed Income withholding is now by unit as well as ratio. The 88 non-served assets change the census, not the list.
- The 214 figure of the order is not reproduced; the MORGAN carry count is stated above.
- Whether a carry-forward should refuse a withheld last trade date (3 served rows, 126 interpolated) is still the CTO's
  question, as in the second seat.
