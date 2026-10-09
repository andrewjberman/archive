# KIT_PEAK_E2 -- lots peak on the pandas 2.2.3 kit (TO-DB-b-67, counts only)

Run: handler --local, day 2026-10-06, producer default batch (1000), one process on dell2.

| Item | Value |
|---|---|
| Runtime (read from the run's own process) | Python 3.12.10, pandas 2.2.3, numpy 1.26.4, pyarrow 14.0.2 |
| Population / accounts run | 7604 / 7604 |
| Lots stage completed | True |
| Batch size | 1000 (8 batches: 7 of 1000, 1 of 604) |
| Lots peak, pandas 2.2.3 (this run) | 1500.7 MB |
| Lots peak, pandas 3.0.6 (round 30, DB-b-55) | 1763.4 MB |
| Limit | 2048 MB |
| Verdict | FITS |
| Lots wall / total wall | 332.25 s / 447.07 s |
| Returns / class stage peak | 302.1 MB / 320.2 MB |
| Kit sha256 | c76af678143a5f92c4a9638a8ac25e47d2f2c294a014cd3a457af96c55ff17bf |

Peak basis: process peak working set (Windows). The measured libraries (pandas, numpy, pyarrow) are the kit's; boto3 and psutil were copied from the box (row IRPT_DASHBD-W44-S1).
