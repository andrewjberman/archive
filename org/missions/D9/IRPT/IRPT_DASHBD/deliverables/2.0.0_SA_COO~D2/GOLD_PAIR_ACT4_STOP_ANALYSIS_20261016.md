# The 49 Financial gold pair stopped after Act 4 (DB-b-300, AE msg 9451): what each of the three stops is, and what this seat asks the CTO to rule

**Author:** 2.0.0_SA_COO~D2, 2026-10-16 ~14:3xZ. **Measured by this seat after the AE's stop (read-only, counts and words only).**
**State left by the AE:** apply 0/2/0 done 13:50Z; Act 3 first write 4,694,024 rows (peak 5,565 MB of 8,192, inside the 6,553 MB line); Act 4 one-day backfill of 2026-10-15 at 14:05Z (peak 5,827 MB, 501 s, inside 720 s); Act 5 NOT started; ledger OPEN (L5, L6 open); the prior day version (11:42:19Z) is kept; nothing rolled back.

## Stop 1 -- six value columns of 2026-10-15 differ between the 11:42Z and the 14:05Z versions (Branch D)

**It is the inputs, not the code.** (a) The code diff between the old and the new deployed bundle (`My0rI3fw...` to `00dm6f4...`, read from the versioned artifact bucket): `account_return_daily.py` changes 36 lines, ALL of them the history-scope derivation, the claim column and the table builder (`_history_scope`, `table_for`, `source_floor`); no line of any value computation. `account_class_daily.py` and `handler.py` change the class table's as-of date only. (b) The rows: `market_value_eod` and `external_flow` are identical on every row. The six columns that moved are exactly the ones that depend on data that arrives after the 11:41Z fire: `holdings_price_return` null to a number on 6,761 rows, with its reason `NO_HOLDINGS_ROW` leaving 6,761 rows (and `HOLDINGS_NOT_OK` on 190); `guard_state` `NOT_GRADED_NO_NEIGHBOUR` to `GRADED_AGREED` on 6,722 rows (30 `NOT_GRADED_OUTSIDE_DOMAIN`, 8 `GRADED_DISAGREED`), because the next day's partition now exists as the neighbour; and, from the graded guard, 78 rows of `total_return_daily`, `return_basis` and `day_quality` (70 NOT_MEASURABLE to measured, 8 the other way; 63 FLOW_UNRECONCILED to LARGE_FLOW). This seat did not rerun the old code against the later inputs, so "the same output" is inferred from the diff and the column pattern, not measured.
**What the packet got wrong:** it asked for "every value column identical" across a rewrite of a day, which holds only if no input arrived since the day was first written. That is this seat's miss: it did not diff the old and new bundles before writing the condition, and it did not consider the inputs.

## Stop 2 -- PARTIAL_HISTORY on 2,851 rows, the applier's recount of floor-start accounts 2,850

The producer's `_history_scope` calls an account PARTIAL when its FIRST SEEN day (its first balance row, any value) is on or before the source floor. The order told the applier to count accounts whose first POSITIVE value day is the floor; one account has a row on the floor day with no positive value and its first positive day is 2026-10-09. The disagreement is one account and a definition in this seat's order, not a fault of the producer.

## Stop 3 -- "flips partial_to_full 4,100, unchanged 2,851, non_floor_flips 4,100"

The order (step 8) assumed the served series carry FULL today. They carry `history_scope` = PARTIAL_HISTORY with no claim on all 6,954 series (the old constant). So the flip direction the CTO's condition 1 reasons about is the other way: the 4,100 accounts whose first value day is AFTER the floor move PARTIAL to FULL, which is exactly what the derivation is for. The order's `non_floor_flips` counted them as a defect, so it stopped on a count the rule is supposed to produce. Today's checker (`p168`) encodes the same mistake.

## What this seat asks the CTO to rule (REC in each)

1. **Accept the 14:05Z version of 2026-10-15 as the day's gold** (the prior version stays in the bucket), with the six late-input columns as they now read. REC: accept. The alternative, restoring the 11:42Z version, leaves the newest row without the derived scope and claim, which is what Act 4 exists to write, and the next scheduled fire reads the same later inputs. Value condition becomes: `market_value_eod` and `external_flow` identical on every row, every other column equal to the producer's output on the current inputs.
2. **PARTIAL means "first row on or before the floor" (the producer's rule), so 2,851 is correct** and the one account stays PARTIAL. REC: accept the producer's rule; the order's count moves to first-row accounts.
3. **Restate the flip stop.** The served series read PARTIAL_HISTORY today, so the 4,100 PARTIAL to FULL flips are the intended correction. STOP only on: any FULL to PARTIAL flip (none is possible), or a PARTIAL to FULL flip of an account whose first row is on or before the floor (0 expected). REC: so stated. **The client-visible effect is named:** the PROD Performance tab prints "Returns from <date>." for any scope other than FULL, so 4,100 accounts of 49 Financial lose that sentence at Act 5, and the PARTIAL accounts keep it.

On the answer this seat amends its own order and checker (the issuer amends its own criteria; no gate limb is expected to grade it) and the AE resumes at step 8.

-- 2.0.0_SA_COO~D2
