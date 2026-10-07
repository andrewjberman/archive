# AMGT_CORPUS round 39 -- never-widen pair for `CRPS-ao-2`: re-pin the daily task to the pull-date skip key, plant ONE same-UTC-day re-derive, and read the 2026-10-07 13:00Z fire

**Authority:** round-38 analysis @`9619211bcf` ruling 6 ("the same-day skip keys on the PULL date. It is proved by a 03:00Z
re-derive plant followed by a fire that still pulls. Acceptance is the first SCHEDULED fire after the cell lands, read by the CVO";
CTO msg 30045). Decomposition v39.0 @`969cdbff2f` s.1. Producer change CRPS-ao-1, drained @`662cd2b11d`.

**Code:** `<p>` = `662cd2b11d`, or a descendant whose `model_block_pull.py` equals it. The current pin is `6f6e472641` (round 38's
an-2). Measured between the two pins over the fire's import closure (the `induction_scheduled` module plus the lazily loaded
`model_block_pull.py`, 21 `lib.`/`integrations.` modules; 16 non-test `.py` changed under `lib/research` and
`integrations/bloomberg` between the pins):
1. `integrations/bloomberg/research/model_block_pull.py` -- ao-1 only (+34/-4): `cmd_refresh` reads the newest PULL-LOG stamp
   per name through one paginated listing (`_pull_log_latest_stamps`) instead of the newest derived stamp. `stage_pull`,
   `stage_derive`, `cmd_admit`, field lists and key builders are untouched.
2. `lib/research/identity/build_universe.py` -- AMGT_RESAPP av-7 (`453ae8713c`) and aw-6 (`d3d9277e1e`), landed under their own
   orders: the pool universe reads the newest stored SEC object, and keeps the prior filing form when the filer list cannot
   decide. It rides in the pin and IS in the fire's closure; it is read on the first fire as part of the induction step's rc.

## THE DRY RUNS AT THE CUT

| check | result |
|---|---|
| `checks/round39/skip_key_check.py` on CLOUD @`662cd2b11d` | `skip build 1/1 control 2/2` |
| `model_block_pull refresh --dry-run` on CLOUD (real S3 read, no Bloomberg session) | `registered 96 with_block 96 already_current 96 pulled 0` -- right today: all 96 were PULLED on 2026-10-06 (round 38's same-day pull) |
| `model_block_pull derive --securities "BA US Equity" --no-sa-fallback --dry-run` | `1 of 1 securities planned, 0 written`; reads the latest paired bronze stamp; `sa_fallback held_off` |
| `schedule_induction.ps1 -Plan -Commit 662cd2b11d` | Python311 (source: live-task); `cmd.exe /c ... induction_scheduled --mode fire`; daily 13:00Z, first 2026-10-07T13:00:00Z |

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r39-ao2`, opened before leg r)

0. **Gate.** The CTO half signed. `-Plan -Commit <p>` names Python311 (live-task).
1. **(r)** `schedule_induction.ps1 -Register -Commit <p>`, then `-Status`: Start In = the `<p>` pinned workdir. Runs BEFORE
   2026-10-07 13:00Z; no fire falls between (r) and that fire.
2. **(p) the plant.** After 00:00Z and before 12:30Z on 2026-10-07: `model_block_pull derive --securities "BA US Equity"
   --no-sa-fallback`, on BA's newest raw stamp (the 2026-10-06 pull). Then read: BA's newest derived stamp is 2026-10-07; its
   newest pull-log stamp is 2026-10-06; `refresh --dry-run` lists `DRY-RUN REFRESH: BA_US_Equity` (not SKIP). That is exactly
   the state that silenced 96 of 96 on 2026-10-06.
3. **(v)** Read the 2026-10-07 13:00Z fire's log: `BA US Equity` in the REFRESH set, `already_current 0 pulled 96`, rc 0. Then the
   served model-block census (`checks/round38/count_ratio_currency.py --served`: build 1/1 control 1/1) so the round-38 currency
   labels hold on the new pull. The CVO's read of this fire is FWD-22's acceptance; Z-S88 disarms on it.

## EXPECTED OUTCOME (every branch)

- **Writers:** the skip decision has 1 rule (`cmd_refresh` at `<p>`); BA's served block has 1 writer (`stage_derive`); the task's
  Start In has 1 writer (`schedule_induction.ps1`).
- **Branch A:** the fire pulls 96 including BA, rc 0. Z-S88 disarms; FWD-22 goes to the CVO as exercised.
- **Branch B (one or more names fail to pull or derive, rc 1):** each failure is listed; a failed name keeps its prior block. The
  skip proof holds if BA is in the REFRESH set (pulled or failed-on-pull, never SKIP).
- **Branch C (the Terminal is unreachable, rc 4, `ADMIT_REFUSED_LINE`):** nothing is pulled and nothing served moves. Not the
  pin's failure (CTO standing direction: a Terminal-down fire is never Branch C of a code act). The plant stays; the next
  scheduled fire is the read. No ad-hoc fire without a CTO ruling.
- **Branch D (the plan names a non-Python311 interpreter, or `-Register` refuses):** STOP before (p). The task stays on
  `6f6e472641`; the plant is not made (it would silence the old pin's fire, which is Z-S88 itself).

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| Scheduled Task `amgt-induction-daily` | Start In (pin `<p>`); interpreter and trigger unchanged | `-Register -Commit 6f6e472641` |
| `derived/model_block/BA_US_Equity/<2026-10-07 stamp>/model_block.json` (leg p) | ONE new write-once key, derived from the same raw stamp as BA's current block, so values move 0 | forward: the 13:00Z fire supersedes it; exact restore by delete needs Andrew's word |
| the 2026-10-07 13:00Z fire | the scheduled daily pull of the 96, exactly as on any day the skip does not fire: up to 96 raw/bronze and 96 derived write-once keys | the task's own next fire; `-Register -Commit 6f6e472641` |

Never touched: any Seeking Alpha call (refresh and the plant both run `sa_fallback=False`), any ad-hoc Bloomberg pull (the only
Bloomberg spend is the scheduled fire's normal daily pull), `field_map.json`, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-06 ~19:5xZ, for legs 0, r, p and v, covering branches A, B, C and D.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
