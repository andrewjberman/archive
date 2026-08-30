# ADVI_BDPARITY.P1-PROBE — BP1-4: the census design the P2 full-population run inherits

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T04:0xZ (read) | **Vintage of every number: gold @2026-08-30T03:22:17Z** (post-re-emission, campaign complete 535/535)
**Status:** design half COMPLETE. **The classification-threshold slot is PENDING-CRO and is NOT filled by this seat** — a tolerance chosen by the measurer is the one act the probe is forbidden.

## 1. POPULATION, with denominators

| population | count | source, settled vintage |
|---|---|---|
| accounts in `twr_daily` on 2026-08-28 | **7,370** | the day's partition, post-re-emission |
| of those, `r_net` non-null (linkable) | **6,436** | 87.3% |
| `UNCOMPUTABLE-ZERO-BMV` | 924 | status vocabulary |
| `NO-PRIOR-BALANCE-ACCOUNT-ABSENT` | 10 | |
| accounts in `canonical_positions` 08-28 | 6,185 | candidates table §4 |
| history depth | **535 date partitions**, 2024-07-08 .. 2026-08-28 | 1,070 objects, 118.2 MB |

**The P2 denominator is 7,370, not 6,436** — a non-linkable account is a CELL OUTCOME, not an exclusion. Reporting only linkable accounts would delete the population the probe most needs to see.

## 2. ENDPOINTS, and the cost that is not obvious

`/portfolioreporting/api/performance/performancePeriod` is the only endpoint the parity question needs. The vehicle also pulls `costBasis` and `allocation` — **3 calls per account**, measured on this probe (5 accounts → 15 objects). **A 7,370-account census on the current vehicle is ~22,110 vendor calls.** If P2 needs only performance, the vehicle needs a per-feed selector it does not have today; that is a build item, named here so the census is not costed at one call per account.

⭐ **THE ANCHOR COST — the census-design fact that ANNOTATION 3 asked be printed as a P2-1 line.**
A true SI value requires the SI range **requested at the account's own inception** (`level.startDate`). **That value exists only INSIDE a response.** So per account SI parity costs **either** a prior anchor-read call **or** a second call after reading the anchor — i.e. **SI doubles the census's call count**, or needs an anchor source we do not have outside BD. **QTD / YTD / 1Y cost one call; SI costs two.** A census budgeted at one call per account silently drops SI for the entire population.

## 3. RUNTIME — measured, not extrapolated

| operation | measured |
|---|---|
| metadata-only schema pass, all 535 partitions | **67.8 s** |
| full sweep with per-partition read, all 535 | **156 s** |
| 411-partition load filtered to 5 accounts | inside one run |

⛔ **RUNTIME IS NOT THE CONSTRAINT AND NEVER WAS.** The prior estimate ("37 partitions in 0.2 s, so 535 is seconds") was right about time and silent about the thing that matters — see §4.

## 4. THE LOADER CONTRACT — non-negotiable, and it is why the estimate was insufficient

**A bare full-history `to_table()` RAISES**: `Unsupported cast from double to null`. Three partitions (**2024-07-08, 2025-01-09, 2026-08-18**) carry a **reduced schema** — `r_net`/`r_gross` null-typed and `bmv`/`emv`/`cf_net`/`cf_gross` **ABSENT** (11 columns vs 15 on the settled vintage; 10 vs 14 pre-re-emission). **A cast is insufficient — it cannot conjure an absent column.** The census MUST read a fixed column subset per fragment and concatenate, or declare a unified schema.
**This failure only exists in the UNION**, so it is invisible to every load smaller than one spanning both shapes. **It survived the re-emission** — the three are still all-null after 535/535 were rewritten, so it is a data property, not an emission-time gap.

## 5. THE REQUEST-SIDE HOLE MANIFEST — carried beside every affected cell

**2026-08-11 .. 2026-08-17 is a 5-trading-day hole**, plus **2026-08-18 all-null** = **6 days** absent from any window spanning them. Measured against BD on the probe: QTD 36 vs 42, YTD 159 vs 165 — **gap exactly 6, residual ZERO**. 1Y gap 7 = 6 + the one-day open-boundary term now RULED out by `1.0.0_SA_CTO` 85237.
**Every P2 cell whose window spans that range carries the hole as a NAMED MECHANISM with its day count**, never as an unexplained delta.

## 6. PERIOD CONVENTION — ruled, one rule for all four periods

`1.0.0_SA_CTO` 85237 (P3-3): **a period `[start, end]` links every trading day's return from start THROUGH end inclusive; the base is the close of the trading day BEFORE start; a period whose start precedes coverage is NO-COVERAGE, never opened late.** The linker's 1Y open moves to this rule (request side unchanged, no re-pull). **Expected on these bytes: 1Y `days_linked` 246, the +1 residual → 0, and the 1Y deltas move by one day's return — to be stated SIGNED, before/after.**

## 7. OUTCOME VOCABULARY — MECE, in test order

Coverage first (a permanent property of the account), then window, then value:

| outcome | meaning | P1 count (of 5 SI cells) |
|---|---|---|
| `UNAVAILABLE-NO-COVERAGE` | anchor precedes our gold floor | **2** |
| `UNAVAILABLE-SI-WINDOW-NOT-AT-ANCHOR` | anchor known; BD computed the fallback window | **2** |
| `COMPUTED` | comparable | **1** |
| `UNAVAILABLE-NO-ANCHOR` | reserved: a response with no `level.startDate` | 0 |
| `UNAVAILABLE-RANGE-MISMATCH` | requested ≠ returned at the joined index | 0 on P1 (20 of 20 matched) |

**The join is `(requested_index, returned startDate, returned endDate)`** — BD returns `name: null` and `type: null` on every range, so position finds the cell and the dates certify it. **The census re-checks the order signature per response and refuses the whole response if it changes** (an order change is instrument failure, not a data finding).

## 8. ⛔ CLASSIFICATION THRESHOLDS — PENDING-CRO, DELIBERATELY EMPTY

The §7 taxonomy (**EXACT · EXACT-SHIFTED · TIGHT within N bp with its distribution · LARGE**) needs **`4.0.0_SA_CRO`'s N-bp word**. The issuer is re-spawning that seat for this one act.
**This slot stays empty until it lands.** The P1 deltas (**-0.040470 … +0.024253**, both signs) are the distribution the threshold will be set against — **published signed and unclassified**, because choosing a tolerance to fit the deltas already in hand is fitting the predicate to the outcome.

## 9. Bounds

- Every number here is the **settled post-re-emission vintage**; a P2 run must state its own vintage, since our side moved 529 of 535 partitions inside one hour today.
- The gross-leg (`r_gross`) comparison stays **UNAVAILABLE** until the re-emitted leg is verified; `r_net` is unaffected.
- The 22,110-call figure is arithmetic on the current vehicle's 3-endpoint design, **not** a measured census run.
