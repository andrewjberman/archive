# ADVI_BDPARITY -- 3-account live parity spot check, 2026-09-01T00:0xZ

**Seat:** `0.4.0_DS_ClientPlatform~Y`
**Asked by:** Andrew, verbatim via `1.0.0_SA_CTO` 90324 -- *"I want to validate now, i do not want to wait."*
**Egress authority:** Andrew-direct 23:4xZ 2026-08-31, verbatim, carried by `1.0.0_SA_CTO` 90324:
> I dont care how we have to phrase it, vendor egress allowed
> if its easier to make it explicit, all vendor egress is allowed tonight for all agents

⛔ **THIS IS A PROBE, NOT A CENSUS, AND THE STANDING SENTENCE IS UNCHANGED: parity is PROBED --
n=5 from P1 plus these 3 -- with 11 open calculation differences and a twelfth found here. The
5,309-account census is ARMED AND UNFIRED. Nothing here may be read as "parity proven."**

---

## The result -- 9 cells, delta = ours - BD, SIGNED, bp of cumulative return

| BD | schwab | period | range_match | ours | BD | delta (bp) | CLASS | days ours/BD |
|---|---|---|---|---|---|---|---|---|
| 20277481 | 0026881039 | QTD | True | 0.011767 | 0.011767 | +0.008 | EXACT | 42/42, 42/42 |
| 20277481 | 0026881039 | YTD | True | 0.083671 | 0.083712 | -0.407 | EXACT | 165/165, 165/165 |
| 20277481 | 0026881039 | 1Y  | True | 0.101928 | 0.103800 | **-18.722** | **LARGE** | 252/252, 252/252 |
| 20265531 | 0022002671 | QTD | True | 0.014621 | 0.014621 | +0.000 | EXACT | 42/42, 42/42 |
| 20265531 | 0022002671 | YTD | True | 0.094498 | 0.094501 | -0.030 | EXACT | 165/165, 165/165 |
| 20265531 | 0022002671 | 1Y  | True | 0.142046 | 0.142047 | -0.012 | EXACT | 252/252, 252/252 |
| 20350771 | 0065125789 | QTD | True | 0.015646 | 0.015646 | +0.000 | EXACT | 42/42, 42/42 |
| 20350771 | 0065125789 | YTD | True | 0.104161 | 0.104161 | +0.000 | EXACT | 165/165, 165/165 |
| 20350771 | 0065125789 | 1Y  | True | 0.155256 | 0.155256 | +0.000 | EXACT | 252/252, 252/252 |

```
  CLASS DISTRIBUTION   EXACT 8 | TIGHT 0 | LARGE 1        denominator 9 cells (3 accounts x 3 periods)
  range_match          9 of 9 TRUE
  day-count residual   NONZERO on 0 of 9
```

**A distribution, never a rate** (plan section 8): a single "parity rate" over 9 cells would report
the opposite of what the data says, exactly as it did at P1.

## The one LARGE, and why it is the informative cell

`20277481` 1Y reads **252/252 linked on BOTH sides** with ranges matching exactly. **It is therefore
not our missing days and not a window disagreement -- it is a genuine calculation difference**, the
same class as the eleven already open at P3-EXACT. Owner: P3, held by `1.0.0_SA_CTO`. Not chased here.

The other two accounts agree to **nine millionths of a basis point** across all three periods.

## Method -- the ruled chain, nothing built

⛔ A standing parity comparator is under Andrew's COMPLETE VETO. This was a one-shot caller of the
existing chain, discarded after the run; no comparator was created.

- **Our side:** `data/assets/scripts/gold/runners_49f/parity_period_returns.py` `link()` -- geometric
  linking, because our gold chain emits DAILY returns only and never these periods.
  **Its own self-test passed 27 of 27 arms in this session BEFORE it was trusted.**
- **Input:** 271 `twr_daily` partitions, `2025-08-01..2026-08-28`, **0 load errors**, 813 rows for the
  3 accounts -- **all three present on all 271 days**. `earliest_partition` passed so
  `UNAVAILABLE-WINDOW-NOT-LOADED` stays distinguishable from dormancy.
- **BD's side:** read from the landed bronze by the ruled join -- **position finds the cell, the dates
  certify it.** BD again returned `name: null` / `type: null` on every range, so a label join was
  impossible, as ruled. Cumulative TWR from `timeWeightedReturns.return`, `returnAnnualized: false`.
- **Classification:** the CRO's ruled thresholds -- EXACT `|d| <= 0.5 bp`, TIGHT `<= 10 bp`, else LARGE
  (`ADVI_BDPARITY_BP1-4_CLASSIFICATION_THRESHOLDS_20260830.md`).

## Declared exclusion -- SI is NOT computed, and this is not an absence-because-equal

The puller returned `accounts_without_anchor: [20277481, 20265531, 20350771]` -- **all three carry no
inception.** Per the defect both `1.0.0_SA_CTO` and `2.0.0_SA_COO` carried, BD's Since-Inception range
then **silently collapses to the window** and BD returns a figure LABELLED "Since Inception" that is
arithmetically QTD, with nothing raised. **Comparing it would have manufactured a spurious EXACT and
inflated the agreement count.** Four of BD's six returned ranges (SI + two calendar years) are
deliberately not compared.

## Provenance of the bytes

Pull fired 2026-08-31T23:53:19Z, landed 23:53:26-27Z, `feeds=["performance"]`, `q_start=2026-07-01`,
`q_end=2026-08-28`, `pull_date=2026-08-31` (pinned).
**Vendor cost: 3 data calls + 1 auth = 4.** Objects:
```
  blackdiamond/49f/bronze/reporting_performance/2026-08-31/reporting_performance_20277481_2026-08-28.json  581,098 B
  blackdiamond/49f/bronze/reporting_performance/2026-08-31/reporting_performance_20265531_2026-08-28.json  726,554 B
  blackdiamond/49f/bronze/reporting_performance/2026-08-31/reporting_performance_20350771_2026-08-28.json  550,053 B
```

## W2's acceptance evidence is intact -- measured, not asserted

The pull landed in a partition holding none of the pinned baseline. Verified AFTER the fact with the
committed verifier:
```
  pinned baseline objects   : 18
  still at pinned VersionId : 18 of 18
  MOVED 0   DISAPPEARED 0   VERDICT: UNTOUCHED
```
The pinned objects live at `pull_date` 2026-07-17 and 2026-08-30; this wrote 2026-08-31. The
intersection of the would-write key set with the pinned key set was measured at **0 BEFORE firing.**

## Two findings surfaced, neither chased

1. **THE 00:00Z MINT DID NOT FIRE.** At 2026-09-01T00:07:33Z the secret's `LastChangedDate` still read
   `2026-08-31T00:03:47Z`; the prior cycle had landed by 00:03:47Z. **The session is UNROTATED, not
   expired** -- this pull made 3 successful data calls at session age **23.83 h**, so there is positive
   evidence of life, not merely absence of failure. Rotation failure and expiry are different faults
   with different owners. Reported to `1.0.0_SA_CTO` / `0.0.0_AB_MSTR`; owner not this seat.
2. **A twelfth calculation difference** (`20277481` 1Y, -18.72 bp, both sides fully linked). P3 item.

---
**Evidence rides `0.4.0_DS_ClientPlatform~Y` at this commit; the raw comparison table and our-side
cells were computed in-session from the artifacts named above.**
