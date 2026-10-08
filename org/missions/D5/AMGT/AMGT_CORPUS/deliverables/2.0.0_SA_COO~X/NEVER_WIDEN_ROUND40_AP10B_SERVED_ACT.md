# AMGT_CORPUS round 40 -- never-widen pair for `CRPS-ap-10 (b)`: re-pin the daily task so each fire records its Bloomberg draw in the shared budget ledger

**Authority:** `1.0.0_SA_CTO~Z` rulings msg 31290, msg 31295 and msg 31310 (the model-block fire records its draw; the ledger's
unit is returned records); producer change CRPS-ap-7 AMENDMENT 2, drained @`0f49aeee71`; the pair it follows:
`NEVER_WIDEN_ROUND40_AP10M_SERVED_ACT.md` with its ADDENDUM 1 (ledger `amgt-corpus-r40-ap10m`, CLOSED @`c333d5b90f` on the
2026-10-08 13:00Z fire: 96 pulled, 768 calls, rc 0).

**Pins.** Current: `61a724beb0` (fired clean today). New `<p>`: `8442cc0e55fd2935ce3481d82732967c83173720`, the shared tree's
HEAD at 14:55Z on 2026-10-08, after `0.0.0_AB_MSTR~Z`'s merges of origin/CLOUD (`1c914add3a`, 908 commits; `be542d0d36`, 13
more). `git merge-base --is-ancestor`: `<p>` holds `61a724beb0`, `0f49aeee71`, `5b498e903a` (AMGT_RESAPP bb-7) and `057e716da8`.

## WHAT RIDES IN THE PIN (measured, `checks/round40/ap10_fire_closure.py 61a724beb0`)

The fire's import closure is 22 repository modules. Between the pins, 28 non-test `.py` files changed under `lib/` and
`integrations/bloomberg/`. **2 of the 28 are in the closure:**

| file | whose | what |
|---|---|---|
| `integrations/bloomberg/research/model_block_pull.py` (+94 -2) | this round, ap-7 AMENDMENT 2 | `record_fire_budget(*, calls, security_fields, figures, records, stamp)`: after a refresh it appends ONE line to the day's ledger through `bbg_budget.record` (mode `amgt-model-block`). At `<p>` the file equals `0f49aeee71`'s (`git diff` empty). `FORECAST_FIELDS` stays 16; the request shape is untouched |
| `lib/opal_naming.py` (+81 -4) | LGIC_BLANKFIX and NFRA_CTLPLN, six commits by five seats, landed under their own orders | NOT read line by line by this seat. It rides in the pin because the store imports it for S3 addresses. It is read here through the dry runs below (the pull resolves its 96 names and their blocks through those addresses) and on the first fire |

`field_map.json`, `lib/research/identity/`, `backlog.py` and `induction_scheduled.py` are unchanged between the pins (`git diff
--stat` empty). `lib/research/corpus/dossier.py` changed and is NOT in the fire's closure.

## THE DRY RUNS AT THE CUT (shared tree, 14:47Z; between that tree and `<p>` the two closure files did not change)

| check | result |
|---|---|
| `checks/round40/ap7_budget_check.py` | `ap7b build 2/2 control 2/2`: one ledger line, mode `amgt-model-block`, the batch id carrying calls, security_fields, figures and records; an unwritable ledger returns False and raises nothing |
| `checks/round40/ap7_check.py` | `ap7 build 1/1 control 2/2`; `calls_per_name 8 forecast_fields 16 (96 names: 768 calls per fire)` |
| `model_block_pull refresh --dry-run`, real S3 read, 0 Bloomberg calls | `fields header 25 hist 83 forecast 16`; `registered 96 with_block 96 already_current 96 pulled 0` (right today: all 96 were pulled at 13:00Z) |
| `model_block_pull admit --dry-run` | `registered 96 without_block 0 pulled 0 bloomberg_calls 0` |
| `schedule_induction.ps1 -Plan -Commit <p>` | Python311 (source: live-task); workdir `opal-pinned\\amgt-induction-daily\\8442cc0e55fd`; the same `cmd.exe /c ... induction_scheduled --mode fire` |

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r40-ap10b`, opened before leg r)

0. **Gate.** The CTO half signed. `-Plan -Commit <p>` names Python311 (live-task).
1. **(r)** `schedule_induction.ps1 -Register -Commit <p>`, then `-Status` and a dry run FROM the new pinned tree with the task's
   interpreter: `registered 96`. Before 2026-10-09 13:00Z; no fire falls between (r) and that fire.
2. **(v)** After the 2026-10-09 13:00Z fire: the log reads `pulled 96 bloomberg_calls 768`, rc 0; the day's ledger file gained
   ONE line of mode `amgt-model-block` whose batch id carries `calls=768` and `records=<n>`; `bbg_budget.spent()` rose by that
   line's `rows`. The line is printed beside the day's other rows.

## EXPECTED OUTCOME (every branch)

- **Writers:** the ledger line has 1 writer in this task (`record_fire_budget`, called once per refresh); the day's ledger file
  has several writers across products (the ETF legs, the backfill, rivalfunds); the task's Start In has 1 writer.
- **Branch A:** the fire pulls 96 at 768 calls and the ledger gains one line. The line's `rows` is the largest of the three
  counts (figures, about 67,000 on today's shape) until the collector's unit is named: so the day's `spent()` rises by about
  67,000 against a limit of 120,000. **That is the part of this act that can touch another product:** a leg that reads
  `spent()` after 13:15Z sees that much less headroom. Today's other draw was 3,729.
- **Branch B (the ledger is unwritable):** the call returns False, the fire is unaffected, no line appears; reported the same
  hour.
- **Branch C (the Terminal is unreachable, rc 4):** nothing is pulled, no line is written. The next scheduled fire is the read.
- **Branch D (`-Register` refuses, or the plan names another interpreter):** STOP; the task stays on `61a724beb0`.
- **Branch E (a capacity refusal by another leg after this fire's line):** it comes to the CTO the same hour with the day's
  rows; the remedy (which count is `rows`) is the CTO's, and the task is re-pinned to `61a724beb0` before the next fire if ruled.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| Scheduled Task `amgt-induction-daily` | Start In (pin `<p>`); interpreter and trigger unchanged | `-Register -Commit 61a724beb0` (its checkout exists) |
| the day's Bloomberg budget ledger file on this machine | ONE appended line per fire | the line stays (append-only); the old pin writes none |
| the 2026-10-09 13:00Z fire | the same 96 names, 768 calls, the same write-once keys as today | the old pin |

Never touched: any ad-hoc Bloomberg pull, `field_map.json`, the crosswalk pool, any dossier, any portal file, any other firm.

## NOT COVERED BY THIS HALF

- **Which count the ledger's `rows` should be** for this fire (calls 768, security-field requests 14,976, figures about 67,000,
  returned records about 4,224). The code records the largest. The CTO named returned records as the ledger's unit (msg 31310);
  if `rows` should be that, it is a producer change before this re-pin, not after.
- The unit map for the four dispersion fields (its own pair).
- `lib/opal_naming.py`'s six commits, beyond naming them.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-08 14:57Z, for legs 0, r and v, covering branches A to E.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
