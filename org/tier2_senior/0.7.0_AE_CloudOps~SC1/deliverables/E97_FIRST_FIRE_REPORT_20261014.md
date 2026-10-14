# TO-SC-e97b -- first BD fire that ran C_06 after the ship: cost, chain launch-to-stop, rolling re-derive line (0.7.0_AE_CloudOps~SC1, 2026-10-14 ~01:30Z)

Written for a reader with zero prior context. The order asks this seat, after the first BD fire that RUNS C_06
following the ship, for C_06's wall time, the chain's launch-to-stop and the `C06-ROLLING-REDERIVE` line. Leg G
(per-date totals against the AUA, the bars, the advisor table, `restated_through`, the second fire's
idempotence) is the issuer's and is NOT graded here. Every figure below is measured; none is graded.

Which fire: the 23:00:11Z launch on 2026-10-13. The two launches between the ship and this one (09:46:59Z and
12:45:16Z) ran S_00, A_00 and A_02 only and wrote no C_06 telemetry.

## 1. Cost (order step 5: chain more than 30 minutes over the pre-ship chain)

| | 04:00:46Z fire (pre-ship) | 23:00:11Z fire 2026-10-12 (first SC-e-91 fire) | 23:00:11Z fire 2026-10-13 (first e97b fire) |
|---|---|---|---|
| C_06 wall time | 15.5 s (telemetry) | 186.0 s (`[PERF]`) | 353.1 s (`[PERF]`); telemetry run_id 0a679247d7d9 reads 351.2 s |
| C_06 peak memory, PSS | 6,767 MB | 6,349 MB | 6,491 MB |
| C_06 peak memory, RSS | 6,814 MB | 6,396 MB | **11,582 MB (log) / 11,595 MB (telemetry)** |
| chain launch-to-stop | at least 7,766.7 s | 7,915 s | **8,065 s** (launch 23:00:11Z, `PARALLEL CHAIN COMPLETE` 2026-10-14T01:14:36Z) |
| difference to this fire | -298 s | -150 s | |

Against a STOP threshold of +1,800 s the chain is +298 s over the 04:00:46Z fire and +150 s over SC-e-91's first
fire. **The cost arm of the STOP rule did not fire.** The runner read `stopped` at 01:25:23Z. The exact EC2 stop
second was not measured (the instance reports `Client.InstanceInitiatedShutdown` with no timestamp), so the chain
figure is launch to the chain's own completion line, as in the SC-e-91 report.

One number this seat reports and does not judge: C_06's RSS peak rose from about 6.4 GB to about 11.6 GB. The
runner is an `r6i.4xlarge` (128 GiB); the telemetry's highest system memory used was 12,600 MB (9.9 percent),
against 12,480 MB (9.8 percent) in the previous fire. PSS, the order's basis, moved 6,349 to 6,491 MB.

## 2. The C06 lines of this fire's log

```
C06-ROLLING-REDERIVE window=2026-09-25..2026-10-09 dates=15 relationships_read=3793 relationships_rewritten=3274 keys_written=13096
C06-RETAINED-ONLY relationships_read=3793 of 3793 relationships_rewritten=0 holdings_moved=0 firm_days_adjusted=0 advisor_days_adjusted=0
```

- `C06-ROLLING-RULE-UNREADABLE`: **0 lines**, so the sibling `gold_dispatch.sh` WAS readable beside C_06 on the
  runner and the build was not the fail-closed no-op. The order's BLIND item (whether the runner has the file
  beside C_06) reads: present.
- The re-derive wrote 3,274 of 3,793 relationships, 13,096 keys, equal to the dry run's 3,274 and 13,096 that the
  COO half records. The SC-e-91 retained pass that follows it on the same fire moved 0 holdings.
- The log file read is `gold_incremental_2026-10-14_20261014_012024.log`, the tail 4 MB; `gold_incremental_*`
  logs are cumulative, so the lines above were taken by their own text, not by a `(Ns)` duration line.

## 3. What this seat does NOT do

It does not read the totals, the bars or the advisors against their conditions and it restores nothing. Those
reads are the issuer's leg G, and the STOP rule's other arms (a window day's firm total more than $1.00 from the
AUA, an advisor key dropped) are the issuer's to call. The data-side rollback handles are in
`E97_PREFIRE_VERSIONS_20261012.json` (30,329 keys, each with its destination bucket) and the before bodies beside
it. Code rollback, unused: C_06 to `zjQmOYVVYTSGOWLFQ0P33vVeWkwp4_eT`, D_04 to `ap.CyBT8aJijz5kWFsSNjEFU99itbXED`.

The second fire's idempotence read (0 relationship keys rewritten) is the issuer's after the next fire that runs
C_06: 04:00Z today.
