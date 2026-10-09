# REASON_SET_RULE24 -- why our return and Black Diamond's differ, over the 990 OUTSIDE segments (TO-DB-b-98, 0.9.0_WK_IRPT_DASHBD~73)

Source: `TIEOUT_COMPOUND_V2.json` (TO-DB-b-57, tolerance 0.35 pp). Record: `UNEXPLAINED_CLASSIFIED.json`. Classifier: `classify_unexplained.py`
(S3 reads only, zero vendor calls). No client identifier beyond the account key and no balance is written in this file.

## Re-derivation (cell step 1)

V2's OUTSIDE rows number 990. The 510 whose V2 reason is UNEXPLAINED re-derive to 510 distinct (account, segment) pairs over 461 accounts,
equal to V2's summary count. (The per-segment OUTSIDE rows DO carry `reason` and `evidence` in the V2 file; the order text said they do not. Row
IRPT_DASHBD-D2-W73-S3.)

## Declared reason set (UNEXPLAINED is not a member)

The four V2 reasons kept as V2 assigns them (480 segments): FLOW_TIMING 449, INCOME_DATE 26, COVERAGE_DAYS 4, MISSING_PRICE 1.
Five reasons added, each tested from the segment's own inputs (served daily gold series; the landed Black Diamond account point), first match wins:

| order | reason | test on the segment | segments |
|---|---|---|---|
| 1 | BOUNDARY_VALUE_GAP | Black Diamond's beginning or ending value, or its net gain, differs from the served series by more than max($1, 0.1%) AND (BD net gain minus served gain) divided by the mean served value predicts the signed return gap to within 0.35 pp | 96 |
| 2 | NEAR_ZERO_BASE | beginning value, ending value, flows and gain all tie, AND the lowest balance in the segment is at most 1% of its peak (the return is a ratio on a vanishing base) | 156 |
| 3 | ZERO_GAIN_VENDOR_TWR | dollars tie, BD net gain and served gain both under $1, yet BD reports a time-weighted return above 0.35 pp | 45 |
| 4 | FLOW_CONVENTION_ENVELOPE | dollars tie, the segment has flows, and BD's gross return lies inside the served link re-formed under START, MID and END flow timing, widened by 0.35 pp | 3 |
| 5 | WINDOW_ONE_DAY_SHIFT | BD daysHeld differs from the linked day count and dropping the first or the last linked day brings the served link within 0.35 pp of BD gross | 13 |

A segment no test holds for is a DEFECT, filed as a row, never a reason: 197 segments over two causes (below).

## (i) MECE over the declared domain

Domain: the 990 V2 OUTSIDE segments, one unscoped read, denominator printed: 990 = 449 + 26 + 4 + 1 + 156 + 96 + 45 + 3 + 13 + 197. Exclusive by
construction: the tests run in the fixed order above and a segment takes the first reason it satisfies; the four kept reasons were assigned by V2
before this cell and are not re-tested. Exhaustive by subtraction: 990 minus the 793 reasoned segments leaves 197, each carried by a DEFECT row. The
subtraction runs over the 510 V2-UNEXPLAINED segments (510 = 313 reasoned + 197 DEFECT) and the 480 V2-reasoned ones, domain and population identical.
Limit stated: first-match exclusivity means a segment satisfying two tests is counted under the earlier one; overlap was not tabulated.

## (ii) Same grain

One segment (account + start + end) is one row in every count; no reason is assigned at account or period grain.

## (iii) One axis

Each reason answers one question: what differs between the two sources for this segment (BOUNDARY_VALUE_GAP: their dollar inputs; NEAR_ZERO_BASE,
ZERO_GAIN_VENDOR_TWR: the return ratio on identical dollars; FLOW_CONVENTION_ENVELOPE, WINDOW_ONE_DAY_SHIFT, and the kept reasons: a timing or
window convention). The kept reasons are not re-argued here.

## (iv) What each remedy does not move

- A tolerance change (open call 2f53) moves the OUTSIDE population itself; it does not move which reason a segment carries.
- Re-linking under another flow convention (FLOW_TIMING / FLOW_CONVENTION_ENVELOPE) does not move a BOUNDARY_VALUE_GAP segment: its dollars differ.
- Correcting a boundary value (BOUNDARY_VALUE_GAP) does not move NEAR_ZERO_BASE or ZERO_GAIN_VENDOR_TWR segments: their dollars already tie.
- A day-window fix (WINDOW_ONE_DAY_SHIFT, COVERAGE_DAYS) does not move a segment whose day counts already agree.
- Naming a reason does not move the return: it states why two figures differ; it closes no gap and changes no served value.

## Honest limits

The thresholds (1% of peak, $1 or 0.1% dollar tie) are this record's choices, not Andrew's; the reasons are inferred from inputs, not confirmed by
Black Diamond. DEFECT causes: DOLLARS_DIFFER_NO_RECONCILIATION (74, row IRPT_DASHBD-D2-W73-S1): the dollars differ and the gain gap does not
reconcile the return gap. DOLLARS_TIE_RETURN_DIFFERS_NO_NAMED_CAUSE (123, row IRPT_DASHBD-D2-W73-S2): dollars tie, base not near zero, and no
convention or window test closes the gap (observed absolute gaps 0.37 to 141.88 pp).
