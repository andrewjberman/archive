# MDAILY_RUNNER_SLICE_READ -- HG-t-13 (row MDPF_HEALGAP-S1)

Read-only. No AWS write, no Lambda invoke, no SSM send, no instance touched. No timer or background task armed.

DENOMINATOR: 6 dispatch entries read
VERDICT: RUNS-SLICE
NOOP: UNKNOWN because the slice body carries a today-dependent field and no served-bytes comparison against a same-day rebuild was read; the key is the same single object on every run
GROUNDING: infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:125, infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:538, infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:547, infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:554, infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:556, data/assets/scripts/gold/build_cottonwood_mdpf_slice.py:141, data/assets/scripts/gold/build_cottonwood_mdpf_slice.py:1353, data/assets/scripts/gold/build_cottonwood_mdpf_slice.py:1501, data/assets/scripts/gold/build_dim_model_portfolio.py:538

## What was read

The 6 dispatch entries read: the staging sync at `mdpf-daily-dispatch.sh:125` and `:130`, and the four 6d COTTONWOOD invocations at `:554` (dim), `:555` (pair), `:556` (slice) and `:562` (global re-stage).

1. **Staging.** `:125` runs `aws s3 sync s3://opal-data-mdpf/code/scripts/ /opt/mdpf/scripts/ --delete`. The sync is recursive, so `code/scripts/assets_gold/` lands at `/opt/mdpf/scripts/assets_gold`, which is the default `COTTONWOOD_GOLD_DIR` at `:538`.
2. **Presence in the staged set.** `head-object` on `opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_slice.py` returned 88273 bytes, ETag `2d9b120affde04e98a42271d6740deb6`, LastModified `2026-10-09T17:53:07Z`. `md5sum` of `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` is `2d9b120affde04e98a42271d6740deb6`. The file is present in the set the runner pulls, and its bytes match the repo file.
3. **Condition.** `:547` runs the 6d block only when `build_cottonwood_mdpf_slice.py` exists under `COTTONWOOD_GOLD_DIR`. When it is absent, `:568-569` fail the stage. The dispatch has no separate catch-up step. The block is reached only if stages 6a-6c return 0 (`:504`, `:516`, `:520`, `:524` each `|| return 1`).
4. **What the slice writes.** The slice reads gold dim partitions and holdings with `get_object` (`build_cottonwood_mdpf_slice.py:422`, `:597`). It writes exactly one object: `SLICE_KEY = REVAMP_PREFIX + "cottonwood/aggregate_aua_timeseries.json"` in bucket `opal-data-assets` (`:141`, `:1501`). The `put_object` is unconditional, with no skip-if-exists check. The slice writes no gold partition. The body's `meta.source_vintage.trading_days_behind_settled_frontier` is computed from `dt.date.today()` (`:1353-1366`).
5. **The step before it does write a gold partition.** `:554` runs `build_dim_model_portfolio.py --date <cot_date> --upload`, where `cot_date` is the newest silver `fact_model_assignment` partition (`:549-552`). The builder writes `blackdiamond/cottonwood/gold/dim_model_portfolio/date=<cot_date>/data.parquet` (`build_dim_model_portfolio.py:538`, put at `:542`). The pair at `:555` stages `gold/mdpf_revamp/cottonwood/*` artifacts, which are not gold partitions.
6. **Served state, read 2026-10-11T04:0xZ.** `opal-data-assets` slice key: LastModified `2026-10-10T13:31:08Z`, ETag `50425224d45dc36f6588544bb0525d4d`, 162895 bytes, so no later write is recorded for 10-10. Newest gold dim partitions: `date=2026-10-08` at 13:30:40Z, `date=2026-10-09` at 13:30:41Z, `date=2026-10-10` at 13:30:39Z.

## Answer and its limits

- The EC2 path runs the slice later in the day with no catch-up step, when the staged-file condition holds. That condition holds, so VERDICT is RUNS-SLICE.
- Inference, not measured: the 10-10 gold partition write at 13:30:39Z is about five seconds after the minute the row records for the EC2 launch. Stages 6a-6c run for minutes before the slice, so the 13:31:08Z slice write is not the EC2 path's. The Lambda is the likely writer of both.
- NOOP is UNKNOWN. The keys are fixed, one object per run, so the key level is a no-op. The bytes are not: the body carries a date-derived field, and no served object was diffed against a rebuild. The read that would answer it is a GET of the served slice key, compared with a same-inputs DRY-RUN build with the date pinned, or the ETag of the served object across two consecutive days.
- The schedule that starts the instance is not read (row MDPF_HEALGAP-S1 notes), and no EC2 describe was made. Whether the instance ran on 2026-10-10 is UNREAD.
- The dim step at `:554` rewrites one cottonwood gold partition on the EC2 path. This is filed as a row, not fixed here.

Rows filed: MDPF_HEALGAP-D1-W10-S1 and MDPF_HEALGAP-D1-W10-S2 in `org/missions/D8/MDPF/MDPF_HEALGAP/surprise-channel/investigations/INVESTIGATION_v1.md`. The D1 coordinate follows the order and the sibling W6 precedent: the row gate requires it on dell1.
