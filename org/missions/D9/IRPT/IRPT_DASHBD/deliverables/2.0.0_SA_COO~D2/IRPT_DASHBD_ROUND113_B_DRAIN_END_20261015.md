# IRPT_DASHBD round 113 (the CTO's round-112 L10 answer, msg 7875), workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~01:5xZ)

**One order, drained; a READ: nothing served moved, nothing written to AWS, nothing deployed; counts, hashes and words only in the repo; the client gold and the household table stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @e53c37c8ac. Drained: `DB-b-229` (~184, branch commits 44c4bc160f and ec8ee1b8ea, merged @cf4a94db99). On the landed tree `DB113-1-AC1` PASSES, and so do the nine earlier live criteria of rounds 110-112 (10 of 10 re-run). `round-close-check` reads **MAY-CLOSE** (1 order complete, 1 proof instance VALID, 0 judgment criteria). Push state: origin box/dell2 read 04e930b75c (ls-remote); `e53c37c8ac` was already ON origin by the box-sync; the worker commits, the merge `cf4a94db99` and this packet are LOCAL until the next box-sync.

## What the cell found (record `~184/RD_NOT_MEASURABLE_R113.json`)

- **The 56,311 unmeasured account-days, by cause (11 causes, the counts sum to the total):** `LINK_BREAK_BASE_NONPOSITIVE` with the row's own price reason HOLDINGS_NOT_OK 50,173 (0.8910); `FLOW_UNRECONCILED:GRADED_DISAGREED` 5,187 (0.0921); `FLOW_UNRECONCILED:GUARD_NOT_REACHED` 435 (0.0077); `FLOW_UNRECONCILED:NOT_GRADED_OUTSIDE_DOMAIN` 359 (0.0064); `INELIGIBLE_AFTER_COMPUTE` 81 (0.0014, claim inferred: the gold does not persist that reason); no row 7; `OTHER` 0.
- **2026-04-21:** a trading day in `lib/trading_calendar.py` AND in the producer (range mode, `trading_days_between`, line 2130): the two calendars agree, so the first suspect is cleared. 858 households broken (the checker recounts 858; round 112's 861 was the since-inception window count). The date's NOT_MEASURABLE rows are only 123 (117 non-positive base, 6 absent base, all price); the gold holds 944 FLOW_UNRECONCILED rows that day. Gold rows 2026-04-20 / 21 / 22: 5,896 / 5,902 / 5,911.
- **Next five dates by households broken:** 2026-07-02 (180), 2026-10-13 (159), 2026-09-22 (149), 2026-10-06 (148), 2026-09-16 (147).
- **Corrected premise (row `W184-S2`, ruled in `D2-S48`):** the households broken on 2026-04-21 are carried by the flow guard's disagreement (943 of that date's 1,061 household-sense unmeasured account-days), not by link breaks. The 89 percent NOT_MEASURABLE share is the all-dates picture (long-run non-positive-base days), a different thing from the worst date.

## What this seat read for itself

I re-ran `DB113-1-AC1` in the worker's tree and on the landed tree (PASS, rc 0, twice), re-validated the proof instance (VALID, rc 0), re-ran the ten criteria of rounds 110-113 (10 of 10 match their expectation) and read both worker rows. The checker recounts 858 households and the five next dates from the private table independently of the record. I did not re-derive the cause split from the S3 gold myself. No pages. **Not a grade.**

## Issuer errors this round (mine, disclosed)

The order's Why repeated round 112's "861 households ... NOT_MEASURABLE rows are the cause" as a premise for the date; the read shows the date is a flow-guard event. Corrected in `D2-S48`, not re-cut.

## Rows held (owners named)

`W184-S1` (the trading calendar answers from the hardcoded NYSE fallback on dell2: INERT, no action here). `W184-S2` (ARMED, disarm owner this seat) disarmed in `D2-S48` by carrying it to the CTO in the slug. The commit gate's client-data check gap (`W182-S1`, owner 0.0.0_AB_MSTR) still stands; this seat's identifier scans stand in. No ARMED row has a dark owner.

## What goes to the CTO (one ask, in the slug)

2026-04-21 is a FLOW_UNRECONCILED event (guard graded and disagreed, 943 household-sense account-days), and the long-run mass (89 percent) is the non-positive-base link break with a price reason. May the next cell be a READ of the flow guard's disagreement on 2026-04-21 and on the next five dates (which input disagrees: the flow, the value, or the guard's tolerance), before any repair, since the repair moves served numbers and needs a never-widen pair?

## What this does to the FWD outcomes

Inputs to `FWD-2` and `FWD-21`: neither is met. The cause of the largest household gap is now named; no served number moved. Grading is the CTO's at L10.

## Open

**Andrew:** the as-of approval row `dell2-20261014T195533Z-90a9` (client-facing) and call a252 (the 49 Financial disclosure file). **This seat:** `DB-b-183` L3, the first scheduled D_04 run after the 12:08:39Z upload.

-- 2.0.0_SA_COO~D2
