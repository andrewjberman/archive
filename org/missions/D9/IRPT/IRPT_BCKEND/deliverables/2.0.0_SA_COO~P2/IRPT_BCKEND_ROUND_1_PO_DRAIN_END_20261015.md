# IRPT_BCKEND round 1, workstream ~PO (the Orion Inflection raw feed) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~05:3xZ). To: 3.0.0_SA_CVO. One order, issued @b0ec635168 on the CTO's msg 7980: IB-pr-552 `complete` (merged @62d5757800). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PO"` reads `verdict=MAY-CLOSE` (orders=1, 1 complete). I re-ran IB199-4-AC1 to AC3 on the worker's tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **Nothing was pulled, re-pulled, written to AWS, signed or invoked; no Orion API request was made.**

## What the CVO needs to know

- **The raw producer is manual.** The flat `.jsonl.gz` positions key the mirror needs is written by `data/inf/manual_api/pull_inflection_positions_daily.py:445`, a command-line pull (`--upload-bronze`) on no schedule; the deployed lambda `inf-api-positions` writes only `.parquet`. The same folder writes the flat transactions and performance keys.
- **Seven positions days landed parquet-only and were dropped** (the two known days, 2026-07-01 and 2026-09-28, and five more); transactions and performance have none. Source census: positions 4,723 keys, 2,358 flat days.
- **The mirror is not the defect.** It refuses `.parquet` by design (ruling 16: a parquet is schema-coerced and its raw content is not recoverable); the defect is that the raw producer is not scheduled. This answers the CTO's second point against his hypothesis.
- **The re-pull is small:** positions only, 7 days, 2,240 requests, about 19 minutes at the shared 2 requests/second floor (cost inferred from the code's own limiter); transactions and performance need none for parquet-only days.
- **Fold design:** one EventBridge Scheduler schedule, 06:00 America/New_York, names from `opal_naming`, trading-day frontier by `lib/trading_calendar.py`. `2.0.0_SA_COO~I2`'s round-116 feed is not yet written.
- **Rows:** D2-S182 dispositions D2-W396-S1 to S7 (all INERT). STILL ARMED, carried: D2-W394-S2 (the silver sweep cannot see a bronze key that never landed), D2-W392-S2, W349-S1, W361-S1, W348-S2, W368-S2 (owner me), D2-S158 (with the CTO).
- **Not cut and why:** the two pairs the READ leads to, (a) the one-time 7-day positions raw re-pull and (b) the scheduled producer in the fold; the CTO's word on their shape is asked in the same tick.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
