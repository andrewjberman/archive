# NFRA_FIDUPL.TO-FV-s-3 -- Historical backfill walk, run 1

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. Order released by msg 9113; run-1 timing per msg 9122; later-run caps per msg 9135. Runs ledger nfra-fidupl-histwalk-runs-20261021 opened BEFORE the run. Started only after `date -u` read 15:50:31Z with no unread message (no hold). No cookie or profile directory was touched.

run 1: SSM a5ea6d23-f7c0-413a-bf3c-d7ad5ddf8b74 on i-028e830f7226cc685, START 15:50:33Z, Success (transport) at about 16:06Z, hist_walk.py exit=0
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/hist_walk.py --config /opt/fidelity-uploader/config.json --max-days 20 --max-seconds 900 (SSM executionTimeout 1200)
sign-in count: ONE sign-in in this run (SIGNIN ok, CLOSE ok). In the trailing hour at 15:50Z the issuer's sessions were 15:19Z (ok) and 15:30Z (failed at the SMS code step), so run 1 was the third, at the cap. No 401, 403 or lockout line.

## stdout, verbatim (245 lines)

```
SIGNIN ok secs=37
REQ POST status.json status=200 secs=1
REQ GET profileList.json status=200 secs=1
REQ POST status.json status=200 secs=0
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=12410276 secs=2
FILE psn bytes=12410276
DAY 2026-10-15 position=SKIPPED prices=SKIPPED psn=LANDED secs=72
REQ POST status.json status=200 secs=0
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=30302764 secs=3
FILE position bytes=30302764
FILE unknown status=200 bytes=645447 secs=0
FILE prices bytes=645447
FILE unknown status=200 bytes=12409300 secs=0
FILE psn bytes=12409300
DAY 2026-10-14 position=LANDED prices=LANDED psn=LANDED secs=65
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=30302508 secs=11
FILE position bytes=30302508
FILE unknown status=200 bytes=644797 secs=0
FILE prices bytes=644797
FILE unknown status=200 bytes=12411662 secs=2
FILE psn bytes=12411662
DAY 2026-10-13 position=LANDED prices=LANDED psn=LANDED secs=69
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30339339 secs=12
FILE position bytes=30339339
FILE unknown status=200 bytes=646931 secs=0
FILE prices bytes=646931
FILE unknown status=200 bytes=12433984 secs=1
FILE psn bytes=12433984
DAY 2026-10-12 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=30326797 secs=3
FILE position bytes=30326797
FILE unknown status=200 bytes=645483 secs=0
FILE prices bytes=645483
FILE unknown status=200 bytes=12429200 secs=0
FILE psn bytes=12429200
DAY 2026-10-09 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=0
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30595635 secs=11
FILE position bytes=30595635
FILE unknown status=200 bytes=646193 secs=1
FILE prices bytes=646193
FILE unknown status=200 bytes=12549684 secs=3
FILE psn bytes=12549684
DAY 2026-10-08 position=LANDED prices=LANDED psn=LANDED secs=59
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30224639 secs=10
FILE position bytes=30224639
FILE unknown status=200 bytes=646202 secs=0
FILE prices bytes=646202
FILE unknown status=200 bytes=12397120 secs=3
FILE psn bytes=12397120
DAY 2026-10-07 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30223659 secs=11
FILE position bytes=30223659
FILE unknown status=200 bytes=645038 secs=0
FILE prices bytes=645038
FILE unknown status=200 bytes=12398998 secs=2
FILE psn bytes=12398998
DAY 2026-10-06 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=0
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=30313114 secs=2
FILE position bytes=30313114
FILE unknown status=200 bytes=644789 secs=0
FILE prices bytes=644789
FILE unknown status=200 bytes=12450876 secs=0
FILE psn bytes=12450876
DAY 2026-10-05 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30390684 secs=1
FILE position bytes=30390684
FILE unknown status=200 bytes=648439 secs=0
FILE prices bytes=648439
FILE unknown status=200 bytes=12496068 secs=0
FILE psn bytes=12496068
DAY 2026-10-02 position=LANDED prices=LANDED psn=LANDED secs=46
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=0
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30089145 secs=2
FILE position bytes=30089145
FILE unknown status=200 bytes=649476 secs=1
FILE prices bytes=649476
FILE unknown status=200 bytes=12352702 secs=3
FILE psn bytes=12352702
DAY 2026-10-01 position=LANDED prices=LANDED psn=LANDED secs=51
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=0
FILE unknown status=200 bytes=30026429 secs=10
FILE position bytes=30026429
FILE unknown status=200 bytes=649148 secs=0
FILE prices bytes=649148
FILE unknown status=200 bytes=12335558 secs=3
FILE psn bytes=12335558
DAY 2026-09-30 position=LANDED prices=LANDED psn=LANDED secs=56
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=30021891 secs=11
FILE position bytes=30021891
FILE unknown status=200 bytes=644364 secs=0
FILE prices bytes=644364
FILE unknown status=200 bytes=12313410 secs=3
FILE psn bytes=12313410
DAY 2026-09-29 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29921870 secs=11
FILE position bytes=29921870
FILE unknown status=200 bytes=645757 secs=0
FILE prices bytes=645757
FILE unknown status=200 bytes=12276604 secs=3
FILE psn bytes=12276604
DAY 2026-09-28 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29933318 secs=10
FILE position bytes=29933318
FILE unknown status=200 bytes=650100 secs=0
FILE prices bytes=650100
FILE unknown status=200 bytes=12284282 secs=2
FILE psn bytes=12284282
DAY 2026-09-25 position=LANDED prices=LANDED psn=LANDED secs=55
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29914854 secs=1
FILE position bytes=29914854
FILE unknown status=200 bytes=652274 secs=0
FILE prices bytes=652274
FILE unknown status=200 bytes=12276702 secs=0
FILE psn bytes=12276702
DAY 2026-09-24 position=LANDED prices=LANDED psn=LANDED secs=45
STOP budget wall budget reached before 2026-09-23
CLOSE ok secs=0
OK: histwalk run_id=20261021T155032Z sign_ins=1 stop=budget
exit=0
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

## The walk record (s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/histwalk-20261021T155032Z.json, 3746 bytes)

```
keys: ['caps', 'days', 'finished_at', 'histwalk', 'partial', 'per_type', 'run_error', 'run_id', 'scope', 'sign_ins', 'started_at', 'stop']
histwalk = true
sign_ins = 1
run_error = null
stop = {"evidence": "wall budget reached before 2026-09-23", "reason": "budget"}
run_id = "20261021T155032Z"
started_at = "2026-10-21T15:50:32Z"
finished_at = "2026-10-21T16:05:53Z"
caps = {"max_days": 20, "max_seconds": 900}
per_type = {"position": {"bytes_landed": 452926646, "earliest_landed": "20260924", "empty_days": 0, "landed_days": 15, "skipped_days": 1, "stop_reason": null, "stopped": false}, "prices": {"bytes_landed": 9704438, "earliest_landed": "20260924", "empty_days": 0, "landed_days": 15, "skipped_days": 1, "stop_reason": null, "stopped": false}, "psn": {"bytes_landed": 198226426, "earliest_landed": "20260924", "empty_days": 0, "landed_days": 16, "skipped_days": 0, "stop_reason": null, "stopped": false}}
```

## What the output shows (read from the output only)

- Stop: budget, "wall budget reached before 2026-09-23". The walk covered 16 trading days, 2026-10-15 back to 2026-09-24, at about 45 to 72 s per day, and ended itself with exit 0.
- The type labelled `psn` in the DAY lines is the type `position_balance_fl` (file `position_balance_fl.psn`) in S3; the order calls this type "balances".
- 2026-10-15: position and prices SKIPPED (already landed earlier), psn LANDED. Every later day: position, prices and psn LANDED.
- No type has stopped yet (stop_reason null, empty_days 0 for all three).
- stderr: the calendar WARN only.

## What S3 shows (read-only, 16:07Z): keys written since 15:50Z excluding `_runs/`, 46 in all

| type (S3 prefix) | keys | earliest landed content date | latest landed | bytes |
|---|---|---|---|---|
| position | 15 | 20260924 | 20261014 | 452926646 |
| position_balance_fl | 16 | 20260924 | 20261015 | 198226426 |
| prices | 15 | 20260924 | 20261014 | 9704438 |
