# Cross-adjudication submission: call 6c9a, which Lambda hosts the Cottonwood transaction stage

## Context
`2.0.0_SA_COO~F2`'s plan `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/R136_COTTONWOOD_TRANSACTION_WIRING_PLAN.md` names three hosts:
1. the Cottonwood landing function `account-return-daily` (which writes `account_return_daily` and was just rewritten under DB-b-308);
2. the filled-report function `reporting-gold-cot`;
3. a new function.

The 49 Financial table runs as the LAST stage of the function that already writes that firm's returns day (signed today, sha256 b67bd4ad).

## Position
(1), CONDITIONAL on one read-only sizing read of `account-return-daily` by `~F2` before any cell is cut:
- its role reads the Black Diamond transaction silver, or one read grant on that one prefix suffices;
- the last stage fits inside 80 percent of the function's memory and time, measured on its last scheduled fires plus an offline run of the
  producer on one day.

If either fails, (3) a new function. Never (2): the served filled report must not share a failure mode with a new table.

## Why it gave pause
### Ambiguity
It is unmeasured whether the landing function's role and time budget fit; the plan says so.
### Out of pattern
Nothing is out of pattern; option (1) is the 49 Financial shape. Only the host function differs per firm.
### Other solutions
- (3) first: the cleanest blast radius, but a new function, root and schedule when an existing writer of the same firm's day may fit. It is
  kept as the fallback.
- (2): rejected, for the reason above.
