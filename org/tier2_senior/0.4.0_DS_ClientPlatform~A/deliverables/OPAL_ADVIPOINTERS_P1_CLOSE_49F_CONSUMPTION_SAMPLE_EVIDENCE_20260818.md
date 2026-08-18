# CONSUMPTION-SAMPLE EVIDENCE -- P1C-3 exercise transcript (trimmed to deciding lines; full raw log was session-scratch)

**Setup:** full mirror of s3://opal-data-assets/portal/gold/advi/49financial/ -> local (aws s3 sync, 4,222 files verified by find-count); asof=2026-08-10 (newest spine partition); emitters invoked from data/assets/scripts/gold/runners_49f/ with local roots; jd2 pulled from s3://opal-data-assets/blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-08-10/.

## Invocations + deciding output (rc + wall-clock per attempt; failure signatures verbatim)
```
== CONSUMPTION SAMPLE asof=2026-08-10 root=/cygdrive/c/Users/ANDREW~1/AppData/Local/Temp/claude/C--Users-AndrewBerman-Desktop-ajb-workspace/7f36b8bf-86fb-49e9-9d89-650b5ac3f7e9/scratchpad/49f_canonical ==
d02 rc=1 wall=0.00s
d03 rc=1 wall=0.00s
d04 rc=1 wall=0.00s
d06 rc=2 wall=0.00s
d07 rc=2 wall=0.98s
d09 rc=2 wall=1.01s
d10 rc=2 wall=1.00s
d12 rc=2 wall=0.94s
d13 rc=2 wall=0.93s
d09 rc=1 wall=0.86s
d10 rc=2 wall=0.81s
d12 rc=2 wall=0.81s
d13 rc=2 wall=0.82s
d07 rc=1 wall=0.84s
d03 rc=1 wall=0.65s
---- distinct failure signatures ----
      2     raise ValueError("No objects to concatenate")
      3 FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\ANDREW~1\\AppData\\Local\\Temp\\claude\\C--Users-AndrewBerman-Desktop-ajb-workspace\\7f36b8bf-86fb-49e9-9d89-650b5ac3f7e9\\scratchpad\\49f_canonical\\dimensions\\dim_relationship\\date=2026-08-10\\data.parquet'
      1 REFUSED: build mode needs --date + --canonical-local + --jd2-dir
      2 ValueError: No objects to concatenate
      1 d06_firm_mix_summary.py: error: the following arguments are required: --a07-root, --a07-date
      1 d07_firm_leaderboard.py: error: the following arguments are required: --jd2-dir
      1 d09_firm_timeseries_overview.py: error: the following arguments are required: --jd2-dir
      2 d10_firm_cumulative_chart.py: error: the following arguments are required: --jd2-dir
      2 d12_firm_timeseries_chart.py: error: the following arguments are required: --jd2-dir
      2 d13_firm_partner_analytics.py: error: the following arguments are required: --jd2-dir
```

**Reading:** every emitter fails LOUDLY on a named absent input, none silently: dim_relationship@asof (d02/d04/d07-class), --a07-root (d06), --jd2-dir (universal: d03/d07/d09/d10/d12/d13), xwalk (d05/d14 REFUSED by argv guard), canonical_positions (d05 read path). The pass rides the first P2 chain cycle + P3C-2 persist acts. jd2 exists on S3 (25 partitions ..2026-08-17) and is an input-resolution fact, not a gap.
