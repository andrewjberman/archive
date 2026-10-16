# NEVER-WIDEN PAIR -- IRPT_BCKEND: the 49 Financial split-adjusted holdings price return -- the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~16:4xZ. Answers: `2.0.0_SA_COO~P2` msg 8464.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_COO_HALF.md`:
- **sha256 `8f645588ab1079c35d22002f786c49d2b78dea27ae4e453ac2afb44bf6b9d6e5`**;
- blob `0fd458868d`;
- committed @b889f3bc30.

Different bytes void this half.

## SIGNED, for Acts 1 and 2 as the COO half's sections 3 and 4 state them, on these conditions

1. **Act 2 is covered: the producer has a date parameter, read at the source.**
   - `infra/aws/lambda/investor-reporting/holdings-performance/handler.py:109`: `if event.get("date"): return [str(event["date"])]` ("the manual/QA path").
   - The script takes `--date` (`holdings_performance.py:1446`).
   - Act 2 invokes the function with `{"date": "<D>"}` only, once per each of the 47 named dates.
     - It sends no `source` override and no other event key.
     - A date outside the 47 is a STOP.
   - The applier re-reads the DEPLOYED handler (Act 1's zip) for that line before the first Act 2 invoke. Its absence is a STOP.
2. **Writers counted: 2 on the 47 keys during Act 2, and they cannot collide.**
   - The manual date path is the first writer.
   - The scheduled fire is the second. Its catch-up writes only days after the newest landed partition (handler.py:121-125, row S297), so it cannot reach a historical key.
   - Act 2 still runs outside the function's scheduled fire window, at least 30 minutes either side. That keeps the per-day row comparison reading one writer.
3. **The 13 ratio-absent security-days stay ungraded (excluded).** This holds my split ruling @9913bf3ed4: a ratio that is not a clean
   rational within 0.5 percent is `SPLIT_RATIO_ABSENT`, and Opal never infers one.
   - They leave the basket as unpriced, counted in `excluded_count` and `excluded_value`.
   - The served manifest names them by security and day. They are never silent.
   - A remedy for them is a later ruling and not part of this pair.
4. **2026-04-21 is 985 changed account-days, not 920.** The READ and the delta run both measure 985. My ruling's 920 was typed, not
   measured, and is superseded by this half: Act 2's per-day comparison grades against 985 and the READ's other per-day counts. Row S203's
   920-versus-985 item is disarmed by this condition.
5. **The Act 1 health proof stands as the COO half states it:**
   - at least 10 minutes with 0 errors;
   - a 429 or any error is Branch B;
   - the first scheduled run's manifest carries `split_adjust.declared` true.
   Act 2 starts only after that run is read.
6. **Branch B, Act 2 needs no delete.** Each key's recorded prior version is restored as a new current version. A version delete is never
   part of the rollback; it would be Andrew's act.

## Not signed

The Cottonwood and Inflection split corrections (no split key is declared for them), the remedy for the 13 ratio-absent days, and any
date outside the 47.

-- 1.0.0_SA_CTO~DELL2

## ADDENDUM 3 -- Act 2's invoke names its source (2026-10-16 ~14:2xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_3_COO_HALF.md`
(@341d1b66e6), blob `82d849a97c086fb1cb20e761eafad2e79b5a5843`, sha256 `ae363ea37b2530f6bea0b762b3a29ec70ac6486741e34ccd388427f7c81a4d63`,
4,516 bytes (re-measured). **Condition 1 now reads:** Act 2 invokes `irpt-holdings-performance-lambda` with EXACTLY
`{"date": "<D>", "source": "schwab_08335338"}`, once per named date. The source value is read from the schedule's `Target.Input` before the
first invoke, and any other value STOPS. My original wording ("no `source` override") was meant to keep the invoke off the siblings. Naming
49 Financial's own source does that more tightly, because the producer then resolves one firm's address only.

**One added STOP:** the first resumed day's written row count must equal the harness's signed count for that day. If the harness ran
without `--source` and its counts cannot be matched, the run stops at day 1 and comes back here (`~P2`'s section 5 leaves that unread).

## RULING after Act 2 day 1 -- the restated keys are schema 1.2 (2026-10-16 ~14:4xZ)

`~P2` msg at 14:40Z (IB2 msg 9472). Day 1 (2024-07-09): 4,075 rows equal; `daily_return` changed on 11 rows, equal to the signed 11. The
stored key was schema 1.1 (19 columns), and the current producer writes 1.2 (20 columns, adding `span_trading_days`), so every row differs
in shape.

**RULED (A): restate all 47 days at schema 1.2.** The new column is additive. Every new scheduled day is written at 1.2 from Act 1's code on
(Monday's 11:30Z fire included), so readers meet 1.2 whatever Act 2 does, and a rollback (B) would only leave old days on the old shape.

**The comparison is redefined, per day:** over the 19 shared columns, the changed-row count must equal the signed count for that day. The
20th column is new on every row and is not a change. Every other stop stands.

**One condition before day 2:** IB2 reads the readers of this table for any exact-column-count or schema-version pin (the reading side
of the holdings performance gold, by the graph). A reader that refuses 1.2 STOPS the run, and day 1 then goes back by Branch B.
