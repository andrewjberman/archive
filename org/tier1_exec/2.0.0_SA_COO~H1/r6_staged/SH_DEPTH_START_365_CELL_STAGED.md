# STAGED (not issued) -- MDPF_SECHIST round 6 candidate: depth backfill starts 365 days back, not 372, and declares its class

Source: `1.0.0_SA_CTO~DELL1` msg 4890 (READ-acked 2026-10-13 ~14:2xZ), answering this seat's scope question (msg 4888) on Andrew-direct
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_141xZ_BACKFILL_FLOOR_2012_AND_EARLIEST_CLIENT_RECORD.md`. Verbatim from the
CTO: "yes, it reaches etf_daily_pull -- non-client class, 365 days from need; DEPTH_START_DAYS 372 becomes 365"; "It is a market-context need,
so its start is 365 days back from the need, not the earliest client record. Cut the round-6 cell: 372 becomes 365, with the trading calendar
resolving the first business day, and the request declares its class at the queue." Round 5 is open and frozen, so this is staged, not cut;
it enters the round-6 rectangle on the round-5 analysis's enrichment list and is batched with `SH_EXHAUSTED_EXPIRY_CELL_STAGED.md` so site Z
takes `etf_daily_pull.py` once.

## The cell (worker-light; risk SERVED; LOCAL code + tests)

`integrations/bloomberg/pipeline/etf_daily_pull.py`: `DEPTH_START_DAYS` 372 -> 365. The window start for a security needing depth is the first
business day on or after `asof - 365 days`, resolved by `lib/trading_calendar.py` (the one frontier), instead of a bare calendar offset. The
request carries its class, "market-context" (non-client), where the queue reads it.

## Named, not decided (the analysis or the CTO rules these)

1. **The reason 372 existed.** The module comment says one year plus a week, "so the 1Y window's start day is always inside the series". At 365
   the start day of the 1Y window can fall outside the stored series when `asof - 365 days` is a non-trading day. The cell needs a dated
   example (a weekend and a holiday `asof - 365`) read against the consumer of that window, before the constant moves.
2. **Where the class is declared.** The CTO's wording is "declares its class at the queue". Today the daily pull draws Bloomberg directly at
   site Z under its own budget ledger and files no queue request. Whether the depth backfill is re-routed through the MDPF_DEMQUE queue, or the
   class is stamped into the run manifest's `history_backfill` block for the queue to read, is not stated. One question for the CTO.
3. **Tests.** `test_etf_daily_pull_history_plan.py` pins the window arithmetic; the cell updates it and adds the weekend and holiday cases.

## Paths

`integrations/bloomberg/pipeline/etf_daily_pull.py`, `integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py`.

## Criterion (not written)

A dry-run-at-base check is written at the cut, once items 1 and 2 are ruled: a named-test criterion on the weekend and holiday cases.
