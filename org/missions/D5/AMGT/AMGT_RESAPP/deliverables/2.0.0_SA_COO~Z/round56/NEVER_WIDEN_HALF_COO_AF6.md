# AMGT_RESAPP round 56 -- `AMGT-af-6` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-01 ~06:2xZ

**The act (ONE):** merge branch `wk-AMGT_RESAPP-199` (af-3, head `bd145a4531`) into CLOUD on the site-Z shared tree, BEFORE the 07:00 ET
(11:00Z) fire of the Scheduled Task `OPAL_BBGTML_daily_pull`. That task's `:price_leg` step runs
`integrations/bloomberg/research/price_axis_pull.py` from this WORKING TREE, so the merge is the served act. Executor: this seat.
Decomposition s.64c; order `task-orders/AMGT_RESAPP.TO-AMGT-af-3.price-ranking-over-the-covered-names.md` (AC1 35 of 35, AC2 YES).

**What the merge changes in the producer:** the universe is no longer the 34-name `0.9.0_WK_AMGT_RESAPP~4/universe.json`; it is the
covered names read fresh from gold `research_dossier/` (95 at the cut; 95 mapped, 0 unmapped), each mapped by the identity crosswalk.
Names with fewer than 2 PX_LAST observations in the window, and any unmapped name, go into each product's own `excluded` record with a
reason. No schedule, no breakout rule, no table, no IAM change.

## THE BASE, read live at signing (06:2xZ) -- table `opal-harvest-security-metrics`

| key (`axis_date`, ticker `_CURRENT`) | state | generation_id | rows | run |
|---|---|---|---|---|
| `TRENDING_PRICE#2026-09-29` | COMPLETE | `20260930T110821Z-6a3068ca2435` | 32 | `R20260930T110821Z` |
| `BREAKOUT_PRICE#2026-09-29` | COMPLETE | `20260930T110827Z-5dee13d06724` | 32 | `R20260930T110821Z` |
| `TRENDING_PRICE#2026-09-30` | ABSENT (no item) | -- | -- | -- |
| `BREAKOUT_PRICE#2026-09-30` | ABSENT (no item) | -- | -- | -- |

Immediately before the merge, re-read these four keys. A 09-30 pointer that already exists is a STOP and a re-sign.

## WRITERS OF THE PROPERTY: 1

The PRICE generations have one writer: `compute_price_axis` (`lib/research/price/generation.py`), reached only through
`price_axis_pull.py main()` -- the 07:00 ET task step or a hand run on this box. Both read the same working tree, so both are covered.
No `--month`-style override exists; the as-of is `lib.trading_calendar.prev_trading_day(now)`.

## READERS

- `read_rankings` (the price bars) serves the requested date's pointer, else walks back to the latest COMPLETE pointer.
- `read_rank_series` and the overlay's per-name reads follow the same pointers (af-2's T-1 fallback, served only after round 57's
  redeploy).
- So a new 09-30 generation becomes the served price ranking the moment its pointer commits, and nothing else moves.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback per key

| key | what it MAY touch | rollback |
|---|---|---|
| `TRENDING_PRICE#2026-09-30` / `_CURRENT` | created (no item today) by the 07:00 ET run | re-run the producer from the pre-merge commit (`git show <pre-merge>:integrations/bloomberg/research/price_axis_pull.py`, same for `generation.py`) on this box: it overwrites the pointer with a 34-name generation (a write, never a delete) |
| `BREAKOUT_PRICE#2026-09-30` / `_CURRENT` | created (no item today) by the same run | the same re-run |
| generation partitions `<AXIS>#2026-09-30#<generation_id>` | new rows under a new generation id; no existing row is overwritten | none needed: an unreferenced generation is never served |
| the producer's record copy under `deliverables/0.9.0_WK_AMGT_RESAPP~6/` | one new JSON file per run | none needed |

Reverting the merge commit (`git revert -m 1`, a new commit) before the next fire restores the old producer for every later day.

## EXPECTED OUTCOME -- both branches, read from the producer's own rule (never predicted)

- **Branch A, the terminal session is signed in at 07:00 ET:** the run reads PX_LAST for the 95 mapped tickers over
  2026-08-31..2026-09-30. TRENDING_PRICE ranks every ticker with at least 2 observations by its 30-day return. BREAKOUT_PRICE ranks
  those with at least `min_breakout_observations` (3). Every other covered name appears in the product's `excluded` record with its
  reason. The row count is whatever the pull returns: the half names the rule, not the number.
- **Branch B, the session is not signed in (placement s.5 item 1, Andrew's login):** the pull fails (the step exits 80-83). No pointer
  is written, so the served ranking stays at 09-29 and DELTA=0. The new code waits for the next fire or Andrew's re-run after he signs
  in. FWD-35 is graded on the first scheduled generation, a QUALIFIED WAIT (PRD v0.32).

## THE GRADE (CTO round-55 analysis @5a3c8e4462 ruling 2)

The served read after the fire compares fields every write moves -- the 09-30 pointers' `generation_id` and `run_id` -- against the
pre-act values printed beside them (both ABSENT above), then reads `read_rankings('TRENDING','PRICE')`: `as_of_date` 2026-09-30, the
row count, the `excluded` record's count and names, and the covered denominator printed fresh. Branch B reads the four keys unchanged
(pointer still ABSENT at 09-30; 09-29 generation ids as tabled) and says so.

## WHAT THIS HALF DOES NOT COVER

No ad-hoc producer run (an ad-hoc generation is never FWD-35 evidence); no scoped-API deploy (round 57); no S3 or DynamoDB delete; no
vendor call (Bloomberg is the firm's own terminal session, the schedule's existing source).
