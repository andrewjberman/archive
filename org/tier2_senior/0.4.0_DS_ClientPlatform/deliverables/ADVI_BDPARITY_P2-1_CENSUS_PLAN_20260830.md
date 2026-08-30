# ADVI_BDPARITY.P2-CENSUS — P2-1: the census plan, and the artifact Andrew's word is asked on

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T08:1xZ (read) | **Issuer:** `2.0.0_SA_COO` 85980
**CENSUS VINTAGE:** gold `twr_daily` `date=2026-08-28`, partition LastModified **2026-08-30T05:09:10Z** (post-C02-g-6). Every number below is that vintage and no other.
⛔ **NO VENDOR CALL WAS MADE PRODUCING THIS PLAN.** P2-2 does not start on anything but Andrew's per-use word. **The probe's 2026-08-29T212315Z word was ONE pull of five accounts and is SPENT.**

## 1. POPULATION — 5,309, with both residuals as printed OUTCOMES

An account is only pullable if it resolves to a `bd_account_id`.

| | count |
|---|---|
| our accounts, `twr_daily` at the census vintage | 7,370 |
| `dim_account_xref` entries carrying a `bd_account_id` | 5,375 |
| **PULLABLE = the intersection — THE CENSUS DENOMINATOR** | **5,309** |
| ours NOT pullable -> `UNAVAILABLE-NOT-RESOLVABLE` | **2,061** |
| BD-pullable with no our-side value | **66** |

⭐ **5,309 independently reproduces the figure `3.0.0_SA_CVO` used in ANNOTATION 2** ("cannot anchor a 5,309-account census") — two seats, different arithmetic, same number.
⛔ **The two residuals are printed, never dropped.** A census reporting 5,309 without them looks complete while omitting **2,127** accounts' worth of story.
⛔ **THE "13 NINE-DIGIT KEYS" EXCLUSION DOES NOT APPLY AND IS WITHDRAWN AS A POPULATION OPERAND** (`2.0.0_SA_COO` 86424). Measured: `twr_daily` and `canonical_positions` are **100% ten-digit, ZERO nine-digit**. The nine-digit keys — **142**, many not Schwab-shaped (`J26000039`, `X04944670`, `Z05818068`, `BWF021838`, 8 masked) — live on the **xref** plane, which is R3's scope, untouched here. **I found no set of exactly 13 anywhere and did not reconcile to a number I was handed.**

## 2. ENDPOINT — performance only

`/portfolioreporting/api/performance/performancePeriod`. **`costBasis` and `allocation` are OUT**: the parity question never reads them, and the vehicle's 3-feed loop would **triple** the ask for data P2 discards.
**BUILD ITEM (P2-1, no egress):** the puller has no per-feed selector. Adding one is a code change with a unit test on the request builder — **never a call** — landed under Rule 13 and **read on the running artifact before P2-2**. ⚠ **Lane note:** the puller is `infra/aws/**`, where `safe-commit` refuses the DS lane; BP1-1 needed an AE lane to land and this will too. Named now so it is scheduled, not discovered.

## 3. THE RULED PERIODS, AND WHY SI COSTS A SECOND PASS

QTD / YTD / 1Y / SI, `q_end` = the **measured** last trading day (`lib/trading_calendar.expected_last_trading_day`), never assumed.

```
pass 1   QTD / YTD / 1Y are CORRECT on the first call — they do not depend on the anchor.
         The SI slot returns the ANCHOR (combinedLevels[].startDate) even though its VALUE
         is the fallback window, which is arithmetically QTD (face A3, fired on 4 of 5 at P1).
pass 2   SI re-requested AT that anchor — the only comparable SI value.
```
**SI's pass is its own line, so deferring SI to P3 reads as a halving rather than vanishing into a total.**

## 4. ⭐ THE COST, AND THE ONE UNMEASURED THING THAT MOVES IT 50x

Per-call cost **MEASURED at the probe**: 21s for 15 calls = **1.40 s/call**.

| per-call account cardinality | calls (2 passes) | serial runtime |
|---|---|---|
| **ASSUMED = 1** (never measured) | **10,618** | **~4.1 h** |
| if N = 10 | 1,062 | ~25 min |
| if N = 50 | 214 | ~5 min |

⛔ **CARDINALITY IS ASSUMED, NOT MEASURED, AND THE PLAN SAYS SO.** `accountFilters.accounts` is a **LIST**; every call we have ever made put exactly **one** account in it — because `run()` loops per account, **not because BD requires it**. Nobody has established what the endpoint accepts.
**THE OPTIONAL FIRST WORD:** one probe call, **2 accounts**, settles it and re-sizes everything above. **A word granted at one-account-per-call and executed at fifty is a different act from the one approved — and so is the reverse.** Andrew picks; nothing is fired either way without him.

## 5. REQUEST-SIDE HOLE MANIFEST

**2026-08-11 / 12 / 13 / 14 / 17** — five trading days absent from our gold; **2026-08-18** present but all-null (partition-wide refusal). Carried as `OUR-DATA-ABSENCE` on **every cell whose window spans them**, with the day count, never netted.
**C02-g-7 will backfill the five dates.** Four predictions are pre-registered against that (msg 86259, adopted as a producer arm at 86269) **before the write** — if it lands before P2-2, the manifest shrinks to 08-18 alone and H1 says the residual goes 1 -> 0.

## 6. FROZEN CONVENTIONS — consumed verbatim, not re-derived

- **Thresholds** `4.0.0_SA_CRO` @`9f894ec5d9` + A1: **EXACT |d| <= 0.5 bp · TIGHT 0.5 < |d| <= 10 bp with its distribution · LARGE > 10 bp**; unit bp of **cumulative** return; `delta = ours - BD`, **SIGNED, never absolute**; **day-count residual FIRST**.
- **Period convention** `1.0.0_SA_CTO` 85237: `[start, end]` links every trading day from start **through** end inclusive, base = close of the trading day before start.
- **Anchor + basis** `3.0.0_SA_CVO` @`f11fb765ad` + annotations 1–3: anchor = BD funding-inception, admissible only where our coverage (**first-linkable**) opens on or before BD's first return day; basis **CUMULATIVE**, read from BD's own `returnAnnualized` field, **never inferred from which of our figures matches**.
- **Outcome vocabulary** (MECE, coverage first): `COMPUTED` · `UNAVAILABLE-NO-COVERAGE` · `UNAVAILABLE-SI-WINDOW-NOT-AT-ANCHOR` · `UNAVAILABLE-NO-ANCHOR` · `UNAVAILABLE-RANGE-MISMATCH` · `UNAVAILABLE-NOT-RESOLVABLE` (new at P2, §1) · and on differenced windows `VACUOUS-NO-LINKED-DAYS` with its Rule-24 record.

## 7. WHAT EVERY CELL PRINTS

Requested vs returned range **with the requested index** (BD returns `name: null`/`type: null`, so **position finds the cell and the dates certify it**; the order signature is re-checked per response and a change **refuses the whole response**); our value, BD's value, the **signed** delta in **bp and Dlog**; `days_expected` / `days_linked` / in-window refusals with the **residual**; the SI line (anchor, first return day, branch, our first linkable, coverage basis); and the differenced sub-windows, hole-free by additivity, with their own day columns.

## 8. P2-4's HEADLINE — a distribution, never a rate

Class distribution **per period and per leg, with denominators**. ⛔ **Never a single "parity rate"**: at P1 all 16 ruled-window cells read LARGE and that was **uninformative** — the hole was in every window — while the differenced sub-windows held the program's only EXACT evidence. **A single number would have reported the opposite of what the data said.**

## 9. Bounds

- Cardinality **ASSUMED**; runtime scales directly off it.
- Whether BD accepts a mid-quarter `asOf` at population scale is evidenced by **n=5** (it honoured it at P1), not by a census.
- The C2 gross-leg cell is read at **P2-3** on the post-C02-g-6 vintage, where the exclusion lifts.
- `UNAVAILABLE-NOT-RESOLVABLE` is measured at the census vintage; the xref moves, so P2-2 re-derives it at fire time and states both.
