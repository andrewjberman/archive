# ADVI_BDPARITY.P1-PROBE — BP1-2 the probe table + BP1-3 named mechanisms

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T03:3xZ (read) | **Cohort:** `4.0.0_SA_CRO` @`7cd0cc1200`
**Harness:** `ADVI_BDPARITY_BP1-2_probe_table_20260830.py` (re-runnable)
**BD side:** bronze `pull_date=2026-08-30`, the ONE pull Andrew authorised, fired 03:05:19–03:05:40Z. **No second call.**
**Our side:** `twr_daily`, **GOLD VINTAGE 2026-08-30T03:22:17Z** — the settled post-re-emission baseline (535 of 535, campaign complete 03:22:43Z). 411 partitions loaded over 2025-01-01..2026-08-28.

## The table — 20 cells (5 accounts × 4 ruled periods)

| account | period | requested | returned | match | outcome | ours | BD | delta | our days | BD days |
|---|---|---|---|---|---|---|---|---|---|---|
| 0022312917 | QTD | 07-01..08-28 | 07-01..08-28 | ✔ | COMPUTED | -0.001472 | 0.003928 | **-0.005400** | 36 | 42 |
| 0022312917 | YTD | 01-01..08-28 | 01-01..08-28 | ✔ | COMPUTED | -0.001966 | 0.016236 | **-0.018203** | 159 | 165 |
| 0022312917 | 1Y | 2025-08-28.. | 2025-08-28.. | ✔ | COMPUTED | 0.010141 | 0.026672 | **-0.016531** | 245 | 252 |
| 0022312917 | SI | 07-01..08-28 | 07-01..08-28 | ✔ | **NO-COVERAGE** | — | 0.003928 | — | — | 42 |
| 0038836097 | QTD | 07-01..08-28 | 07-01..08-28 | ✔ | COMPUTED | 0.044008 | 0.030349 | **+0.013660** | 36 | 42 |
| 0038836097 | YTD | 01-01..08-28 | 01-01..08-28 | ✔ | COMPUTED | 0.131540 | 0.116205 | **+0.015335** | 159 | 165 |
| 0038836097 | 1Y | 2025-08-28.. | 2025-08-28.. | ✔ | COMPUTED | 0.190441 | 0.178192 | **+0.012249** | 245 | 252 |
| 0038836097 | SI | 07-01..08-28 | 07-01..08-28 | ✔ | **NO-COVERAGE** | — | 0.030349 | — | — | 42 |
| 0010083855 | QTD | 07-01..08-28 | 07-01..08-28 | ✔ | COMPUTED | 0.016617 | 0.012514 | **+0.004102** | 36 | 42 |
| 0010083855 | YTD | 01-01..08-28 | 01-01..08-28 | ✔ | COMPUTED | 0.095522 | 0.091101 | **+0.004421** | 159 | 165 |
| 0010083855 | 1Y | 2025-08-28.. | 2025-08-28.. | ✔ | COMPUTED | 0.144626 | 0.140636 | **+0.003990** | 245 | 252 |
| 0010083855 | SI | 07-01..08-28 | 07-01..08-28 | ✔ | **SI-WINDOW-NOT-AT-ANCHOR** | — | 0.012514 | — | — | 42 |
| 0027265115 | QTD | 07-01..08-28 | 07-01..08-28 | ✔ | COMPUTED | 0.050638 | 0.026385 | **+0.024253** | 36 | 42 |
| 0027265115 | YTD | 01-01..08-28 | 01-01..08-28 | ✔ | COMPUTED | -0.046430 | -0.057099 | **+0.010669** | 107 | 116 |
| 0027265115 | 1Y | 2025-08-28.. | 2025-08-28.. | ✔ | COMPUTED | -0.046430 | -0.057099 | **+0.010669** | 107 | 116 |
| 0027265115 | SI | **03-16**..08-28 | **03-16**..08-28 | ✔ | **COMPUTED** | -0.046430 | -0.057099 | **+0.010669** | 107 | 116 |
| 0076459710 | QTD | 07-01..08-28 | 07-01..08-28 | ✔ | COMPUTED | 0.087360 | 0.127830 | **-0.040470** | 31 | 38 |
| 0076459710 | YTD | 01-01..08-28 | 01-01..08-28 | ✔ | COMPUTED | 0.087360 | 0.127830 | **-0.040470** | 31 | 38 |
| 0076459710 | 1Y | 2025-08-28.. | 2025-08-28.. | ✔ | COMPUTED | 0.087360 | 0.127830 | **-0.040470** | 31 | 38 |
| 0076459710 | SI | 07-01..08-28 | 07-01..08-28 | ✔ | **SI-WINDOW-NOT-AT-ANCHOR** | — | 0.127830 | — | — | 38 |

**DENOMINATORS: 20 cells · `range_match` TRUE 20 of 20 · both values present 18 · COMPUTED 16 · NO-COVERAGE 2 · SI-WINDOW-NOT-AT-ANCHOR 2.**
**SI denominator: 1 computed / 2 window / 2 coverage, of 5** — exactly `3.0.0_SA_CVO` ANNOTATION 3's ruled vocabulary.

## BP1-3 — the named mechanisms

### 1. The day-count gap is FULLY accounted, residual ZERO
```
period  ours   BD    gap    5-day hole (08-11..08-17) + all-null 08-18 = 6    1Y boundary +1    RESIDUAL
QTD      36     42     6                          6                                  –              0
YTD     159    165     6                          6                                  –              0
1Y      245    252     7                          6                                 +1              0
```
**No unexplained remainder on any period.** The hole and the all-null 2026-08-18 are ours; the extra 1Y day is a convention difference we authored (below).

### 2. ⛔ A ONE-DAY BOUNDARY MISMATCH WE CREATED OURSELVES
The **puller** requests 1Y from `q_end` minus one year = **2025-08-28**. Our **linker** opens 1Y the day after = **2025-08-29** (so exactly one year of daily returns links). **We ask BD for one window and compute our own over another.** It is small, one-signed, and lands at the open — the exact TIGHT-never-EXACT signature the taxonomy reserves for a convention mismatch. **It is a DEFINITION delta, not a calculation delta, and it is ours, not BD's.** Not tuned here (P3 is the convention gate); named, and it explains the 1Y column's extra day precisely.

### 3. Every delta is SIGNED and not absolute
Deltas run **-0.040470 to +0.024253**. **Both signs occur** — 0022312917 and 0076459710 read below BD, the other three above. A magnitude-only summary would have destroyed the axis carrying the defect.

### 4. The two inception-recent accounts return identical figures across YTD / 1Y / SI
0027265115 (inception 2026-03-16) and 0076459710 (2026-07-08) show the **same value for YTD, 1Y and SI**. That is correct, not a bug: the account did not exist before its inception, so all three windows collapse to the same lived period. It is also why an inception-recent member was required — it is the only cohort member where SI is separable at all.

## BP1-3 mechanism 1, AT THE CELL GRAIN — closing `3.0.0_SA_CVO` 85268's gap

That grade was right: "residual ZERO" held at the **period** grain and was **not shown** per cell,
where a **third term** appears. Decomposition now printed per cell:
`bd_days_held = our_days_linked + hole-in-window + anchor-day + OUR non-OK days + residual`

⛔ **MY FIRST RUN DOUBLE-COUNTED AND EVERY RESIDUAL READ -1.** I listed **2026-08-18** in the hole
AND it was already inside `days_neutral` — its partition EXISTS with all-null returns, so it is a
neutral day, not an absent one. **The hole is the 5 ABSENT trading days; 08-18 is a refusal.**
Corrected; the -1 vanished across the board.

| cells | residual | why |
|---|---|---|
| **8** (every QTD/YTD on a full-life account, + 0027265115 QTD, 0076459710 SI) | **0** | fully accounted |
| **3** (1Y on the full-life accounts) | **+1** | **the CTO-ruled boundary day** — our linker opens 1Y a day late. **Goes to 0 when 85237's fix lands.** A predicted residual, not an anomaly |
| 0010083855 SI | -274 | **incomparable by construction**: our SI runs from its 2025-05-28 inception (309 linked days), BD computed only the 07-01..08-28 fallback window (42). Already `SI-WINDOW-NOT-AT-ANCHOR` |
| 0027265115 YTD/1Y (-10), 0076459710 QTD/YTD/1Y (-4) | ≠0 | **different denominators, not a missing term**: BD counts only days the account was **HELD** (116, 38); we count days in the **requested window**. Both accounts began mid-window |

⭐ **THE THIRD TERM IS A VALUE-DELTA MECHANISM IN ITS OWN RIGHT, exactly as 85268 said:** on
0027265115's SI window our chain refuses days BD computed through (`UNCOMPUTABLE-ZERO-BMV` /
`REFUSED-NO-BMV` inside the window). **BD linked days we did not.** That is distinct from the hole,
invisible at the period grain, and a candidate mechanism for the value difference — not only the
count difference.

⚠ **AND THE STANDING LIMIT ON ALL OF IT:** the hole and the refusals explain **DAY COUNTS, not
VALUES**. A count mechanism becomes a value mechanism only when the missing days' returns are known.
Until the backfill supplies them, these are **CANDIDATE** mechanisms printed as such on every cell
they touch.

## The SI line, per account

| account | BD anchor (`level.startDate`) | first return day | branch | our first linkable | outcome |
|---|---|---|---|---|---|
| 0022312917 | 2023-03-24 | 2023-03-27 | bmv-zero-next-trading-day | — | NO-COVERAGE (pre-floor) |
| 0038836097 | 2024-06-10 | 2024-06-11 | bmv-zero-next-trading-day | — | NO-COVERAGE (pre-floor) |
| 0010083855 | 2025-05-28 | **2025-05-29** | bmv-zero-next-trading-day | **2025-05-29** | SI-WINDOW-NOT-AT-ANCHOR |
| 0027265115 | 2026-03-16 | **2026-03-17** | bmv-zero-next-trading-day | **2026-03-17** | **COMPUTED** |
| 0076459710 | 2026-07-08 | **2026-07-09** | bmv-zero-next-trading-day | **2026-07-09** | SI-WINDOW-NOT-AT-ANCHOR |

⭐ **THE BMV-0 RULE NOW HAS n=3, and the third and fourth instances come from a DIFFERENT INSTRUMENT.** `3.0.0_SA_CVO` stated it from BD's returned `beginningMarketValue` on one account. Here, **three accounts' first LINKABLE day in OUR gold lands exactly one trading day after their BD inception** — 05-28→05-29, 03-16→03-17, 07-08→07-09. That is our plane agreeing with a rule derived from BD's plane, which is corroboration rather than repetition.

**`3.0.0_SA_CVO`'s section-1 prediction held:** the two accounts failing on coverage are **the two oldest** (2023-03-24 and 2024-06-10, both before the 2024-07-08 gold floor). It landed as an outcome, not a defect.

## ⛔ THE PINNED BD BYTES ARE NOW CITED BY VersionId, NOT BY KEY

**W2 (the 5,309-account census, Andrew's word 18:0xZ) writes to FOUR OF THE FIVE SAME S3 KEYS as this
table's BD side** — same `pull_date=2026-08-30`, same `q_end`, same accounts (13477111, 18927251,
21089351, 22596361; only 23221671 is absent from the xref cohort). **A key is `{feed}_{account}_{q_end}`
and carries no pull identity**, so W2's response for those accounts becomes the CURRENT object.

**The bucket is versioned (Status: Enabled), so nothing is destroyed — but a citation BY KEY silently
starts resolving to different bytes.** This table's BD side is therefore pinned by **VersionId**, all
18 P1-era object-versions captured **BEFORE** W2 ran:
`ADVI_BDPARITY_P1_bronze_object_versions_20260830.json`. The five performance objects this table was
computed from are among them.

⚠ **Captured live, in the only window where it was possible.** After W2 the "latest" version is
W2's; recovering P1's would then require knowing a VersionId nobody had recorded. **Evidence that is
about to be shadowed has to be pinned while it is still current.**

## Bounds

- **`bd_annualized` is `False` on every cell** — read from BD's own `timeWeightedReturns.returnAnnualized`, never inferred from which of our figures matches. The ruled CUMULATIVE basis is confirmed against the vendor's own label.
- **Deltas are NOT classified into the §7 taxonomy here.** Thresholds need `4.0.0_SA_CRO`'s N-bp word; the seat is released and a classification without it would be a tolerance chosen by the measurer.
- **The C2 cell (0010083855) is graded UNAVAILABLE for the gross leg** until the re-emission's corrected `r_gross` is verified; `r_net` comparisons above are unaffected.
- **One vintage, stated:** our side is the post-re-emission baseline @2026-08-30T03:22:17Z. An earlier run of the first-appearance sweep read pre-re-emission bytes; the dates above are the post-campaign values.
