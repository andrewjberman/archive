# The history-ceiling ramp, dell1's half: what the round-10 cell carries (issuer 2.0.0_SA_COO~Q1, 2026-10-15 ~21:3xZ)

**Input:** CTO ruling `ledger/CTO_RULING_HISTORY_CEILING_RAMP_20261015.md` @08a12d383e (msg 6250): steps 2x (11,716 cells a day), 4x (23,432), 5x (29,290); each step after one completed drawing day at the step before, with no vendor limit warning and every production leg complete; hold at the last good step on the first warning or a missed leg; history channel only; the surface E cap follows the ceiling; site Z's drawer change is MSTR to MSTR. Andrew's words: `deliverables/2.0.0_SA_COO~Q1/ANDREW_DIRECT_20261015_21xxZ_RAISE_PULL_LIMITS_FLOOR_IS_NOT_A_CAP.md` and the trading-day word of 193xZ.
**Status:** a design read at HEAD `f7a77c05a9`. The CTO named this "a round-10 cell beside DQ-t-69"; it is cut at the round-10 issuance, after `TO-DQ-t34` is terminal (the 2026-10-17 fire) and the CTO's round-9 analysis is in hand. Nothing here is built and nothing at site Z moves from this file.

## What the code does today (read)

| fact | where |
|---|---|
| The drawer's room comes from `bbg_quote.quote(...)["allowance_today"]`, which reads `history.ceiling` from `bbg_allowance.json` and refuses a backfill date unless that ceiling's claim is `measured` | `bbg_quote.py` `_history_backfill`; `standing_drawer.py` `run` |
| `ceiling_from_ledger.py --write` re-measures the ceiling as the LARGEST single-day sum of history cells on the served demand ledger, and writes it `measured` | `ceiling_from_ledger.py` `promote_history` |
| The surface E cap is 10 percent of the measured history ceiling (585 today) | DQ-t-55 `450bf78800` |
| The carry-over adds the unused part of the ceiling on each trading day between two fires | `standing_drawer.py` `carry_over` |

## The design point that is easy to get wrong

**The steps must be absolute cell values, not multiples of the live ceiling.** Each completed day re-measures `history.ceiling` as the largest day drawn. After a day at 11,716 the ceiling reads 11,716; a step defined as "2x the ceiling" would then read 23,432, then 46,864: the steps would compound and skip the 4x and 5x the CTO ruled. So the ramp keeps a fixed base (5,858) and a step table (11,716, 23,432, 29,290), and the ceiling's re-measure only records evidence. The cell carries a test that a day at step 1 does not change step 2's value.

## Dell1's half

1. **Allowance file.** A new `history.ramp` block beside `history.ceiling`: `{"base": 5858, "steps": [11716, 23432, 29290], "step": 0, "claim": "held", "basis": "<the CTO ruling path and message>"}`. `claim` stays `held` for a step until a completed day at it is on the ledger (an unmeasured figure never reads `measured`). `step` is the highest step a completed day has earned; it starts at 0 (the base).
2. **The day's room** is `steps[step + 1]` when the next step is earned and `steps[step]` otherwise, never above the last step; the existing carry-over and the trading-day room (DQ-t-69) stay inside it as today.
3. **The ramp's reads, all read-only on dell1:** (a) the last drawing day's `BBG_ACTUALS.jsonl` lines (drawn cells, `outcome`), (b) the receipt's stop reason (`STOPPED` with a `VENDOR_DIAGNOSTIC` reason is a vendor warning), (c) the day's budget ledger for production's spend. A step is earned only when (a) shows the day drawn to its step with outcome `DRAWN`, (b) shows no vendor warning, and the production-leg check below passes.
4. **Production legs complete.** The CTO's condition needs each leg's exit code for the day. Those codes are written by the site Z job (`scheduled_daily_pull.cmd`, disjoint codes per leg) and are NOT readable from dell1. This is the named gap: the site Z half (CloudOps, MSTR to MSTR) must expose "every leg rc 0 on day D" to the drawer as a single readable line, and the ramp refuses to step up when that line is absent (fail closed).
5. **Stop.** The first vendor warning or missed leg holds `step` where it is and writes one finding row to the project's surprise channel for the CTO; no step is retried without a new read.
6. **Surface E cap.** Unchanged in code (it follows the measured ceiling): 585, then 1,171, 2,343, 2,929 as the days complete. The CTO's ruling states this is as defined.
7. **Quotes.** The frozen quotes stay as filed (the pessimistic dates); the restated finish dates are re-quoted with the observed rooms after the first step-up day, labelled `held` until measured.

## Measured since the first draft: when the drawer fires

The site Z ledger entry `mdpf-demque-zq-t34-close` (author `0.7.0_AE_CloudOps~ZQ`, device sitez measured) records the drawer task `mdpf-demque-drawer-daily` at **10:00 ET, `MSFT_TaskDailyTrigger` `DaysInterval` 1**. That is after the 7:00 AM ET production job and the about 9:00 AM research pull, so a trading-day room read at 10:00 sees both legs' spend if they have finished. Whether they have finished by 10:00 is NOT measured (a leg's run time is in site Z's logs, not here); it is the first read the CloudOps half takes.

## Criteria the cell would carry (three, mechanical)

- AC1: named tests on stub ledgers: the steps do not compound; no step-up without a completed day; a vendor warning holds the step; an absent production line holds it.
- AC2: on the REAL allowance file and fixture ledgers: the ramp block reads, the room at each step is 11,716, 23,432, 29,290, and the file's other channels are byte-identical.
- AC3: the DEMQUE folder green.

## Where this reaches client history

Client history is 199,341 Bloomberg history cells (B1 34,437; the 14 names 7,685; the porting test 3,195; the 27 active slices 154,024). At the 5x step it is 6.8 drawing days; at 4x, 8.5; the ramp's first two steps take two drawing days at 11,716 and 23,432, so the first four fires after the ramp lands draw about 11,716 + 23,432 + 29,290 + 29,290 = 93,728 cells. Client history clears in eight drawing days from the first step if every step is earned (11,716 + 23,432 = 35,148 in the first two, then 164,193 at 29,290 is six more days), so "a few days" needs a ceiling above the ruled 5x. Two items beyond the cells: the 227-cell fund-type check draws from the REFERENCE channel (ceiling 52, five days), which the ramp as ruled does not touch; and 1,006 of the 2,739 active names the builder cannot price are not in the 199,341.

## Added ~22:5xZ: site Z's statement, and A4

- **Site Z (CTO~Z msg 34585, relayed as 6268/6271):** the drawer task reads `bbg_allowance.json` from its working tree, so a ramp step is this seat's allowance commit carried by box-sync; no CloudOps change. A step counts only for a 10:00 ET (14:00Z) fire whose tree held the new figure AT FIRE TIME; read that from the fire, never from the commit time. That is site Z's statement, not measured here. The TR-first move `579477d0de` is on `origin/box/sitez` @bca548c5ca (measured).
- **The code half still stands.** A bare edit of `history.ceiling` to 11,716 would write an unmeasured figure as `measured`, and the drawer refuses a backfill date unless the ceiling's claim is `measured`; so the `history.ramp` block and its read are still the dell1 cell.
- **The ramp's reads come from the S3 demand ledger** (`bbg_ledger_upload.py`, daily 12:30Z). It converts six modes only (demque-backfill, daily, backfill, names, history-owed, etf_history_backfill), at held cells-per-row. It carries NO mode for A1 (models), A4 (research price axis), A5 (constituents), and it appends an absent `bbgtml-unmetered` row when no `bbgtml-*` record exists. So "every production leg complete" is readable from it for A2 and A3 only. Named gaps for the CloudOps/MSTR half: a completeness line for A1, A4, A5 (the CTO's ruling and the relay both assume the ledger carries them).
- **A4 (CTO msg 6304):** AMGT_RESAPP's A4 window step 1 (30 to 90 days, about +4,250 observations a day, ledger mode `amgt-price-axis`) goes first and never on the same trading day as a ramp step. `amgt-price-axis` is not in the uploader's conversion table, so it reads absent; the round-10 cell adds that row once COO~R1 confirms one cell per observation. This seat holds: no ramp step on the day of an A4 step or the day after, and posts each ramp step day in the CTO's ramp ruling file.

- **Confirmed by COO~R1 (msg 6306, ~22:4xZ):** ledger mode `amgt-price-axis` is written by `price_axis_pull.py` after the pull; `rows` is the non-null PX_LAST observations the vendor returned, summed over every name before trimming; PX_LAST is the only field, so one observation is one cell; the batch id ends `rows_unit=returned-observations`. The round-10 cell adds a conversion row `amgt-price-axis` to `bbg_ledger_upload.py` with channel `history`, one cell per row, claim `held` (a count of returned observations, not a vendor meter). A4's step 1 target day is not set; it follows the day-0 read of the first price-leg fire and R1 reports it in the message that says the commit landed.
