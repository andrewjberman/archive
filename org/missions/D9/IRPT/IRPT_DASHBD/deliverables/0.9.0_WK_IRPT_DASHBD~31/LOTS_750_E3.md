# LOTS_750_E3 -- TO-DB-b-52 (counts only)

Record: `LOTS_750_E3.json`. Day 2026-10-06; population 7,604 accounts, all 7,604 run; the extended reporting-gold handler's own
`--local` mode, one process per run, round 28's runner imported by `lots_750_run.py` (not restated). No S3 write, no Lambda invoke,
no limit changed. Handler bytes unchanged; the producer's one change is `DEFAULT_BATCH_SIZE = 1000` to `2000`.

| order | batch size | lots s | lots peak MB | total s | total peak MB | total <= 750 s |
|---|---|---|---|---|---|---|
| 1 | 2,000 | 514.04 | 1,663.9 | 757.55 | 1,663.9 | no |
| 2 | 4,000 | 573.84 | 1,827.5 | 813.18 | 1,827.5 | no |
| 3 | 0 (one batch) | no record | 2,733.1 (last progress line) | no record | -- | no |
| 4 | 3,000 | 485.91 | 1,665.5 | 707.34 | 1,665.5 | yes |
| 5 | 1,500 | 408.25 | 1,764.4 | 627.25 | 1,764.4 | yes |
| 6 | 2,000 | 456.00 | 1,477.3 | 692.81 | 1,525.8 | yes |

- Run 3 (one batch): the process ended about 900 s into the lots stage with no DONE line and no record, before the runner's
  3,600 s cap; its last progress line read 2,733.1 MB at 900.4 s. Over the 2,048 MB limit and past 900 s either way.
- Chosen: 2,000 (run 6; the lowest lots peak among the runs at or under 750 s: 3 runs qualify, 1,477.3 MB against 1,665.5 and 1,764.4).
  The same size gave 757.55 s at run 1 and 692.81 s at run 6: run to run spread at one size is 64.7 s on this box under other workers.
- Default run (no batch-size argument; the log shows 4 batches of up to 2,000): lots 442.04 s / 1,526.3 MB, total 666.98 s / 1,553.4 MB,
  lots stage completed.
- Limits: target 750 s, timeout 900 s, memory 2,048 MB. Every completed run's peak is under 2,048 MB.
- Machine: 16 cores, 63.7 GB RAM, 12 handler workers, 1 run at a time by this worker, 2 other workers running light analyses on the
  same machine, pandas 3.0.6 (the served runtime is 2.2.3), Python 3.14.7.
- Tests: `test_account_activity_lots.py` 45 passed.
- Rows: IRPT_DASHBD-W31-S1 (run 3 ended without a record), IRPT_DASHBD-W31-S2 (same size, two totals either side of 750 s).
