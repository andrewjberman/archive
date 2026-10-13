# MDPF_DEMQUE.TO-DQ-t34 -- post-reboot NEVER-2 artifact measurement

**Seat:** `0.7.0_AE_CloudOps~ZQ` (site Z, re-seated after the 2026-10-13 18:57Z reboot; CTO~Z msg 33696/33700)
**Measured at:** 2026-10-13T19:2x-19:4xZ, `box/sitez` @`549c4f26c7`
**Entry measured:** `mdpf-demque-zq-t34-close` (OPEN at read time; now HELD-SOVEREIGN-GATED)
**CTO site-Z half:** `CTO_HALF_MDPF_DEMQUE_T34_SITEZ_DRAWER_CLOSES_COMPLETED_20261011_Z.md` @`2d0bc9b7e8`

repo-relative: `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_DEMQUE_ZQ_T34_POSTREBOOT_MEASURE_20261013Z.md`

## VERDICT: the deploy is NOT half-landed. L1 and L2 stay closed; only the AC2 verify leg L3 is open, on a clock.

Neither branch of msg 33700 applies: the world does not show L3 done (so not SUPERSEDED), and nothing is
half-landed (so nothing to finish or roll back). The entry is now on a named external hold with a re-read date,
so it reads KNOWN-HELD rather than aging into a RED nobody owns.

## 1. The artifact, measured by CONTENT with controls

`git rev-parse <ref>:<file>` on the three granted files, plus `git hash-object` on the working bytes:

| file | signed candidate `8152a8ea42` | HEAD `549c4f26c7` | working bytes | pre-merge `66d0e6577f` (negative control) |
|---|---|---|---|---|
| `standing_drawer.py` | `b9b5e95743` | `ec390b1bc3` | `ec390b1bc3` | `d3be03d854` (differs -- control OK) |
| `test_demque_standing_drawer.py` | `b3ab220789` | `77aa07b510` | `77aa07b510` | `f7dbfdc345` (differs -- control OK) |
| `test_demque_standing_drawer_close.py` | `4c3f5a8c62` | `5773e5e9b3` | `5773e5e9b3` | ABSENT (control OK) |

**The blobs moved off the signed candidate, and the cause is named, not inferred.** `git log 9037d7b4c2..HEAD`
on exactly those three paths returns TWO commits out of a 6,013-commit span, both the issuer's own round-9
worker on a later cell:

- `0b5d4015f1` build(MDPF_DEMQUE round 9, DQ-t-44, `0.9.0_WK_MDPF_DEMQUE~36`)
- `db708a8ef7` fix(MDPF_DEMQUE round 9, DQ-t-44, `0.9.0_WK_MDPF_DEMQUE~36`)

So this is authorised later work on the same files by the same project's own fabric, not drift of my act, and
CTO half condition 2's revert clause is not triggered by it. The merge is contained
(`git merge-base --is-ancestor 9037d7b4c2 HEAD` -> YES; candidate `8152a8ea42` -> YES), but containment is the
ancillary reading here; the oracle is the content comparison above plus the behaviour check in section 2.

## 2. The delivered behaviour still holds at HEAD

- **AC1** `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R9_CHECKS/dq_t34_tests.py` -> `CL-OK`,
  3 passed (`..._is_closed_and_skipped`, `..._records_complete_not_drawn`, `..._no_zero_cell_drawn_line_after_completion`).
- **Whole demque suite** `python -m pytest data/mdpf/scripts/demque/ -q` -> **183 passed**, 0 failed. L1's proof
  recorded 139 at the merge; DQ-t-44 added tests. Nothing regressed.
- **AC2** `python .../dq_t34_close.py` -> `CLOSE-BAD no COMPLETE row yet (2 rows for the job, 11716 cells drawn)`
  -- the expected date-gated reading, byte-identical in substance to the 10-11 reading.

## 3. The two fires since L2 both held the trading-day gate, including the one that survived the reboot

`mdpf-demque-drawer-daily`: State `Ready`, LastRunTime **2026-10-13 10:00:01** local, LastTaskResult **0**,
NextRunTime 2026-10-14 10:00, NumberOfMissedRuns **0**. Action unchanged:
`python.exe data/mdpf/scripts/demque/standing_drawer.py --apply`, working directory the repository root. The task
survived the 18:57Z reboot and its 10:00 ET fire today (14:00Z) predates the reboot.

Side effects, measured against a working positive control:

- `BBG_ACTUALS.jsonl`, denominator **5 rows** (whole file, no `head`): rows dated 2026-10-13 = **0**,
  2026-10-12 = **0**, 2026-10-11 = **1**, 2026-10-10 = **1**. Rows with `"outcome": "COMPLETE"` = **0**.
- **My first predicate was wrong and the control is how I know:** I grepped `"day": "<date>"`, which returned 0
  for the 10-11 positive control too. The ledger key is `"date"`; the corrected census is the one above.
- `MDPF_DEMQUE_ZQ_STANDING/` still holds exactly the three 2026-10-11 artifacts (`history-2026-10-11.parquet`,
  `receipt.2026-10-11.json`, `run.2026-10-11.started.json`) -- no marker, receipt or parquet for 10-12 or 10-13,
  so the trading-day gate returned before any of them on both fires.

2026-10-12 Mon and 2026-10-13 Tue are both trading days by `lib/trading_calendar.py` (which WARNs that it is
answering from the hardcoded NYSE fallback `NYSE/hardcoded-fallback-2010-2027`).

## 4. The L3 gate is real, dated, and one fire's allowance covers it

- `standing_drawer.py --schedule --from 2026-10-13 --days 10` -> `{"fires": ["2026-10-17", "2026-10-18"]}`.
- The task's trigger is `MSFT_TaskDailyTrigger`, `DaysInterval 1`, no `DaysOfWeek` restriction, Enabled True,
  `StartWhenAvailable` True -- **so it does fire on a Saturday.** Had the trigger been weekday-only the whole
  2026-10-17 gate would have been a wish; it is not.
- `standing_drawer.py --plan --request DEMQUE-TR-COMPARISON-DIVIDEND-PAYERS` (read only) ->
  `{"remaining_cells": 1004, "securities": ["MO US Equity", "XOM US Equity"], "window_start": "2025-10-09"}`.
- **The order's own "about 3,400 cells left" is stale, and the issuer already superseded it.** The live quote
  `DEMQUE-TR-COMPARISON-DIVIDEND-PAYERS.quote.json` was re-frozen by `2.0.0_SA_COO~Q1` at
  **2026-10-13T15:34:29Z** under Andrew-direct 2026-10-13 addendum 2 (CTO msg 4889): the window is trimmed to
  365 days (2025-10-09..2026-10-08, 251 trading days), the 11,716 drawn cells are kept, and the remainder is the
  identity set of 1,004 cells on MO and XOM. `finish_date` 2026-10-17 with `finish_date_claim` **`held`** --
  downgraded from `measured` by the issuer's own `correction` field, on the stated ground that the finish rests
  on that fire rather than on a measured rate. My independent `--plan` read corroborates 1,004 on the same two
  securities. My own prior fires drew 5,858 cells each, so one fire's room covers 1,004 comfortably.

No surprise row is owed for any of the above: the blob movement, the stale cell figure and the re-freeze are all
the issuer's own recorded acts, and AC1 still passes against them.

## 5. What is owed, and by whom

| item | owner | condition |
|---|---|---|
| L3 / AC2 `dq_t34_close.py` -> `CLOSE-OK` | `0.7.0_AE_CloudOps~ZQ` | the 2026-10-17 fire records the one `COMPLETE` line |
| the `proof_of_spec` instance + `proof-of-spec-check.py` | `0.7.0_AE_CloudOps~ZQ` | authored AT the fire; it cannot be valid before AC2 passes, so no skeleton is filed |
| close the ledger entry | `0.7.0_AE_CloudOps~ZQ` | after L3 carries proof |
| flip the order's `<status>` | `2.0.0_SA_COO~Q1` (issuer) | the assignee does not edit the order file |

Hold recorded on the entry: `gate-type external`, re-read **2026-10-18**, so a 10-17 fire that does NOT complete
the request resurfaces as `HELD-PAST-REREAD` -- its own finding class -- rather than as an aged OPEN.

-- `0.7.0_AE_CloudOps~ZQ`
