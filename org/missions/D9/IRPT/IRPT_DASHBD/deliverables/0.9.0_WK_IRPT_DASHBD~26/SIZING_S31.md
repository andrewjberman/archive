# SIZING_S31 -- IRPT_DASHBD.TO-DB-b-46 (counts only)

The extended reporting-gold handler, `handler.py --local` mode, one trading day (2026-10-06), over the handler's own population, in one
process, against `900 s` / `2048 MB`. S3 reads only; nothing written to S3; the handler and the producer are HEAD's bytes, unchanged
(sha256 values in `SIZING_S31.json`). Driver: `sizing_s31.py`. Record: `SIZING_S31.json`. Machine: 8 physical cores, 16 logical, 63.7 GB.

## A. The run

| Quantity | Count |
|---|---|
| population (the handler's `population_accounts`, holdings gold 2026-10-06) | 7,597 |
| account set the run took (`account_set`: population united with the newest reporting partition) | 7,597 |
| wall cap | 3,600 s; not reached (`stopped_at_cap` false) |
| `account_return_daily` rows / `account_class_daily` rows written | 6,888 / 25,013 |
| lots stage | REFUSED (`LOTS_SKIPPED`): the three lots tables were not produced |

## B. Wall time and peak working set per stage

| Stage | Wall (s) | Peak working set (MB) | Over 900 s / 2048 MB |
|---|---|---|---|
| returns | 122.57 | 257.8 | no / no |
| class | 92.69 | 295.6 | no / no |
| lots (to the refusal) | 244.65 | 2,759.5 | no / yes, by 711.5 MB |
| other (population read, returns parquet write) | 1.16 | -- | -- |
| total | 461.06 | 2,759.5 | no (439 s under) / yes, by 711.5 MB |

Peak method: the largest working set sampled every 0.25 s while a stage ran, raised to the process's own `peak_wset` when that counter
rose in the stage (the lots figure is that exact counter). The total peak is the process `peak_wset`.

Lots stage, by step (seconds): `first_data_dates` 118.33, `unrealized_rows` 108.89, `read_window` 15.24, `classify_flow_days` 1.37,
`realized_rows` 0.01 (the step that refused). Mean over the stage: 0.0322 s per account (244.65 s over 7,597), a batch mean.

## C. The refusal and the per-account tail

The lots stage read all 7,597 accounts and built the unrealized rows, then `realized_rows` refused: a realized lot id appears twice in one
frame. `REALIZED_ID_REPEAT_COUNTS.json` (read from the 2026-10-06 realized-lot partition, no ids written):

| Quantity | Count |
|---|---|
| rows in the partition (all in the account set) | 2,523 |
| distinct lot ids | 2,435 |
| lot ids that repeat | 87 |
| rows in repeated ids | 175 (one id appears three times, 86 twice) |
| accounts holding a repeated id | 36 |
| repeated ids spanning more than one account | 0 |
| rows equal to another row in every column | 0 |

The stage never reached the per-account activity loop, the in-kind step or the writes. `per_account_seconds` p50, p95, p99 and max are
null (0 samples): the stage's reads and classification are batched over all accounts. No figure is extrapolated; the stage's complete wall
time and peak are unmeasured, and the 2,759.5 MB is a floor on the lots peak.

## D. Verdict

BREACH. Memory: 2,759.5 MB against 2,048 MB, 711.5 MB (34.7 percent) over, reached before the stage finished. Timeout: not breached up to
the refusal (461.06 s of 900 s). Rows `IRPT_DASHBD-W26-S1` (the refusal and the memory breach, BLOCKING, ARMED) and `IRPT_DASHBD-W26-S2`
(the null per-account tail). This is a laptop measure (pandas 3.0.6, Windows working set); the served function runs pandas 2.2.3 on Linux.
