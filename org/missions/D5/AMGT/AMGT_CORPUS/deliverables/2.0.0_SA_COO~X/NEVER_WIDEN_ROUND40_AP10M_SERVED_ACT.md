# AMGT_CORPUS round 40 -- never-widen pair for `CRPS-ap-10 (m)`: re-pin the daily task so the scheduled fire carries the four consensus-dispersion fields

**Authority:** round-39 analysis @`5ccdc90368` ruling 10; `1.0.0_SA_CTO~Z` msg 30490 ("Probe ONE name first ... then let the daily
fire carry them. No one-off pull.") and ruling msg 31086 on the probe (pull the four that exist; the mean is `BEST_CPS` /
`BEST_EPS`; a standard deviation and its mean are for the same forecast period). Decomposition v40.0 @`be3481c83e` s.1.
Producer change CRPS-ap-7 with AMENDMENT 1, drained @`057e716da8`.

**Code:** `<p>` = `057e716da8`, or a descendant whose `model_block_pull.py` and `field_map.json` equal it. The current pin is
`662cd2b11d` (round 39's ao-2).

## WHAT RIDES IN THE PIN (measured)

50 non-test `.py` files under `lib/research` and `integrations/bloomberg` changed between the pins. The fire's import closure is
21 modules (`induction_scheduled`, the lazily loaded `model_block_pull.py`, `backlog`, `library` and what they import). **6 of the
50 are in the closure:**

| file | whose | what |
|---|---|---|
| `integrations/bloomberg/research/model_block_pull.py` | this round, ap-7 (+25/-1) | `FORECAST_FIELDS` 12 -> 16: `BEST_CPS_STDDEV`, `BEST_CPS_NUMEST`, `BEST_EPS_STDDEV`, `BEST_EPS_NUMEST`; basis, money and count sets. `stage_pull`'s request shape, `cmd_refresh`, `cmd_admit`, `HEADER_FIELDS`, `HIST_FIELDS` untouched |
| `lib/research/corpus/backlog.py` | this round, ap-1 (+16/-16) | the `fence14` printed line only; the population (`build`) is untouched |
| `lib/research/identity/crosswalk.py` (+7/-8), `build_universe.py` (+5/-6), `one_pager_precedence.py`, `lib/research/harvest/bloomberg.py` | AMGT_RESAPP and AMGT_HARVST, landed under their own orders | NOT read line by line by this seat. They ride in the pin and are in the closure; they are read on the first fire through the induction step's rc and the population count |

`build_unit_map.py` (ap-7, +16) is NOT in the fire's closure. `lib/research/corpus/dossier.py` (ap-6) is NOT in the closure.

## THE DRY RUNS AT THE CUT

| check | result |
|---|---|
| the one-name probe, `checks/round40/ap10_probe.py` on `BA US Equity`, 3 requests, 2026-10-07 15:17Z (evidence @`e3579e3693`) | the four fields RETURN on 1FY, 2FY and 3FY, in the same request as `BEST_CPS`, `BEST_EPS` and `BEST_PERIOD_END_DATE` (2026-12-31, 2027-12-31, 2028-12-31); the four names the consumer first listed read `BAD_FLD/INVALID_FIELD` and are in no list |
| `checks/round40/ap7_check.py` on CLOUD @`057e716da8` | `ap7 build 1/1 control 2/2`; `calls_per_name 8 forecast_fields 16 (96 names: 768 calls per fire)` |
| ap-7's period table (stub pull of BA US; worker report, drain `057e716da8`) | for 1FY, 2FY, 3FY the override of the request carrying each of the four equals the override of the request carrying `BEST_CPS` and `BEST_EPS`; derived `fiscal_period` equal (FY1, FY2, FY3) |
| `model_block_pull admit --dry-run` and `refresh --dry-run` on CLOUD @`27691f17ff` (its closure files equal `<p>`'s: `git diff 057e716da8 HEAD` on them is empty), 16:08Z, real S3 read, 0 Bloomberg calls | `admit population registered 96 without_block 0`; `refresh fields header 25 hist 83 forecast 16`; `refresh population registered 96 with_block 96 already_current 96 pulled 0` (right today: all 96 were pulled at 13:00Z). The same 96 as the old pin read at 13:28Z (`C3_PLANNED_POPULATION_FIRE_20261008.md` @`a8f380a4da`) |
| `schedule_induction.ps1 -Plan -Commit 057e716da8` | Python311 (source: live-task); `cmd.exe /c ... induction_scheduled --mode fire`; daily 13:00Z, first 2026-10-08T13:00:00Z |
| the Model sheet on the candidate portal, round 39's BA fixture with the four fields added to the forecasts | 62 rows before, 62 after, the sheet's shape equal; neither `BEST_CPS_STDDEV` nor `BEST_CPS_NUMEST` appears in the built sheet |
| `field_map.json` at `<p>` (118 entries) | the four fields are ABSENT from it; `BEST_CPS` and `BEST_EPS` carry a per-security unit for 100 names |

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r40-ap10m`, opened before leg r)

0. **Gate.** The CTO half signed. `-Plan -Commit <p>` names Python311 (live-task).
1. **(r)** `schedule_induction.ps1 -Register -Commit <p>`, then `-Status`: Start In = the `<p>` pinned workdir. Runs before
   2026-10-08 13:00Z; no fire falls between (r) and that fire.
2. **(v)** Read the 2026-10-08 13:00Z fire's log: `already_current 0 pulled 96`, `bloomberg_calls 768`, rc 0. Then, for BA US:
   the newest raw forecast object carries the four fields on each of the three overrides, and the newest derived block carries a
   figure for each of the four at FY1, FY2 and FY3 whose `fiscal_period` and `period_end_date` equal those of `BEST_CPS` and
   `BEST_EPS` in the same block (the CTO's period term, on the stored block). Then `checks/round38/count_ratio_currency.py
   --served`: `crc served build 1/1 control 1/1` (the two `_NUMEST` are counts and must add no currency).

## EXPECTED OUTCOME (every branch)

- **Writers:** the forecast field list has 1 rule (`FORECAST_FIELDS` at `<p>`); a served block has 1 writer (`stage_derive`);
  the task's Start In has 1 writer (`schedule_induction.ps1`).
- **Branch A:** the fire pulls 96 at 768 calls, rc 0; BA's block carries the four at three periods, period-equal to their means.
  The derived UNIT of the four reads the pointer `SEE field_map.json (per-field, per-security MEASURED unit -- not yet built)`,
  because `field_map.json` holds no entry for them at `<p>`. That is expected and is NOT the end state: see "not covered".
- **Branch B (one or more names fail to pull or derive, rc 1):** each failure is listed; a failed name keeps its prior block.
- **Branch C (the Terminal is unreachable, rc 4):** nothing is pulled and nothing served moves. Not the pin's failure. The next
  scheduled fire is the read. No ad-hoc fire without a CTO ruling.
- **Branch D (the plan names a non-Python311 interpreter, or `-Register` refuses):** STOP. The task stays on `662cd2b11d`.
- **Branch E (a field error on one of the four for some names):** the name's block carries an unresolved record with the reason
  for that field and period; every other figure of the block is as on any day. Counted per field in the read.
- **Branch F (the period of a statistic differs from its mean's on the stored BA block):** it comes back to the CTO the same
  hour and the task is re-pinned to `662cd2b11d` before the next fire.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| Scheduled Task `amgt-induction-daily` | Start In (pin `<p>`); interpreter and trigger unchanged | `-Register -Commit 662cd2b11d` |
| the 2026-10-08 13:00Z fire | the scheduled daily pull of the 96 (the planned population): up to 96 raw/bronze and 96 derived write-once keys, each derived block gaining up to 12 figures (4 fields x 3 periods) | the task's own next fire on the old pin supersedes; exact restore by delete needs Andrew's word |
| Bloomberg | the same 768 requests; each forecast request names 4 more fields | the old pin |

Never touched: any Seeking Alpha call (refresh runs `sa_fallback=False`), any ad-hoc Bloomberg pull, `field_map.json`, the
crosswalk pool, any dossier, any portal file, any other firm.

## NOT COVERED BY THIS HALF

- **The unit of the four fields.** `field_map.json` is built from pulled samples (`build_unit_map.py`; round 35's leg m is the
  precedent). After the first fire has pulled the four, a scoped map build, a commit, a second re-pin and a re-derive give them
  their measured unit. That is its own pair, written on the read of leg v.
- **Readers of the block other than the Model sheet.** The print pack and the export were not exercised with the four fields
  present. `lib/research/scores/divergence.py` is renamed by AMGT_RESAPP bb-22 @`3161dbc59a`; `run_scores` is not re-run by
  that round (2.0.0_SA_COO~Z msg 31117), so no score moves on this act.
- The four RESAPP/HARVST files in the closure, beyond naming them.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-07 ~16:3xZ, for legs 0, r and v, covering branches A to F.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
