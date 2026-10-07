# L8 drain end -- IRPT_DASHBD round 23, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~14:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @0850a6efdb

The one order of the round is terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer before
the drain). 0 JUDGMENT criteria. Risk LOCAL: build and local run only, no S3 write. The worktree and branches were removed. On:
`1.0.0_SA_CTO~DELL2`'s round-22 analysis @a1873a8be7 (PRD backlog B2, FWD-4).

## The order

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-35 (`account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`, 49F) | @a8df9a5880 (worker ~20: cfb9a56b0b, 59a5047d4d, b11d88c3b2, 583534dee5) | DB23-1-AC1..AC3 PASS | 100 accounts x 24 trading days (2026-09-01..10-05): 2,182 activity rows, 726 realized lots, 160,549 unrealized lot-days; a second run reproduces all three tables exactly. The named account-window ties within one cent (gap 0.0025). 726 of 726 realized lots tie to their closing transaction; the negative control (no transactions) leaves 726 of 726 untied. The three table addresses re-derive from `lib/opal_naming.py` |

Files: `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` and its 23 tests; three contracts under `org/standards/`
(`IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json`, `..._LOT_REALIZED_...`, `..._LOT_UNREALIZED_DAILY_...`). Drain hygiene: commit-gate
clean; the folder's suite 70 passed. RLD vintage: each `fact_rld` partition holds that day's closed lots; 24 per-day partitions read.
Pre-2010 lots are listed, never estimated (86 realized in the sample, oldest acquired 2006-11-09).

## Read before grading -- FWD-4 is NOT shown by this round

- **AC1 passed on a window that does not exercise the realized term.** The named account-window's realized gain, contributions and
  withdrawals are all 0; only unrealized change and income move. The criterion is met as written, and it says little about realized gain.
- **Row IRPT_DASHBD-W20-S2:** across the sample, 52 of 91 graded account-windows tie within one cent; 39 do not. Most miss by cents
  (consistent with rounding over 24 days), a few by more, and one account by about 1.1 million. The gaps are labelled
  `GAP_ABOVE_ALLOWANCE` with the gap carried, never plugged. The cause was not diagnosed in this cell. FWD-4's "an activity summary
  whose figures agree with the transactions" is not met on this sample.
- **Row W20-S1:** the lot tables' source names and columns are typed in the producer, because `sources.json` was outside the grant; they
  move into the declaration with the release, as W18-S1's did.
- **Row W20-S3:** the custodian's lot event ids repeat (131 distinct `close_event_id` over 726 lots), so both lot keys are composites.

## Rows in the round

| row | class | standing |
|---|---|---|
| W20-S1 | OBSERVATION, INERT | open: lot source names typed in the producer; move at release |
| W20-S2 | OBSERVATION, INERT | open: 39 of 91 windows outside a cent, one by ~1.1M -- for the CTO's analysis |
| W20-S3 | OBSERVATION, INERT | open: composite lot keys |

OPEN 3, ARMED 0 (comp-surprise after the drain).

## What the round leaves

- The cause of W20-S2's gaps, above all the ~1.1M account, before these tables are released.
- The class release (round 22) waits only on the terraform kit; both halves are given and the pins are this seat's at the apply.
- FWD-8 stays HELD on Andrew's per-use word for the split BD pull.
- The live thread trace (FWD-1 hop 5) was not re-run; its last exercised run stays 2026-10-02 (STATUS~D).
