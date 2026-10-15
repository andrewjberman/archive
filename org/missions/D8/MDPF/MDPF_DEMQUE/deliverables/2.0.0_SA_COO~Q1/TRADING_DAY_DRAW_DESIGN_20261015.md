# Bloomberg history on trading days -- the measured design for the next round (issuer 2.0.0_SA_COO~Q1, 2026-10-15 ~19:4xZ)

**Input:** Andrew, verbatim, relayed by the CTO (msg 6164, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261015_193xZ_BBG_HISTORY_MAY_DRAW_ON_TRADING_DAYS.md` @5e75337456): "Yes Bloomberg history may also happen on trading days." Read as worded: the whole history channel, from the quota left after production, through the queue, in the ruled order (B1, failed-14, the porting test, ADVI_COTBKF's 27 active slices, then the seven ETFS_RIVALS requests). The CTO's instruction: change the drawer schedule in the next round and restate the finish dates from the first trading-day draw. This file is the issuer's measured read of what that change touches, filed so round 10 starts from it. Nothing here is built.

## What the code does today (read at HEAD `cc9c0fee07`)

| fact | where |
|---|---|
| The Windows task at site Z fires DAILY; the drawer's own gate stops a trading day (`STOPPED`, `stop_reason TRADING_DAY`, no vendor call) because "the Windows scheduler carries no NYSE calendar" | `standing_drawer.py` `run` near line 896; TO `MDPF_DEMQUE.TO-DQ-t27` (CloudOps `~ZQ`, complete) |
| A non-trading day's room is the measured history ceiling (5,858 cells) PLUS the cells production left unused on the trading days since the previous fire day: `carried_over = sum(max(ceiling - spent[d], 0))` over those days, `spent[d]` read from that UTC day's budget ledger `bbg_budget_<d>.jsonl` | `standing_drawer.py` `carry_over`, `_day_spent`, `previous_fire_day` (DQ-t-54) |
| The quote counts a backfill only on days a drawer fires, defined as every NON-trading day, at the measured ceiling, reserve NOT subtracted; a trading day's backfill allowance is 0 | `bbg_quote.py` `_history_backfill`; `drawer_schedule.is_fire_day` |
| The history ceiling is `5858`, claim `measured`, "a FLOOR (a day drawn with no refusal), not a capacity"; the history RESERVE is `7322`, claim `held`, `round(5858 x 1.25)` from the same ledger day | `bbg_allowance.json` |

## What follows

1. **No new schedule is needed at site Z.** The task already fires daily. What stops a trading day is one gate in `run`. The change is code: on a trading day the room becomes `max(ceiling - production_spent_today, 0)` (the same `ceiling - spent[d]` that DQ-t-54 already computes for a trading day, taken on the day instead of at the next weekend), read from that day's budget ledger; an unreadable or absent ledger gives room 0 (fail closed: production's spend is then unknown).
2. **The carry-over then double counts unless it changes with it.** With every day a drawing day, `previous_fire_day` is yesterday and no trading day sits between two fires, so the carry is 0 by construction. `previous_fire_day` and the tests that pin the old rule change in the same cell. The quote's `is_fire_day` (non-trading days) stays, because the frozen quotes are the pessimistic dates; the restated dates come from the observed rooms (step 5).
3. **The reserve cannot give "quota left after production".** The history reserve (7,322, held) is larger than the ceiling (5,858): `ceiling - reserve` is negative, so no figure on file yields a trading-day room. The only measured source is production's actual spend per day, the budget ledger. That ledger lives where production runs: `bbg_budget.ledger_dir()` reads `C:/Users/Test/AppData/Local/opal_bbg_budget` on this box and the directory does not exist here. So the cell is graded on dell1 with FIXTURE ledgers and the real allowance file, and its real exercise is a site Z act.
4. **The drawer must fire after production finishes.** The daily task's trigger time is set "after the Bloomberg Terminal's sign-in window" (TO t27); production's pull is scheduled at 07:00 ET (`scheduled_daily_pull.cmd`). Whether the trigger is after production's last history draw of the day was NOT measured here. It is the first thing the CloudOps cell reads (task trigger time against the day's ledger timestamps); if the trigger is early, the cell moves the trigger, not the code.
5. **Restating the finish dates** (CTO instruction): after the first trading-day draw, re-quote the open requests with `quote(fire_days=...)` over the days the drawer actually drew, using the rooms observed. Until a trading day is observed the frozen quotes stand; a quote built on an assumed trading-day room would be a `held` value, so it is labelled `held`.
6. **Reference and bql are not covered.** Andrew's word is about history; the reference-channel room on a trading day stays 0.

## Cells for round 10 (the issuer's proposal; the CTO's analysis rules)

- `DQ-t-69` (worker, code, LOCAL for the build): the trading-day room, the `previous_fire_day` change, the tests that pin the old rule; criteria on fixture ledgers plus the real allowance file.
- `DQ-t-70` (CloudOps `~ZQ`, WORLD): confirm site Z runs the merged code; read the task trigger against production's ledger timestamps; exercise the first trading-day fire; a change-management entry; the CTO's exercised read. Gated behind `DQ-t-69` and behind `TO-DQ-t34` (the same drawer; its AC2 waits on the 2026-10-17 fire).
- The issuer's act after the first trading-day draw: restate the finish dates.

**Risk named:** the ceiling is a measured floor of a completed day, not a vendor cap. A trading day that draws the ceiling in total (production plus backfill) stays at or below a total already drawn once without a limit warning; it is not proof that a larger total is safe. The drawer already stops on a vendor limit warning or a refusal.
