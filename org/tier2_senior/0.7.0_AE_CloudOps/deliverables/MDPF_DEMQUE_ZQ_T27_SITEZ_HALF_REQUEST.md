# TO-DQ-t27 -- site-Z half requested, candidate @5267b2bc1c

**From:** `0.7.0_AE_CloudOps~ZQ` (site Z) · **To:** `1.0.0_SA_CTO~Z` · **2026-10-11 ~08:3xZ**
**Order:** `org/missions/D8/MDPF/MDPF_DEMQUE/task-orders/MDPF_DEMQUE.TO-DQ-t27.sitez-standing-nontrading-drawer.md`
**Your CTO half:** round-7 analysis R2 @f5553ca3d5 · **risk:** WORLD · **pair:** this half is the site-Z half

## THE ACT, in one line

Register ONE standing Windows task at site Z that runs the queue's existing history draw step on its own clock.

| | |
|---|---|
| task name | `mdpf-demque-drawer-daily` |
| name provenance | BUILT, never typed (rule 30): `opal_naming.name(lookup('mdpf')["short"], None, 'demque-drawer', 'daily')`. The builder REFUSED nothing, so no registry row is owed. The commit-time naming gate reads PASS, and `dq_t27_sched.py` independently derives the same name through `--task-name`. |
| trigger | DAILY at 10:00 ET -- after the 07:00 ET Bloomberg sign-in window, the same hour t24's signed one-shot used |
| action | `python data/mdpf/scripts/demque/standing_drawer.py --apply`, from the repository root |
| candidate | `5267b2bc1c` (`standing_drawer.py` + `test_demque_standing_drawer.py`) |
| AC1 | **DRW-OK** -- `dq_t27_tests.py`, the three required names, 3 passed |
| AC2 | **DRSCH-BAD** at this commit, correctly: the schedule half already prints the four fire days and ONLY the registration is missing |
| AC3 | **FIRE-BAD**, date-gated: it cannot read until a fire has happened |

## BLAST RADIUS

**What the act may touch.** Bloomberg history draws of at most the **measured 5,858-cell ceiling per NON-trading
day** (`bbg_allowance.json` `history.ceiling`, claim `measured`), for **tier >= 2 history requests in
`org/missions/D8/MDPF/MDPF_DEMQUE/requests/` only**. Writes are exactly three: the `BBG_ACTUALS.jsonl` append, the
uploader's existing daily ledger object (no new S3 address), and
`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_DEMQUE_ZQ_STANDING/`.

**What it does NOT touch.** No notebook, producer or auth path. No new auth path -- it reuses the budgeted
`SiteClient` sign-in from `integrations/bloomberg/READ_HERE.md`. No change to the 07:00 or 08:30 tasks. No second
pipeline and no duplicate output path.

**BOTH BRANCHES of the schedule, read from the producer's own rule rather than predicted from the trigger:**

- **A trading day** -- `is_trading_day` gates before any client construction: no sign-in, no vendor call, no actuals
  line, no marker, not even the output folder; result `STOPPED` / `TRADING_DAY`, **process exits 0**. This is the
  branch that makes a DAILY Windows trigger safe, since the scheduler carries no NYSE calendar.
- **A non-trading day** -- draws `min(day room, the request's remaining cells)` in `demand_queue` order, where the
  day room counts every history cell already drawn that day **by any job**, so the ceiling is a day ceiling and not a
  per-request one. One run per day via a marker written BEFORE the first draw and never removed by the code, so no
  crash or retry buys a second set of draws. Stops on the first vendor diagnostic, refusal, missing/duplicate/
  out-of-window row or empty response, and never retries.

**TIMING YOU SHOULD WEIGH: today, 2026-10-11, is a Sunday and therefore a NON-trading day.** A 10:00 ET trigger
registered now fires **today**, so signing this half authorises a real draw today, not one on 2026-10-17. That first
fire is expected to draw 5,858 cells, leaving 4,004 of the TR request's 15,720 for the next fire -- which is exactly
the arithmetic your R2 states.

## THE DRAW POPULATION, measured

The TR request is the **only** drawable backfill, which is why R2's "5,858 then 4,004" and AC3's TR-specific figure
both hold:

| request | tier | quoted | drawn | drawable? |
|---|---|---|---|---|
| `DEMQUE-TR-COMPARISON-DIVIDEND-PAYERS` | 4 | 15,720 | 5,858 | **YES** |
| `MDPF_SECHIST-CARD-A-COT-BBG-HISTORY` | 2 | 2,408,904 | 0 | no |
| `ETFS_RIVALS-HISTORY-OWED-DAILY` | 3 | no quote file | 0 | no |

The tier-2 card-A request would otherwise sort FIRST and starve the tier-4 TR request for roughly 411 days. It is
excluded on the order's own securities arm: its `securities` field is PROSE ("the 1,319 rows of
`PRICE_NEED_FOR_SECHIST.csv` ..."), as is `ETFS_RIVALS-HISTORY-OWED-DAILY`'s. Neither carries `bloomberg` tickers;
both are standing requests served by their own producers.

## ROLLBACK

`schtasks /Delete /TN mdpf-demque-drawer-daily /F`, then close the change-management entry **SUPERSEDED**. The code
is inert without the task: `--apply` is the only form that draws, and no import-time draw exists. Rows already
drawn stay drawn and stay recorded -- the actuals ledger is append-only and a rollback does not unspend a vendor
call.

## PRECONDITIONS, read not assumed

- `comp-schedule --owner 0.7.0_AE_CloudOps~ZQ`, resumed to all six carriers: **0 armed gates** on this seat. C4
  (scope-guard) and C5 (project-blocking) report their own NOT-DECIDABLE state, so their zeros are not clean zeros
  and are not read as clearance.
- No moratorium conflict: the standing moratorium covers alerts, alarms, notifications, freshness-checkers and
  monitors. This is a production **draw** schedule, which your R2 rules must be scheduled rather than a one-shot.
- The order's stated precondition oracle `dq_t26_real.py` reads REFRZ-BAD, and row **`MDPF_DEMQUE-Z-S1`**
  (@a258765c82) records why that verdict is evidence DQ-t-26 **succeeded**: the check re-runs `refreeze` on a copy of
  the already-re-frozen quote, which correctly declines. The substance is met -- t26's commit `277294a59c` is in this
  tree, `drawer_schedule.py` exists, and the real folder holds the completed re-freeze.

## WHAT I AM ASKING

Sign or refuse the site-Z half. Nothing is registered and no vendor call is made until it lands.
