# NFRA_FIDUPL.TO-FV-s-3 -- Historical backfill walk, run 2 (stop: error)

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Later-run caps per msg 9135; run 2 not before 16:35Z per msg 9122. Runs ledger nfra-fidupl-histwalk-runs-20261021 open before the run. Started only after `date -u` read 16:35:39Z with no unread message and no other automation in progress. No cookie or profile directory was touched.

run 2: SSM cfc2dcbc-315f-432b-8956-c61923bf4503 on i-028e830f7226cc685, START 16:35:42Z, Success (transport) at about 16:54Z, hist_walk.py exit=1
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/hist_walk.py --config /opt/fidelity-uploader/config.json --max-days 60 --max-seconds 2400 (SSM executionTimeout 3000)
sign-in count: ONE sign-in in this run (SIGNIN ok secs=35, CLOSE ok secs=17). Trailing hour at 16:35Z: run 1 at 15:50Z (mine) and the issuer's session at 16:21Z, so run 2 was the third, at the cap. At most 2 of my runs started in that rolling hour. No 401, 403 or lockout line.

## stdout, verbatim (293 lines)

```
SIGNIN ok secs=35
REQ POST status.json status=200 secs=1
REQ GET profileList.json status=200 secs=0
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29921695 secs=5
FILE position bytes=29921695
FILE unknown status=200 bytes=651765 secs=1
FILE prices bytes=651765
FILE unknown status=200 bytes=12278164 secs=3
FILE psn bytes=12278164
DAY 2026-09-23 position=LANDED prices=LANDED psn=LANDED secs=103
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29905682 secs=11
FILE position bytes=29905682
FILE unknown status=200 bytes=650813 secs=0
FILE prices bytes=650813
FILE unknown status=200 bytes=12273946 secs=2
FILE psn bytes=12273946
DAY 2026-09-22 position=LANDED prices=LANDED psn=LANDED secs=59
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=12266222 secs=2
FILE psn bytes=12266222
DAY 2026-09-21 position=SKIPPED prices=SKIPPED psn=LANDED secs=18
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29910287 secs=10
FILE position bytes=29910287
FILE unknown status=200 bytes=654509 secs=0
FILE prices bytes=654509
FILE unknown status=200 bytes=12275758 secs=2
FILE psn bytes=12275758
DAY 2026-09-18 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29844403 secs=12
FILE position bytes=29844403
FILE unknown status=200 bytes=654554 secs=0
FILE prices bytes=654554
FILE unknown status=200 bytes=12249484 secs=2
FILE psn bytes=12249484
DAY 2026-09-17 position=LANDED prices=LANDED psn=LANDED secs=59
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29880740 secs=9
FILE position bytes=29880740
FILE unknown status=200 bytes=657136 secs=0
FILE prices bytes=657136
FILE unknown status=200 bytes=12263388 secs=2
FILE psn bytes=12263388
DAY 2026-09-16 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29693850 secs=5
FILE position bytes=29693850
FILE unknown status=200 bytes=647814 secs=0
FILE prices bytes=647814
FILE unknown status=200 bytes=12195864 secs=1
FILE psn bytes=12195864
DAY 2026-09-15 position=LANDED prices=LANDED psn=LANDED secs=52
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29670050 secs=11
FILE position bytes=29670050
FILE unknown status=200 bytes=647698 secs=1
FILE prices bytes=647698
FILE unknown status=200 bytes=12186424 secs=3
FILE psn bytes=12186424
DAY 2026-09-14 position=LANDED prices=LANDED psn=LANDED secs=61
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29679952 secs=5
FILE position bytes=29679952
FILE unknown status=200 bytes=643173 secs=0
FILE prices bytes=643173
FILE unknown status=200 bytes=12189578 secs=1
FILE psn bytes=12189578
DAY 2026-09-11 position=LANDED prices=LANDED psn=LANDED secs=50
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29670135 secs=4
FILE position bytes=29670135
FILE unknown status=200 bytes=643239 secs=0
FILE prices bytes=643239
FILE unknown status=200 bytes=12186856 secs=1
FILE psn bytes=12186856
DAY 2026-09-10 position=LANDED prices=LANDED psn=LANDED secs=51
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29491244 secs=5
FILE position bytes=29491244
FILE unknown status=200 bytes=637391 secs=0
FILE prices bytes=637391
FILE unknown status=200 bytes=12123812 secs=1
FILE psn bytes=12123812
DAY 2026-09-09 position=LANDED prices=LANDED psn=LANDED secs=51
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29478097 secs=11
FILE position bytes=29478097
FILE unknown status=200 bytes=634808 secs=1
FILE prices bytes=634808
FILE unknown status=200 bytes=12121244 secs=3
FILE psn bytes=12121244
DAY 2026-09-08 position=LANDED prices=LANDED psn=LANDED secs=62
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29506399 secs=11
FILE position bytes=29506399
FILE unknown status=200 bytes=634937 secs=0
FILE prices bytes=634937
FILE unknown status=200 bytes=12138254 secs=2
FILE psn bytes=12138254
DAY 2026-09-04 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29493655 secs=11
FILE position bytes=29493655
FILE unknown status=200 bytes=634176 secs=0
FILE prices bytes=634176
FILE unknown status=200 bytes=12130190 secs=3
FILE psn bytes=12130190
DAY 2026-09-03 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=0
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29446945 secs=9
FILE position bytes=29446945
FILE unknown status=200 bytes=626641 secs=0
FILE prices bytes=626641
FILE unknown status=200 bytes=12111186 secs=2
FILE psn bytes=12111186
DAY 2026-09-02 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29400371 secs=5
FILE position bytes=29400371
FILE unknown status=200 bytes=627234 secs=0
FILE prices bytes=627234
FILE unknown status=200 bytes=12098624 secs=1
FILE psn bytes=12098624
DAY 2026-09-01 position=LANDED prices=LANDED psn=LANDED secs=53
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29401291 secs=5
FILE position bytes=29401291
FILE unknown status=200 bytes=629857 secs=0
FILE prices bytes=629857
FILE unknown status=200 bytes=12100752 secs=1
FILE psn bytes=12100752
DAY 2026-08-31 position=LANDED prices=LANDED psn=LANDED secs=52
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29341245 secs=3
FILE position bytes=29341245
FILE unknown status=200 bytes=630287 secs=0
FILE prices bytes=630287
FILE unknown status=200 bytes=12067138 secs=1
FILE psn bytes=12067138
DAY 2026-08-28 position=LANDED prices=LANDED psn=LANDED secs=49
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29276387 secs=5
FILE position bytes=29276387
FILE unknown status=200 bytes=629436 secs=0
FILE prices bytes=629436
FILE unknown status=200 bytes=12040888 secs=1
FILE psn bytes=12040888
DAY 2026-08-27 position=LANDED prices=LANDED psn=LANDED secs=52
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=504 secs=8
ERROR: histwalk did not finish: WalkError
CLOSE ok secs=17
ERROR: histwalk run_id=20261021T163541Z sign_ins=1 stop=error
exit=1
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

## The walk record (s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/histwalk-20261021T163541Z.json, 4245 bytes)

```
keys: ['caps', 'days', 'finished_at', 'histwalk', 'partial', 'per_type', 'run_error', 'run_id', 'scope', 'sign_ins', 'started_at', 'stop']
histwalk = true
sign_ins = 1
run_error = "WalkError"
stop = {"evidence": "WalkError on 2026-08-27", "reason": "error"}
run_id = "20261021T163541Z"
started_at = "2026-10-21T16:35:41Z"
finished_at = "2026-10-21T16:54:15Z"
caps = {"max_days": 60, "max_seconds": 2400}
partial = false
per_type = {"position": {"bytes_landed": 533012428, "earliest_landed": "20260827", "empty_days": 0, "landed_days": 18, "skipped_days": 1, "stop_reason": null, "stopped": false}, "prices": {"bytes_landed": 11535468, "earliest_landed": "20260827", "empty_days": 0, "landed_days": 18, "skipped_days": 1, "stop_reason": null, "stopped": false}, "psn": {"bytes_landed": 231297772, "earliest_landed": "20260827", "empty_days": 0, "landed_days": 19, "skipped_days": 0, "stop_reason": null, "stopped": false}}
days: 19
last 3 days: [{"date": "2026-08-31", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 52}, {"date": "2026-08-28", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 49}, {"date": "2026-08-27", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 52}]
```

## What the output shows (read from the output only)

- Days walked in run 2: 19 trading days, 2026-09-23 back to 2026-08-27, 18 to 103 s per day. 2026-09-21: position and prices SKIPPED, psn LANDED; every other day position, prices and psn LANDED.
- The stop: after day 2026-08-27 was fully landed, the next day's sequence ended with `REQ POST status.json status=504 secs=8`, then `ERROR: histwalk did not finish: WalkError`, `CLOSE ok secs=17` and `stop=error`. The record reads stop {reason "error", evidence "WalkError on 2026-08-27"}.
- No type has stopped: stop_reason null and empty_days 0 for position, prices and psn.
- Run 2 totals: position 18 days landed, 533012428 bytes; prices 18 days, 11535468 bytes; psn 19 days, 231297772 bytes; earliest landed 20260827 for each.
- Per the order an `error` stop is not retried and the chaining stops. The state file /opt/fidelity-uploader/work/histwalk_state.json was last written 16:54Z (442 bytes) so a resume would continue below 2026-08-27.

## What S3 shows (read-only, 16:56Z): keys written since 15:50Z excluding `_runs/`, both runs, 101 in all

| type (S3 prefix) | keys | earliest landed content date | latest landed | bytes |
|---|---|---|---|---|
| position | 33 | 20260827 | 20261014 | 985939074 |
| position_balance_fl | 35 | 20260827 | 20261015 | 429524198 |
| prices | 33 | 20260827 | 20261014 | 21239906 |

Walk records: histwalk-20261021T155032Z.json (run 1, stop budget) and histwalk-20261021T163541Z.json (run 2, stop error).
