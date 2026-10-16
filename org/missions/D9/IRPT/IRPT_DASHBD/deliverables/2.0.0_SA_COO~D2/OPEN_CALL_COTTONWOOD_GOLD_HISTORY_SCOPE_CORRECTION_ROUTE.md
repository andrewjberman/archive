# Open call -- how the 65 landed Cottonwood gold days get the derived history_scope (IRPT_DASHBD round 149, 2.0.0_SA_COO~D2)

**Raised by:** 2.0.0_SA_COO~D2, 2026-10-16 ~10:0xZ, after the CTO's ruling msg 9226 (history_scope derived per account, never a constant; `history_scope_claim` = inferred).

**The fact.** The Cottonwood landing function (`irpt-cot-account-return-daily-lambda`, handler `infra/aws/lambda/investor-reporting/account-return-daily/handler.py`, adapter `write_day`) REFUSES to write a `date=` partition that already holds objects (the no-overwrite guard of DB-b-254: one LIST before any put, `GoldWriteError`). The 65 Cottonwood gold days already landed (2026-07-10 to 2026-10-14) carry `history_scope` = `PARTIAL_HISTORY` on every row and no claim. Cell `DB-b-294` makes the adapter derive the scope for NEW days only. The publisher reads the NEWEST row of each account, so a series stays on the old constant until the newest landed row of each account is a derived one: for an account that stopped holding value, that row is an old partition for good.

**Three routes (the question is which one; each is a separate signed pair after the drain of cells 292 to 295):**
- **(a) Delete and re-land.** Andrew deletes the 65 gold partitions by listed key (an S3 delete, which is his act under the standing hard stop), then the landing function re-lands them with the new code. Cost: a delete of served-adjacent gold, a window with no Cottonwood gold, 65 landing events.
- **(b) The publisher derives for landed days.** The Cottonwood publish handler derives the scope itself from the gold it reads (first value day vs the earliest gold day) and writes the claim. Cost: a second place where the rule lives (the producer and the publisher), and the gold stays wrong.
- **(c) A signed, explicit rewrite path.** The landing handler gains an event `{"rewrite": {"start": ..., "end": ...}}` (at most MAX_BACKFILL_DAYS days, only days already landed, the way the 49 Financial `reporting-gold` handler's `backfill` works), whose `write_day` call overwrites the named partitions; the bucket is versioned, so every prior version is kept and nothing is deleted. The scheduled path keeps the guard unchanged. Cost: one more code cell, then a never-widen pair for the 65 days (code update, then one rewrite event per chunk, read-backs).

**REC: (c).** It follows the one precedent the estate already has for correcting landed gold (the 49 Financial backfill), deletes nothing, keeps the rule in the producer, and leaves the no-overwrite guard on every path but the explicit one.

**What it gates:** the Cottonwood part of the history_scope work only (the Cottonwood landing code update, the gold correction and the Cottonwood republish under publisher 0.4.0). The 49 Financial side, the unreported-days statement and everything in cells 292 to 295 do not wait on it.

-- 2.0.0_SA_COO~D2
