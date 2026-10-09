# LOTS_P95_E3 -- full run p95 at the producer default (counts only)

- day 2026-10-06; population 7604 accounts; default batch size 1000 (runs pass no --batch-size)
- runs at the default: 5; p95 of total wall seconds (linear interpolation): 652.38; bar 750

| run | batch | lots stage completed | lots s | lots MB | total s | total MB |
|---|---|---|---|---|---|---|
| 1 | 2000 | True | 560.91 | 1626.5 | 824.3 | 1626.5 |
| 2 | 2000 | True | 569.4 | 1643.5 | 835.42 | 1643.5 |
| 3 | 1500 | True | 455.26 | 1496.5 | 672.24 | 1500.2 |
| 4 | 1500 | True | 435.58 | 1629.5 | 655.47 | 1629.5 |
| 5 | 1500 | True | 647.22 | 1479.6 | 955.01 | 1489.1 |
| 6 | 1500 | True | 633.17 | 1535.6 | 905.77 | 1535.6 |
| 7 | 1500 | True | 508.44 | 1638.9 | 782.71 | 1638.9 |
| 8 | 1000 | True | 406.04 | 1763.4 | 625.42 | 1763.4 |
| 9 | 1000 | True | 378.43 | 1657.3 | 607.93 | 1657.3 |
| 10 | 1000 | True | 403.18 | 1722.2 | 608.27 | 1722.2 |
| 11 | 1000 | True | 449.01 | 1511.7 | 659.12 | 1511.7 |
| 12 | 1000 | True | 398.09 | 1518.9 | 621.07 | 1518.9 |

- interrupted by the reaper, not timings: 2 runs (at 360 s and 630 s into the lots stage)
- machine: 16 cores, 63.7 GB, 12 handler workers; one other worker ran a light S3 analysis concurrently.
