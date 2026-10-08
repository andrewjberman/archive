# BATCHED_E2 -- the lots stage in bounded batches (TO-DB-b-48), counts only

Day 2026-10-06. The handler's own `--local` mode, unchanged but for the batch size it passes, over its own population; one process per run; S3 reads only; no limit changed.

## Change
- Producer: `compute_local_batched` runs the accounts in sorted, disjoint batches of `batch_size` (default 1000), scans the balance history once for all of them, and releases each batch before the next. `compute_local` sorts the realized rows into the one table order (business date, account, lot, quantity), the order the activity and unrealized rows were already in.
- Handler: `lots_days(..., batch_size=None)` and `local(..., batch_size=None)` pass the size through; `--batch-size N` on the CLI. The returns and class stages are untouched.
- Tests: 109 pass (producer 45, handler 64), including a batched-equals-whole test and a handler batch-size test.

## Runs (7,604 accounts, 7,604 run, lots stage completed in 2 of 2)
| batch size | batches | lots s | lots peak MB | total s | total peak MB |
|---|---|---|---|---|---|
| 250 | 31 | 684.61 | 1713.4 | 905.67 | 1713.4 |
| 1000 | 8 | 495.54 | 1735.3 | 768.91 | 1735.3 |

- Lots peak max/min: 1.013 (bound 1.25). Round 27's unbatched lots peak: 2,759.5 MB (refused).
- Against the served limits (900 s, 2,048 MB), for the issuer to grade: batch 250: wall over 900 s True, peak over 2,048 MB False; batch 1000: wall over 900 s False, peak over 2,048 MB False. Measured on pandas 3.0.6, not the served 2.2.3.
- Machine: 8 physical / 16 logical cores, 63.7 GB RAM, 12 workers.

## Identity
- Sample (200 accounts, 36 of them with a repeated realized lot id, 5 batches of 40): sha256 of each table, batched vs unbatched, identical in 3 of 3; rows activity_daily 186, lot_realized 649, lot_unrealized_daily 20886. In-kind legs in the sample: 0.
- Full population, the two batch sizes: table bytes identical in 3 of 3; rows activity_daily 6,888, lot_realized 2,523, lot_unrealized_daily 568,009.
