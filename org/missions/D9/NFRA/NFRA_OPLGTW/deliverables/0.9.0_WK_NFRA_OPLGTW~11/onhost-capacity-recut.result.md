# OG-r-3 result -- on-host capacity re-cut (0.9.0_WK_NFRA_OPLGTW~11)

Served release under test: `4248b70b39` (host md5 of `schwab/{engine,integration,export}.py` = `b06a27f7...`, `f436630c...`,
`c9943e78...` = that commit's bytes, 3 of 3; `EC2_MANIFEST.json` `deployed_commit` 4248b70b3911...). Host `i-07dccb1615503ac99`
(t4g.small class, 1,846 MB, service unrestarted since 2026-09-29 05:22:10Z before, between and after every run).
Run: `onhost_bench.py --scale full`, SSM `e32bd390-4b24-4e5f-9e4d-49824f691a05`, 2026-09-29T06:47:12Z..06:47:34Z (22.3 s), in
process under `/opt/opal-gateway/.venv`, synthetic data only, no state-store call (the export arm's store, catalog, fetch and
audit sink are in-memory doubles, so no `RUNTIME#bench-og-r3-*` key was written). Host scratch removed; nothing deployed.
Verdict in CAPACITY.json: **INSUFFICIENT**. A measured result, not a failure to repair.

## Changes made to the harness (commit 1efe069571, then a one-line path fix)
1. `_cap_respected` reads `peak_child_rss_bytes` on every path (an unread RSS is not respected).
2. The export arm calls the served `SchwabService.export_query` through `export.generate_csv` at 11 columns; the old
   `run_export(...)` call and its `csv`-bytes read are removed (row Z-W11-S2).
3. AC4 windows are read by `probes/assemble_capacity.py` (CloudWatch, both ruled windows).

## `cap_respected` consumer census (printed by `test_ogr3_ac01`, denominator = lines scanned)
`onhost_bench.py` (705 lines): the definition at :206; ONE call site of `_cap_respected(` (:569, the single function that
grades every job); reads of the `cap_respected` / `all_cap_respected` verdict at :578, :650, :655, :663 (4). Round 1 read it
at 6 places. `og_r3.py`: re-derives the grade from each recorded peak and only compares the recorded flag with it (a
disagreement is itself a failure); mutant B (flag forced True on the maximal job) is caught: `[flag disagrees]`.

## Peaks (host, 11 columns = dim_position, the widest exportable set by contract column count)
| job | rows x columns | outcome | peak child RSS (bytes) | vs cap 268,435,456 |
|---|---|---|---|---|
| maximal query | 12 objects | LIMIT_EXCEEDED | 286,691,328 | OVER by 18,255,872 |
| concurrent A / B | 8,000 rows x 12 objects | ok / ok | 205,750,272 / 205,463,552 | under |
| export FULL | 250,000 x 11 | LIMIT_EXCEEDED memory, 1.4 s | 272,683,008 | OVER by 4,247,552 |
| export TENTH | 25,000 x 11 | ok, csv 3,748,900 B, 2.9 s | 171,974,656 | under |
| export probe | 125,000 x 11 | ok, csv 18,743,499 B, 8.1 s | 225,271,808 | under |

**Export peak ratio full / tenth = 1.5856** (the full run was killed at the cap, so its true peak is higher). A second full
run, same host, read maximal 286,830,592; full 275,021,824; tenth 170,377,216; probe 225,247,232; ratio 1.6142. Files gone
after every export run (export dir empty, no engine job dir left). CSV size is not the constraint: about 150 bytes a row.

## The two admission reserves (both inputs printed; admission code unchanged)
- From the formula: `ceil(193,228,800 x 1.25) + 134,217,728 = 375,753,728`; input = the engine's OG-p-1 floor 193,228,800 (the
  live gateway's measured VmHWM was 101,580,800 after the 05:22Z restart, below the floor); required for 2 jobs 912,624,640.
- Priced against the measured child peak: max peak 286,691,328 (overshoot 18,255,872 over the cap); reserve
  `375,753,728 + 2 x 18,255,872 = 412,265,472`; required for 2 jobs `375,753,728 + 2 x 286,691,328 = 949,136,384`.
- **Gap 36,511,744 bytes** -> finding row `NFRA_OPLGTW-Z-W11-S11`. Host memory 1,936,322,560 admits both.
(My reading of "re-derived from the measured peak child RSS": the overshoot the engine's own poll allows is added to the
reserve. If the issuer meant another derivation the raw inputs are in CAPACITY.json `admission`.)

## AC4 windows (CloudWatch, period 86400, LB `app/opal-gateway/89166a68f337e5a4`, TG `targetgroup/opal-gateway-tg/00997fc81f087cb8`)
- BASELINE 2026-09-11T00:00Z..2026-09-18T00:00Z: 7 day-buckets, `HTTPCode_Target_5XX_Count` 0 in every bucket, `RequestCount`
  3,323 / 1,123 / 1,142 / 4,309 / 2,778 / 5,017 / 1,781 = **19,473** (window sample count 19,473); window p95 0.4960 s vs
  OGP1-AC11 0.5535024102704742 s = **-10.4 %** (cap +20 %). Zero failures with a denominator of 19,473 requests.
- POST-RELEASE (Q5) 2026-09-21T00:00Z..2026-09-28T00:00Z: 7 day-buckets, 5XX 0 in every bucket, `RequestCount` 1,385 / 1,285 /
  1,676 / 3,469 / 1,517 / 1,314 / 1,320 = **11,966** (sample count 11,824); window p95 0.5950 s = +7.5 % vs the same reference
  (printed, supporting). Zero failures with a denominator of 11,966.
(The AWS CLI renders datapoint timestamps in local time, `2026-09-10T20:00:00-04:00` for the 09-11 UTC bucket; the assembler
converts to UTC. A first assembly that sliced the string shifted every bucket by a day and read a false empty seventh bucket.)
- ALB `idle_timeout` 60 s (> the 30 s prep deadline), read `2026-09-29T06:46:20Z`, ARN
  `arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4`, 52 s before the run.

## Criteria (run as written from the worktree root; details in the proof instance)
AC1 PASS (test_ogr3_ac01); AC2 **FAIL** (maximal and the 250,000-row export exceed the cap); AC3 **FAIL** (the 250,000-row export
does not complete: LIMIT_EXCEEDED/memory); AC4 PASS; AC5 PASS; AC6 PASS (verdict INSUFFICIENT with its
`for_prd_revision_if_insufficient` block). Two mechanical FAILs are measured results; the order stays `pending`.

## Rows
`NFRA_OPLGTW-Z-W11-S10` (contract-scale wide export INSUFFICIENT, ARMED), `NFRA_OPLGTW-Z-W11-S11` (admission gap 36,511,744 bytes,
ARMED). Rows S1 (Z-W11-S1) and S2 (Z-W11-S2) are disarmed by this cell: S2 by removing the old leg, S1 by measuring width at 11
columns with the column count beside every peak.

## Not measured
`dim_asset` (9 columns but three free-text description columns) was not exported; the widest set was chosen by column count as
the amendment states. The parent process's own memory was not part of this run's grade.
