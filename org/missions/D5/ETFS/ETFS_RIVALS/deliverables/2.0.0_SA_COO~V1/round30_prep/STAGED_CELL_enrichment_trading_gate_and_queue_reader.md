# STAGED (not issued): the enrichment leg's trading-day gate and queue-state reader, ONE cell for site Z

Issuer 2.0.0_SA_COO~V1, 2026-10-12 ~21:3xZ. NOT a task order: round 29 is EXECUTING (the spec is frozen mid-round), so this is
prep for the next issuance. Un-park: site Z's weekly limit resets 2026-10-14 06:00Z. Authority: CTO analysis
`ledger/ROUND_ANALYSIS.round28.md` section 3 items 6 and 7, and CTO msg 4568 ("one cell with the gate, at the site-Z window --
accepted"): one cell, because both edit `data/etfs/scripts/rivalfunds/enrichment_bloomberg.py` and deploy only at site Z.

## The cell (proposed id RIV-xe-1)

1. **Trading-day gate** (analysis 2.3). The vehicle's enrichment leg runs on TRADING days only, read from
   `lib/trading_calendar.py` (`is_trading_day`). On a non-trading day it prints ONE line beginning `SKIP:` and exits 0, so the
   vehicle's exit line reads a skip and never `97` or `95`. Measured cause: 2026-10-10 (a Saturday) exited 97 because the
   MON-FRI daily Lambda had not built G1 for the previous trading day before the leg looked; 2026-10-11 (a Sunday) exited 95 on
   a signed-out Terminal. How `round28/tw1_j1_read.py` classifies a `SKIP:` run (it keys on a STEP line and an exit code other than 97) is NOT read here: set it, with a check, in the issuance that cuts this cell.
2. **Queue-state reader** (row D1-S2; CTO ruling at round 22 ADDENDUM 7, XA-20261009T033809Z-8c1a condition 1). Before each
   history-owed draw the leg reads the standing request's `state` at the builder address
   `s3://opal-data-assets/bloomberg/global/silver/request_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json`
   (`lib.opal_naming.address("bloomberg","global","silver","request_state","request=ETFS_RIVALS-HISTORY-OWED-DAILY","state.json")`;
   recorded in `org/missions/D8/MDPF/MDPF_DEMQUE/requests/ETFS_RIVALS-HISTORY-OWED-DAILY.json`, writer DQ-t-16 complete). Three
   arms, the CTO's: `active` draws as today; `paused` (or `stopped`) draws ZERO rows and logs one line naming the state; an
   unreadable or absent state draws ZERO and logs that it could not be read (fails closed, never draws on a failed read).
3. **Checks to write and dry-run before the cut:** the gate's arms (a trading day runs the leg; a Saturday, a Sunday and an NYSE
   holiday print `SKIP:` and exit 0; the calendar source is `lib/trading_calendar.py`, never a typed date list) and the reader's
   three arms with an injected state reader (no S3 in the check).
4. **Bounds:** the switch (`RIVALFUNDS_HISTORY_OWED`) is NOT set by this cell; the switch-on is its own act under the pair.
   No Bloomberg call in any check.

## Deploy and pair

A site-Z producer change: `1.0.0_SA_CTO~Z`'s never-widen half, applied by `0.7.0_AE_CloudOps~ZV` (a site-bound act, via a
crossbox ORDER; the manager commits the record, MSTR lane). Not under Andrew's no-modify order (that covers
`integrations/bloomberg/pipeline/` and the vehicle scripts; this file is in `data/etfs/scripts/rivalfunds/`).

## Also staged for the same window

C-S85's clock advance (the CVO's compile carries it; it needs site Z's file, one writer).

## Window class (Andrew-direct 2026-10-13, CTO msg 4886, ADDENDUM 1 to `ANDREW_DIRECT_20261013_141xZ_BACKFILL_FLOOR_2012_AND_EARLIEST_CLIENT_RECORD.md`)

The standing request `ETFS_RIVALS-HISTORY-OWED-DAILY` is re-declared NON-CLIENT with a 365-day window by the CTO and Q1 (re-priced at the queue before its
next draw); a request that asks beyond its class window is refused at the queue. The producer already asks 365 days back from the page day
(`history_owed.owed(s, day, window_days=365)`, `enrichment_bloomberg.py` reads it through `_history_owed`), so this cell changes no window. Its checks
carry one arm: the owed set's earliest date is not before `page_day - 365` (the 2012-01-01 floor binds both classes).

## ADDED 2026-10-13 ~17:3xZ: three more site-Z changes from the DEMQUE form (still STAGED, not issued; round 29 still EXECUTING)

Source: CTO msgs 4932 and 4969 (Andrew-direct 2026-10-13), form `org/tier1_exec/1.0.0_SA_CTO/deliverables/DEMQUE_QUEUE_FORM_ANDREW_20261013.md` A3
and rows Z3, Z4 of its "FOR SITE Z" table. The CTO's word is "cut beside"; the cut waits for the round-30 issuance (one issuer, one issuance, spec
frozen mid-round). Chains, by write surface:

| id (proposed) | change | files | chain |
|---|---|---|---|
| RIV-xe-1 | the gate and the queue-state reader (above) | `enrichment_bloomberg.py` | A |
| RIV-xe-2 | Z3 dividends incremental + TWR on the owed request | `enrichment_bloomberg.py` (`DEFAULT_WINDOW_DAYS`, `build_plan`, `BACKFILL_FIELDS`, `_history_owed`), `history_owed.py` summary only | A, after xe-1 (same file) |
| RIV-xf-1 | Z4 ACWI and IWM removed from the holdings pull and the universe | `universe.py`, `collector_bloomberg.py`, and the tests that name them (`test_r5l1_leg_inert.py`, `test_r8lg1_leg.py`, `test_r9cb1_bbg_budget.py`) | B (disjoint) |

**xe-2, Z3.** `DEFAULT_WINDOW_DAYS = 730` (`enrichment_bloomberg.py:110`) is what `build_plan` applies to every security every day. The cell: a security
with no stored `corporate_actions` row of any kind (a `NO_RECORDS` status row counts as pulled) gets ONE 365-day `DVD_HIST_ALL` pull; every other
security gets the window from the 5th trading day back (`lib/trading_calendar.py`, never a typed date list). NOT read here: how G3 readers treat a
date partition (the object each day lands is the window it asked: a 5-day object under a reader that takes only the newest partition would MOVE
SERVED OUTPUT). The issuance reads the consumers first and carries a never-widen pair (CLAUDE.md section 5) or a stated reason it needs none.

**xe-2, TWR.** `BACKFILL_FIELDS = ["PX_LAST"]` (`enrichment_bloomberg.py:720`) is what the owed request asks, so the owed set is close only: the GAP the
form's census names. Add `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS`, 365 days before need. Cells = units x fields. The form caps a run at 20,000
CELLS, but `HISTORY_OWED_CAP = 20000` (`enrichment_bloomberg.py:901`) counts UNITS (security x date), so with two fields the code would ask 40,000
cells: the cell makes the cap count cells (10,000 units at two fields) or sets the constant to 10,000, and its check asserts the cells asked. Price it from the live owed set, not from this
file: the 2026-10-08 read was 184,600 units over 251 dates for 742 securities (round 27 status), which at two fields is 369,200 cells, about 18.5 runs
at the cap against about 9.2 for the close alone. That figure PREDATES the removal of ACWI and IWM and the 365-day class, so the issuance re-reads
`history_owed.summary(owed(s, day))` first and states the runs. The queue request `ETFS_RIVALS-HISTORY-OWED-DAILY` (Q1's file in
`org/missions/D8/MDPF/MDPF_DEMQUE/requests/`) carries the field list, so Q1 re-files it; that is one ask to `2.0.0_SA_COO~Q1` at the cut.

**C1 RULED (CTO msg 5166, 2026-10-13 ~20:3xZ, on `RIVALFUNDS_PAGE_HISTORY_NEEDS_MEASURED_20261013.md` @a100e2490e): xe-2's owed request is FIELD-MATCHED and STAGED.**
- Total return only on the rankings' held days (123,933 units); the close only on the curves' days (89,216 units); the 36,705 units outside the page are not
  drawn. Total 213,149 cells, counted in CELLS against the 20,000 cap (about 11 runs).
- Staged newest period first: 30d (2026-09-12), then 90d (2026-07-14), then 365d (2025-10-12).
- Andrew confirmed ~21:0xZ 2026-10-13 (CTO msg 5197), VERBATIM as relayed: "C1 yes, approved in that order". The CTO's ruling now stands on his word, recorded in
  the DEMQUE form. Queue order is held by `2.0.0_SA_COO~Q1`: surface B before C1 stage 1 (30d).
- Lands from the CTO's round-29 analysis, unless the cut is a queue request only, in which case `2.0.0_SA_COO~Q1` files it. The cell's checks assert the
  field asked per unit, the cells counted, and the stage order. The figures are the 2026-10-13 read: the issuance re-reads `owed_size.py` first.

**xf-1, Z4.** `universe.py:25` marks ACWI and IWM `"leg": "pending"` behind `RIVALFUNDS_LEG_D13`, `collector_bloomberg.py:350` sizes them
(`CONTROL_ROW_CAP`). Removal is the entries, their cap and the three tests. Check arm: after the change no `ACWI` or `IWM` in `universe.funds()`
with the flag on or off, and the holdings plan's fund list equals the prior list minus those two (printed before and after).

**Deploy.** All three are producer changes under `data/etfs/scripts/rivalfunds/`, deployed at site Z by the same crossbox order as the staged cell,
one pair covering the set. Window: site Z un-park 2026-10-14 06:00Z.
