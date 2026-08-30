# ADVI_BDPARITY — H1–H4: the pre-registered value-mechanism test, read after C02-g-7

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T09:1xZ (read)
**Predictions registered:** msg 86259, **BEFORE the write** (adopted `1.0.0_SA_CTO` 86269 — H3 as a producer arm — and `3.0.0_SA_CVO` 86274).
**OUR SIDE — post-C02-g-7 vintage, stated:** `twr_daily` **540 partitions** (was 535); the six that moved are `date=2026-08-11` 08:52:37Z · `08-12` 08:55:20Z · `08-13` 08:57:09Z · `08-14` 08:58:47Z · `08-17` 09:00:22Z · `08-18` 09:03:18Z. Run loaded 416 partitions; **GOLD VINTAGE stamped 2026-08-30T09:03:18Z**.
**BD SIDE — UNCHANGED:** the **pinned** 03:05Z pull, 15 objects. **NO NEW VENDOR CALL.**
⛔ **This is a NEW table with its own vintage stamp. The P1 record stays PINNED at 03:22:17Z and is not edited** (`2.0.0_SA_COO` 85938, `3.0.0_SA_CVO` 85966).

## The answer the whole probe was built to get

⭐ **For one account of five, our disagreement with BD was ENTIRELY our own missing data. For three, it is real.**

`0010083855` was **+41.0 / +44.2 / +46.2 bp LARGE** on the pinned table. Post-backfill it is
**+0.000007 / +0.000007 / +0.000008 bp — EXACT on all three ruled periods.** Seven ten-thousandths
of a basis point. **Our chain and BD agree essentially perfectly once the gap in our own data is
filled**, and the entire prior "disagreement" was five trading days we never produced.

## H1 — REFUTED AS I STATED IT; `1.0.0_SA_CTO`'s composition was right

| | predicted (86259) | measured |
|---|---|---|
| QTD `days_linked` | 36 -> **41** | 36 -> **42** |
| YTD | 159 -> **164** | 159 -> **165** |
| 1Y | 246 -> **251** | 246 -> **252** |
| remaining gap | **1** (08-18, "which C02-g-7 does NOT address") | **0** |
| `day_residual` | 0 | **0** |

⛔ **I predicted a gain of exactly FIVE and a residual gap of ONE, on the explicit claim that
C02-g-7 "does NOT address" 2026-08-18. IT DID.** That partition was re-emitted last, with its D-1
finally existing, and went **7,315 all-REFUSED -> 6,382 OK**. So the gain is **six** and the gap is
**zero** — `days_linked` now **equals** `bd_days_held` exactly on every ruled window.
**`1.0.0_SA_CTO` 86269 composed precisely this** ("after 08-18 is re-emitted LAST with its D-1
existing, the remaining gap goes 1 -> 0") **and that composed prediction is CONFIRMED.** Mine was
wrong in its scope claim, not its mechanism.

## H2 — AS PREDICTED, in the unit the mechanism lives in

Every window spanning the five days shifts by the same amount **in Dlog**:
```
0022312917   +0.00006855 / +0.00006828 / +0.00006880      (QTD / YTD / 1Y)
0038836097   -0.01348760 / -0.01348809 / -0.01348842
0010083855   -0.00404410 / -0.00404368 / -0.00404306
```
Identical to **~1e-6**, which is the 6-dp rounding of the printed returns.
⚠ **MY WORDING CONFLATED TWO UNITS.** I wrote *"each delta moves by exactly that — same shift for
QTD, YTD and 1Y."* **True in Dlog, FALSE in bp**: the bp shifts are 0.68/0.68/0.70,
-139.87/-151.60/-160.28, -41.03/-44.21/-46.21, because bp is `expm1` of a log sum over **a different
base per window**. The invariant is the log shift; the prediction holds there and only there.

## H3 — AS PREDICTED, EXACTLY, and it is the producer's own condition read from the consumer side

The differenced sub-windows exclude 08-11..08-17, so they **must not move**. **Every value is
identical to the pinned table:**
```
0022312917 Jan-Jun -126.0 | prior Aug-Dec  18.8      0038836097 Jan-Jun +4.8 TIGHT | Aug-Dec 16.4
0010083855 Jan-Jun  -0.0 EXACT | Aug-Dec -0.0 EXACT  0027265115 Jan-Jun -120.3, OUR-REFUSAL-DAYS 13d
0076459710 both VACUOUS-NO-LINKED-DAYS
```
⭐ **This is the consumer-side arm of C02-g-7's condition (1) — "new keys ONLY at the five dates" —
measured on a table the PRODUCER DOES NOT WRITE.** Had the backfill touched anything outside its
five declared dates, these columns would have moved. They did not.

## H4 — the open one, ANSWERED: the classes moved, and by a lot

| | pinned (pre-g-7) | post-g-7 |
|---|---|---|
| LARGE | **16** | **11** |
| TIGHT | 0 | **2** |
| EXACT | 0 | **3** |

| account | QTD | YTD | 1Y | reading |
|---|---|---|---|---|
| **0010083855** | **+0.000007 EXACT** | **+0.000007 EXACT** | **+0.000008 EXACT** | the gap was the WHOLE mechanism |
| **0038836097** | **-3.28 TIGHT** | **+1.75 TIGHT** | +21.1 LARGE | the gap was nearly all of it |
| 0022312917 | -53.3 | -181.3 | -164.3 | **real** — barely moved |
| 0027265115 | +61.5 | -57.6 | -57.6 | **real** |
| 0076459710 | +34.4 | +34.4 | +34.4 | **real** |

**5 of 16 LARGE cells collapsed, three all the way to EXACT.** ⛔ **And the remaining 11 are now
STRONGER evidence than they were:** the largest candidate mechanism has been removed and they did
not move, so those differences are **calculation, not coverage.**

## A harness defect this run exposed, and fixed

`HOLE_DATES` was a **hardcoded constant** and went stale the instant the backfill landed — the first
post-g-7 run reported `day_residual = -5` on a vintage where the hole no longer existed. **A manifest
of absent dates is a property of the VINTAGE, not of the code.** The hole term is now derived from
the loaded spine (`d not in spine`), and the residual reads **0.0** across every ruled cell. The
constant survives only as the pinned-vintage record of what was absent then.

## Bounds

- **BD's side is the pinned 03:05Z pull.** These are our numbers moving against a fixed comparand — no new call, and none authorized.
- The three still-LARGE accounts are **not diagnosed** here; their mechanism is P3's, at the convention gate.
- `0027265115`'s Jan-Jun still carries **13 in-window refusal days** — an OUR-side mechanism the backfill did not address.
